@echo off
REM Sovereign Intelligence Framework - Windows Startup Script

echo.
echo ================================
echo SOVEREIGN INTELLIGENCE FRAMEWORK
echo Tactical Archive Dashboard
echo ================================
echo.

REM Check Python
python --version

echo.
echo Installing dependencies...
pip install -r requirements.txt -q

echo.
echo Starting dashboard...
echo ^(^* Launching on http://localhost:8501
echo.

streamlit run app.py
pause
