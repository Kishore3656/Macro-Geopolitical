"""Geo Map - Exact Stitch UI design implementation."""

import streamlit as st
import plotly.graph_objects as go
from api.client import get_client


def render():
    client = get_client()
    conflicts_data = client.get_conflicts(limit=15)
    bilateral_data = client.get_bilateral_relations(limit=5)
    events_data = client.get_recent_events(event_type="all", limit=50)

    conflicts_list = conflicts_data.get("data", [])
    bilateral_list = bilateral_data.get("data", [])
    events_list = events_data.get("data", [])

    # ── Page title ───────────────────────────────────────────────────────────
    st.markdown("""
<div style="margin-bottom:20px;">
  <h2 style="font-size:32px;margin:0;color:#ffffff;font-family:'Courier New';">GEO MAP</h2>
  <p style="font-size:11px;color:#8a9baa;margin:4px 0;">GEOGRAPHIC_INTELLIGENCE_FEED</p>
</div>
""", unsafe_allow_html=True)

    # ── 3-column layout ───────────────────────────────────────────────────────
    left, center, right = st.columns([1.0, 2.2, 1.2])

    # ────────────────── LEFT COLUMN ───────────────────────────────────────────
    with left:
        # Map legend
        st.markdown("""
<div style="margin-bottom:16px;">
  <div style="font-size:10px;color:#8a9baa;font-weight:bold;margin-bottom:8px;">MAP LEGEND</div>
  <div style="font-size:9px;color:#8a9baa;">
    <div style="margin:4px 0;"><span style="display:inline-block;width:10px;height:10px;background:#ff2d2d;border-radius:50%;margin-right:6px;vertical-align:middle;"></span>Extreme Conflict</div>
    <div style="margin:4px 0;"><span style="display:inline-block;width:10px;height:10px;background:#ffb867;border-radius:50%;margin-right:6px;vertical-align:middle;"></span>Elevated Tension</div>
    <div style="margin:4px 0;"><span style="display:inline-block;width:10px;height:10px;background:#4a6080;border-radius:50%;margin-right:6px;vertical-align:middle;"></span>Stable Region</div>
  </div>
</div>
""", unsafe_allow_html=True)

        # Arc type filter
        st.markdown("""
<div style="margin-bottom:16px;">
  <div style="font-size:10px;color:#8a9baa;font-weight:bold;margin-bottom:8px;">ARC TYPE FILTER</div>
  <div style="display:flex;gap:6px;flex-wrap:wrap;">
    <div style="border:1px solid #ffb867;padding:6px 12px;font-size:9px;color:#ffb867;cursor:pointer;">MILITARY</div>
    <div style="border:1px solid #2e3140;padding:6px 12px;font-size:9px;color:#4a5060;cursor:pointer;">SANCTIONS</div>
    <div style="border:1px solid #2e3140;padding:6px 12px;font-size:9px;color:#4a5060;cursor:pointer;">TRADE</div>
    <div style="border:1px solid #2e3140;padding:6px 12px;font-size:9px;color:#4a5060;cursor:pointer;">DIPLOMATIC</div>
  </div>
</div>
""", unsafe_allow_html=True)

        # Global statistics
        st.markdown("""
<div style="margin-bottom:16px;">
  <div style="font-size:10px;color:#8a9baa;font-weight:bold;margin-bottom:8px;">GLOBAL STATISTICS</div>
  <div style="font-size:9px;color:#8a9baa;">
""", unsafe_allow_html=True)

        active_conflicts = len(conflicts_list)
        st.markdown(f"""
    <div style="display:flex;justify-content:space-between;margin:4px 0;"><span>Active Conflicts</span><span style="color:#ffffff;">{active_conflicts}</span></div>
    <div style="display:flex;justify-content:space-between;margin:4px 0;"><span>POS_SENTIMENT</span><span style="color:#6ecf8a;">14.2%</span></div>
    <div style="display:flex;justify-content:space-between;margin:4px 0;"><span>NEG_SENTIMENT</span><span style="color:#ff2d2d;">68.0%</span></div>
    <div style="display:flex;justify-content:space-between;margin:4px 0;"><span>NEU_STABILITY</span><span style="color:#ffb867;">17.3%</span></div>
  </div>
</div>
""", unsafe_allow_html=True)

    # ────────────────── CENTER: Map ──────────────────────────────────────────
    with center:
        # Build conflict country map
        conflict_countries = {}
        for conflict in conflicts_list[:15]:
            cc = conflict.get("country_code", "")
            if cc:
                conflict_countries[cc] = min(10, conflict.get("severity_score", 0) * 10)

        all_countries = list(conflict_countries.keys()) if conflict_countries else ["RUS", "UKR", "SYR"]
        scores = list(conflict_countries.values()) if conflict_countries else [9.8, 9.5, 8.1]

        fig = go.Figure()
        fig.add_trace(go.Choropleth(
            locations=all_countries,
            z=scores,
            locationmode="ISO-3",
            colorscale=[
                [0.0,  "#0a0b0f"],
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
            ),
            paper_bgcolor="#0a0b0f",
            plot_bgcolor="#0a0b0f",
            margin=dict(l=0, r=0, t=0, b=0),
            height=300,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        # Coordinate display
        st.markdown("""
<div style="text-align:center;font-size:10px;color:#8a9baa;margin-top:8px;padding:8px;border:1px solid #2e3140;">
  <div style="font-size:12px;color:#ffffff;font-family:'Courier New';">55.7558° N, 37.6173° E</div>
  <div style="font-size:8px;color:#4a5060;">REGION_CRITICAL_SECTOR</div>
</div>
""", unsafe_allow_html=True)

        # Headline density chart
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
            font=dict(family="Courier New", size=8, color="#8a9baa"),
            margin=dict(l=0, r=0, t=20, b=0),
            height=100,
            title=dict(text="HEADLINE DENSITY BY STRATEGIC CITY", font=dict(size=9, color="#8a9baa"), x=0),
            xaxis=dict(showgrid=False, tickfont=dict(size=7), color="#4a5060"),
            yaxis=dict(showgrid=True, gridcolor="#1f2129", tickfont=dict(size=7), color="#4a5060"),
            bargap=0.2,
        )
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    # ────────────────── RIGHT: Relations ──────────────────────────────────────
    with right:
        st.markdown('<div style="font-size:11px;color:#8a9baa;font-weight:bold;margin-bottom:8px;">TOP RELATION STRESS</div>', unsafe_allow_html=True)

        if bilateral_list:
            relations_display = bilateral_list[:5]
        else:
            relations_display = [
                {"pair": "US — UA", "stress_level": 9.8},
                {"pair": "CN — TW", "stress_level": 8.4},
                {"pair": "IR — IL", "stress_level": 8.1},
            ]

        for rel in relations_display:
            pair = rel.get("pair", "N/A")
            stress = rel.get("stress_level", 5.0)
            status = "CRITICAL" if stress > 8 else "ELEVATED" if stress > 6 else "STABLE"
            color = "#ff2d2d" if status == "CRITICAL" else "#ffb867" if status == "ELEVATED" else "#6ecf8a"

            st.markdown(f"""
<div style="border:1px solid #2e3140;padding:8px;margin-bottom:8px;background:#0a0b0f;">
  <div style="font-size:10px;color:#ffffff;font-weight:bold;">{pair}</div>
  <div style="font-size:8px;color:#8a9baa;">BILATERAL_RELATION<br/>{status}</div>
  <div style="text-align:right;font-size:14px;color:{color};font-weight:bold;margin-top:4px;">{stress:.1f}</div>
</div>
""", unsafe_allow_html=True)

        st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)

        # Reliability score
        st.markdown("""
<div style="border:1px solid #ffb867;padding:12px;text-align:center;">
  <div style="font-size:10px;color:#8a9baa;margin-bottom:4px;">RELIABILITY_SCORE</div>
  <div style="font-size:28px;color:#ffffff;font-weight:bold;">8.9+</div>
  <div style="font-size:8px;color:#4a5060;margin-top:4px;">Algorithmic synthesis suggests escalation probability in high-tension zones within 72 hours.</div>
</div>
""", unsafe_html=True)

        st.markdown('<div style="height:8px;"></div>', unsafe_home="True)

        # Status badges
        st.markdown("""
<div style="display:flex;gap:6px;flex-wrap:wrap;">
  <div style="border:1px solid #4a5060;padding:4px 8px;font-size:8px;color:#8a9baa;border-radius:2px;">SYSTEM_STABLE</div>
  <div style="border:1px solid #4a5060;padding:4px 8px;font-size:8px;color:#8a9baa;border-radius:2px;">ENCRYPTION_AES256</div>
  <div style="border:1px solid #ffb867;padding:4px 8px;font-size:8px;color:#ffb867;border-radius:2px;">LATENCY_12MS</div>
</div>
""", unsafe_html=True)
