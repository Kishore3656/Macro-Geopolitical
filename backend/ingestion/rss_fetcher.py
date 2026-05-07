"""
RSS Fetcher
===========
Polls multiple free RSS news feeds and stores headlines in SQLite
with VADER sentiment scores attached.

Feeds used (configured in config.py):
  - Reuters World News
  - BBC World News
  - Al Jazeera
  - Associated Press

Deduplication: rows are keyed on (title, source) so re-polling the same
feed won't create duplicate entries.

Usage:
  python ingestion/rss_fetcher.py
"""

from datetime import datetime, timezone

import feedparser

from config import RSS_FEEDS, NEWS_DB
from ingestion.db import get_conn
from nlp.sentiment import score_headline


def _parse_date(entry) -> str:
    """Extract publish date from a feedparser entry, fallback to now."""
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        try:
            dt = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except (TypeError, ValueError):
            pass
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


def fetch_all() -> int:
    """
    Poll all RSS feeds, score each headline with VADER, and insert into SQLite.
    Returns total rows inserted.
    """
    conn  = get_conn(NEWS_DB)
    total = 0
    now   = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
        except Exception as e:
            print(f"RSS: failed to parse {feed_url} — {e}")
            continue

        source = feed.feed.get("title", feed_url)

        for entry in feed.entries:
            title = (entry.get("title") or "").strip()
            if not title:
                continue

            published_at = _parse_date(entry)
            sentiment    = score_headline(title)

            try:
                cursor = conn.execute(
                    """INSERT OR IGNORE INTO rss_articles
                       (title, source, published_at, vader_compound, vader_label, fetched_at)
                       VALUES (?,?,?,?,?,?)""",
                    (
                        title,
                        source,
                        published_at,
                        sentiment["compound"],
                        sentiment["label"],
                        now,
                    ),
                )
                if cursor.rowcount:
                    total += 1
            except Exception as e:
                print(f"RSS: insert error — {e}")
                continue

    conn.commit()
    conn.close()
    print(f"RSS: inserted {total} new articles across {len(RSS_FEEDS)} feeds")
    return total


if __name__ == "__main__":
    fetch_all()
