"""
FastAPI backend for GeoMarket Intelligence.
Exposes real data endpoints for the Streamlit UI.

Endpoints:
  GET /api/gti              → Current GTI score + components
  GET /api/gti/history     → Last N GTI readings
  GET /api/signals         → Current ML predictions + volatility
  GET /api/headlines       → Latest headlines with sentiment
  GET /api/market/spy      → S&P 500 OHLCV + technicals
  GET /api/market/sectors  → Sector performance
  GET /health              → Server health check

Run: uvicorn api.main:app --reload
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import os
import json
import asyncio
import sys
from typing import List

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import GTI_DB, NEWS_DB, MARKET_DB, PREDICTIONS_DB
from gti.aggregator import compute_gti
from prediction.predict import run_inference
from ingestion.db import get_conn, db_transaction

llm_settings = {
    "llm_enabled": os.getenv("USE_LLM_SENTIMENT", "false").lower() == "true",
    "llm_provider": os.getenv("LLM_PROVIDER", "none"),
}

app = FastAPI(title="GeoMarket Intelligence API", version="1.0.0")

allowed_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


# ────────────────────────────────────────────────────────────────────────────
# WebSocket Connection Manager
# ────────────────────────────────────────────────────────────────────────────

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, List[WebSocket]] = {
            "gti": [],
            "market": [],
            "signals": []
        }

    async def connect(self, websocket: WebSocket, channel: str):
        await websocket.accept()
        if channel not in self.active_connections:
            self.active_connections[channel] = []
        self.active_connections[channel].append(websocket)

    def disconnect(self, websocket: WebSocket, channel: str):
        if channel in self.active_connections and websocket in self.active_connections[channel]:
            self.active_connections[channel].remove(websocket)

    async def broadcast(self, message: dict, channel: str):
        dead_connections = []
        for connection in self.active_connections.get(channel, []):
            try:
                await connection.send_json(message)
            except Exception:
                dead_connections.append(connection)

        for connection in dead_connections:
            self.disconnect(connection, channel)


manager = ConnectionManager()


# Broadcast functions (called by scheduler)
async def broadcast_gti_update(gti_data: dict):
    """Broadcast GTI update to all connected clients."""
    await manager.broadcast({"type": "gti_update", "data": gti_data}, "gti")


async def broadcast_market_update(market_data: dict):
    """Broadcast market update to all connected clients."""
    await manager.broadcast({"type": "market_update", "data": market_data}, "market")


async def broadcast_signals_update(signals_data: dict):
    """Broadcast signals update to all connected clients."""
    await manager.broadcast({"type": "signals_update", "data": signals_data}, "signals")


# ────────────────────────────────────────────────────────────────────────────
# GTI Endpoints
# ────────────────────────────────────────────────────────────────────────────

@app.get("/api/gti")
def get_gti_current():
    """
    Get the current GTI score and its three components.
    If no recent data, compute fresh (will use defaults if no source data available).
    """
    try:
        with db_transaction(GTI_DB) as conn:
            row = conn.execute(
                "SELECT * FROM gti_scores ORDER BY timestamp DESC LIMIT 1"
            ).fetchone()

        if row:
            gti_score = float(row["gti_score"])
            regime = row["regime"] if row["regime"] else "neutral"
            conflict_ct = int(row["conflict_ct"])
            avg_tone = float(row["avg_tone"])
            vader_avg = float(row["vader_avg"])
        else:
            # Compute fresh if none in DB — will return defaults if no source data
            result = compute_gti()
            gti_score = result["gti_score"]
            regime = result.get("regime", "neutral")
            conflict_ct = result.get("conflict_ct", 0)
            avg_tone = result.get("avg_tone", 0.0)
            vader_avg = result.get("vader_avg", 0.0)

        if gti_score < 0.3:
            risk_level = "LOW_CONFLICT"
        elif gti_score < 0.6:
            risk_level = "MODERATE_TENSION"
        else:
            risk_level = "HIGH_CONFLICT"

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "score": round(gti_score, 4),
            "risk_level": risk_level,
            "regime": regime,
            "sentiment": round(vader_avg, 4),
            "volatility": round(avg_tone, 4),
            "conflict_count": conflict_ct,
            "peaceful_count": max(0, 100 - conflict_ct),
            "conflict_ratio": round(conflict_ct / max(1, 100), 4),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/gti/history")
def get_gti_history(hours: int = 48):
    """Get GTI history for the last N hours."""
    try:
        cutoff = (datetime.utcnow() - timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M:%S")
        with db_transaction(GTI_DB) as conn:
            rows = conn.execute(
                "SELECT timestamp, gti_score FROM gti_scores WHERE timestamp >= ? ORDER BY timestamp ASC",
                (cutoff,),
            ).fetchall()

        return {
            "history": [
                {
                    "timestamp": r["timestamp"],
                    "score": float(r["gti_score"]),
                    "risk_level": "LOW_CONFLICT" if float(r["gti_score"]) < 0.3 else "MODERATE_TENSION" if float(r["gti_score"]) < 0.6 else "HIGH_CONFLICT",
                }
                for r in rows
            ],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ────────────────────────────────────────────────────────────────────────────
# Prediction/Signal Endpoints
# ────────────────────────────────────────────────────────────────────────────

@app.get("/api/signals")
def get_signals_current():
    """
    Get the latest ML predictions for volatility and direction.
    If models not ready, return clear status message.
    """
    try:
        result = run_inference()

        if "error" in result:
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "status": "AWAITING_DATA",
                "vol_prediction": "UNKNOWN",
                "vol_prob": 0.0,
                "dir_prediction": "UNKNOWN",
                "dir_prob": 0.0,
                "narrative": result.get("error", "Models training or data backfilling in progress"),
                "regime": "neutral",
                "regime_confidence": 0.0,
                "entities": [],
            }

        # Get latest GTI for regime context
        regime = "neutral"
        regime_confidence = 0.5
        try:
            with db_transaction(GTI_DB) as conn:
                gti_row = conn.execute(
                    "SELECT regime FROM gti_scores ORDER BY timestamp DESC LIMIT 1"
                ).fetchone()
            if gti_row and gti_row["regime"]:
                regime = gti_row["regime"]
        except Exception:
            pass

        # Try to get entities from recent headlines (optional)
        entities = []
        try:
            with db_transaction(NEWS_DB) as conn:
                headlines = conn.execute(
                    """SELECT title FROM rss_articles
                       WHERE fetched_at >= datetime('now', '-1 hour')
                       ORDER BY fetched_at DESC LIMIT 5"""
                ).fetchall()
            if headlines and llm_settings.get("llm_enabled"):
                try:
                    from nlp.llm_sentiment import get_llm_analysis
                    headline_texts = [h["title"] for h in headlines]
                    llm_analysis = get_llm_analysis(headline_texts)
                    entities = llm_analysis.entities or []
                    regime_confidence = llm_analysis.confidence
                except Exception:
                    pass
        except Exception:
            pass

        # Build narrative from prediction + regime
        narrative = f"Direction: {result['dir_prediction']} ({result['dir_prob']:.1%}). "
        narrative += f"Volatility: {result['vol_prediction']} ({result['vol_prob']:.1%}). "
        narrative += f"Regime: {regime} ({regime_confidence:.0%} confidence)."
        if entities:
            narrative += f" Key topics: {', '.join(str(e) for e in entities[:3])}."

        return {
            "timestamp": result.get("timestamp", datetime.utcnow().isoformat()),
            "status": "LIVE",
            "gti_score": round(result.get("gti_score", 0.5), 4),
            "vol_prediction": result["vol_prediction"],
            "vol_prob": round(result["vol_prob"], 4),
            "dir_prediction": result["dir_prediction"],
            "dir_prob": round(result["dir_prob"], 4),
            "model_version": result.get("model_version", "unknown"),
            "narrative": narrative,
            "regime": regime,
            "regime_confidence": round(regime_confidence, 2),
            "entities": entities,
        }
    except Exception as e:
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "status": "ERROR",
            "error": str(e),
            "vol_prediction": "ERROR",
            "dir_prediction": "ERROR",
            "vol_prob": 0.0,
            "dir_prob": 0.0,
        }


@app.get("/api/signals/history")
def get_signals_history(limit: int = 100):
    """Get prediction history from the DB."""
    try:
        conn = get_conn(PREDICTIONS_DB)
        rows = conn.execute(
            "SELECT * FROM predictions ORDER BY timestamp DESC LIMIT ?",
            (limit,),
        ).fetchall()
        conn.close()

        return {
            "total": len(rows),
            "data": [
                {
                    "timestamp": r["timestamp"],
                    "gti_score": float(r["gti_score"]),
                    "vol_prediction": r["vol_prediction"],
                    "vol_prob": float(r["vol_prob"]),
                    "dir_prediction": r["dir_prediction"],
                    "dir_prob": float(r["dir_prob"]),
                }
                for r in reversed(rows)
            ],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ────────────────────────────────────────────────────────────────────────────
# Headlines & Sentiment
# ────────────────────────────────────────────────────────────────────────────

@app.get("/api/headlines")
def get_headlines(limit: int = 20):
    """
    Get latest RSS headlines with sentiment scores.
    """
    try:
        cutoff = (datetime.utcnow() - timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S")
        with db_transaction(NEWS_DB) as conn:
            rows = conn.execute(
                """
                SELECT published_at, title, source, vader_compound
                FROM rss_articles
                WHERE fetched_at >= ?
                ORDER BY fetched_at DESC
                LIMIT ?
                """,
                (cutoff, limit),
            ).fetchall()

        headlines = []
        for r in rows:
            compound = float(r["vader_compound"]) if r["vader_compound"] else 0.0
            if compound < -0.05:
                sentiment = "negative"
                score_display = f"{compound:.2f}"
            elif compound > 0.05:
                sentiment = "positive"
                score_display = f"+{compound:.2f}"
            else:
                sentiment = "neutral"
                score_display = f"{compound:.2f}"

            headlines.append({
                "timestamp": r["published_at"],
                "title": r["title"],
                "source": r["source"],
                "sentiment": sentiment,
                "compound_score": compound,
                "display_score": score_display,
            })

        return {
            "headlines": headlines,
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ────────────────────────────────────────────────────────────────────────────
# Market Data
# ────────────────────────────────────────────────────────────────────────────

@app.get("/api/market/spy")
def get_market_spy(bars: int = 100):
    """
    Get recent S&P 500 OHLCV bars.
    Returns mock data if DB is empty (awaiting scheduler to backfill).
    """
    try:
        with db_transaction(MARKET_DB) as conn:
            rows = conn.execute(
                """
                SELECT timestamp, open, high, low, close, volume
                FROM ohlcv
                WHERE symbol='SPY'
                ORDER BY timestamp ASC
                LIMIT ?
                """,
                (bars,),
            ).fetchall()

        if not rows:
            # Return live-like data structure with placeholder
            return {
                "bars": [],
                "current_price": 0.0,
                "daily_change_pct": 0.0,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "awaiting_data",
                "message": "Scheduler backfilling market data — check /api/diagnostic",
            }

        data = [
            {
                "timestamp": r["timestamp"],
                "open": float(r["open"]),
                "high": float(r["high"]),
                "low": float(r["low"]),
                "close": float(r["close"]),
                "volume": int(r["volume"]),
            }
            for r in rows
        ]

        latest = data[-1]
        prev = data[-2] if len(data) > 1 else latest

        return {
            "bars": data,
            "current_price": round(latest["close"], 2),
            "daily_change_pct": round(
                ((latest["close"] - prev["close"]) / prev["close"]) * 100, 2
            ) if prev["close"] > 0 else 0.0,
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/market/sectors")
def get_market_sectors():
    """
    Get sector performance from real market data.
    Returns placeholder if data not yet available.
    """
    try:
        sector_symbols = ["XLK", "XLV", "XLF", "XLE", "XLI", "XLY", "XLB", "XLU", "XLRE", "XLC"]
        sector_names = {
            "XLK": "Technology", "XLV": "Healthcare", "XLF": "Financials",
            "XLE": "Energy", "XLI": "Industrials", "XLY": "Consumer Disc.",
            "XLB": "Materials", "XLU": "Utilities", "XLRE": "Real Estate", "XLC": "Comm. Services"
        }
        sectors = []

        with db_transaction(MARKET_DB) as conn:
            for symbol in sector_symbols:
                rows = conn.execute(
                    "SELECT close, timestamp FROM ohlcv WHERE symbol=? ORDER BY timestamp DESC LIMIT 2",
                    (symbol,),
                ).fetchall()

                if rows and len(rows) >= 2:
                    current = float(rows[0]["close"])
                    prev = float(rows[1]["close"])
                    change = ((current - prev) / prev) * 100 if prev > 0 else 0
                else:
                    current = 0.0
                    change = 0.0

                sectors.append({
                    "name": sector_names.get(symbol, symbol),
                    "symbol": symbol,
                    "change": round(change, 2),
                    "price": round(current, 2),
                })

        has_data = any(s["price"] > 0 for s in sectors)

        return {
            "sectors": [
                {
                    "name": s["name"],
                    "performance": s["price"],
                    "change_pct": s["change"],
                }
                for s in sectors
            ],
            "timestamp": datetime.utcnow().isoformat(),
            "status": "live" if has_data else "awaiting_data",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ────────────────────────────────────────────────────────────────────────────
# Geopolitical Intelligence Endpoints
# ────────────────────────────────────────────────────────────────────────────

@app.get("/api/conflicts")
def get_conflicts(limit: int = 15):
    """
    Get active conflict countries/regions with severity scores.
    Data sourced from GDELT events.
    """
    try:
        with db_transaction(GTI_DB) as conn:
            rows = conn.execute(
                """
                SELECT country_code, conflict_count, avg_goldstein, latest_event_time
                FROM conflict_summary
                ORDER BY conflict_count DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()

        if not rows:
            return {"total": 0, "data": []}

        conflicts = []
        for r in rows:
            goldstein = float(r["avg_goldstein"]) if r["avg_goldstein"] else -5.0
            if goldstein < -5.0:
                severity = "CRITICAL"
                severity_score = 0.9
            elif goldstein < -2.0:
                severity = "ELEVATED"
                severity_score = 0.6
            else:
                severity = "STABLE"
                severity_score = 0.3

            conflicts.append({
                "country_code": r["country_code"],
                "event_count": int(r["conflict_count"]),
                "severity": severity,
                "severity_score": severity_score,
                "avg_goldstein": round(goldstein, 2),
                "latest_event": r["latest_event_time"],
            })

        return {
            "conflicts": [
                {
                    "country": c["country_code"],
                    "count": c["event_count"],
                    "severity": c["severity"].lower(),
                }
                for c in conflicts
            ],
            "total_events": sum(c["event_count"] for c in conflicts),
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        return {
            "conflicts": [],
            "total_events": 0,
            "timestamp": datetime.utcnow().isoformat(),
        }


@app.get("/api/bilateral")
def get_bilateral_relations(limit: int = 10):
    """
    Get bilateral geopolitical relationships and their stress levels.
    """
    try:
        with db_transaction(GTI_DB) as conn:
            rows = conn.execute(
                """
                SELECT actor1, actor2, relation_count, avg_goldstein, latest_time
                FROM bilateral_summary
                ORDER BY relation_count DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()

        if not rows:
            return {"total": 0, "data": []}

        relations = []
        for r in rows:
            goldstein = float(r["avg_goldstein"]) if r["avg_goldstein"] else 0.0
            stress = min(100, max(0, (-(goldstein - 5.0)) * 10))

            relations.append({
                "pair": f"{r['actor1']} ↔ {r['actor2']}",
                "event_count": int(r["relation_count"]),
                "stress_level": round(stress, 1),
                "avg_goldstein": round(goldstein, 2),
                "latest_event": r["latest_time"],
            })

        return {
            "relations": [
                {
                    "country1": r["pair"].split(" ↔ ")[0],
                    "country2": r["pair"].split(" ↔ ")[1] if " ↔ " in r["pair"] else "",
                    "stress_level": r["stress_level"],
                    "stress_category": "critical" if r["stress_level"] > 70 else "tense" if r["stress_level"] > 40 else "stable",
                    "recent_events": r["event_count"],
                }
                for r in relations
            ],
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        return {
            "relations": [],
            "timestamp": datetime.utcnow().isoformat(),
        }


@app.get("/api/events")
def get_recent_events(event_type: str = "all", limit: int = 20):
    """
    Get recent geopolitical events with location coordinates.
    Supports filtering by event_type: conflict, diplomatic, economic, or all.
    """
    try:
        if event_type == "conflict":
            query = "SELECT * FROM gdelt_events WHERE goldstein_scale < -5.0 ORDER BY event_date DESC LIMIT ?"
        elif event_type == "diplomatic":
            query = "SELECT * FROM gdelt_events WHERE cameo_code BETWEEN 50 AND 90 ORDER BY event_date DESC LIMIT ?"
        elif event_type == "economic":
            query = "SELECT * FROM gdelt_events WHERE cameo_code BETWEEN 100 AND 110 ORDER BY event_date DESC LIMIT ?"
        else:
            query = "SELECT * FROM gdelt_events ORDER BY event_date DESC LIMIT ?"

        with db_transaction(GTI_DB) as conn:
            rows = conn.execute(query, (limit,)).fetchall()

        events = []
        for r in rows:
            events.append({
                "event_id": r["event_id"],
                "date": r["event_date"],
                "actor1": r["actor1_countrycode"],
                "actor2": r["actor2_countrycode"],
                "latitude": float(r["latitude"]) if r["latitude"] else None,
                "longitude": float(r["longitude"]) if r["longitude"] else None,
                "goldstein_scale": float(r["goldstein_scale"]),
                "article_count": int(r["num_articles"]),
                "avg_tone": float(r["avg_tone"]) if r["avg_tone"] else 0.0,
            })

        return {
            "events": [
                {
                    "event_id": e["event_id"],
                    "event_type": event_type,
                    "country": e["actor1"],
                    "location": "",
                    "latitude": e["latitude"],
                    "longitude": e["longitude"],
                    "event_code": e["goldstein_scale"],
                    "goldstein_scale": e["goldstein_scale"],
                    "timestamp": e["date"],
                }
                for e in events
            ],
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        return {
            "events": [],
            "timestamp": datetime.utcnow().isoformat(),
        }


# ────────────────────────────────────────────────────────────────────────────
# Settings
# ────────────────────────────────────────────────────────────────────────────

@app.post("/api/settings/llm")
def update_llm_settings(llm_enabled: bool = None, llm_provider: str = None):
    """
    Update LLM settings. Settings are stored in-memory and persisted via env vars.
    Frontend can toggle LLM on/off and select provider (ollama, huggingface).
    """
    try:
        global llm_settings
        if llm_enabled is not None:
            llm_settings["llm_enabled"] = llm_enabled
        if llm_provider is not None and llm_provider in ["ollama", "huggingface", "none"]:
            llm_settings["llm_provider"] = llm_provider

        return {
            "status": "success",
            "llm_enabled": llm_settings["llm_enabled"],
            "llm_provider": llm_settings["llm_provider"],
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/settings/llm")
def get_llm_settings():
    """Get current LLM settings."""
    return {
        "llm_enabled": llm_settings["llm_enabled"],
        "llm_provider": llm_settings["llm_provider"],
        "timestamp": datetime.utcnow().isoformat(),
    }


# ────────────────────────────────────────────────────────────────────────────
# Health Check
# ────────────────────────────────────────────────────────────────────────────

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
    }


@app.get("/api/diagnostic")
def get_diagnostic_status():
    """
    Diagnostic endpoint showing data availability and system readiness.
    Shows row counts for each database table and identifies missing data.
    """
    diagnostics = {
        "timestamp": datetime.utcnow().isoformat(),
        "data_availability": {},
        "models": {},
        "issues": [],
    }

    # GTI data
    try:
        with db_transaction(GTI_DB) as conn:
            gti_count = conn.execute("SELECT COUNT(*) as cnt FROM gti_scores").fetchone()["cnt"]
            gdelt_count = conn.execute("SELECT COUNT(*) as cnt FROM gdelt_events").fetchone()["cnt"]
            diagnostics["data_availability"]["gti_scores"] = gti_count
            diagnostics["data_availability"]["gdelt_events"] = gdelt_count
            if gti_count == 0:
                diagnostics["issues"].append("No GTI scores yet — scheduler not running or no data ingested")
            if gdelt_count == 0:
                diagnostics["issues"].append("No GDELT events — geopolitical data not backfilled")
    except Exception as e:
        diagnostics["issues"].append(f"GTI DB error: {e}")

    # Market data
    try:
        with db_transaction(MARKET_DB) as conn:
            spy_count = conn.execute("SELECT COUNT(*) as cnt FROM ohlcv WHERE symbol='SPY'").fetchone()["cnt"]
            vix_count = conn.execute("SELECT COUNT(*) as cnt FROM ohlcv WHERE symbol='VIX'").fetchone()["cnt"]
            diagnostics["data_availability"]["spy_bars"] = spy_count
            diagnostics["data_availability"]["vix_bars"] = vix_count
            if spy_count == 0:
                diagnostics["issues"].append("No SPY data — market data not backfilled")
            if vix_count == 0:
                diagnostics["issues"].append("No VIX data — volatility index not available")
    except Exception as e:
        diagnostics["issues"].append(f"Market DB error: {e}")

    # News data
    try:
        with db_transaction(NEWS_DB) as conn:
            rss_count = conn.execute("SELECT COUNT(*) as cnt FROM rss_articles").fetchone()["cnt"]
            diagnostics["data_availability"]["rss_articles"] = rss_count
            if rss_count == 0:
                diagnostics["issues"].append("No RSS articles — news data not ingested")
    except Exception as e:
        diagnostics["issues"].append(f"News DB error: {e}")

    # Predictions
    try:
        with db_transaction(PREDICTIONS_DB) as conn:
            pred_count = conn.execute("SELECT COUNT(*) as cnt FROM predictions").fetchone()["cnt"]
            diagnostics["data_availability"]["predictions"] = pred_count
    except Exception as e:
        diagnostics["issues"].append(f"Predictions DB error: {e}")

    # Model status
    import os
    from config import LGBM_VOL_PATH, LGBM_DIR_PATH

    vol_exists = os.path.exists(LGBM_VOL_PATH)
    dir_exists = os.path.exists(LGBM_DIR_PATH)
    diagnostics["models"]["volatility"] = "trained" if vol_exists else "missing"
    diagnostics["models"]["direction"] = "trained" if dir_exists else "missing"

    if not (vol_exists and dir_exists):
        diagnostics["issues"].append("Models not trained — run: python prediction/train.py")

    # Summary
    diagnostics["status"] = "ready" if not diagnostics["issues"] else "incomplete"
    diagnostics["data_ready"] = (
        diagnostics["data_availability"].get("gti_scores", 0) > 0 and
        diagnostics["data_availability"].get("spy_bars", 0) > 0
    )

    return diagnostics


@app.get("/")
def root():
    return {
        "service": "GeoMarket Intelligence API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running",
    }


# ────────────────────────────────────────────────────────────────────────────
# WebSocket Endpoints
# ────────────────────────────────────────────────────────────────────────────

@app.websocket("/ws/gti")
async def websocket_gti(websocket: WebSocket):
    """WebSocket endpoint for GTI real-time updates."""
    await manager.connect(websocket, "gti")
    try:
        while True:
            # Send current GTI data immediately on connect
            gti_data = get_gti_current()
            await websocket.send_json({"type": "gti_update", "data": gti_data})
            # Keep connection alive
            await asyncio.sleep(60)
    except WebSocketDisconnect:
        manager.disconnect(websocket, "gti")
    except Exception:
        manager.disconnect(websocket, "gti")


@app.websocket("/ws/market")
async def websocket_market(websocket: WebSocket):
    """WebSocket endpoint for market real-time updates."""
    await manager.connect(websocket, "market")
    try:
        while True:
            market_data = get_market_spy(bars=100)
            await websocket.send_json({"type": "market_update", "data": market_data})
            await asyncio.sleep(60)
    except WebSocketDisconnect:
        manager.disconnect(websocket, "market")
    except Exception:
        manager.disconnect(websocket, "market")


@app.websocket("/ws/signals")
async def websocket_signals(websocket: WebSocket):
    """WebSocket endpoint for ML signals real-time updates."""
    await manager.connect(websocket, "signals")
    try:
        while True:
            signals_data = get_signals_current()
            await websocket.send_json({"type": "signals_update", "data": signals_data})
            await asyncio.sleep(60)
    except WebSocketDisconnect:
        manager.disconnect(websocket, "signals")
    except Exception:
        manager.disconnect(websocket, "signals")
