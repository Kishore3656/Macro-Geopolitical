"""Trading Guide - Simple, actionable reference for users new to the platform"""

import streamlit as st

from components import alert_box, data_card, divider_section, StatusLevel, DataPoint


def render():
    st.markdown("## TRADING GUIDE")
    st.caption("How to read signals, manage risk, and use this platform effectively")
    st.divider()

    # ── Platform Overview ──────────────────────────────────────────────────────
    st.markdown("### WHAT THIS PLATFORM DOES")
    col1, col2, col3 = st.columns(3)
    with col1:
        data_card("DATA INGESTION", [
            DataPoint("Reuters, BBC, AP, AJ", "News Sources",   StatusLevel.NEUTRAL),
            DataPoint("Every 5 minutes",       "RSS Refresh",    StatusLevel.POSITIVE),
            DataPoint("GDELT events",          "Geopolitical",   StatusLevel.NEUTRAL),
        ])
    with col2:
        data_card("ML MODELS", [
            DataPoint("LightGBM",  "Model Type",        StatusLevel.NEUTRAL),
            DataPoint("SPY hourly","Training Data",     StatusLevel.NEUTRAL),
            DataPoint("GTI + OHLCV","Features",         StatusLevel.NEUTRAL),
        ])
    with col3:
        data_card("SIGNALS OUTPUT", [
            DataPoint("UP / DOWN",   "Direction Call",  StatusLevel.NEUTRAL),
            DataPoint("HIGH / LOW",  "Volatility Call", StatusLevel.NEUTRAL),
            DataPoint("0–100%",      "Confidence",      StatusLevel.NEUTRAL),
        ])

    divider_section()

    # ── Reading the GTI ────────────────────────────────────────────────────────
    st.markdown("### GEOPOLITICAL TENSION INDEX (GTI)")
    st.markdown(
        "The GTI is a single number from **0.0 (calm) to 1.0 (max tension)** "
        "built from three real-time signals:"
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        data_card("GDELT CONFLICTS (50%)", [
            DataPoint("Conflict ratio",        "Signal",  StatusLevel.NEUTRAL),
            DataPoint("GoldsteinScale < -5.0", "Trigger", StatusLevel.NEGATIVE),
            DataPoint("6-hour window",         "Lookback", StatusLevel.NEUTRAL),
        ])
    with col2:
        data_card("GLOBAL TONE (30%)", [
            DataPoint("Avg article tone",    "Signal",   StatusLevel.NEUTRAL),
            DataPoint("Negative = tension",  "Direction", StatusLevel.NEUTRAL),
            DataPoint("GDELT AvgTone field", "Source",   StatusLevel.NEUTRAL),
        ])
    with col3:
        data_card("NEWS SENTIMENT (20%)", [
            DataPoint("VADER compound",     "Signal",   StatusLevel.NEUTRAL),
            DataPoint("RSS headlines",       "Source",   StatusLevel.NEUTRAL),
            DataPoint("-1.0 to +1.0 scale", "Range",    StatusLevel.NEUTRAL),
        ])

    st.markdown("**Interpretation guide:**")
    col1, col2, col3, col4 = st.columns(4)
    for col, (range_str, label, desc, status) in zip(
        [col1, col2, col3, col4],
        [("0.0 – 0.3", "CALM",     "Low geopolitical risk. Markets likely stable.", StatusLevel.POSITIVE),
         ("0.3 – 0.5", "MODERATE", "Mild tension. Normal volatility expected.",     StatusLevel.NEUTRAL),
         ("0.5 – 0.7", "ELEVATED", "Rising risk. Consider defensive positions.",    StatusLevel.PRIMARY),
         ("0.7 – 1.0", "CRITICAL", "High tension. Reduce exposure, widen stops.",   StatusLevel.NEGATIVE)]
    ):
        with col:
            st.markdown(f"<span class='{status.value} data-md'>{range_str}</span>", unsafe_allow_html=True)
            st.markdown(f"**{label}**")
            st.caption(desc)

    divider_section()

    # ── Reading AI Signals ─────────────────────────────────────────────────────
    st.markdown("### HOW TO READ AI SIGNALS")
    alert_box(
        "Signals are probabilistic, not guaranteed. Always combine with your own analysis and use stop-losses.",
        StatusLevel.PRIMARY
    )
    st.markdown("")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Signal Fields Explained")
        fields = [
            ("ID",         "Unique signal reference (SIG-001, SIG-002…)"),
            ("Asset",      "Ticker symbol to trade (NVDA, SPY, GLD…)"),
            ("Type",       "BUY = go long, SELL = go short, HOLD = wait"),
            ("Confidence", "Model probability. >85% is high conviction"),
            ("Entry",      "Suggested price to enter the trade"),
            ("Target",     "Price objective if trade works"),
            ("Stop",       "Exit level if trade goes against you"),
        ]
        for field, desc in fields:
            c1, c2 = st.columns([1.2, 3])
            with c1:
                st.markdown(f"**{field}**")
            with c2:
                st.caption(desc)
            st.divider()

    with col2:
        st.markdown("#### Confidence Level Guide")
        for low, high, action, status in [
            ("90–100%", "Very High", "Strong signal. Size normally.",                    StatusLevel.POSITIVE),
            ("75–90%",  "High",      "Good signal. Reduce size slightly.",               StatusLevel.POSITIVE),
            ("60–75%",  "Moderate",  "Use caution. Smaller position, tighter stop.",     StatusLevel.NEUTRAL),
            ("<60%",    "Low",       "Skip or paper-trade only. Not actionable.",        StatusLevel.NEGATIVE),
        ]:
            c1, c2, c3 = st.columns([1, 1.2, 2.5])
            with c1:
                st.markdown(f"<span class='{status.value}'>{low}</span>", unsafe_allow_html=True)
            with c2:
                st.caption(high)
            with c3:
                st.caption(action)
            st.divider()

    divider_section()

    # ── Risk Management ────────────────────────────────────────────────────────
    st.markdown("### RISK MANAGEMENT BASICS")
    col1, col2, col3 = st.columns(3)
    with col1:
        data_card("POSITION SIZING", [
            DataPoint("1–2% per trade",  "Max Risk",         StatusLevel.POSITIVE),
            DataPoint("Never exceed",    "5% total exposure", StatusLevel.NEGATIVE),
            DataPoint("Smaller on low-confidence", "Rule",   StatusLevel.NEUTRAL),
        ])
    with col2:
        data_card("STOP-LOSS RULES", [
            DataPoint("Always set a stop",    "Rule #1",      StatusLevel.POSITIVE),
            DataPoint("Use signal stop level","Default",      StatusLevel.NEUTRAL),
            DataPoint("Move to break-even",   "At 50% target",StatusLevel.NEUTRAL),
        ])
    with col3:
        data_card("MARKET CONDITIONS", [
            DataPoint("GTI > 0.7 → reduce size", "High Risk",    StatusLevel.NEGATIVE),
            DataPoint("VIX > 25 → defensive",    "Volatile",     StatusLevel.NEGATIVE),
            DataPoint("Earnings week → avoid",   "Event Risk",   StatusLevel.NEUTRAL),
        ])

    divider_section()

    # ── Dashboard Navigation ───────────────────────────────────────────────────
    st.markdown("### DASHBOARD NAVIGATION")
    tabs = [
        ("Tactical Archive",    "Real-time market overview, alerts, sector breakdown, and portfolio impact. Start here every session."),
        ("Earth Pulse",         "Global markets, exchange-by-exchange pulse, capital flows, geo-risk map, and economic calendar."),
        ("Market Intelligence", "S&P 500 deep-dive: sector rankings, movers, earnings, valuation, breadth, and technical signals."),
        ("AI Signals",          "Live ML-generated trade signals, model confidence, anomaly detection, and sentiment breakdown."),
        ("Geo Map",             "Country-level heatmap, currency intelligence, commodity prices, supply chain, and trade flows."),
        ("Trading Guide",       "This page — platform reference, signal interpretation, and risk management rules."),
    ]
    for tab_name, description in tabs:
        c1, c2 = st.columns([1.5, 3.5])
        with c1:
            st.markdown(f"**{tab_name}**")
        with c2:
            st.caption(description)
        st.divider()

    divider_section()

    # ── Quick Start Checklist ──────────────────────────────────────────────────
    st.markdown("### DAILY CHECKLIST")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Before Market Open")
        for item in [
            "Check GTI score — above 0.5? Reduce position sizes",
            "Review Economic Calendar on Earth Pulse for events today",
            "Scan Critical Alerts on Tactical Archive",
            "Note any earnings releases (Market Intelligence tab)",
        ]:
            st.markdown(f"- {item}")
    with col2:
        st.markdown("#### During Session")
        for item in [
            "Check AI Signals for new BUY/SELL with >75% confidence",
            "Monitor VIX — spike above 20 = reduce risk",
            "Watch sector rotation on Market Intelligence",
            "Check Geo Map for commodity moves if holding related assets",
        ]:
            st.markdown(f"- {item}")

    divider_section()

    alert_box(
        "This platform provides analytical intelligence only. It is not financial advice. "
        "Always do your own research and understand the risks before trading.",
        StatusLevel.NEUTRAL
    )
