import { test, expect } from '@playwright/test';

test.describe('AI Signals Page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/?tab=ai_signals');
  });

  test('should display AI Signals page title', async ({ page }) => {
    const title = page.locator('.page-title');
    await expect(title).toContainText('AI SIGNALS');
  });

  test('should display page subtitle', async ({ page }) => {
    const subtitle = page.locator('.page-subtitle');
    await expect(subtitle).toContainText('PREDICTIVE MODELING & INFERENCE');
  });

  test('should display model output panels', async ({ page }) => {
    const panels = page.locator('.model-output-panel');
    const count = await panels.count();
    expect(count).toBeGreaterThan(0);
  });

  test('should display Expected Volatility section', async ({ page }) => {
    await expect(page.locator('text=EXPECTED VOLATILITY')).toBeVisible();
    await expect(page.locator('text=20H ROLLING FORECAST')).toBeVisible();
  });

  test('should display Directional Bias section', async ({ page }) => {
    await expect(page.locator('text=DIRECTIONAL BIAS')).toBeVisible();
    await expect(page.locator('text=NEXT-HOUR PREDICTION')).toBeVisible();
  });

  test('should display Feature Weights section', async ({ page }) => {
    await expect(page.locator('text=FEATURE WEIGHTS')).toBeVisible();

    // Check feature rows
    await expect(page.locator('text=GTI SCORE')).toBeVisible();
    await expect(page.locator('text=RETURNS 1H')).toBeVisible();
    await expect(page.locator('text=VADER AVG')).toBeVisible();
    await expect(page.locator('text=VOL 20H')).toBeVisible();
  });

  test('should display feature bars', async ({ page }) => {
    const featureBars = page.locator('.feature-bar-fill');
    const count = await featureBars.count();
    expect(count).toBeGreaterThan(0);
  });

  test('should display Inference History section', async ({ page }) => {
    await expect(page.locator('text=INFERENCE HISTORY')).toBeVisible();

    const historyEmpty = page.locator('.history-empty');
    await expect(historyEmpty).toBeVisible();
    await expect(historyEmpty).toContainText('NO HISTORICAL DATA LOADED');
  });

  test('should display confidence metrics', async ({ page }) => {
    const confidenceElements = page.locator('.model-confidence');
    const count = await confidenceElements.count();
    expect(count).toBeGreaterThan(0);

    // Should show confidence percentages
    await expect(page.locator('text=CONFIDENCE:')).toBeVisible();
  });
});
