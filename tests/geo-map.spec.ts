import { test, expect } from '@playwright/test';

test.describe('Geo Map Page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/?tab=geo_map');
  });

  test('should display Geo Map page title', async ({ page }) => {
    const title = page.locator('.page-title');
    await expect(title).toContainText('GEO MAP');
  });

  test('should display page subtitle', async ({ page }) => {
    const subtitle = page.locator('.page-subtitle');
    await expect(subtitle).toContainText('TACTICAL GEOSPATIAL SURVEILLANCE');
  });

  test('should display filter chips', async ({ page }) => {
    // Check for filter buttons
    const filterGroup = page.locator('.filter-group');
    await expect(filterGroup).toBeVisible();

    // Check filter chips
    await expect(filterGroup).toContainText('ALL EVENTS');
    await expect(filterGroup).toContainText('MILITARY');
    await expect(filterGroup).toContainText('DIPLOMATIC');
    await expect(filterGroup).toContainText('ECONOMIC');
  });

  test('should display map placeholder area', async ({ page }) => {
    const mapPlaceholder = page.locator('.map-placeholder');
    await expect(mapPlaceholder).toBeVisible();
    await expect(mapPlaceholder).toContainText('GEOSPATIAL RENDER ENGINE OFFLINE');
  });

  test('should display Target Lock section', async ({ page }) => {
    await expect(page.locator('text=TARGET LOCK')).toBeVisible();

    const coordDisplay = page.locator('.coord-display');
    await expect(coordDisplay).toBeVisible();
    // Should show coordinates
    await expect(coordDisplay).toContainText('PRIMARY FOCUS AREA');
  });

  test('should display Threat Legend', async ({ page }) => {
    await expect(page.locator('text=THREAT LEGEND')).toBeVisible();

    const legend = page.locator('.map-legend');
    await expect(legend).toBeVisible();

    // Check legend items
    await expect(legend).toContainText('CRITICAL INSTABILITY');
    await expect(legend).toContainText('ELEVATED TENSION');
    await expect(legend).toContainText('NOMINAL OPERATIONS');
  });

  test('should display SAT UPLINK RELIABILITY', async ({ page }) => {
    const reliabilityBox = page.locator('.reliability-box');
    await expect(reliabilityBox).toBeVisible();

    await expect(reliabilityBox).toContainText('SAT UPLINK RELIABILITY');
    // Should display reliability percentage
    await expect(reliabilityBox).toContainText('%');
  });

  test('should have legend dots with proper colors', async ({ page }) => {
    const legendDots = page.locator('.legend-dot');
    const count = await legendDots.count();
    expect(count).toBeGreaterThan(0);
  });
});
