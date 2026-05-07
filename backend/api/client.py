"""
Streamlit client for the GeoMarket API.
Handles HTTP requests to backend endpoints with caching and error handling.
"""

import requests
import streamlit as st
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

# Determine API URL from environment or default
API_BASE_URL = "http://localhost:8000"


@st.cache_data(ttl=60)
def _cached_get(endpoint: str) -> Dict[str, Any]:
    """Cached GET request (no params)."""
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


@st.cache_data(ttl=300)
def _cached_get_with_param(endpoint: str, param_name: str, param_value: Any) -> Dict[str, Any]:
    """Cached GET request with single parameter."""
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}", params={param_name: param_value}, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


@st.cache_data(ttl=60)
def _cached_get_events(event_type: str, limit: int) -> Dict[str, Any]:
    """Cached GET request for events with event_type and limit."""
    try:
        response = requests.get(f"{API_BASE_URL}/api/events", params={"event_type": event_type, "limit": limit}, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


class APIClient:
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()

    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make GET request to API endpoint."""
        try:
            url = f"{self.base_url}{endpoint}"
            response = self.session.get(url, params=params, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def get_gti_current(self) -> Dict[str, Any]:
        """Get current GTI score and components."""
        return _cached_get("/api/gti")

    def get_gti_history(self, hours: int = 48) -> Dict[str, Any]:
        """Get GTI history for last N hours."""
        return _cached_get_with_param("/api/gti/history", "hours", hours)

    def get_signals_current(self) -> Dict[str, Any]:
        """Get latest ML predictions."""
        return _cached_get("/api/signals")

    def get_signals_history(self, limit: int = 100) -> Dict[str, Any]:
        """Get prediction history."""
        return _cached_get_with_param("/api/signals/history", "limit", limit)

    def get_headlines(self, limit: int = 20) -> Dict[str, Any]:
        """Get latest headlines with sentiment."""
        return _cached_get_with_param("/api/headlines", "limit", limit)

    def get_market_spy(self, bars: int = 100) -> Dict[str, Any]:
        """Get S&P 500 market data."""
        return _cached_get_with_param("/api/market/spy", "bars", bars)

    def get_market_sectors(self) -> Dict[str, Any]:
        """Get sector performance data."""
        return _cached_get("/api/market/sectors")

    def get_conflicts(self, limit: int = 15) -> Dict[str, Any]:
        """Get active conflicts from GDELT."""
        return _cached_get_with_param("/api/conflicts", "limit", limit)

    def get_bilateral_relations(self, limit: int = 10) -> Dict[str, Any]:
        """Get bilateral geopolitical relationships."""
        return _cached_get_with_param("/api/bilateral", "limit", limit)

    def get_recent_events(self, event_type: str = "all", limit: int = 20) -> Dict[str, Any]:
        """Get recent geopolitical events."""
        return _cached_get_events(event_type, limit)

    def health_check(self) -> bool:
        """Check if API is healthy."""
        try:
            response = self._get("/health")
            return response.get("status") == "healthy"
        except:
            return False


# Global client instance
_client: Optional[APIClient] = None


def get_client() -> APIClient:
    """Get or create the global API client."""
    global _client
    if _client is None:
        _client = APIClient()
    return _client


def is_api_ready() -> bool:
    """Check if API is accessible."""
    return get_client().health_check()


# ────────────────────────────────────────────────────────────────────────────
# Module-level cached functions (for Streamlit @st.cache_data compatibility)
# These wrap the client methods to avoid hashing self parameter
# ────────────────────────────────────────────────────────────────────────────

@st.cache_data(ttl=60)
def _cached_get(endpoint: str) -> Dict[str, Any]:
    """Module-level cached GET without self parameter."""
    return get_client()._get(endpoint)


@st.cache_data(ttl=300)
def _cached_get_with_param(endpoint: str, param_name: str, param_value) -> Dict[str, Any]:
    """Module-level cached GET with single parameter."""
    return get_client()._get(endpoint, {param_name: param_value})


@st.cache_data(ttl=60)
def _cached_get_events(event_type: str, limit: int) -> Dict[str, Any]:
    """Module-level cached GET for events with two parameters."""
    return get_client()._get("/api/events", {"event_type": event_type, "limit": limit})
