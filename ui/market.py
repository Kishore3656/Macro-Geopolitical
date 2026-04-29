"""Market - Exact Stitch UI design implementation."""

import streamlit as st
import plotly.graph_objects as go
from api.client import get_client
from datetime import datetime


def render():
    client = get_client()
    market_spy = client.get_market_spy(bars=100)
    market_sectors = client.get_market_sectors()

    # ── Page title ───────────────────────────────────────────────────────────
    st.markdown("""
<div style="margin-bottom:20px;">
  <h2 style="font-size:32px;margin:0;color:#ffffff;font-family:'Courier New';">MARKET</h2>
  <p style="font-size:11px;color:#8a9baa;margin:4px 0;">EQUITY_INTELLIGENCE_FEED</p>
</div>
""", unsafe_html=True)

    # ── Hero cards ──────────────────────────────────────────────────────────
    spy_price = market_spy.get("current_price", 0)
    spy_change = market_spy.get("daily_change", 0)
    spy_change_cls = "pos" if spy_change >= 0 else "neg"
    spy_arrow = "▲" if spy_change >= 0 else "▼"

    sectors = market_sectors.get("sectors", [])
    top_sector = max(sectors, key=lambda s: s["change"]) if sectors else {"name": "N/A", "change": 0, "price": 0}

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
<div style="border:1px solid #2e3140;padding:12px;background:#0a0b0f;text-align:center;">
  <div style="font-size:10px;color:#ffb867;">EQUITY_INDEX / SPY</div>
  <div style="font-size:28px;color:#ffffff;font-weight:bold;margin:6px 0;">${spy_price:.2f}</div>
  <div style="font-size:12px;color:{'#6ecf8a' if spy_change >= 0 else '#ff6b6b'};font-weight:bold;">{spy_arrow} {abs(spy_change):+.3f}%</div>
  <div style="font-size:8px;color:#4a5060;margin-top:4px;">PRICE_LIVE_FEED</div>
</div>
""", unsafe_html=True)

    with col2:
        st.markdown(f"""
<div style="border:1px solid #2e3140;padding:12px;background:#0a0b0f;text-align:center;">
  <div style="font-size:10px;color:#ffb867;">MARKET_VOLATILITY / EST</div>
  <div style="font-size:28px;color:#ffffff;font-weight:bold;margin:6px 0;">{abs(spy_change * 2):.2f}%</div>
  <div style="font-size:12px;color:#ffb867;font-weight:bold;">DYNAMIC</div>
  <div style="font-size:8px;color:#4a5060;margin-top:4px;">ESTIMATED_VIX</div>
</div>
""", unsafe_html=True)

    with col3:
        st.markdown(f"""
<div style="border:1px solid #2e3140;padding:12px;background:#0a0b0f;text-align:center;">
  <div style="font-size:10px;color:#ffb867;">TOP_SECTOR / {top_sector['name'].upper()}</div>
  <div style="font-size:28px;color:#ffffff;font-weight:bold;margin:6px 0;">${top_sector['price']:.2f}</div>
  <div style="font-size:12px;color:{'#6ecf8a' if top_sector['change'] >= 0 else '#ff6b6b'};font-weight:bold;">{'▲' if top_sector['change'] >= 0 else '▼'} {abs(top_sector['change']):+.3f}%</div>
  <div style="font-size:8px;color:#4a5060;margin-top:4px;">SECTOR_PERFORMANCE</div>
</div>
""", unsafe_html=True)

    st.markdown('<div style="height:16px;"></div>', unsafe_html=True)

    # ── SPY Candlestick Chart ───────────────────────────────────────────────
    st.markdown("""
<div style="font-size:11px;color:#8a9baa;font-weight:bold;margin-bottom:8px;display:flex;justify-content:space-between;">
  <span>S&P 500 TACTICAL SURVEILLANCE</span>
  <span style="font-size:9px;color:#4a5060;">HOURLY_CANDLESTICK | REFRESH_LIVE</span>
</div>
""", unsafe_html=True)

    bars = market_spy.get("data", [])
    if bars and len(bars) >= 2:
        dates = [datetime.fromisoformat(b["timestamp"]).strftime("%Y-%m-%d") for b in bars[-40:]]
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
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#0a0b0f",
            margin=dict(l=0, r=0, t=0, b=0),
            height=240,
            xaxis=dict(showgrid=False, rangeslider=dict(visible=False), tickfont=dict(size=8, color="#4a5060")),
            yaxis=dict(showgrid=True, gridcolor="#1f2129", tickfont=dict(size=8, color="#4a5060"), side="right"),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.markdown('<div style="text-align:center;color:#4a5060;padding:40px;font-size:12px;">Initializing market data...</div>', unsafe_html=True)

    st.markdown('<div style="height:12px;"></div>', unsafe_html=True)

    # ── VIX and GLD Panels ──────────────────────────────────────────────────
    col_vix, col_gld = st.columns(2)

    with col_vix:
        st.markdown('<div style="font-size:10px;color:#8a9baa;font-weight:bold;margin-bottom:8px;">● VIX_VOLATILITY_SURFACE</div>', unsafe_html=True)
        st.markdown("""
<div style="border:1px solid #2e3140;padding:40px;text-align:center;background:#0a0b0f;height:140px;display:flex;align-items:center;justify-content:center;">
  <div style="font-size:11px;color:#4a5060;">awaiting_market_initialization</div>
</div>
""", unsafe_html=True)

    with col_gld:
        st.markdown('<div style="font-size:10px;color:#8a9baa;font-weight:bold;margin-bottom:8px;">● GLD_LIQUIDITY_MAP</div>', unsafe_html=True)
        st.markdown("""
<div style="border:1px solid #2e3140;padding:40px;text-align:center;background:#0a0b0f;height:140px;display:flex;align-items:center;justify-content:center;">
  <div style="font-size:11px;color:#4a5060;">awaiting_market_initialization</div>
</div>
""", unsafe_html=True)

    st.markdown('<div style="height:16px;"></div>', unsafe_html=True)

    # ── Sector Performance Grid ────────────────────────────────────────────
    st.markdown("""
<div style="font-size:11px;color:#8a9baa;font-weight:bold;margin-bottom:8px;">● SECTOR_PERFORMANCE_GRID</div>
<div style="font-size:9px;color:#4a5060;margin-bottom:12px;">ALL_11_SECTORS | UPDATED LIVE</div>
""", unsafe_html=True)

    sector_cols = st.columns(5)
    for i, sector in enumerate(sectors):
        col = sector_cols[i % 5]
        color = "#6ecf8a" if sector["change"] >= 0 else "#ff6b6b"
        with col:
            st.markdown(f"""
<div style="border:1px solid #2e3140;padding:10px;background:#0a0b0f;text-align:center;margin:4px;">
  <div style="font-size:9px;color:#8a9baa;margin-bottom:4px;">{sector['name']}</div>
  <div style="font-size:14px;color:#ffffff;font-weight:bold;">${sector['price']:.2f}</div>
  <div style="font-size:11px;color:{color};font-weight:bold;">{sector['change']:+.2f}%</div>
</div>
""", unsafe_html=True)
