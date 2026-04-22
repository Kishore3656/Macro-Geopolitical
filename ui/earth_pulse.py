"""Earth Pulse - GEOMARKET INTELLIGENCE"""

import streamlit as st
from datetime import datetime
import plotly.graph_objects as go
import numpy as np
from api.client import get_client


def _gti_history_chart(history_data: list) -> go.Figure:
    """GTI history sparkline chart from real data."""
    if not history_data:
        return _empty_chart("No GTI history data")

    timestamps = [datetime.fromisoformat(d["timestamp"]) for d in history_data]
    values = [d["gti_score"] * 100 for d in history_data]  # Scale to 0-100

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=timestamps, y=values,
        mode="lines",
        line=dict(color="#ffb867", width=1.5),
        fill="tozeroy",
        fillcolor="rgba(255,184,103,0.06)",
        hovertemplate="%{y:.1f}<extra></extra>",
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
        height=100,
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False, color="#2e3140"),
        yaxis=dict(showgrid=True, gridcolor="#1f2129", showticklabels=True,
                   tickfont=dict(size=8, color="#4a5060"), zeroline=False,
                   tickformat=".0f"),
        showlegend=False,
    )
    return fig


def _empty_chart(message: str) -> go.Figure:
    """Return empty chart with message."""
    fig = go.Figure()
    fig.add_annotation(text=message, x=0.5, y=0.5, showarrow=False)
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=100,
        margin=dict(l=0, r=0, t=0, b=0),
    )
    return fig


def _format_percentage_change(new_val: float, old_val: float) -> str:
    """Format percentage change for display."""
    if old_val == 0:
        return "N/A"
    change = ((new_val - old_val) / old_val) * 100
    symbol = "↑" if change >= 0 else "↓"
    return f"{symbol} {abs(change):.1f}%"


def render():
    client = get_client()

    # Fetch real data
    gti_data = client.get_gti_current()
    gti_history = client.get_gti_history(hours=48)
    headlines_data = client.get_headlines(limit=4)

    if "error" in gti_data:
        st.error(f"API Error: {gti_data['error']}")
        return

    # ── Page header ───────────────────────────────────────────────────────────
    st.markdown("""
<div class="system-status-row">
  <span class="system-status-label">SYSTEM_STATUS: GTI_INDEX</span>
</div>
""", unsafe_allow_html=True)

    # ── 3-column layout ───────────────────────────────────────────────────────
    left, center, right = st.columns([1.2, 2.2, 1.4])

    # ────────────────── LEFT: GTI + Signal Cards ─────────────────────────────
    with left:
        gti_score = gti_data.get("gti_score", 0.0)
        gti_display = gti_score * 100  # Scale to 0-100 for display
        risk_level = gti_data.get("risk_level", "UNKNOWN")

        # GTI Hero
        st.markdown(f"""
<div class="gti-hero-wrapper">
  <div class="gti-hero-number">{gti_display:.1f}</div>
  <div class="gti-hero-meta">
    <span class="gti-hero-badge">{risk_level}</span>
    <span class="gti-hero-change">LIVE_FEED</span>
  </div>
</div>
<div class="gti-hero-feed-label">REAL-TIME_GEOPOLITICAL_FEED</div>
""", unsafe_allow_html=True)

        st.markdown('<div class="section-header" style="margin-top:14px;">SIGNAL COMPONENTS</div>', unsafe_allow_html=True)

        # Conflict score (from conflict_ratio)
        conflict_pct = gti_data.get("conflict_ratio", 0.5) * 100
        conflict_class = "signal-card-elevated" if conflict_pct > 60 else "signal-card"
        st.markdown(f"""
<div class="signal-card {conflict_class}">
  <div class="signal-card-header">
    <span class="signal-card-name">CONFLICT</span>
  </div>
  <div class="signal-card-value">{conflict_pct:.1f}</div>
  <div class="signal-card-desc">GDELT event conflict ratio<br/>from live event stream.</div>
  <div class="signal-bar-wrap"><div class="signal-bar-fill signal-bar-fill-error" style="width:{conflict_pct}%;"></div></div>
</div>
""", unsafe_allow_html=True)

        # Tone index (normalized GDELT AvgTone)
        tone_val = gti_data.get("tone_index", 0.0)
        tone_display = tone_val if tone_val else 50.0  # Default to neutral
        st.markdown(f"""
<div class="signal-card">
  <div class="signal-card-header">
    <span class="signal-card-name">TONE_INDEX</span>
  </div>
  <div class="signal-card-value">{tone_display:.1f}</div>
  <div class="signal-desc signal-card-desc">GDELT media sentiment<br/>from global news analysis.</div>
  <div class="signal-bar-wrap"><div class="signal-bar-fill" style="width:{tone_display}%;"></div></div>
</div>
""", unsafe_allow_html=True)

        # VADER sentiment (from RSS headlines)
        vader_val = gti_data.get("vader_sentiment", 0.5) * 100
        vader_class = "signal-card-stable" if vader_val > 50 else "signal-card"
        st.markdown(f"""
<div class="signal-card {vader_class}">
  <div class="signal-card-header">
    <span class="signal-card-name">VADER_SENTIMENT</span>
  </div>
  <div class="signal-card-value">{vader_val:.1f}</div>
  <div class="signal-card-desc">RSS headline sentiment score<br/>from aggregated news feeds.</div>
  <div class="signal-bar-wrap"><div class="signal-bar-fill signal-bar-fill-green" style="width:{vader_val}%;"></div></div>
</div>
""", unsafe_allow_html=True)

        # Volatility (estimated from GTI)
        vol_badge = "HIGH" if gti_score > 0.6 else "VARIABLE" if gti_score > 0.3 else "LOW"
        vol_color = "signal-card-critical" if vol_badge == "HIGH" else "signal-card"
        st.markdown(f"""
<div class="signal-card {vol_color}">
  <div class="signal-card-header">
    <span class="signal-card-name">VOLATILITY</span>
    <span class="vol-badge vol-badge-{'high' if vol_badge == 'HIGH' else 'low'}">{vol_badge}</span>
  </div>
  <div style="display:flex;gap:4px;margin-top:6px;">
    <div style="flex:1;height:16px;background:#ff2d2d;opacity:{0.9 if gti_score > 0.6 else 0.3};"></div>
    <div style="flex:1;height:16px;background:#ff4d1a;opacity:{0.7 if gti_score > 0.5 else 0.3};"></div>
    <div style="flex:1;height:16px;background:#ff6600;opacity:{0.5 if gti_score > 0.4 else 0.3};"></div>
    <div style="flex:1;height:16px;background:#ff8800;opacity:{0.3 if gti_score > 0.3 else 0.1};"></div>
  </div>
</div>
""", unsafe_allow_html=True)

        st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)

        # Risk legend
        st.markdown("""
<div class="risk-legend">
  <div class="risk-legend-item"><div class="risk-dot risk-dot-critical"></div> HIGH_CONFLICT (60–100)</div>
  <div class="risk-legend-item"><div class="risk-dot risk-dot-elevated"></div> MODERATE_TENSION (30–60)</div>
  <div class="risk-legend-item"><div class="risk-dot risk-dot-stable"></div> LOW_CONFLICT (0–30)</div>
</div>
""", unsafe_allow_html=True)

    # ────────────────── CENTER: Globe + coordinate ───────────────────────────
    with center:
        # Globe using hardcoded hotspots (in production, feed from GDELT events)
        lats_conflict = [50.4, 48.0, 35.7, 15.5, 12.5, 16.9, 33.5, 23.7]
        lons_conflict = [30.5, 37.6, 51.4, 44.2, 42.8, 96.1, 36.3, 90.4]
        sizes_conflict = [20, 15, 18, 12, 10, 14, 16, 11]

        # Color based on GTI risk level
        if gti_score > 0.6:
            colors_conflict = ["#ff2d2d"] * 4 + ["#ffb867"] * 4
        elif gti_score > 0.3:
            colors_conflict = ["#ffb867"] * 8
        else:
            colors_conflict = ["#8a9baa"] * 8

        fig_globe = go.Figure()

        # Globe base
        theta = np.linspace(0, 2 * np.pi, 300)
        phi = np.linspace(0, np.pi, 300)
        x = np.outer(np.sin(phi), np.cos(theta))
        y = np.outer(np.sin(phi), np.sin(theta))
        z = np.outer(np.cos(phi), np.ones(300))

        fig_globe.add_trace(go.Surface(
            x=x, y=y, z=z,
            colorscale=[[0, "#0d1117"], [1, "#1a2030"]],
            showscale=False,
            opacity=0.95,
            lighting=dict(ambient=0.6, diffuse=0.4),
        ))

        # Conflict hotspots
        for lat, lon, sz, col in zip(lats_conflict, lons_conflict, sizes_conflict, colors_conflict):
            lat_r = np.radians(lat)
            lon_r = np.radians(lon)
            cx = np.cos(lat_r) * np.cos(lon_r)
            cy = np.cos(lat_r) * np.sin(lon_r)
            cz = np.sin(lat_r)
            fig_globe.add_trace(go.Scatter3d(
                x=[cx], y=[cy], z=[cz],
                mode="markers",
                marker=dict(size=sz / 3, color=col, opacity=0.9),
                showlegend=False,
                hoverinfo="skip",
            ))

        fig_globe.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            scene=dict(
                bgcolor="rgba(0,0,0,0)",
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                zaxis=dict(visible=False),
                camera=dict(eye=dict(x=1.4, y=0.8, z=0.6)),
                aspectmode="cube",
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            height=320,
        )
        st.plotly_chart(fig_globe, use_container_width=True, config={"displayModeBar": False})

        st.markdown(f"""
<div class="coord-display" style="margin-top:0;">
  <div class="caption-mono">GLOBAL_CONFLICT_HEATMAP | GTI={gti_display:.1f} | {risk_level}</div>
</div>
""", unsafe_allow_html=True)

    # ────────────────── RIGHT: 48H History + Headlines ───────────────────────
    with right:
        st.markdown('<div class="section-header">48H GTI HISTORY</div>', unsafe_allow_html=True)
        history_list = gti_history.get("data", [])
        st.plotly_chart(_gti_history_chart(history_list), use_container_width=True, config={"displayModeBar": False})

        st.markdown('<div class="section-header" style="margin-top:8px;">LATEST HEADLINES</div>', unsafe_allow_html=True)

        headlines_list = headlines_data.get("data", [])
        if not headlines_list:
            st.markdown('<div style="color:#8a9baa;font-size:12px;">No recent headlines</div>', unsafe_allow_html=True)
        else:
            for h in headlines_list[:4]:
                title = h.get("title", "")[:70] + "..." if len(h.get("title", "")) > 70 else h.get("title", "")
                score = h.get("compound_score", 0.0)
                score_cls = "neg" if h.get("sentiment") == "negative" else "pos" if h.get("sentiment") == "positive" else "neu"
                ts = h.get("timestamp", "").split(" ")[1] if " " in h.get("timestamp", "") else "N/A"
                source = h.get("source", "UNKNOWN")[:15]

                cls = "headline-score-neg" if score_cls == "neg" else "headline-score-pos" if score_cls == "pos" else "headline-score-neu"
                st.markdown(f"""
<div class="headline-item">
  <div class="headline-meta">
    <span class="headline-time">{ts}</span>
    <span class="headline-score {cls}">{score:+.2f}</span>
  </div>
  <div class="headline-title">{title}</div>
  <div class="headline-source">{source}</div>
</div>
""", unsafe_allow_html=True)
