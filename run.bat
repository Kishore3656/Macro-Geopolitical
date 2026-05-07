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

echo [3/3] Starting FastAPI backend (port 8000)...
start "FastAPI Backend" python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

REM Wait a bit for backend to start
timeout /t 2 /nobreak

echo.
echo Starting React frontend (port 3000)...
cd frontend
npm install --silent
start "React Frontend" npm run dev

echo.
echo ========================================
echo  Services started!
echo ========================================
echo  Backend: http://localhost:8000
echo  Frontend: http://localhost:3000
echo.
echo Check your browser - should auto-open at http://localhost:3000
echo.
pause
