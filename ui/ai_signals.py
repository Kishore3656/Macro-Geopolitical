"""AI Signals - Exact Stitch UI design implementation."""

import streamlit as st
import plotly.graph_objects as go
from api.client import get_client


def render():
    client = get_client()
    signals_data = client.get_signals_current()
    signals_history = client.get_signals_history(limit=100)
    gti_data = client.get_gti_current()

    # ── Page title ───────────────────────────────────────────────────────────
    st.markdown("""
<div style="margin-bottom:20px;">
  <h2 style="font-size:32px;margin:0;color:#ffffff;font-family:'Courier New';">AI SIGNALS</h2>
  <p style="font-size:11px;color:#8a9baa;margin:4px 0;">ML_PREDICTION_INTELLIGENCE</p>
</div>
""", unsafe_html=True)

    # ── 3-column layout ───────────────────────────────────────────────────────
    left, center, right = st.columns([1.1, 2.0, 1.2])

    # ────────────────── LEFT: Model Output ────────────────────────────────────
    with left:
        st.markdown('<div style="font-size:11px;color:#8a9baa;font-weight:bold;margin-bottom:8px;">MODEL OUTPUT</div>', unsafe_html=True)

        vol_pred = signals_data.get("vol_prediction", "VARIABLE")
        vol_prob = signals_data.get("vol_prob", 0.5) * 100
        dir_pred = signals_data.get("dir_prediction", "NEUTRAL")
        dir_prob = signals_data.get("dir_prob", 0.5) * 100

        # Volatility section
        st.markdown(f"""
<div style="border:1px solid #2e3140;padding:10px;margin-bottom:12px;background:#0a0b0f;">
  <div style="font-size:9px;color:#8a9baa;">VOLATILITY_PREDICTION</div>
  <div style="font-size:24px;color:#ffb867;font-weight:bold;margin-top:4px;">{vol_pred}</div>
  <div style="font-size:8px;color:#4a5060;margin-top:2px;">Confidence: {vol_prob:.0f}%</div>
</div>
""", unsafe_html=True)

        # Direction section
        dir_color = "#6ecf8a" if dir_pred == "BULLISH" else "#ff6b6b" if dir_pred == "BEARISH" else "#ffb867"
        st.markdown(f"""
<div style="border:1px solid {dir_color};padding:10px;margin-bottom:12px;background:#0a0b0f;">
  <div style="font-size:9px;color:#8a9baa;">DIRECTION_PREDICTION</div>
  <div style="font-size:24px;color:{dir_color};font-weight:bold;margin-top:4px;">{dir_pred}</div>
  <div style="font-size:8px;color:#4a5060;margin-top:2px;">Confidence: {dir_prob:.0f}%</div>
</div>
""", unsafe_html=True)

        # GTI input
        gti_score = gti_data.get("gti_score", 0.5) * 100
        st.markdown(f"""
<div style="border:1px solid #2e3140;padding:8px;background:#0a0b0f;">
  <div style="font-size:9px;color:#8a9baa;margin-bottom:6px;">GTI_INPUT_FEATURES</div>
  <div style="font-size:8px;color:#4a5060;">
    <div style="display:flex;justify-content:space-between;margin:2px 0;"><span>GTI_SCORE</span><span style="color:#ffffff;">{gti_score:.1f}</span></div>
    <div style="display:flex;justify-content:space-between;margin:2px 0;"><span>RETURNS_1H</span><span style="color:#ffffff;">0.42%</span></div>
    <div style="display:flex;justify-content:space-between;margin:2px 0;"><span>VADER_AVG</span><span style="color:#ffffff;">0.12</span></div>
  </div>
</div>
""", unsafe_html=True)

    # ────────────────── CENTER: GTI Component Breakdown ──────────────────────
    with center:
        st.markdown('<div style="font-size:11px;color:#8a9baa;font-weight:bold;margin-bottom:8px;">GTI COMPONENT BREAKDOWN</div>', unsafe_html=True)

        # Chart
        history_list = signals_history.get("data", [])
        if history_list:
            timestamps = [h["timestamp"][:10] for h in history_list[-24:]]
            gti_values = [h.get("gti_score", 0.5) * 100 for h in history_list[-24:]]

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=timestamps, y=gti_values,
                mode="lines",
                line=dict(color="#00ffff", width=2),
                fill="tozeroy",
                fillcolor="rgba(0,255,255,0.1)",
            ))
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="#0a0b0f",
                margin=dict(l=0, r=0, t=0, b=0),
                height=180,
                xaxis=dict(showgrid=False, tickfont=dict(size=7), color="#4a5060"),
                yaxis=dict(showgrid=True, gridcolor="#1f2129", tickfont=dict(size=7), color="#4a5060"),
                showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        st.markdown('<div style="font-size:10px;color:#8a9baa;margin-top:12px;margin-bottom:8px;">FULL_IMPACT FACTORS</div>', unsafe_html=True)

        factors = [
            ("MACRO_VOLATILITY", 0.85),
            ("GEOPOLITICAL_RISK", 0.72),
            ("SENTIMENT_AGGREGATE", 0.68),
            ("LIQUIDITY_DEPTH", 0.54),
        ]

        for factor, weight in factors:
            st.markdown(f"""
<div style="font-size:8px;color:#8a9baa;margin:4px 0;display:flex;justify-content:space-between;">
  <span>{factor}</span>
  <span style="color:#ffffff;font-weight:bold;">{weight:.2f}</span>
</div>
""", unsafe_html=True)

    # ────────────────── RIGHT: Prediction History ────────────────────────────
    with right:
        st.markdown('<div style="font-size:11px;color:#8a9baa;font-weight:bold;margin-bottom:8px;">PREDICTION HISTORY (SIMULATION MODE)</div>', unsafe_html=True)

        if history_list:
            for h in history_list[:8]:
                ts = h.get("timestamp", "N/A")[:10]
                vol = h.get("vol_prediction", "N/A")
                dir_p = h.get("dir_prediction", "N/A")
                vol_c = h.get("vol_prob", 0) * 100
                dir_c = h.get("dir_prob", 0) * 100

                dir_color = "#6ecf8a" if dir_p == "BULLISH" else "#ff6b6b" if dir_p == "BEARISH" else "#ffb867"

                st.markdown(f"""
<div style="border-bottom:1px solid #1f2129;padding:6px 0;margin-bottom:6px;">
  <div style="font-size:8px;color:#4a5060;">{ts}</div>
  <div style="font-size:9px;color:#8a9baa;margin-top:2px;">Vol: <span style="color:#ffffff;">{vol}</span> ({vol_c:.0f}%)</div>
  <div style="font-size:9px;color:#8a9baa;">Dir: <span style="color:{dir_color};">{dir_p}</span> ({dir_c:.0f}%)</div>
</div>
""", unsafe_html=True)
        else:
            st.markdown('<div style="color:#4a5060;font-size:9px;">No prediction history</div>', unsafe_html=True)

        st.markdown('<div style="height:12px;"></div>', unsafe_html=True)

        # Asset impact
        st.markdown('<div style="font-size:10px;color:#8a9baa;font-weight:bold;margin-bottom:8px;">ASSET IMPACT</div>', unsafe_html=True)

        if dir_pred == "BULLISH":
            st.markdown("""
<div style="font-size:8px;color:#6ecf8a;">BULLISH CATALYSTS</div>
<div style="font-size:8px;color:#4a5060;margin-top:4px;">USO, EWZ, FXI, GLD</div>
""", unsafe_html=True)
        elif dir_pred == "BEARISH":
            st.markdown("""
<div style="font-size:8px;color:#ff6b6b;">BEARISH_CATALYSTS</div>
<div style="font-size:8px;color:#4a5060;margin-top:4px;">SHV, VGIT, IEF, TLT</div>
""", unsafe_html=True)
        else:
            st.markdown("""
<div style="font-size:8px;color:#ffb867;">NEUTRAL_POSITIONING</div>
<div style="font-size:8px;color:#4a5060;margin-top:4px;">Monitor for directional clarity</div>
""", unsafe_html=True)
