import { test, expect } from '@playwright/test';

test.describe('GeoMarket Navigation', () => {
  test('should load the home page', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/GeoMarket Intelligence/);
  });

  test('should display the navbar with all tabs', async ({ page }) => {
    await page.goto('/');

    // Check navbar exists
    const navbar = page.locator('.topnav');
    await expect(navbar).toBeVisible();

    // Check all tab names are visible
    await expect(page.locator('.topnav-tabs')).toContainText('EARTH PULSE');
    await expect(page.locator('.topnav-tabs')).toContainText('GEO MAP');
    await expect(page.locator('.topnav-tabs')).toContainText('AI SIGNALS');
    await expect(page.locator('.topnav-tabs')).toContainText('MARKET');
  });

  test('should display the sidebar', async ({ page }) => {
    await page.goto('/');

    const sidebar = page.locator('.left-sidebar');
    await expect(sidebar).toBeVisible();

    // Check sidebar items
    await expect(page.locator('.sidebar-nav')).toContainText('INTELLIGENCE');
    await expect(page.locator('.sidebar-nav')).toContainText('Archive');
    await expect(page.locator('.sidebar-nav')).toContainText('Surveillance');
    await expect(page.locator('.sidebar-nav')).toContainText('Tactical');
  });

  test('should display the footer status bar', async ({ page }) => {
    await page.goto('/');

    const statusBar = page.locator('.status-bar');
    await expect(statusBar).toBeVisible();

    // Check status bar content
    await expect(statusBar).toContainText('SYSTEM_STABLE');
    await expect(statusBar).toContainText('ENCRYPTION_AES256');
  });

  test('should switch tabs using navigation buttons', async ({ page, context }) => {
    await page.goto('/');

    // Get initial page count
    const initialPages = context.pages().length;

    // Click on "Geo Map" tab using the button mechanism
    await page.getByRole('button', { name: /Geo Map/i }).click();

    // Verify no new tabs opened
    expect(context.pages().length).toBe(initialPages);

    // Verify the page updated by checking for map-specific element
    await expect(page.locator('.map-placeholder')).toBeVisible();
  });

  test('should navigate through all tabs with proper elements', async ({ page }) => {
    const tabs = [
      { name: 'Earth Pulse', selector: '.gti-hero-number' },
      { name: 'Geo Map', selector: '.map-placeholder' },
      { name: 'AI Signals', selector: '.model-output-panel' },
      { name: 'Market', selector: '.market-hero-card' },
    ];

    for (const tab of tabs) {
      await page.goto('/');
      await page.getByRole('button', { name: new RegExp(tab.name, 'i') }).click();
      await expect(page.locator(tab.selector)).toBeVisible();
    }
  });
});
