"""
AI Signals - Machine learning predictions and algorithmic intelligence
"""

import streamlit as st
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components import (
    data_card, alert_box, live_indicator, status_badge,
    divider_section, hero_stat, section_divider,
    StatusLevel, DataPoint
)


def render_ai_signals_header():
    """ML Intelligence command center"""
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.markdown("## AI SIGNALS", unsafe_allow_html=True)
        st.caption("Machine Learning Predictions & Algorithmic Intelligence")

    with col2:
        live_indicator("ML MODELS ACTIVE")

    with col3:
        current_time = datetime.now().strftime("%H:%M:%S")
        st.markdown(f'<div class="data-md">{current_time}</div>', unsafe_allow_html=True)

    st.divider()


def render_model_confidence():
    """Current ML model confidence metrics"""
    st.markdown("### MODEL CONFIDENCE SCORES", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    models = [
        ("Price Direction", "87.4%", StatusLevel.POSITIVE),
        ("Volatility Pred", "72.1%", StatusLevel.POSITIVE),
        ("Sentiment Analysis", "64.8%", StatusLevel.NEUTRAL),
        ("Anomaly Detection", "91.3%", StatusLevel.POSITIVE),
    ]

    for col, (name, score, status) in zip([col1, col2, col3, col4], models):
        with col:
            hero_stat(score, name, accent=(status == StatusLevel.POSITIVE))


def render_active_signals():
    """Live algorithmic trading signals"""
    st.markdown("### ACTIVE TRADING SIGNALS", unsafe_allow_html=True)

    signals = [
        {
            "id": "SIG-001",
            "asset": "NVDA",
            "type": "BUY",
            "confidence": "94.2%",
            "entry": "$892.50",
            "target": "$945.00",
            "stop": "$865.00",
            "reasoning": "Breakout above 200-DMA with bullish divergence",
            "strength": StatusLevel.POSITIVE
        },
        {
            "id": "SIG-002",
            "asset": "SPY",
            "type": "HOLD",
            "confidence": "72.8%",
            "entry": "$425.30",
            "target": "$435.00",
            "stop": "$420.00",
            "reasoning": "Consolidation pattern - await breakout confirmation",
            "strength": StatusLevel.NEUTRAL
        },
        {
            "id": "SIG-003",
            "asset": "QQQ",
            "type": "SELL",
            "confidence": "81.5%",
            "entry": "$356.80",
            "target": "$340.00",
            "stop": "$365.00",
            "reasoning": "Overbought conditions with negative divergence",
            "strength": StatusLevel.NEGATIVE
        },
        {
            "id": "SIG-004",
            "asset": "GLD",
            "type": "BUY",
            "confidence": "77.3%",
            "entry": "$187.25",
            "target": "$198.00",
            "stop": "$182.50",
            "reasoning": "Safe-haven accumulation amid volatility",
            "strength": StatusLevel.POSITIVE
        },
    ]

    for signal in signals:
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([0.8, 1, 1.2, 1.5, 2])

            with col1:
                st.markdown(f"<span class='label-md'>{signal['id']}</span>", unsafe_allow_html=True)

            with col2:
                st.markdown(f"**{signal['asset']}**")

            with col3:
                signal_color = "text-positive" if signal['type'] == "BUY" else "text-negative" if signal['type'] == "SELL" else "text-secondary"
                st.markdown(
                    f"<span class='{signal_color}'>{signal['type']}</span>",
                    unsafe_allow_html=True
                )

            with col4:
                st.markdown(
                    f"<span class='{signal['strength'].value}'>{signal['confidence']}</span>",
                    unsafe_allow_html=True
                )

            with col5:
                st.caption(signal['reasoning'])

            # Expanded details
            col_a, col_b, col_c = st.columns([1.5, 1.5, 1.5])
            with col_a:
                st.caption(f"Entry: {signal['entry']}")
            with col_b:
                st.caption(f"Target: {signal['target']}")
            with col_c:
                st.caption(f"Stop: {signal['stop']}")

            st.divider()


def render_prediction_analysis():
    """Forward-looking predictions"""
    st.markdown("### FORWARD PREDICTIONS (24-HOUR)", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        data_card(
            "S&P 500",
            [
                DataPoint("+0.8%", "Expected Move", StatusLevel.POSITIVE),
                DataPoint("8,315", "Fair Value", StatusLevel.NEUTRAL),
                DataPoint("68%", "Probability", StatusLevel.POSITIVE),
            ],
            footer="Based on 50M historical patterns"
        )

    with col2:
        data_card(
            "VIX INDEX",
            [
                DataPoint("-1.2%", "Expected Move", StatusLevel.POSITIVE),
                DataPoint("12.2", "Fair Value", StatusLevel.POSITIVE),
                DataPoint("73%", "Probability", StatusLevel.POSITIVE),
            ],
            footer="Volatility mean-reversion signal"
        )

    with col3:
        data_card(
            "USD INDEX",
            [
                DataPoint("+0.3%", "Expected Move", StatusLevel.NEUTRAL),
                DataPoint("104.5", "Fair Value", StatusLevel.NEUTRAL),
                DataPoint("52%", "Probability", StatusLevel.NEUTRAL),
            ],
            footer="Range-bound consolidation expected"
        )


def render_anomaly_detection():
    """Unusual market patterns"""
    st.markdown("### ANOMALY ALERTS", unsafe_allow_html=True)

    anomalies = [
        {
            "severity": StatusLevel.NEGATIVE,
            "pattern": "Large Block Trade Detected",
            "details": "10M shares of MSFT accumulating over 90 minutes",
            "confidence": "96%",
            "action": "Monitor for institutional buying"
        },
        {
            "severity": StatusLevel.PRIMARY,
            "pattern": "Unusual Options Activity",
            "details": "Call options on SPY with 2-week expiration spiking",
            "confidence": "78%",
            "action": "Check implied volatility changes"
        },
        {
            "severity": StatusLevel.NEGATIVE,
            "pattern": "Liquidity Withdrawal",
            "details": "Bid-ask spreads widening on corporate bonds",
            "confidence": "82%",
            "action": "Risk-off sentiment emerging"
        },
    ]

    for anomaly in anomalies:
        col1, col2, col3 = st.columns([0.1, 4, 1])

        with col1:
            st.markdown(f"<span class='{anomaly['severity'].value}'>●</span>", unsafe_allow_html=True)

        with col2:
            st.markdown(f"**{anomaly['pattern']}**")
            st.caption(anomaly['details'])
            st.caption(f"<span class='text-secondary'>Confidence: {anomaly['confidence']}</span>", unsafe_allow_html=True)

        with col3:
            st.button("Act", key=f"anomaly_{anomaly['pattern']}")

        st.divider()


def render_model_performance():
    """Historical model accuracy"""
    st.markdown("### MODEL PERFORMANCE (30-DAY)", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    metrics = [
        ("Win Rate", "67.3%", StatusLevel.POSITIVE),
        ("Avg Return", "+2.45%", StatusLevel.POSITIVE),
        ("Max Drawdown", "-3.2%", StatusLevel.NEUTRAL),
        ("Sharpe Ratio", "1.87", StatusLevel.POSITIVE),
    ]

    for col, (label, value, status) in zip([col1, col2, col3, col4], metrics):
        with col:
            hero_stat(value, label, accent=(status == StatusLevel.POSITIVE))


def render_correlation_matrix():
    """Asset correlation heatmap"""
    st.markdown("### CORRELATION ANALYSIS", unsafe_allow_html=True)

    st.markdown("""
    | Asset | S&P 500 | QQQ | VIX | USD | Gold |
    |-------|---------|-----|-----|-----|------|
    | **S&P 500** | 1.00 | 0.92 | -0.78 | -0.45 | 0.12 |
    | **QQQ** | 0.92 | 1.00 | -0.82 | -0.52 | 0.08 |
    | **VIX** | -0.78 | -0.82 | 1.00 | 0.34 | -0.08 |
    | **USD** | -0.45 | -0.52 | 0.34 | 1.00 | -0.68 |
    | **Gold** | 0.12 | 0.08 | -0.08 | -0.68 | 1.00 |
    """)

    st.caption("Strong negative correlation between stocks and VIX suggests flight-to-safety potential")


def render_sentiment_analysis():
    """Social and news sentiment"""
    st.markdown("### SENTIMENT ANALYSIS", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### News Sentiment")
        news_sources = [
            {"source": "Financial Times", "sentiment": "Bullish", "score": "+0.72"},
            {"source": "Bloomberg", "sentiment": "Neutral", "score": "+0.18"},
            {"source": "Reuters", "sentiment": "Bullish", "score": "+0.64"},
            {"source": "CNBC", "sentiment": "Very Bullish", "score": "+0.88"},
        ]

        for source in news_sources:
            col_a, col_b, col_c = st.columns([2, 1.5, 1])
            with col_a:
                st.markdown(f"**{source['source']}**")
            with col_b:
                st.caption(source['sentiment'])
            with col_c:
                sentiment_status = StatusLevel.POSITIVE if "+0." in source['score'] else StatusLevel.NEGATIVE
                st.markdown(
                    f"<span class='{sentiment_status.value}'>{source['score']}</span>",
                    unsafe_allow_html=True
                )
            st.divider()

    with col2:
        st.markdown("#### Social Sentiment")
        social_data = [
            {"platform": "Twitter Mentions", "trend": "+145%", "status": StatusLevel.POSITIVE},
            {"platform": "Reddit Communities", "trend": "+89%", "status": StatusLevel.POSITIVE},
            {"platform": "StockTwits", "trend": "+234%", "status": StatusLevel.POSITIVE},
            {"platform": "Fear & Greed Index", "trend": "75 (Greed)", "status": StatusLevel.POSITIVE},
        ]

        for data in social_data:
            col_a, col_b = st.columns([2, 1])
            with col_a:
                st.markdown(f"**{data['platform']}**")
            with col_b:
                st.markdown(
                    f"<span class='{data['status'].value}'>{data['trend']}</span>",
                    unsafe_allow_html=True
                )
            st.divider()


def render():
    """Main AI Signals view"""
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "styles.css")) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    render_ai_signals_header()
    render_model_confidence()
    divider_section()

    render_active_signals()
    divider_section()

    render_prediction_analysis()
    divider_section()

    render_anomaly_detection()
    divider_section()

    render_model_performance()
    divider_section()

    render_correlation_matrix()
    divider_section()

    render_sentiment_analysis()


if __name__ == "__main__":
    st.set_page_config(
        page_title="AI Signals | ML Intelligence",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    render()
