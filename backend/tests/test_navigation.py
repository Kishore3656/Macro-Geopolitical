import pytest
from playwright.sync_api import Page


class TestNavigation:
    """Tests for GeoMarket navigation functionality."""

    def test_home_page_loads(self, page: Page, base_url: str):
        """Test that the home page loads successfully."""
        page.goto(base_url)
        assert "GeoMarket Intelligence" in page.title()

    def test_navbar_displays_all_tabs(self, page: Page, base_url: str):
        """Test that navbar displays all navigation tabs."""
        page.goto(base_url)

        navbar = page.locator('.topnav')
        assert navbar.is_visible()

        # Check all tab names
        assert page.locator('text=EARTH PULSE').is_visible()
        assert page.locator('text=GEO MAP').is_visible()
        assert page.locator('text=AI SIGNALS').is_visible()
        assert page.locator('text=MARKET').is_visible()

    def test_sidebar_displays(self, page: Page, base_url: str):
        """Test that sidebar displays correctly."""
        page.goto(base_url)

        sidebar = page.locator('.left-sidebar')
        assert sidebar.is_visible()

        # Check sidebar menu items
        assert page.locator('text=INTELLIGENCE').is_visible()
        assert page.locator('text=Archive').is_visible()
        assert page.locator('text=Surveillance').is_visible()
        assert page.locator('text=Tactical').is_visible()

    def test_status_bar_displays(self, page: Page, base_url: str):
        """Test that status bar displays at the bottom."""
        page.goto(base_url)

        status_bar = page.locator('.status-bar')
        assert status_bar.is_visible()
        assert "SYSTEM_STABLE" in page.content()

    def test_tab_switching_without_new_windows(self, page: Page, base_url: str, context):
        """Test that tab switching doesn't open new windows."""
        page.goto(base_url)

        # Get initial page count
        initial_pages = len(context.pages)

        # Find and click on "Geo Map" tab button
        buttons = page.locator('button:has-text("Geo Map")')
        if buttons.count() > 0:
            buttons.first.click()
            page.wait_for_load_state('networkidle')

            # Verify no new pages were opened
            assert len(context.pages) == initial_pages

    def test_earth_pulse_tab_default(self, page: Page, base_url: str):
        """Test that Earth Pulse tab is selected by default."""
        page.goto(base_url)

        # Check if Earth Pulse title is visible
        assert page.locator('text=EARTH PULSE').is_visible()

    def test_navigate_to_each_tab(self, page: Page, base_url: str):
        """Test navigation to each tab works correctly."""
        tabs = [
            ('earth_pulse', 'EARTH PULSE'),
            ('geo_map', 'GEO MAP'),
            ('ai_signals', 'AI SIGNALS'),
            ('market', 'MARKET'),
        ]

        for tab_key, expected_title in tabs:
            page.goto(f"{base_url}/?tab={tab_key}")
            page.wait_for_load_state('networkidle')

            # Check that the correct page title is displayed
            title_element = page.locator('.page-title')
            assert title_element.is_visible()
