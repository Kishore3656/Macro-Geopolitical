# GeoMarket Intelligence — Sovereign Intelligence Framework

GeoMarket Intelligence is a robust, Streamlit-based market and geopolitical analysis dashboard. It aggregates global news, conflict data, and market metrics to provide real-time, AI-driven trading signals and risk assessments.

## Features

- **Geopolitical Tension Index (GTI):** A proprietary index (0.0 to 1.0) built from real-time GDELT conflict data, global tone analysis, and VADER sentiment analysis on news headlines.
- **AI Trading Signals:** Machine learning predictions (using LightGBM) trained on SPY OHLCV and GTI features, offering directional calls (UP/DOWN), volatility expectations, and confidence scoring.
- **Tactical Dashboards:**
  - **Earth Pulse:** Global markets, capital flows, and economic calendar.
  - **Geo Map:** Country-level heatmaps, currency intelligence, and commodity tracking.
  - **Market:** S&P 500 deep-dive, sector rankings, and technical signals.
  - **AI Signals:** Live ML-generated trade signals and anomaly detection.

## Project Structure

- `app.py`: Main Streamlit application entry point.
- `styles.css`: Custom Sovereign Intelligence Framework UI styling.
- `ui/`: User interface components and page layouts (e.g., `trading_guide.py`).
- `ingestion/`: Data pipelines and fetchers.
  - `gdelt_fetcher.py`: Downloads and parses GDELT v2 event data into a local SQLite database.

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/geo-market-ml.git
   cd geo-market-ml
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize Data (GDELT Backfill):**
   Fetch the last 30 days of GDELT events to populate the local SQLite database.
   ```bash
   python -m ingestion.gdelt_fetcher --backfill --days 30
   ```

4. **Run the Dashboard:**
   ```bash
   streamlit run app.py
   ```

## Data Sources

- **GDELT Project (v2):** Global Database of Events, Language, and Tone for conflict monitoring.
- **News RSS Feeds:** Reuters, BBC, AP, Al Jazeera.
- **Market Data:** (e.g., Yahoo Finance / Alpha Vantage)

## Disclaimer

**This platform provides analytical intelligence only. It is not financial advice.** Always do your own research, manage your risk (e.g., using stop-losses), and understand market conditions before trading. Signals are probabilistic, not guaranteed.