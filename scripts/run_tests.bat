@echo off
REM GeoMarket Intelligence - Playwright Test Runner

echo.
echo ================================
echo Running Playwright Tests
echo ================================
echo.

REM Set virtual environment
set "VENV_PY=%~dp0venv\Scripts\python.exe"

REM Check if venv exists
if not exist "%VENV_PY%" (
    echo ERROR: venv not found. Run:
    echo   python -m venv venv
    echo   venv\Scripts\pip install -r requirements.txt
    pause
    exit /b 1
)

REM Install playwright browsers if not present
echo Installing Playwright browsers...
"%VENV_PY%" -m playwright install chromium firefox webkit

echo.
echo Starting Streamlit app in background...
start "GeoMarket App" "%VENV_PY%" -m streamlit run app.py --logger.level=error

REM Wait for app to start
timeout /t 5 /nobreak

echo.
echo Running tests...
"%VENV_PY%" -m pytest tests/ -v --tb=short

echo.
echo ================================
echo Tests Complete
echo ================================
pause
