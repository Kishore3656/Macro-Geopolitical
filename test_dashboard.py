"""
Playwright smoke test for the GeoMarket dashboard.

Checks that the dashboard loads and the main UI sections are visible.
Does not require market data or model files because the dashboard renders
placeholders when data is absent.

Prerequisites:
  pip install playwright
  playwright install chromium

Usage:
  python -m test_dashboard
  python test_dashboard.py
"""

import sys

from playwright.sync_api import TimeoutError as PlaywrightTimeout
from playwright.sync_api import sync_playwright

DASHBOARD_URL = "http://localhost:8501"
HEADING_TEXT = "GEOMARKET INTELLIGENCE"
VISIBLE_LABELS = [
    "GTI Score",
    "Volatility Forecast",
    "Direction (next hour)",
    "Active Conflict Events",
    "News Origin Globe",
    "GTI — 48H History",
    "Currency & Commodity Impact — News Driven",
    "Latest Headlines",
]


def run_test() -> bool:
    """Return True if the dashboard shell renders its key sections."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            print(f"Navigating to {DASHBOARD_URL} ...")
            page.goto(DASHBOARD_URL, wait_until="domcontentloaded", timeout=30_000)

            print("Waiting for Streamlit to finish rendering ...")
            try:
                page.wait_for_selector(f"text={HEADING_TEXT}", timeout=20_000)
            except PlaywrightTimeout:
                print(
                    f"\nFAIL: Heading not found within 20s.\n"
                    f"  Expected substring: '{HEADING_TEXT}'\n"
                    f"  Is the dashboard running? streamlit run dashboard/app.py"
                )
                return False

            print(f"  PASS heading: {HEADING_TEXT}")
            print("\nChecking primary dashboard sections ...")

            all_ok = True
            for label in VISIBLE_LABELS:
                try:
                    page.locator(f"text={label}").first.wait_for(
                        state="visible", timeout=8_000
                    )
                    print(f"  PASS: {label}")
                except PlaywrightTimeout:
                    print(f"  FAIL: '{label}' not visible within 8s")
                    all_ok = False

            return all_ok
        except Exception as exc:
            print(f"\nUnexpected error during test: {exc}")
            return False
        finally:
            browser.close()


if __name__ == "__main__":
    passed = run_test()
    if passed:
        print("\nAll assertions passed. Dashboard is rendering correctly.")
        sys.exit(0)

    print("\nOne or more assertions failed. See output above.")
    sys.exit(1)
