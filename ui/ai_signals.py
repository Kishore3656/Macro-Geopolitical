"""AI Signals - Machine learning predictions and algorithmic intelligence"""

import streamlit as st
from datetime import datetime

from components import (
    data_card, alert_box, live_indicator, status_badge,
    divider_section, hero_stat,
    StatusLevel, DataPoint
)


def render():
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown("## AI SIGNALS")
        st.caption("Machine Learning Predictions & Algorithmic Intelligence")
    with col2:
        live_indicator("ML MODELS ACTIVE")
    with col3:
        st.markdown(f'<div class="data-md">{datetime.now().strftime("%H:%M:%S")}</div>', unsafe_allow_html=True)
    st.divider()

    # Model confidence
    st.markdown("### MODEL CONFIDENCE SCORES")
    col1, col2, col3, col4 = st.columns(4)
    for col, (name, score, status) in zip(
        [col1, col2, col3, col4],
        [("Price Direction",    "87.4%", StatusLevel.POSITIVE),
         ("Volatility Pred",    "72.1%", StatusLevel.POSITIVE),
         ("Sentiment Analysis", "64.8%", StatusLevel.NEUTRAL),
         ("Anomaly Detection",  "91.3%", StatusLevel.POSITIVE)]
    ):
        with col:
            hero_stat(score, name, accent=(status == StatusLevel.POSITIVE))

    divider_section()

    # Active trading signals
    st.markdown("### ACTIVE TRADING SIGNALS")
    signals = [
        ("SIG-001", "NVDA", "BUY",  "94.2%", "$892.50", "$945.00", "$865.00", "Breakout above 200-DMA with bullish divergence",     StatusLevel.POSITIVE),
        ("SIG-002", "SPY",  "HOLD", "72.8%", "$425.30", "$435.00", "$420.00", "Consolidation pattern — await breakout confirmation", StatusLevel.NEUTRAL),
        ("SIG-003", "QQQ",  "SELL", "81.5%", "$356.80", "$340.00", "$365.00", "Overbought conditions with negative divergence",      StatusLevel.NEGATIVE),
        ("SIG-004", "GLD",  "BUY",  "77.3%", "$187.25", "$198.00", "$182.50", "Safe-haven accumulation amid volatility",             StatusLevel.POSITIVE),
    ]
    for sig_id, asset, sig_type, conf, entry, target, stop, reason, strength in signals:
        c1, c2, c3, c4, c5 = st.columns([0.8, 1, 1.2, 1.5, 2])
        with c1:
            st.markdown(f"<span class='label-md'>{sig_id}</span>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"**{asset}**")
        with c3:
            color = "text-positive" if sig_type == "BUY" else "text-negative" if sig_type == "SELL" else "text-secondary"
            st.markdown(f"<span class='{color}'>{sig_type}</span>", unsafe_allow_html=True)
        with c4:
            st.markdown(f"<span class='{strength.value}'>{conf}</span>", unsafe_allow_html=True)
        with c5:
            st.caption(reason)
        ca, cb, cc = st.columns(3)
        with ca:
            st.caption(f"Entry: {entry}")
        with cb:
            st.caption(f"Target: {target}")
        with cc:
            st.caption(f"Stop: {stop}")
        st.divider()

    divider_section()

    # Forward predictions
    st.markdown("### FORWARD PREDICTIONS (24-HOUR)")
    col1, col2, col3 = st.columns(3)
    with col1:
        data_card("S&P 500", [
            DataPoint("+0.8%", "Expected Move", StatusLevel.POSITIVE),
            DataPoint("8,315", "Fair Value",    StatusLevel.NEUTRAL),
            DataPoint("68%",   "Probability",   StatusLevel.POSITIVE),
        ], footer="Based on 50M historical patterns")
    with col2:
        data_card("VIX INDEX", [
            DataPoint("-1.2%", "Expected Move", StatusLevel.POSITIVE),
            DataPoint("12.2",  "Fair Value",    StatusLevel.POSITIVE),
            DataPoint("73%",   "Probability",   StatusLevel.POSITIVE),
        ], footer="Volatility mean-reversion signal")
    with col3:
        data_card("USD INDEX", [
            DataPoint("+0.3%", "Expected Move", StatusLevel.NEUTRAL),
            DataPoint("104.5", "Fair Value",    StatusLevel.NEUTRAL),
            DataPoint("52%",   "Probability",   StatusLevel.NEUTRAL),
        ], footer="Range-bound consolidation expected")

    divider_section()

    # Anomaly detection
    st.markdown("### ANOMALY ALERTS")
    anomalies = [
        (StatusLevel.NEGATIVE, "Large Block Trade Detected",  "10M shares of MSFT accumulating over 90 minutes",     "96%", "Monitor for institutional buying"),
        (StatusLevel.PRIMARY,  "Unusual Options Activity",    "Call options on SPY with 2-week expiration spiking",   "78%", "Check implied volatility changes"),
        (StatusLevel.NEGATIVE, "Liquidity Withdrawal",        "Bid-ask spreads widening on corporate bonds",          "82%", "Risk-off sentiment emerging"),
    ]
    for severity, pattern, details, conf, action in anomalies:
        c1, c2, c3 = st.columns([0.1, 4, 1])
        with c1:
            st.markdown(f"<span class='{severity.value}'>●</span>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"**{pattern}**")
            st.caption(details)
            st.caption(f"<span class='text-secondary'>Confidence: {conf} — {action}</span>", unsafe_allow_html=True)
        with c3:
            st.button("Act", key=f"anomaly_{pattern[:20]}")
        st.divider()

    divider_section()

    # Model performance
    st.markdown("### MODEL PERFORMANCE (30-DAY)")
    col1, col2, col3, col4 = st.columns(4)
    for col, (label, value, status) in zip(
        [col1, col2, col3, col4],
        [("Win Rate",     "67.3%", StatusLevel.POSITIVE),
         ("Avg Return",   "+2.45%", StatusLevel.POSITIVE),
         ("Max Drawdown", "-3.2%",  StatusLevel.NEUTRAL),
         ("Sharpe Ratio", "1.87",   StatusLevel.POSITIVE)]
    ):
        with col:
            hero_stat(value, label, accent=(status == StatusLevel.POSITIVE))

    divider_section()

    # Correlation matrix
    st.markdown("### CORRELATION ANALYSIS")
    st.markdown("""
| Asset | S&P 500 | QQQ | VIX | USD | Gold |
|-------|---------|-----|-----|-----|------|
| **S&P 500** | 1.00 | 0.92 | -0.78 | -0.45 | 0.12 |
| **QQQ** | 0.92 | 1.00 | -0.82 | -0.52 | 0.08 |
| **VIX** | -0.78 | -0.82 | 1.00 | 0.34 | -0.08 |
| **USD** | -0.45 | -0.52 | 0.34 | 1.00 | -0.68 |
| **Gold** | 0.12 | 0.08 | -0.08 | -0.68 | 1.00 |
""")
    st.caption("Strong negative correlation between stocks and VIX indicates flight-to-safety potential")

    divider_section()

    # Sentiment analysis
    st.markdown("### SENTIMENT ANALYSIS")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### News Sentiment")
        for source, sentiment, score in [("Financial Times", "Bullish", "+0.72"), ("Bloomberg", "Neutral", "+0.18"), ("Reuters", "Bullish", "+0.64"), ("CNBC", "Very Bullish", "+0.88")]:
            c1, c2, c3 = st.columns([2, 1.5, 1])
            with c1:
                st.markdown(f"**{source}**")
            with c2:
                st.caption(sentiment)
            with c3:
                s = StatusLevel.POSITIVE if "+" in score else StatusLevel.NEGATIVE
                st.markdown(f"<span class='{s.value}'>{score}</span>", unsafe_allow_html=True)
            st.divider()
    with col2:
        st.markdown("#### Social Sentiment")
        for platform, trend in [("Twitter Mentions", "+145%"), ("Reddit Communities", "+89%"), ("StockTwits", "+234%"), ("Fear & Greed Index", "75 (Greed)")]:
            c1, c2 = st.columns([2, 1])
            with c1:
                st.markdown(f"**{platform}**")
            with c2:
                st.markdown(f"<span class='text-positive'>{trend}</span>", unsafe_allow_html=True)
            st.divider()
