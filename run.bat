@echo off
setlocal
cd /d "%~dp0"
set "ROOT=%~dp0"

echo ============================================================
echo   Geo-Market ML — Startup
echo ============================================================

:: ── 1. Create venv if missing ─────────────────────────────────────────────
if not exist "venv\Scripts\python.exe" (
    echo [1/5] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Could not create venv. Is Python installed and on PATH?
        pause & exit /b 1
    )
) else (
    echo [1/5] Virtual environment found.
)

call venv\Scripts\activate

:: ── 2. Install dependencies from requirements.txt ─────────────────────────
echo [2/5] Installing dependencies ^(this may take a minute on first run^)...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo [ERROR] pip install failed. Check your internet connection.
    pause & exit /b 1
)
echo       Done.

:: ── 3. Create directories and initialise databases ────────────────────────
echo [3/5] Initialising databases...
if not exist "data" mkdir data
if not exist "prediction\models" mkdir prediction\models
python -c "from ingestion.db import init_all; init_all()"
if errorlevel 1 (
    echo [ERROR] Database init failed.
    pause & exit /b 1
)

:: ── 4. Launch scheduler in its own window ─────────────────────────────────
echo [4/5] Starting scheduler...
start "Scheduler — Geo-Market ML" cmd /k "cd /d "%ROOT%" && call venv\Scripts\activate && python scheduler.py"

:: ── 5. If no models exist, run backfill + train in a background window ─────
echo [5/5] Checking for trained models...
if not exist "prediction\models\lgbm_volatility.pkl" (
    echo       No models found — launching backfill + training in a separate window.
    echo       This takes 5-15 min. Dashboard will show "No data yet" until it finishes.
    start "Backfill + Train — Geo-Market ML" cmd /k "cd /d "%ROOT%" && call venv\Scripts\activate && echo Backfilling GDELT... && python -m ingestion.gdelt_fetcher --backfill --days 30 && echo Backfilling market data... && python -m ingestion.market_fetcher --backfill --days 30 && echo Fetching RSS... && python -m ingestion.rss_fetcher && echo Computing GTI... && python -m gti.aggregator && echo Training models... && python prediction\train.py && echo DONE. Models trained. Dashboard will update on next refresh."
) else (
    echo       Models found — skipping backfill.
)

:: ── Give scheduler 4 seconds to start, then open dashboard ────────────────
echo.
echo Waiting for Streamlit to start...
timeout /t 4 /nobreak >nul

echo Opening dashboard at http://localhost:8501
start "" "http://localhost:8501"
streamlit run dashboard/app.py

endlocal
pause
