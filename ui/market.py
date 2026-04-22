"""Market - GEOMARKET INTELLIGENCE"""

import streamlit as st
from datetime import datetime, timedelta
import plotly.graph_objects as go
import numpy as np
import random


def _spy_candlestick() -> go.Figure:
    """S&P 500 candlestick chart — simulated OHLCV data."""
    random.seed(99)
    bars = 40
    dates = [datetime.now() - timedelta(hours=bars - i) for i in range(bars)]
    close = [508.0]
    for _ in range(bars - 1):
        close.append(close[-1] * (1 + random.gauss(0.0002, 0.003)))
    opens, highs, lows, closes = [], [], [], []
    for c in close:
        o = c * (1 + random.gauss(0, 0.001))
        h = max(o, c) * (1 + abs(random.gauss(0, 0.001)))
        l = min(o, c) * (1 - abs(random.gauss(0, 0.001)))
        opens.append(o); highs.append(h); lows.append(l); closes.append(c)

    colors = ["#6ecf8a" if closes[i] >= opens[i] else "#ff6b6b" for i in range(bars)]
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=dates,
        open=opens, high=highs, low=lows, close=closes,
        increasing=dict(line=dict(color="#6ecf8a", width=1), fillcolor="#6ecf8a"),
        decreasing=dict(line=dict(color="#ff6b6b", width=1), fillcolor="#ff6b6b"),
        showlegend=False,
        whiskerwidth=0.3,
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#0a0b0f",
        margin=dict(l=0, r=0, t=0, b=0),
        height=240,
        xaxis=dict(
            showgrid=False, rangeslider=dict(visible=False),
            tickfont=dict(size=8, color="#4a5060"), color="#4a5060",
        ),
        yaxis=dict(
            showgrid=True, gridcolor="#1f2129",
            tickfont=dict(size=8, color="#4a5060"),
            tickformat=".2f", zeroline=False,
            side="right",
        ),
        xaxis_rangeslider_visible=False,
    )
    return fig


def _vix_surface() -> go.Figure:
    """VIX volatility surface — heatmap-style."""
    random.seed(11)
    x = np.linspace(1, 30, 15)
    y = np.linspace(10, 25, 10)
    z = [[14.9 + random.gauss(0, 1.5) + 0.05 * xi - 0.1 * yi for xi in x] for yi in y]
    fig = go.Figure(go.Heatmap(
        z=z,
        colorscale=[
            [0.0, "#0a0b0f"],
            [0.3, "#1a2530"],
            [0.6, "#4a3000"],
            [0.8, "#8b5a00"],
            [1.0, "#ffb867"],
        ],
        showscale=False,
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
        height=120,
        xaxis=dict(showticklabels=False, showgrid=False),
        yaxis=dict(showticklabels=False, showgrid=False),
    )
    return fig


def _gld_liquidity() -> go.Figure:
    """GLD liquidity map — bar chart style."""
    random.seed(22)
    hours = list(range(1, 13))
    vols = [random.randint(40, 180) for _ in hours]
    colors = ["#ffb867" if v > 120 else "#4a6080" for v in vols]
    fig = go.Figure(go.Bar(
        x=hours, y=vols,
        marker_color=colors,
        marker_line_width=0,
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
        height=120,
        xaxis=dict(showticklabels=False, showgrid=False),
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        bargap=0.15,
    )
    return fig


def render():
    # ── Page header ───────────────────────────────────────────────────────────
    now_str = datetime.now().strftime("%H:%M:%S")

    # ── 3 hero metric cards ───────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
<div class="market-hero-card">
  <div class="market-hero-corner">NYSE Source: 96</div>
  <div class="market-hero-ticker">EQUITY_INDEX / SPY</div>
  <div class="market-hero-change market-hero-change-pos">▲ +1.245</div>
  <div class="market-hero-value">508.42</div>
  <div class="market-hero-sub">VOL_3090: 42.1M</div>
</div>
""", unsafe_allow_html=True)

    with c2:
        st.markdown("""
<div class="market-hero-card">
  <div class="market-hero-ticker">VOLATILITY / VIX</div>
  <div class="market-hero-change market-hero-change-pos">▲ +4.826</div>
  <div class="market-hero-value">14.92</div>
  <div class="market-hero-sub">FEAR_INDEX_ACTIVE</div>
</div>
""", unsafe_allow_html=True)

    with c3:
        st.markdown("""
<div class="market-hero-card">
  <div class="market-hero-ticker">COMMODITY / GLD</div>
  <div class="market-hero-change market-hero-change-neg">▼ -0.345</div>
  <div class="market-hero-value">201.18</div>
  <div class="market-hero-sub">AU_SPOT_REFERENCE</div>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)

    # ── S&P 500 tactical surveillance (full width chart) ──────────────────────
    st.markdown(f"""
<div class="chart-panel">
  <div class="chart-panel-header">
    <div>
      <div class="chart-panel-title">S&P 500 Tactical Surveillance</div>
      <div class="chart-panel-meta">INTERVAL: 48H CANDLESTICK / REFRESH: LIVE</div>
    </div>
    <div style="display:flex;align-items:center;gap:8px;">
      <div class="interval-btns">
        <div class="interval-btn interval-btn-active">1H</div>
        <div class="interval-btn">4H</div>
        <div class="interval-btn">1D</div>
      </div>
      <span class="live-badge">LIVE</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    spy_chart = _spy_candlestick()
    st.plotly_chart(spy_chart, use_container_width=True, config={"displayModeBar": False})

    st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)

    # ── Bottom: VIX surface + GLD liquidity (side by side) ───────────────────
    v_col, g_col = st.columns(2)

    with v_col:
        st.markdown("""
<div class="chart-panel">
  <div class="chart-panel-header">
    <div class="chart-panel-title">● VIX_VOLATILITY_SURFACE</div>
    <div class="chart-panel-meta">REF_X1_AREA</div>
  </div>
</div>
""", unsafe_allow_html=True)
        st.plotly_chart(_vix_surface(), use_container_width=True, config={"displayModeBar": False})
        st.markdown('<div class="chart-panel-ref">{ AREA_PLOT_LOADED }</div>', unsafe_allow_html=True)

    with g_col:
        st.markdown("""
<div class="chart-panel">
  <div class="chart-panel-header">
    <div class="chart-panel-title">● GLD_LIQUIDITY_MAP</div>
    <div class="chart-panel-meta">REF_X2_AREA</div>
  </div>
</div>
""", unsafe_allow_html=True)
        st.plotly_chart(_gld_liquidity(), use_container_width=True, config={"displayModeBar": False})
        st.markdown('<div class="chart-panel-ref">{ AREA_PLOT_LOADED }</div>', unsafe_allow_html=True)
