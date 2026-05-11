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


def _build_live_features() -> tuple[pd.DataFrame, dict]:
    """
    Assemble one feature row from the latest GTI score + recent market bars.
    Returns (feature DataFrame, metadata dict) or (empty DataFrame, {}) if not enough data.

    Metadata includes gti_score, close (for outcome resolution).
    """
    # Latest GTI
    conn = get_conn(GTI_DB)
    gti  = conn.execute(
        "SELECT * FROM gti_scores ORDER BY timestamp DESC LIMIT 1"
    ).fetchone()
    conn.close()

    if not gti:
        print("Predict: no GTI data — run gti/aggregator.py first")
        return pd.DataFrame(), {}

    # Last 25 hourly SPY bars (need 20 for vol_20h + buffer), including VIX and GLD
    conn     = get_conn(MARKET_DB)
    mkt_rows = conn.execute(
        """SELECT symbol, open, high, low, close, volume
           FROM ohlcv WHERE symbol IN ('SPY', 'VIX', 'GLD')
           ORDER BY timestamp DESC LIMIT 75"""  # 25 per symbol
    ).fetchall()
    conn.close()

    if not mkt_rows:
        print("Predict: not enough market data — run market_fetcher.py first")
        return pd.DataFrame(), {}

    # Build separate DataFrames per symbol
    mkt_df = pd.DataFrame([dict(r) for r in mkt_rows])

    spy_rows = mkt_df[mkt_df["symbol"] == "SPY"].sort_values("timestamp").tail(25)
    vix_rows = mkt_df[mkt_df["symbol"] == "VIX"].sort_values("timestamp").tail(25)
    gld_rows = mkt_df[mkt_df["symbol"] == "GLD"].sort_values("timestamp").tail(25)

    if len(spy_rows) < 5:
        print("Predict: not enough SPY data")
        return pd.DataFrame(), {}

    spy_latest = spy_rows.iloc[-1]
    vix_latest = vix_rows.iloc[-1] if len(vix_rows) > 0 else None
    gld_latest = gld_rows.iloc[-1] if len(gld_rows) > 0 else None

    # Compute returns and volatility from SPY
    spy_closes = spy_rows["close"].values
    returns_series = pd.Series(spy_closes).pct_change(1)
    returns_1h     = returns_series.iloc[-1]
    returns_4h     = pd.Series(spy_closes).pct_change(4).iloc[-1]
    vol_20h        = returns_series.rolling(min(20, len(returns_series))).std().iloc[-1]

    # Compute VIX and GLD features
    vix_close = float(vix_latest["close"]) if vix_latest is not None else 20.0
    vix_closes = vix_rows["close"].values if len(vix_rows) > 1 else [vix_close]
    # Guard against zero-division (bad VIX data)
    vix_change_1h = 0.0
    if len(vix_closes) > 1 and vix_closes[-2] and vix_closes[-2] != 0:
        vix_change_1h = (vix_closes[-1] - vix_closes[-2]) / vix_closes[-2]

    gld_close = float(gld_latest["close"]) if gld_latest is not None else spy_latest["close"]
    gld_closes = gld_rows["close"].values if len(gld_rows) > 1 else [gld_close]
    # Guard against zero-division (bad GLD data)
    gld_returns_1h = 0.0
    if len(gld_closes) > 1 and gld_closes[-2] and gld_closes[-2] != 0:
        gld_returns_1h = (gld_closes[-1] - gld_closes[-2]) / gld_closes[-2]

    # Time features
    from datetime import datetime as dt
    now = dt.utcnow()
    hour_of_day = now.hour
    day_of_week = now.weekday()

    # Lagged GTI (approximated — assume GTI updated every 15 min, so lag_1 = 15 min ago, lag_4 = 1 hour ago)
    # For live prediction, we use current GTI as a proxy
    gti_lag_1 = float(gti["gti_score"]) * 0.98  # Slight decay approximation
    gti_lag_4 = float(gti["gti_score"]) * 0.96

    # Compute technical indicators for live prediction
    spy_closes = spy_rows["close"].values

    # RSI (14-period simplified)
    if len(spy_closes) >= 14:
        delta = pd.Series(spy_closes).diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        rsi_14 = (100 - (100 / (1 + rs))).iloc[-1]
    else:
        rsi_14 = 50.0

    # MACD (simplified for live)
    if len(spy_closes) >= 26:
        exp1 = pd.Series(spy_closes).ewm(span=12).mean()
        exp2 = pd.Series(spy_closes).ewm(span=26).mean()
        macd_diff = (exp1 - exp2).iloc[-1]
    else:
        macd_diff = 0.0

    # Bollinger Bands
    if len(spy_closes) >= 20:
        sma20 = pd.Series(spy_closes).rolling(20).mean().iloc[-1]
        std20 = pd.Series(spy_closes).rolling(20).std().iloc[-1]
        bb_upper = sma20 + (std20 * 2)
        bb_lower = sma20 - (std20 * 2)
    else:
        bb_upper = spy_latest["high"]
        bb_lower = spy_latest["low"]

    # ATR (14-period simplified)
    if len(spy_rows) >= 14:
        rows_data = spy_rows.tail(14)[["high", "low", "close"]].values
        true_ranges = []
        for i in range(len(rows_data)):
            hl = rows_data[i][0] - rows_data[i][1]
            hc = abs(rows_data[i][0] - (rows_data[i-1][2] if i > 0 else rows_data[i][2]))
            lc = abs(rows_data[i][1] - (rows_data[i-1][2] if i > 0 else rows_data[i][2]))
            true_ranges.append(max(hl, hc, lc))
        atr_14 = sum(true_ranges) / len(true_ranges) / spy_latest["close"]
    else:
        atr_14 = 0.01

    # Volume features
    spy_vol = spy_rows["volume"].values
    if len(spy_vol) >= 20:
        vol_sma = spy_vol[-20:].mean()
        volume_sma_20 = vol_sma / (spy_latest["volume"] + 1)
    else:
        volume_sma_20 = 1.0

    # Momentum
    if len(spy_closes) >= 20:
        price_momentum = (spy_closes[-1] - spy_closes[-20]) / spy_closes[-20]
    else:
        price_momentum = returns_1h

    # VIX percentile
    vix_closes_list = vix_rows["close"].values if len(vix_rows) > 0 else [vix_close]
    if len(vix_closes_list) >= 20:
        vix_min = min(vix_closes_list[-20:])
        vix_max = max(vix_closes_list[-20:])
        vix_percentile = (vix_close - vix_min) / (vix_max - vix_min + 0.01)
    else:
        vix_percentile = 0.5

    row = {
        "gti_score":     float(gti["gti_score"]),
        "conflict_ct":   int(gti["conflict_ct"]),
        "avg_tone":      float(gti["avg_tone"]),
        "vader_avg":     float(gti["vader_avg"]),
        "open":          float(spy_latest["open"]),
        "high":          float(spy_latest["high"]),
        "low":           float(spy_latest["low"]),
        "close":         float(spy_latest["close"]),
        "volume":        float(spy_latest["volume"]),
        "returns_1h":    float(returns_1h) if pd.notna(returns_1h) else 0.0,
        "returns_4h":    float(returns_4h) if pd.notna(returns_4h) else 0.0,
        "vol_20h":       float(vol_20h)    if pd.notna(vol_20h)    else 0.01,
        "vix_close":     float(vix_close),
        "vix_change_1h": float(vix_change_1h),
        "gld_returns_1h": float(gld_returns_1h),
        "hour_of_day":   int(hour_of_day),
        "day_of_week":   int(day_of_week),
        "gti_lag_1":     float(gti_lag_1),
        "gti_lag_4":     float(gti_lag_4),
        "rsi_14":        float(rsi_14),
        "macd_diff":     float(macd_diff),
        "bb_upper":      float(bb_upper),
        "bb_lower":      float(bb_lower),
        "atr_14":        float(atr_14),
        "volume_sma_20": float(volume_sma_20),
        "price_momentum": float(price_momentum),
        "vix_percentile": float(vix_percentile),
    }

    metadata = {
        "gti_score": float(gti["gti_score"]),
        "close": float(spy_latest["close"]),
    }

    return pd.DataFrame([row])[FEATURE_COLS], metadata


def run_inference() -> dict:
    """Run live prediction. Returns result dict or error dict."""
    try:
        vol_model, dir_model = _load_models()
    except FileNotFoundError as e:
        print(f"Predict: {e}")
        return {"error": str(e)}

    X, metadata = _build_live_features()
    if X.empty:
        return {"error": "Insufficient data for inference"}

    vol_prob = float(vol_model.predict_proba(X)[0][1])
    dir_prob = float(dir_model.predict_proba(X)[0][1])
    vol_pred = "HIGH" if vol_prob >= 0.5 else "LOW"
    dir_pred = "UP"   if dir_prob >= 0.5 else "DOWN"

    ts     = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    # Get current model version from registry
    model_version = "unknown"
    registry_path = os.path.join(os.path.dirname(LGBM_VOL_PATH), "model_registry.json")
    if os.path.exists(registry_path):
        import json
        try:
            with open(registry_path, "r") as f:
                registry = json.load(f)
                if registry.get("direction") and len(registry["direction"]) > 0:
                    model_version = registry["direction"][0]["version"]
        except Exception:
            pass

    result = {
        "timestamp":      ts,
        "gti_score":      metadata["gti_score"],
        "vol_prediction": vol_pred,
        "vol_prob":       round(vol_prob, 4),
        "dir_prediction": dir_pred,
        "dir_prob":       round(dir_prob, 4),
        "model_version":  model_version,
    }

    # Persist to predictions DB
    conn = get_conn(PREDICTIONS_DB)
    conn.execute(
        """INSERT OR REPLACE INTO predictions
           (timestamp, gti_score, vol_prediction, dir_prediction, vol_prob, dir_prob, model_version, close)
           VALUES (?,?,?,?,?,?,?,?)""",
        (ts, result["gti_score"], vol_pred, dir_pred,
         result["vol_prob"], result["dir_prob"], model_version, metadata["close"]),
    )
    conn.commit()
    conn.close()

    print(
        f"Predict [{ts}]  GTI={result['gti_score']:.3f}"
        f"  vol={vol_pred} ({vol_prob:.1%})"
        f"  dir={dir_pred} ({dir_prob:.1%})"
        f"  model={model_version}"
    )
    return result


if __name__ == "__main__":
    import json
    print(json.dumps(run_inference(), indent=2))
