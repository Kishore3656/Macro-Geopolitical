import { test, expect } from '@playwright/test';

test.describe('Market Intelligence Page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/?tab=market');
  });

  test('should display market hero cards', async ({ page }) => {
    const cards = page.locator('.market-hero-card');
    const count = await cards.count();
    expect(count).toBeGreaterThan(0);
  });

  test('should display PRIMARY ASSET TRAJECTORY text', async ({ page }) => {
    await expect(page.locator('text=PRIMARY ASSET TRAJECTORY')).toBeVisible();
  });

  test('should display SPY ticker card', async ({ page }) => {
    await expect(page.locator('text=SPY')).toBeVisible();
    await expect(page.locator('text=S&P 500 ETF')).toBeVisible();
    await expect(page.locator('text=HOURLY OHLCV SYNC')).toBeVisible();
  });

  test('should display DXY ticker card', async ({ page }) => {
    await expect(page.locator('text=DXY')).toBeVisible();
    await expect(page.locator('text=U.S. DOLLAR INDEX')).toBeVisible();
  });

  test('should display LIVE badge on metric card', async ({ page }) => {
    const liveBadge = page.locator('.live-badge');
    await expect(liveBadge).toBeVisible();
    await expect(liveBadge).toContainText('LIVE');
  });

  test('should display chart panel header', async ({ page }) => {
    const chartPanel = page.locator('.chart-panel');
    await expect(chartPanel).toBeVisible();

    await expect(page.locator('text=PRIMARY ASSET TRAJECTORY')).toBeVisible();
  });

  test('should display interval buttons', async ({ page }) => {
    const intervalBtns = page.locator('.interval-btn');
    const count = await intervalBtns.count();
    expect(count).toBeGreaterThan(0);

    // Check interval options
    await expect(page.locator('.interval-btns')).toContainText('1H');
    await expect(page.locator('.interval-btns')).toContainText('4H');
    await expect(page.locator('.interval-btns')).toContainText('1D');
  });

  test('should have active interval button (4H)', async ({ page }) => {
    const activeBtn = page.locator('.interval-btn-active');
    await expect(activeBtn).toBeVisible();
  });

  test('should display chart area placeholder', async ({ page }) => {
    const chartArea = page.locator('.chart-area-empty');
    await expect(chartArea).toBeVisible();
    await expect(chartArea).toContainText('CHARTING ENGINE');
  });

  test('should display market hero values', async ({ page }) => {
    const heroValues = page.locator('.market-hero-value');
    const count = await heroValues.count();
    expect(count).toBeGreaterThan(0);
  });

  test('should display price changes', async ({ page }) => {
    const changes = page.locator('.market-hero-change');
    const count = await changes.count();
    expect(count).toBeGreaterThan(0);
  });
});
