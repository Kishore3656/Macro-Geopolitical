# 🚀 GeoMarket Intelligence - Quick Start Guide

## One-Click Setup

Simply **double-click `run.bat`** in the project root directory!

That's it! The script will:
1. ✅ Create Python virtual environment (if needed)
2. ✅ Install Python dependencies
3. ✅ Start FastAPI backend on port 8000
4. ✅ Install Node.js dependencies (first run only)
5. ✅ Start React frontend on port 3000

---

## What Happens Next

Two terminal windows will open automatically:

### Terminal 1: FastAPI Backend
```
GeoMarket API (port 8000)
```
- Shows: `Uvicorn running on 0.0.0.0:8000`
- API Docs: http://localhost:8000/docs

### Terminal 2: React Frontend
```
GeoMarket UI (port 3000)
```
- Shows: `Ready in [X] seconds`
- Open: http://localhost:3000

---

## Access the Dashboard

Open your browser and go to:
### 🌍 http://localhost:3000

You should see:
- **Earth Pulse** (main dashboard) with global tensions
- Navigation to Market, AI Signals, and Geo Intelligence

---

## 4 Dashboards Available

| Dashboard | URL | Purpose |
|-----------|-----|---------|
| **Earth Pulse** | `/earth-pulse` | Geopolitical tensions, GTI score, headlines |
| **Market Intelligence** | `/market` | S&P 500, SPY price, sector performance |
| **AI Signals** | `/ai-signals` | ML trading signals, confidence metrics |
| **Geo Intelligence** | `/geo-map` | Bilateral relations, geopolitical events |

---

## Troubleshooting

### ❌ Infinite Loading on First Visit
**Solution:** Wait 2-3 minutes for backend data to initialize

### ❌ Port Already in Use
**Solution:** Change port in `run.bat`:
```batch
# Line 43: Change 8000 to another port (e.g., 9000)
# Line 58: Change 3000 to another port (e.g., 3001)
```

### ❌ npm install fails
**Solution:** Delete `frontend/node_modules` and run again

### ❌ Python venv issues
**Solution:** Delete `venv` folder and run again

---

## Frontend Features

✨ **Modern UI Design**
- Glass-morphism cards
- Gradient backgrounds
- Smooth hover animations
- Responsive grid layouts

📊 **Real-Time Data**
- WebSocket connections for live updates
- Zustand state management
- Auto-refresh on data changes

🎨 **Color-Coded Status**
- Green: Good/Bullish/Stable
- Amber: Warning/Elevated
- Red: Danger/Bearish/Critical

---

## Backend API Endpoints

All accessible from http://localhost:8000:

```
GET  /api/gti              - Current GTI score
GET  /api/gti/history      - Historical GTI data
GET  /api/signals          - Current trading signal
GET  /api/signals/history  - Signal history
GET  /api/market/spy       - S&P 500 data
GET  /api/market/sectors   - Sector performance
GET  /api/headlines        - News headlines
GET  /api/conflicts        - Active conflicts
GET  /api/bilateral        - Bilateral relations
GET  /api/events           - Geopolitical events

WS   /ws/gti              - GTI real-time WebSocket
WS   /ws/market           - Market real-time WebSocket
WS   /ws/signals          - Signals real-time WebSocket
```

---

## Environment Variables

Optional - edit `run.bat` to customize:

```batch
REM Backend
set API_HOST=0.0.0.0
set API_PORT=8000

REM Frontend
set NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## File Structure

```
d:\trading bot\geo-market-ml\
├── api/                    # FastAPI backend
│   ├── main.py            # Entry point
│   ├── routes/            # API endpoints
│   └── models/            # Data models
├── frontend/              # React/Next.js 15
│   ├── src/
│   │   ├── app/          # Page routes
│   │   ├── components/   # React components
│   │   ├── hooks/        # Custom hooks
│   │   ├── store/        # Zustand store
│   │   └── lib/          # Utilities
│   ├── package.json
│   └── next.config.ts
├── requirements.txt       # Python dependencies
├── run.bat               # Start script
├── TESTING_REPORT.md     # Detailed test report
└── QUICK_START.md        # This file
```

---

## Performance Tips

1. **First Load:** May take 30-60 seconds while data loads
2. **Charts:** Use `Ctrl+Shift+K` to clear browser cache if slow
3. **Mobile:** Responsive design works on phones/tablets
4. **Memory:** Close other browser tabs for better performance

---

## Still Need Help?

Check `TESTING_REPORT.md` for:
- Detailed error fixes
- UI design system
- Verification checklist
- Known limitations

---

**Ready? Double-click `run.bat` and enjoy! 🎉**
