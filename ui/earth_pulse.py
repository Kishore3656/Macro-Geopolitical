"""Earth Pulse - GEOMARKET INTELLIGENCE"""

import streamlit as st
from datetime import datetime, timedelta
import plotly.graph_objects as go
import numpy as np
import random


def _gti_history_chart() -> go.Figure:
    """48H GTI history sparkline chart."""
    random.seed(42)
    hours = 48
    t = [datetime.now() - timedelta(hours=hours - i) for i in range(hours)]
    base = 24.0
    vals = [base]
    for _ in range(hours - 1):
        vals.append(max(0, min(100, vals[-1] + random.gauss(0.3, 1.2))))

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=t, y=vals,
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


def render():
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
        # GTI Hero
        st.markdown("""
<div class="gti-hero-wrapper">
  <div class="gti-hero-number">26.5</div>
  <div class="gti-hero-meta">
    <span class="gti-hero-badge">LOW_CONFLICT</span>
    <span class="gti-hero-change">-4.2% (24H)</span>
  </div>
</div>
<div class="gti-hero-feed-label">REAL-TIME_GEOPOLITICAL_FEED</div>
""", unsafe_allow_html=True)

        st.markdown('<div class="section-header" style="margin-top:14px;">SIGNAL COMPONENTS</div>', unsafe_allow_html=True)

        # Conflict score
        st.markdown("""
<div class="signal-card signal-card-elevated">
  <div class="signal-card-header">
    <span class="signal-card-name">CONFLICT</span>
  </div>
  <div class="signal-card-value">85.2</div>
  <div class="signal-card-desc">Escalation detected in Sector T-G.<br/>A kinetic energy report sliding.</div>
  <div class="signal-bar-wrap"><div class="signal-bar-fill signal-bar-fill-error" style="width:85.2%;"></div></div>
</div>
""", unsafe_allow_html=True)

        # Tone index
        st.markdown("""
<div class="signal-card">
  <div class="signal-card-header">
    <span class="signal-card-name">TONE_INDEX</span>
  </div>
  <div class="signal-card-value">42.1</div>
  <div class="signal-desc signal-card-desc">Nuclear Diplomatic pulse<br/>deterred by diplomatic talks.</div>
  <div class="signal-bar-wrap"><div class="signal-bar-fill" style="width:42.1%;"></div></div>
</div>
""", unsafe_allow_html=True)

        # VADER sentiment
        st.markdown("""
<div class="signal-card signal-card-stable">
  <div class="signal-card-header">
    <span class="signal-card-name">VADER_SENTIMENT</span>
  </div>
  <div class="signal-card-value">0.46</div>
  <div class="signal-card-desc">Solid sources showing positive<br/>recovery trends.</div>
  <div class="signal-bar-wrap"><div class="signal-bar-fill signal-bar-fill-green" style="width:46%;"></div></div>
</div>
""", unsafe_allow_html=True)

        # Volatility
        st.markdown("""
<div class="signal-card signal-card-critical">
  <div class="signal-card-header">
    <span class="signal-card-name">VOLATILITY</span>
    <span class="vol-badge vol-badge-high">HIGH</span>
  </div>
  <div style="display:flex;gap:4px;margin-top:6px;">
    <div style="flex:1;height:16px;background:#ff2d2d;opacity:0.9;"></div>
    <div style="flex:1;height:16px;background:#ff4d1a;opacity:0.7;"></div>
    <div style="flex:1;height:16px;background:#ff6600;opacity:0.5;"></div>
    <div style="flex:1;height:16px;background:#ff8800;opacity:0.3;"></div>
  </div>
</div>
""", unsafe_allow_html=True)

        st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)

        # Risk legend
        st.markdown("""
<div class="risk-legend">
  <div class="risk-legend-item"><div class="risk-dot risk-dot-critical"></div> CRITICAL_THREAT (75–100)</div>
  <div class="risk-legend-item"><div class="risk-dot risk-dot-elevated"></div> ELEVATED_WATCH (40–74)</div>
  <div class="risk-legend-item"><div class="risk-dot risk-dot-stable"></div> NOMINAL_STABLE (0–39)</div>
</div>
""", unsafe_allow_html=True)

    # ────────────────── CENTER: Globe + coordinate ───────────────────────────
    with center:
        # Simulated globe using a dark sphere with plotly
        lats_conflict = [50.4, 48.0, 35.7, 15.5, 12.5, 16.9, 33.5, 23.7]
        lons_conflict = [30.5, 37.6, 51.4, 44.2, 42.8, 96.1, 36.3, 90.4]
        sizes_conflict = [20, 15, 18, 12, 10, 14, 16, 11]
        colors_conflict = ["#ff2d2d", "#ff2d2d", "#ffb867", "#ffb867", "#8a9baa", "#ffb867", "#ff2d2d", "#8a9baa"]

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

        st.markdown("""
<div class="coord-display" style="margin-top:0;">
  <div class="caption-mono">COORDINATE_USER_ACTIVE_v4</div>
</div>
""", unsafe_allow_html=True)

    # ────────────────── RIGHT: 48H History + Headlines ───────────────────────
    with right:
        st.markdown('<div class="section-header">48H GTI HISTORY</div>', unsafe_allow_html=True)
        st.plotly_chart(_gti_history_chart(), use_container_width=True, config={"displayModeBar": False})

        st.markdown('<div class="section-header" style="margin-top:8px;">LATEST HEADLINES</div>', unsafe_allow_html=True)

        headlines = [
            ("13:09 UTC", "-9.71", "neg",
             "Maritime blockade tightening in southern trade corridors.",
             "SOURCE: AP_REUTERS_108", "CONFIDENCE: 96"),
            ("13:00 UTC", "+8.02", "pos",
             "Bilateral trade agreement signed between Baltic alliance.",
             "SOURCE: REUTERS_411", "CONFIDENCE: 88"),
            ("12:55 UTC", "+8.12", "neg",
             "Energy grid fluctuation reported across central hub.",
             "SOURCE: GDELT_309", "CONFIDENCE: 74"),
            ("12:51 UTC", "-6.08", "neg",
             "Cyber-reconnaissance detected in national bank infrastructure.",
             "SOURCE: CYBER_SRC", "CONFIDENCE: 91"),
        ]

        for time, score, score_cls, title, source1, source2 in headlines:
            cls = "headline-score-neg" if score_cls == "neg" else "headline-score-pos"
            st.markdown(f"""
<div class="headline-item">
  <div class="headline-meta">
    <span class="headline-time">{time}</span>
    <span class="headline-score {cls}">{score}</span>
  </div>
  <div class="headline-title">{title}</div>
  <div class="headline-source">{source1} &nbsp;|&nbsp; {source2}</div>
</div>
""", unsafe_allow_html=True)
