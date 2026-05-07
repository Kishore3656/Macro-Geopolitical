# 🚀 START HERE - GeoMarket Trading Bot

## Quick Start (3 Steps)

### Step 1: Train ML Models (First Time Only)

```powershell
# From project root, run:
.\RUN.ps1 train

# Or directly:
.\scripts\train-models.ps1
```

**What happens:**
- Initialize SQLite databases
- Download 60 days of market data (GDELT, Yahoo Finance, RSS)
- Build feature matrix with 27 technical indicators
- Train 2 ML models (direction & volatility)
- Save trained models to: `backend/prediction/models/`

**Expected time:** 5-10 minutes

**Expected output:**
```
✓ Models trained!
✓ Saved to backend/prediction/models/lgbm_direction.pkl
✓ Saved to backend/prediction/models/lgbm_volatility.pkl
```

---

### Step 2: Start 3 Services

```powershell
# All at once:
.\RUN.ps1 start

# Or manually in 3 separate terminals:
.\scripts\start-scheduler.ps1     # Terminal 1 - Background jobs
.\scripts\start-api.ps1           # Terminal 2 - REST API (port 8000)
.\scripts\start-frontend.ps1      # Terminal 3 - Dashboard (port 3000)
```

**Services:**
- **Scheduler:** Runs background jobs (GTI, model training)
- **API:** REST endpoints (http://localhost:8000)
- **Frontend:** React dashboard (http://localhost:3000)

---

### Step 3: Open Dashboard

```
http://localhost:3000
```

You'll see:
- 🎯 Real-time signals (UP/DOWN with confidence)
- 📊 Volatility predictions
- 🗺️ Geopolitical risk map
- 📈 Technical indicators
- 📰 Latest news

---

## Folder Organization

```
📁 Project Root
├── RUN.ps1                    ← Main entry point (use this!)
├── FOLDER_GUIDE.md            ← Folder structure explained
├── FOLDER_GUIDE.md            ← Quick reference
│
├── backend/
│   └── prediction/models/     ← ✨ TRAINED MODELS SAVED HERE
│       ├── lgbm_direction.pkl
│       ├── lgbm_volatility.pkl
│       ├── model_registry.json
│       └── archive/           ← Previous versions
│
├── scripts/                   ← Ready-to-run startup scripts
│   ├── train-models.ps1
│   ├── start-scheduler.ps1
│   ├── start-api.ps1
│   ├── start-frontend.ps1
│   └── run_tests.ps1
│
├── utils/                     ← Training utilities
│   └── setup_and_train.py
│
├── docs/                      ← All documentation
│   ├── PHASE_7_SUMMARY.md
│   ├── TRAIN_INSTRUCTIONS.md
│   ├── ML_IMPROVEMENTS.md
│   └── ... (19+ guides)
│
├── data/                      ← Runtime databases (auto-created)
│   ├── gti.db
│   ├── market.db
│   ├── news.db
│   └── predictions.db
│
└── logs/                      ← Application logs
    └── trading_bot.log
```

---

## Available Commands

```powershell
# Training
.\RUN.ps1 train                 # Train ML models (5-10 min)
.\RUN.ps1 train -Days 90        # Train with 90 days of data

# Run Services
.\RUN.ps1 start                 # Start all 3 services
.\RUN.ps1 scheduler             # Start scheduler only
.\RUN.ps1 api                   # Start API only
.\RUN.ps1 frontend              # Start frontend only

# Info
.\RUN.ps1 help                  # Show help
```

---

## What's New (Phase 7)

✅ **Improved ML Accuracy:** +5-10 percentage points
- Enhanced hyperparameters
- 8 new technical indicators (RSI, MACD, Bollinger Bands, ATR, etc.)
- Better training evaluation

✅ **Organized Structure:** Clean folder layout
- `scripts/` for startup scripts
- `utils/` for training
- `docs/` for documentation
- `backend/prediction/models/` for trained models

✅ **Easy Training:** One-command pipeline
```powershell
.\RUN.ps1 train
```

---

## Troubleshooting

### Models not found?
Train them first:
```powershell
.\RUN.ps1 train
```

### Port 3000 or 8000 already in use?
Use different ports:
```powershell
cd frontend
npm run dev -- -p 3001  # Frontend on 3001

# For API, change start-api.ps1:
python -m uvicorn backend.api.main:app --port 8001
```

### Dashboard shows old data?
Clear cache:
```
Ctrl+Shift+Delete → Clear all → Refresh F5
```

### Need more details?
See:
- `docs/TRAIN_INSTRUCTIONS.md` - Training guide
- `docs/PHASE_7_SUMMARY.md` - Phase overview
- `docs/ML_IMPROVEMENTS.md` - Technical details
- `FOLDER_GUIDE.md` - Folder structure

---

## Next Steps

1. ✅ Run `.\RUN.ps1 train` (takes 5-10 min)
2. ✅ Run `.\RUN.ps1 start` (opens 3 terminals)
3. ✅ Open http://localhost:3000 in browser
4. ✅ Watch real-time predictions!

---

**Ready to go? Run:**
```powershell
.\RUN.ps1 train
```
