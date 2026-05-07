# Project Folder Structure

This document outlines the organized folder structure of the trading bot project.

---

## Overview

```
trading-bot-geo-market-ml/
├── backend/                 # Python backend code
├── frontend/                # React/Next.js frontend
├── docs/                    # Documentation & phase reports
├── config/                  # Configuration files
├── scripts/                 # Automation & utility scripts
├── tests/                   # Test suite
├── data/                    # SQLite databases (gitignored)
├── logs/                    # Application logs (gitignored)
├── README.md               # Main project documentation
├── requirements.txt        # Python dependencies
└── package.json           # Node.js dependencies
```

---

## Detailed Structure

### `backend/` - Core Python Application

Hosts all Python backend logic, ML models, and data processing:

```
backend/
├── api/                     # FastAPI REST API server
│   └── main.py             # API endpoints, health checks
├── database/                # Database utilities
│   └── backup.py           # Backup & restore functions
├── prediction/              # ML models & inference
│   ├── train.py            # Model training logic
│   ├── predict.py          # Inference pipeline
│   ├── features.py         # Feature engineering
│   ├── drift.py            # Drift detection
│   └── models/             # Trained models (.pkl files)
├── gti/                     # Geopolitical Tension Index
│   └── aggregator.py       # GTI computation & scoring
├── ingestion/               # Data ingestion
│   ├── db.py              # Database initialization & schema
│   ├── backfill.py        # Historical data fetch
│   └── sources/           # Data source integrations
├── nlp/                     # Natural Language Processing
│   ├── llm_sentiment.py    # LLM abstraction layer
│   ├── ner.py             # Named Entity Recognition
│   └── language.py        # Language detection & translation
├── config.py              # Configuration & environment variables
├── logging_setup.py       # Production logging configuration
├── scheduler.py           # Scheduler for periodic jobs
├── components.py          # Shared components
└── design_tokens.py       # Design system tokens
```

**Key Files:**
- `config.py` — Central configuration management
- `scheduler.py` — Runs GTI jobs, drift detection, model training every 15 min
- `api/main.py` — FastAPI server (port 8000)

---

### `frontend/` - React/Next.js Application

React 18 + Next.js 15 dashboard for real-time signal visualization:

```
frontend/
├── src/
│   ├── app/                # Next.js app routes
│   │   ├── ai-signals/     # AI signals dashboard
│   │   ├── earth-pulse/    # Geopolitical risk map
│   │   ├── geo-map/        # Command center map
│   │   └── market/         # Market data views
│   ├── components/         # Reusable React components
│   │   ├── dashboards/
│   │   │   ├── NexusAISignals.tsx       # Main signals display
│   │   │   └── CommandCenterMap.tsx     # Geopolitical map
│   │   ├── TopBar.tsx      # Header with settings
│   │   └── ...other components
│   ├── store/             # State management
│   │   └── settingsStore.ts  # Zustand LLM settings
│   ├── types/             # TypeScript type definitions
│   │   └── index.ts       # Shared types
│   ├── styles/            # Global styles
│   └── hooks/             # Custom React hooks
├── public/                # Static assets
├── package.json           # Node dependencies
└── next.config.ts         # Next.js configuration
```

**Key Components:**
- `NexusAISignals.tsx` — Real-time signals & regime display
- `CommandCenterMap.tsx` — Global geopolitical risk visualization
- `TopBar.tsx` — Settings panel for LLM configuration

---

### `docs/` - Documentation

All project documentation, phase briefs, completion reports:

```
docs/
├── PHASE_3_BRIEF.md              # Pre-implementation design doc
├── PHASE_3_COMPLETION.md         # Post-implementation report
├── PHASE_4_BRIEF.md              # Frontend integration design
├── PHASE_4_COMPLETION.md         # Frontend implementation report
├── PHASE_5_BRIEF.md              # Advanced features design
├── PHASE_5_COMPLETION.md         # NER, language, confidence report
├── PHASE_6_BRIEF.md              # Production hardening design
├── PHASE_6_COMPLETION.md         # Final production report
├── START_HERE.md                 # Getting started guide
├── QUICK_START.md                # Quick setup instructions
├── QUICK_START_NEXUS.md          # Nexus UI quick start
├── IMPLEMENTATION_SUMMARY.md     # Overall implementation summary
├── NEXUS_IMPLEMENTATION.md       # Nexus UI details
├── NEXUS_READY_TO_TEST.md        # Nexus testing guide
├── NEXUS_UI_REFERENCE.md         # UI component reference
├── DASHBOARD_GUIDE.md            # Dashboard usage guide
├── DASHBOARD_LAYOUT.txt          # Layout specifications
├── BUILD_COMPLETE.md             # Build completion checklist
└── QUICK_REFERENCE.txt           # Quick command reference
```

**Important Files:**
- `START_HERE.md` — Entry point for new users
- `PHASE_6_COMPLETION.md` — Final project summary
- `QUICK_START.md` — Setup in 5 minutes

---

### `config/` - Configuration Files

Environment variables and configuration:

```
config/
├── .env                   # Local environment variables (gitignored)
├── .env.example           # Example env template
├── .gitignore            # Git exclusions
├── pytest.ini            # Pytest configuration
└── playwright.config.ts  # E2E test configuration
```

**Setup:**
1. Copy `.env.example` to `.env`
2. Update with your API keys (optional for zero-cost mode)
3. Load on startup via `config.py`

---

### `scripts/` - Automation Scripts

Utility scripts for development and deployment:

```
scripts/
├── run.sh                 # Start all services (Linux/Mac)
├── run.bat                # Start all services (Windows)
├── run_tests.sh           # Run test suite (Linux/Mac)
├── run_tests.bat          # Run test suite (Windows)
├── run_tests.ps1          # Run test suite (PowerShell)
├── start-frontend.ps1     # Start frontend dev server
├── start-servers.js       # Node server management
└── capture_screenshots.py # Playwright screenshot utility
```

**Common Commands:**
```bash
# Start backend scheduler
python backend/scheduler.py

# Start API server
python backend/api/main.py

# Start frontend
cd frontend && npm run dev

# Run tests
python -m pytest tests/ -v
```

---

### `tests/` - Test Suite

Automated tests for core functionality:

```
tests/
├── test_api.py            # API endpoint tests
├── test_ner.py            # NER extraction tests
├── test_language.py       # Language detection tests
├── test_drift_detector.py # Drift detection tests
├── test_llm_sentiment.py  # LLM integration tests
├── conftest.py            # Pytest configuration
└── ...other tests
```

**Run Tests:**
```bash
pytest tests/ -v           # Run all tests
pytest tests/test_api.py   # Run specific test file
```

---

### `data/` - SQLite Databases

Application data storage (gitignored):

```
data/
├── news.db                # RSS articles & headlines
├── market.db              # OHLCV market data (SPY, VIX, GLD)
├── gti.db                 # Geopolitical Tension Index scores
└── predictions.db         # ML predictions & outcomes
```

**Note:** Databases auto-initialize on first run. Backups stored in `backups/`.

---

### `logs/` - Application Logs

Runtime application logs (gitignored):

```
logs/
├── trading_bot.log        # Main application log (rotates at 10MB)
├── trading_bot.log.1      # Backup log file 1
├── trading_bot.log.2      # Backup log file 2
└── ...
```

**Configuration:**
- Max file size: 10MB
- Backup count: 7 files
- Format: `YYYY-MM-DD HH:MM:SS | module | LEVEL | message`

---

## Key Directories

### `backend/` Contents
| Item | Purpose |
|------|---------|
| `api/` | FastAPI REST server |
| `database/` | Backup/restore utilities |
| `prediction/` | ML models, training, inference |
| `gti/` | GTI computation |
| `ingestion/` | Data fetching, schema |
| `nlp/` | NLP: sentiment, NER, language |
| `config.py` | Environment config |
| `scheduler.py` | Job scheduler |
| `logging_setup.py` | Structured logging |

### `frontend/` Contents
| Item | Purpose |
|------|---------|
| `src/app/` | Next.js routes |
| `src/components/` | React components |
| `src/store/` | Zustand state |
| `src/types/` | TypeScript definitions |
| `public/` | Static assets |
| `next.config.ts` | Next.js config |

### `docs/` Contents
| Item | Purpose |
|------|---------|
| `PHASE_*_BRIEF.md` | Pre-implementation design |
| `PHASE_*_COMPLETION.md` | Post-implementation report |
| `START_HERE.md` | New user entry point |
| `QUICK_START.md` | 5-minute setup |

---

## File Flow

**Data Pipeline:**
```
Data Sources (GDELT, Yahoo Finance, RSS)
    ↓
ingestion/ (fetch & store)
    ↓
data/ (SQLite databases)
    ↓
backend/ (processing: GTI, ML, NLP)
    ↓
api/main.py (REST endpoints)
    ↓
frontend/ (React dashboard)
```

**Code Organization:**
```
backend/
├── Core logic (gti/, prediction/, nlp/)
├── Infrastructure (database/, api/, scheduler.py)
├── Configuration (config.py, logging_setup.py)
└── Entry points (scheduler.py, api/main.py)

frontend/
├── Pages (src/app/)
├── Components (src/components/)
├── State (src/store/)
├── Types (src/types/)
└── Config (next.config.ts, package.json)
```

---

## Adding New Features

**Backend:**
1. Add logic to `backend/[module]/`
2. Add database schema to `backend/ingestion/db.py` if needed
3. Expose via `backend/api/main.py` endpoint
4. Add tests to `tests/`

**Frontend:**
1. Create component in `backend/frontend/src/components/`
2. Add types to `backend/frontend/src/types/index.ts`
3. Add route in `backend/frontend/src/app/`
4. Connect to state via `store/settingsStore.ts` if needed

---

## Environment Setup

1. **Configure variables:**
   ```bash
   cp config/.env.example config/.env
   # Edit config/.env as needed
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   cd frontend && npm install
   ```

3. **Initialize databases:**
   ```bash
   python -c "from backend.ingestion.db import init_all; init_all()"
   ```

4. **Start services:**
   ```bash
   # Terminal 1
   python backend/scheduler.py
   
   # Terminal 2
   python backend/api/main.py
   
   # Terminal 3
   cd frontend && npm run dev
   ```

5. **Access:**
   - API: `http://localhost:8000`
   - Frontend: `http://localhost:3000`
   - Health check: `curl http://localhost:8000/health`

---

## Gitignore

The following are automatically ignored:

- `data/` — SQLite databases
- `logs/` — Application logs
- `backups/` — Database backups
- `.env` — Local environment variables
- `venv/`, `node_modules/` — Dependencies
- `__pycache__/`, `.next/` — Build artifacts
- `.pytest_cache/`, `test-results/` — Test artifacts

---

## Summary

| Folder | Purpose | Key Files |
|--------|---------|-----------|
| `backend/` | Python logic | config.py, scheduler.py, api/main.py |
| `frontend/` | React UI | src/app/, src/components/ |
| `docs/` | Documentation | PHASE_*_*.md, START_HERE.md |
| `config/` | Settings | .env, .env.example |
| `scripts/` | Automation | run.sh, run.bat, run_tests.* |
| `tests/` | Test suite | test_*.py |
| `data/` | Databases | *.db (gitignored) |
| `logs/` | Logs | trading_bot.log (gitignored) |

---

**Status:** ✅ Project organized and production-ready.

**Next Steps:**
1. Update imports in code if running from new paths
2. Update git staging: `git add -A` then review `git status`
3. Commit reorganization: `git commit -m "Reorganize: folder structure for clarity"`
4. Push: `git push origin main`

