"""Tactical Intelligence - Real-time market surveillance and strategic analysis"""

import streamlit as st
from datetime import datetime

from components import (
    data_card, live_indicator, status_badge, divider_section,
    activity_timeline, alert_box, hero_stat,
    StatusLevel, DataPoint, ButtonProps, button
)


def render():
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown("## TACTICAL ARCHIVE")
        st.caption("Real-time Market Intelligence & Sovereign Analysis")
    with col2:
        live_indicator("LIVE FEED")
    with col3:
        st.markdown(f'<div class="data-md">{datetime.now().strftime("%H:%M:%S")}</div>', unsafe_allow_html=True)
    st.divider()

    # Market overview
    st.markdown("### MARKET OVERVIEW")
    col1, col2, col3, col4 = st.columns(4)
    metrics = [
        ("GLOBAL INDEX", "8,247.32", StatusLevel.POSITIVE, "+2.3%"),
        ("VOLATILITY",   "12.8",     StatusLevel.NEUTRAL,  "→"),
        ("SENTIMENT",    "Bullish",  StatusLevel.POSITIVE, "+18%"),
        ("VOLUME (24H)", "342.5B",   StatusLevel.NEUTRAL,  "↑"),
    ]
    for col, (label, value, status, trend) in zip([col1, col2, col3, col4], metrics):
        with col:
            hero_stat(value, label, accent=(status == StatusLevel.POSITIVE))
            st.caption(f"<span class='{status.value}'>{trend}</span>", unsafe_allow_html=True)

    divider_section()

    # Critical alerts
    st.markdown("### CRITICAL ALERTS")
    alerts = [
        (StatusLevel.NEGATIVE, "Volatility Spike Detected",  "European markets experiencing 18% intraday variance", "2 minutes ago"),
        (StatusLevel.POSITIVE, "Bullish Breakout Forming",   "Tech index breaching 6-month resistance",             "5 minutes ago"),
        (StatusLevel.PRIMARY,  "Fed Minutes Released",       "Hawkish tone detected — market response pending",     "12 minutes ago"),
    ]
    for severity, title, desc, ts in alerts:
        c1, c2 = st.columns([0.1, 0.9])
        with c1:
            status_badge("●", severity)
        with c2:
            st.markdown(f"**{title}**")
            st.caption(desc)
            st.caption(f"<span class='text-secondary'>{ts}</span>", unsafe_allow_html=True)
        st.divider()

    divider_section()

    # Sector analysis
    st.markdown("### SECTOR INTELLIGENCE")
    sectors = [
        ("Technology",  "+8.24%", StatusLevel.POSITIVE, "87.2B"),
        ("Healthcare",  "+2.10%", StatusLevel.POSITIVE, "34.1B"),
        ("Financials",  "+1.85%", StatusLevel.POSITIVE, "56.8B"),
        ("Energy",      "-2.34%", StatusLevel.NEGATIVE, "23.4B"),
        ("Consumer",    "-0.92%", StatusLevel.NEGATIVE, "18.9B"),
        ("Industrials", "+1.23%", StatusLevel.POSITIVE, "41.5B"),
    ]
    cols = st.columns(3)
    for idx, (name, value, status, vol) in enumerate(sectors):
        with cols[idx % 3]:
            c1, c2 = st.columns([2, 1])
            with c1:
                st.markdown(f"**{name}**")
                st.caption(f"Vol: {vol}")
            with c2:
                st.markdown(f"<span class='{status.value} data-md'>{value}</span>", unsafe_allow_html=True)

    divider_section()

    # Portfolio impact
    st.markdown("### PORTFOLIO IMPACT ANALYSIS")
    col1, col2, col3 = st.columns(3)
    with col1:
        data_card("AGGRESSIVE PORTFOLIO", [
            DataPoint("+8.2%",  "Daily P&L",        StatusLevel.POSITIVE),
            DataPoint("$2.4M",  "Unrealized Gains", StatusLevel.POSITIVE),
            DataPoint("Tech: 45%", "Sector Exposure", StatusLevel.NEUTRAL),
        ])
    with col2:
        data_card("BALANCED PORTFOLIO", [
            DataPoint("+2.1%",  "Daily P&L",        StatusLevel.POSITIVE),
            DataPoint("$458K",  "Unrealized Gains", StatusLevel.POSITIVE),
            DataPoint("Mixed",  "Sector Exposure",  StatusLevel.NEUTRAL),
        ])
    with col3:
        data_card("CONSERVATIVE PORTFOLIO", [
            DataPoint("-0.3%",   "Daily P&L",         StatusLevel.NEGATIVE),
            DataPoint("-$145K",  "Unrealized Losses", StatusLevel.NEGATIVE),
            DataPoint("Bonds: 60%", "Sector Exposure", StatusLevel.NEUTRAL),
        ])

    divider_section()

    # Activity feed
    st.markdown("### ACTIVITY FEED")
    activity_timeline([
        {"time": "14:32", "title": "Large Institutional Buy",    "description": "Tech ETF accumulation: $2.3B"},
        {"time": "14:28", "title": "Economic Data Release",      "description": "Jobless claims 3.1M vs expected 3.2M"},
        {"time": "14:15", "title": "Sector Rotation Detected",   "description": "Capital flowing from Growth to Value"},
        {"time": "14:08", "title": "Supply Chain Alert",         "description": "Port congestion may impact shipping costs"},
    ])

    divider_section()

    # Geopolitical context
    st.markdown("### GEOPOLITICAL INTELLIGENCE")
    contexts = [
        ("Eastern Europe",   "ELEVATED", StatusLevel.NEGATIVE, "Energy prices +12% this week"),
        ("US-China Relations","MODERATE", StatusLevel.PRIMARY,  "Tech tariffs in discussion"),
        ("Central Banks",    "HIGH",     StatusLevel.NEUTRAL,  "Rate decisions next month"),
    ]
    for region, risk, status, impact in contexts:
        c1, c2, c3, c4 = st.columns([2, 1.5, 2, 1])
        with c1:
            st.markdown(f"**{region}**")
        with c2:
            st.markdown(f"<span class='{status.value}'>{risk}</span>", unsafe_allow_html=True)
        with c3:
            st.caption(impact)
        with c4:
            st.button("Details", key=f"geo_{region}")
        st.divider()

    divider_section()

    # 24-hour forecast
    st.markdown("### 24-HOUR FORECAST")
    c1, c2 = st.columns(2)
    with c1:
        alert_box("↑ Market likely to continue uptrend into close. Watch 8,300 resistance level.", StatusLevel.POSITIVE)
    with c2:
        alert_box("⏰ Fed speakers tomorrow AM — potential volatility trigger", StatusLevel.PRIMARY)
