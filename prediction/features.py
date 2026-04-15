"""
Feature Engineering
===================
Joins GTI scores with hourly market OHLCV data to produce a feature matrix
that LightGBM can train and predict on.

Features produced:
  From GTI:
    gti_score    — current tension level (0.0–1.0)
    conflict_ct  — number of conflict events in the GTI window
    avg_tone     — average GDELT media tone
    vader_avg    — average RSS headline sentiment

  From market data (SPY by default):
    open, high, low, close, volume
    returns_1h   — 1-hour price return
    returns_4h   — 4-hour price return
    vol_20h      — 20-hour rolling volatility (std of hourly returns)

Targets (what we're predicting, shifted -1 = next hour):
  target_vol  — 1 if next-hour absolute return > 20h rolling vol (high vol)
  target_dir  — 1 if next-hour close > current close (price goes up)

Alignment:
  GTI scores and market bars are both rounded to the hour and inner-joined,
  so every feature row has both a GTI score and a matching market bar.
"""

from datetime import datetime, timedelta

import pandas as pd

from config import GTI_DB, MARKET_DB, MAX_ROWS
from ingestion.db import get_conn

# These are the columns LightGBM will train on
FEATURE_COLS = [
    "gti_score",
    "conflict_ct",
    "avg_tone",
    "vader_avg",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "returns_1h",
    "returns_4h",
    "vol_20h",
]


def build_feature_matrix(
    symbol: str = "SPY",
    lookback_days: int = 30,
) -> pd.DataFrame:
    """
    Build a feature matrix aligned by hour.

    Parameters
    ----------
    symbol       : market symbol to use for OHLCV (default: SPY)
    lookback_days: how many days of history to include

    Returns
    -------
    pd.DataFrame with FEATURE_COLS + target_vol + target_dir columns.
    Empty DataFrame if there is not enough data.
    """
    cutoff = (
        datetime.utcnow() - timedelta(days=lookback_days)
    ).strftime("%Y-%m-%d %H:%M:%S")

    # ── Load GTI ─────────────────────────────────────────────────────────
    conn     = get_conn(GTI_DB)
    gti_rows = conn.execute(
        f"""SELECT timestamp, gti_score, conflict_ct, avg_tone, vader_avg
            FROM gti_scores
            WHERE timestamp >= ?
            ORDER BY timestamp
            LIMIT {MAX_ROWS}""",
        (cutoff,),
    ).fetchall()
    conn.close()

    # ── Load OHLCV ────────────────────────────────────────────────────────
    conn     = get_conn(MARKET_DB)
    mkt_rows = conn.execute(
        f"""SELECT timestamp, open, high, low, close, volume
            FROM ohlcv
            WHERE symbol = ? AND timestamp >= ?
            ORDER BY timestamp
            LIMIT {MAX_ROWS}""",
        (symbol, cutoff),
    ).fetchall()
    conn.close()

    if not gti_rows or not mkt_rows:
        print("Features: not enough data — run backfill first")
        return pd.DataFrame()

    gti_df = pd.DataFrame([dict(r) for r in gti_rows])
    mkt_df = pd.DataFrame([dict(r) for r in mkt_rows])

    gti_df["timestamp"] = pd.to_datetime(gti_df["timestamp"])
    mkt_df["timestamp"] = pd.to_datetime(mkt_df["timestamp"])

    # Round to hour so both series align cleanly
    gti_df["hour"] = gti_df["timestamp"].dt.floor("h")
    mkt_df["hour"] = mkt_df["timestamp"].dt.floor("h")

    # Keep only the latest GTI reading per hour (in case of duplicates)
    gti_df = (
        gti_df.sort_values("timestamp")
        .drop_duplicates("hour", keep="last")
    )

    # Merge on hour
    df = pd.merge(
        mkt_df,
        gti_df[["hour", "gti_score", "conflict_ct", "avg_tone", "vader_avg"]],
        on="hour",
        how="inner",
    )
    df = df.sort_values("hour").reset_index(drop=True)

    if df.empty:
        print("Features: GTI and market data don't overlap — check timestamps")
        return pd.DataFrame()

    # ── Engineered market features ────────────────────────────────────────
    df["returns_1h"] = df["close"].pct_change(1)
    df["returns_4h"] = df["close"].pct_change(4)
    df["vol_20h"]    = df["returns_1h"].rolling(20, min_periods=20).std()

    # ── Targets (next-hour prediction) ────────────────────────────────────
    next_close       = df["close"].shift(-1)
    next_returns     = df["returns_1h"].shift(-1).abs()
    df["target_dir"] = (next_close > df["close"]).astype(int)
    df["target_vol"] = (next_returns > df["vol_20h"]).astype(int)

    # Drop rows with NaN in features or targets
    df = df.dropna(subset=FEATURE_COLS + ["target_vol", "target_dir"])
    df = df.reset_index(drop=True)

    print(f"Features: built {len(df)} rows for {symbol} ({lookback_days}d lookback)")
    return df
