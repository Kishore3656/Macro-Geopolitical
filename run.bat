@echo off
setlocal
cd /d "%~dp0"
set "ROOT=%~dp0"
set "VENV_PY=%ROOT%venv\Scripts\python.exe"

echo ============================================================
echo   Geo-Market ML - Startup
echo ============================================================

if not exist "%VENV_PY%" (
    echo [1/5] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Could not create venv. Is Python installed and on PATH?
        pause
        exit /b 1
    )
) else (
    echo [1/5] Virtual environment found.
)

call "%ROOT%venv\Scripts\activate.bat"

echo [2/5] Installing dependencies (this may take a minute on first run)...
"%VENV_PY%" -m pip install -q -r requirements.txt
if errorlevel 1 (
    echo [ERROR] pip install failed. Check your internet connection.
    pause
    exit /b 1
)
echo       Done.

echo [3/5] Initialising databases...
if not exist "data" mkdir data
if not exist "prediction\models" mkdir prediction\models
"%VENV_PY%" -c "from ingestion.db import init_all; init_all()"
if errorlevel 1 (
    echo [ERROR] Database init failed.
    pause
    exit /b 1
)

echo [4/5] Starting scheduler...
start "Scheduler - Geo-Market ML" cmd /k ""%ROOT%launch_scheduler.bat""

echo [5/5] Checking for trained models...
if not exist "prediction\models\lgbm_volatility.pkl" (
    echo       No models found - launching backfill + training in a separate window.
    echo       This takes 5-15 min. Dashboard will show "No data yet" until it finishes.
    start "Backfill + Train - Geo-Market ML" cmd /k ""%ROOT%launch_backfill.bat""
) else (
    echo       Models found - skipping backfill.
)

echo.
echo Waiting for Streamlit to start...
timeout /t 4 /nobreak >nul

echo Opening dashboard at http://localhost:8501
start "" "http://localhost:8501"
"%VENV_PY%" -m streamlit run dashboard/app.py

endlocal
pause
