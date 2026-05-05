import { test, expect } from '@playwright/test';

test.describe('Geo Map Page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/geo-map');
  });

  test('should display Geopolitical Intelligence heading', async ({ page }) => {
    await expect(page.getByRole('heading', { name: /Geopolitical Intelligence/i })).toBeVisible();
  });

  test('should display main geo metrics', async ({ page }) => {
    await expect(page.getByText(/Total Relations/i)).toBeVisible();
    await expect(page.getByText(/Critical Zones/i)).toBeVisible();
    await expect(page.getByText(/Recent Events/i)).toBeVisible();
  });

  test('should display bilateral relations section', async ({ page }) => {
    await expect(page.getByText(/Bilateral Relations \(Top Tensions\)/i)).toBeVisible();
  });

  test('should display recent geopolitical events section', async ({ page }) => {
    await expect(page.getByText(/Recent Geopolitical Events/i)).toBeVisible();
  });
});
