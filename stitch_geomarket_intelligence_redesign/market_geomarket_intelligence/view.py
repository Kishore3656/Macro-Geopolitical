"""
Market Analysis - Deep-dive equity analysis and strategic positioning
"""

import streamlit as st
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components import (
    data_card, metric_box, live_indicator,
    status_badge, divider_section, stat_comparison,
    data_table_tactical, alert_box, hero_stat, section_divider,
    StatusLevel, DataPoint, activity_timeline
)


def render_market_header():
    """Market analysis command center"""
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.markdown("## MARKET INTELLIGENCE", unsafe_allow_html=True)
        st.caption("Deep Equity Analysis & Strategic Positioning")

    with col2:
        live_indicator("MARKET FEED")

    with col3:
        current_time = datetime.now().strftime("%H:%M:%S")
        st.markdown(f'<div class="data-md">{current_time}</div>', unsafe_allow_html=True)

    st.divider()


def render_market_overview():
    """Key market metrics"""
    st.markdown("### MARKET OVERVIEW", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    metrics = [
        ("S&P 500", "8,247", "+2.3%", StatusLevel.POSITIVE),
        ("NASDAQ", "16,542", "+4.1%", StatusLevel.POSITIVE),
        ("DOW 30", "42,156", "+1.8%", StatusLevel.POSITIVE),
        ("VIX", "12.8", "-8.2%", StatusLevel.POSITIVE),
    ]

    columns = [col1, col2, col3, col4]

    for col, (label, value, change, status) in zip(columns, metrics):
        with col:
            hero_stat(value, label, accent=(status == StatusLevel.POSITIVE))
            st.markdown(
                f"<span class='{status.value}'>{change}</span>",
                unsafe_allow_html=True
            )


def render_sector_rankings():
    """All sectors ranked by performance"""
    st.markdown("### SECTOR PERFORMANCE RANKINGS", unsafe_allow_html=True)

    sectors = [
        {"rank": 1, "name": "Technology", "return": "+8.24%", "status": StatusLevel.POSITIVE, "weight": "28%", "momentum": "STRONG"},
        {"rank": 2, "name": "Healthcare", "return": "+4.10%", "status": StatusLevel.POSITIVE, "weight": "13%", "momentum": "SOLID"},
        {"rank": 3, "name": "Financials", "return": "+2.85%", "status": StatusLevel.POSITIVE, "weight": "14%", "momentum": "NEUTRAL"},
        {"rank": 4, "name": "Consumer Disc", "return": "+1.92%", "status": StatusLevel.POSITIVE, "weight": "10%", "momentum": "WEAK"},
        {"rank": 5, "name": "Industrials", "return": "+1.23%", "status": StatusLevel.POSITIVE, "weight": "9%", "momentum": "WEAK"},
        {"rank": 6, "name": "Utilities", "return": "+0.84%", "status": StatusLevel.POSITIVE, "weight": "3%", "momentum": "FLAT"},
        {"rank": 7, "name": "Materials", "return": "-1.02%", "status": StatusLevel.NEGATIVE, "weight": "5%", "momentum": "DECLINING"},
        {"rank": 8, "name": "Energy", "return": "-2.34%", "status": StatusLevel.NEGATIVE, "weight": "4%", "momentum": "DETERIORATING"},
        {"rank": 9, "name": "Consumer Staples", "return": "-0.92%", "status": StatusLevel.NEGATIVE, "weight": "7%", "momentum": "WEAK"},
        {"rank": 10, "name": "Real Estate", "return": "-3.15%", "status": StatusLevel.NEGATIVE, "weight": "3%", "momentum": "DECLINING"},
    ]

    for sector in sectors:
        col1, col2, col3, col4, col5, col6 = st.columns([0.5, 2, 1.5, 1.5, 1, 1.5])

        with col1:
            st.markdown(f"<span class='label-md'>{sector['rank']}</span>", unsafe_allow_html=True)

        with col2:
            st.markdown(f"**{sector['name']}**")

        with col3:
            st.markdown(
                f"<span class='{sector['status'].value} data-md'>{sector['return']}</span>",
                unsafe_allow_html=True
            )

        with col4:
            st.caption(f"Index wgt: {sector['weight']}")

        with col5:
            momentum_status = StatusLevel.POSITIVE if "STRONG" in sector['momentum'] or "SOLID" in sector['momentum'] else StatusLevel.NEGATIVE if "DECLINING" in sector['momentum'] or "DETERIORATING" in sector['momentum'] else StatusLevel.NEUTRAL
            st.markdown(
                f"<span class='{momentum_status.value} data-sm'>{sector['momentum']}</span>",
                unsafe_allow_html=True
            )

        with col6:
            st.button("View", key=f"sector_{sector['name']}", use_container_width=True)

        st.divider()


def render_top_gainers_losers():
    """Individual stock movers"""
    st.markdown("### MARKET MOVERS", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Top Gainers")
        gainers = [
            {"symbol": "NVDA", "name": "NVIDIA", "price": "892.34", "change": "+12.8%", "volume": "52.3M"},
            {"symbol": "MSFT", "name": "Microsoft", "price": "423.18", "change": "+8.2%", "volume": "28.1M"},
            {"symbol": "TSLA", "name": "Tesla", "price": "178.92", "change": "+6.5%", "volume": "94.2M"},
            {"symbol": "META", "name": "Meta", "price": "487.65", "change": "+5.3%", "volume": "18.7M"},
            {"symbol": "AMZN", "name": "Amazon", "price": "184.23", "change": "+4.1%", "volume": "32.4M"},
        ]

        for stock in gainers:
            col_a, col_b, col_c, col_d = st.columns([1, 1.5, 1.2, 1])
            with col_a:
                st.markdown(f"<span class='label-md'>{stock['symbol']}</span>", unsafe_allow_html=True)
            with col_b:
                st.caption(stock['name'])
            with col_c:
                st.markdown(
                    f"<span class='text-positive data-md'>{stock['change']}</span>",
                    unsafe_allow_html=True
                )
            with col_d:
                st.caption(f"Vol: {stock['volume']}")
            st.divider()

    with col2:
        st.markdown("#### Top Losers")
        losers = [
            {"symbol": "XLE", "name": "Energy ETF", "price": "72.15", "change": "-4.2%", "volume": "8.2M"},
            {"symbol": "URA", "name": "Uranium ETF", "price": "28.34", "change": "-3.8%", "volume": "5.1M"},
            {"symbol": "IYR", "name": "Real Estate ETF", "price": "64.92", "change": "-3.1%", "volume": "4.3M"},
            {"symbol": "BDX", "name": "Becton Dickinson", "price": "241.82", "change": "-2.9%", "volume": "1.2M"},
            {"symbol": "GD", "name": "General Dynamics", "price": "278.45", "change": "-2.3%", "volume": "0.8M"},
        ]

        for stock in losers:
            col_a, col_b, col_c, col_d = st.columns([1, 1.5, 1.2, 1])
            with col_a:
                st.markdown(f"<span class='label-md'>{stock['symbol']}</span>", unsafe_allow_html=True)
            with col_b:
                st.caption(stock['name'])
            with col_c:
                st.markdown(
                    f"<span class='text-negative data-md'>{stock['change']}</span>",
                    unsafe_allow_html=True
                )
            with col_d:
                st.caption(f"Vol: {stock['volume']}")
            st.divider()


def render_earnings_calendar():
    """Upcoming earnings events"""
    st.markdown("### EARNINGS INTELLIGENCE", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("#### This Week")
        earnings = [
            {"date": "Today", "company": "NVIDIA", "time": "Post-Market", "est_eps": "0.64", "last_eps": "0.58"},
            {"date": "Tomorrow", "company": "Meta", "time": "Post-Market", "est_eps": "4.85", "last_eps": "4.12"},
            {"date": "Wed", "company": "Tesla", "time": "Post-Market", "est_eps": "0.72", "last_eps": "0.68"},
            {"date": "Thu", "company": "Microsoft", "time": "Post-Market", "est_eps": "2.94", "last_eps": "2.45"},
        ]

        for earning in earnings:
            col_a, col_b, col_c = st.columns([1.5, 2, 1.5])
            with col_a:
                st.markdown(f"**{earning['company']}**")
            with col_b:
                st.caption(f"EPS Est: {earning['est_eps']} vs {earning['last_eps']}")
            with col_c:
                st.caption(earning['time'])
            st.divider()

    with col2:
        st.markdown("#### Market Impact Analysis")
        impact_alert = alert_box(
            "📊 Earnings season in full swing. Tech earnings likely to drive market direction. Watch for guidance changes and margin pressures.",
            StatusLevel.PRIMARY
        )


def render_valuation_metrics():
    """Broad market valuation"""
    st.markdown("### VALUATION METRICS", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    metrics = [
        ("S&P 500 P/E", "22.3x", "Elevated", StatusLevel.NEUTRAL),
        ("Forward P/E", "19.8x", "Fair", StatusLevel.POSITIVE),
        ("Dividend Yield", "1.68%", "Rising", StatusLevel.POSITIVE),
        ("PEG Ratio", "1.42x", "Fair", StatusLevel.NEUTRAL),
    ]

    for col, (label, value, desc, status) in zip([col1, col2, col3, col4], metrics):
        with col:
            st.markdown(f"<span class='label-md'>{label}</span>", unsafe_allow_html=True)
            st.markdown(f"<span class='data-lg {status.value}'>{value}</span>", unsafe_allow_html=True)
            st.caption(desc)


def render_market_breadth():
    """Advance/decline analysis"""
    st.markdown("### MARKET BREADTH", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        data_card(
            "NYSE BREADTH",
            [
                DataPoint("2,847", "Advancing", StatusLevel.POSITIVE),
                DataPoint("892", "Declining", StatusLevel.NEGATIVE),
                DataPoint("3.2:1", "Ratio", StatusLevel.POSITIVE),
            ]
        )

    with col2:
        data_card(
            "NASDAQ BREADTH",
            [
                DataPoint("4,128", "Advancing", StatusLevel.POSITIVE),
                DataPoint("1,245", "Declining", StatusLevel.NEGATIVE),
                DataPoint("3.3:1", "Ratio", StatusLevel.POSITIVE),
            ]
        )

    with col3:
        data_card(
            "S&P 500 BREADTH",
            [
                DataPoint("438", "Above 50-DMA", StatusLevel.POSITIVE),
                DataPoint("62", "Below 50-DMA", StatusLevel.NEGATIVE),
                DataPoint("87.6%", "Bullish %", StatusLevel.POSITIVE),
            ]
        )


def render_technical_analysis():
    """Market technical signals"""
    st.markdown("### TECHNICAL ANALYSIS SIGNALS", unsafe_allow_html=True)

    signals = [
        {"name": "50-Day Moving Average", "status": StatusLevel.POSITIVE, "signal": "Price above - Bullish"},
        {"name": "200-Day Moving Average", "status": StatusLevel.POSITIVE, "signal": "Price above - Strong Uptrend"},
        {"name": "RSI (14)", "status": StatusLevel.NEUTRAL, "signal": "55.2 - Neither Overbought nor Oversold"},
        {"name": "MACD", "status": StatusLevel.POSITIVE, "signal": "Positive Histogram - Bullish Momentum"},
        {"name": "Bollinger Bands", "status": StatusLevel.NEUTRAL, "signal": "Mid-band - Consolidating"},
    ]

    for signal in signals:
        col1, col2, col3 = st.columns([2, 1.5, 2])
        with col1:
            st.markdown(f"**{signal['name']}**")
        with col2:
            st.markdown(
                f"<span class='{signal['status'].value} label-md'>●</span>",
                unsafe_allow_html=True
            )
        with col3:
            st.caption(signal['signal'])
        st.divider()


def render():
    """Main market view"""
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "styles.css")) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    render_market_header()
    render_market_overview()
    divider_section()

    render_sector_rankings()
    divider_section()

    render_top_gainers_losers()
    divider_section()

    render_earnings_calendar()
    divider_section()

    render_valuation_metrics()
    divider_section()

    render_market_breadth()
    divider_section()

    render_technical_analysis()


if __name__ == "__main__":
    st.set_page_config(
        page_title="Market Intelligence | Equity Analysis",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    render()
