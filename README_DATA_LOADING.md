# ⚠️ CRITICAL: How to Get Real Data (Not Random Values)

## Problem You're Seeing

**Dashboard shows random/placeholder data instead of real market prices and geopolitical events.**

## Why This Happens

When you run `run.bat` or `RUN.ps1 start`, the system starts but **has NO DATA YET**:

1. **Databases are empty** (first time startup)
2. **Scheduler fetches real data** (takes 2-3 minutes first time)
3. **Until data arrives, API returns placeholder values**

---

## The Solution: Wait for Scheduler

### Step 1: Run the startup script
```cmd
run.bat
```
or
```powershell
.\RUN.ps1 start
```

### Step 2: Watch the Scheduler terminal
You'll see it doing this:
```
[INFO] Market [SPY] fetched via yfinance — 720 bars
[INFO] Market [VIX] fetched via yfinance — 720 bars
[INFO] GDELT: Fetching geopolitical events...
[INFO] GTI [2026-05-07 14:00:00] score=0.4231 level=MODERATE
[INFO] Predict [2026-05-07 14:01:00] vol=HIGH (65%) dir=UP (52%)
```

### Step 3: Check diagnostic endpoint
```bash
curl http://localhost:8000/api/diagnostic
```

**Look for:**
```json
{
  "status": "ready",
  "data_ready": true,
  "data_availability": {
    "gti_scores": 96,
    "gdelt_events": 15234,
    "spy_bars": 720
  }
}
```

**If numbers are 0, it's still loading.**

---

## Timeline

| Time | What's Happening | What You'll See |
|------|------------------|-----------------|
| **t=0** | Services start | Blank dashboard |
| **t=30s** | Scheduler backfills market data | API still showing "awaiting_data" |
| **t=60s** | GDELT events loading | Scheduler terminal shows progress |
| **t=120s** | GTI scores computed | `/api/diagnostic` starts showing counts |
| **t=180s** | Models run predictions | Dashboard updates with real data ✓ |

---

## What Each Status Means

### ✅ "data_ready": true
System has real data. Dashboard will show:
- Real GTI scores (geopolitical tension 0-1)
- Real market prices (SPY, VIX, GLD)
- Real ML predictions (volatility + direction)
- Real news sentiment
- Real geopolitical events

### ⏳ "data_ready": false
System is still loading. This is normal. Wait 2-3 minutes.

Shows in API responses:
```json
{
  "status": "awaiting_data",
  "message": "Scheduler backfilling market data — check /api/diagnostic"
}
```

---

## How the Data Gets There

```
┌─────────────────────────────────────────┐
│          SCHEDULER (Background Job)     │
└──────────────┬──────────────────────────┘
               │ Runs every 15 minutes
               ├─→ RSS Fetcher (Reuters, BBC, AJ, AP)
               ├─→ GDELT Fetcher (world geopolitical events)
               ├─→ NewsAPI Fetcher (English headlines)
               ├─→ Market Fetcher (SPY, VIX, GLD prices)
               ├─→ GTI Aggregator (combines signals)
               └─→ ML Predictor (runs models)
                    │
                    ↓
            ┌──────────────────┐
            │  SQLite DBs      │
            ├──────────────────┤
            │ gti.db           │ ← GTI scores
            │ market.db        │ ← OHLCV prices
            │ news.db          │ ← Articles + sentiment
            │ predictions.db   │ ← ML outputs
            └────────┬─────────┘
                     │
                     ↓
            ┌──────────────────┐
            │   FastAPI        │
            │   /api/*         │
            └────────┬─────────┘
                     │
                     ↓
            ┌──────────────────┐
            │   Dashboard      │
            │  Real Data! ✓    │
            └──────────────────┘
```

---

## Most Common Reasons for "Random Data"

### 1. **Scheduler Not Running**
Check if you see a "Scheduler" terminal window.
- If not: Run `run.bat` again
- If yes: Check for errors in Scheduler window

### 2. **Scheduler Crashed**
Check Scheduler terminal for error messages like:
```
[ERROR] Market job failed: <reason>
[ERROR] GDELT job failed: <reason>
```

**Solutions:**
- Check internet connection (GDELT, market data need external APIs)
- Restart: Close all terminals and run `run.bat` again
- Wait: Some APIs rate-limit—just wait a few minutes

### 3. **Data Backfill Takes Longer Than Expected**
First-time backfill of 30 days can take 5-10 minutes if:
- Your internet is slow
- GDELT servers are busy
- Market data source is rate-limiting

**Just wait.** Watch Scheduler terminal for progress.

### 4. **API Running But No Scheduler**
If you started services manually:
```powershell
.\RUN.ps1 api        # Just API
.\RUN.ps1 frontend   # Just frontend
```

You need to also run:
```powershell
.\RUN.ps1 scheduler  # Start this separately
```

---

## Verify Real Data is Loaded

Once `data_ready: true`, test real values:

```bash
# GTI score (should be between 0.0 and 1.0)
curl http://localhost:8000/api/gti | jq '.score'

# Current SPY price (should be realistic, e.g., 480.50)
curl http://localhost:8000/api/market/spy | jq '.current_price'

# Volatility prediction (should be HIGH or LOW, not UNKNOWN)
curl http://localhost:8000/api/signals | jq '.vol_prediction'

# Number of conflicts (should be > 0)
curl http://localhost:8000/api/conflicts | jq '.total_events'
```

All non-zero = real data loaded ✓

---

## What's Actually in Each Database

After backfill completes:

| Database | Contains | Row Count |
|----------|----------|-----------|
| **gti.db** | GTI scores computed every 15 min | ~96 (6-hour history) |
| **market.db** | SPY, VIX, GLD hourly OHLCV | ~720 per symbol (30 days) |
| **news.db** | RSS articles + sentiment | ~200-500 |
| **predictions.db** | ML outputs (vol/direction) | ~96 (6-hour history) |

Check counts:
```bash
curl http://localhost:8000/api/diagnostic | jq '.data_availability'
```

---

## After First Load

Once data is loaded:
- **Scheduler keeps running** — updates every 15 minutes
- **Dashboard stays fresh** — new data every 15 minutes
- **You see live trading signals** — based on real geopolitical + market data

---

## If You Still See Random Values After 5 Minutes

1. **Check Scheduler terminal** — are there error messages?
2. **Restart everything** — close all 4 windows, run `run.bat` again
3. **Check internet** — Can you reach http://data.gdeltproject.org?
4. **Check system health** — Visit `/api/diagnostic` to see what's missing

If still broken: Check the `GET_LIVE_DATA.md` troubleshooting section or look at scheduler logs.

---

## Summary

| Situation | What's Happening | What to Do |
|-----------|-----------------|-----------|
| Blank dashboard on first run | Scheduler backfilling data (normal) | **Wait 2-3 minutes** |
| Dashboard shows zeros | Data not loaded yet | **Check diagnostic** endpoint |
| Dashboard shows random values | Old cached data before this update | **Restart system** |
| API returns "awaiting_data" | Scheduler still running | **Wait for counts > 0** |
| Scheduler terminal shows errors | External API failure | **Check internet, wait 5 min** |

---

**TL;DR:** Run `run.bat` → Wait 3 minutes → Real data loads automatically. If not, check `/api/diagnostic`.
