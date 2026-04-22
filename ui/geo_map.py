"""Geo Map - GEOMARKET INTELLIGENCE"""

import streamlit as st
from datetime import datetime
import plotly.graph_objects as go
import numpy as np


def _make_bar_html(pct: float, css_class: str = "") -> str:
    return f"""
<div class="signal-bar-wrap">
  <div class="signal-bar-fill {css_class}" style="width:{min(pct,100):.1f}%;"></div>
</div>"""


def render():
    # ── Page header ───────────────────────────────────────────────────────────
    st.markdown("""
<div class="system-status-row">
  <span class="system-status-label">SYSTEM_STATUS: GTI_INDEX</span>
</div>
<div class="page-title-row">
  <span class="page-title">GEO MAP</span>
</div>
<div class="page-subtitle">GEOGRAPHIC INTELLIGENCE FEED</div>
""", unsafe_allow_html=True)

    # ── 3-column layout: left panel | map | right panel ──────────────────────
    left, center, right = st.columns([1.1, 2.5, 1.3])

    # ────────────────── LEFT PANEL ───────────────────────────────────────────
    with left:
        # Map legend
        st.markdown('<div class="map-legend">', unsafe_allow_html=True)
        st.markdown('<div class="map-legend-title">MAP LEGEND</div>', unsafe_allow_html=True)
        st.markdown("""
<div class="map-legend-item">
  <div class="legend-dot legend-dot-extreme"></div> Extreme Conflict
</div>
<div class="map-legend-item">
  <div class="legend-dot legend-dot-elevated"></div> Elevated Tension
</div>
<div class="map-legend-item">
  <div class="legend-dot legend-dot-stable"></div> Stable Region
</div>
""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)

        # Arc type filter
        st.markdown('<div class="section-header">ARC TYPE FILTER</div>', unsafe_allow_html=True)
        st.markdown("""
<div class="filter-group">
  <div class="filter-chip filter-chip-active">MILITARY</div>
  <div class="filter-chip">SANCTIONS</div>
  <div class="filter-chip">TRADE</div>
</div>
<div class="filter-group">
  <div class="filter-chip">DIPLOMATIC</div>
</div>
""", unsafe_allow_html=True)

        st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)

        # Global statistics
        st.markdown('<div class="section-header">GLOBAL STATISTICS</div>', unsafe_allow_html=True)
        stats = [
            ("Active Conflicts", "42"),
            ("METRIC", "VALUE"),
            ("POS_SENTIMENT", "14.2%"),
            ("NEG_SENTIMENT", "68.0%"),
            ("NEU_STABILITY", "17.3%"),
        ]
        for i, (label, value) in enumerate(stats):
            if i == 1:
                st.markdown(f"""
<div class="global-stat-row" style="opacity:0.5;">
  <span class="global-stat-label">{label}</span>
  <span class="global-stat-value">{value}</span>
</div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
<div class="global-stat-row">
  <span class="global-stat-label">{label}</span>
  <span class="global-stat-value">{value}</span>
</div>""", unsafe_allow_html=True)

    # ────────────────── CENTER: MAP ──────────────────────────────────────────
    with center:
        # World choropleth with conflict overlays
        conflict_countries = {
            "RUS": 9.8, "UKR": 9.5, "SYR": 8.1, "YEM": 7.2,
            "SDN": 6.5, "MMR": 7.0, "ETH": 6.2, "IRQ": 5.9,
            "LBY": 5.5, "MLI": 5.8, "AFG": 8.9, "PAK": 5.2,
            "IRN": 7.1, "SAU": 4.8, "TWN": 6.0,
        }
        all_countries = list(conflict_countries.keys())
        scores = list(conflict_countries.values())

        fig = go.Figure()
        fig.add_trace(go.Choropleth(
            locations=all_countries,
            z=scores,
            locationmode="ISO-3",
            colorscale=[
                [0.0,  "#0e1017"],
                [0.3,  "#1f2535"],
                [0.55, "#4a2d00"],
                [0.75, "#8b4800"],
                [0.9,  "#cc6600"],
                [1.0,  "#ff2d2d"],
            ],
            zmin=0, zmax=10,
            showscale=False,
            marker_line_color="#2e3140",
            marker_line_width=0.5,
        ))

        # Arc lines for conflict arcs (simplified as annotations)
        arc_pairs = [
            ("RUS", "UKR", 55.0, 37.0, 48.5, 32.0),
            ("IRN", "ISR", 32.0, 53.0, 31.5, 34.8),
            ("CHN", "TWN", 35.0, 105.0, 23.5, 121.0),
            ("SAU", "YEM", 23.5, 45.5, 15.5, 44.0),
        ]

        fig.update_layout(
            geo=dict(
                showframe=False,
                showcoastlines=True,
                coastlinecolor="#2e3140",
                showland=True,
                landcolor="#13151d",
                showocean=True,
                oceancolor="#0a0b0f",
                showlakes=False,
                showcountries=True,
                countrycolor="#2e3140",
                countrywidth=0.5,
                bgcolor="#0a0b0f",
                projection_type="natural earth",
            ),
            paper_bgcolor="#0a0b0f",
            plot_bgcolor="#0a0b0f",
            margin=dict(l=0, r=0, t=0, b=0),
            height=350,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        # Coordinate / focus display
        st.markdown("""
<div class="coord-display">
  <div class="coord-value">55.7558° N, 37.6173° E</div>
  <div class="coord-label">REGION_CRITICAL_SECTOR</div>
</div>
""", unsafe_allow_html=True)

        st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)

        # Headline density chart (bar chart)
        cities = ["Moscow", "Kyiv", "Tehran", "Beijing", "Riyadh", "Kabul", "Damascus", "Aden"]
        density = [42, 38, 29, 25, 18, 22, 31, 14]

        fig2 = go.Figure(go.Bar(
            x=cities, y=density,
            marker_color=["#ff2d2d" if d > 35 else "#ffb867" if d > 20 else "#4a6080" for d in density],
            marker_line_width=0,
        ))
        fig2.update_layout(
            paper_bgcolor="#0a0b0f",
            plot_bgcolor="#13151d",
            font=dict(family="JetBrains Mono", size=9, color="#8a9baa"),
            margin=dict(l=0, r=0, t=24, b=0),
            height=110,
            title=dict(text="HEADLINE DENSITY BY STRATEGIC CITY", font=dict(size=9, color="#8a9baa"), x=0),
            xaxis=dict(showgrid=False, tickfont=dict(size=8), color="#4a5060"),
            yaxis=dict(showgrid=True, gridcolor="#1f2129", tickfont=dict(size=8), color="#4a5060"),
            bargap=0.2,
        )
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

        st.markdown('<div class="caption-mono" style="text-align:right;">LINE_FEED_SYNCED</div>', unsafe_allow_html=True)

    # ────────────────── RIGHT PANEL ──────────────────────────────────────────
    with right:
        st.markdown('<div class="section-header">TOP RELATION STRESS</div>', unsafe_allow_html=True)

        relations = [
            ("US — UA",           "KINSHIP_ENGAGEMENT", "OPTIMAL",   None,    9.8,  "ok"),
            ("CN — TW",           "NAVAL_PROXIMITY",    "ELEVATED",  None,    8.4,  "warn"),
            ("IR — IL",           "PROXY_SECURITY",     "CRITICAL",  None,    8.1,  "bad"),
            ("US — CN",           "TRADE_SANCTIONS",    "MONITORED", None,    7.2,  "warn"),
            ("SA — YE",           "CEASEFIRE_STATUS",   "MONITORED", None,    5.1,  "ok"),
        ]

        for pair, label, status, _, score, tier in relations:
            score_cls = "relation-score" if tier == "bad" else ("relation-score relation-score-warn" if tier == "warn" else "relation-score relation-score-ok")
            st.markdown(f"""
<div class="relation-item">
  <div>
    <div class="relation-pair">{pair}</div>
    <div class="relation-status">{label}<br/>{status}</div>
  </div>
  <div class="{score_cls}">{score}</div>
</div>""", unsafe_allow_html=True)

        st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)

        # Reliability score
        st.markdown("""
<div class="reliability-box">
  <div class="reliability-label">RELIABILITY_SCORE</div>
  <div class="reliability-value">8.9+</div>
  <div class="reliability-desc">
    "Algorithmic synthesis suggests 12% probability<br/>
    of escalation in South China Sea within 72<br/>
    hours."
  </div>
</div>
""", unsafe_allow_html=True)

        st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)

        # Status badges
        st.markdown("""
<div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:4px;">
  <span class="vol-badge vol-badge-low" style="font-size:8px;">SYSTEM_STABLE</span>
  <span class="vol-badge vol-badge-low" style="font-size:8px;">ENCRYPTION_AES256</span>
  <span class="gti-badge" style="font-size:8px;padding:2px 6px;">LATENCY_12MS</span>
</div>
""", unsafe_allow_html=True)
