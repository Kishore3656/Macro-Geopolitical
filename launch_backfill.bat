@echo off
cd /d "%~dp0"
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"
call venv\Scripts\activate.bat
echo Backfilling GDELT...
venv\Scripts\python.exe -m ingestion.gdelt_fetcher --backfill --days 30
echo Backfilling market data...
venv\Scripts\python.exe -m ingestion.market_fetcher --backfill --days 30
echo Fetching RSS...
venv\Scripts\python.exe -m ingestion.rss_fetcher
echo Computing GTI...
venv\Scripts\python.exe -m gti.aggregator
echo Training models...
venv\Scripts\python.exe prediction\train.py
echo.
echo DONE. Models trained. Dashboard will update on next refresh.
pause
