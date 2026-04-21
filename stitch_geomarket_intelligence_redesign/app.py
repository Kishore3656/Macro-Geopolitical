"""
Sovereign Intelligence Framework - Main Dashboard
Multi-view tactical market intelligence platform
"""

import streamlit as st
from datetime import datetime
import sys
import os

# Import views
from tactical_intelligence import view as tactical_view
from earth_pulse_geomarket_intelligence import view as earth_pulse_view
from market_geomarket_intelligence import view as market_view
from ai_signals_geomarket_intelligence import view as ai_signals_view
from geo_map_geomarket_intelligence import view as geo_map_view

# Page configuration
st.set_page_config(
    page_title="Sovereign Intelligence | Tactical Archive",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply global CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def render_sidebar():
    """Main navigation sidebar"""
    with st.sidebar:
        st.markdown("## COMMAND CENTER", unsafe_allow_html=True)

        st.markdown("---")

        # Navigation menu
        selected = st.radio(
            "Intelligence Module",
            [
                "🎯 Tactical Archive",
                "🌍 Earth Pulse",
                "📈 Market Intelligence",
                "🤖 AI Signals",
                "🌐 Geo Map"
            ],
            index=0,
            label_visibility="collapsed"
        )

        st.markdown("---")

        # Quick stats
        st.markdown("### MARKET STATUS", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("S&P 500", "8,247", "+2.3%", delta_color="normal")
        with col2:
            st.metric("VIX", "12.8", "-8.2%", delta_color="inverse")

        st.markdown("---")

        # System status
        st.markdown("### SYSTEM STATUS", unsafe_allow_html=True)
        st.markdown("""
        <div class="live-indicator">SYSTEMS ONLINE</div>
        """, unsafe_allow_html=True)

        st.caption("Data: Real-time • Models: Active • Connections: Secure")

        st.markdown("---")

        # Settings
        with st.expander("⚙️ Settings"):
            update_freq = st.select_slider(
                "Update Frequency",
                options=["1 Min", "5 Min", "15 Min", "1 Hour"],
                value="5 Min"
            )

            theme = st.selectbox(
                "Theme",
                ["Tactical (Dark)", "Archive (Darker)", "Minimal"]
            )

            alerts = st.checkbox("Enable Alerts", value=True)

        st.markdown("---")
        st.caption(f"Last Update: {datetime.now().strftime('%H:%M:%S')}")

        return selected


def render_header():
    """Main header with time and status"""
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.markdown("## SOVEREIGN INTELLIGENCE FRAMEWORK", unsafe_allow_html=True)
        st.caption("Tactical Archive • Real-Time Market Intelligence")

    with col2:
        st.markdown(
            '<div class="live-indicator">LIVE FEED</div>',
            unsafe_allow_html=True
        )

    with col3:
        current_time = datetime.now().strftime("%H:%M:%S UTC")
        st.markdown(f'<div class="data-md">{current_time}</div>', unsafe_allow_html=True)

    st.divider()


def render_footer():
    """Footer information"""
    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.caption("**Data Sources:** Bloomberg | Reuters | Fed")

    with col2:
        st.caption("**Models:** ML Pipeline v2.3 | Sentiment Analysis")

    with col3:
        st.caption("**Security:** AES-256 Encrypted | Zero-Trust Auth")


def main():
    """Main application entry point"""
    # Render sidebar and get active view
    selected_view = render_sidebar()

    # Render main header
    render_header()

    # Route to selected view
    if "Tactical Archive" in selected_view:
        tactical_view.render()

    elif "Earth Pulse" in selected_view:
        earth_pulse_view.render()

    elif "Market Intelligence" in selected_view:
        market_view.render()

    elif "AI Signals" in selected_view:
        ai_signals_view.render()

    elif "Geo Map" in selected_view:
        geo_map_view.render()

    # Render footer
    render_footer()


if __name__ == "__main__":
    main()
