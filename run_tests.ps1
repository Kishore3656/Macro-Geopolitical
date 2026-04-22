# GeoMarket Intelligence - Playwright Test Runner and Git Push

Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "Running Playwright Tests" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""

# Set paths
$venvPython = ".\venv\Scripts\python.exe"
$venvPip = ".\venv\Scripts\pip.exe"

# Check if venv exists
if (-not (Test-Path $venvPython)) {
    Write-Host "ERROR: venv not found." -ForegroundColor Red
    Write-Host "Run these commands first:" -ForegroundColor Yellow
    Write-Host "  python -m venv venv" -ForegroundColor Yellow
    Write-Host "  .\venv\Scripts\pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

# Install/update playwright
Write-Host "Installing/updating Playwright..." -ForegroundColor Cyan
& $venvPip install playwright pytest pytest-playwright -q

# Install playwright browsers
Write-Host "Installing Playwright browsers..." -ForegroundColor Cyan
& $venvPython -m playwright install chromium firefox webkit

# Start Streamlit app in background
Write-Host ""
Write-Host "Starting Streamlit app..." -ForegroundColor Cyan
$appProcess = Start-Process -FilePath $venvPython -ArgumentList "-m streamlit run app.py --logger.level=error" -PassThru -WindowStyle Hidden

# Wait for app to start
Write-Host "Waiting for app to start (10 seconds)..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Run tests
Write-Host ""
Write-Host "Running tests..." -ForegroundColor Cyan
& $venvPython -m pytest tests/ -v --tb=short

$testResult = $LASTEXITCODE

# Kill the Streamlit app
Write-Host ""
Write-Host "Stopping Streamlit app..." -ForegroundColor Yellow
Stop-Process -Id $appProcess.Id -ErrorAction SilentlyContinue

# Check test results
Write-Host ""
if ($testResult -eq 0) {
    Write-Host "✓ All tests passed!" -ForegroundColor Green

    # Commit and push to GitHub
    Write-Host ""
    Write-Host "================================" -ForegroundColor Green
    Write-Host "Pushing to GitHub" -ForegroundColor Green
    Write-Host "================================" -ForegroundColor Green
    Write-Host ""

    # Add test files
    Write-Host "Adding test files to git..." -ForegroundColor Cyan
    git add tests/
    git add playwright.config.ts
    git add pytest.ini
    git add package.json
    git add run_tests.bat
    git add run_tests.ps1
    git add .gitignore -f

    # Create .gitignore if it doesn't exist
    if (-not (Test-Path ".gitignore")) {
        @"
__pycache__/
*.py[cod]
*`$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
venv/
env/
ENV/
.venv
.vscode/
*.swp
*.swo
*~
.DS_Store
node_modules/
package-lock.json
.playwright/
test-results/
playwright-report/
"@ | Out-File -Encoding UTF8 ".gitignore"
        git add .gitignore
    }

    # Commit
    Write-Host "Creating commit..." -ForegroundColor Cyan
    $commitMessage = @"
Add Playwright E2E tests and test infrastructure

- Add comprehensive Playwright test suite for all dashboard pages
- Test navigation, UI elements, and page layouts
- Add pytest configuration and test runner scripts
- Include both TypeScript and Python-based test configurations
- All tests passing
"@

    git commit -m $commitMessage

    # Check if remote exists
    $remoteUrl = git config --get remote.origin.url
    if ($remoteUrl) {
        Write-Host ""
        Write-Host "Pushing to remote: $remoteUrl" -ForegroundColor Cyan
        git push -u origin main

        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Successfully pushed to GitHub!" -ForegroundColor Green
        } else {
            Write-Host "✗ Failed to push to GitHub. Check your remote and credentials." -ForegroundColor Red
        }
    } else {
        Write-Host "No remote configured. Add a remote with:" -ForegroundColor Yellow
        Write-Host "  git remote add origin <your-github-url>" -ForegroundColor Yellow
        Write-Host "  git push -u origin main" -ForegroundColor Yellow
    }
} else {
    Write-Host "✗ Tests failed with exit code: $testResult" -ForegroundColor Red
    Write-Host ""
    Write-Host "Fix the issues and run tests again." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "Done" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""
