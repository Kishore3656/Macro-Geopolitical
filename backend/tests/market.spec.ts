import { test, expect } from '@playwright/test';

test.describe('Market Intelligence Page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/market');
  });

  test('should display Market Intelligence heading', async ({ page }) => {
    await expect(page.getByRole('heading', { name: /Market Intelligence/i })).toBeVisible();
  });

  test('should display SPY metric cards', async ({ page }) => {
    await expect(page.locator('p', { hasText: 'SPY Price' })).toBeVisible();
    await expect(page.getByText(/Daily Change/i)).toBeVisible();
    await expect(page.locator('p', { hasText: 'Volume' })).toBeVisible();
    await expect(page.getByText(/52W High/i)).toBeVisible();
  });

  test('should display main chart and market state sections', async ({ page }) => {
    await expect(page.getByText(/SPY 5-Day Chart \(1H\)/i)).toBeVisible();
    await expect(page.getByText(/Market State/i)).toBeVisible();
  });

  test('should display sector performance section', async ({ page }) => {
    await expect(page.getByRole('heading', { name: /Sector Performance/i })).toBeVisible();
  });
});
