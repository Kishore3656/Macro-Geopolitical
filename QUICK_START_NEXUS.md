# NEXUS Command - Quick Start Guide

**Last Updated**: May 5, 2026

---

## ⚡ 30-Second Setup

### Option 1: One Command (Simplest)
```bash
cd "d:\trading bot\geo-market-ml"
run.bat
```
This opens two windows automatically - backend and frontend.

### Option 2: Manual Setup (More Control)

**Terminal 1 - Backend:**
```bash
cd "d:\trading bot\geo-market-ml"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd "d:\trading bot\geo-market-ml\frontend"
npm install
npm run dev
```

**Then open:** http://localhost:3000

---

## 🎮 Navigation

Once loaded, you'll see the NEXUS interface with 5 sections:

| Page | URL | What You See |
|------|-----|--------------|
| **NEXUS Command** | http://localhost:3000 | Main command center + geopolitical map |
| **Earth Pulse** | http://localhost:3000/earth-pulse | Global risk & event analysis |
| **Geo Map** | http://localhost:3000/geo-map | World tensions heatmap |
| **Market** | http://localhost:3000/market | Financial assets & sectors |
| **AI Signals** | http://localhost:3000/ai-signals | ML predictions & accuracy |

Click the sidebar to navigate between pages.

---

## ✅ Quick Verification

After startup, check these:

```bash
# Backend check (in new terminal or browser)
curl http://localhost:8000/api/signals

# Frontend check
Open http://localhost:3000 in browser
```

**You should see:**
- Geopolitical map with colored regions
- Live news ticker on the right
- Market data in the panels
- No console errors (press F12 to check)

---

## 🎨 What's New in NEXUS

Compared to the old dashboard, you now have:

✅ **Dark terminal aesthetic** - Black background with green text  
✅ **Exact NEXUS design** - Matches your provided screenshot  
✅ **Unified theme** - All 5 pages use the same style  
✅ **Real data only** - No dummy content anywhere  
✅ **Live events** - Geopolitical events update from your API  
✅ **Market integration** - SPY, sectors, assets all live  
✅ **Signal tracking** - ML predictions with accuracy stats  

---

## 🔴 Common Issues & Fixes

### "Cannot find module" errors
```bash
cd frontend
npm install
npm run dev
```

### Backend not responding
```bash
# Check if it's running on port 8000
netstat -ano | findstr :8000

# Kill if stuck:
taskkill /PID <PID> /F

# Restart:
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### Data not loading (blank panels)
1. Open DevTools (F12)
2. Check Network tab for failed requests
3. Verify backend endpoints:
   - `GET http://localhost:8000/api/signals`
   - `GET http://localhost:8000/api/market/spy`
   - `GET http://localhost:8000/api/gti`

### Styling looks broken
```bash
cd frontend
npm run dev  # Restart - rebuilds Tailwind CSS
```

---

## 📸 Capturing Screenshots

Once everything is running, you can take screenshots of each page:

1. **Home/NEXUS Command**: Shows the full command center
2. **Earth Pulse**: Shows geopolitical risk analysis
3. **Geo Map**: Shows world tensions visualization
4. **Market**: Shows financial asset tracking
5. **AI Signals**: Shows ML prediction accuracy

Press `F12` → **View** → **Toggle Device Toolbar** to see mobile layout.

---

## 🚀 Testing Real Data

The dashboard pulls data from these API endpoints:

```
/api/signals              - Current ML prediction (UP/DOWN)
/api/signals/history      - Last 100 predictions
/api/market/spy           - S&P 500 price & volume
/api/market/sectors       - 11 sector performance
/api/gti                  - Geopolitical score
/api/bilateral            - Country pair tensions
/api/events               - Recent geopolitical events
```

If the API endpoints don't return data, the panels will show empty or "loading" states.

---

## 💾 Project Files Structure

```
d:\trading bot\geo-market-ml\
├── api/                          # FastAPI backend
│   ├── main.py                   # Entry point
│   └── routes/                   # API endpoints
│
├── frontend/                      # Next.js 15 frontend
│   ├── src/
│   │   ├── app/                  # 5 page routes
│   │   ├── components/
│   │   │   ├── dashboards/       # 5 NEXUS dashboards (NEW)
│   │   │   ├── themes/           # Design system (NEW)
│   │   │   └── layout/           # Sidebar, headers
│   │   ├── hooks/                # useSignals, useMarket, useGTI
│   │   ├── lib/api.ts            # API client
│   │   └── types/index.ts        # Type definitions
│   ├── package.json
│   ├── tsconfig.json
│   └── next.config.ts
│
├── venv/                         # Python virtual env
├── requirements.txt              # Python dependencies
├── run.bat                       # One-click startup
├── NEXUS_IMPLEMENTATION.md       # Full technical docs
└── QUICK_START_NEXUS.md          # This file
```

---

## 🎯 Next Actions

### To deploy to production:
1. Push code to GitHub
2. Connect Vercel repo
3. Set environment variables
4. Deploy with `vercel deploy`

### To customize colors:
Search for color classes in dashboard files and replace:
- `text-green-400` → your color
- `border-cyan-400/30` → your color
- `bg-red-500/20` → your color

### To add real-time updates:
Replace `useEffect` hooks with WebSocket connections to reduce API calls.

---

## 📞 Help & Support

**Questions about the dashboard?**  
→ See NEXUS_IMPLEMENTATION.md (full technical docs)

**Troubleshooting data loading?**  
→ Check browser Network tab (F12) for failed API calls

**Want to change colors/styling?**  
→ Edit the component className properties directly

**Need to understand the code?**  
→ Look at the comments in the component files

---

## ✨ You're All Set!

Your NEXUS Command dashboard is ready to use with **real, live data** from your backend APIs. All 5 pages are styled consistently and fully functional.

**Run `npm run dev` and start trading.** 🚀

---

*NEXUS Command Interface | Built May 5, 2026 | React + Next.js 15*
