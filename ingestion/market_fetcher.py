"""
Market Data Fetcher
===================
Downloads OHLCV (Open, High, Low, Close, Volume) price data and stores it in SQLite.

Data source strategy — tries each source in order, stops at first success:
  1. yfinance Ticker.history()  — uses a different Yahoo endpoint than yf.download(),
                                   avoids the JSON challenge page that breaks download()
  2. pandas_datareader / Stooq  — free CSV endpoint, no API key, different network path,
                                   reliable fallback when Yahoo blocks or rate-limits

Symbols tracked (configured in config.py):
  SPY  — S&P 500 ETF (broad US market proxy)
  VIX  — Volatility Index (fear gauge)
  GLD  — Gold ETF (safe-haven proxy)

Usage:
  python -m ingestion.market_fetcher
  python -m ingestion.market_fetcher --backfill --days 30
  python -m ingestion.market_fetcher --backfill --symbols SPY VIX --days 7
"""

import argparse
from datetime import datetime, timedelta

import pandas as pd
import yfinance as yf

from config import MARKET_DB, SYMBOLS
from ingestion.db import get_conn

# Yahoo Finance ticker overrides
YF_OVERRIDES = {
    "VIX": "^VIX",
}

# Stooq ticker overrides (stooq uses lowercase + .US suffix for US equities)
STOOQ_OVERRIDES = {
    "SPY": "spy.us",
    "GLD": "gld.us",
    "VIX": "^vix",
}


def _yf_ticker_history(symbol: str, start: datetime, end: datetime) -> pd.DataFrame:
    """
    Source 1: yfinance Ticker.history().
    Uses a different internal Yahoo endpoint than yf.download() and is less
    prone to the JSON challenge/block that causes JSONDecodeError on download().
    Returns hourly OHLCV or empty DataFrame on any failure.
    """
    yf_sym = YF_OVERRIDES.get(symbol, symbol)
    try:
        ticker = yf.Ticker(yf_sym)
        df = ticker.history(start=start, end=end, interval="1h", auto_adjust=True)
        if df.empty:
            return pd.DataFrame()
        # Ticker.history() returns a DatetimeIndex with tz — strip tz for consistency
        df.index = df.index.tz_localize(None) if df.index.tz is None else df.index.tz_convert(None)
        return df[["Open", "High", "Low", "Close", "Volume"]]
    except Exception as exc:
        print(f"Market [{symbol}] yfinance Ticker.history failed: {exc}")
        return pd.DataFrame()


def _stooq_history(symbol: str, start: datetime, end: datetime) -> pd.DataFrame:
    """
    Source 2: Stooq via pandas_datareader.
    Stooq serves clean daily CSV data — no API key, different network path.
    Note: Stooq only provides daily bars, not hourly. We resample to daily
    when this fallback is used and mark the interval in the timestamp as market close.
    Returns daily OHLCV or empty DataFrame on any failure.
    """
    try:
        import pandas_datareader.data as web
        stooq_sym = STOOQ_OVERRIDES.get(symbol, symbol.lower() + ".us")
        df = web.DataReader(stooq_sym, "stooq", start=start, end=end)
        if df.empty:
            return pd.DataFrame()
        df = df.sort_index()
        # Stooq column names are already Open/High/Low/Close/Volume
        df = df[["Open", "High", "Low", "Close", "Volume"]]
        return df
    except Exception as exc:
        print(f"Market [{symbol}] Stooq fallback failed: {exc}")
        return pd.DataFrame()


def _download_symbol(symbol: str, start: datetime, end: datetime) -> pd.DataFrame:
    """
    Try each data source in order. Return the first non-empty result.
    """
    for source_fn, source_name in [
        (_yf_ticker_history, "yfinance"),
        (_stooq_history,     "stooq"),
    ]:
        df = source_fn(symbol, start, end)
        if not df.empty:
            print(f"Market [{symbol}] fetched via {source_name} — {len(df)} bars")
            return df

    print(f"Market [{symbol}] all sources failed — no data written")
    return pd.DataFrame()


def _insert_ohlcv(symbol: str, df: pd.DataFrame) -> int:
    """Insert OHLCV rows for one symbol. Returns count of new rows inserted."""
    required = {"Open", "High", "Low", "Close", "Volume"}
    if not required.issubset(set(df.columns)):
        print(f"Market [{symbol}] missing columns: {required - set(df.columns)}")
        return 0

    conn     = get_conn(MARKET_DB)
    inserted = 0

    for ts, row in df.iterrows():
        timestamp = ts.strftime("%Y-%m-%d %H:%M:%S") if hasattr(ts, "strftime") else str(ts)
        try:
            cursor = conn.execute(
                """INSERT OR IGNORE INTO ohlcv
                   (symbol, timestamp, open, high, low, close, volume)
                   VALUES (?,?,?,?,?,?,?)""",
                (
                    symbol,
                    timestamp,
                    float(row["Open"])   if pd.notna(row["Open"])   else None,
                    float(row["High"])   if pd.notna(row["High"])   else None,
                    float(row["Low"])    if pd.notna(row["Low"])    else None,
                    float(row["Close"])  if pd.notna(row["Close"])  else None,
                    float(row["Volume"]) if pd.notna(row["Volume"]) else None,
                ),
            )
            if cursor.rowcount:
                inserted += 1
        except Exception as e:
            print(f"Market [{symbol}] insert error at {timestamp}: {e}")

    conn.commit()
    conn.close()
    return inserted


def fetch_latest(symbols: list = None):
    """Fetch the last 2 days of data for each symbol."""
    symbols = symbols or SYMBOLS
    end   = datetime.utcnow()
    start = end - timedelta(days=2)
    for sym in symbols:
        df = _download_symbol(sym, start, end)
        if df.empty:
            continue
        n = _insert_ohlcv(sym, df)
        print(f"Market [{sym}] inserted {n} new rows")


def backfill(symbols: list = None, days: int = 30):
    """
    Fetch the last N days of data for each symbol.
    yfinance supports up to 730 days of hourly history.
    Stooq fallback provides daily bars when yfinance is unavailable.
    """
    symbols = symbols or SYMBOLS
    end   = datetime.utcnow()
    start = end - timedelta(days=days)
    for sym in symbols:
        df = _download_symbol(sym, start, end)
        if df.empty:
            continue
        n = _insert_ohlcv(sym, df)
        print(f"Market backfill [{sym}] inserted {n} rows over {days} days")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Market data fetcher (yfinance + stooq fallback)")
    parser.add_argument("--backfill", action="store_true",
                        help="Fetch historical data instead of latest")
    parser.add_argument("--symbols", nargs="+", default=None,
                        help="Symbols to fetch (default: from config.py)")
    parser.add_argument("--days", type=int, default=30,
                        help="Days to backfill (default: 30)")
    args = parser.parse_args()

    if args.backfill:
        backfill(args.symbols, args.days)
    else:
        fetch_latest(args.symbols)
