"""Earth Pulse - Real-time geopolitical intelligence analysis."""

import streamlit as st
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
from api.client import get_client


def render():
    client = get_client()
    gti_data = client.get_gti_current()
    gti_history = client.get_gti_history(hours=48)
    headlines_data = client.get_headlines(limit=4)
    events_data = client.get_recent_events(event_type="conflict", limit=8)

    gti_score = gti_data.get("gti_score", 0.0)
    gti_display = min(100, gti_score * 100)

    col_left, col_center, col_right = st.columns([1.1, 2.0, 1.3])

    # ── LEFT COLUMN: GTI HERO + SIGNAL CARDS ──────────────────────────────────
    with col_left:
        st.markdown(f"""
<div class="gti-hero-wrapper">
  <div class="gti-hero-number">{gti_display:.1f}</div>
  <div class="gti-hero-meta">
    <div class="gti-hero-badge">CURRENT_ASSESSMENT</div>
    <div class="gti-hero-feed-label">Geopolitical Tension Index</div>
  </div>
</div>
""", unsafe_allow_html=True)

        signal_cards = [
            ("CONFLICT", gti_data.get("conflict_ratio", 0.5) * 100, "GDELT event conflict ratio from live event stream."),
            ("TONE_INDEX", gti_data.get("tone_index", 50.0), "GDELT media sentiment from global news analysis."),
            ("VADER_SENTIMENT", gti_data.get("vader_sentiment", 0.5) * 100, "RSS headline sentiment score from aggregated news feeds."),
            ("VOLATILITY", (gti_score * 100 * 2) if gti_score > 0 else 20, "Market volatility estimate based on GTI."),
        ]

        for name, value, desc in signal_cards:
            if value > 70:
                card_cls = "signal-card-critical"
                bar_cls = "signal-bar-fill-error"
            elif value > 40:
                card_cls = "signal-card-elevated"
                bar_cls = "signal-bar-fill"
            else:
                card_cls = "signal-card-stable"
                bar_cls = "signal-bar-fill-green"

            st.markdown(f"""
<div class="signal-card {card_cls}">
  <div class="signal-card-name">{name}</div>
  <div class="signal-card-value">{value:.1f}</div>
  <div class="signal-card-desc">{desc}</div>
  <div class="signal-bar-wrap">
    <div class="signal-bar-fill {bar_cls}" style="width: {min(value, 100)}%"></div>
  </div>
</div>
""", unsafe_allow_html=True)

        st.markdown("""
<div class="risk-legend">
  <div class="risk-legend-item">
    <div class="risk-dot risk-dot-critical"></div> CRITICAL (80-100)
  </div>
  <div class="risk-legend-item">
    <div class="risk-dot risk-dot-elevated"></div> ELEVATED (40-80)
  </div>
  <div class="risk-legend-item">
    <div class="risk-dot risk-dot-stable"></div> STABLE (0-40)
  </div>
</div>
""", unsafe_allow_html=True)

    # ── CENTER COLUMN: 3D GLOBE ───────────────────────────────────────────────
    with col_center:
        events_list = events_data.get("data", [])

        if events_list:
            lats = [e.get("latitude", 0) for e in events_list if e.get("latitude") is not None]
            lons = [e.get("longitude", 0) for e in events_list if e.get("longitude") is not None]
            sizes = [min(25, abs(e.get("goldstein_scale", -5)) * 2) for e in events_list]
        else:
            lats = [50.4, 48.0, 35.7, 15.5, 12.5, 16.9, 33.5, 23.7]
            lons = [30.5, 37.6, 51.4, 44.2, 42.8, 96.1, 36.3, 90.4]
            sizes = [20, 15, 18, 12, 10, 14, 16, 11]

        fig = go.Figure()

        theta = np.linspace(0, 2 * np.pi, 300)
        phi = np.linspace(0, np.pi, 300)
        x = np.outer(np.sin(phi), np.cos(theta))
        y = np.outer(np.sin(phi), np.sin(theta))
        z = np.outer(np.cos(phi), np.ones(300))

        fig.add_trace(go.Surface(
            x=x, y=y, z=z,
            colorscale=[[0, "#0d1117"], [1, "#1a2030"]],
            showscale=False,
            opacity=0.95,
        ))

        num_hotspots = len(lats)
        for i, (lat, lon, sz) in enumerate(zip(lats, lons, sizes)):
            lat_r = np.radians(lat)
            lon_r = np.radians(lon)
            cx = np.cos(lat_r) * np.cos(lon_r)
            cy = np.cos(lat_r) * np.sin(lon_r)
            cz = np.sin(lat_r)

            intensity = (i + 1) / num_hotspots
            color = "#ff2d2d" if intensity > 0.6 else "#ffb867"

            fig.add_trace(go.Scatter3d(
                x=[cx], y=[cy], z=[cz],
                mode="markers",
                marker=dict(size=sz / 2.5, color=color, opacity=0.9),
                showlegend=False,
                hoverinfo="skip",
            ))

        fig.update_layout(
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
            height=340,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        if lats and lons:
            sample_lat, sample_lon = lats[0], lons[0]
            lat_dir = "N" if sample_lat >= 0 else "S"
            lon_dir = "E" if sample_lon >= 0 else "W"
            st.markdown(f"""
<div class="coord-display">
  <div class="coord-value">{abs(sample_lat):.4f}° {lat_dir}, {abs(sample_lon):.4f}° {lon_dir}</div>
  <div class="coord-label">REGION_CRITICAL_SECTOR</div>
</div>
""", unsafe_allow_html=True)

    # ── RIGHT COLUMN: HISTORY + HEADLINES ──────────────────────────────────────
    with col_right:
        st.markdown('<div style="font-size:11px;color:#8a9baa;margin-bottom:8px;">48H GTI HISTORY</div>', unsafe_allow_html=True)

        history_list = gti_history.get("data", [])
        if history_list:
            timestamps = [datetime.fromisoformat(d["timestamp"]) for d in history_list]
            values = [d["gti_score"] * 100 for d in history_list]

            fig_history = go.Figure()
            fig_history.add_trace(go.Scatter(
                x=timestamps, y=values,
                mode="lines",
                line=dict(color="#ffb867", width=2),
                fill="tozeroy",
                fillcolor="rgba(255,184,103,0.1)",
                hovertemplate="%{y:.0f}<extra></extra>",
            ))
            fig_history.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=0, t=0, b=0),
                height=90,
                xaxis=dict(showgrid=False, showticklabels=False, color="#2e3140"),
                yaxis=dict(showgrid=True, gridcolor="#1f2129", tickfont=dict(size=8, color="#4a5060")),
                showlegend=False,
            )
            st.plotly_chart(fig_history, use_container_width=True, config={"displayModeBar": False})

        st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:11px;color:#8a9baa;margin-bottom:8px;">LATEST HEADLINES</div>', unsafe_allow_html=True)

        headlines_list = headlines_data.get("data", [])
        if headlines_list:
            for h in headlines_list[:3]:
                title = h.get("title", "")[:80]
                timestamp = h.get("timestamp", "").split(" ")[1] if " " in h.get("timestamp", "") else "N/A"
                sentiment = h.get("sentiment", "neutral")
                score = h.get("compound_score", 0.0)
                source = h.get("source", "UNKNOWN")[:12]

                sentiment_color_cls = "headline-score-neg" if sentiment == "negative" else "headline-score-pos" if sentiment == "positive" else ""

                st.markdown(f"""
<div class="headline-item">
  <div class="headline-meta">
    <div class="headline-time">{timestamp}</div>
    <div class="headline-score {sentiment_color_cls}">{score:+.2f}</div>
  </div>
  <div class="headline-title">{title}</div>
  <div class="headline-source">{source}</div>
</div>
""", unsafe_allow_html=True)
