# RapidAPI Geopolitical Events Integration

This document describes how the Trading Bot integrates the **RapidAPI Geopolitical Events Database** as a supplementary data source for geopolitical event ingestion.

## Overview

The system fetches geopolitical events from two sources:

1. **GDELT** (Global Database of Events, Language, and Tone) — Free, unlimited, 15-minute update frequency
2. **RapidAPI Geopolitical Events Database** (optional) — Curated geopolitical events, free tier: 100 requests/month

Both sources write to the same `gdelt_events` table in `gti.db` and contribute to the `conflict_summary` aggregation, which powers the `/api/regions` endpoint and live map visualization.

## Getting Started

### 1. Free RapidAPI Key (Optional)

If you want to enable the RapidAPI fetcher:

1. Visit: https://rapidapi.com/nmk3/api/geopolitical-events-database1
2. Click **Subscribe to Test** → Select **Basic (Free)** plan (100 requests/month)
3. Create or sign in to your RapidAPI account
4. Copy the **X-RapidAPI-Key** value from the code samples panel
5. Set it as an environment variable before starting the backend:

**PowerShell:**
```powershell
$env:RAPIDAPI_KEY = "your_key_here"
python -m uvicorn api.main:app --reload --port 8000
```

**Windows CMD:**
```batch
set RAPIDAPI_KEY=your_key_here
python -m uvicorn api.main:app --reload --port 8000
```

**Or add it to `run.bat`:**
```batch
set RAPIDAPI_KEY=your_key_here
```

### 2. Without RapidAPI Key

The system works perfectly with **GDELT only**:
- No API key needed
- Unlimited free calls
- 15-minute update frequency
- Data feeds directly into `/api/events` and `/api/regions`

If `RAPIDAPI_KEY` is not set, the scheduler will skip the RapidAPI job and log a note.

## Architecture

### Job Schedule

The scheduler runs RapidAPI fetches **every 6 hours**:
- 4 fetches per day × 30 days = ~120 requests/month
- Safely within the 100 req/month free tier (conservative margin)
- Can be adjusted in `backend/scheduler.py` line ~212

### Data Pipeline

```
RapidAPI Events (e.g., "CRITICAL: Russian military exercise near Ukraine border")
        ↓
rapidapi_fetcher.py: Fetch via API + map fields to gdelt_events schema
        ↓
gti.db: gdelt_events table (insert or ignore duplicates)
        ↓
Refresh conflict_summary (aggregate by country_code)
        ↓
/api/events, /api/regions endpoints → Frontend (live map, regional tension)
```

### Field Mapping

RapidAPI response fields → `gdelt_events` table columns:

| RapidAPI Field | Maps To | Notes |
|---|---|---|
| `id` / `event_id` | `event_id` | Unique event identifier |
| `date` / `event_date` | `event_date` | ISO 8601 timestamp |
| `country` / `actor1_country` | `actor1_country` | Country code or name |
| `event_type` / `type` | `event_code`, `cameo_code` | Geopolitical event classification |
| `severity` / `goldstein_scale` | `goldstein_scale` | -10 (conflict) to +10 (cooperation) |
| `latitude` / `lat` | `latitude` | Decimal degrees |
| `longitude` / `lon` | `longitude` | Decimal degrees |
| `location` / `country` | `location` | Human-readable location name |

### Severity → Goldstein Conversion

Since RapidAPI may return severity labels, the fetcher converts them to GDELT's Goldstein scale:

```python
"CRITICAL" → -10.0  (high conflict)
"HIGH"     → -8.0
"MEDIUM"   → -4.0
"LOW"      → -1.0
"STABLE"   → 0.0
"POSITIVE" → 5.0
```

Numeric Goldstein values (if already in -10 to +10 range) are passed through as-is.

## Code Structure

### `backend/ingestion/rapidapi_fetcher.py`

Main fetcher module. Key functions:

- **`fetch_rapidapi_events(days_back=7) → int`**
  - Fetches events from the past 7 days (configurable)
  - Returns count of events inserted
  - Gracefully handles missing `RAPIDAPI_KEY` (returns 0, logs info)
  - Updates `conflict_summary` after insertion

- **`_goldstein_from_severity(val) → float`**
  - Converts severity label or numeric value to Goldstein scale
  - Defaults to 0.0 if value is None or unmappable

### `backend/scheduler.py`

Orchestrates RapidAPI fetches. Key additions:

- **`job_rapidapi()`** (line ~61)
  - Wrapper that calls `fetch_rapidapi_events()` and logs results
  - Catches exceptions so failures don't halt the scheduler

- **Scheduler job** (line ~210)
  - Runs every 6 hours via `IntervalTrigger(hours=6)`
  - Misfire grace time: 60 seconds

Example output in scheduler logs:
```
[INFO]  RapidAPI: inserted 7 events
[INFO]  RapidAPI: no events in response
[WARNING]  RapidAPI fetch failed: Connection timeout
```

## Verification

### 1. Check Scheduler Logs

Run the scheduler and look for RapidAPI job execution:

```powershell
cd backend
python scheduler.py
```

You should see periodic lines like:
```
2026-05-07 14:30:00  [INFO]  RapidAPI: inserted 12 events
2026-05-07 20:30:00  [INFO]  RapidAPI: inserted 8 events
```

### 2. Query API Endpoints

Confirm events are in the database:

```bash
curl http://localhost:8000/api/events?limit=5
```

Response should include events with proper `goldstein_scale`, `location`, `latitude`, `longitude` fields.

### 3. Check Conflict Summary

Verify regional aggregation is working:

```bash
curl http://localhost:8000/api/regions
```

Regions should show live `tension` values (0–10 scale) instead of all 0.0.

### 4. Database Direct Query

If the API endpoints don't show data yet, check the database directly:

```powershell
sqlite3 data/gti.db "SELECT COUNT(*) FROM gdelt_events;"
sqlite3 data/gti.db "SELECT COUNT(*) FROM conflict_summary WHERE conflict_count > 0;"
```

Should show non-zero counts after the scheduler runs.

### 5. Frontend Map

Open http://localhost:3000 and navigate to the **Geo Map** page:
- **Recent Geopolitical Events** list should populate with events
- **Regional Tension** cards should show colors (green/yellow/magenta) instead of all green
- **Tension Index** should display a value > 0 (if there's active conflict)

## Troubleshooting

### RapidAPI Fetcher Logs Nothing

**Cause:** `RAPIDAPI_KEY` not set.  
**Fix:** Verify the environment variable is set:
```powershell
$env:RAPIDAPI_KEY
```
If empty, set it and restart the scheduler.

### HTTP 403 or 429 Errors

**Cause:** API key invalid, expired, or rate limit exceeded.  
**Fix:**
1. Check the key is correct (copy from RapidAPI dashboard again)
2. Verify the plan is active (free tier may have expired)
3. Wait before retrying (rate limit resets hourly)

### No Events in /api/events or /api/regions

**Cause:** Data hasn't been fetched yet, or both GDELT and RapidAPI are failing.  
**Fix:**
1. Check scheduler logs for errors
2. Verify internet connection
3. Wait 2–3 minutes for initial backfill
4. Check `/api/diagnostic` endpoint:
   ```bash
   curl http://localhost:8000/api/diagnostic
   ```
   Should show `"data_ready": true` and event counts > 0

### RapidAPI Response Format Unexpected

**Cause:** API changed response structure.  
**Fix:**
1. Check the RapidAPI documentation for current schema
2. Update the field mapping in `rapidapi_fetcher.py` lines 74–82
3. The fetcher has flexible parsing (tries multiple field names) to handle minor format variations

## Cost Analysis

### Free Tier

- **100 requests/month**
- Scheduler runs every 6 hours = 4 calls/day = ~120 calls/month
- **Safe margin:** 20 extra calls/month (accounts for retries or higher frequency testing)

### Paid Tier

RapidAPI offers paid plans with higher rate limits. If you want higher-frequency updates (e.g., every 2 hours = 12 calls/day = 360 calls/month), upgrade to a paid plan.

Current configuration (every 6 hours) is designed for the free tier. To change:

**File:** `backend/scheduler.py` line ~212
```python
scheduler.add_job(
    job_rapidapi,
    IntervalTrigger(hours=6),  # ← Change this number
    id="rapidapi",
    ...
)
```

## Integration Points

### Database Schema

Both GDELT and RapidAPI write to:
- **Table:** `gti.db` → `gdelt_events`
- **Schema:** `event_id`, `event_date`, `actor1_country`, `actor2_country`, `event_code`, `cameo_code`, `goldstein_scale`, `latitude`, `longitude`, `location`, `num_articles`, `avg_tone`

### Conflict Summary Refresh

After each RapidAPI batch insert, the fetcher runs an UPSERT:

```sql
INSERT INTO conflict_summary (country_code, conflict_count, avg_goldstein, latest_event_time)
SELECT actor1_country, COUNT(*), AVG(goldstein_scale), MAX(event_date)
FROM gdelt_events
WHERE actor1_country IS NOT NULL AND actor1_country != ''
GROUP BY actor1_country
ON CONFLICT(country_code) DO UPDATE SET
  conflict_count = excluded.conflict_count,
  avg_goldstein = excluded.avg_goldstein,
  latest_event_time = excluded.latest_event_time
```

This aggregates all events (both GDELT and RapidAPI) by country, enabling the `/api/regions` endpoint to return live regional tension.

### API Endpoints Powered by RapidAPI Data

- **`GET /api/events`** — Recent events (includes RapidAPI events)
- **`GET /api/regions`** — Regional tension (aggregates from conflict_summary, which includes RapidAPI)
- **`GET /api/bilateral`** — Bilateral relations (based on both GDELT and RapidAPI)

## See Also

- [GDELT Integration](./NEXUS_IMPLEMENTATION.md#gdelt-integration) — Details on GDELT fetcher
- [Data Ingestion Architecture](./NEXUS_IMPLEMENTATION.md#data-ingestion) — Overall pipeline
- [run.bat Configuration](../run.bat) — How to set environment variables
