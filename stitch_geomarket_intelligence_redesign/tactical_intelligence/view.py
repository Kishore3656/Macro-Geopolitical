"""
Tactical Intelligence - Real-time market surveillance and strategic analysis
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, Any, List
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components import (
    data_card, metric_box, live_indicator, panel_header,
    status_badge, divider_section, stat_comparison,
    activity_timeline, alert_box, hero_stat, section_divider,
    StatusLevel, DataPoint, ButtonProps, button
)


def render_tactical_header():
    """Top command bar"""
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.markdown("## TACTICAL ARCHIVE", unsafe_allow_html=True)
        st.caption("Real-time Market Intelligence & Sovereign Analysis")

    with col2:
        live_indicator("LIVE FEED")

    with col3:
        current_time = datetime.now().strftime("%H:%M:%S")
        st.markdown(f'<div class="data-md">{current_time}</div>', unsafe_allow_html=True)

    st.divider()


def render_market_overview():
    """Primary market metrics at a glance"""
    st.markdown("### MARKET OVERVIEW", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    metrics = [
        ("GLOBAL INDEX", "8,247.32", StatusLevel.POSITIVE, "+2.3%"),
        ("VOLATILITY", "12.8", StatusLevel.NEUTRAL, "→"),
        ("SENTIMENT", "Bullish", StatusLevel.POSITIVE, "+18%"),
        ("VOLUME (24H)", "342.5B", StatusLevel.NEUTRAL, "↑"),
    ]

    columns = [col1, col2, col3, col4]

    for col, (label, value, status, trend) in zip(columns, metrics):
        with col:
            hero_stat(value, label, accent=(status == StatusLevel.POSITIVE))
            st.caption(f"<span class='{status.value}'>{trend}</span>", unsafe_allow_html=True)


def render_critical_alerts():
    """High-priority intelligence alerts"""
    st.markdown("### CRITICAL ALERTS", unsafe_allow_html=True)

    alerts = [
        {
            "severity": StatusLevel.NEGATIVE,
            "title": "Volatility Spike Detected",
            "description": "European markets experiencing 18% intraday variance",
            "timestamp": "2 minutes ago"
        },
        {
            "severity": StatusLevel.POSITIVE,
            "title": "Bullish Breakout Forming",
            "description": "Tech index breaching 6-month resistance",
            "timestamp": "5 minutes ago"
        },
        {
            "severity": StatusLevel.PRIMARY,
            "title": "Fed Minutes Released",
            "description": "Hawkish tone detected - market response pending",
            "timestamp": "12 minutes ago"
        },
    ]

    for alert in alerts:
        col1, col2 = st.columns([0.1, 0.9])

        with col1:
            status_badge("●", alert["severity"])

        with col2:
            st.markdown(f"**{alert['title']}**")
            st.caption(alert["description"])
            st.caption(f"<span class='text-secondary'>{alert['timestamp']}</span>", unsafe_allow_html=True)

        st.divider()


def render_sector_analysis():
    """Breakdown by market sector"""
    st.markdown("### SECTOR INTELLIGENCE", unsafe_allow_html=True)

    sectors = [
        {"name": "Technology", "value": "+8.24%", "status": StatusLevel.POSITIVE, "volume": "87.2B"},
        {"name": "Healthcare", "value": "+2.10%", "status": StatusLevel.POSITIVE, "volume": "34.1B"},
        {"name": "Financials", "value": "+1.85%", "status": StatusLevel.POSITIVE, "volume": "56.8B"},
        {"name": "Energy", "value": "-2.34%", "status": StatusLevel.NEGATIVE, "volume": "23.4B"},
        {"name": "Consumer", "value": "-0.92%", "status": StatusLevel.NEGATIVE, "volume": "18.9B"},
        {"name": "Industrials", "value": "+1.23%", "status": StatusLevel.POSITIVE, "volume": "41.5B"},
    ]

    cols = st.columns(3)

    for idx, sector in enumerate(sectors):
        with cols[idx % 3]:
            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown(f"**{sector['name']}**")
                st.caption(f"Vol: {sector['volume']}")

            with col2:
                st.markdown(
                    f"<span class='{sector['status'].value} data-md'>{sector['value']}</span>",
                    unsafe_allow_html=True
                )


def render_activity_feed():
    """Real-time market activity timeline"""
    st.markdown("### ACTIVITY FEED", unsafe_allow_html=True)

    events = [
        {
            "time": "14:32",
            "title": "Large Institutional Buy",
            "description": "Tech ETF accumulation: $2.3B",
        },
        {
            "time": "14:28",
            "title": "Economic Data Release",
            "description": "jobless claims at 3.1M vs expected 3.2M",
        },
        {
            "time": "14:15",
            "title": "Sector Rotation Detected",
            "description": "Capital flowing from Growth to Value",
        },
        {
            "time": "14:08",
            "title": "Supply Chain Alert",
            "description": "Port congestion may impact shipping costs",
        },
    ]

    activity_timeline(events)


def render_portfolio_impact():
    """How current movements affect portfolios"""
    st.markdown("### PORTFOLIO IMPACT ANALYSIS", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        data_card(
            "AGGRESSIVE PORTFOLIO",
            [
                DataPoint("+8.2%", "Daily P&L", StatusLevel.POSITIVE),
                DataPoint("$2.4M", "Unrealized Gains", StatusLevel.POSITIVE),
                DataPoint("Tech: 45%", "Sector Exposure", StatusLevel.NEUTRAL),
            ]
        )

    with col2:
        data_card(
            "BALANCED PORTFOLIO",
            [
                DataPoint("+2.1%", "Daily P&L", StatusLevel.POSITIVE),
                DataPoint("$458K", "Unrealized Gains", StatusLevel.POSITIVE),
                DataPoint("Mixed", "Sector Exposure", StatusLevel.NEUTRAL),
            ]
        )

    with col3:
        data_card(
            "CONSERVATIVE PORTFOLIO",
            [
                DataPoint("-0.3%", "Daily P&L", StatusLevel.NEGATIVE),
                DataPoint("-$145K", "Unrealized Losses", StatusLevel.NEGATIVE),
                DataPoint("Bonds: 60%", "Sector Exposure", StatusLevel.NEUTRAL),
            ]
        )


def render_geopolitical_context():
    """Global factors affecting markets"""
    st.markdown("### GEOPOLITICAL INTELLIGENCE", unsafe_allow_html=True)

    contexts = [
        {
            "region": "Eastern Europe",
            "risk": "ELEVATED",
            "impact": "Energy prices +12% this week",
            "status": StatusLevel.NEGATIVE
        },
        {
            "region": "US-China Relations",
            "risk": "MODERATE",
            "impact": "Tech tariffs in discussion",
            "status": StatusLevel.PRIMARY
        },
        {
            "region": "Central Banks",
            "risk": "HIGH",
            "impact": "Rate decisions next month",
            "status": StatusLevel.NEUTRAL
        },
    ]

    for context in contexts:
        col1, col2, col3, col4 = st.columns([2, 1.5, 2, 1])

        with col1:
            st.markdown(f"**{context['region']}**")

        with col2:
            st.markdown(
                f"<span class='{context['status'].value}'>{context['risk']}</span>",
                unsafe_allow_html=True
            )

        with col3:
            st.caption(context['impact'])

        with col4:
            st.button("Details", key=f"geo_{context['region']}")

        st.divider()


def render_forecast_panel():
    """Next-24h market forecast"""
    st.markdown("### 24-HOUR FORECAST", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        alert_box(
            "⬆ Market likely to continue uptrend into close. Watch 8,300 resistance level.",
            StatusLevel.POSITIVE
        )

    with col2:
        alert_box(
            "⏰ Fed speakers tomorrow AM — potential volatility trigger",
            StatusLevel.PRIMARY
        )


def render():
    """Main tactical intelligence view"""
    # Apply custom CSS
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "styles.css")) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Header
    render_tactical_header()

    # Primary content sections
    render_market_overview()
    divider_section()

    render_critical_alerts()
    divider_section()

    render_sector_analysis()
    divider_section()

    render_portfolio_impact()
    divider_section()

    render_activity_feed()
    divider_section()

    render_geopolitical_context()
    divider_section()

    render_forecast_panel()


if __name__ == "__main__":
    st.set_page_config(
        page_title="Tactical Archive | Sovereign Intelligence",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    render()
