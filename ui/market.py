"""Market Intelligence - Deep equity analysis and strategic positioning"""

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
        st.markdown("## MARKET INTELLIGENCE")
        st.caption("Deep Equity Analysis & Strategic Positioning")
    with col2:
        live_indicator("MARKET FEED")
    with col3:
        st.markdown(f'<div class="data-md">{datetime.now().strftime("%H:%M:%S")}</div>', unsafe_allow_html=True)
    st.divider()

    # Market overview
    st.markdown("### MARKET OVERVIEW")
    col1, col2, col3, col4 = st.columns(4)
    for col, (label, value, change, status) in zip(
        [col1, col2, col3, col4],
        [("S&P 500", "8,247", "+2.3%", StatusLevel.POSITIVE),
         ("NASDAQ",  "16,542", "+4.1%", StatusLevel.POSITIVE),
         ("DOW 30",  "42,156", "+1.8%", StatusLevel.POSITIVE),
         ("VIX",     "12.8",  "-8.2%", StatusLevel.POSITIVE)]
    ):
        with col:
            hero_stat(value, label, accent=True)
            st.markdown(f"<span class='{status.value}'>{change}</span>", unsafe_allow_html=True)

    divider_section()

    # Sector rankings
    st.markdown("### SECTOR PERFORMANCE RANKINGS")
    sectors = [
        (1,  "Technology",       "+8.24%", StatusLevel.POSITIVE, "28%", "STRONG"),
        (2,  "Healthcare",       "+4.10%", StatusLevel.POSITIVE, "13%", "SOLID"),
        (3,  "Financials",       "+2.85%", StatusLevel.POSITIVE, "14%", "NEUTRAL"),
        (4,  "Consumer Disc",    "+1.92%", StatusLevel.POSITIVE, "10%", "WEAK"),
        (5,  "Industrials",      "+1.23%", StatusLevel.POSITIVE, "9%",  "WEAK"),
        (6,  "Utilities",        "+0.84%", StatusLevel.POSITIVE, "3%",  "FLAT"),
        (7,  "Materials",        "-1.02%", StatusLevel.NEGATIVE, "5%",  "DECLINING"),
        (8,  "Energy",           "-2.34%", StatusLevel.NEGATIVE, "4%",  "DETERIORATING"),
        (9,  "Consumer Staples", "-0.92%", StatusLevel.NEGATIVE, "7%",  "WEAK"),
        (10, "Real Estate",      "-3.15%", StatusLevel.NEGATIVE, "3%",  "DECLINING"),
    ]
    for rank, name, ret, status, weight, momentum in sectors:
        c1, c2, c3, c4, c5, c6 = st.columns([0.5, 2, 1.5, 1.5, 1, 1.5])
        with c1:
            st.markdown(f"<span class='label-md'>{rank}</span>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"**{name}**")
        with c3:
            st.markdown(f"<span class='{status.value} data-md'>{ret}</span>", unsafe_allow_html=True)
        with c4:
            st.caption(f"Index wgt: {weight}")
        with c5:
            mom_status = StatusLevel.POSITIVE if momentum in ("STRONG", "SOLID") else StatusLevel.NEGATIVE if momentum in ("DECLINING", "DETERIORATING") else StatusLevel.NEUTRAL
            st.markdown(f"<span class='{mom_status.value} data-sm'>{momentum}</span>", unsafe_allow_html=True)
        with c6:
            st.button("View", key=f"sector_{name}", use_container_width=True)
        st.divider()

    divider_section()

    # Market movers
    st.markdown("### MARKET MOVERS")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Top Gainers")
        for sym, name, change in [("NVDA", "NVIDIA", "+12.8%"), ("MSFT", "Microsoft", "+8.2%"), ("TSLA", "Tesla", "+6.5%"), ("META", "Meta", "+5.3%"), ("AMZN", "Amazon", "+4.1%")]:
            c1, c2, c3 = st.columns([1, 2, 1.2])
            with c1:
                st.markdown(f"<span class='label-md'>{sym}</span>", unsafe_allow_html=True)
            with c2:
                st.caption(name)
            with c3:
                st.markdown(f"<span class='text-positive data-md'>{change}</span>", unsafe_allow_html=True)
            st.divider()
    with col2:
        st.markdown("#### Top Losers")
        for sym, name, change in [("XLE", "Energy ETF", "-4.2%"), ("URA", "Uranium ETF", "-3.8%"), ("IYR", "Real Estate ETF", "-3.1%"), ("BDX", "Becton Dickinson", "-2.9%"), ("GD", "General Dynamics", "-2.3%")]:
            c1, c2, c3 = st.columns([1, 2, 1.2])
            with c1:
                st.markdown(f"<span class='label-md'>{sym}</span>", unsafe_allow_html=True)
            with c2:
                st.caption(name)
            with c3:
                st.markdown(f"<span class='text-negative data-md'>{change}</span>", unsafe_allow_html=True)
            st.divider()

    divider_section()

    # Earnings calendar
    st.markdown("### EARNINGS INTELLIGENCE")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### This Week")
        for date, company, time, est, last in [("Today", "NVIDIA", "Post-Market", "0.64", "0.58"), ("Tomorrow", "Meta", "Post-Market", "4.85", "4.12"), ("Wed", "Tesla", "Post-Market", "0.72", "0.68"), ("Thu", "Microsoft", "Post-Market", "2.94", "2.45")]:
            c1, c2, c3 = st.columns([1.5, 2, 1.5])
            with c1:
                st.markdown(f"**{company}**")
            with c2:
                st.caption(f"EPS Est: {est} vs {last}")
            with c3:
                st.caption(time)
            st.divider()
    with col2:
        st.markdown("#### Market Impact Analysis")
        alert_box("Earnings season in full swing. Tech earnings likely to drive market direction. Watch for guidance changes and margin pressures.", StatusLevel.PRIMARY)

    divider_section()

    # Valuation metrics
    st.markdown("### VALUATION METRICS")
    col1, col2, col3, col4 = st.columns(4)
    for col, (label, value, desc, status) in zip(
        [col1, col2, col3, col4],
        [("S&P 500 P/E",    "22.3x", "Elevated", StatusLevel.NEUTRAL),
         ("Forward P/E",    "19.8x", "Fair",      StatusLevel.POSITIVE),
         ("Dividend Yield", "1.68%", "Rising",    StatusLevel.POSITIVE),
         ("PEG Ratio",      "1.42x", "Fair",      StatusLevel.NEUTRAL)]
    ):
        with col:
            st.markdown(f"<span class='label-md'>{label}</span>", unsafe_allow_html=True)
            st.markdown(f"<span class='data-lg {status.value}'>{value}</span>", unsafe_allow_html=True)
            st.caption(desc)

    divider_section()

    # Market breadth
    st.markdown("### MARKET BREADTH")
    col1, col2, col3 = st.columns(3)
    with col1:
        data_card("NYSE BREADTH", [
            DataPoint("2,847", "Advancing", StatusLevel.POSITIVE),
            DataPoint("892",   "Declining", StatusLevel.NEGATIVE),
            DataPoint("3.2:1", "Ratio",     StatusLevel.POSITIVE),
        ])
    with col2:
        data_card("NASDAQ BREADTH", [
            DataPoint("4,128", "Advancing", StatusLevel.POSITIVE),
            DataPoint("1,245", "Declining", StatusLevel.NEGATIVE),
            DataPoint("3.3:1", "Ratio",     StatusLevel.POSITIVE),
        ])
    with col3:
        data_card("S&P 500 BREADTH", [
            DataPoint("438",   "Above 50-DMA", StatusLevel.POSITIVE),
            DataPoint("62",    "Below 50-DMA", StatusLevel.NEGATIVE),
            DataPoint("87.6%", "Bullish %",    StatusLevel.POSITIVE),
        ])

    divider_section()

    # Technical signals
    st.markdown("### TECHNICAL ANALYSIS SIGNALS")
    signals = [
        ("50-Day Moving Average",  StatusLevel.POSITIVE, "Price above — Bullish"),
        ("200-Day Moving Average", StatusLevel.POSITIVE, "Price above — Strong Uptrend"),
        ("RSI (14)",               StatusLevel.NEUTRAL,  "55.2 — Neither Overbought nor Oversold"),
        ("MACD",                   StatusLevel.POSITIVE, "Positive Histogram — Bullish Momentum"),
        ("Bollinger Bands",        StatusLevel.NEUTRAL,  "Mid-band — Consolidating"),
    ]
    for name, status, signal in signals:
        c1, c2, c3 = st.columns([2, 1.5, 2])
        with c1:
            st.markdown(f"**{name}**")
        with c2:
            st.markdown(f"<span class='{status.value} label-md'>●</span>", unsafe_allow_html=True)
        with c3:
            st.caption(signal)
        st.divider()
