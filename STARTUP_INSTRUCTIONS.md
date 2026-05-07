# How to Start the Trading Bot Dashboard

Since `run.bat` has environment limitations, follow these manual steps instead:

## 📋 Quick Start (2 terminals)

### Terminal 1: Start Backend

```powershell
cd "d:\trading bot\geo-market-ml"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

**You should see:**
```
Uvicorn running on http://0.0.0.0:8000
```

### Terminal 2: Start Frontend

```powershell
cd "d:\trading bot\geo-market-ml\frontend"
npm install
npm run dev
```

**You should see:**
```
ready - started server on 0.0.0.0:3000
```

### Open Dashboard

Once both are running, open your browser to:
```
http://localhost:3000
```

---

## ✅ Verification

Check that everything is working:

```powershell
# In any terminal, test the backend
curl http://localhost:8000/health
```

You should see a response with `"status": "ok"`.

---

## 🆘 Troubleshooting

**Backend won't start?**
- Make sure Python 3.8+ is installed
- Delete `venv` folder and try again
- Check if port 8000 is available

**Frontend won't start?**
- Make sure Node.js is installed
- Try `npm cache clean --force`
- Check if port 3000 is available

**Dashboard shows no data?**
- Backend must be running first
- Check browser console for errors (F12)
- Verify API endpoints are responding

---

That's it! The dashboard will now load with live trading data.
