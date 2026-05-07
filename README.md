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
**Zero API Costs** — Uses free tier or local services:
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
\\\ash
git clone https://github.com/kishore3656/trading-bot-geo-market-ml.git
cd trading-bot-geo-market-ml

# Python dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Frontend dependencies
cd frontend && npm install && cd ..
\\\

### 2. Initialize Databases
\\\ash
python -c "from ingestion.db import init_all; init_all()"
\\\

### 3. Start Scheduler
\\\ash
python scheduler.py
# Runs every 15 min: fetches news, computes GTI, runs ML inference
\\\

### 4. Start API Server
\\\ash
python api/main.py
# Server on http://localhost:8000
\\\

### 5. Start Frontend (Optional)
\\\ash
cd frontend && npm run dev
# Frontend on http://localhost:3000
\\\

## Status

**Phase 6 Complete** ? Production-ready system with:
- Phases 1-5 fully implemented
- Error handling + logging
- Health checks
- Database backups
- Documentation
- Tests
- CI/CD pipeline
- Docker support

See [PHASE_1_COMPLETION.md](PHASE_1_COMPLETION.md) through [PHASE_6_COMPLETION.md](PHASE_6_COMPLETION.md) for detailed phase reports.

## Documentation

- [README.md](README.md) — This file
- [DEPLOYMENT.md](DEPLOYMENT.md) — Production deployment guide
- [ARCHITECTURE.md](ARCHITECTURE.md) — System architecture and data flow
- [PHASE_6_BRIEF.md](PHASE_6_BRIEF.md) — Phase 6 overview

## Support

For issues, questions, or suggestions:
1. Check logs: \	ail -f logs/trading_bot.log\
2. Run health check: \curl http://localhost:8000/api/status\
3. Review troubleshooting in [DEPLOYMENT.md](DEPLOYMENT.md)

---

**Status**: Production-ready (All phases complete)
