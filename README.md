# Sovereign Intelligence Framework

## The Tactical Archive

A military-grade market intelligence dashboard featuring **Monastic Brutalism** design principles—a fusion of stark technical precision and editorial authority. Built for high-consequence decision-making in global financial markets.

### Core Aesthetic

- **Midnight Tonal Scale:** Dark surfaces (0c0e14 → 33343b) minimize eye fatigue
- **Amber Pulse:** Critical alerts and live status via #ffb867 accent
- **No Borders:** Tonal shifts define boundaries, not 1px lines
- **Precision:** Hard (0px) corner radius reinforces tactical accuracy
- **Typography War:** Lora serif for narrative authority + JetBrains Mono for data alignment

---

## Architecture

### Views

1. **🎯 Tactical Archive** - Real-time market surveillance and strategic analysis
   - Market overview metrics (S&P 500, volatility, sentiment)
   - Critical alerts with severity ranking
   - Sector intelligence breakdown
   - Portfolio impact analysis
   - Geopolitical context
   - 24-hour forecasts

2. **🌍 Earth Pulse** - Geospatial market intelligence
   - Global market heatmap by region
   - Exchange-by-exchange performance (NYSE, LSE, TSE, SSE, DAX, ASX)
   - Capital flow patterns (inbound/outbound)
   - Geo-risk markers (geopolitical events)
   - Economic calendar (next 7 days)
   - Market synchronization analysis

3. **📈 Market Intelligence** - Deep equity analysis
   - Market overview (S&P 500, NASDAQ, DOW, VIX)
   - Sector performance rankings (all 11 sectors)
   - Top gainers/losers
   - Earnings intelligence calendar
   - Valuation metrics (P/E, forward P/E, dividend yield)
   - Market breadth analysis (advance/decline)
   - Technical analysis signals (MA, MACD, RSI, etc.)

4. **🤖 AI Signals** - Machine learning intelligence
   - Model confidence scores
   - Active trading signals (BUY/HOLD/SELL)
   - 24-hour forward predictions
   - Anomaly detection alerts
   - Model performance metrics (win rate, Sharpe ratio)
   - Correlation matrix analysis
   - Sentiment analysis (news + social)

5. **🌐 Geo Map** - Interactive geographic intelligence
   - Regional market performance breakdown
   - Country-by-country heatmap
   - Currency intelligence (FX pairs)
   - Commodity prices (energy, metals, agriculture)
   - Supply chain health indicators
   - Major trade flow analysis

### Design System

**Colors:**
- Surface: #0c0e14 (void) → #33343b (highest)
- Primary: #ffb867 (amber, live indicators)
- Status: #9dd3aa (positive), #ffb4ab (negative)
- Text: #e2e2eb (anti-retina-burn off-white)

**Typography:**
- Serif: Lora (headlines, narrative)
- Data: JetBrains Mono (aligned numbers)
- UI: IBM Plex Mono (labels, utility)

**Components:**
- Buttons: Mechanical switch (0ms transition, invert on hover)
- Cards: No dividers, vertical spacing (16px/24px/32px)
- Inputs: Underline-only terminal style
- Panels: Hydraulic transitions (cubic-bezier 0.4,0,0.2,1)

---

## Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Running

```bash
# Start the dashboard
streamlit run app.py

# Or from command line
streamlit run app.py --logger.level=debug --client.showErrorDetails=true
```

The dashboard will be available at: `http://localhost:8501`

---

## File Structure

```
geo-market-ml/
├── app.py                                 # Main dashboard entry
├── components.py                          # Reusable UI components
├── design_tokens.py                       # Design system (colors, fonts, spacing)
├── styles.css                             # Global CSS + design system
├── requirements.txt                       # Dependencies
│
├── tactical_intelligence/
│   ├── __init__.py
│   ├── view.py                            # Market surveillance view
│   └── DESIGN.md                          # Design specification
│
├── earth_pulse_geomarket_intelligence/
│   ├── __init__.py
│   └── view.py                            # Geospatial intelligence view
│
├── market_geomarket_intelligence/
│   ├── __init__.py
│   └── view.py                            # Equity analysis view
│
├── ai_signals_geomarket_intelligence/
│   ├── __init__.py
│   └── view.py                            # ML predictions view
│
├── geo_map_geomarket_intelligence/
│   ├── __init__.py
│   └── view.py                            # Geographic markets view
│
├── api/                                   # API module
├── data/                                  # Data processing
├── gti/                                   # GTI module
├── ingestion/                             # Data ingestion pipeline
├── nlp/                                   # NLP processing
└── prediction/                            # ML prediction models
```

---

## Design Principles

### "Monastic Brutalism"

1. **Stark Technical Precision:** Every pixel has purpose
2. **Archival Elegance:** Serif typography suggests curated intelligence
3. **Intentional Asymmetry:** Reject the 12-column grid for breathing room
4. **No Soft Corners:** 0px radius = precision and authority
5. **Tonal Layering:** Surfaces defined by color, not borders
6. **Dead Space Signifies Clarity:** Don't fill every corner

### "The No-Line Rule"

Traditional 1px borders are forbidden. Instead:
- Use surface color transitions (#111319 → #191b22)
- Apply 15% opacity ghost borders with `outline_variant`
- Embrace tonal shifts to define sections

### "Amber Pulse"

All live indicators use amber (#ffb867) with:
- 2-second linear pulse animation
- 20px outer glow spread at 10% opacity
- Instantly grabs attention during critical events

---

## Component Usage

### Data Card

```python
from components import data_card, DataPoint, StatusLevel

data_card(
    "MARKET OVERVIEW",
    [
        DataPoint("8,247.32", "S&P 500", StatusLevel.POSITIVE),
        DataPoint("+2.3%", "Daily Change", StatusLevel.POSITIVE),
        DataPoint("2.1B", "Volume (24H)", StatusLevel.NEUTRAL),
    ]
)
```

### Metric Box

```python
from components import metric_box, StatusLevel

metric_box(
    "VIX INDEX",
    "12.8",
    status=StatusLevel.POSITIVE,
    trend="↓ -8.2%"
)
```

### Live Indicator

```python
from components import live_indicator

live_indicator("LIVE FEED")
```

---

## Customization

### Change Colors

Edit `design_tokens.py`:
```python
COLORS = {
    "primary": "#ffb867",  # Change amber to another hex
    # ... other colors
}
```

### Change Typography

Edit `styles.css`:
```css
--font-headline: "Lora", serif;
--font-data: "JetBrains Mono", monospace;
```

### Modify Spacing

Edit `design_tokens.py`:
```python
SPACING = {
    "lg": "16px",  # Change from 16px to custom value
}
```

---

## Performance Tips

1. **Lazy Load Views:** Each view is imported on-demand via sidebar selection
2. **Memoization:** Use `@st.cache_data` for expensive computations
3. **Session State:** Use `st.session_state` for persistent state across reruns
4. **Conditional Rendering:** Only render visible sections

---

## Security Notes

- All data is local to the Streamlit session (no persistence by default)
- For production, integrate authentication via Streamlit secrets
- HTTPS required for production deployments
- Consider rate limiting on data feeds

---

## Future Enhancements

- WebSocket integration for real-time data feeds
- D3.js/Plotly maps for geographic visualization
- Export dashboards to PDF/PNG
- Dark/Light theme toggle
- Custom alert thresholds
- Portfolio tracking integration
- Historical backtesting view

---

## Support

For issues, enhancements, or questions: Refer to DESIGN.md for design system specification.

---

**Built with:** Streamlit + Python + Pure CSS  
**Design Inspiration:** Military intelligence, financial terminals, brutalist architecture  
**Last Updated:** April 2026
