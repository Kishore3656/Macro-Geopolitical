# Start the scheduler
Write-Host "Starting Trading Bot Scheduler..." -ForegroundColor Green
Write-Host "This keeps running and schedules all background jobs" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop`n" -ForegroundColor Yellow

cd backend
python scheduler.py
