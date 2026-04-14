"""
Playwright smoke test for the Geopolitical Market Dashboard.

Checks that the dashboard loads and all four KPI cards are visible.
Does NOT require market data or model files — the dashboard renders
placeholder cards when data is absent, so the test passes in any state.

Prerequisites (run once):
  pip install playwright
  playwright install chromium

Usage:
  python -m test_dashboard          # from geo-market-ml/ with venv active
  python test_dashboard.py          # equivalent

The Streamlit dashboard must already be running in another terminal:
  streamlit run dashboard/app.py
"""

import sys
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

DASHBOARD_URL = "http://localhost:8501"

# Must match st.title() in dashboard/app.py exactly (emoji included)
HEADING_TEXT = "Geopolitical Tension Index — Market Dashboard"

# Must match st.metric() label arguments in dashboard/app.py exactly
KPI_LABELS = [
    "GTI Score",
    "Volatility (next hour)",
    "Direction (next hour)",
    "Conflict Events (6h window)",
]


def run_test() -> bool:
    """
    Returns True if all assertions pass, False otherwise.
    Browser is always closed even on failure.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            print(f"Navigating to {DASHBOARD_URL} ...")
            # domcontentloaded — Streamlit holds a persistent WebSocket so
            # networkidle never fires; domcontentloaded is the correct signal
            page.goto(DASHBOARD_URL, wait_until="domcontentloaded", timeout=30_000)

            print("Waiting for Streamlit to finish rendering ...")
            # Wait for the main heading — this also acts as a boot timeout
            try:
                page.wait_for_selector(
                    f"text={HEADING_TEXT}",
                    timeout=20_000,
                )
            except PlaywrightTimeout:
                print(
                    f"\nFAIL: Heading not found within 20s.\n"
                    f"  Expected substring: '{HEADING_TEXT}'\n"
                    f"  Is the dashboard running?  streamlit run dashboard/app.py"
                )
                return False
            print(f"  PASS heading: {HEADING_TEXT}")

            # Verify all four KPI cards
            print("\nChecking KPI cards ...")
            all_ok = True
            for label in KPI_LABELS:
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
    else:
        print("\nOne or more assertions failed. See output above.")
        sys.exit(1)
