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

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import os

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
    Get sector performance (simulated for now).
    In production, would fetch real sector ETF data.
    """
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "sectors": [
            {"name": "Technology", "symbol": "XLK", "change": 1.24, "price": 185.42},
            {"name": "Healthcare", "symbol": "XLV", "change": 0.64, "price": 142.18},
            {"name": "Financials", "symbol": "XLF", "change": -0.32, "price": 38.29},
            {"name": "Energy", "symbol": "XLE", "change": 2.15, "price": 89.53},
            {"name": "Industrials", "symbol": "XLI", "change": 1.82, "price": 102.74},
            {"name": "Consumer Disc.", "symbol": "XLY", "change": -0.18, "price": 74.62},
            {"name": "Materials", "symbol": "XLB", "change": 0.45, "price": 91.23},
            {"name": "Utilities", "symbol": "XLU", "change": -1.23, "price": 71.89},
            {"name": "Real Estate", "symbol": "XLRE", "change": -0.89, "price": 60.41},
            {"name": "Comm. Services", "symbol": "XLC", "change": 0.92, "price": 63.15},
        ],
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


@app.get("/")
def root():
    return {
        "service": "GeoMarket Intelligence API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running",
    }
