"""Geo Map - Interactive geographic market intelligence"""

import streamlit as st
from datetime import datetime

from components import (
    data_card, live_indicator, divider_section, hero_stat,
    StatusLevel, DataPoint
)


def render():
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown("## GEO MAP")
        st.caption("Interactive Geographic Market Intelligence")
    with col2:
        live_indicator("MAP DATA LIVE")
    with col3:
        st.markdown(f'<div class="data-md">{datetime.now().strftime("%H:%M:%S")}</div>', unsafe_allow_html=True)
    st.divider()

    # Regional breakdown
    st.markdown("### REGIONAL MARKET PERFORMANCE")
    regions = [
        ("North America",   "S&P 500",  "8,247.32", "+2.3%", StatusLevel.POSITIVE, "2,847", "$2.1T"),
        ("Europe",          "STOXX 600","487.24",    "+1.2%", StatusLevel.POSITIVE, "600",   "$890B"),
        ("Asia-Pacific",    "MSCI APJ", "3,456.78",  "+3.4%", StatusLevel.POSITIVE, "1,230", "$5.2T"),
        ("Emerging Markets","MSCI EM",  "1,087.34",  "+1.8%", StatusLevel.POSITIVE, "789",   "$1.1T"),
    ]
    for region, index, value, change, status, companies, volume in regions:
        c1, c2, c3, c4, c5 = st.columns([1.5, 1.5, 1, 1.5, 1.5])
        with c1:
            st.markdown(f"**{region}**")
            st.caption(index)
        with c2:
            st.markdown(f"<span class='data-lg'>{value}</span>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<span class='{status.value}'>{change}</span>", unsafe_allow_html=True)
        with c4:
            st.caption(f"Companies: {companies}")
        with c5:
            st.caption(f"Volume: {volume}")
        st.divider()

    divider_section()

    # Country heatmap
    st.markdown("### COUNTRY PERFORMANCE HEATMAP")
    countries = [
        ("USA",         "+2.8%", StatusLevel.POSITIVE, "$48.2T"),
        ("Japan",       "+3.2%", StatusLevel.POSITIVE, "$5.1T"),
        ("UK",          "+1.1%", StatusLevel.POSITIVE, "$3.4T"),
        ("Germany",     "+0.9%", StatusLevel.POSITIVE, "$2.8T"),
        ("France",      "+1.2%", StatusLevel.POSITIVE, "$2.5T"),
        ("Switzerland", "+0.7%", StatusLevel.POSITIVE, "$1.9T"),
        ("India",       "+4.2%", StatusLevel.POSITIVE, "$4.2T"),
        ("China",       "-0.8%", StatusLevel.NEGATIVE, "$9.8T"),
        ("Australia",   "+1.4%", StatusLevel.POSITIVE, "$1.8T"),
        ("Brazil",      "+2.1%", StatusLevel.POSITIVE, "$0.9T"),
        ("Canada",      "+1.8%", StatusLevel.POSITIVE, "$2.3T"),
        ("South Korea", "+2.9%", StatusLevel.POSITIVE, "$1.8T"),
    ]
    cols = st.columns(4)
    for idx, (country, ret, status, mcap) in enumerate(countries):
        with cols[idx % 4]:
            st.markdown(f"**{country}**")
            st.markdown(f"<span class='{status.value} data-md'>{ret}</span>", unsafe_allow_html=True)
            st.caption(f"MCap: {mcap}")
            st.divider()

    divider_section()

    # Currency flows
    st.markdown("### CURRENCY INTELLIGENCE")
    col1, col2, col3 = st.columns(3)
    for col, (pair, rate, change, status) in zip(
        [col1, col2, col3],
        [("EUR/USD", "1.0892", "-0.8%", StatusLevel.NEGATIVE),
         ("GBP/USD", "1.2734", "-1.2%", StatusLevel.NEGATIVE),
         ("USD/JPY", "148.25", "+2.1%", StatusLevel.POSITIVE)]
    ):
        with col:
            st.markdown(f"**{pair}**")
            st.markdown(f"<span class='data-lg'>{rate}</span>", unsafe_allow_html=True)
            st.markdown(f"<span class='{status.value}'>{change}</span>", unsafe_allow_html=True)

    divider_section()

    # Commodity map
    st.markdown("### COMMODITY INTELLIGENCE")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### Energy")
        for name, price, change, status in [("WTI Crude", "$82.45", "-1.2%", StatusLevel.NEGATIVE), ("Brent", "$87.23", "-0.8%", StatusLevel.NEGATIVE), ("Natural Gas", "$2.84", "+3.2%", StatusLevel.POSITIVE)]:
            c1, c2, c3 = st.columns([1.5, 1, 1])
            with c1:
                st.markdown(f"**{name}**")
            with c2:
                st.markdown(price)
            with c3:
                st.markdown(f"<span class='{status.value}'>{change}</span>", unsafe_allow_html=True)
            st.divider()
    with col2:
        st.markdown("#### Metals")
        for name, price, change, status in [("Gold", "$2,087.50", "+0.8%", StatusLevel.POSITIVE), ("Silver", "$24.67", "+1.2%", StatusLevel.POSITIVE), ("Copper", "$4.28", "-0.5%", StatusLevel.NEGATIVE)]:
            c1, c2, c3 = st.columns([1.5, 1, 1])
            with c1:
                st.markdown(f"**{name}**")
            with c2:
                st.markdown(price)
            with c3:
                st.markdown(f"<span class='{status.value}'>{change}</span>", unsafe_allow_html=True)
            st.divider()
    with col3:
        st.markdown("#### Agriculture")
        for name, price, change, status in [("Wheat", "$586.75", "+2.1%", StatusLevel.POSITIVE), ("Corn", "$456.25", "-1.8%", StatusLevel.NEGATIVE), ("Soybeans", "$1,234.50", "+0.9%", StatusLevel.POSITIVE)]:
            c1, c2, c3 = st.columns([1.5, 1, 1])
            with c1:
                st.markdown(f"**{name}**")
            with c2:
                st.markdown(price)
            with c3:
                st.markdown(f"<span class='{status.value}'>{change}</span>", unsafe_allow_html=True)
            st.divider()

    divider_section()

    # Supply chain
    st.markdown("### SUPPLY CHAIN HEALTH")
    col1, col2, col3 = st.columns(3)
    with col1:
        data_card("SHIPPING RATES", [
            DataPoint("$1,847.50", "Shanghai-Rotterdam", StatusLevel.NEUTRAL),
            DataPoint("↑ 2.3%",   "Weekly Change",       StatusLevel.NEUTRAL),
            DataPoint("34 days",  "Transit Time",         StatusLevel.NEUTRAL),
        ])
    with col2:
        data_card("PORT CONGESTION", [
            DataPoint("2.1 days", "Singapore", StatusLevel.POSITIVE),
            DataPoint("3.4 days", "Rotterdam", StatusLevel.NEUTRAL),
            DataPoint("1.8 days", "Shanghai",  StatusLevel.POSITIVE),
        ])
    with col3:
        data_card("FREIGHT INDEX", [
            DataPoint("1,234.5",       "Current Level",    StatusLevel.NEUTRAL),
            DataPoint("-4.2%",         "30-Day Change",    StatusLevel.POSITIVE),
            DataPoint("Avg: 1,456.8",  "Historical",       StatusLevel.NEUTRAL),
        ])

    divider_section()

    # Trade flows
    st.markdown("### MAJOR TRADE FLOWS")
    flows = [
        ("USA → Asia",            "$2.3T annually", "↑ +8.4% YoY", StatusLevel.POSITIVE, "Electronics, Machinery"),
        ("Europe → USA",          "$890B annually", "→ +1.2% YoY", StatusLevel.NEUTRAL,  "Chemicals, Automotive"),
        ("Asia → Europe",         "$1.2T annually", "↑ +5.1% YoY", StatusLevel.POSITIVE, "Electronics, Textiles"),
        ("Emerging → Developed",  "$3.8T annually", "↑ +3.8% YoY", StatusLevel.POSITIVE, "Raw Materials, Energy"),
    ]
    for route, volume, trend, status, goods in flows:
        c1, c2, c3, c4 = st.columns([1.8, 1.5, 1, 2])
        with c1:
            st.markdown(f"**{route}**")
            st.caption(f"Volume: {volume}")
        with c2:
            st.markdown(f"<span class='{status.value}'>{trend}</span>", unsafe_allow_html=True)
        with c3:
            st.button("Details", key=f"flow_{route}")
        with c4:
            st.caption(f"Goods: {goods}")
        st.divider()
