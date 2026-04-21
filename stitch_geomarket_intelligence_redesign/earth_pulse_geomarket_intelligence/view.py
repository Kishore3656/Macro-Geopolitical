"""
Earth Pulse - Geospatial market analysis and global intelligence
"""

import streamlit as st
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components import (
    data_card, metric_box, live_indicator, panel_header,
    status_badge, divider_section, stat_comparison,
    data_grid, alert_box, hero_stat, section_divider,
    StatusLevel, DataPoint
)


def render_earth_pulse_header():
    """Geospatial intelligence command center"""
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.markdown("## EARTH PULSE", unsafe_allow_html=True)
        st.caption("Global Market Movement & Geospatial Intelligence")

    with col2:
        live_indicator("SATELLITE FEED")

    with col3:
        current_time = datetime.now().strftime("%H:%M:%S")
        st.markdown(f'<div class="data-md">{current_time}</div>', unsafe_allow_html=True)

    st.divider()


def render_global_heatmap():
    """Visual market heat distribution by region"""
    st.markdown("### GLOBAL MARKET HEATMAP", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    regions = [
        {"name": "Asia-Pacific", "value": "+4.2%", "status": StatusLevel.POSITIVE, "markets": "12"},
        {"name": "Europe", "value": "+1.8%", "status": StatusLevel.POSITIVE, "markets": "8"},
        {"name": "Americas", "value": "+2.9%", "status": StatusLevel.POSITIVE, "markets": "15"},
    ]

    for col, region in zip([col1, col2, col3], regions):
        with col:
            with st.container():
                st.markdown(f"**{region['name']}**")
                st.markdown(
                    f"<p class='data-lg {region['status'].value}'>{region['value']}</p>",
                    unsafe_allow_html=True
                )
                st.caption(f"{region['markets']} active markets")


def render_major_exchanges():
    """Exchange-by-exchange performance"""
    st.markdown("### MAJOR EXCHANGE PULSE", unsafe_allow_html=True)

    exchanges = [
        {
            "exchange": "NYSE",
            "region": "USA",
            "index": "S&P 500",
            "value": "8,247.32",
            "change": "+2.3%",
            "status": StatusLevel.POSITIVE,
            "volume": "2.1B shares",
            "volatility": "12.8"
        },
        {
            "exchange": "LSE",
            "region": "UK",
            "index": "FTSE 100",
            "value": "7,842.55",
            "change": "+1.2%",
            "status": StatusLevel.POSITIVE,
            "volume": "156M shares",
            "volatility": "8.4"
        },
        {
            "exchange": "TSE",
            "region": "Japan",
            "index": "Nikkei 225",
            "value": "29,156.82",
            "change": "+3.1%",
            "status": StatusLevel.POSITIVE,
            "volume": "987M shares",
            "volatility": "14.2"
        },
        {
            "exchange": "SSE",
            "region": "China",
            "index": "Shanghai Composite",
            "value": "3,087.42",
            "change": "-0.8%",
            "status": StatusLevel.NEGATIVE,
            "volume": "423M shares",
            "volatility": "16.5"
        },
        {
            "exchange": "DAX",
            "region": "Germany",
            "index": "DAX 40",
            "value": "17,823.45",
            "change": "+0.9%",
            "status": StatusLevel.POSITIVE,
            "volume": "234M shares",
            "volatility": "9.2"
        },
        {
            "exchange": "ASX",
            "region": "Australia",
            "index": "ASX 200",
            "value": "7,456.23",
            "change": "+1.4%",
            "status": StatusLevel.POSITIVE,
            "volume": "128M shares",
            "volatility": "11.3"
        },
    ]

    for exchange in exchanges:
        col1, col2, col3, col4, col5 = st.columns([1.5, 1.5, 1.5, 1, 1])

        with col1:
            st.markdown(f"**{exchange['exchange']}**")
            st.caption(exchange['region'])

        with col2:
            st.markdown(f"<span class='label-md'>{exchange['index']}</span>", unsafe_allow_html=True)

        with col3:
            st.markdown(f"<span class='data-md'>{exchange['value']}</span>", unsafe_allow_html=True)

        with col4:
            st.markdown(
                f"<span class='{exchange['status'].value}'>{exchange['change']}</span>",
                unsafe_allow_html=True
            )

        with col5:
            vol_numeric = float(exchange['volatility'])
            vol_status = StatusLevel.NEGATIVE if vol_numeric > 13 else StatusLevel.POSITIVE
            st.markdown(
                f"<span class='{vol_status.value} data-sm'>σ{exchange['volatility']}</span>",
                unsafe_allow_html=True
            )

        st.divider()


def render_capital_flows():
    """Global capital movement patterns"""
    st.markdown("### CAPITAL FLOW INTELLIGENCE", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Inbound Capital")
        inflows = [
            {"source": "Emerging Markets", "amount": "$8.4B", "status": StatusLevel.POSITIVE},
            {"source": "Sovereign Funds", "amount": "$5.2B", "status": StatusLevel.POSITIVE},
            {"source": "Retail Investors", "amount": "$2.1B", "status": StatusLevel.POSITIVE},
        ]

        for flow in inflows:
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.markdown(f"**{flow['source']}**")
            with col_b:
                st.markdown(
                    f"<span class='{flow['status'].value}'>{flow['amount']}</span>",
                    unsafe_allow_html=True
                )
            st.divider()

    with col2:
        st.markdown("#### Outbound Capital")
        outflows = [
            {"dest": "Currency Markets", "amount": "$3.2B", "status": StatusLevel.NEGATIVE},
            {"dest": "Commodities", "amount": "$1.8B", "status": StatusLevel.NEGATIVE},
            {"dest": "Bonds", "amount": "$2.5B", "status": StatusLevel.NEUTRAL},
        ]

        for flow in outflows:
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.markdown(f"**{flow['dest']}**")
            with col_b:
                st.markdown(
                    f"<span class='{flow['status'].value}'>{flow['amount']}</span>",
                    unsafe_allow_html=True
                )
            st.divider()


def render_geopolitical_markers():
    """Real-time geo-risk indicators"""
    st.markdown("### GEO-RISK MARKERS", unsafe_allow_html=True)

    risks = [
        {
            "location": "Eastern Europe",
            "risk_level": "HIGH",
            "status": StatusLevel.NEGATIVE,
            "impact": "Energy prices, defense stocks",
            "trend": "↑ Escalating"
        },
        {
            "location": "US-Taiwan Strait",
            "risk_level": "MODERATE",
            "status": StatusLevel.PRIMARY,
            "impact": "Tech supply chains, semiconductor prices",
            "trend": "→ Stable"
        },
        {
            "location": "Middle East Oil Routes",
            "risk_level": "MODERATE",
            "status": StatusLevel.PRIMARY,
            "impact": "Oil & gas, shipping costs",
            "trend": "↓ Improving"
        },
        {
            "location": "EU Regulatory Changes",
            "risk_level": "MODERATE",
            "status": StatusLevel.PRIMARY,
            "impact": "Tech fines, banking regulations",
            "trend": "→ Ongoing"
        },
    ]

    for risk in risks:
        col1, col2, col3, col4 = st.columns([1.5, 1.2, 2, 1.3])

        with col1:
            st.markdown(f"**{risk['location']}**")

        with col2:
            st.markdown(
                f"<span class='{risk['status'].value} label-md'>{risk['risk_level']}</span>",
                unsafe_allow_html=True
            )

        with col3:
            st.caption(risk['impact'])

        with col4:
            st.markdown(f"<span class='text-secondary'>{risk['trend']}</span>", unsafe_allow_html=True)

        st.divider()


def render_economic_calendar():
    """Upcoming economic events by region"""
    st.markdown("### ECONOMIC CALENDAR (NEXT 7 DAYS)", unsafe_allow_html=True)

    events = [
        {"date": "Today", "time": "14:30", "country": "USA", "event": "Fed Minutes", "impact": "HIGH"},
        {"date": "Tomorrow", "time": "09:00", "country": "EUR", "event": "CPI Release", "impact": "HIGH"},
        {"date": "Wed", "time": "15:00", "country": "GBP", "event": "BOE Decision", "impact": "CRITICAL"},
        {"date": "Thu", "time": "08:30", "country": "JPY", "event": "Employment Data", "impact": "MEDIUM"},
        {"date": "Fri", "time": "13:30", "country": "USA", "event": "Jobs Report", "impact": "CRITICAL"},
    ]

    for event in events:
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 2, 1])

        with col1:
            st.caption(f"**{event['date']}**")

        with col2:
            st.caption(event['time'])

        with col3:
            st.markdown(f"<span class='label-md'>{event['country']}</span>", unsafe_allow_html=True)

        with col4:
            st.markdown(f"**{event['event']}**")

        with col5:
            impact_status = StatusLevel.NEGATIVE if event['impact'] == 'CRITICAL' else StatusLevel.PRIMARY
            st.markdown(
                f"<span class='{impact_status.value}'>{event['impact']}</span>",
                unsafe_allow_html=True
            )

        st.divider()


def render_market_synchronization():
    """Cross-market correlation analysis"""
    st.markdown("### MARKET SYNCHRONIZATION INDEX", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        data_card(
            "EQUITY CORRELATION",
            [
                DataPoint("0.87", "All Markets", StatusLevel.POSITIVE),
                DataPoint("0.92", "Developed", StatusLevel.POSITIVE),
                DataPoint("0.65", "Emerging", StatusLevel.NEUTRAL),
            ]
        )

    with col2:
        data_card(
            "SECTOR COHERENCE",
            [
                DataPoint("0.76", "Tech Leading", StatusLevel.POSITIVE),
                DataPoint("0.43", "Energy Lagging", StatusLevel.NEGATIVE),
                DataPoint("0.81", "Financials", StatusLevel.POSITIVE),
            ]
        )

    with col3:
        data_card(
            "CURRENCY MOVES",
            [
                DataPoint("USD Index: 104.2", "Strong Dollar", StatusLevel.POSITIVE),
                DataPoint("EUR/USD: 1.09", "Euro Weak", StatusLevel.NEGATIVE),
                DataPoint("JPY Vol: 18.4%", "Elevated", StatusLevel.NEUTRAL),
            ]
        )


def render():
    """Main Earth Pulse view"""
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "styles.css")) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    render_earth_pulse_header()
    render_global_heatmap()
    divider_section()

    render_major_exchanges()
    divider_section()

    render_capital_flows()
    divider_section()

    render_geopolitical_markers()
    divider_section()

    render_economic_calendar()
    divider_section()

    render_market_synchronization()


if __name__ == "__main__":
    st.set_page_config(
        page_title="Earth Pulse | Geospatial Intelligence",
        page_icon="🌍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    render()
