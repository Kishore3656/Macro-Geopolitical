"""
Geo Map - Interactive geographic market intelligence
"""

import streamlit as st
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components import (
    data_card, live_indicator, status_badge,
    divider_section, hero_stat, section_divider,
    StatusLevel, DataPoint
)


def render_geomap_header():
    """Geographic intelligence command center"""
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.markdown("## GEO MAP", unsafe_allow_html=True)
        st.caption("Interactive Geographic Market Intelligence")

    with col2:
        live_indicator("MAP DATA LIVE")

    with col3:
        current_time = datetime.now().strftime("%H:%M:%S")
        st.markdown(f'<div class="data-md">{current_time}</div>', unsafe_allow_html=True)

    st.divider()


def render_regional_breakdown():
    """Market performance by region"""
    st.markdown("### REGIONAL MARKET PERFORMANCE", unsafe_allow_html=True)

    regions = [
        {
            "region": "North America",
            "index": "S&P 500",
            "value": "8,247.32",
            "change": "+2.3%",
            "status": StatusLevel.POSITIVE,
            "companies": "2,847",
            "tradable_volume": "$2.1T"
        },
        {
            "region": "Europe",
            "index": "STOXX 600",
            "value": "487.24",
            "change": "+1.2%",
            "status": StatusLevel.POSITIVE,
            "companies": "600",
            "tradable_volume": "$890B"
        },
        {
            "region": "Asia-Pacific",
            "index": "MSCI APJ",
            "value": "3,456.78",
            "change": "+3.4%",
            "status": StatusLevel.POSITIVE,
            "companies": "1,230",
            "tradable_volume": "$5.2T"
        },
        {
            "region": "Emerging Markets",
            "index": "MSCI EM",
            "value": "1,087.34",
            "change": "+1.8%",
            "status": StatusLevel.POSITIVE,
            "companies": "789",
            "tradable_volume": "$1.1T"
        },
    ]

    for region in regions:
        col1, col2, col3, col4, col5 = st.columns([1.5, 1.5, 1, 1.5, 1.5])

        with col1:
            st.markdown(f"**{region['region']}**")
            st.caption(region['index'])

        with col2:
            st.markdown(f"<span class='data-lg'>{region['value']}</span>", unsafe_allow_html=True)

        with col3:
            st.markdown(
                f"<span class='{region['status'].value}'>{region['change']}</span>",
                unsafe_allow_html=True
            )

        with col4:
            st.caption(f"Companies: {region['companies']}")

        with col5:
            st.caption(f"Volume: {region['tradable_volume']}")

        st.divider()


def render_country_heatmap():
    """Individual country performance"""
    st.markdown("### COUNTRY PERFORMANCE HEATMAP", unsafe_allow_html=True)

    countries = [
        {"flag": "🇺🇸", "country": "USA", "return": "+2.8%", "status": StatusLevel.POSITIVE, "market_cap": "$48.2T"},
        {"flag": "🇯🇵", "country": "Japan", "return": "+3.2%", "status": StatusLevel.POSITIVE, "market_cap": "$5.1T"},
        {"flag": "🇬🇧", "country": "UK", "return": "+1.1%", "status": StatusLevel.POSITIVE, "market_cap": "$3.4T"},
        {"flag": "🇩🇪", "country": "Germany", "return": "+0.9%", "status": StatusLevel.POSITIVE, "market_cap": "$2.8T"},
        {"flag": "🇫🇷", "country": "France", "return": "+1.2%", "status": StatusLevel.POSITIVE, "market_cap": "$2.5T"},
        {"flag": "🇨🇭", "country": "Switzerland", "return": "+0.7%", "status": StatusLevel.POSITIVE, "market_cap": "$1.9T"},
        {"flag": "🇮🇳", "country": "India", "return": "+4.2%", "status": StatusLevel.POSITIVE, "market_cap": "$4.2T"},
        {"flag": "🇨🇳", "country": "China", "return": "-0.8%", "status": StatusLevel.NEGATIVE, "market_cap": "$9.8T"},
        {"flag": "🇦🇺", "country": "Australia", "return": "+1.4%", "status": StatusLevel.POSITIVE, "market_cap": "$1.8T"},
        {"flag": "🇧🇷", "country": "Brazil", "return": "+2.1%", "status": StatusLevel.POSITIVE, "market_cap": "$0.9T"},
        {"flag": "🇨🇦", "country": "Canada", "return": "+1.8%", "status": StatusLevel.POSITIVE, "market_cap": "$2.3T"},
        {"flag": "🇰🇷", "country": "South Korea", "return": "+2.9%", "status": StatusLevel.POSITIVE, "market_cap": "$1.8T"},
    ]

    cols = st.columns(4)

    for idx, country in enumerate(countries):
        with cols[idx % 4]:
            with st.container():
                col_a, col_b = st.columns([1, 1.5])
                with col_a:
                    st.markdown(f"<span style='font-size: 1.5rem;'>{country['flag']}</span>", unsafe_allow_html=True)
                with col_b:
                    st.markdown(f"**{country['country']}**")

                st.markdown(
                    f"<span class='{country['status'].value} data-md'>{country['return']}</span>",
                    unsafe_allow_html=True
                )
                st.caption(f"MCap: {country['market_cap']}")
                st.divider()


def render_currency_flows():
    """Currency strength and flows"""
    st.markdown("### CURRENCY INTELLIGENCE", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    currencies = [
        {"pair": "EUR/USD", "rate": "1.0892", "change": "-0.8%", "status": StatusLevel.NEGATIVE},
        {"pair": "GBP/USD", "rate": "1.2734", "change": "-1.2%", "status": StatusLevel.NEGATIVE},
        {"pair": "USD/JPY", "rate": "148.25", "change": "+2.1%", "status": StatusLevel.POSITIVE},
    ]

    with col1:
        for curr in currencies[:1]:
            st.markdown(f"**{curr['pair']}**")
            st.markdown(f"<span class='data-lg'>{curr['rate']}</span>", unsafe_allow_html=True)
            st.markdown(
                f"<span class='{curr['status'].value}'>{curr['change']}</span>",
                unsafe_allow_html=True
            )

    with col2:
        for curr in currencies[1:2]:
            st.markdown(f"**{curr['pair']}**")
            st.markdown(f"<span class='data-lg'>{curr['rate']}</span>", unsafe_allow_html=True)
            st.markdown(
                f"<span class='{curr['status'].value}'>{curr['change']}</span>",
                unsafe_allow_html=True
            )

    with col3:
        for curr in currencies[2:]:
            st.markdown(f"**{curr['pair']}**")
            st.markdown(f"<span class='data-lg'>{curr['rate']}</span>", unsafe_allow_html=True)
            st.markdown(
                f"<span class='{curr['status'].value}'>{curr['change']}</span>",
                unsafe_allow_html=True
            )


def render_commodity_map():
    """Global commodity pricing"""
    st.markdown("### COMMODITY INTELLIGENCE", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### Energy")
        energy = [
            {"commodity": "WTI Crude", "price": "$82.45", "change": "-1.2%", "status": StatusLevel.NEGATIVE},
            {"commodity": "Brent", "price": "$87.23", "change": "-0.8%", "status": StatusLevel.NEGATIVE},
            {"commodity": "Natural Gas", "price": "$2.84", "change": "+3.2%", "status": StatusLevel.POSITIVE},
        ]

        for item in energy:
            col_a, col_b, col_c = st.columns([1.5, 1, 1])
            with col_a:
                st.markdown(f"**{item['commodity']}**")
            with col_b:
                st.markdown(f"{item['price']}")
            with col_c:
                st.markdown(
                    f"<span class='{item['status'].value}'>{item['change']}</span>",
                    unsafe_allow_html=True
                )
            st.divider()

    with col2:
        st.markdown("#### Metals")
        metals = [
            {"commodity": "Gold", "price": "$2,087.50", "change": "+0.8%", "status": StatusLevel.POSITIVE},
            {"commodity": "Silver", "price": "$24.67", "change": "+1.2%", "status": StatusLevel.POSITIVE},
            {"commodity": "Copper", "price": "$4.28", "change": "-0.5%", "status": StatusLevel.NEGATIVE},
        ]

        for item in metals:
            col_a, col_b, col_c = st.columns([1.5, 1, 1])
            with col_a:
                st.markdown(f"**{item['commodity']}**")
            with col_b:
                st.markdown(f"{item['price']}")
            with col_c:
                st.markdown(
                    f"<span class='{item['status'].value}'>{item['change']}</span>",
                    unsafe_allow_html=True
                )
            st.divider()

    with col3:
        st.markdown("#### Agriculture")
        agri = [
            {"commodity": "Wheat", "price": "$586.75", "change": "+2.1%", "status": StatusLevel.POSITIVE},
            {"commodity": "Corn", "price": "$456.25", "change": "-1.8%", "status": StatusLevel.NEGATIVE},
            {"commodity": "Soybeans", "price": "$1,234.50", "change": "+0.9%", "status": StatusLevel.POSITIVE},
        ]

        for item in agri:
            col_a, col_b, col_c = st.columns([1.5, 1, 1])
            with col_a:
                st.markdown(f"**{item['commodity']}**")
            with col_b:
                st.markdown(f"{item['price']}")
            with col_c:
                st.markdown(
                    f"<span class='{item['status'].value}'>{item['change']}</span>",
                    unsafe_allow_html=True
                )
            st.divider()


def render_supply_chain():
    """Global supply chain indicators"""
    st.markdown("### SUPPLY CHAIN HEALTH", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        data_card(
            "SHIPPING RATES",
            [
                DataPoint("$1,847.50", "Shanghai-Rotterdam", StatusLevel.NEUTRAL),
                DataPoint("↑ 2.3%", "Weekly Change", StatusLevel.NEUTRAL),
                DataPoint("34 days", "Transit Time", StatusLevel.NEUTRAL),
            ]
        )

    with col2:
        data_card(
            "PORT CONGESTION",
            [
                DataPoint("2.1 days", "Singapore", StatusLevel.POSITIVE),
                DataPoint("3.4 days", "Rotterdam", StatusLevel.NEUTRAL),
                DataPoint("1.8 days", "Shanghai", StatusLevel.POSITIVE),
            ]
        )

    with col3:
        data_card(
            "FREIGHT INDEX",
            [
                DataPoint("1,234.5", "Current Level", StatusLevel.NEUTRAL),
                DataPoint("-4.2%", "30-Day Change", StatusLevel.POSITIVE),
                DataPoint("Historical Avg", "1,456.8", StatusLevel.NEUTRAL),
            ]
        )


def render_trade_flows():
    """International trade patterns"""
    st.markdown("### MAJOR TRADE FLOWS", unsafe_allow_html=True)

    flows = [
        {
            "route": "USA → Asia",
            "volume": "$2.3T annually",
            "trend": "↑ +8.4% YoY",
            "status": StatusLevel.POSITIVE,
            "key_goods": "Electronics, Machinery"
        },
        {
            "route": "Europe → USA",
            "volume": "$890B annually",
            "trend": "→ +1.2% YoY",
            "status": StatusLevel.NEUTRAL,
            "key_goods": "Chemicals, Automotive"
        },
        {
            "route": "Asia → Europe",
            "volume": "$1.2T annually",
            "trend": "↑ +5.1% YoY",
            "status": StatusLevel.POSITIVE,
            "key_goods": "Electronics, Textiles"
        },
        {
            "route": "Emerging → Developed",
            "volume": "$3.8T annually",
            "trend": "↑ +3.8% YoY",
            "status": StatusLevel.POSITIVE,
            "key_goods": "Raw Materials, Energy"
        },
    ]

    for flow in flows:
        col1, col2, col3, col4 = st.columns([1.8, 1.5, 1, 2])

        with col1:
            st.markdown(f"**{flow['route']}**")
            st.caption(f"Volume: {flow['volume']}")

        with col2:
            st.markdown(
                f"<span class='{flow['status'].value}'>{flow['trend']}</span>",
                unsafe_allow_html=True
            )

        with col3:
            st.button("Details", key=f"flow_{flow['route']}")

        with col4:
            st.caption(f"Goods: {flow['key_goods']}")

        st.divider()


def render():
    """Main Geo Map view"""
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "styles.css")) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    render_geomap_header()
    render_regional_breakdown()
    divider_section()

    render_country_heatmap()
    divider_section()

    render_currency_flows()
    divider_section()

    render_commodity_map()
    divider_section()

    render_supply_chain()
    divider_section()

    render_trade_flows()


if __name__ == "__main__":
    st.set_page_config(
        page_title="Geo Map | Geographic Intelligence",
        page_icon="🌐",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    render()
