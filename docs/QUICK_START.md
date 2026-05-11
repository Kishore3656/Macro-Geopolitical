# Quick Start - 60 Seconds to Live Trading Data

## TL;DR - Run This:
```powershell
cd "d:\trading bot\geo-market-ml"
.\RUN.ps1 start
```

**Wait 2-3 minutes.** Dashboard opens at http://localhost:3000.

---

## That's It!

The system will:
1. Backfill 30 days of geopolitical + market data
2. Compute real GTI scores (geopolitical tension)
3. Run ML predictions (volatility + direction)
4. Stream live updates every 15 minutes

---

## Verify It's Working

```bash
# Check system health
curl http://localhost:8000/api/diagnostic | jq '.data_ready'

# Should return: true (after 2-3 min)

# View GTI score
curl http://localhost:8000/api/gti | jq '.score'

# View market price
curl http://localhost:8000/api/market/spy | jq '.current_price'

# View ML predictions
curl http://localhost:8000/api/signals | jq '.vol_prediction'
```

---

## 3 Terminals, 3 Services

When you run `.\RUN.ps1 start`:

| Terminal | Service | Port | What to watch |
|----------|---------|------|---------------|
| 1 | Scheduler | (background) | Data fetching every 15 min |
| 2 | API | 8000 | http://localhost:8000/health |
| 3 | Frontend | 3000 | http://localhost:3000 |

---

## Endpoints Cheat Sheet

```bash
curl http://localhost:8000/api/diagnostic        # System health
curl http://localhost:8000/api/gti               # GTI score (geopolitical tension)
curl http://localhost:8000/api/signals           # ML predictions
curl http://localhost:8000/api/market/spy        # S&P 500 prices
curl http://localhost:8000/api/conflicts         # Geopolitical events
curl http://localhost:8000/api/headlines         # News sentiment
```

---

## If Nothing Shows Up After 3 Minutes

**Check diagnostic:**
```bash
curl http://localhost:8000/api/diagnostic
```

If `"status": "incomplete"`, check the `"issues"` list. Most common:
- `"No SPY data"` → Market fetch in progress (wait 30s)
- `"No GDELT events"` → Geopolitical data backfilling (normal, takes 1-2 min)
- `"Models not found"` → Run `.\RUN.ps1 train`

---

## Individual Services (if needed)

```powershell
.\RUN.ps1 scheduler   # Just run background jobs
.\RUN.ps1 api        # Just start API server
.\RUN.ps1 frontend   # Just start dashboard
.\RUN.ps1 train      # Retrain ML models
.\RUN.ps1 help       # Show all commands
```

---

## Stop Services

In any terminal: **Ctrl+C**

All services will stop gracefully.

---

**Status:** ✅ Ready to run  
**Next Step:** `.\RUN.ps1 start`
