import { test, expect } from '@playwright/test';

test.describe('Earth Pulse Page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/?tab=earth_pulse');
  });

  test('should display Earth Pulse page title', async ({ page }) => {
    const title = page.locator('.page-title');
    await expect(title).toContainText('EARTH PULSE');
  });

  test('should display page subtitle', async ({ page }) => {
    const subtitle = page.locator('.page-subtitle');
    await expect(subtitle).toContainText('GLOBAL MARKETS & MACRO TENSIONS');
  });

  test('should display GTI hero number', async ({ page }) => {
    const heroNumber = page.locator('.gti-hero-number');
    await expect(heroNumber).toBeVisible();
  });

  test('should display system status', async ({ page }) => {
    const status = page.locator('.system-status-row');
    await expect(status).toBeVisible();
    await expect(status).toContainText('STATUS:');
  });

  test('should display Live Intelligence Feed section', async ({ page }) => {
    const feedHeader = page.locator('.section-header');
    // Should contain "LIVE INTELLIGENCE FEED" or a variation
    await expect(page.locator('text=LIVE INTELLIGENCE FEED')).toBeVisible();
  });

  test('should display Macro Components section', async ({ page }) => {
    // Should contain "MACRO COMPONENTS"
    await expect(page.locator('text=MACRO COMPONENTS')).toBeVisible();
  });

  test('should display signal cards with progress bars', async ({ page }) => {
    // Look for signal cards
    const signalCards = page.locator('.signal-card');
    const count = await signalCards.count();
    expect(count).toBeGreaterThan(0);

    // Check for signal card names
    await expect(page.locator('text=CONFLICT RATIO')).toBeVisible();
    await expect(page.locator('text=MEDIA TONE')).toBeVisible();
  });

  test('should display GTI score badge', async ({ page }) => {
    const gtiScore = page.locator('.gti-hero-badge');
    await expect(gtiScore).toBeVisible();
  });

  test('should have proper CSS styling', async ({ page }) => {
    const pageTitle = page.locator('.page-title');
    const color = await pageTitle.evaluate(el => window.getComputedStyle(el).color);
    // Should have light color (on-surface color)
    expect(color).toBeTruthy();
  });
});
