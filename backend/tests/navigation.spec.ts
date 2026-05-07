import { test, expect } from '@playwright/test';

test.describe('GeoMarket Navigation', () => {
  test('should redirect home to Earth Pulse and load the home page', async ({ page }) => {
    await page.goto('/', { waitUntil: 'networkidle' });
    await expect(page).toHaveURL(/\/earth-pulse$/);
    await expect(page).toHaveTitle(/GeoMarket Intelligence/);
    await expect(page.getByRole('heading', { name: /Earth Pulse/i })).toBeVisible({ timeout: 10000 });
  });

  test('should display the sidebar navigation links', async ({ page }) => {
    await page.goto('/earth-pulse', { waitUntil: 'networkidle' });
    await expect(page.getByRole('link', { name: /Earth Pulse/i })).toBeVisible({ timeout: 10000 });
    await expect(page.getByRole('link', { name: /Geo Map/i })).toBeVisible({ timeout: 10000 });
    await expect(page.getByRole('link', { name: /Market/i })).toBeVisible({ timeout: 10000 });
    await expect(page.getByRole('link', { name: /AI Signals/i })).toBeVisible({ timeout: 10000 });
  });

  test('should navigate to each dashboard using sidebar links', async ({ page }) => {
    const pages = [
      { link: /Earth Pulse/i, heading: /Earth Pulse/i, url: /\/earth-pulse$/ },
      { link: /Geo Map/i, heading: /Geopolitical Intelligence/i, url: /\/geo-map$/ },
      { link: /Market/i, heading: /Market Intelligence/i, url: /\/market$/ },
      { link: /AI Signals/i, heading: /AI Trading Signals/i, url: /\/ai-signals$/ },
    ];

    await page.goto('/earth-pulse', { waitUntil: 'networkidle' });

    for (const pageInfo of pages) {
      await page.getByRole('link', { name: pageInfo.link }).click();
      await expect(page).toHaveURL(pageInfo.url);
      await expect(page.getByRole('heading', { name: pageInfo.heading })).toBeVisible({ timeout: 10000 });
    }
  });
});
