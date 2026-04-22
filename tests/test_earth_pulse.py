import pytest
from playwright.sync_api import Page


class TestEarthPulsePage:
    """Tests for Earth Pulse dashboard page."""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page, base_url: str):
        """Navigate to Earth Pulse page before each test."""
        page.goto(f"{base_url}/?tab=earth_pulse")
        page.wait_for_load_state('networkidle')

    def test_earth_pulse_title_visible(self, page: Page):
        """Test that Earth Pulse title is displayed."""
        title = page.locator('.page-title')
        assert title.is_visible()
        assert 'EARTH PULSE' in page.content()

    def test_page_subtitle_visible(self, page: Page):
        """Test that page subtitle is displayed."""
        subtitle = page.locator('.page-subtitle')
        assert subtitle.is_visible()
        assert 'GLOBAL MARKETS & MACRO TENSIONS' in page.content()

    def test_gti_hero_number_visible(self, page: Page):
        """Test that GTI hero number is displayed."""
        hero = page.locator('.gti-hero-number')
        assert hero.is_visible()

    def test_system_status_visible(self, page: Page):
        """Test that system status is displayed."""
        status = page.locator('.system-status-row')
        assert status.is_visible()
        assert 'STATUS:' in page.content()

    def test_live_intelligence_feed_visible(self, page: Page):
        """Test that Live Intelligence Feed section is visible."""
        assert 'LIVE INTELLIGENCE FEED' in page.content()

    def test_macro_components_visible(self, page: Page):
        """Test that Macro Components section is visible."""
        assert 'MACRO COMPONENTS' in page.content()

    def test_signal_cards_visible(self, page: Page):
        """Test that signal cards are visible."""
        signal_cards = page.locator('.signal-card')
        assert signal_cards.count() > 0

        # Check for specific signal names
        assert 'CONFLICT RATIO' in page.content()
        assert 'MEDIA TONE' in page.content()

    def test_gti_badge_visible(self, page: Page):
        """Test that GTI badge is visible."""
        badge = page.locator('.gti-hero-badge')
        assert badge.is_visible()

    def test_progress_bars_visible(self, page: Page):
        """Test that progress bars are visible."""
        bars = page.locator('.signal-bar-fill')
        assert bars.count() > 0

    def test_page_has_proper_layout(self, page: Page):
        """Test that page has proper layout structure."""
        # Check main content area exists
        main_col = page.locator('[data-testid="stVerticalBlock"]')
        assert main_col.count() > 0

    def test_hero_metadata_visible(self, page: Page):
        """Test that hero metadata is visible."""
        meta = page.locator('.gti-hero-meta')
        assert meta.is_visible()
