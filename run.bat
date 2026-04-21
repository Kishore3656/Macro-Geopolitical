@echo off
REM Sovereign Intelligence Framework - Windows Startup Script

echo.
echo ================================
echo SOVEREIGN INTELLIGENCE FRAMEWORK
echo Tactical Archive Dashboard
echo ================================
echo.

REM Resolve script directory so this works from any working directory
set "SCRIPT_DIR=%~dp0"

REM Activate venv if present
if exist "%SCRIPT_DIR%venv\Scripts\activate.bat" (
    call "%SCRIPT_DIR%venv\Scripts\activate.bat"
) else (
    echo WARNING: venv not found at %SCRIPT_DIR%venv - using system Python
    echo Run: python -m venv venv  ^&^&  venv\Scripts\activate  ^&^&  pip install -r requirements.txt
)

REM Check Python is reachable
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Install Python 3.10+ and re-run.
    pause
    exit /b 1
)

echo.
echo Installing/updating dependencies...
pip install -r "%SCRIPT_DIR%requirements.txt" -q

echo.
echo Starting dashboard...
echo (* Launching on http://localhost:8501
echo.

streamlit run "%SCRIPT_DIR%app.py"
pause
