import { test, expect } from '@playwright/test';

test.describe('AI Signals Page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/ai-signals');
  });

  test('should display AI Trading Signals heading', async ({ page }) => {
    await expect(page.getByRole('heading', { name: /AI Trading Signals/i })).toBeVisible();
  });

  test('should display current signal metrics when available', async ({ page }) => {
    await expect(page.getByText(/Total Predictions/i)).toBeVisible();
    await expect(page.getByText(/Win Rate/i)).toBeVisible();
    await expect(page.getByText(/High Volatility/i)).toBeVisible();
    await expect(page.getByText(/Model Confidence Over Time/i)).toBeVisible();
  });

  test('should display recent signals section', async ({ page }) => {
    await expect(page.getByText(/Recent Signals/i)).toBeVisible();
  });
});
