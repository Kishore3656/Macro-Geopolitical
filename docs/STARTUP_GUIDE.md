# Trading Bot Startup Guide

After the folder reorganization, use this guide to get the system running.

---

## New Folder Structure

The project has been reorganized into clear folders:

```
trading-bot-geo-market-ml/
├── backend/              # Python backend (scheduler, API, models, NLP, etc.)
├── frontend/             # React dashboard
├── docs/                 # All documentation
├── config/               # Configuration files
├── scripts/              # Utility scripts
├── tests/                # Test suite
├── data/                 # SQLite databases (gitignored)
├── logs/                 # Application logs (gitignored)
├── README.md            # Main documentation
├── FOLDER_STRUCTURE.md  # Detailed folder layout
└── STARTUP_GUIDE.md     # This file
```

See `FOLDER_STRUCTURE.md` for complete details.

---

## Quick Start (3 Commands)

### 1. Install Dependencies

```powershell
# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend && npm install
cd ..
```

### 2. Initialize Databases

```powershell
# Create database schema
python -c "import sys; sys.path.insert(0, 'backend'); from ingestion.db import init_all; init_all()"
```

### 3. Start Services

Open **3 PowerShell terminals** and run these commands (one per terminal):

**Terminal 1 - Scheduler (Background Jobs):**
```powershell
.\start-scheduler.ps1
```

**Terminal 2 - API Server:**
```powershell
.\start-api.ps1
```

**Terminal 3 - Frontend:**
```powershell
.\start-frontend.ps1
```

---

## Accessing the System

Once all three services are running:

- **Frontend Dashboard:** http://localhost:3000
- **API Server:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Health Check:** `curl http://localhost:8000/health`

---

## Step-by-Step Startup

### Prerequisites

- Python 3.11+
- Node.js 18+
- Git

### Step 1: Configuration

```powershell
# Copy environment template
Copy-Item config\.env.example config\.env

# Edit as needed (most defaults work for zero-cost mode)
# nano config/.env
```

### Step 2: Python Dependencies

```powershell
pip install -r requirements.txt

# Verify key packages
python -c "import fastapi, lightgbm, nltk, spacy; print('All packages OK')"
```

### Step 3: Frontend Dependencies

```powershell
cd frontend
npm install
npm run build  # Optional but recommended
cd ..
```

### Step 4: Initialize Databases

```powershell
# Create tables and schema
python -c "import sys; sys.path.insert(0, 'backend'); from ingestion.db import init_all; init_all()"

# Verify
python -c "import sys; sys.path.insert(0, 'backend'); from ingestion.db import get_all_dbs; print(f'Databases ready')"
```

### Step 5: Start Services

Open 3 new PowerShell windows in the project root:

**Window 1 - Scheduler (runs every 15 min):**
```powershell
.\start-scheduler.ps1

# You should see:
# [INFO] Starting Trading Bot Scheduler
# [INFO] GTI job scheduled for every 15 minutes
# [INFO] Market data fetch scheduled for every 5 minutes
```

**Window 2 - API Server (handles requests):**
```powershell
.\start-api.ps1

# You should see:
# INFO:     Uvicorn running on http://0.0.0.0:8000
# INFO:     Application startup complete
```

**Window 3 - Frontend (web dashboard):**
```powershell
.\start-frontend.ps1

# You should see:
# > ready - started server on 0.0.0.0:3000, url: http://localhost:3000
# > event compiled client and server successfully
```

### Step 6: Verify All Systems

In a 4th terminal, run health checks:

```powershell
# Check API
curl http://localhost:8000/health | jq '.'

# Should return:
# {
#   "status": "ok",
#   "timestamp": "2026-05-07T15:30:00Z"
# }

# Check signals endpoint
curl http://localhost:8000/api/signals | jq '.'

# Should return data including:
# - dir_prediction (UP/DOWN)
# - vol_prediction (LOW/MEDIUM/HIGH)
# - regime (risk-on/off/neutral/crisis)
# - narrative (text explanation)
```

### Step 7: Open Dashboard

Go to **http://localhost:3000** in your browser:

- See real-time signals
- View geopolitical risk map
- Check model status
- Configure LLM settings (gear icon)
- Watch live updates

---

## File Locations

| Purpose | Location |
|---------|----------|
| Python code | `backend/` |
| React app | `frontend/` |
| Config files | `config/` |
| Databases | `data/` (created on first run) |
| Logs | `logs/` (created on first run) |
| Backups | `backups/` (created automatically) |
| Tests | `tests/` |
| Documentation | `docs/` |

---

## Common Commands

### Backend Operations

```powershell
# From project root:
cd backend

# Train models manually
python prediction/train.py --lookback 30

# Run inference
python prediction/predict.py

# Compute GTI
python gti/aggregator.py

# Create database backup
python -c "from database.backup import backup_all_databases; backup_all_databases()"

# List available backups
python -c "from database.backup import list_available_backups; print(list_available_backups())"

# Restore from backup
python -c "from database.backup import restore_from_backup; restore_from_backup('20260507_143022')"
```

### Frontend Operations

```powershell
# From project root:
cd frontend

# Development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run tests
npm test
```

### Testing

```powershell
# From project root:

# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_api.py -v

# Run with coverage
python -m pytest tests/ --cov=backend --cov-report=html
```

---

## Troubleshooting

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'config'`

**Solution:** The import paths have been fixed to work from the new `backend/` location. Make sure you're running from the project root or the backend directory:

```powershell
# Run from project root:
cd backend
python scheduler.py

# OR from project root via wrapper:
.\start-scheduler.ps1
```

### API Won't Start

**Problem:** `Address already in use (port 8000)`

**Solution:** Port 8000 is already in use. Either:
1. Stop the existing process: `Get-Process python | Where-Object { $_.CommandLine -match "main.py" } | Stop-Process`
2. Use a different port: `python -m uvicorn backend.api.main:app --port 8001`

### Frontend Won't Start

**Problem:** `EADDRINUSE: address already in use 0.0.0.0:3000`

**Solution:** Port 3000 is in use. Use a different port:
```powershell
cd frontend
npm run dev -- -p 3001
```

### Database Errors

**Problem:** `sqlite3.OperationalError: no such table`

**Solution:** Reinitialize databases:
```powershell
cd backend
python -c "from ingestion.db import init_all; init_all()"
```

### Missing Dependencies

**Problem:** `ModuleNotFoundError: No module named 'lightgbm'`

**Solution:** Install dependencies:
```powershell
pip install -r requirements.txt
```

---

## Environment Variables

**Key configuration in `config/.env`:**

```env
# Database paths (auto-created)
DATA_DIR=../data
LOG_DIR=../logs

# Scheduler (how often to fetch data)
RSS_POLL_MINS=5
GDELT_POLL_MINS=15
MARKET_POLL_MINS=5
NEWSAPI_POLL_MINS=15

# LLM Settings (optional, free tier)
USE_LLM_SENTIMENT=false
LLM_PROVIDER=none  # Can be: none, ollama, huggingface
OLLAMA_API_URL=http://localhost:11434
HUGGINGFACE_API_KEY=

# API Settings
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
API_PORT=8000
```

See `config/.env.example` for all available options.

---

## System Architecture

```
Data Sources (GDELT, Yahoo Finance, RSS)
    ↓
backend/ingestion/ (fetchers, data cleaning)
    ↓
data/ (SQLite databases)
    ↓
backend/gti/ (GTI computation)
    ↓
backend/prediction/ (ML models)
    ↓
backend/nlp/ (Sentiment, NER, language)
    ↓
backend/api/main.py (FastAPI REST server)
    ↓
frontend/ (React dashboard)
    ↓
Browser (http://localhost:3000)
```

---

## Performance Notes

**Expected startup times:**
- API: 2-5 seconds
- Frontend: 5-10 seconds
- Scheduler: 3-5 seconds
- First GTI job: 10-15 seconds (subsequent: 5-10s)

**Resource usage (idle):**
- Backend: ~80-150 MB
- Frontend dev: ~200-300 MB
- Minimal CPU (<5%) between jobs

---

## Zero-Cost Mode

All components run with **zero API costs**:

- ✅ GDELT data: Free public dataset
- ✅ Market data: Yahoo Finance free
- ✅ News: RSS feeds free
- ✅ ML inference: LightGBM local
- ✅ Sentiment: VADER (NLTK) free
- ✅ LLM (optional): Ollama local OR HuggingFace free tier
- ✅ Database: SQLite file-based
- ✅ Frontend: React local development

To use optional paid LLMs, set environment variables:
```env
USE_LLM_SENTIMENT=true
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...
```

---

## Next Steps

1. **Verify all services are running** (3 terminals, all showing logs)
2. **Check dashboard** at http://localhost:3000
3. **Run health check** `curl http://localhost:8000/health`
4. **Check signals** `curl http://localhost:8000/api/signals | jq '.'`
5. **Configure settings** (click gear icon in dashboard)
6. **Read docs** in `docs/` folder for detailed information

---

## Support

**Quick Help:**
- `docs/START_HERE.md` — New user guide
- `docs/QUICK_START.md` — 5-minute setup
- `docs/PHASE_6_COMPLETION.md` — Final project summary
- `FOLDER_STRUCTURE.md` — Folder organization

**For issues:**
- Check log files: `logs/trading_bot.log`
- Check API logs: Terminal 2 (API server output)
- Check frontend logs: Terminal 3 (Frontend server output)

---

## Summary

| Step | Command | Expected Result |
|------|---------|-----------------|
| 1. Deps | `pip install -r requirements.txt` | All packages installed |
| 2. Config | Edit `config/.env` | Configuration ready |
| 3. DB | `python -c "..."` init_all` | Tables created |
| 4. Scheduler | `.\start-scheduler.ps1` | Jobs scheduled every 15 min |
| 5. API | `.\start-api.ps1` | Server running on 8000 |
| 6. Frontend | `.\start-frontend.ps1` | Dashboard on http://localhost:3000 |
| 7. Verify | `curl http://localhost:8000/health` | `{"status": "ok"}` |

---

**Status:** ✅ Ready to launch

**All systems organized and production-ready. Start the 3 services and enjoy!**

