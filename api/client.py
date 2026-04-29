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

    @st.cache_data(ttl=60)
    def get_gti_current(self) -> Dict[str, Any]:
        """Get current GTI score and components."""
        return self._get("/api/gti")

    @st.cache_data(ttl=300)
    def get_gti_history(self, hours: int = 48) -> Dict[str, Any]:
        """Get GTI history for last N hours."""
        return self._get("/api/gti/history", {"hours": hours})

    @st.cache_data(ttl=60)
    def get_signals_current(self) -> Dict[str, Any]:
        """Get latest ML predictions."""
        return self._get("/api/signals")

    @st.cache_data(ttl=300)
    def get_signals_history(self, limit: int = 100) -> Dict[str, Any]:
        """Get prediction history."""
        return self._get("/api/signals/history", {"limit": limit})

    @st.cache_data(ttl=120)
    def get_headlines(self, limit: int = 20) -> Dict[str, Any]:
        """Get latest headlines with sentiment."""
        return self._get("/api/headlines", {"limit": limit})

    @st.cache_data(ttl=300)
    def get_market_spy(self, bars: int = 100) -> Dict[str, Any]:
        """Get S&P 500 market data."""
        return self._get("/api/market/spy", {"bars": bars})

    @st.cache_data(ttl=300)
    def get_market_sectors(self) -> Dict[str, Any]:
        """Get sector performance data."""
        return self._get("/api/market/sectors")

    @st.cache_data(ttl=60)
    def get_conflicts(self, limit: int = 15) -> Dict[str, Any]:
        """Get active conflicts from GDELT."""
        return self._get("/api/conflicts", {"limit": limit})

    @st.cache_data(ttl=60)
    def get_bilateral_relations(self, limit: int = 10) -> Dict[str, Any]:
        """Get bilateral geopolitical relationships."""
        return self._get("/api/bilateral", {"limit": limit})

    @st.cache_data(ttl=60)
    def get_recent_events(self, event_type: str = "all", limit: int = 20) -> Dict[str, Any]:
        """Get recent geopolitical events."""
        return self._get("/api/events", {"event_type": event_type, "limit": limit})

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
