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
from typing import List

from config import GTI_DB, NEWS_DB, MARKET_DB, PREDICTIONS_DB
from gti.aggregator import compute_gti
from prediction.predict import run_inference
from ingestion.db import get_conn

app = FastAPI(title="GeoMarket Intelligence API", version="1.0.0")

# Enable CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
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
    If no recent data, compute fresh.
    """
    try:
        conn = get_conn(GTI_DB)
        row = conn.execute(
            "SELECT * FROM gti_scores ORDER BY timestamp DESC LIMIT 1"
        ).fetchone()
        conn.close()

        if row:
            gti_score = float(row["gti_score"])
        else:
            # Compute fresh if none in DB
            result = compute_gti()
            gti_score = result["gti_score"]

        # Determine risk level
        if gti_score < 0.3:
            risk_level = "LOW_CONFLICT"
        elif gti_score < 0.6:
            risk_level = "MODERATE_TENSION"
        else:
            risk_level = "HIGH_CONFLICT"

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "gti_score": round(gti_score, 4),
            "risk_level": risk_level,
            "conflict_ratio": float(row["conflict_ct"]) / max(1, 100) if row else 0.5,
            "tone_index": float(row["avg_tone"]) if row else 0.0,
            "vader_sentiment": float(row["vader_avg"]) if row else 0.0,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/gti/history")
def get_gti_history(hours: int = 48):
    """Get GTI history for the last N hours."""
    try:
        cutoff = (datetime.utcnow() - timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M:%S")
        conn = get_conn(GTI_DB)
        rows = conn.execute(
            "SELECT timestamp, gti_score FROM gti_scores WHERE timestamp >= ? ORDER BY timestamp ASC",
            (cutoff,),
        ).fetchall()
        conn.close()

        return {
            "hours": hours,
            "data": [
                {
                    "timestamp": r["timestamp"],
                    "gti_score": float(r["gti_score"]),
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
    If models not trained, return mock predictions.
    """
    try:
        result = run_inference()
        if "error" in result:
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "status": "SIMULATION_MODE",
                "vol_prediction": "VARIABLE",
                "vol_prob": 0.5,
                "dir_prediction": "BULLISH",
                "dir_prob": 0.3,
                "message": "Models not trained yet",
            }
        return {
            "timestamp": result.get("timestamp", datetime.utcnow().isoformat()),
            "status": "LIVE",
            "gti_score": result["gti_score"],
            "vol_prediction": result["vol_prediction"],
            "vol_prob": result["vol_prob"],
            "dir_prediction": result["dir_prediction"],
            "dir_prob": result["dir_prob"],
        }
    except Exception as e:
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "status": "ERROR",
            "error": str(e),
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
        conn = get_conn(NEWS_DB)
        rows = conn.execute(
            """
            SELECT timestamp, title, source, vader_compound
            FROM rss_articles
            WHERE fetched_at >= ?
            ORDER BY fetched_at DESC
            LIMIT ?
            """,
            (cutoff, limit),
        ).fetchall()
        conn.close()

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
                "timestamp": r["timestamp"],
                "title": r["title"],
                "source": r["source"],
                "sentiment": sentiment,
                "compound_score": compound,
                "display_score": score_display,
            })

        return {
            "total": len(headlines),
            "data": headlines,
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
    """
    try:
        conn = get_conn(MARKET_DB)
        rows = conn.execute(
            """
            SELECT timestamp, open, high, low, close, volume
            FROM ohlcv
            WHERE symbol='SPY'
            ORDER BY timestamp DESC
            LIMIT ?
            """,
            (bars,),
        ).fetchall()
        conn.close()

        if not rows:
            return {"error": "No SPY data", "data": []}

        data = [
            {
                "timestamp": r["timestamp"],
                "open": float(r["open"]),
                "high": float(r["high"]),
                "low": float(r["low"]),
                "close": float(r["close"]),
                "volume": int(r["volume"]),
            }
            for r in reversed(rows)
        ]

        latest = data[-1]
        prev = data[-2] if len(data) > 1 else latest

        return {
            "symbol": "SPY",
            "current_price": latest["close"],
            "daily_change": round(
                ((latest["close"] - prev["close"]) / prev["close"]) * 100, 2
            ),
            "bars": len(data),
            "data": data,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/market/sectors")
def get_market_sectors():
    """
    Get sector performance from real market data.
    """
    try:
        conn = get_conn(MARKET_DB)
        sector_symbols = ["XLK", "XLV", "XLF", "XLE", "XLI", "XLY", "XLB", "XLU", "XLRE", "XLC"]
        sectors = []

        for symbol in sector_symbols:
            row = conn.execute(
                "SELECT close, timestamp FROM ohlcv WHERE symbol=? ORDER BY timestamp DESC LIMIT 2",
                (symbol,),
            ).fetchall()

            if row and len(row) >= 2:
                current = float(row[0]["close"])
                prev = float(row[1]["close"])
                change = ((current - prev) / prev) * 100 if prev > 0 else 0
            else:
                current = 0
                change = 0

            sector_names = {
                "XLK": "Technology", "XLV": "Healthcare", "XLF": "Financials",
                "XLE": "Energy", "XLI": "Industrials", "XLY": "Consumer Disc.",
                "XLB": "Materials", "XLU": "Utilities", "XLRE": "Real Estate", "XLC": "Comm. Services"
            }

            sectors.append({
                "name": sector_names.get(symbol, symbol),
                "symbol": symbol,
                "change": round(change, 2),
                "price": round(current, 2),
            })

        conn.close()
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "sectors": sectors,
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
        conn = get_conn(GTI_DB)
        rows = conn.execute(
            """
            SELECT country_code, conflict_count, avg_goldstein, latest_event_time
            FROM conflict_summary
            ORDER BY conflict_count DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        conn.close()

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

        return {"total": len(conflicts), "data": conflicts}
    except Exception as e:
        return {"error": str(e), "data": []}


@app.get("/api/bilateral")
def get_bilateral_relations(limit: int = 10):
    """
    Get bilateral geopolitical relationships and their stress levels.
    """
    try:
        conn = get_conn(GTI_DB)
        rows = conn.execute(
            """
            SELECT actor1, actor2, relation_count, avg_goldstein, latest_time
            FROM bilateral_summary
            ORDER BY relation_count DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        conn.close()

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

        return {"total": len(relations), "data": relations}
    except Exception as e:
        return {"error": str(e), "data": []}


@app.get("/api/events")
def get_recent_events(event_type: str = "all", limit: int = 20):
    """
    Get recent geopolitical events with location coordinates.
    Supports filtering by event_type: conflict, diplomatic, economic, or all.
    """
    try:
        conn = get_conn(GTI_DB)

        if event_type == "conflict":
            query = "SELECT * FROM gdelt_events WHERE goldstein_scale < -5.0 ORDER BY event_date DESC LIMIT ?"
        elif event_type == "diplomatic":
            query = "SELECT * FROM gdelt_events WHERE cameo_code BETWEEN 50 AND 90 ORDER BY event_date DESC LIMIT ?"
        elif event_type == "economic":
            query = "SELECT * FROM gdelt_events WHERE cameo_code BETWEEN 100 AND 110 ORDER BY event_date DESC LIMIT ?"
        else:
            query = "SELECT * FROM gdelt_events ORDER BY event_date DESC LIMIT ?"

        rows = conn.execute(query, (limit,)).fetchall()
        conn.close()

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

        return {"total": len(events), "event_type": event_type, "data": events}
    except Exception as e:
        return {"error": str(e), "data": []}


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
