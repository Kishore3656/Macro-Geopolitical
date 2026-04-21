@echo off
setlocal
cd /d "%~dp0"

set "ROOT=%~dp0"
set "VENV_PY=%ROOT%venv\Scripts\python.exe"
set "VENV_ACTIVATE=%ROOT%venv\Scripts\activate.bat"
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"

echo ============================================================
echo   GeoMarket Intelligence Dashboard
echo ============================================================

echo [1/5] Checking virtual environment...
if not exist "%VENV_PY%" (
    echo       Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Could not create venv. Is Python installed and on PATH?
        pause
        exit /b 1
    )
) else (
    echo       Virtual environment found.
)

call "%VENV_ACTIVATE%"

echo [2/5] Installing dependencies...
"%VENV_PY%" -m pip install -q -r requirements.txt
"%VENV_PY%" -m pip install -q setuptools
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
echo       Done.

echo [4/5] Starting scheduler terminal...
start "GeoMarket Scheduler" cmd /k ""%ROOT%launch_scheduler.bat""

echo [5/5] Starting Streamlit dashboard terminal...
start "GeoMarket Dashboard" cmd /k ""%ROOT%launch_dashboard.bat""

if not exist "prediction\models\lgbm_volatility.pkl" (
    echo.
    echo No trained models found. Starting backfill and training in a separate terminal.
    echo The dashboard may show "No data yet" until this finishes.
    start "GeoMarket Training" cmd /k ""%ROOT%launch_backfill.bat""
) else (
    echo.
    echo Trained models found.
)

echo.
echo ============================================================
echo   Dashboard: http://localhost:8501
echo   Scheduler and dashboard are running in separate terminals.
echo   Close those terminal windows to stop them.
echo ============================================================
echo.

pause
