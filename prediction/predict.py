"""
Live Inference
==============
Loads the trained LightGBM models and runs a prediction against the
most recent GTI score + market data.

How it works:
  1. Pull the latest GTI row from gti.db
  2. Pull the last 25 hourly SPY bars from market.db
  3. Compute returns_1h, returns_4h, vol_20h from those bars
  4. Assemble a single feature row matching FEATURE_COLS
  5. Run both models (volatility + direction) to get probabilities
  6. Save the result to predictions.db

Output:
  {
    "timestamp":      "2024-01-15 14:00:00",
    "gti_score":      0.4231,
    "vol_prediction": "HIGH",   ← or "LOW"
    "vol_prob":       0.6812,   ← model confidence
    "dir_prediction": "UP",     ← or "DOWN"
    "dir_prob":       0.5543
  }

Usage:
  python prediction/predict.py
"""

import os
from datetime import datetime

import joblib
import pandas as pd

from config import LGBM_VOL_PATH, LGBM_DIR_PATH, PREDICTIONS_DB, GTI_DB, MARKET_DB
from prediction.features import FEATURE_COLS
from ingestion.db import get_conn


def _load_models():
    """Load both trained models. Raises FileNotFoundError if not trained yet."""
    missing = [p for p in [LGBM_VOL_PATH, LGBM_DIR_PATH] if not os.path.exists(p)]
    if missing:
        raise FileNotFoundError(
            f"Models not found: {missing}\n"
            "Run: python prediction/train.py"
        )
    return joblib.load(LGBM_VOL_PATH), joblib.load(LGBM_DIR_PATH)


def _build_live_features() -> pd.DataFrame:
    """
    Assemble one feature row from the latest GTI score + recent market bars.
    Returns empty DataFrame if there is not enough data.
    """
    # Latest GTI
    conn = get_conn(GTI_DB)
    gti  = conn.execute(
        "SELECT * FROM gti_scores ORDER BY timestamp DESC LIMIT 1"
    ).fetchone()
    conn.close()

    if not gti:
        print("Predict: no GTI data — run gti/aggregator.py first")
        return pd.DataFrame()

    # Last 25 hourly SPY bars (need 20 for vol_20h + buffer)
    conn     = get_conn(MARKET_DB)
    mkt_rows = conn.execute(
        """SELECT open, high, low, close, volume
           FROM ohlcv WHERE symbol='SPY'
           ORDER BY timestamp DESC LIMIT 25"""
    ).fetchall()
    conn.close()

    if len(mkt_rows) < 5:
        print("Predict: not enough market data — run market_fetcher.py first")
        return pd.DataFrame()

    # Reverse so oldest→newest
    mkt_df = pd.DataFrame([dict(r) for r in reversed(mkt_rows)])
    latest = mkt_df.iloc[-1]

    returns_series = mkt_df["close"].pct_change(1)
    returns_1h     = returns_series.iloc[-1]
    returns_4h     = mkt_df["close"].pct_change(min(4, len(mkt_df) - 1)).iloc[-1]
    vol_20h        = returns_series.rolling(min(20, len(mkt_df))).std().iloc[-1]

    row = {
        "gti_score":   float(gti["gti_score"]),
        "conflict_ct": int(gti["conflict_ct"]),
        "avg_tone":    float(gti["avg_tone"]),
        "vader_avg":   float(gti["vader_avg"]),
        "open":        float(latest["open"]),
        "high":        float(latest["high"]),
        "low":         float(latest["low"]),
        "close":       float(latest["close"]),
        "volume":      float(latest["volume"]),
        "returns_1h":  float(returns_1h) if pd.notna(returns_1h) else 0.0,
        "returns_4h":  float(returns_4h) if pd.notna(returns_4h) else 0.0,
        "vol_20h":     float(vol_20h)    if pd.notna(vol_20h)    else 0.01,
    }
    return pd.DataFrame([row])[FEATURE_COLS]


def run_inference() -> dict:
    """Run live prediction. Returns result dict or error dict."""
    try:
        vol_model, dir_model = _load_models()
    except FileNotFoundError as e:
        print(f"Predict: {e}")
        return {"error": str(e)}

    X = _build_live_features()
    if X.empty:
        return {"error": "Insufficient data for inference"}

    vol_prob = float(vol_model.predict_proba(X)[0][1])
    dir_prob = float(dir_model.predict_proba(X)[0][1])
    vol_pred = "HIGH" if vol_prob >= 0.5 else "LOW"
    dir_pred = "UP"   if dir_prob >= 0.5 else "DOWN"

    ts     = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    result = {
        "timestamp":      ts,
        "gti_score":      float(X["gti_score"].iloc[0]),
        "vol_prediction": vol_pred,
        "vol_prob":       round(vol_prob, 4),
        "dir_prediction": dir_pred,
        "dir_prob":       round(dir_prob, 4),
    }

    # Persist to predictions DB
    conn = get_conn(PREDICTIONS_DB)
    conn.execute(
        """INSERT OR REPLACE INTO predictions
           (timestamp, gti_score, vol_prediction, dir_prediction, vol_prob, dir_prob)
           VALUES (?,?,?,?,?,?)""",
        (ts, result["gti_score"], vol_pred, dir_pred,
         result["vol_prob"], result["dir_prob"]),
    )
    conn.commit()
    conn.close()

    print(
        f"Predict [{ts}]  GTI={result['gti_score']:.3f}"
        f"  vol={vol_pred} ({vol_prob:.1%})"
        f"  dir={dir_pred} ({dir_prob:.1%})"
    )
    return result


if __name__ == "__main__":
    import json
    print(json.dumps(run_inference(), indent=2))
