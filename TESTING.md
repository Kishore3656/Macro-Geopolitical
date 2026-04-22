# Playwright E2E Testing Guide

This project includes comprehensive Playwright-based end-to-end tests for the GeoMarket Intelligence dashboard.

## Test Structure

### Test Files

- `tests/test_navigation.py` - Navigation and layout tests
- `tests/test_earth_pulse.py` - Earth Pulse page specific tests
- `tests/test_geo_map.py` - Geo Map page tests (TypeScript/JS)
- `tests/test_ai_signals.py` - AI Signals page tests (TypeScript/JS)
- `tests/test_market.py` - Market Intelligence page tests (TypeScript/JS)

### Configuration Files

- `pytest.ini` - Pytest configuration for Python tests
- `playwright.config.ts` - Playwright configuration for TypeScript tests
- `tests/conftest.py` - Pytest fixtures and setup

## Running Tests

### Option 1: PowerShell Script (Recommended for Windows)

```powershell
.\run_tests.ps1
```

This script will:
1. Install/update Playwright and dependencies
2. Install browser runtimes
3. Start the Streamlit app
4. Run all tests
5. Push changes to GitHub (if tests pass)

### Option 2: Batch Script

```batch
run_tests.bat
```

### Option 3: Manual Execution

#### Python Tests (pytest)

```bash
# Install dependencies
pip install playwright pytest pytest-playwright

# Install browsers
python -m playwright install

# Run tests
pytest tests/test_*.py -v
```

#### TypeScript Tests (Node.js)

```bash
# Install dependencies
npm install

# Run tests
npx playwright test

# Run tests in UI mode
npx playwright test --ui

# Run tests in headed mode
npx playwright test --headed
```

## Test Coverage

### Navigation Tests
- ✓ Home page loads correctly
- ✓ Navbar displays all tabs
- ✓ Sidebar displays correctly
- ✓ Status bar is visible
- ✓ Tab switching doesn't open new windows
- ✓ Each tab can be navigated to

### Earth Pulse Tests
- ✓ Title and subtitle display
- ✓ GTI hero number visible
- ✓ System status visible
- ✓ Live Intelligence Feed section
- ✓ Macro Components section
- ✓ Signal cards and progress bars
- ✓ GTI badge visible

### Geo Map Tests
- ✓ Page title and subtitle
- ✓ Filter chips display
- ✓ Map placeholder area
- ✓ Target Lock section
- ✓ Threat Legend
- ✓ SAT UPLINK RELIABILITY box
- ✓ Legend dots with colors

### AI Signals Tests
- ✓ Page title and subtitle
- ✓ Model output panels
- ✓ Expected Volatility section
- ✓ Directional Bias section
- ✓ Feature Weights with progress bars
- ✓ Inference History section
- ✓ Confidence metrics

### Market Intelligence Tests
- ✓ Page title and subtitle
- ✓ Market hero cards (SPY, DXY)
- ✓ LIVE badge
- ✓ Chart panel and interval buttons
- ✓ Chart area placeholder
- ✓ Price values and changes

## Debugging

### View Test Report

```bash
pytest tests/ -v
npx playwright show-report
```

### Run Single Test

```bash
pytest tests/test_navigation.py::TestNavigation::test_home_page_loads -v
```

### Run Tests in Debug Mode

```bash
npx playwright test --debug
```

### Take Screenshots on Failure

Screenshots are automatically captured on test failures in the `test-results/` directory.

## CI/CD Integration

To integrate with GitHub Actions:

1. Create `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt
      - run: python -m pytest tests/
```

## Troubleshooting

### Tests timeout waiting for Streamlit

- Ensure Streamlit is running on `http://localhost:8501`
- Check if port 8501 is available
- Increase timeout in `pytest.ini` if needed

### Browser not found

```bash
python -m playwright install chromium
npx playwright install
```

### Import errors

```bash
pip install playwright pytest pytest-playwright
```

## Best Practices

1. **Keep tests focused** - Each test should verify one thing
2. **Use clear names** - Test names should describe what they test
3. **Avoid hard-coded waits** - Use `wait_for_load_state()` or locators
4. **Isolate state** - Each test should be independent
5. **Handle dynamic content** - Streamlit may require additional waits

## Contributing

When adding new features to the dashboard:

1. Add corresponding test cases
2. Run the full test suite before committing
3. Update this documentation if test structure changes
4. Ensure all tests pass before pushing
