# GeoMarket Trading Bot - Main Entry Point
# ==========================================

param(
    [string]$Command = "help",
    [int]$Days = 60
)

$Root = $PSScriptRoot

function Show-Help {
    Write-Host "`n========================================================" -ForegroundColor Cyan
    Write-Host "   GeoMarket Trading Bot - Command Center" -ForegroundColor Cyan
    Write-Host "========================================================`n" -ForegroundColor Cyan

    Write-Host "USAGE:" -ForegroundColor Yellow
    Write-Host "  .\RUN.ps1 <command> [options]`n" -ForegroundColor White

    Write-Host "COMMANDS:" -ForegroundColor Yellow
    Write-Host "  train        Train ML models (5-10 min)" -ForegroundColor Green
    Write-Host "  start        Start all 3 services" -ForegroundColor Green
    Write-Host "  scheduler    Start background scheduler only" -ForegroundColor Green
    Write-Host "  api          Start API server only (port 8000)" -ForegroundColor Green
    Write-Host "  frontend     Start frontend only (port 3000)" -ForegroundColor Green
    Write-Host "  help         Show this help message" -ForegroundColor Green

    Write-Host "`nOPTIONS:" -ForegroundColor Yellow
    Write-Host "  -Days <num>  Days of data for training (default: 60)" -ForegroundColor White

    Write-Host "`nEXAMPLES:" -ForegroundColor Yellow
    Write-Host "  .\RUN.ps1 train              # Train with 60 days of data" -ForegroundColor Cyan
    Write-Host "  .\RUN.ps1 train -Days 90     # Train with 90 days of data" -ForegroundColor Cyan
    Write-Host "  .\RUN.ps1 start              # Start all services" -ForegroundColor Cyan
    Write-Host "  .\RUN.ps1 api                # Start API only" -ForegroundColor Cyan

    Write-Host "`nFIRST TIME SETUP:" -ForegroundColor Yellow
    Write-Host "  1. .\RUN.ps1 train          # Train models (takes 5-10 min)" -ForegroundColor White
    Write-Host "  2. .\RUN.ps1 start          # Start 3 services" -ForegroundColor White
    Write-Host "  3. Open http://localhost:3000 in browser" -ForegroundColor White

    Write-Host "`nDIRECTORY STRUCTURE:" -ForegroundColor Yellow
    Write-Host "  backend/              Backend Python code and models" -ForegroundColor White
    Write-Host "    prediction/models/  <- Trained models stored here" -ForegroundColor Green
    Write-Host "  frontend/             React/Next.js dashboard" -ForegroundColor White
    Write-Host "  scripts/              Startup and utility scripts" -ForegroundColor White
    Write-Host "  docs/                 Documentation and guides" -ForegroundColor White
    Write-Host "  utils/                Training pipeline" -ForegroundColor White
    Write-Host "  data/                 SQLite databases (runtime)" -ForegroundColor White
    Write-Host "  RUN.ps1               This file (main entry point)" -ForegroundColor Cyan

    Write-Host "`nDEBUGGING:" -ForegroundColor Yellow
    Write-Host "  Check models exist:       ls backend/prediction/models/" -ForegroundColor White
    Write-Host "  View accuracy scores:     cat backend/prediction/models/model_registry.json" -ForegroundColor White
    Write-Host "  Test API:                 curl http://localhost:8000/health" -ForegroundColor White
    Write-Host "  View logs:                tail -f logs/trading_bot.log" -ForegroundColor White
    Write-Host "`n"
}

function Train-Models {
    Write-Host "`n========================================================" -ForegroundColor Green
    Write-Host "   Training ML Models (Phase 7)" -ForegroundColor Green
    Write-Host "========================================================`n" -ForegroundColor Green

    & "$Root\scripts\train-models.ps1"
}

function Start-All {
    Write-Host "`n========================================================" -ForegroundColor Cyan
    Write-Host "   Starting GeoMarket System (3 Services)" -ForegroundColor Cyan
    Write-Host "========================================================`n" -ForegroundColor Cyan

    Write-Host "Opening 3 terminal windows..." -ForegroundColor Yellow
    Write-Host "Press Ctrl+C in any terminal to stop that service`n" -ForegroundColor Yellow

    # Check if models exist before starting
    if (!(Test-Path "$Root\backend\prediction\models\lgbm_direction.pkl")) {
        Write-Host "[!] Models not found! Running training first..." -ForegroundColor Yellow
        & Train-Models
    }

    # Start services
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$Root'; & '.\scripts\start-scheduler.ps1'"
    Start-Sleep -Milliseconds 500
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$Root'; & '.\scripts\start-api.ps1'"
    Start-Sleep -Milliseconds 500
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$Root'; & '.\scripts\start-frontend.ps1'"

    Write-Host "[OK] Services started in 3 new windows" -ForegroundColor Green
    Write-Host "`nWaiting for services to start (30 seconds)..." -ForegroundColor Cyan
    Start-Sleep -Seconds 30

    Write-Host "`n[OK] Opening dashboard in browser..." -ForegroundColor Green
    Start-Process "http://localhost:3000"

    Write-Host "`nServices running:" -ForegroundColor Green
    Write-Host "  Scheduler: Running background jobs" -ForegroundColor White
    Write-Host "  API: http://localhost:8000" -ForegroundColor White
    Write-Host "  Dashboard: http://localhost:3000" -ForegroundColor White
}

# Main router
switch ($Command.ToLower()) {
    "train" {
        Train-Models
    }
    "start" {
        Start-All
    }
    "scheduler" {
        & "$Root\scripts\start-scheduler.ps1"
    }
    "api" {
        & "$Root\scripts\start-api.ps1"
    }
    "frontend" {
        & "$Root\scripts\start-frontend.ps1"
    }
    "help" {
        Show-Help
    }
    default {
        Write-Host "Unknown command: $Command`n" -ForegroundColor Red
        Show-Help
    }
}
