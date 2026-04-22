@echo off
REM Sovereign Intelligence Framework - Windows Startup Script

echo.
echo ================================
echo SOVEREIGN INTELLIGENCE FRAMEWORK
echo Tactical Archive Dashboard
echo ================================
echo.

REM Always run from the directory this .bat file lives in
cd /d "%~dp0"

set "VENV_PY=%~dp0venv\Scripts\python.exe"
set "VENV_PIP=%~dp0venv\Scripts\pip.exe"
set "VENV_STREAMLIT=%~dp0venv\Scripts\streamlit.exe"

REM Verify venv exists
if not exist "%VENV_PY%" (
    echo ERROR: venv not found. Run these commands first:
    echo   python -m venv venv
    echo   venv\Scripts\pip install -r requirements.txt
    pause
    exit /b 1
)

REM Show Python version
"%VENV_PY%" --version

echo.
echo Installing/updating dependencies...
"%VENV_PIP%" install -r requirements.txt -q

echo.
echo Starting dashboard...
echo (* Launching on http://localhost:8501
echo.

"%VENV_STREAMLIT%" run app.py
pause
