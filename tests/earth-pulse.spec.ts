import { test, expect } from '@playwright/test';

test.describe('Earth Pulse Page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/?tab=earth_pulse');
  });

  test('should display GTI hero number element', async ({ page }) => {
    const heroNumber = page.locator('.gti-hero-number');
    await expect(heroNumber).toBeVisible();
  });

  test('should display GTI assessment text', async ({ page }) => {
    const badge = page.locator('.gti-hero-badge');
    await expect(badge).toContainText('CURRENT_ASSESSMENT');
  });

  test('should display GTI hero number', async ({ page }) => {
    const heroNumber = page.locator('.gti-hero-number');
    await expect(heroNumber).toBeVisible();
  });

  test('should display signal cards', async ({ page }) => {
    const signals = page.locator('.signal-card');
    const count = await signals.count();
    expect(count).toBeGreaterThan(0);
  });

  test('should display Geopolitical Tension Index label', async ({ page }) => {
    await expect(page.locator('text=Geopolitical Tension Index')).toBeVisible();
  });

  test('should display risk legend', async ({ page }) => {
    const legend = page.locator('.risk-legend');
    await expect(legend).toBeVisible();
    await expect(page.locator('text=CRITICAL')).toBeVisible();
    await expect(page.locator('text=ELEVATED')).toBeVisible();
    await expect(page.locator('text=STABLE')).toBeVisible();
  });

  test('should display progress bars on signal cards', async ({ page }) => {
    const progressBars = page.locator('.signal-bar-fill');
    const count = await progressBars.count();
    expect(count).toBeGreaterThan(0);
  });

  test('should have visible signal card values', async ({ page }) => {
    const signalValues = page.locator('.signal-card-value');
    const count = await signalValues.count();
    expect(count).toBeGreaterThan(0);

    // Verify at least one card is visible
    const firstValue = signalValues.first();
    await expect(firstValue).toBeVisible();
  });

  test('should display coordinates', async ({ page }) => {
    const coordDisplay = page.locator('.coord-display');
    await expect(coordDisplay).toBeVisible();
  });
});
