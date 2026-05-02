import { test, expect } from '@playwright/test';

test.describe('AI Signals Page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/?tab=ai_signals');
  });

  test('should display model output section', async ({ page }) => {
    const modelOutput = page.locator('.model-output-panel');
    await expect(modelOutput).toBeVisible();
  });

  test('should display MODEL OUTPUT text label', async ({ page }) => {
    await expect(page.locator('text=MODEL OUTPUT')).toBeVisible();
  });

  test('should display model output panels', async ({ page }) => {
    const panels = page.locator('.model-output-panel');
    const count = await panels.count();
    expect(count).toBeGreaterThan(0);
  });

  test('should display volatility prediction panel', async ({ page }) => {
    await expect(page.locator('text=VOLATILITY_PREDICTION')).toBeVisible();
  });

  test('should display direction prediction panel', async ({ page }) => {
    await expect(page.locator('text=DIRECTION_PREDICTION')).toBeVisible();
  });

  test('should display feature rows with GTI features', async ({ page }) => {
    const featureRows = page.locator('.feature-row');
    const count = await featureRows.count();
    expect(count).toBeGreaterThan(0);

    // Check for GTI input features
    await expect(page.locator('text=GTI_INPUT_FEATURES')).toBeVisible();
  });

  test('should display confidence text', async ({ page }) => {
    await expect(page.locator('text=Confidence:')).toBeVisible();
  });

  test('should display feature values', async ({ page }) => {
    const featureValues = page.locator('.feature-value');
    const count = await featureValues.count();
    expect(count).toBeGreaterThan(0);
  });

  test('should display model output panels', async ({ page }) => {
    const panels = page.locator('.model-output-panel');
    const count = await panels.count();
    expect(count).toBeGreaterThan(0);
  });
});
