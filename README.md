# Trading Bot: Geopolitical Intelligence + ML Predictions

A production-grade system combining geopolitical data, sentiment analysis, and machine learning to generate real-time market signals. Powered by GDELT, LightGBM, and optional LLM sentiment analysis.

## Features

### Core Capabilities
- **Geopolitical Tension Index (GTI)**: Real-time market risk assessment based on global conflict data
- **ML Predictions**: Direction (UP/DOWN) and volatility (LOW/MEDIUM/HIGH) predictions using LightGBM
- **Sentiment Analysis**: Headlines analyzed via VADER (always available) or optional LLM (Ollama/HuggingFace)
- **Market Regime Detection**: Automatic classification (risk-on/risk-off/crisis/neutral)
- **Named Entity Recognition**: Extract financial entities (stocks, commodities, countries) from headlines
- **Multi-Language Support**: Auto-translate non-English headlines for analysis
- **Confidence Scoring**: Regime prediction confidence based on consensus (0-100%)

### Advanced Features
- **Real-Time API**: FastAPI backend with WebSocket support for live updates
- **React Dashboard**: Modern web UI with Tailwind CSS (Next.js 15)
- **Drift Detection**: Automatic model retraining when accuracy drops
- **Production Logging**: Structured logging with rotation and file archival
- **Database Backups**: Daily timestamped backups with retention policy
- **Health Monitoring**: System status endpoints for all components

### Cost
**Zero API Costs** - Uses free tier or local services:
- GDELT: Free event data
- Ollama: Local LLM (free)
- HuggingFace: Free tier (30k req/month)
- VADER: Built-in NLTK sentiment
- SQLite: File-based databases (free)

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+ (for frontend)
- 4GB RAM, 2GB disk

### 1. Clone & Setup
```bash
git clone https://github.com/kishore3656/trading-bot-geo-market-ml.git
cd trading-bot-geo-market-ml

# Python dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Frontend dependencies
cd frontend && npm install && cd ..
```

### 2. Initialize Databases
```bash
python -c "from ingestion.db import init_all; init_all()"
```

### 3. Start Scheduler
```bash
python scheduler.py
# Runs every 15 min: fetches news, computes GTI, runs ML inference
```

### 4. Start API Server
```bash
python api/main.py
# Server on http://localhost:8000
```

### 5. Start Frontend (Optional)
```bash
cd frontend && npm run dev
# Frontend on http://localhost:3000
```

## Status

**Phase 7 Complete** - Production-ready system with:
- Phases 1-6 fully implemented
- **Phase 7: ML accuracy +5-10pp** (27 technical indicators)
- Live geopolitical data integration from GDELT
- Error handling + logging
- Health checks + real-time monitoring
- Database backups
- Complete documentation
- Full training pipeline

## Quick Start

**See [docs/00_MASTER_SETUP.md](docs/00_MASTER_SETUP.md)** ← Start here!

Or run one command:
```bash
.\run.bat
# Then open http://localhost:3000
```

## Documentation

- **[docs/00_MASTER_SETUP.md](docs/00_MASTER_SETUP.md)** ← Start here
- [docs/LIVE_REGIONS_DATA.md](docs/LIVE_REGIONS_DATA.md) - Real geopolitical data wiring
- [docs/ML_IMPROVEMENTS.md](docs/ML_IMPROVEMENTS.md) - Phase 7 ML improvements
- [docs/PHASE_7_SUMMARY.md](docs/PHASE_7_SUMMARY.md) - What's new in Phase 7
- [docs/NEXUS_IMPLEMENTATION.md](docs/NEXUS_IMPLEMENTATION.md) - Full technical details
- [DEPLOYMENT.md](DEPLOYMENT.md) - Production deployment

## Support

For issues, questions, or suggestions:
1. Check logs: `tail -f logs/trading_bot.log`
2. Run health check: `curl http://localhost:8000/api/status`
3. Review troubleshooting in [DEPLOYMENT.md](DEPLOYMENT.md)

---

**Status**: Production-ready (All phases complete)
