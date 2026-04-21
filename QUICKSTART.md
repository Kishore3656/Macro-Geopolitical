# Quick Start Guide

## 30 Second Setup

### Windows
```bash
cd "d:\trading bot\geo-market-ml"
run.bat
```

### macOS / Linux
```bash
cd ~/trading\ bot/geo-market-ml
bash run.sh
```

---

## Manual Setup

### 1. Install Python 3.10+
```bash
python --version
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Dashboard
```bash
streamlit run app.py
```

The dashboard will open at **http://localhost:8501**

---

## What You Get

✅ **5 Integrated Intelligence Modules:**
- 🎯 Tactical Archive (real-time market surveillance)
- 🌍 Earth Pulse (geospatial intelligence)
- 📈 Market Intelligence (equity analysis)
- 🤖 AI Signals (ML predictions)
- 🌐 Geo Map (geographic markets)

✅ **Design System:**
- Monastic Brutalism aesthetic (dark + authoritative)
- Midnight tonal color palette
- Precision typography (serif + monospace)
- Zero-border component design
- Amber pulse live indicators

✅ **Production-Ready Components:**
- Data cards with intelligent spacing
- Metric boxes with trend indicators
- Live status indicators
- Alert notifications
- Activity timelines
- Status badges
- Responsive grid layouts

---

## Navigation

**Sidebar Menu:**
- Select any intelligence module
- View market status metrics
- Configure settings
- Check system status

**Each Module Features:**
- Command center header
- Primary intelligence panel
- Deep-dive analysis sections
- Activity feeds
- Related intelligence
- Footer with data sources

---

## Customization

### Change Theme Colors
Edit `design_tokens.py`:
```python
COLORS = {
    "primary": "#ffb867",      # Amber accent
    "surface_lowest": "#0c0e14", # Deep void
    "surface_container": "#1e1f26", # Main surface
}
```

### Add New Components
Edit `components.py` and follow existing patterns:
```python
def my_component(label: str) -> None:
    """Description"""
    st.markdown(f"<span class='label-md'>{label}</span>", unsafe_allow_html=True)
```

### Create New Views
1. Create folder: `my_view_geomarket_intelligence/`
2. Add `__init__.py` and `view.py`
3. Implement `render()` function
4. Import in `app.py` and add to sidebar

---

## Performance

- **Fast Load:** CSS-only styling (no heavy JS)
- **Responsive:** Mobile-friendly layout
- **Efficient:** Component-level rendering
- **Scalable:** Easy to add new modules

---

## Architecture

```
app.py (Main entry)
├── render_sidebar()
├── render_header()
└── Route to selected view
    ├── tactical_view.render()
    ├── earth_pulse_view.render()
    ├── market_view.render()
    ├── ai_signals_view.render()
    └── geo_map_view.render()
```

Each view:
- Imports shared `components.py`
- Uses `design_tokens.py` via CSS
- Renders via `styles.css`
- Standalone, but coordinated

---

## Troubleshooting

### Port Already in Use
```bash
streamlit run app.py --server.port 8502
```

### Module Not Found
Ensure you're in the correct directory:
```bash
cd "d:\trading bot\geo-market-ml"
```

### CSS Not Loading
Clear Streamlit cache:
```bash
streamlit cache clear
streamlit run app.py
```

### Missing Dependencies
```bash
pip install --upgrade -r requirements.txt
```

---

## Production Deployment

### Streamlit Cloud
```bash
git push  # Push to GitHub
# Connect repo on share.streamlit.io
```

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "app.py"]
```

### Heroku
```bash
git push heroku main
# Configure environment variables in Heroku dashboard
```

---

## Next Steps

1. **Integrate Real Data:** Replace mock data with live feeds
2. **Add WebSockets:** Real-time updates via websocket-client
3. **Implement Auth:** Streamlit secrets + database
4. **Build API Layer:** FastAPI backend for data
5. **Add Export:** PDF/CSV export functionality
6. **Mobile App:** React Native wrapper

---

## Support & Docs

- **Design System:** See `DESIGN.md`
- **Component Library:** See `components.py` docstrings
- **Configuration:** See `.streamlit/config.toml`
- **Dependencies:** See `requirements.txt`

---

**Ready? Run your dashboard now:**

```bash
streamlit run app.py
```

🚀 Launch into the Tactical Archive!
