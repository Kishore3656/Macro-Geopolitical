"""Market - GEOMARKET INTELLIGENCE"""

import streamlit as st
from datetime import datetime
import plotly.graph_objects as go
import numpy as np
import random
from api.client import get_client


def _spy_candlestick(market_data: dict) -> go.Figure:
    """S&P 500 candlestick chart from real market data."""
    bars = market_data.get("data", [])
    if not bars or len(bars) < 2:
        fig = go.Figure()
        fig.add_annotation(text="No market data available", x=0.5, y=0.5, showarrow=False)
        fig.update_layout(height=240, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        return fig

    dates = [datetime.fromisoformat(b["timestamp"]) for b in bars[-40:]]
    opens = [b["open"] for b in bars[-40:]]
    highs = [b["high"] for b in bars[-40:]]
    lows = [b["low"] for b in bars[-40:]]
    closes = [b["close"] for b in bars[-40:]]

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
    client = get_client()

    # Fetch real market data
    market_spy = client.get_market_spy(bars=100)
    market_sectors = client.get_market_sectors()

    # ── Page header ───────────────────────────────────────────────────────────
    now_str = datetime.now().strftime("%H:%M:%S")

    # Get SPY info
    spy_price = market_spy.get("current_price", 0)
    spy_change = market_spy.get("daily_change", 0)
    spy_change_cls = "market-hero-change-pos" if spy_change >= 0 else "market-hero-change-neg"
    spy_arrow = "▲" if spy_change >= 0 else "▼"

    # ── 3 hero metric cards ───────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
<div class="market-hero-card">
  <div class="market-hero-corner">LIVE DATA: ACTIVE</div>
  <div class="market-hero-ticker">EQUITY_INDEX / SPY</div>
  <div class="market-hero-change {spy_change_cls}">{spy_arrow} {abs(spy_change):+.3f}%</div>
  <div class="market-hero-value">${spy_price:.2f}</div>
  <div class="market-hero-sub">PRICE_LIVE_FEED</div>
</div>
""", unsafe_allow_html=True)

    # Get top sector
    sectors = market_sectors.get("sectors", [])
    top_sector = max(sectors, key=lambda s: s["change"]) if sectors else {"name": "N/A", "change": 0, "price": 0}
    top_change_cls = "market-hero-change-pos" if top_sector["change"] >= 0 else "market-hero-change-neg"
    top_arrow = "▲" if top_sector["change"] >= 0 else "▼"

    with c2:
        st.markdown(f"""
<div class="market-hero-card">
  <div class="market-hero-ticker">TOP_SECTOR / {top_sector['name'].upper()}</div>
  <div class="market-hero-change {top_change_cls}">{top_arrow} {abs(top_sector['change']):+.3f}%</div>
  <div class="market-hero-value">${top_sector['price']:.2f}</div>
  <div class="market-hero-sub">SECTOR_PERFORMANCE</div>
</div>
""", unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
<div class="market-hero-card">
  <div class="market-hero-ticker">MARKET_VOLATILITY / EST</div>
  <div class="market-hero-change market-hero-change-pos">DYNAMIC</div>
  <div class="market-hero-value">{spy_change * 2:.2f}%</div>
  <div class="market-hero-sub">ESTIMATED_VIX</div>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)

    # ── S&P 500 tactical surveillance (full width chart) ──────────────────────
    st.markdown(f"""
<div class="chart-panel">
  <div class="chart-panel-header">
    <div>
      <div class="chart-panel-title">S&P 500 Tactical Surveillance</div>
      <div class="chart-panel-meta">INTERVAL: HOURLY CANDLESTICK / REFRESH: LIVE | {now_str}</div>
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

    spy_chart = _spy_candlestick(market_spy)
    st.plotly_chart(spy_chart, use_container_width=True, config={"displayModeBar": False})

    st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)

    # ── Sector performance table ──────────────────────────────────────────────
    st.markdown("""
<div class="chart-panel">
  <div class="chart-panel-header">
    <div class="chart-panel-title">● SECTOR_PERFORMANCE_GRID</div>
    <div class="chart-panel-meta">ALL_11_SECTORS | UPDATED LIVE</div>
  </div>
</div>
""", unsafe_allow_html=True)

    # Render sectors as grid
    sector_cols = st.columns(5)
    for i, sector in enumerate(sectors):
        col = sector_cols[i % 5]
        change_cls = "positive" if sector["change"] >= 0 else "negative"
        with col:
            st.markdown(f"""
<div style="border:1px solid #2e3140;padding:8px;border-radius:4px;text-align:center;margin:4px;background:#0a0b0f;">
  <div style="font-size:11px;color:#8a9baa;">{sector['name']}</div>
  <div style="font-size:14px;color:#d8dae8;font-weight:bold;">${sector['price']:.2f}</div>
  <div style="font-size:12px;color:{'#6ecf8a' if sector['change'] >= 0 else '#ff6b6b'};">{sector['change']:+.2f}%</div>
</div>
""", unsafe_allow_html=True)
