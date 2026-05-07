# Get Live Data Flowing - CRITICAL SETUP

**Problem:** API is working but databases are empty. No real data = no GTI, no market data, no predictions.

**Solution:** Run the scheduler to backfill and stream live data.

---

## Why Nothing is Showing

The system has **three layers**:

1. **Databases** (SQLite) — empty, waiting for data ✗
2. **Models** (LightGBM) — trained and ready ✓
3. **API** (FastAPI) — running but returning zeros ⚠️

The **scheduler** is the glue that connects them. Without it:
- No GDELT events (geopolitical data)
- No market prices (SPY, VIX, GLD)
- No news sentiment (RSS feeds)
- No GTI score
- No predictions

---

## Step-by-Step: Start Live Data Pipeline

### 1. Open PowerShell and run:
```powershell
cd "d:\trading bot\geo-market-ml"
.\RUN.ps1 start
```

This launches **3 terminal windows**:
- **Scheduler** — fetches and updates data every 15 minutes
- **API** — serves predictions on http://localhost:8000
- **Frontend** — dashboard at http://localhost:3000

### 2. Wait for scheduler to backfill (2-5 minutes first time)

The scheduler will:
1. Fetch 30 days of GDELT events (geopolitical)
2. Fetch 30 days of market data (SPY, VIX, GLD)
3. Compute GTI scores
4. Run inference on all models
5. Then continue every 15 minutes

**Expected output in Scheduler terminal:**
```
[INFO] Market [SPY] fetched via yfinance — 720 bars
[INFO] Market [VIX] fetched via yfinance — 720 bars
[INFO] GDELT: Fetching latest updates...
[INFO] GTI [2026-05-07 14:00:00] score=0.4231 level=MODERATE conflicts=145
[INFO] Predict [2026-05-07 14:01:00] vol=HIGH (65.2%) dir=UP (52.1%)
```

---

## Check System Health

### Quick diagnostic:
```bash
curl http://localhost:8000/api/diagnostic
```

**Output shows:**
```json
{
  "data_availability": {
    "gti_scores": 96,
    "gdelt_events": 15234,
    "spy_bars": 720,
    "rss_articles": 245,
    "predictions": 96
  },
  "status": "ready",
  "data_ready": true
}
```

**If empty:**
- `gti_scores: 0` → scheduler not running or just started
- `gdelt_events: 0` → GDELT backfill in progress
- `spy_bars: 0` → market fetch not complete

### View current GTI:
```bash
curl http://localhost:8000/api/gti
```

### View market data:
```bash
curl http://localhost:8000/api/market/spy
```

### View ML predictions:
```bash
curl http://localhost:8000/api/signals
```

---

## What Each Endpoint Now Shows

| Endpoint | Status | Data |
|----------|--------|------|
| `/api/diagnostic` | **NEW** | Row counts + system health |
| `/api/gti` | **LIVE** | Real GTI scores from DB |
| `/api/market/spy` | **LIVE** | Real SPY/VIX/GLD prices |
| `/api/signals` | **LIVE** | Real ML predictions |
| `/api/headlines` | **LIVE** | Real news sentiment |
| `/api/conflicts` | **LIVE** | Real geopolitical events |

---

## Scheduler Job Schedule

Once backfill complete:

| Job | Interval | What it does |
|-----|----------|-------------|
| RSS Fetcher | Every 5 min | Pulls news from Reuters, BBC, AJ, AP |
| GDELT Fetcher | Every 15 min | Geopolitical events from world news |
| NewsAPI Fetcher | Every 15 min | English-language headline sentiment |
| Market Fetcher | Every 15 min | SPY, VIX, GLD hourly OHLCV |
| GTI Aggregator | Every 15 min (+2min) | Combines signals into 0-1 score |
| Predictor | Every 15 min (+3min) | ML model inference |

---

## Troubleshooting

### "No GTI data" after 5 minutes?

1. Check scheduler terminal for errors
2. Manually test fetchers:
   ```powershell
   python backend/ingestion/market_fetcher.py
   python backend/ingestion/gdelt_fetcher.py
   ```

### "Models not found"?

Models are already trained. If missing:
```powershell
.\RUN.ps1 train
```

### Market data stuck at zero?

yfinance may be rate-limited. The fetcher auto-falls back to Stooq (slower). Wait 2-3 minutes.

### Scheduler keeps failing?

Check for missing dependencies:
```powershell
pip install apscheduler requests pandas yfinance pandas-datareader
```

---

## Once Running: Verify All Systems

```bash
# GTI score (geopolitical tension 0-1)
curl http://localhost:8000/api/gti | jq '.score'

# Latest market price
curl http://localhost:8000/api/market/spy | jq '.current_price'

# Volatility prediction
curl http://localhost:8000/api/signals | jq '.vol_prediction'

# Direction prediction
curl http://localhost:8000/api/signals | jq '.dir_prediction'

# All conflicts
curl http://localhost:8000/api/conflicts | jq '.total_events'
```

---

## Timeline

- **t=0s** → Run `.\RUN.ps1 start`
- **t=0-5s** → Services start (scheduler, API, frontend)
- **t=5-10s** → Scheduler begins backfill
- **t=10-120s** → Market data streams in
- **t=120-180s** → GDELT events loaded
- **t=180s+** → All endpoints return real data

**First API calls at t=180s** will return 0s (empty DB). **By t=300s**, expect full data.

---

## Next: The Dashboard

Once `/api/diagnostic` shows `data_ready: true`, open:
```
http://localhost:3000
```

Dashboard shows:
- **GTI Score** — real geopolitical tension
- **Market Data** — live SPY, VIX, GLD
- **ML Signals** — volatility + direction predictions
- **Conflict Map** — where the geopolitical events are
- **Asset Impact** — sector-by-sector performance

---

## File Locations

| Component | Location |
|-----------|----------|
| Models | `backend/prediction/models/` |
| Databases | `data/` (auto-created) |
| Logs | `logs/trading_bot.log` |
| Scheduler | `backend/scheduler.py` |
| API | `backend/api/main.py` |
| Config | `backend/config.py` |

---

**Status: READY TO RUN** 🚀

Run: `.\RUN.ps1 start`
