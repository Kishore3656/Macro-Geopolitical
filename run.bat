@echo off
REM Trading Bot - Unified Dashboard Startup Script

echo.
echo ========================================
echo  Trading Bot - Unified Dashboard
echo ========================================
echo.

REM Get the project directory
set PROJECT_DIR=%~dp0
cd /d "%PROJECT_DIR%"

echo [1/3] Setting up Python environment...
if not exist venv (
    python -m venv venv
)
call venv\Scripts\activate.bat

echo [2/3] Installing dependencies...
pip install -q -r requirements.txt

echo [3/3] Starting services (Scheduler, API, Frontend)...

REM Optional: Set RAPIDAPI_KEY to enable RapidAPI geopolitical events (free tier: 100 req/month)
REM Signup at: https://rapidapi.com/nmk3/api/geopolitical-events-database1
REM set RAPIDAPI_KEY=your_key_here

REM Start scheduler (background data fetching)
start "Scheduler" cmd /k "cd backend && python scheduler.py"
timeout /t 2 /nobreak

REM Start FastAPI backend (port 8000)
start "FastAPI Backend" cmd /k "cd backend && python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000"

REM Wait for backend to fully initialize
timeout /t 5 /nobreak

echo.
echo Installing frontend dependencies (this may take a minute)...
cd frontend
call npm install
if errorlevel 1 (
    echo [ERROR] npm install failed. Check the frontend window for details.
    cd ..
    pause
    exit /b 1
)
cd ..

echo.
echo Starting React frontend (port 3000)...
start "React Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo  Services started!
echo ========================================
echo  Backend: http://localhost:8000
echo  Frontend: http://localhost:3000
echo.
echo Waiting for services to initialize (30 seconds)...
timeout /t 10 /nobreak

echo.
echo ========================================
echo  IMPORTANT: WAIT FOR DATA TO BACKFILL
echo ========================================
echo.
echo 4 terminal windows should now be open:
echo   1. Scheduler - Fetching real market + geopolitical data
echo   2. FastAPI Backend - http://localhost:8000
echo   3. React Frontend - http://localhost:3000
echo   4. This console
echo.
echo WAIT 2-3 MINUTES for initial data backfill:
echo   - First time: Fetches 30 days of data (GDELT, SPY, VIX, GLD)
echo   - Then: Updates every 15 minutes
echo.
echo CHECK PROGRESS:
echo   1. Watch the Scheduler terminal for messages
echo   2. Visit: http://localhost:8000/api/diagnostic
echo   3. Should show: "data_ready": true (after 2-3 min)
echo.
echo TROUBLESHOOTING:
echo   - If Scheduler shows errors, check internet connection
echo   - If API shows "awaiting_data", just wait a few more minutes
echo   - Close all terminals and re-run this script if something breaks
echo.
echo To stop: Close all 4 terminal windows.
echo.
pause
