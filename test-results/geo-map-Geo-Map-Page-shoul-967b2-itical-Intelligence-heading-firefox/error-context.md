# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: geo-map.spec.ts >> Geo Map Page >> should display Geopolitical Intelligence heading
- Location: tests\geo-map.spec.ts:8:7

# Error details

```
Error: page.goto: NS_ERROR_CONNECTION_REFUSED
Call log:
  - navigating to "http://localhost:3000/geo-map", waiting until "load"

```

# Page snapshot

```yaml
- generic [ref=e3]:
  - heading [level=1] [ref=e5]
  - paragraph
  - paragraph
```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test';
  2  | 
  3  | test.describe('Geo Map Page', () => {
  4  |   test.beforeEach(async ({ page }) => {
> 5  |     await page.goto('/geo-map');
     |                ^ Error: page.goto: NS_ERROR_CONNECTION_REFUSED
  6  |   });
  7  | 
  8  |   test('should display Geopolitical Intelligence heading', async ({ page }) => {
  9  |     await expect(page.getByRole('heading', { name: /Geopolitical Intelligence/i })).toBeVisible();
  10 |   });
  11 | 
  12 |   test('should display main geo metrics', async ({ page }) => {
  13 |     await expect(page.getByText(/Total Relations/i)).toBeVisible();
  14 |     await expect(page.getByText(/Critical Zones/i)).toBeVisible();
  15 |     await expect(page.getByText(/Recent Events/i)).toBeVisible();
  16 |   });
  17 | 
  18 |   test('should display bilateral relations section', async ({ page }) => {
  19 |     await expect(page.getByText(/Bilateral Relations \(Top Tensions\)/i)).toBeVisible();
  20 |   });
  21 | 
  22 |   test('should display recent geopolitical events section', async ({ page }) => {
  23 |     await expect(page.getByText(/Recent Geopolitical Events/i)).toBeVisible();
  24 |   });
  25 | });
  26 | 
```