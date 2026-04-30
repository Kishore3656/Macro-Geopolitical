# GeoMarket Intelligence — Sovereign Intelligence Framework

A production-ready market and geopolitical analysis platform built with **Streamlit** (primary UI) + **FastAPI** (backend) + **React/Next.js** (optional modern frontend). Real-time GTI scoring, AI-driven trading signals, and tactical intelligence dashboards.

## Quick Start

### Run Everything
```bash
# 1. Start the FastAPI backend (provides all data)
uvicorn api.main:app --reload

# 2. Start the Streamlit UI (primary dashboard)
streamlit run app.py

# 3. Optionally, start the React frontend
cd frontend && npm run dev
```

- **Streamlit UI:** http://localhost:8501
- **API Backend:** http://localhost:8000
- **React Frontend (optional):** http://localhost:3000

## Features

### Geopolitical Tension Index (GTI)
- Real-time proprietary index (0.0 to 1.0) from GDELT v2 event data
- Global tone analysis, VADER sentiment scoring
- Historical tracking and anomaly detection

### AI Trading Signals
- LightGBM-trained ML models on SPY OHLCV + GTI features
- Directional predictions (UP/DOWN), confidence metrics, volatility expectations
- Live inference from latest market data

### Four Core Dashboards
- **Earth Pulse:** Global markets, capital flows, economic indicators
- **Geo Map:** Country-level geopolitical heatmaps, currency flows, commodities
- **Market:** S&P 500 analysis, sector rankings, technical indicators
- **AI Signals:** ML-generated trade signals with confidence scores

## Project Structure

```
├── app.py                     # Streamlit primary UI
├── styles.css                 # Custom styling
├── api/
│   ├── main.py               # FastAPI backend (port 8000)
│   └── client.py             # API client utilities
├── ui/                        # Streamlit UI components
├── ingestion/                 # Data pipelines (GDELT, news, market data)
├── prediction/                # ML models (LightGBM inference)
├── nlp/                       # NLP utilities (VADER, entity extraction)
├── gti/                       # GTI computation and aggregation
├── frontend/                  # React 19 + Next.js 15 (optional modern UI)
│   ├── src/components/        # Dashboard components
│   ├── .env.local             # Points to API backend
│   └── package.json           # Dependencies
└── tests/                     # Test suites
```

## API Endpoints

All endpoints live on `http://localhost:8000`:

| Endpoint | Method | Response |
|----------|--------|----------|
| `/health` | GET | Server status |
| `/api/gti` | GET | Current GTI score + components |
| `/api/gti/history` | GET | Last N GTI readings |
| `/api/signals` | GET | Current ML predictions |
| `/api/headlines` | GET | Latest headlines + sentiment |
| `/api/market/spy` | GET | S&P 500 OHLCV + technicals |
| `/api/market/sectors` | GET | Sector performance |

WebSocket support for real-time streaming at `/ws/{topic}`.

## Architecture

- **Backend:** FastAPI (async, CORS-enabled, WebSocket support)
- **Primary UI:** Streamlit (reactive, stateful)
- **Optional Frontend:** React 19 + Next.js 15 (modern, responsive, TypeScript)
- **Data:** SQLite databases (GTI, news, market, predictions)
- **ML:** LightGBM for trade signal generation

Both UIs fetch from the same FastAPI backend. Run them simultaneously or independently.

## Installation

```bash
# Backend dependencies
pip install -r requirements.txt

# Frontend (optional)
cd frontend
npm install
```

## Running

**Start the backend first** (it must be running before UIs):
```bash
uvicorn api.main:app --reload
```

**Then start your preferred UI:**

Streamlit (primary, recommended):
```bash
streamlit run app.py
```

Or React (modern alternative):
```bash
cd frontend && npm run dev
```

## Data Sources

- **GDELT Project v2:** Global conflict and event data
- **News Feeds:** Reuters, BBC, AP, Al Jazeera via RSS
- **Market Data:** Yahoo Finance / Alpha Vantage APIs
- **Local SQLite:** Cached GTI, news, market, prediction data

## Disclaimer

**Analytical intelligence only—not financial advice.** Always conduct your own research, manage risk with stops, and understand market conditions before trading. Signals are probabilistic, not guaranteed.