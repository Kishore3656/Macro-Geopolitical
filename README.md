# GeoMarket Intelligence — Sovereign Intelligence Framework

A production-ready market and geopolitical analysis platform built with **React 19 + Next.js 15** (unified frontend) + **FastAPI** (backend). Real-time GTI scoring, AI-driven trading signals, and tactical intelligence dashboards with WebSocket streaming.

## Quick Start

### Run Everything
```bash
# 1. Start the FastAPI backend (provides all data)
uvicorn api.main:app --reload

# 2. Start the React/Next.js frontend
cd frontend && npm run dev
```

- **API Backend:** http://localhost:8000
- **Unified Frontend:** http://localhost:3000

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
├── api/                        # FastAPI backend (port 8000)
│   ├── main.py                # WebSocket + REST endpoints
│   └── client.py              # API client utilities
├── frontend/                  # React 19 + Next.js 15 unified UI
│   ├── src/
│   │   ├── app/              # Next.js 15 App Router (earth-pulse, geo-map, market, ai-signals)
│   │   ├── components/       # Dashboard components (EarthPulse, Market, GeoMap, AISignals)
│   │   ├── hooks/            # Custom hooks (useGTI, useMarket, useSignals, useWebSocket)
│   │   ├── store/            # Zustand state management (gtiStore, marketStore, signalsStore)
│   │   ├── types/            # TypeScript interfaces for all API responses
│   │   ├── lib/              # Utilities (api.ts for typed fetch wrapper)
│   │   └── components/ui/    # Reusable UI components (StatusBadge, SignalCard, etc.)
│   ├── .env.local             # NEXT_PUBLIC_API_URL=http://localhost:8000
│   └── package.json           # Dependencies (recharts, zustand, tailwind)
├── ingestion/                 # Data pipelines (GDELT, news, market data)
├── prediction/                # ML models (LightGBM inference)
├── nlp/                       # NLP utilities (VADER, entity extraction)
├── gti/                       # GTI computation and aggregation
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

- **Backend:** FastAPI (async, CORS-enabled, WebSocket streaming on /ws/gti, /ws/market, /ws/signals)
- **Frontend:** React 19 + Next.js 15 App Router (TypeScript, Tailwind CSS, Zustand state management)
- **Data:** SQLite databases (GTI, news, market, predictions)
- **ML:** LightGBM for trade signal generation
- **Real-time:** WebSocket connections with exponential backoff reconnection for live data streaming

The unified React frontend replaces the previous Streamlit UI and provides a modern, responsive experience with URL-based routing and real-time WebSocket updates.

## Installation

```bash
# Backend dependencies
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

## Running

**Start the backend first** (it must be running before the frontend):
```bash
uvicorn api.main:app --reload
```

**Then start the React/Next.js frontend:**

```bash
cd frontend && npm run dev
```

Visit **http://localhost:3000** and navigate through the four dashboards:
- **Earth Pulse:** GTI score, headlines, and active conflicts
- **Geo Map:** Country bilateral relations and geopolitical events
- **Market:** S&P 500 candlestick charts and sector performance
- **AI Signals:** ML predictions with confidence metrics and signal history

## Data Sources

- **GDELT Project v2:** Global conflict and event data
- **News Feeds:** Reuters, BBC, AP, Al Jazeera via RSS
- **Market Data:** Yahoo Finance / Alpha Vantage APIs
- **Local SQLite:** Cached GTI, news, market, prediction data

## Disclaimer

**Analytical intelligence only—not financial advice.** Always conduct your own research, manage risk with stops, and understand market conditions before trading. Signals are probabilistic, not guaranteed.