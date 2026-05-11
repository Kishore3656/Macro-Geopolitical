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
    "vix_close",
    "vix_change_1h",
    "gld_returns_1h",
    "hour_of_day",
    "day_of_week",
    "gti_lag_1",
    "gti_lag_4",
    "rsi_14",
    "macd_diff",
    "bb_upper",
    "bb_lower",
    "atr_14",
    "volume_sma_20",
    "price_momentum",
    "vix_percentile",
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

    # ── Load OHLCV for primary symbol + VIX + GLD ─────────────────────────
    conn     = get_conn(MARKET_DB)
    mkt_rows = conn.execute(
        f"""SELECT timestamp, symbol, open, high, low, close, volume
            FROM ohlcv
            WHERE (symbol IN (?, 'VIX', 'GLD')) AND timestamp >= ?
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

    # Pivot market data so each symbol becomes its own column set
    mkt_df = (
        mkt_df.sort_values("timestamp")
        .drop_duplicates(["hour", "symbol"], keep="last")
    )

    spy_df = mkt_df[mkt_df["symbol"] == symbol][["hour", "open", "high", "low", "close", "volume"]].copy()
    spy_df.rename(columns={
        "open": "spy_open",
        "high": "spy_high",
        "low": "spy_low",
        "close": "spy_close",
        "volume": "spy_volume"
    }, inplace=True)

    vix_df = mkt_df[mkt_df["symbol"] == "VIX"][["hour", "close"]].copy()
    vix_df.rename(columns={"close": "vix_close"}, inplace=True)

    gld_df = mkt_df[mkt_df["symbol"] == "GLD"][["hour", "close"]].copy()
    gld_df.rename(columns={"close": "gld_close"}, inplace=True)

    # Merge on hour: GTI + SPY + VIX + GLD
    df = pd.merge(
        spy_df,
        gti_df[["hour", "gti_score", "conflict_ct", "avg_tone", "vader_avg"]],
        on="hour",
        how="inner",
    )
    df = pd.merge(df, vix_df, on="hour", how="left")
    df = pd.merge(df, gld_df, on="hour", how="left")

    df = df.sort_values("hour").reset_index(drop=True)

    if df.empty:
        print("Features: GTI and market data don't overlap — check timestamps")
        return pd.DataFrame()

    # Rename SPY columns back to original names for compatibility
    df.rename(columns={
        "spy_open": "open",
        "spy_high": "high",
        "spy_low": "low",
        "spy_close": "close",
        "spy_volume": "volume"
    }, inplace=True)

    # ── Engineered market features ────────────────────────────────────────
    df["returns_1h"] = df["close"].pct_change(1)
    df["returns_4h"] = df["close"].pct_change(4)
    df["vol_20h"]    = df["returns_1h"].rolling(20, min_periods=20).std()

    # VIX and GLD features (forward-fill gaps if they don't trade all hours)
    df["vix_close"] = df["vix_close"].ffill().bfill()
    # Fill still-missing VIX (entirely empty column) with neutral default
    if df["vix_close"].isna().all():
        print("WARNING: VIX data entirely missing — filling with neutral value 20.0")
        df["vix_close"] = 20.0
    df["vix_change_1h"] = df["vix_close"].pct_change(1).fillna(0.0)  # first row NaN → 0

    df["gld_close"] = df["gld_close"].ffill().bfill()
    # Fill still-missing GLD (entirely empty column) with neutral default
    if df["gld_close"].isna().all():
        print("WARNING: GLD data entirely missing — filling with neutral value 180.0")
        df["gld_close"] = 180.0
    df["gld_returns_1h"] = df["gld_close"].pct_change(1).fillna(0.0)  # first row NaN → 0

    # Time-of-day features
    df["hour_of_day"] = df["hour"].dt.hour
    df["day_of_week"] = df["hour"].dt.dayofweek

    # Lagged GTI features
    df["gti_lag_1"] = df["gti_score"].shift(1)
    df["gti_lag_4"] = df["gti_score"].shift(4)

    # ── Technical Indicators ──────────────────────────────────────────────
    # RSI (14-period)
    delta = df["close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df["rsi_14"] = 100 - (100 / (1 + rs))

    # MACD
    exp1 = df["close"].ewm(span=12).mean()
    exp2 = df["close"].ewm(span=26).mean()
    df["macd_diff"] = exp1 - exp2

    # Bollinger Bands (20-period, 2 std)
    sma20 = df["close"].rolling(20).mean()
    std20 = df["close"].rolling(20).std()
    df["bb_upper"] = sma20 + (std20 * 2)
    df["bb_lower"] = sma20 - (std20 * 2)

    # ATR (14-period) — normalized by close
    high_low = df["high"] - df["low"]
    high_close = abs(df["high"] - df["close"].shift(1))
    low_close = abs(df["low"] - df["close"].shift(1))
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = ranges.max(axis=1)
    df["atr_14"] = true_range.rolling(14).mean() / df["close"]

    # Volume-based features
    df["volume_sma_20"] = df["volume"].rolling(20).mean() / (df["volume"] + 1)

    # Momentum
    df["price_momentum"] = (df["close"] - df["close"].shift(20)) / df["close"].shift(20)

    # VIX percentile rank (normalized against recent range)
    vix_min = df["vix_close"].rolling(20).min()
    vix_max = df["vix_close"].rolling(20).max()
    df["vix_percentile"] = (df["vix_close"] - vix_min) / (vix_max - vix_min + 0.01)

    # ── Targets (next-hour prediction) ────────────────────────────────────
    next_close       = df["close"].shift(-1)
    next_returns     = df["returns_1h"].shift(-1).abs()
    df["target_dir"] = (next_close > df["close"]).astype(int)
    df["target_vol"] = (next_returns > df["vol_20h"]).astype(int)

    # Drop rows with NaN in features or targets
    pre_drop = len(df)
    df = df.dropna(subset=FEATURE_COLS + ["target_vol", "target_dir"])
    if len(df) < pre_drop:
        print(f"WARNING: dropna removed {pre_drop - len(df)} rows ({len(df)} remaining)")
    df = df.reset_index(drop=True)

    print(f"Features: built {len(df)} rows for {symbol} ({lookback_days}d lookback)")
    return df
