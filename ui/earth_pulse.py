"""Earth Pulse - Exact Stitch UI design implementation."""

import streamlit as st
from datetime import datetime
import plotly.graph_objects as go
import numpy as np
from api.client import get_client


def render():
    client = get_client()

    # Fetch real data
    gti_data = client.get_gti_current()
    gti_history = client.get_gti_history(hours=48)
    headlines_data = client.get_headlines(limit=4)
    events_data = client.get_recent_events(event_type="conflict", limit=8)

    if "error" in gti_data:
        st.error(f"API Error: {gti_data['error']}")
        return

    # ── Page title ───────────────────────────────────────────────────────────
    st.markdown("""
<div style="text-align:center;margin-bottom:20px;">
  <h1 style="font-size:48px;margin:0;color:#ffffff;font-family:'Courier New';">EARTH PULSE</h1>
  <p style="font-size:12px;color:#8a9baa;margin:4px 0;">REAL-TIME_GEOPOLITICAL_ANALYSIS</p>
</div>
""", unsafe_allow_html=True)

    # ── 3-column layout ───────────────────────────────────────────────────────
    left, center, right = st.columns([1.1, 2.0, 1.3])

    gti_score = gti_data.get("gti_score", 0.0)
    gti_display = min(100, gti_score * 100)
    risk_level = gti_data.get("risk_level", "UNKNOWN")

    # ────────────────── LEFT COLUMN ───────────────────────────────────────────
    with left:
        # GTI Hero number
        st.markdown(f"""
<div style="text-align:center;margin-bottom:20px;">
  <div style="font-size:96px;font-weight:bold;color:#ffffff;line-height:1;font-family:'Courier New';">{gti_display:.1f}</div>
  <div style="font-size:11px;color:#8a9baa;margin-top:4px;">Geopolitical Tension Index</div>
  <div style="font-size:9px;color:#ffb867;margin-top:2px;">CURRENT_ASSESSMENT</div>
</div>
""", unsafe_allow_html=True)

        st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)

        # Signal cards
        signal_cards = [
            ("CONFLICT", gti_data.get("conflict_ratio", 0.5) * 100, "GDELT event conflict ratio from live event stream."),
            ("TONE_INDEX", gti_data.get("tone_index", 50.0), "GDELT media sentiment from global news analysis."),
            ("VADER_SENTIMENT", gti_data.get("vader_sentiment", 0.5) * 100, "RSS headline sentiment score from aggregated news feeds."),
            ("VOLATILITY", (gti_score * 100 * 2) if gti_score > 0 else 20, "Market volatility estimate based on GTI."),
        ]

        for name, value, desc in signal_cards:
            color = "#ff2d2d" if value > 70 else "#ffb867" if value > 40 else "#4a6080"
            st.markdown(f"""
<div style="border-left:3px solid {color};padding:8px;margin-bottom:8px;background:#0a0b0f;">
  <div style="font-size:11px;color:#8a9baa;font-weight:bold;">{name}</div>
  <div style="font-size:24px;color:#ffffff;font-weight:bold;">{value:.1f}</div>
  <div style="font-size:8px;color:#4a5060;margin-top:2px;">{desc}</div>
  <div style="width:100%;height:6px;background:#1f2129;margin-top:6px;border-radius:2px;">
    <div style="width:{min(value, 100)}%;height:100%;background:{color};border-radius:2px;"></div>
  </div>
</div>
""", unsafe_allow_html=True)

        st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)

        # Risk legend
        st.markdown("""
<div style="font-size:9px;color:#8a9baa;">
  <div style="margin:4px 0;"><span style="display:inline-block;width:12px;height:12px;background:#ff2d2d;border-radius:2px;margin-right:6px;vertical-align:middle;"></span>CRITICAL (80-100)</div>
  <div style="margin:4px 0;"><span style="display:inline-block;width:12px;height:12px;background:#ffb867;border-radius:2px;margin-right:6px;vertical-align:middle;"></span>ELEVATED (40-80)</div>
  <div style="margin:4px 0;"><span style="display:inline-block;width:12px;height:12px;background:#4a6080;border-radius:2px;margin-right:6px;vertical-align:middle;"></span>STABLE (0-40)</div>
</div>
""", unsafe_allow_html=True)

    # ────────────────── CENTER: Globe ─────────────────────────────────────────
    with center:
        # Fetch real hotspot data
        events_list = events_data.get("data", [])

        if events_list:
            lats = [e.get("latitude", 0) for e in events_list if e.get("latitude") is not None]
            lons = [e.get("longitude", 0) for e in events_list if e.get("longitude") is not None]
            sizes = [min(25, abs(e.get("goldstein_scale", -5)) * 2) for e in events_list]
        else:
            # Fallback hardcoded data
            lats = [50.4, 48.0, 35.7, 15.5, 12.5, 16.9, 33.5, 23.7]
            lons = [30.5, 37.6, 51.4, 44.2, 42.8, 96.1, 36.3, 90.4]
            sizes = [20, 15, 18, 12, 10, 14, 16, 11]

        # Create 3D globe
        fig = go.Figure()

        # Globe surface
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

        # Conflict hotspots
        num_hotspots = len(lats)
        for i, (lat, lon, sz) in enumerate(zip(lats, lons, sizes)):
            lat_r = np.radians(lat)
            lon_r = np.radians(lon)
            cx = np.cos(lat_r) * np.cos(lon_r)
            cy = np.cos(lat_r) * np.sin(lon_r)
            cz = np.sin(lat_r)

            # Color based on intensity
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

        # Coordinate display
        if lats and lons:
            sample_lat, sample_lon = lats[0], lons[0]
            lat_dir = "N" if sample_lat >= 0 else "S"
            lon_dir = "E" if sample_lon >= 0 else "W"
            st.markdown(f"""
<div style="text-align:center;font-size:11px;color:#8a9baa;margin-top:8px;">
  <div style="font-size:14px;color:#ffffff;font-family:'Courier New';">{abs(sample_lat):.4f}° {lat_dir}, {abs(sample_lon):.4f}° {lon_dir}</div>
  <div style="font-size:9px;color:#4a5060;">REGION_CRITICAL_SECTOR</div>
</div>
""", unsafe_allow_html=True)

    # ────────────────── RIGHT: History + Headlines ────────────────────────────
    with right:
        # 48H History chart
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

                sentiment_color = "#ff2d2d" if sentiment == "negative" else "#6ecf8a" if sentiment == "positive" else "#ffb867"

                st.markdown(f"""
<div style="border-bottom:1px solid #1f2129;padding:8px 0;margin-bottom:8px;">
  <div style="font-size:8px;color:#4a5060;margin-bottom:4px;">
    <span>{timestamp}</span>
    <span style="float:right;color:{sentiment_color};">{score:+.2f}</span>
  </div>
  <div style="font-size:10px;color:#d8dae8;line-height:1.3;">{title}</div>
  <div style="font-size:8px;color:#4a5060;margin-top:2px;">{source}</div>
</div>
""", unsafe_allow_html=True)
        else:
            st.markdown('<div style="color:#4a5060;font-size:9px;">No recent headlines</div>', unsafe_allow_html=True)
