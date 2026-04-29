"""AI Signals - ML prediction intelligence."""

import streamlit as st
import plotly.graph_objects as go
from api.client import get_client


def render():
    client = get_client()
    signals_data = client.get_signals_current()
    signals_history = client.get_signals_history(limit=100)
    gti_data = client.get_gti_current()

    vol_pred = signals_data.get("vol_prediction", "VARIABLE")
    vol_prob = signals_data.get("vol_prob", 0.5) * 100
    dir_pred = signals_data.get("dir_prediction", "NEUTRAL")
    dir_prob = signals_data.get("dir_prob", 0.5) * 100

    col_left, col_center, col_right = st.columns([1.1, 2.0, 1.2])

    # ── LEFT: MODEL OUTPUT ───────────────────────────────────────────────────
    with col_left:
        st.markdown('<div style="font-size:11px;color:#8a9baa;font-weight:bold;margin-bottom:8px;">MODEL OUTPUT</div>', unsafe_allow_html=True)

        st.markdown(f"""
<div class="model-output-panel">
  <div class="model-output-title">VOLATILITY_PREDICTION</div>
  <div class="model-volatility">{vol_pred}</div>
  <div class="model-vol-label">Confidence: {vol_prob:.0f}%</div>
</div>
""", unsafe_allow_html=True)

        dir_color = "#6ecf8a" if dir_pred == "BULLISH" else "#ff6b6b" if dir_pred == "BEARISH" else "#ffb867"
        st.markdown(f"""
<div class="model-output-panel" style="border-color:{dir_color};">
  <div class="model-output-title">DIRECTION_PREDICTION</div>
  <div style="font-size:24px;color:{dir_color};font-weight:bold;margin-top:4px;">{dir_pred}</div>
  <div class="model-confidence">Confidence: {dir_prob:.0f}%</div>
</div>
""", unsafe_allow_html=True)

        gti_score = gti_data.get("gti_score", 0.5) * 100
        st.markdown(f"""
<div class="model-output-panel">
  <div class="model-output-title">GTI_INPUT_FEATURES</div>
  <div class="feature-row">
    <div class="feature-name">GTI_SCORE</div>
    <div class="feature-value">{gti_score:.1f}</div>
  </div>
  <div class="feature-row">
    <div class="feature-name">RETURNS_1H</div>
    <div class="feature-value">0.42%</div>
  </div>
  <div class="feature-row">
    <div class="feature-name">VADER_AVG</div>
    <div class="feature-value">0.12</div>
  </div>
</div>
""", unsafe_allow_html=True)

    # ── CENTER: GTI COMPONENT BREAKDOWN ──────────────────────────────────────
    with col_center:
        st.markdown('<div style="font-size:11px;color:#8a9baa;font-weight:bold;margin-bottom:8px;">GTI COMPONENT BREAKDOWN</div>', unsafe_allow_html=True)

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

        st.markdown('<div style="font-size:10px;color:#8a9baa;margin-top:12px;margin-bottom:8px;">FULL_IMPACT FACTORS</div>', unsafe_allow_html=True)

        factors = [
            ("MACRO_VOLATILITY", 0.85, "ff8c42"),
            ("GEOPOLITICAL_RISK", 0.72, "ffb867"),
            ("SENTIMENT_AGGREGATE", 0.68, "8a9baa"),
            ("LIQUIDITY_DEPTH", 0.54, "6eaacf"),
        ]

        for factor, weight, color in factors:
            st.markdown(f"""
<div class="feature-row">
  <div class="feature-name">{factor}</div>
  <div class="feature-bar-wrap">
    <div class="feature-bar-fill" style="width:{weight*100}%;background:#{color};"></div>
  </div>
  <div class="feature-value">{weight:.2f}</div>
</div>
""", unsafe_allow_html=True)

    # ── RIGHT: PREDICTION HISTORY ───────────────────────────────────────────
    with col_right:
        st.markdown('<div style="font-size:11px;color:#8a9baa;font-weight:bold;margin-bottom:8px;">PREDICTION HISTORY (SIMULATION MODE)</div>', unsafe_allow_html=True)

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
""", unsafe_allow_html=True)
        else:
            st.markdown('<div style="color:#4a5060;font-size:9px;">No prediction history</div>', unsafe_allow_html=True)

        st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)

        st.markdown('<div style="font-size:10px;color:#8a9baa;font-weight:bold;margin-bottom:8px;">ASSET IMPACT</div>', unsafe_allow_html=True)

        if dir_pred == "BULLISH":
            st.markdown("""
<div style="font-size:8px;color:#6ecf8a;">BULLISH CATALYSTS</div>
<div style="font-size:8px;color:#4a5060;margin-top:4px;">USO, EWZ, FXI, GLD</div>
""", unsafe_allow_html=True)
        elif dir_pred == "BEARISH":
            st.markdown("""
<div style="font-size:8px;color:#ff6b6b;">BEARISH_CATALYSTS</div>
<div style="font-size:8px;color:#4a5060;margin-top:4px;">SHV, VGIT, IEF, TLT</div>
""", unsafe_allow_html=True)
        else:
            st.markdown("""
<div style="font-size:8px;color:#ffb867;">NEUTRAL_POSITIONING</div>
<div style="font-size:8px;color:#4a5060;margin-top:4px;">Monitor for directional clarity</div>
""", unsafe_allow_html=True)
