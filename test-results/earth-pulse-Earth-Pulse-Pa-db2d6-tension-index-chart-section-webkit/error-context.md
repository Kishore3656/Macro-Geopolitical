# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: earth-pulse.spec.ts >> Earth Pulse Page >> should display the tension index chart section
- Location: tests\earth-pulse.spec.ts:23:7

# Error details

```
Error: page.goto: Could not connect to server
Call log:
  - navigating to "http://localhost:3000/earth-pulse", waiting until "load"

```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test';
  2  | 
  3  | test.describe('Earth Pulse Page', () => {
  4  |   test.beforeEach(async ({ page }) => {
> 5  |     await page.goto('/earth-pulse');
     |                ^ Error: page.goto: Could not connect to server
  6  |   });
  7  | 
  8  |   test('should display Earth Pulse heading', async ({ page }) => {
  9  |     await expect(page.getByRole('heading', { name: /Earth Pulse/i })).toBeVisible();
  10 |   });
  11 | 
  12 |   test('should display core GTI metrics', async ({ page }) => {
  13 |     await expect(page.getByText(/GTI Score/i)).toBeVisible();
  14 |     await expect(page.getByText(/Sentiment/i)).toBeVisible();
  15 |     await expect(page.getByText(/Volatility/i)).toBeVisible();
  16 |     await expect(page.getByText(/Active Events/i)).toBeVisible();
  17 |   });
  18 | 
  19 |   test('should display the Top Headlines section', async ({ page }) => {
  20 |     await expect(page.getByText(/Top Headlines/i)).toBeVisible();
  21 |   });
  22 | 
  23 |   test('should display the tension index chart section', async ({ page }) => {
  24 |     await expect(page.getByText(/Tension Index Trend \(48H\)/i)).toBeVisible();
  25 |   });
  26 | });
  27 | 
```