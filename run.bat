@echo off
setlocal enabledelayedexpansion
REM GeoMarket Intelligence Framework - Automatic Startup Script
REM Starts both backend and frontend without any prompts

echo.
echo ================================
echo GEOMARKET INTELLIGENCE FRAMEWORK
echo Real-time GTI ^& Trading Signals
echo ================================
echo.
echo Starting both services automatically...
echo.

cd /d "%~dp0"

set "VENV_PY=%~dp0venv\Scripts\python.exe"
set "VENV_PIP=%~dp0venv\Scripts\pip.exe"
set "ROOT_DIR=%~dp0"

REM Verify venv exists
if not exist "%VENV_PY%" (
    echo ERROR: venv not found. Creating virtual environment...
    python -m venv venv
    echo Installing dependencies...
    "%VENV_PIP%" install -r requirements.txt -q
) else (
    echo Python version:
    "%VENV_PY%" --version
    echo.
    echo Updating dependencies...
    "%VENV_PIP%" install -r requirements.txt -q
)

echo.
echo ================================
echo STARTING SERVICES
echo ================================
echo.

REM Start FastAPI backend in new window
echo Starting FastAPI Backend (port 8000)...
start "GeoMarket API" /D "%ROOT_DIR%" cmd /k ""%VENV_PY%" -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000"

REM Wait a moment for backend to initialize
timeout /t 3 /nobreak >nul

REM Install frontend dependencies if not present
if not exist "%ROOT_DIR%\frontend\node_modules" (
    echo Installing frontend dependencies...
    cd /d "%ROOT_DIR%\frontend"
    call npm install -q
    cd /d "%ROOT_DIR%"
)

REM Start React frontend in new window
echo Starting React Frontend (port 3000)...
start "GeoMarket UI" /D "%ROOT_DIR%\frontend" cmd /k "npm run dev"

echo.
echo ================================
echo SERVICES STARTING
echo ================================
echo.
echo FastAPI Backend: http://localhost:8000
echo FastAPI Docs:   http://localhost:8000/docs
echo Frontend UI:    http://localhost:3000
echo.
echo Both windows will open in separate terminals.
echo Close any window to stop that service.
echo.

REM Keep this window open for reference
timeout /t 5 /nobreak >nul
echo.
echo Services are now running. Press any key to close this window.
echo (The services will continue running in their own windows)
pause
exit /b 0
