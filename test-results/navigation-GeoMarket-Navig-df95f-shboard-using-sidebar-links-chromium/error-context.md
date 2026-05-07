# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: navigation.spec.ts >> GeoMarket Navigation >> should navigate to each dashboard using sidebar links
- Location: tests\navigation.spec.ts:19:7

# Error details

```
Error: page.goto: net::ERR_CONNECTION_REFUSED at http://localhost:3000/earth-pulse
Call log:
  - navigating to "http://localhost:3000/earth-pulse", waiting until "networkidle"

```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test';
  2  | 
  3  | test.describe('GeoMarket Navigation', () => {
  4  |   test('should redirect home to Earth Pulse and load the home page', async ({ page }) => {
  5  |     await page.goto('/', { waitUntil: 'networkidle' });
  6  |     await expect(page).toHaveURL(/\/earth-pulse$/);
  7  |     await expect(page).toHaveTitle(/GeoMarket Intelligence/);
  8  |     await expect(page.getByRole('heading', { name: /Earth Pulse/i })).toBeVisible({ timeout: 10000 });
  9  |   });
  10 | 
  11 |   test('should display the sidebar navigation links', async ({ page }) => {
  12 |     await page.goto('/earth-pulse', { waitUntil: 'networkidle' });
  13 |     await expect(page.getByRole('link', { name: /Earth Pulse/i })).toBeVisible({ timeout: 10000 });
  14 |     await expect(page.getByRole('link', { name: /Geo Map/i })).toBeVisible({ timeout: 10000 });
  15 |     await expect(page.getByRole('link', { name: /Market/i })).toBeVisible({ timeout: 10000 });
  16 |     await expect(page.getByRole('link', { name: /AI Signals/i })).toBeVisible({ timeout: 10000 });
  17 |   });
  18 | 
  19 |   test('should navigate to each dashboard using sidebar links', async ({ page }) => {
  20 |     const pages = [
  21 |       { link: /Earth Pulse/i, heading: /Earth Pulse/i, url: /\/earth-pulse$/ },
  22 |       { link: /Geo Map/i, heading: /Geopolitical Intelligence/i, url: /\/geo-map$/ },
  23 |       { link: /Market/i, heading: /Market Intelligence/i, url: /\/market$/ },
  24 |       { link: /AI Signals/i, heading: /AI Trading Signals/i, url: /\/ai-signals$/ },
  25 |     ];
  26 | 
> 27 |     await page.goto('/earth-pulse', { waitUntil: 'networkidle' });
     |                ^ Error: page.goto: net::ERR_CONNECTION_REFUSED at http://localhost:3000/earth-pulse
  28 | 
  29 |     for (const pageInfo of pages) {
  30 |       await page.getByRole('link', { name: pageInfo.link }).click();
  31 |       await expect(page).toHaveURL(pageInfo.url);
  32 |       await expect(page.getByRole('heading', { name: pageInfo.heading })).toBeVisible({ timeout: 10000 });
  33 |     }
  34 |   });
  35 | });
  36 | 
```