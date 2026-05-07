# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: ai-signals.spec.ts >> AI Signals Page >> should display recent signals section
- Location: tests\ai-signals.spec.ts:19:7

# Error details

```
Error: page.goto: Could not connect to server
Call log:
  - navigating to "http://localhost:3000/ai-signals", waiting until "load"

```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test';
  2  | 
  3  | test.describe('AI Signals Page', () => {
  4  |   test.beforeEach(async ({ page }) => {
> 5  |     await page.goto('/ai-signals');
     |                ^ Error: page.goto: Could not connect to server
  6  |   });
  7  | 
  8  |   test('should display AI Trading Signals heading', async ({ page }) => {
  9  |     await expect(page.getByRole('heading', { name: /AI Trading Signals/i })).toBeVisible();
  10 |   });
  11 | 
  12 |   test('should display current signal metrics when available', async ({ page }) => {
  13 |     await expect(page.getByText(/Total Predictions/i)).toBeVisible();
  14 |     await expect(page.getByText(/Win Rate/i)).toBeVisible();
  15 |     await expect(page.getByText(/High Volatility/i)).toBeVisible();
  16 |     await expect(page.getByText(/Model Confidence Over Time/i)).toBeVisible();
  17 |   });
  18 | 
  19 |   test('should display recent signals section', async ({ page }) => {
  20 |     await expect(page.getByText(/Recent Signals/i)).toBeVisible();
  21 |   });
  22 | });
  23 | 
```