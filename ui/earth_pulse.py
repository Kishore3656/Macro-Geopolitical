"""Earth Pulse - Geospatial market analysis and global intelligence"""

import streamlit as st
from datetime import datetime

from components import (
    data_card, live_indicator, status_badge, divider_section,
    alert_box, hero_stat,
    StatusLevel, DataPoint
)


def render():
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown("## EARTH PULSE")
        st.caption("Global Market Movement & Geospatial Intelligence")
    with col2:
        live_indicator("SATELLITE FEED")
    with col3:
        st.markdown(f'<div class="data-md">{datetime.now().strftime("%H:%M:%S")}</div>', unsafe_allow_html=True)
    st.divider()

    # Global heatmap
    st.markdown("### GLOBAL MARKET HEATMAP")
    col1, col2, col3 = st.columns(3)
    regions = [
        ("Asia-Pacific", "+4.2%", StatusLevel.POSITIVE, "12"),
        ("Europe",       "+1.8%", StatusLevel.POSITIVE, "8"),
        ("Americas",     "+2.9%", StatusLevel.POSITIVE, "15"),
    ]
    for col, (name, value, status, markets) in zip([col1, col2, col3], regions):
        with col:
            st.markdown(f"**{name}**")
            st.markdown(f"<p class='data-lg {status.value}'>{value}</p>", unsafe_allow_html=True)
            st.caption(f"{markets} active markets")

    divider_section()

    # Major exchanges
    st.markdown("### MAJOR EXCHANGE PULSE")
    exchanges = [
        ("NYSE", "USA",       "S&P 500",            "8,247.32",  "+2.3%", StatusLevel.POSITIVE, "12.8"),
        ("LSE",  "UK",        "FTSE 100",            "7,842.55",  "+1.2%", StatusLevel.POSITIVE, "8.4"),
        ("TSE",  "Japan",     "Nikkei 225",          "29,156.82", "+3.1%", StatusLevel.POSITIVE, "14.2"),
        ("SSE",  "China",     "Shanghai Composite",  "3,087.42",  "-0.8%", StatusLevel.NEGATIVE, "16.5"),
        ("DAX",  "Germany",   "DAX 40",              "17,823.45", "+0.9%", StatusLevel.POSITIVE, "9.2"),
        ("ASX",  "Australia", "ASX 200",             "7,456.23",  "+1.4%", StatusLevel.POSITIVE, "11.3"),
    ]
    for exch, region, index, value, change, status, vol in exchanges:
        c1, c2, c3, c4, c5 = st.columns([1.5, 1.5, 1.5, 1, 1])
        with c1:
            st.markdown(f"**{exch}**")
            st.caption(region)
        with c2:
            st.markdown(f"<span class='label-md'>{index}</span>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<span class='data-md'>{value}</span>", unsafe_allow_html=True)
        with c4:
            st.markdown(f"<span class='{status.value}'>{change}</span>", unsafe_allow_html=True)
        with c5:
            vol_status = StatusLevel.NEGATIVE if float(vol) > 13 else StatusLevel.POSITIVE
            st.markdown(f"<span class='{vol_status.value} data-sm'>σ{vol}</span>", unsafe_allow_html=True)
        st.divider()

    divider_section()

    # Capital flows
    st.markdown("### CAPITAL FLOW INTELLIGENCE")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Inbound Capital")
        for source, amount in [("Emerging Markets", "$8.4B"), ("Sovereign Funds", "$5.2B"), ("Retail Investors", "$2.1B")]:
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"**{source}**")
            with c2:
                st.markdown(f"<span class='text-positive'>{amount}</span>", unsafe_allow_html=True)
            st.divider()
    with col2:
        st.markdown("#### Outbound Capital")
        for dest, amount, status in [("Currency Markets", "$3.2B", StatusLevel.NEGATIVE), ("Commodities", "$1.8B", StatusLevel.NEGATIVE), ("Bonds", "$2.5B", StatusLevel.NEUTRAL)]:
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"**{dest}**")
            with c2:
                st.markdown(f"<span class='{status.value}'>{amount}</span>", unsafe_allow_html=True)
            st.divider()

    divider_section()

    # Geo-risk markers
    st.markdown("### GEO-RISK MARKERS")
    risks = [
        ("Eastern Europe",       "HIGH",     StatusLevel.NEGATIVE, "Energy prices, defense stocks",           "↑ Escalating"),
        ("US-Taiwan Strait",     "MODERATE", StatusLevel.PRIMARY,  "Tech supply chains, semiconductor prices", "→ Stable"),
        ("Middle East Oil Routes","MODERATE", StatusLevel.PRIMARY,  "Oil & gas, shipping costs",               "↓ Improving"),
        ("EU Regulatory Changes","MODERATE", StatusLevel.PRIMARY,  "Tech fines, banking regulations",         "→ Ongoing"),
    ]
    for loc, risk_level, status, impact, trend in risks:
        c1, c2, c3, c4 = st.columns([1.5, 1.2, 2, 1.3])
        with c1:
            st.markdown(f"**{loc}**")
        with c2:
            st.markdown(f"<span class='{status.value} label-md'>{risk_level}</span>", unsafe_allow_html=True)
        with c3:
            st.caption(impact)
        with c4:
            st.markdown(f"<span class='text-secondary'>{trend}</span>", unsafe_allow_html=True)
        st.divider()

    divider_section()

    # Economic calendar
    st.markdown("### ECONOMIC CALENDAR (NEXT 7 DAYS)")
    calendar = [
        ("Today",    "14:30", "USA", "Fed Minutes",      "HIGH"),
        ("Tomorrow", "09:00", "EUR", "CPI Release",      "HIGH"),
        ("Wed",      "15:00", "GBP", "BOE Decision",     "CRITICAL"),
        ("Thu",      "08:30", "JPY", "Employment Data",  "MEDIUM"),
        ("Fri",      "13:30", "USA", "Jobs Report",      "CRITICAL"),
    ]
    for date, time, country, event, impact in calendar:
        c1, c2, c3, c4, c5 = st.columns([1, 1, 1, 2, 1])
        with c1:
            st.caption(f"**{date}**")
        with c2:
            st.caption(time)
        with c3:
            st.markdown(f"<span class='label-md'>{country}</span>", unsafe_allow_html=True)
        with c4:
            st.markdown(f"**{event}**")
        with c5:
            impact_status = StatusLevel.NEGATIVE if impact == "CRITICAL" else StatusLevel.PRIMARY
            st.markdown(f"<span class='{impact_status.value}'>{impact}</span>", unsafe_allow_html=True)
        st.divider()

    divider_section()

    # Market synchronization
    st.markdown("### MARKET SYNCHRONIZATION INDEX")
    col1, col2, col3 = st.columns(3)
    with col1:
        data_card("EQUITY CORRELATION", [
            DataPoint("0.87", "All Markets", StatusLevel.POSITIVE),
            DataPoint("0.92", "Developed",   StatusLevel.POSITIVE),
            DataPoint("0.65", "Emerging",    StatusLevel.NEUTRAL),
        ])
    with col2:
        data_card("SECTOR COHERENCE", [
            DataPoint("0.76", "Tech Leading",    StatusLevel.POSITIVE),
            DataPoint("0.43", "Energy Lagging",  StatusLevel.NEGATIVE),
            DataPoint("0.81", "Financials",      StatusLevel.POSITIVE),
        ])
    with col3:
        data_card("CURRENCY MOVES", [
            DataPoint("USD Index: 104.2", "Strong Dollar", StatusLevel.POSITIVE),
            DataPoint("EUR/USD: 1.09",    "Euro Weak",     StatusLevel.NEGATIVE),
            DataPoint("JPY Vol: 18.4%",   "Elevated",      StatusLevel.NEUTRAL),
        ])
