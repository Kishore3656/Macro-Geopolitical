"""
NewsAPI Fetcher
===============
Fetches English top headlines from NewsAPI and stores them in SQLite
with VADER sentiment scores.

Free tier limits:
  - 100 requests per day
  - We stop at 95 (NEWSAPI_DAILY_LIMIT) to leave a safety buffer
  - Daily call count is persisted in data/newsapi_calls.json
  - Each call fetches up to 100 headlines (max page size on free tier)

Get a free key at: https://newsapi.org/register
Set it in your .env file as: NEWSAPI_KEY=your_key_here

Usage:
  python ingestion/newsapi_fetcher.py
"""

import json
import os
from datetime import datetime, date

import requests

from config import NEWS_DB, NEWSAPI_KEY, NEWSAPI_CALLS, NEWSAPI_DAILY_LIMIT
from ingestion.db import get_conn
from nlp.sentiment import score_headline

NEWSAPI_URL = "https://newsapi.org/v2/top-headlines"


def _load_call_log() -> dict:
    """Load today's call count from disk. Resets automatically each new day."""
    today = str(date.today())
    if os.path.exists(NEWSAPI_CALLS):
        try:
            with open(NEWSAPI_CALLS) as f:
                log = json.load(f)
            if log.get("date") == today:
                return log
        except (json.JSONDecodeError, OSError):
            pass
    return {"date": today, "count": 0}


def _save_call_log(log: dict):
    os.makedirs(os.path.dirname(NEWSAPI_CALLS) or ".", exist_ok=True)
    with open(NEWSAPI_CALLS, "w") as f:
        json.dump(log, f)


def fetch_headlines() -> int:
    """
    Fetch top English headlines from NewsAPI and store with VADER sentiment.
    Skips silently if no API key or daily limit reached.
    Returns number of new rows inserted.
    """
    if not NEWSAPI_KEY:
        print("NewsAPI: NEWSAPI_KEY not set in .env — skipping")
        return 0

    log = _load_call_log()
    if log["count"] >= NEWSAPI_DAILY_LIMIT:
        print(f"NewsAPI: daily limit reached ({log['count']}/{NEWSAPI_DAILY_LIMIT}) — skipping")
        return 0

    params = {
        "apiKey":   NEWSAPI_KEY,
        "language": "en",
        "category": "general",
        "pageSize": 100,
    }

    try:
        resp = requests.get(NEWSAPI_URL, params=params, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"NewsAPI: request failed — {e}")
        return 0

    log["count"] += 1
    _save_call_log(log)

    data     = resp.json()
    articles = data.get("articles", [])

    if not articles:
        print(f"NewsAPI: no articles returned (status={data.get('status')}, "
              f"message={data.get('message', '')})")
        return 0

    conn       = get_conn(NEWS_DB)
    inserted   = 0
    fetched_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    for art in articles:
        title = (art.get("title") or "").strip()
        if not title or title == "[Removed]":
            continue

        source       = (art.get("source") or {}).get("name", "Unknown")
        raw_pub      = art.get("publishedAt") or fetched_at
        published_at = raw_pub[:19].replace("T", " ")
        sentiment    = score_headline(title)

        try:
            cursor = conn.execute(
                """INSERT OR IGNORE INTO newsapi_headlines
                   (title, source, published_at, vader_compound, fetched_at)
                   VALUES (?,?,?,?,?)""",
                (title, source, published_at, sentiment["compound"], fetched_at),
            )
            if cursor.rowcount:
                inserted += 1
        except Exception as e:
            print(f"NewsAPI: insert error — {e}")
            continue

    conn.commit()
    conn.close()
    print(f"NewsAPI: inserted {inserted} headlines  "
          f"(calls today: {log['count']}/{NEWSAPI_DAILY_LIMIT})")
    return inserted


if __name__ == "__main__":
    fetch_headlines()
