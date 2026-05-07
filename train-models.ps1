# Train ML Models with Improved Accuracy
# =========================================

Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     GeoMarket ML Model Training & Setup Pipeline      ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

Write-Host "This script will:" -ForegroundColor Green
Write-Host "  1. Initialize all databases" -ForegroundColor Green
Write-Host "  2. Fetch 60 days of historical data (GDELT, markets, RSS)" -ForegroundColor Green
Write-Host "  3. Build feature matrix with technical indicators (RSI, MACD, BB, ATR)" -ForegroundColor Green
Write-Host "  4. Train improved LightGBM models (enhanced hyperparameters)" -ForegroundColor Green
Write-Host "  5. Evaluate model performance and save models" -ForegroundColor Yellow
Write-Host "`nEstimated time: 5-10 minutes`n" -ForegroundColor Yellow

# Activate Python venv
Write-Host "Activating Python virtual environment..." -ForegroundColor Cyan
if (Test-Path "venv\Scripts\Activate.ps1") {
    & "venv\Scripts\Activate.ps1"
    Write-Host "✓ Virtual environment activated`n" -ForegroundColor Green
} else {
    Write-Host "⚠ Virtual environment not found. Creating one..." -ForegroundColor Yellow
    python -m venv venv
    & "venv\Scripts\Activate.ps1"
    Write-Host "Installing dependencies..." -ForegroundColor Cyan
    pip install -r requirements.txt
    Write-Host "✓ Dependencies installed`n" -ForegroundColor Green
}

# Run training
Write-Host "Starting training pipeline..." -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop`n" -ForegroundColor Yellow

python setup_and_train.py --days 60

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✓ Training complete!" -ForegroundColor Green
    Write-Host "`nNext steps:" -ForegroundColor Cyan
    Write-Host "  1. Start scheduler:    .\start-scheduler.ps1" -ForegroundColor Yellow
    Write-Host "  2. Start API server:   .\start-api.ps1" -ForegroundColor Yellow
    Write-Host "  3. Start frontend:     .\start-frontend.ps1" -ForegroundColor Yellow
    Write-Host "  4. Open browser:       http://localhost:3000`n" -ForegroundColor Yellow
} else {
    Write-Host "`n❌ Training failed. Check output above for errors." -ForegroundColor Red
}
