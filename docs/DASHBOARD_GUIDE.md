# Unified Trading Dashboard Guide

## Overview

The new **Unified Dashboard** is your real-time trading command center, combining ML signals, live market data, and geopolitical intelligence into a single interface.

**Access:** Open http://localhost:3000 (or the Dashboard nav link)

---

## Dashboard Sections

### 1. **Primary Alert Band** (Top Three Cards)
Three high-impact cards showing the most critical trading information:

#### AI Signal Card (Green/Red)
- **Current ML Prediction**: UP or DOWN
- **Confidence Score**: 0-100% (based on LightGBM model)
- **Volatility Level**: LOW/MEDIUM/HIGH
- Color: Green for bullish, red for bearish

#### Market Status Card
- **SPY Price**: Current S&P 500 ETF price
- **Daily Change %**: Intraday performance
- **Market Stance**: BULLISH or BEARISH indicator
- Color: Green for positive moves, red for negative

#### Geopolitical Risk Card
- **GTI Score**: 0-100 (Geo-Temporal Tension Index)
- **Risk Level**: CRITICAL (60+) / ELEVATED (40-60) / NORMAL (<40)
- **Event Count**: Recent geopolitical incidents
- Color: Red/amber/green based on tension level

---

### 2. **Main Data Grid** (Middle Section)

#### Left: Signal Performance Table
Shows your **top 5 most recent ML predictions** with:
- Timestamp (exact time of prediction)
- Direction (UP ↑ or DOWN ↓)
- Direction Probability (0-100%)
- Volatility Rating (LOW/MEDIUM/HIGH)

*Useful for:* Reviewing recent signal accuracy, identifying volatility patterns, back-testing confidence levels

#### Right: Key Metrics
- **Top Sectors**: 4 leading market sectors with % performance change
- **Critical Zones**: Bilateral relations with highest stress (country pairs at risk)

---

### 3. **Bottom Data Tables** (Full Width)

#### Bilateral Relations (Left)
Complete list of **country-to-country tensions** with:
- Country pair (e.g., "China ↔ Taiwan")
- Recent event count
- Stress level (0-10 scale shown as visual bar)
- Color coding: Red=critical, amber=tense, gray=stable

*Useful for:* Understanding geopolitical risk exposure, identifying emerging tensions

#### Geopolitical Events (Right)
**Last 10 recent global events** with:
- Country + location
- Event type (protest, military exercise, agreement, etc.)
- Goldstein scale intensity (0-10)
- Timestamp
- Color: Red=high intensity (>7), amber=medium (4-7), green=low (<4)

*Useful for:* Breaking news monitoring, understanding what's driving market volatility

---

## Data Refresh

All data updates in real-time via the backend API:
- **Signals**: Updated every analysis cycle (check your ML pipeline schedule)
- **Market Data**: Updated hourly (SPY bars) or real-time if subscribed
- **Geopolitical Data**: Updated as events are ingested (GDELT + NewsAPI)

---

## How to Use as a Trader

### Morning Routine
1. Check **AI Signal** - Is it UP or DOWN? What's the confidence?
2. Check **GTI Score** - Any geopolitical risks today?
3. Review **Recent Events** - What's driving market sentiment?
4. Check **Market Status** - Is SPY confirming the ML signal?

### During Trading
- Monitor **Signal Performance Table** for new predictions
- Watch **Bilateral Relations** for sudden spikes in tension
- Track **Geopolitical Events** for breaking news

### Decision-Making Framework
```
IF AI Signal = UP AND Market Bullish AND GTI Normal
  → Consider long positions
  
IF AI Signal = UP BUT GTI Critical AND Recent Geopolitical Events
  → Caution: geopolitical risk may override signal
  
IF AI Signal = DOWN AND GTI Elevated
  → Strong signal to avoid risk
```

---

## Drill-Down Pages

For deeper analysis, use the sidebar to access:
- **Earth Pulse**: Full GTI metrics with tension index trend chart
- **Geo Map**: Detailed bilateral relations and event maps
- **Market**: SPY candlestick chart, sector deep dive
- **AI Signals**: Signal history, confidence timeline, performance metrics

---

## Data Schema Reference

### Signal Object
```json
{
  "direction": "UP|DOWN",
  "confidence": 0-1,        // Overall signal confidence
  "direction_prob": 0-1,    // Probability of direction
  "volatility": "LOW|MEDIUM|HIGH"
}
```

### GTI (Geopolitical Tension Index)
```json
{
  "score": 0-1,             // Normalized 0-1, display as 0-100
  "risk_level": "LOW|MEDIUM|HIGH",
  "sentiment": -100 to 100,
  "volatility": 0-100
}
```

### Bilateral Relation
```json
{
  "country1": "string",
  "country2": "string",
  "stress_level": 0-10,
  "stress_category": "stable|tense|critical",
  "recent_events": number
}
```

### Geopolitical Event
```json
{
  "country": "string",
  "location": "string",
  "event_type": "string",
  "goldstein_scale": -10 to 10,  // Display as 0-10
  "timestamp": "ISO-8601"
}
```

---

## Configuration

### Environment Variables
Set in `.env.local` (frontend):
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Color Scheme
- **Green** (#10b981, #34d399): Bullish, low risk, positive sentiment
- **Red** (#ef4444, #f87171): Bearish, high risk, critical alerts
- **Amber** (#f59e0b, #fbbf24): Caution, elevated risk, medium concern
- **Cyan** (#06b6d4, #22d3ee): Information, confidence, data points

---

## Troubleshooting

**"Loading..." persists**
- Check backend is running: `http://localhost:8000/docs`
- Verify CORS is enabled in FastAPI

**Cards show "-" or null values**
- Ingestion pipeline may not have populated data yet
- Check API endpoint: `curl http://localhost:8000/api/gti`

**Events/Relations not updating**
- Check GDELT and NewsAPI data fetchers are running
- Review `ingestion/` logs for errors

---

## Next Steps

1. **Deploy**: Follow Vercel deployment guide when ready for production
2. **Integrate Real-Time Updates**: Add WebSocket support for live signal streaming
3. **Add Alerts**: Implement push notifications for critical GTI threshold breaches
4. **Custom Rules**: Build a rules engine to auto-trigger trades based on signal + GTI combination

