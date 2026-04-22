"""AI Signals - GEOMARKET INTELLIGENCE"""

import streamlit as st
from datetime import datetime, timedelta
import plotly.graph_objects as go
import numpy as np
import random


def _gti_breakdown_chart() -> go.Figure:
    """GTI Component Breakdown — Time-Series Attribution Analysis (CMA)."""
    random.seed(7)
    hours = 24
    t = [datetime.now() - timedelta(hours=hours - i) for i in range(hours)]

    macro = [20 + random.gauss(0, 2) for _ in range(hours)]
    micro = [10 + random.gauss(0, 1.5) for _ in range(hours)]
    quant = [8 + random.gauss(0, 1) for _ in range(hours)]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=t, y=macro, name="MACRO",
        mode="lines", line=dict(color="#ffb867", width=1.5),
        fill="tozeroy", fillcolor="rgba(255,184,103,0.08)",
    ))
    fig.add_trace(go.Scatter(
        x=t, y=micro, name="MICRO",
        mode="lines", line=dict(color="#6eaacf", width=1.2),
        fill="tozeroy", fillcolor="rgba(110,170,207,0.06)",
    ))
    fig.add_trace(go.Scatter(
        x=t, y=quant, name="QUANT",
        mode="lines", line=dict(color="#6ecf8a", width=1.0),
        fill="tozeroy", fillcolor="rgba(110,207,138,0.05)",
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=28, b=0),
        height=180,
        title=dict(
            text="GTI Component Breakdown",
            font=dict(size=10, color="#d8dae8", family="JetBrains Mono"),
            x=0,
        ),
        xaxis=dict(showgrid=False, tickfont=dict(size=8, color="#4a5060"),
                   color="#4a5060", showticklabels=True),
        yaxis=dict(showgrid=True, gridcolor="#1f2129", tickfont=dict(size=8, color="#4a5060"),
                   zeroline=False),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
            font=dict(size=8, color="#8a9baa"),
            bgcolor="rgba(0,0,0,0)",
        ),
        showlegend=True,
    )
    return fig


def render():
    # ── Page header ───────────────────────────────────────────────────────────
    st.markdown("""
<div class="system-status-row">
  <span class="system-status-label">GTI Scores: 55</span>
</div>
""", unsafe_allow_html=True)

    # ── 3-column layout: left | center | right ────────────────────────────────
    left, center, right = st.columns([1.0, 2.4, 1.2])

    # ────────────────── LEFT: Model output + GTI features ───────────────────
    with left:
        st.markdown('<div class="section-header">▸ MODEL OUTPUT</div>', unsafe_allow_html=True)

        # Model output panel — volatility
        st.markdown("""
<div class="model-output-panel">
  <div class="model-output-title">PREDICTED VOLATILITY</div>
  <div class="model-volatility">14.82<span style="font-size:16px;color:#8a9baa;">%</span></div>
  <div class="model-vol-label">▼VARIABLE</div>
  <div class="model-direction">MARKET DIRECTION: <span style="color:#ffb867;">BULLISH</span> <span style="font-size:10px;color:#8a9baa;">30% CONF.</span></div>
</div>
""", unsafe_allow_html=True)

        st.markdown('<div class="section-header" style="margin-top:10px;">GTI INPUT FEATURES</div>', unsafe_allow_html=True)

        features = [
            ("MACRO_SATELLITE", "#ff8c42", 42),
            ("GEOPOLITICAL_RISK", "#ffb867", 28),
            ("SENTIMENT_AGGREGATE", "#8a9baa", 15),
            ("LIQUIDITY_DEPTH", "#6eaacf", 18),
            ("SOCIAL_VOLUME", "#6ecf8a", 60),
        ]
        for name, color, pct in features:
            st.markdown(f"""
<div class="feature-row">
  <span class="feature-name">{name}</span>
  <div class="feature-bar-wrap">
    <div class="feature-bar-fill" style="width:{pct}%;background:{color};"></div>
  </div>
  <span class="feature-value" style="color:{color};">{pct}%</span>
</div>""", unsafe_allow_html=True)

        st.markdown("""
<div class="caption-mono" style="margin-top:6px;">
  LAST_UPDATED: 2026-08-16 19:33:09 UTC<br/>
  MODEL: LGBM_V2 | FEATURE_DIM: 12
</div>
""", unsafe_allow_html=True)

    # ────────────────── CENTER: Breakdown chart + prediction history ─────────
    with center:
        # GTI breakdown chart
        st.plotly_chart(_gti_breakdown_chart(), use_container_width=True, config={"displayModeBar": False})

        st.markdown('<div class="caption-mono" style="margin-top:-8px;margin-bottom:8px;">TIME-SERIES ATTRIBUTION ANALYSIS (CMA)</div>', unsafe_allow_html=True)

        # Prediction history
        st.markdown('<div class="section-header">PREDICTION HISTORY (SIMULATION MODE)</div>', unsafe_allow_html=True)

        st.markdown("""
<div class="history-empty">
  <div class="history-empty-icon">📊</div>
  <div class="history-empty-title">HISTORY LOG EMPTY</div>
  <div class="history-empty-sub">INITIATE TACTICAL SCAN TO POPULATE<br/>PREDICTION DATASET.</div>
  <div class="history-empty-action">▶ INITIATE_SCAN</div>
</div>
""", unsafe_allow_html=True)

        st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)

        # Sentiment footer
        st.markdown("""
<div class="section-header">SENTIMENT MOMENTUM</div>
<div class="sentiment-bar-row">
  <span class="sentiment-bar-label">SENTIMENT SCORE</span>
  <div class="sentiment-bar-track">
    <div class="sent-pos" style="width:22%;height:100%;"></div>
    <div class="sent-neu" style="width:56%;height:100%;"></div>
    <div class="sent-neg" style="width:22%;height:100%;"></div>
  </div>
  <span class="sentiment-stat">22% POSITIVE &nbsp;|&nbsp; 56% NEUTRAL &nbsp;|&nbsp; 22% NEGATIVE</span>
</div>
""", unsafe_allow_html=True)

    # ────────────────── RIGHT: Full impact analysis ──────────────────────────
    with right:
        st.markdown('<div class="section-header">FULL IMPACT ANALYSIS</div>', unsafe_allow_html=True)

        # Bullish assets
        st.markdown("""
<div class="impact-category">
  <div class="impact-category-label">
    ASSET CATEGORY:
    <span class="impact-badge-bullish">BULLISH</span>
  </div>
  <div class="impact-asset-row">
    <span class="impact-asset-name">XAU/USD</span>
    <span class="impact-arrow impact-arrow-up">↑</span>
  </div>
  <div class="impact-asset-row">
    <span class="impact-asset-name">USD/JPY</span>
    <span class="impact-arrow impact-arrow-up">↑</span>
  </div>
  <div class="impact-asset-row">
    <span class="impact-asset-name">BTC/COIN</span>
    <span class="impact-arrow impact-arrow-up">↑</span>
  </div>
</div>
""", unsafe_allow_html=True)

        # Neutral assets
        st.markdown("""
<div class="impact-category">
  <div class="impact-category-label">
    ASSET CATEGORY:
    <span class="impact-badge-neutral">NEUTRAL</span>
  </div>
  <div class="impact-asset-row">
    <span class="impact-asset-name">EUR/USD</span>
    <span class="impact-arrow impact-arrow-neut">→</span>
  </div>
  <div class="impact-asset-row">
    <span class="impact-asset-name">BRENT_OEL</span>
    <span class="impact-arrow impact-arrow-neut">→</span>
  </div>
</div>
""", unsafe_allow_html=True)

        # Bearish assets
        st.markdown("""
<div class="impact-category">
  <div class="impact-category-label">
    ASSET CATEGORY:
    <span class="impact-badge-bearish">BEARISH</span>
  </div>
  <div class="impact-asset-row">
    <span class="impact-asset-name">SPX_500</span>
    <span class="impact-arrow impact-arrow-down">↓</span>
  </div>
  <div class="impact-asset-row">
    <span class="impact-asset-name">NAS_100</span>
    <span class="impact-arrow impact-arrow-down">↓</span>
  </div>
</div>
""", unsafe_allow_html=True)

        st.markdown("""
<div style="margin-top:12px;">
  <div class="caption-mono">SYSTEM_STABLE &nbsp;|&nbsp; ENCRYPTION_AES256 &nbsp;|&nbsp; LATENCY_12MS</div>
</div>
""", unsafe_allow_html=True)
