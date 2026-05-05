import { test, expect } from '@playwright/test';

test.describe('Earth Pulse Page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/earth-pulse');
  });

  test('should display Earth Pulse heading', async ({ page }) => {
    await expect(page.getByRole('heading', { name: /Earth Pulse/i })).toBeVisible();
  });

  test('should display core GTI metrics', async ({ page }) => {
    await expect(page.getByText(/GTI Score/i)).toBeVisible();
    await expect(page.getByText(/Sentiment/i)).toBeVisible();
    await expect(page.getByText(/Volatility/i)).toBeVisible();
    await expect(page.getByText(/Active Events/i)).toBeVisible();
  });

  test('should display the Top Headlines section', async ({ page }) => {
    await expect(page.getByText(/Top Headlines/i)).toBeVisible();
  });

  test('should display the tension index chart section', async ({ page }) => {
    await expect(page.getByText(/Tension Index Trend \(48H\)/i)).toBeVisible();
  });
});
