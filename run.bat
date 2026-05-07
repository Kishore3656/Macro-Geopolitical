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
echo Services should now be running.
echo - Frontend will open at http://localhost:3000
echo - Backend API at http://localhost:8000
echo.
echo To stop: Close the backend and frontend terminal windows.
echo.
pause
