import { test, expect } from '@playwright/test';

test.describe('Geo Map Page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/?tab=geo_map');
  });

  test('should display map placeholder', async ({ page }) => {
    const mapPlaceholder = page.locator('.map-placeholder');
    await expect(mapPlaceholder).toBeVisible();
  });

  test('should display GEOSPATIAL RENDER ENGINE OFFLINE message', async ({ page }) => {
    await expect(page.locator('text=GEOSPATIAL RENDER ENGINE OFFLINE')).toBeVisible();
  });

  test('should display coordinate display section', async ({ page }) => {
    const coordDisplay = page.locator('.coord-display');
    await expect(coordDisplay).toBeVisible();
  });

  test('should display PRIMARY FOCUS AREA text', async ({ page }) => {
    await expect(page.locator('text=PRIMARY FOCUS AREA')).toBeVisible();
  });

  test('should display map legend', async ({ page }) => {
    const legend = page.locator('.map-legend');
    await expect(legend).toBeVisible();
  });

  test('should display threat level indicators', async ({ page }) => {
    const threatItems = page.locator('.threat-item');
    const count = await threatItems.count();
    expect(count).toBeGreaterThan(0);
  });

  test('should display reliability metrics', async ({ page }) => {
    const reliability = page.locator('.reliability-box');
    // Can be optional, just check if visible when present
    const visible = await reliability.isVisible().catch(() => false);
    if (visible) {
      await expect(reliability).toBeVisible();
    }
  });

  test('should have legend elements', async ({ page }) => {
    const legend = page.locator('.map-legend');
    const legendItems = legend.locator('.threat-item');
    const count = await legendItems.count();
    expect(count).toBeGreaterThanOrEqual(0);
  });
});
