# Geopolitical Tension Index — Market Prediction Dashboard

A fully local, CPU-only dashboard that monitors global geopolitical events every
15 minutes, scores world tension as a single number (GTI 0.0–1.0), and predicts
whether the stock market will be volatile or directional in the next hour.

Runs entirely on your machine. No GPU. No paid cloud services. Opens in your browser.

---

## What This Does

```
World News → Sentiment Scoring → GTI Score → LightGBM → Market Prediction
                                                  ↓
                                          Streamlit Dashboard
```

Every 15 minutes the system:
1. Downloads GDELT geopolitical event data (free, no key)
2. Polls Reuters, BBC, Al Jazeera, AP via RSS (free, no key)
3. Fetches top English headlines from NewsAPI (free, 100/day limit)
4. Downloads SPY, VIX, GLD price bars from Yahoo Finance or Stooq (free, no key)
5. Scores all headlines with VADER sentiment
6. Computes a GTI score from GDELT conflict data + VADER sentiment
7. Runs two LightGBM classifiers to predict next-hour volatility and direction
8. Updates the dashboard in your browser

---

## Hardware Requirements

| Spec | This Project |
|---|---|
| GPU | NOT required — everything runs on CPU |
| RAM | ~500MB peak (pandas + LightGBM — well within 8GB) |
| Disk | ~200MB for data after 30 days |
| CPU | Any modern Intel/AMD — model trains in 2–4 min |

---

## Project Structure

```
geo-market-ml/
│
├── ingestion/               ← pulls data from the internet into SQLite
│   ├── __init__.py
│   ├── db.py                ← creates all 4 SQLite databases
│   ├── gdelt_fetcher.py     ← GDELT CSV every 15 min
│   ├── rss_fetcher.py       ← RSS feeds every 5 min
│   ├── newsapi_fetcher.py   ← NewsAPI headlines, 100/day guard
│   └── market_fetcher.py    ← yfinance OHLCV every 15 min
│
├── nlp/
│   ├── __init__.py
│   └── sentiment.py         ← VADER headline scorer (CPU, instant)
│
├── gti/
│   ├── __init__.py
│   └── aggregator.py        ← combines 3 signals → GTI 0.0–1.0
│
├── prediction/
│   ├── __init__.py
│   ├── features.py          ← builds LightGBM feature matrix
│   ├── train.py             ← trains volatility + direction models
│   ├── predict.py           ← live single-row inference
│   └── backtest.py          ← accuracy check on held-out data
│
├── dashboard/
│   ├── __init__.py
│   └── app.py               ← Streamlit browser dashboard
│
├── api/
│   ├── __init__.py
│   └── main.py              ← FastAPI stub (commented out, for web deploy later)
│
├── data/                    ← created automatically, never commit
│   ├── news.db              ← GDELT events, RSS articles, NewsAPI headlines
│   ├── market.db            ← SPY/VIX/GLD OHLCV bars
│   ├── gti.db               ← GTI scores history
│   ├── predictions.db       ← model outputs history
│   └── newsapi_calls.json   ← daily call counter
│
├── prediction/models/       ← created by train.py, never commit
│   ├── lgbm_volatility.pkl
│   └── lgbm_direction.pkl
│
├── scheduler.py             ← runs all jobs on a timer (entry point)
├── config.py                ← all settings in one place
├── .env                     ← your API keys (never commit)
├── .env.example             ← template for .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## What Each Module Does

### `ingestion/db.py`
Creates four SQLite database files on first run.
Must be the first thing you run — every other module depends on these tables existing.

Tables created:
- `gdelt_events` — geopolitical events with GoldsteinScale and AvgTone
- `rss_articles` — headlines with VADER scores
- `newsapi_headlines` — English headlines with VADER scores
- `ohlcv` — hourly price bars for SPY, VIX, GLD
- `gti_scores` — computed GTI values over time
- `predictions` — model output history

### `ingestion/gdelt_fetcher.py`
Downloads GDELT v2 export ZIP files (TSV format, ~10k events per 15 min update).
Parses only 8 of the 61 columns we need (event ID, date, actors, CAMEO code,
GoldsteinScale, article count, tone). Inserts new events only — skips duplicates.

The `--backfill` flag downloads one EOD export per day going back N days.

### `ingestion/rss_fetcher.py`
Parses RSS feeds using feedparser. For each article title, runs VADER sentiment
and stores compound score + label (positive/negative/neutral). Deduplicates by
(title, source) so re-polling doesn't create double entries.

### `ingestion/newsapi_fetcher.py`
Calls the NewsAPI `/v2/top-headlines` endpoint. Tracks daily call count in
`data/newsapi_calls.json` and stops at 95/day (free tier limit is 100).
Resets automatically at midnight.

### `ingestion/market_fetcher.py`
Downloads OHLCV bars using a two-source fallback chain: Yahoo Finance 
(`Ticker.history()`) and Stooq (`pandas_datareader`). This avoids frequent
Yahoo IP blocks and `JSONDecodeError`s on `yf.download()`. Stores with
UNIQUE(symbol, timestamp) so re-fetching is safe.

### `nlp/sentiment.py`
VADER (Valence Aware Dictionary and sEntiment Reasoner) — a rule-based
sentiment analyser built for short texts like news headlines. Runs in
microseconds. No model download. No GPU. Returns compound score (-1 to +1)
and a text label.

### `gti/aggregator.py`
Combines three signals into one GTI score (0.0–1.0):

| Signal | Weight | Source |
|---|---|---|
| GDELT conflict ratio | 50% | Fraction of events with GoldsteinScale < -5 |
| GDELT media tone | 30% | Average AvgTone, inverted and normalised |
| VADER sentiment | 20% | Average RSS compound, inverted and normalised |

Higher GTI = more global tension. Runs over a configurable time window
(default 6 hours, set in config.py).

### `prediction/features.py`
Joins GTI scores and market bars on the hour. Computes:
- `returns_1h` — hourly price return
- `returns_4h` — 4-hour price return
- `vol_20h` — 20-bar rolling volatility (standard deviation of returns)

Targets for training:
- `target_vol` = 1 if next-hour abs return > rolling vol (unusual move)
- `target_dir` = 1 if next-hour close > current close (price up)

### `prediction/train.py`
Trains two LightGBM binary classifiers. Uses the last 20% of rows
(time-ordered) as a held-out test set — no shuffle, because shuffling
time series leaks future data into training. Saves `.pkl` files.

### `prediction/predict.py`
Pulls the single latest GTI row + last 25 market bars, assembles one
feature row, and runs both models. Saves the output to `predictions.db`.
Called every 15 minutes by the scheduler.

### `prediction/backtest.py`
Re-evaluates models on held-out data without retraining. Run monthly
to check for drift. If accuracy drops significantly, retrain with
more days: `python prediction/train.py --days 60`.

### `scheduler.py`
APScheduler BlockingScheduler — runs all jobs on timers. On startup
it runs every job once immediately so the dashboard has data right away,
then falls into the recurring schedule. Each job wraps its import in a
try/except so one failure never stops the others.

### `dashboard/app.py`
Streamlit app with custom "Tactical Archive" interface. We entirely replaced the standard, blocky Streamlit interface with a high-fidelity, custom-built frontend. We bypassed Streamlit's native component limitations by injecting a fully custom frontend payload (HTML/CSS/JS) directly into the app while keeping Python as the data engine.

GUI Architecture & Implementation Summary:
- **Design System ("Sovereign Intelligence Framework")**: Shifted from a generic SaaS look to a "Monastic Brutalism" / Military-Grade HUD style. Implemented a "Midnight Tonal Scale" (deep ink-blacks and dark navys) to reduce eye strain, highlighted by high-contrast neon accents (Cyan for primary data, Amber for warnings, Red for critical alerts, Green for positive trends). Applied custom web fonts (Orbitron, Share Tech Mono, Rajdhani) to distinguish data from UI.
- **Data Bridge (Real-Time Injection)**: Aggregated all live backend data into a single JSON dictionary (GTI Score, Conflict Counts, Predictions, Headlines). Injected directly into browser's global scope using `window.GeoMarketData = {...}` for instant JS access.
- **"Stitch" UI Component Integration**: Makes REST calls to local FastAPI server (`http://127.0.0.1:8000/ui/windows`) to dynamically fetch UI code. Renders with `streamlit.components.v1.html` as a full-screen iframe. Calls `st.stop()` to hide old Streamlit layout, ensuring pure custom frontend.
- **System Behavior**: Auto-refreshes every 60 seconds, pulling latest SQLite data and updating UI seamlessly without browser refresh.

---

## Technologies Used

| Library | Version | Why |
|---|---|---|
| requests | 2.31 | HTTP downloads (GDELT, NewsAPI) |
| feedparser | 6.0.11 | RSS feed parsing |
| newsapi-python | 0.2.7 | NewsAPI client |
| yfinance | 0.2.40 | Yahoo Finance market data |
| pandas-datareader | 0.10.0 | Stooq market data fallback |
| pandas | 2.2 | Data manipulation |
| numpy | 1.26 | Numerical operations |
| vaderSentiment | 3.3.2 | CPU-based headline sentiment |
| lightgbm | 4.3 | Fast gradient boosting classifier |
| scikit-learn | 1.4 | Train/test split, metrics |
| joblib | 1.3 | Model serialisation (.pkl) |
| APScheduler | 3.10 | Background job scheduling |
| streamlit | 1.33 | Browser dashboard |
| plotly | 5.20 | Interactive charts |
| python-dotenv | 1.0 | .env file loading |
| SQLite3 | stdlib | Zero-config local database |

No PyTorch. No TensorFlow. No GPU required. Total install ~400MB.

---

## Setup

```cmd
cd geo-market-ml
python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

copy .env.example .env
notepad .env
# → paste your free NewsAPI key (https://newsapi.org/register)

python -c "from ingestion.db import init_all; init_all()"

python -m ingestion.gdelt_fetcher --backfill --days 30
python -m ingestion.market_fetcher --backfill --days 30

python -m prediction.train

python scheduler.py
```

Open a second terminal:
```cmd
cd geo-market-ml
venv\Scripts\activate
streamlit run dashboard\app.py
```

Dashboard opens at http://localhost:8501

---

## Config Reference (`config.py`)

| Variable | Default | Meaning |
|---|---|---|
| `GDELT_POLL_MINS` | 15 | How often to fetch GDELT |
| `RSS_POLL_MINS` | 5 | How often to poll RSS feeds |
| `NEWSAPI_POLL_MINS` | 15 | How often to call NewsAPI |
| `MARKET_POLL_MINS` | 15 | How often to fetch prices |
| `GTI_WINDOW_HOURS` | 6 | Hours of data used to compute GTI |
| `GTI_CONFLICT_THRESHOLD` | -5.0 | GoldsteinScale below this = conflict event |
| `VADER_COMPOUND_THRESHOLD` | -0.05 | Below this = negative sentiment |
| `NEWSAPI_DAILY_LIMIT` | 95 | Max NewsAPI calls per day (limit is 100) |
| `MAX_ROWS` | 500 | SQLite row fetch cap (RAM guard) |
| `SYMBOLS` | SPY, VIX, GLD | Market symbols to track |

---

## Important Rules

- Never commit `.env` (contains your API key)
- Never commit `data/` or `prediction/models/` (large, local-only)
- Never load more than 500 rows at once from SQLite (8GB RAM limit)
- GDELT backfill for 30 days takes 15–30 minutes — don't interrupt it
- Run `init_all()` before running any fetcher
- Retrain monthly if backtest accuracy drops
