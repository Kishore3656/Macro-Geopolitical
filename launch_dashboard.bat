@echo off
cd /d "%~dp0"
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"
call venv\Scripts\activate.bat
venv\Scripts\python.exe -m streamlit run dashboard\app.py
pause
