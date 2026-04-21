"""Sovereign Intelligence Framework - Main Dashboard"""

import streamlit as st
from datetime import datetime
import os

from ui import tactical, earth_pulse, market, ai_signals, geo_map, trading_guide

st.set_page_config(
    page_title="Sovereign Intelligence | Tactical Archive",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

with open(os.path.join(os.path.dirname(__file__), "styles.css")) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

VIEWS = {
    "🎯 Tactical Archive":    tactical,
    "🌍 Earth Pulse":         earth_pulse,
    "📈 Market Intelligence": market,
    "🤖 AI Signals":          ai_signals,
    "🌐 Geo Map":             geo_map,
    "📖 Trading Guide":       trading_guide,
}


def render_sidebar() -> str:
    with st.sidebar:
        st.markdown("## COMMAND CENTER")
        st.markdown("---")

        selected = st.radio(
            "Intelligence Module",
            list(VIEWS.keys()),
            index=0,
            label_visibility="collapsed"
        )

        st.markdown("---")
        st.markdown("### MARKET STATUS")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("S&P 500", "8,247", "+2.3%", delta_color="normal")
        with col2:
            st.metric("VIX", "12.8", "-8.2%", delta_color="inverse")

        st.markdown("---")
        st.markdown("### SYSTEM STATUS")
        st.markdown('<div class="live-indicator">SYSTEMS ONLINE</div>', unsafe_allow_html=True)
        st.caption("Data: Real-time • Models: Active • Connections: Secure")

        st.markdown("---")
        with st.expander("⚙️ Settings"):
            st.select_slider("Update Frequency", options=["1 Min", "5 Min", "15 Min", "1 Hour"], value="5 Min")
            st.selectbox("Theme", ["Tactical (Dark)", "Archive (Darker)", "Minimal"])
            st.checkbox("Enable Alerts", value=True)

        st.markdown("---")
        st.caption(f"Last Update: {datetime.now().strftime('%H:%M:%S')}")

    return selected


def render_header():
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown("## SOVEREIGN INTELLIGENCE FRAMEWORK")
        st.caption("Tactical Archive • Real-Time Market Intelligence")
    with col2:
        st.markdown('<div class="live-indicator">LIVE FEED</div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="data-md">{datetime.now().strftime("%H:%M:%S UTC")}</div>', unsafe_allow_html=True)
    st.divider()


def render_footer():
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption("**Data Sources:** Reuters | BBC | GDELT | NewsAPI")
    with col2:
        st.caption("**Models:** LightGBM v2 | VADER Sentiment | GTI Index")
    with col3:
        st.caption("**Storage:** SQLite (news · market · gti · predictions)")


def main():
    selected = render_sidebar()
    render_header()
    VIEWS[selected].render()
    render_footer()


if __name__ == "__main__":
    main()
