# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: e2e_data_validation.spec.ts >> GeoMarket E2E - Data Validation & Error Scenarios >> Market Intelligence dashboard validates actual SPY metrics
- Location: tests\e2e_data_validation.spec.ts:33:7

# Error details

```
Error: page.goto: Could not connect to server
Call log:
  - navigating to "http://localhost:3000/market", waiting until "networkidle"

```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test';
  2  | 
  3  | test.describe('GeoMarket E2E - Data Validation & Error Scenarios', () => {
  4  |   
  5  |   test.beforeEach(async ({ page }) => {
  6  |     // Set a global timeout per test for stable CI/CD execution
  7  |     test.setTimeout(30000);
  8  |   });
  9  | 
  10 |   test('Earth Pulse dashboard validates and renders actual GTI data', async ({ page }) => {
  11 |     // Intercept API call to provide predictable GTI data
  12 |     // This matches the frontend expectation where 'score' is used instead of 'gti_score'
  13 |     await page.route('**/api/gti', async (route) => {
  14 |       await route.fulfill({
  15 |         status: 200,
  16 |         contentType: 'application/json',
  17 |         body: JSON.stringify({
  18 |           score: 85.5,
  19 |           risk_level: 'Critical',
  20 |           conflict_ratio: 0.8,
  21 |           tone_index: -5.2
  22 |         })
  23 |       });
  24 |     });
  25 | 
  26 |     await page.goto('/earth-pulse', { waitUntil: 'networkidle' });
  27 | 
  28 |     // Validating the actual mocked data appears on the dashboard
  29 |     await expect(page.getByText('85.5')).toBeVisible({ timeout: 10000 });
  30 |     await expect(page.getByText('Critical')).toBeVisible();
  31 |   });
  32 | 
  33 |   test('Market Intelligence dashboard validates actual SPY metrics', async ({ page }) => {
  34 |     // Intercept API call for Market data
  35 |     await page.route('**/api/market/spy', async (route) => {
  36 |       await route.fulfill({
  37 |         status: 200,
  38 |         contentType: 'application/json',
  39 |         body: JSON.stringify({
  40 |           current_price: 515.25,
  41 |           daily_change_pct: 1.5,
  42 |           bars: []
  43 |         })
  44 |       });
  45 |     });
  46 | 
> 47 |     await page.goto('/market', { waitUntil: 'networkidle' });
     |                ^ Error: page.goto: Could not connect to server
  48 | 
  49 |     // Validating the rendered SPY pricing data
  50 |     await expect(page.getByText('515.25')).toBeVisible({ timeout: 10000 });
  51 |     await expect(page.getByText('1.5')).toBeVisible();
  52 |   });
  53 | 
  54 |   test('Application gracefully handles backend 500 error scenarios', async ({ page }) => {
  55 |     // Simulate a backend crash/error for the signals endpoint
  56 |     await page.route('**/api/signals', async (route) => {
  57 |       await route.fulfill({
  58 |         status: 500,
  59 |         contentType: 'application/json',
  60 |         body: JSON.stringify({ detail: 'Internal Server Error' })
  61 |       });
  62 |     });
  63 | 
  64 |     await page.goto('/ai-signals', { waitUntil: 'networkidle' });
  65 | 
  66 |     // The UI should remain intact without a white-screen-of-death (WSOD)
  67 |     await expect(page.getByRole('heading', { name: /AI Trading Signals/i })).toBeVisible({ timeout: 10000 });
  68 |     
  69 |     // The sidebar navigation should still be completely functional allowing user recovery
  70 |     await expect(page.getByRole('link', { name: /Earth Pulse/i })).toBeVisible();
  71 |   });
  72 | });
```