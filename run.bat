@echo off
REM GeoMarket Intelligence Framework - Windows Startup Script

echo.
echo ================================
echo GEOMARKET INTELLIGENCE FRAMEWORK
echo Real-time GTI & Trading Signals
echo ================================
echo.

cd /d "%~dp0"

set "VENV_PY=%~dp0venv\Scripts\python.exe"
set "VENV_PIP=%~dp0venv\Scripts\pip.exe"

REM Verify venv exists
if not exist "%VENV_PY%" (
    echo ERROR: venv not found. Run these commands first:
    echo   python -m venv venv
    echo   venv\Scripts\pip install -r requirements.txt
    pause
    exit /b 1
)

echo Python version:
"%VENV_PY%" --version

echo.
echo Updating dependencies...
"%VENV_PIP%" install -r requirements.txt -q

echo.
echo ================================
echo STARTUP OPTIONS
echo ================================
echo 1. FastAPI Backend (port 8000)
echo 2. Streamlit UI (port 8501)
echo 3. React Frontend (port 3000)
echo 4. All three (requires multiple terminals)
echo.
set /p choice="Select option (1-4): "

if "%choice%"=="1" (
    echo Starting FastAPI backend...
    "%VENV_PY%" -m uvicorn api.main:app --reload
) else if "%choice%"=="2" (
    echo Starting Streamlit dashboard...
    "%VENV_PY%" -m streamlit run app.py
) else if "%choice%"=="3" (
    echo Starting React frontend...
    cd frontend
    npm run dev
    cd ..
) else if "%choice%"=="4" (
    echo Please start each in a separate terminal window:
    echo   Terminal 1: python -m uvicorn api.main:app --reload
    echo   Terminal 2: streamlit run app.py
    echo   Terminal 3: cd frontend ^&^& npm run dev
) else (
    echo Invalid option. Starting Streamlit by default...
    "%VENV_PY%" -m streamlit run app.py
)

pause
