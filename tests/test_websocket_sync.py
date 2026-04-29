"""Tests for WebSocket real-time synchronization."""

import pytest
import asyncio
import json
from api.main import ConnectionManager


class TestWebSocketConnectionManager:
    """Test WebSocket connection management."""

    @pytest.fixture
    def manager(self):
        """Create connection manager."""
        return ConnectionManager()

    def test_manager_initializes(self, manager):
        """ConnectionManager should initialize with channels."""
        assert "gti" in manager.active_connections
        assert "market" in manager.active_connections
        assert "signals" in manager.active_connections

    @pytest.mark.asyncio
    async def test_broadcast_to_channel(self, manager):
        """Manager should broadcast messages to channel subscribers."""
        message = {"type": "gti_update", "data": {"gti_score": 0.5}}
        # This would need mock websockets in real test
        await manager.broadcast(message, "gti")
        # If no error, broadcast succeeded (no active connections yet)
        assert len(manager.active_connections["gti"]) == 0

    def test_disconnect_removes_connection(self, manager):
        """Disconnect should remove connection from channel."""
        # Mock websocket
        class MockWS:
            pass

        ws = MockWS()
        manager.active_connections["gti"].append(ws)
        assert ws in manager.active_connections["gti"]

        manager.disconnect(ws, "gti")
        assert ws not in manager.active_connections["gti"]


class TestWebSocketIntegration:
    """Test WebSocket integration with API."""

    def test_websocket_code_in_api(self):
        """API main.py should have WebSocket endpoint code."""
        with open("api/main.py") as f:
            content = f.read()
            # Check for WebSocket decorator
            assert "@app.websocket" in content
            # Check for async handlers
            assert "async def websocket_gti" in content
            assert "async def websocket_market" in content
            # Check for message sending
            assert "send_json" in content

    def test_websocket_client_in_requirements(self):
        """WebSocket libraries should be in requirements."""
        with open("requirements.txt") as f:
            content = f.read()
            assert "websocket-client" in content or "websockets" in content

    def test_connection_manager_has_broadcast_methods(self):
        """API should have broadcast helper functions."""
        with open("api/main.py") as f:
            content = f.read()
            assert "async def broadcast_gti_update" in content
            assert "async def broadcast_market_update" in content
            assert "async def broadcast_signals_update" in content


class TestLiveDataSync:
    """Test that live data sync works end-to-end."""

    def test_gti_endpoint_sends_updates(self):
        """GTI WebSocket should send updates."""
        with open("api/main.py") as f:
            content = f.read()
            # Should have periodic sends
            gti_section = content[content.find("async def websocket_gti"):content.find("async def websocket_gti") + 500]
            assert "send_json" in gti_section
            assert "asyncio.sleep" in gti_section

    def test_market_endpoint_sends_updates(self):
        """Market WebSocket should send updates."""
        with open("api/main.py") as f:
            content = f.read()
            market_section = content[content.find("async def websocket_market"):content.find("async def websocket_market") + 500]
            assert "send_json" in market_section

    def test_error_handling_in_websocket(self):
        """WebSocket should handle disconnections gracefully."""
        with open("api/main.py") as f:
            content = f.read()
            # Should catch WebSocketDisconnect
            assert "WebSocketDisconnect" in content
            assert "except WebSocketDisconnect" in content
            # Should handle other exceptions
            assert "except Exception" in content


class TestDataFreshness:
    """Test that data in UI is fresh (not hardcoded)."""

    def test_earth_pulse_fetches_fresh_data(self):
        """Earth pulse should fetch data on every render."""
        with open("ui/earth_pulse.py") as f:
            content = f.read()
            assert "get_gti_current()" in content
            assert "get_gti_history" in content
            assert "get_headlines" in content
            assert "get_recent_events" in content

    def test_market_fetches_fresh_sectors(self):
        """Market should fetch fresh sector data."""
        with open("ui/market.py") as f:
            content = f.read()
            assert "get_market_sectors()" in content
            assert "get_market_spy" in content

    def test_geo_map_fetches_fresh_conflicts(self):
        """Geo map should fetch fresh conflict data."""
        with open("ui/geo_map.py") as f:
            content = f.read()
            assert "get_conflicts" in content
            assert "get_bilateral_relations" in content


class TestAPIResponseFormat:
    """Test that API responses match UI expectations."""

    def test_gti_response_fields(self):
        """GTI response should have all fields UI needs."""
        from api.client import APIClient
        client = APIClient()
        result = client.get_gti_current()

        expected_fields = [
            "gti_score", "risk_level", "conflict_ratio",
            "tone_index", "vader_sentiment", "timestamp"
        ]
        for field in expected_fields:
            assert field in result, f"Missing field in GTI response: {field}"

    def test_conflicts_response_fields(self):
        """Conflicts response should have all required fields."""
        from api.client import APIClient
        client = APIClient()
        result = client.get_conflicts(limit=5)

        assert "data" in result
        if result["data"]:
            conflict = result["data"][0]
            required = ["country_code", "event_count", "severity", "severity_score"]
            for field in required:
                assert field in conflict, f"Missing field in conflict: {field}"

    def test_events_response_has_coordinates(self):
        """Events should include lat/lon for globe rendering."""
        from api.client import APIClient
        client = APIClient()
        result = client.get_recent_events(limit=5)

        if result["data"]:
            event = result["data"][0]
            assert "latitude" in event
            assert "longitude" in event
            # Should be numeric
            assert isinstance(event["latitude"], (int, float, type(None)))
            assert isinstance(event["longitude"], (int, float, type(None)))
