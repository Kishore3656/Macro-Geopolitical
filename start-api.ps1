# Start the FastAPI server
Write-Host "Starting FastAPI Server..." -ForegroundColor Green
Write-Host "API will be available at http://localhost:8000" -ForegroundColor Cyan
Write-Host "Docs available at http://localhost:8000/docs`n" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop`n" -ForegroundColor Yellow

cd backend
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
