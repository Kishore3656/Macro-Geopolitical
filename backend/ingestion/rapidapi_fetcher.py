"""
RapidAPI Geopolitical Events Fetcher
=====================================
Fetches geopolitical events from the RapidAPI Geopolitical Events Database
and stores them in GTI_DB alongside GDELT data.

API: https://rapidapi.com/nmk3/api/geopolitical-events-database1
Free tier: 100 requests/month

Authentication: Requires RAPIDAPI_KEY environment variable
"""
import hashlib
If not set, the fetcher gracefully skips and logs a note.
"""

import os
import logging
import requests
from datetime import datetime, timedelta

from config import GTI_DB
from ingestion.db import db_transaction

logger = logging.getLogger(__name__)

RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY", "")
RAPIDAPI_HOST = "geopolitical-events-database1.p.rapidapi.com"
RAPIDAPI_URL = "https://geopolitical-events-database1.p.rapidapi.com/events"


def fetch_rapidapi_events(days_back: int = 7) -> int:
    """
    Fetch recent geopolitical events from RapidAPI Geopolitical Events Database.
    Inserts them into GTI_DB alongside GDELT data.
    Returns count of events inserted.
    """
    if not RAPIDAPI_KEY:
        logger.info("RAPIDAPI_KEY not set — skipping RapidAPI fetch")
        return 0

    since = (datetime.utcnow() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST,
    }

    try:
        logger.info(f"RapidAPI: fetching events since {since}...")
        resp = requests.get(
            RAPIDAPI_URL,
            headers=headers,
            params={"from": since},
            timeout=15
        )
        resp.raise_for_status()
        data = resp.json()
        logger.debug(f"RapidAPI response: {type(data).__name__}")
    except requests.RequestException as e:
        logger.warning(f"RapidAPI fetch failed: {e}")
        return 0
    except ValueError as e:
        logger.warning(f"RapidAPI JSON parse failed: {e}")
        return 0

    # Extract events from response (flexible parsing for different response formats)
    events = data.get("events") or data.get("data") or (data if isinstance(data, list) else [])
    if not events:
        logger.info(f"RapidAPI: no events in response")
        return 0

    inserted = 0
    try:
        with db_transaction(GTI_DB) as conn:
            for ev in events:
                try:
                    # Map RapidAPI fields to our schema
                    # Use md5 of sorted JSON for deterministic IDs (dict key order varies)
                    import json as _json
                    event_id = ev.get("id") or ev.get("event_id") or hashlib.md5(
                        _json.dumps(ev, sort_keys=True).encode("utf-8")
                    ).hexdigest()
                    event_date = ev.get("date") or ev.get("event_date") or datetime.utcnow().isoformat()
                    country = ev.get("country") or ev.get("actor1_country") or ""
                    event_type = ev.get("event_type") or ev.get("type") or ""
                    goldstein = _goldstein_from_severity(ev.get("severity") or ev.get("goldstein_scale"))
                    latitude = ev.get("latitude") or ev.get("lat") or None
                    longitude = ev.get("longitude") or ev.get("lon") or None
                    location = ev.get("location") or ev.get("country") or ""

                    # Insert into gdelt_events table
                    conn.execute(
                        """INSERT OR IGNORE INTO gdelt_events
                           (event_id, event_date, actor1_country, event_code, cameo_code,
                            goldstein_scale, latitude, longitude, location, num_articles, avg_tone)
                           VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                        (
                            event_id,
                            event_date,
                            country,
                            event_type,
                            event_type,  # cameo_code = event_type
                            goldstein,
                            latitude,
                            longitude,
                            location,
                            1,  # RapidAPI doesn't provide article count, default to 1
                            0.0,  # RapidAPI doesn't provide tone, default to neutral
                        ),
                    )
                    inserted += 1
                except Exception as e:
                    logger.debug(f"RapidAPI: skipping event — {e}")
                    pass

            # Refresh conflict_summary aggregation
            try:
                conn.execute("""
                    INSERT INTO conflict_summary (country_code, conflict_count, avg_goldstein, latest_event_time)
                    SELECT actor1_country, COUNT(*), AVG(goldstein_scale), MAX(event_date)
                    FROM gdelt_events
                    WHERE actor1_country IS NOT NULL AND actor1_country != ''
                    GROUP BY actor1_country
                    ON CONFLICT(country_code) DO UPDATE SET
                      conflict_count = excluded.conflict_count,
                      avg_goldstein = excluded.avg_goldstein,
                      latest_event_time = excluded.latest_event_time
                """)
            except Exception as e:
                logger.debug(f"RapidAPI: conflict_summary refresh failed — {e}")

        logger.info(f"RapidAPI: inserted {inserted} events")
    except Exception as e:
        logger.error(f"RapidAPI database transaction failed: {e}")

    return inserted


def _goldstein_from_severity(val):
    """
    Convert a severity label or numeric value to Goldstein scale (-10 to +10).
    RapidAPI may return severity as: CRITICAL, HIGH, MEDIUM, LOW
    Or as a numeric value already in Goldstein range.
    """
    if val is None:
        return 0.0

    # If numeric, assume it's already in Goldstein range
    if isinstance(val, (int, float)):
        return float(val)

    # Map severity labels to Goldstein equivalents
    mapping = {
        "CRITICAL": -10.0,
        "HIGH": -8.0,
        "MEDIUM": -4.0,
        "LOW": -1.0,
        "STABLE": 0.0,
        "POSITIVE": 5.0,
    }
    return mapping.get(str(val).upper(), 0.0)
