# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: market.spec.ts >> Market Intelligence Page >> should display main chart and market state sections
- Location: tests\market.spec.ts:19:7

# Error details

```
Error: page.goto: net::ERR_CONNECTION_REFUSED at http://localhost:3000/market
Call log:
  - navigating to "http://localhost:3000/market", waiting until "load"

```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test';
  2  | 
  3  | test.describe('Market Intelligence Page', () => {
  4  |   test.beforeEach(async ({ page }) => {
> 5  |     await page.goto('/market');
     |                ^ Error: page.goto: net::ERR_CONNECTION_REFUSED at http://localhost:3000/market
  6  |   });
  7  | 
  8  |   test('should display Market Intelligence heading', async ({ page }) => {
  9  |     await expect(page.getByRole('heading', { name: /Market Intelligence/i })).toBeVisible();
  10 |   });
  11 | 
  12 |   test('should display SPY metric cards', async ({ page }) => {
  13 |     await expect(page.locator('p', { hasText: 'SPY Price' })).toBeVisible();
  14 |     await expect(page.getByText(/Daily Change/i)).toBeVisible();
  15 |     await expect(page.locator('p', { hasText: 'Volume' })).toBeVisible();
  16 |     await expect(page.getByText(/52W High/i)).toBeVisible();
  17 |   });
  18 | 
  19 |   test('should display main chart and market state sections', async ({ page }) => {
  20 |     await expect(page.getByText(/SPY 5-Day Chart \(1H\)/i)).toBeVisible();
  21 |     await expect(page.getByText(/Market State/i)).toBeVisible();
  22 |   });
  23 | 
  24 |   test('should display sector performance section', async ({ page }) => {
  25 |     await expect(page.getByRole('heading', { name: /Sector Performance/i })).toBeVisible();
  26 |   });
  27 | });
  28 | 
```