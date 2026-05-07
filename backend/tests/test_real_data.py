"""Tests for real data endpoints and live data binding."""

import pytest
from datetime import datetime
from api.client import APIClient


@pytest.fixture
def api_client():
    """Create API client for testing."""
    return APIClient()


class TestRealDataEndpoints:
    """Test that UI modules fetch real data from API endpoints."""

    def test_gti_endpoint_returns_real_data(self, api_client):
        """GTI endpoint should return current score from DB, not hardcoded 26.5."""
        result = api_client.get_gti_current()
        assert "gti_score" in result
        assert "risk_level" in result
        assert "conflict_ratio" in result
        assert "tone_index" in result
        assert "vader_sentiment" in result
        assert isinstance(result["gti_score"], (int, float))

    def test_conflicts_endpoint(self, api_client):
        """Conflicts endpoint should return real conflict data."""
        result = api_client.get_conflicts(limit=15)
        assert "data" in result
        assert isinstance(result["data"], list)
        if result["data"]:
            conflict = result["data"][0]
            assert "country_code" in conflict
            assert "event_count" in conflict
            assert "severity" in conflict

    def test_bilateral_endpoint(self, api_client):
        """Bilateral relations endpoint should return real relationship data."""
        result = api_client.get_bilateral_relations(limit=10)
        assert "data" in result
        assert isinstance(result["data"], list)
        if result["data"]:
            relation = result["data"][0]
            assert "pair" in relation
            assert "stress_level" in relation

    def test_events_endpoint(self, api_client):
        """Events endpoint should return real geopolitical events."""
        result = api_client.get_recent_events(event_type="conflict", limit=20)
        assert "data" in result
        assert "event_type" in result
        assert isinstance(result["data"], list)
        if result["data"]:
            event = result["data"][0]
            assert "event_id" in event
            assert "date" in event
            assert "goldstein_scale" in event

    def test_market_spy_endpoint(self, api_client):
        """Market SPY endpoint should return real OHLCV data."""
        result = api_client.get_market_spy(bars=100)
        assert "current_price" in result
        assert "daily_change" in result
        assert "data" in result
        assert isinstance(result["data"], list)
        if result["data"]:
            bar = result["data"][0]
            assert "open" in bar
            assert "high" in bar
            assert "low" in bar
            assert "close" in bar

    def test_market_sectors_endpoint(self, api_client):
        """Market sectors endpoint should return real sector data."""
        result = api_client.get_market_sectors()
        assert "sectors" in result
        assert isinstance(result["sectors"], list)
        assert len(result["sectors"]) > 0
        sector = result["sectors"][0]
        assert "name" in sector
        assert "symbol" in sector
        assert "change" in sector
        assert "price" in sector
        # Verify it's real data (not hardcoded)
        assert isinstance(sector["price"], (int, float))
        assert sector["price"] > 0


class TestNoHardcodedData:
    """Test that hardcoded data has been removed."""

    def test_navbar_gti_not_hardcoded(self):
        """App navbar GTI score should come from API, not hardcoded 26.5."""
        # This test is run by checking app.py doesn't have gti_score = 26.5
        with open("app.py") as f:
            content = f.read()
            # Should not have hardcoded assignment
            assert "gti_score = 26.5" not in content
            # Should fetch from API
            assert "get_gti_current()" in content

    def test_earth_pulse_uses_api_hotspots(self):
        """Earth pulse should fetch hotspots from API, not use hardcoded lats/lons."""
        with open("ui/earth_pulse.py") as f:
            content = f.read()
            # Should not have fixed hardcoded arrays
            assert "lats_conflict = [50.4, 48.0" not in content
            # Should fetch from API
            assert "get_recent_events" in content

    def test_geo_map_uses_api_conflicts(self):
        """Geo map should fetch conflicts from API."""
        with open("ui/geo_map.py") as f:
            content = f.read()
            # Should fetch from API
            assert "get_conflicts" in content or "conflicts_data" in content

    def test_market_vix_not_synthetic(self):
        """Market VIX should use real data, not random.seed()."""
        with open("ui/market.py") as f:
            content = f.read()
            # Should not use seeded random
            assert "random.seed(11)" not in content
            # Should fetch real data
            assert "client" in content


class TestWebSocketEndpoints:
    """Test WebSocket functionality."""

    def test_websocket_endpoints_exist(self):
        """API should have WebSocket endpoints defined."""
        with open("api/main.py") as f:
            content = f.read()
            assert "@app.websocket" in content
            assert "/ws/gti" in content
            assert "/ws/market" in content
            assert "/ws/signals" in content

    def test_connection_manager_exists(self):
        """API should have WebSocket ConnectionManager."""
        with open("api/main.py") as f:
            content = f.read()
            assert "class ConnectionManager" in content
            assert "async def connect" in content
            assert "async def broadcast" in content


class TestLiveDataFlow:
    """Test that data flows from API to UI correctly."""

    def test_gti_current_has_required_fields(self, api_client):
        """GTI should return all required fields for UI rendering."""
        result = api_client.get_gti_current()
        required_fields = ["gti_score", "risk_level", "conflict_ratio", "tone_index", "vader_sentiment"]
        for field in required_fields:
            assert field in result, f"Missing field: {field}"

    def test_events_have_location_data(self, api_client):
        """Events should include location for globe rendering."""
        result = api_client.get_recent_events(limit=5)
        if result["data"]:
            event = result["data"][0]
            # Should have coordinates for globe
            assert "latitude" in event
            assert "longitude" in event

    def test_sectors_match_expected_names(self, api_client):
        """Sectors should include the standard sector ETFs."""
        result = api_client.get_market_sectors()
        sectors = result.get("sectors", [])
        symbols = [s["symbol"] for s in sectors]
        # Should have at least some standard sectors
        expected_symbols = ["XLK", "XLV", "XLF", "XLE", "XLI"]
        for symbol in expected_symbols:
            assert symbol in symbols, f"Missing sector: {symbol}"
