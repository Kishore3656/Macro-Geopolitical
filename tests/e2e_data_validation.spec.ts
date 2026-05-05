import { test, expect } from '@playwright/test';

test.describe('GeoMarket E2E - Data Validation & Error Scenarios', () => {
  
  test.beforeEach(async ({ page }) => {
    // Set a global timeout per test for stable CI/CD execution
    test.setTimeout(30000);
  });

  test('Earth Pulse dashboard validates and renders actual GTI data', async ({ page }) => {
    // Intercept API call to provide predictable GTI data
    // This matches the frontend expectation where 'score' is used instead of 'gti_score'
    await page.route('**/api/gti', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          score: 85.5,
          risk_level: 'Critical',
          conflict_ratio: 0.8,
          tone_index: -5.2
        })
      });
    });

    await page.goto('/earth-pulse', { waitUntil: 'networkidle' });

    // Validating the actual mocked data appears on the dashboard
    await expect(page.getByText('85.5')).toBeVisible({ timeout: 10000 });
    await expect(page.getByText('Critical')).toBeVisible();
  });

  test('Market Intelligence dashboard validates actual SPY metrics', async ({ page }) => {
    // Intercept API call for Market data
    await page.route('**/api/market/spy', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          current_price: 515.25,
          daily_change_pct: 1.5,
          bars: []
        })
      });
    });

    await page.goto('/market', { waitUntil: 'networkidle' });

    // Validating the rendered SPY pricing data
    await expect(page.getByText('515.25')).toBeVisible({ timeout: 10000 });
    await expect(page.getByText('1.5')).toBeVisible();
  });

  test('Application gracefully handles backend 500 error scenarios', async ({ page }) => {
    // Simulate a backend crash/error for the signals endpoint
    await page.route('**/api/signals', async (route) => {
      await route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({ detail: 'Internal Server Error' })
      });
    });

    await page.goto('/ai-signals', { waitUntil: 'networkidle' });

    // The UI should remain intact without a white-screen-of-death (WSOD)
    await expect(page.getByRole('heading', { name: /AI Trading Signals/i })).toBeVisible({ timeout: 10000 });
    
    // The sidebar navigation should still be completely functional allowing user recovery
    await expect(page.getByRole('link', { name: /Earth Pulse/i })).toBeVisible();
  });
});