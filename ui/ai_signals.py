"""AI Signals - GEOMARKET INTELLIGENCE"""

import streamlit as st
from datetime import datetime
import plotly.graph_objects as go
import numpy as np
from api.client import get_client


def _gti_breakdown_chart(signals_data: dict) -> go.Figure:
    """GTI Component Breakdown from live signal history."""
    history = signals_data.get("data", [])[:24]
    if not history:
        fig = go.Figure()
        fig.add_annotation(text="No signal history", x=0.5, y=0.5, showarrow=False)
        fig.update_layout(height=180, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        return fig

    timestamps = [datetime.fromisoformat(h["timestamp"]) for h in history]
    vol_probs = [h.get("vol_prob", 0.5) * 100 for h in history]
    dir_probs = [h.get("dir_prob", 0.5) * 100 for h in history]
    gti_scores = [h.get("gti_score", 0.5) * 100 for h in history]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=timestamps, y=gti_scores, name="GTI",
        mode="lines", line=dict(color="#ffb867", width=1.5),
        fill="tozeroy", fillcolor="rgba(255,184,103,0.08)",
    ))
    fig.add_trace(go.Scatter(
        x=timestamps, y=vol_probs, name="VOL_PROB",
        mode="lines", line=dict(color="#6eaacf", width=1.2),
        fill="tozeroy", fillcolor="rgba(110,170,207,0.06)",
    ))
    fig.add_trace(go.Scatter(
        x=timestamps, y=dir_probs, name="DIR_PROB",
        mode="lines", line=dict(color="#6ecf8a", width=1.0),
        fill="tozeroy", fillcolor="rgba(110,207,138,0.05)",
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=28, b=0),
        height=180,
        title=dict(
            text="Signal Component Breakdown",
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
    client = get_client()

    # Fetch real signals
    signals_current = client.get_signals_current()
    signals_history = client.get_signals_history(limit=100)

    # ── Page header ───────────────────────────────────────────────────────────
    gti_score = signals_current.get("gti_score", 0.5)
    gti_display = gti_score * 100
    st.markdown(f"""
<div class="system-status-row">
  <span class="system-status-label">GTI: {gti_display:.1f} | STATUS: {signals_current.get('status', 'UNKNOWN')}</span>
</div>
""", unsafe_allow_html=True)

    # ── 3-column layout: left | center | right ────────────────────────────────
    left, center, right = st.columns([1.0, 2.4, 1.2])

    # ────────────────── LEFT: Model output + GTI features ───────────────────
    with left:
        st.markdown('<div class="section-header">▸ MODEL OUTPUT</div>', unsafe_allow_html=True)

        vol_pred = signals_current.get("vol_prediction", "UNKNOWN")
        vol_prob = signals_current.get("vol_prob", 0.5)
        dir_pred = signals_current.get("dir_prediction", "UNKNOWN")
        dir_prob = signals_current.get("dir_prob", 0.5)

        vol_label = "▼" if vol_prob < 0.4 else "▲" if vol_prob > 0.6 else "="
        st.markdown(f"""
<div class="model-output-panel">
  <div class="model-output-title">PREDICTED VOLATILITY</div>
  <div class="model-volatility">{vol_prob*100:.1f}<span style="font-size:16px;color:#8a9baa;">%</span></div>
  <div class="model-vol-label">{vol_label} {vol_pred}</div>
  <div class="model-direction">MARKET DIRECTION: <span style="color:#ffb867;">{dir_pred}</span> <span style="font-size:10px;color:#8a9baa;">{dir_prob*100:.0f}% CONF.</span></div>
</div>
""", unsafe_allow_html=True)

        st.markdown('<div class="section-header" style="margin-top:10px;">GTI INPUT FEATURES</div>', unsafe_allow_html=True)

        features = [
            ("GTI_SCORE", "#ff8c42", gti_display),
            ("VOL_PROB", "#ffb867", vol_prob * 100),
            ("DIR_PROB", "#8a9baa", dir_prob * 100),
            ("CONFLICT_RATIO", "#6eaacf", (signals_current.get("conflict_ratio", 0.5) if "conflict_ratio" in signals_current else 0.5) * 100),
            ("SIGNAL_STATUS", "#6ecf8a", 100 if signals_current.get("status") == "LIVE" else 50),
        ]
        for name, color, pct in features:
            st.markdown(f"""
<div class="feature-row">
  <span class="feature-name">{name}</span>
  <div class="feature-bar-wrap">
    <div class="feature-bar-fill" style="width:{min(pct, 100)}%;background:{color};"></div>
  </div>
  <span class="feature-value" style="color:{color};">{pct:.0f}%</span>
</div>""", unsafe_allow_html=True)

        st.markdown(f"""
<div class="caption-mono" style="margin-top:6px;">
  LAST_UPDATED: {signals_current.get('timestamp', 'N/A')}<br/>
  MODEL: LGBM_V2 | STATUS: {signals_current.get('status', 'UNKNOWN')}
</div>
""", unsafe_allow_html=True)

    # ────────────────── CENTER: Breakdown chart + prediction history ─────────
    with center:
        # Signal breakdown chart
        st.plotly_chart(_gti_breakdown_chart(signals_history), use_container_width=True, config={"displayModeBar": False})

        st.markdown('<div class="caption-mono" style="margin-top:-8px;margin-bottom:8px;">PREDICTION CONFIDENCE TRAJECTORY</div>', unsafe_allow_html=True)

        # Prediction history
        st.markdown('<div class="section-header">PREDICTION HISTORY</div>', unsafe_allow_html=True)

        history_items = signals_history.get("data", [])
        if not history_items:
            st.markdown("""
<div class="history-empty">
  <div class="history-empty-icon">📊</div>
  <div class="history-empty-title">HISTORY LOG EMPTY</div>
  <div class="history-empty-sub">NO PREDICTIONS YET.<br/>RUN BACKEND TO GENERATE.</div>
</div>
""", unsafe_allow_html=True)
        else:
            for item in history_items[:5]:
                st.markdown(f"""
<div style="font-size:12px;color:#d8dae8;padding:8px;border-left:2px solid #ffb867;margin-bottom:4px;">
  <strong>{item.get('timestamp', 'N/A')}</strong> — Vol: {item.get('vol_prediction')} ({item.get('vol_prob', 0)*100:.0f}%) | Dir: {item.get('dir_prediction')} ({item.get('dir_prob', 0)*100:.0f}%)
</div>
""", unsafe_allow_html=True)

        st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)

        # Sentiment footer (from headlines)
        sentiment_data = client.get_headlines(limit=20)
        headlines = sentiment_data.get("data", [])
        if headlines:
            pos_count = sum(1 for h in headlines if h.get("sentiment") == "positive")
            neu_count = sum(1 for h in headlines if h.get("sentiment") == "neutral")
            neg_count = sum(1 for h in headlines if h.get("sentiment") == "negative")
            total = len(headlines)
            pos_pct = (pos_count / total) * 100 if total > 0 else 0
            neu_pct = (neu_count / total) * 100 if total > 0 else 0
            neg_pct = (neg_count / total) * 100 if total > 0 else 0
        else:
            pos_pct = neu_pct = neg_pct = 33

        st.markdown(f"""
<div class="section-header">SENTIMENT MOMENTUM</div>
<div class="sentiment-bar-row">
  <span class="sentiment-bar-label">SENTIMENT SCORE</span>
  <div class="sentiment-bar-track">
    <div class="sent-pos" style="width:{pos_pct}%;height:100%;"></div>
    <div class="sent-neu" style="width:{neu_pct}%;height:100%;"></div>
    <div class="sent-neg" style="width:{neg_pct}%;height:100%;"></div>
  </div>
  <span class="sentiment-stat">{pos_pct:.0f}% POSITIVE &nbsp;|&nbsp; {neu_pct:.0f}% NEUTRAL &nbsp;|&nbsp; {neg_pct:.0f}% NEGATIVE</span>
</div>
""", unsafe_allow_html=True)

    # ────────────────── RIGHT: Full impact analysis ──────────────────────────
    with right:
        st.markdown('<div class="section-header">ASSET IMPACT</div>', unsafe_allow_html=True)

        if dir_pred == "UP":
            bullish_assets = ["SPX_500", "QQQ_100", "XLK", "XLV", "XLI"]
            neutral_assets = ["EUR/USD", "GLD"]
            bearish_assets = ["TLT", "SHV"]
        elif dir_pred == "DOWN":
            bearish_assets = ["SPX_500", "QQQ_100", "XLE", "XLY", "XLU"]
            neutral_assets = ["USD/JPY", "VIX"]
            bullish_assets = ["GLD", "TLT"]
        else:
            bullish_assets = ["GLD", "USD"]
            neutral_assets = ["SPX_500", "QQQ_100"]
            bearish_assets = []

        # Bullish assets
        st.markdown("""
<div class="impact-category">
  <div class="impact-category-label">
    ASSET CATEGORY:
    <span class="impact-badge-bullish">BULLISH</span>
  </div>
""", unsafe_allow_html=True)
        for asset in bullish_assets[:3]:
            st.markdown(f"""
  <div class="impact-asset-row">
    <span class="impact-asset-name">{asset}</span>
    <span class="impact-arrow impact-arrow-up">↑</span>
  </div>
""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Neutral assets
        st.markdown("""
<div class="impact-category">
  <div class="impact-category-label">
    ASSET CATEGORY:
    <span class="impact-badge-neutral">NEUTRAL</span>
  </div>
""", unsafe_allow_html=True)
        for asset in neutral_assets[:2]:
            st.markdown(f"""
  <div class="impact-asset-row">
    <span class="impact-asset-name">{asset}</span>
    <span class="impact-arrow impact-arrow-neut">→</span>
  </div>
""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Bearish assets
        if bearish_assets:
            st.markdown("""
<div class="impact-category">
  <div class="impact-category-label">
    ASSET CATEGORY:
    <span class="impact-badge-bearish">BEARISH</span>
  </div>
""", unsafe_allow_html=True)
            for asset in bearish_assets[:2]:
                st.markdown(f"""
  <div class="impact-asset-row">
    <span class="impact-asset-name">{asset}</span>
    <span class="impact-arrow impact-arrow-down">↓</span>
  </div>
""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(f"""
<div style="margin-top:12px;">
  <div class="caption-mono">SYSTEM: {signals_current.get('status', 'UNKNOWN')} &nbsp;|&nbsp; CONF: {dir_prob*100:.0f}% &nbsp;|&nbsp; GTI: {gti_display:.1f}</div>
</div>
""", unsafe_allow_html=True)
