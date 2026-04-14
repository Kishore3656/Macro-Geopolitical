"""
GDELT Fetcher
=============
Downloads GDELT v2 event data (CSV ZIP files) and stores them in SQLite.

What is GDELT?
  The Global Database of Events, Language, and Tone — a free dataset that
  monitors world news every 15 minutes, classifies geopolitical events, and
  scores their tone and intensity. No API key needed.

Columns we extract:
  col 0  → GLOBALEVENTID   (unique event ID)
  col 1  → SQLDATE          (YYYYMMDD)
  col 7  → Actor1CountryCode
  col 17 → Actor2CountryCode
  col 26 → EventCode        (CAMEO code, e.g. 190 = use of military force)
  col 30 → GoldsteinScale   (-10 to +10, negative = conflict)
  col 33 → NumArticles      (how widely reported)
  col 34 → AvgTone          (-100 to +100, negative = negative tone)

Usage:
  python -m ingestion.gdelt_fetcher            # fetch latest 15-min update
  python -m ingestion.gdelt_fetcher --backfill --days 30
"""

import io
import zipfile
import argparse
import sqlite3
from datetime import datetime, timedelta

import requests
import pandas as pd

from config import NEWS_DB
from ingestion.db import get_conn

GDELT_LASTUPDATE = "http://data.gdeltproject.org/gdeltv2/lastupdate.txt"
GDELT_BASE       = "http://data.gdeltproject.org/gdeltv2/"

# Column index → name mapping (GDELT v2 export format)
COLS = {
    0:  "event_id",
    1:  "timestamp",
    7:  "actor1_country",
    17: "actor2_country",
    26: "event_code",
    30: "goldstein_scale",
    33: "num_articles",
    34: "avg_tone",
}


def _parse_gdelt_csv(raw_bytes: bytes) -> pd.DataFrame:
    """Unzip and parse a GDELT export ZIP into a DataFrame."""
    with zipfile.ZipFile(io.BytesIO(raw_bytes)) as z:
        csv_name = next(n for n in z.namelist() if n.upper().endswith(".CSV"))
        with z.open(csv_name) as f:
            df = pd.read_csv(
                f,
                sep="\t",
                header=None,
                usecols=list(COLS.keys()),
                dtype={
                    30: "float32",  # GoldsteinScale
                    33: "int32",    # NumArticles
                    34: "float32",  # AvgTone
                },
                low_memory=False,
            )
    df.columns = list(COLS.values())
    df["event_id"] = df["event_id"].astype(str)
    df["timestamp"] = pd.to_datetime(
        df["timestamp"].astype(str), format="%Y%m%d", errors="coerce"
    )
    df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
    df = df.dropna(subset=["event_id", "timestamp"])
    return df


def _insert_df(df: pd.DataFrame) -> int:
    """Insert rows into gdelt_events, skip duplicates. Returns count inserted."""
    conn = get_conn(NEWS_DB)
    inserted = 0
    for _, row in df.iterrows():
        try:
            conn.execute(
                """INSERT OR IGNORE INTO gdelt_events
                   (event_id, timestamp, actor1_country, actor2_country,
                    event_code, goldstein_scale, num_articles, avg_tone)
                   VALUES (?,?,?,?,?,?,?,?)""",
                (
                    row["event_id"],
                    row["timestamp"],
                    row.get("actor1_country"),
                    row.get("actor2_country"),
                    row.get("event_code"),
                    float(row["goldstein_scale"]) if pd.notna(row.get("goldstein_scale")) else None,
                    int(row["num_articles"])      if pd.notna(row.get("num_articles"))   else None,
                    float(row["avg_tone"])        if pd.notna(row.get("avg_tone"))       else None,
                ),
            )
            inserted += 1
        except sqlite3.Error:
            pass
    conn.commit()
    conn.close()
    return inserted


def fetch_latest():
    """Fetch the most recent GDELT 15-minute export and store it."""
    try:
        resp = requests.get(GDELT_LASTUPDATE, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"GDELT: failed to get lastupdate.txt — {e}")
        return

    url = None
    for line in resp.text.strip().splitlines():
        parts = line.split()
        if len(parts) == 3 and parts[2].endswith("export.CSV.zip"):
            url = parts[2]
            break

    if not url:
        print("GDELT: no export URL found in lastupdate.txt")
        return

    try:
        data = requests.get(url, timeout=60).content
        df   = _parse_gdelt_csv(data)
        n    = _insert_df(df)
        print(f"GDELT latest: inserted {n} events  ({len(df)} parsed)")
    except Exception as e:
        print(f"GDELT latest: failed — {e}")


def backfill(days: int = 30):
    """
    Backfill historical GDELT data.
    GDELT publishes one export per 15-min slot; we grab the EOD (235900) file per day.
    A 30-day backfill takes roughly 15–30 minutes.
    """
    end     = datetime.utcnow()
    start   = end - timedelta(days=days)
    current = start

    print(f"GDELT backfill: {days} days from {start.date()} to {end.date()}")

    while current <= end:
        date_str = current.strftime("%Y%m%d")
        url = f"{GDELT_BASE}{date_str}235900.export.CSV.zip"
        try:
            resp = requests.get(url, timeout=60)
            if resp.status_code == 200:
                df = _parse_gdelt_csv(resp.content)
                n  = _insert_df(df)
                print(f"  {date_str}: inserted {n} / {len(df)} events")
            else:
                print(f"  {date_str}: HTTP {resp.status_code} — skipping")
        except Exception as e:
            print(f"  {date_str}: error — {e}")
        current += timedelta(days=1)

    print("GDELT backfill complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GDELT data fetcher")
    parser.add_argument("--backfill", action="store_true",
                        help="Backfill historical data instead of fetching latest")
    parser.add_argument("--days", type=int, default=30,
                        help="Number of days to backfill (default: 30)")
    args = parser.parse_args()

    if args.backfill:
        backfill(args.days)
    else:
        fetch_latest()
