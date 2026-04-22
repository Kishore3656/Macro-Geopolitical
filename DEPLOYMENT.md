# GeoMarket Intelligence — Deployment & Setup

## Quick Start (Local Development)

### Prerequisites
- Python 3.10+
- pip or conda

### Installation & Setup

1. **Clone and install dependencies:**
```bash
cd geo-market-ml
pip install -r requirements.txt
```

2. **Initialize data (populate SQLite databases):**
```bash
python -m ingestion.gdelt_fetcher --backfill --days 7
python -m ingestion.rss_fetcher
```

3. **Train ML models (one-time):**
```bash
python prediction/train.py
```

4. **Run the backend API (in one terminal):**
```bash
uvicorn api.main:app --reload --port 8000
```

5. **Run the Streamlit dashboard (in another terminal):**
```bash
streamlit run app.py --server.port 8501
```

6. **Access the dashboard:**
- Open `http://localhost:8501` in your browser
- API docs available at `http://localhost:8000/docs`

---

## API Endpoints

All endpoints return JSON. CORS enabled.

### GTI (Geopolitical Tension Index)
- `GET /api/gti` — Current GTI score + components
- `GET /api/gti/history?hours=48` — Historical GTI readings

### ML Signals
- `GET /api/signals` — Latest predictions (volatility, direction, confidence)
- `GET /api/signals/history?limit=100` — Prediction history

### Headlines & Sentiment
- `GET /api/headlines?limit=20` — Latest news headlines with VADER sentiment

### Market Data
- `GET /api/market/spy?bars=100` — SPY OHLCV bars
- `GET /api/market/sectors` — Sector ETF performance

### Health
- `GET /health` — Server status
- `GET /` — API info

---

## Production Deployment (Vercel)

### Setup Vercel Project

1. **Link your repo to Vercel:**
```bash
npm install -g vercel
vercel link
```

2. **Configure environment variables in Vercel dashboard:**
```
GTI_DB=gti.db
NEWS_DB=news.db
MARKET_DB=market.db
PREDICTIONS_DB=predictions.db
API_BASE_URL=https://your-vercel-url.vercel.app
```

3. **Deploy:**
```bash
vercel deploy
```

### Architecture Notes

- **Streamlit frontend** deployed as serverless function
- **FastAPI backend** deployed as API route
- **SQLite databases** persisted in `/tmp` or Vercel Blob Storage (for production scale)
- **GDELT/RSS data** fetched via scheduled jobs (e.g., cron)

---

## Data Pipeline

### Real Data Sources

1. **GDELT v2 Events** — Global conflict/tone data
   - Updated every 15 minutes
   - Fetched by `ingestion/gdelt_fetcher.py`
   - Stored in `news.db` (`gdelt_events` table)

2. **RSS News Feeds** — Reuters, BBC, AP, Al Jazeera
   - Fetched by `ingestion/rss_fetcher.py`
   - Sentiment scored with VADER
   - Stored in `news.db` (`rss_articles` table)

3. **Market Data** — SPY OHLCV (hourly)
   - Fetched from Yahoo Finance / Alpha Vantage
   - Stored in `market.db` (`ohlcv` table)
   - Used as features for ML models

### GTI Computation (Every 15 min)

The GTI score (0.0–1.0) is computed from:
- **Conflict Ratio** (50% weight): GDELT events with GoldsteinScale < -5
- **Tone Index** (30% weight): Average GDELT AvgTone (-100 to +100)
- **VADER Sentiment** (20% weight): RSS headline compound score (-1 to +1)

Formula:
```
GTI = 0.50 * conflict_ratio + 0.30 * tone_norm + 0.20 * vader_norm
```

Result stored in `gti.db` (`gti_scores` table).

### ML Model Inference (Hourly)

LightGBM models predict:
- **Volatility**: HIGH or LOW (confidence 0–1)
- **Direction**: UP or DOWN (confidence 0–1)

Features include GTI, market technicals (returns, vol), and GDELT metrics.

Results stored in `predictions.db`.

---

## UI Sync with Real Data

### Earth Pulse Dashboard
- **GTI Hero**: Real GTI score from `/api/gti`
- **Signal Cards**: Conflict ratio, tone index, VADER sentiment
- **Global Heatmap**: Colors reflect GTI level
- **Headlines**: Real RSS feed with sentiment scores

### AI Signals Dashboard
- **Model Output**: Real LightGBM predictions from `/api/signals`
- **History Chart**: 24-hour prediction confidence trajectory
- **Asset Impact**: Bullish/neutral/bearish assets based on direction signal
- **Sentiment Momentum**: VADER sentiment breakdown from headlines

### Geo Map & Market Dashboards
- **SPY Price**: Real-time market data from `/api/market/spy`
- **Sector Performance**: From `/api/market/sectors`
- **Country Heatmap**: GTI by region (future enhancement)

---

## Monitoring & Troubleshooting

### API Health Check
```bash
curl http://localhost:8000/health
```

### Database Status
```bash
sqlite3 gti.db "SELECT COUNT(*) FROM gti_scores;"
sqlite3 news.db "SELECT COUNT(*) FROM gdelt_events;"
```

### Common Issues

| Issue | Solution |
|-------|----------|
| "Models not found" | Run `python prediction/train.py` |
| "No GTI data" | Run `python -m ingestion.gdelt_fetcher --backfill --days 1` |
| "No market data" | Fetch SPY bars first (requires Alpha Vantage API key in config) |
| API 500 error | Check `/health` endpoint, review API logs |

---

## Configuration

Edit `config.py` to customize:
- Data window sizes (GTI_WINDOW_HOURS, MAX_ROWS)
- Database paths
- Conflict/sentiment thresholds
- API port and CORS settings

---

## Disclaimer

This platform provides analytical intelligence only. It is not financial advice. Always do your own research and manage risk appropriately.
