"""GeoMarket Intelligence - Sovereign Intelligence Framework"""

import streamlit as st
from datetime import datetime
import os

from ui import earth_pulse, geo_map, ai_signals, market

st.set_page_config(
    page_title="GeoMarket Intelligence",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

with open(os.path.join(os.path.dirname(__file__), "styles.css")) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

TABS = ["Earth Pulse", "Geo Map", "AI Signals", "Market"]
TAB_KEYS = {t: t.lower().replace(" ", "_") for t in TABS}

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Earth Pulse"

# ── Top navbar ────────────────────────────────────────────────────────────────
try:
    from api.client import get_client
    client = get_client()
    gti_data = client.get_gti_current()
    gti_score = gti_data.get("gti_score", 0)
except Exception:
    gti_score = 0
now_str = datetime.now().strftime("%H:%M:%S")

tab_links_html = ""
for tab in TABS:
    active_cls = "nav-tab-active" if tab == st.session_state.active_tab else ""
    tab_links_html += f'<span class="nav-tab {active_cls}" data-tab-name="{tab}">{tab}</span>'

st.markdown(f"""
<div class="topnav">
  <div class="topnav-left">
    <span class="topnav-logo">GEOMARKET INTELLIGENCE</span>
    <div class="topnav-tabs">{tab_links_html}</div>
  </div>
  <div class="topnav-right">
    <span class="topnav-search">⌕ search...</span>
    <span class="topnav-icon">🔔</span>
    <span class="topnav-icon">⚙</span>
    <span class="gti-badge">GTI Score: {gti_score:.0f}</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Render invisible buttons for Streamlit to track tab changes
col1, col2, col3, col4 = st.columns(4)
if col1.button("Earth Pulse", key="tab_earth_pulse", use_container_width=False):
    st.session_state.active_tab = "Earth Pulse"
    st.experimental_set_query_params(tab="earth_pulse")
if col2.button("Geo Map", key="tab_geo_map", use_container_width=False):
    st.session_state.active_tab = "Geo Map"
    st.experimental_set_query_params(tab="geo_map")
if col3.button("AI Signals", key="tab_ai_signals", use_container_width=False):
    st.session_state.active_tab = "AI Signals"
    st.experimental_set_query_params(tab="ai_signals")
if col4.button("Market", key="tab_market", use_container_width=False):
    st.session_state.active_tab = "Market"
    st.experimental_set_query_params(tab="market")

st.markdown('<div style="height: -20px;"></div>', unsafe_allow_html=True)

# ── Handle tab switching via query param ──────────────────────────────────────
# Update session state from query params immediately so nav renders with correct active state
qp = st.experimental_get_query_params().get("tab", [None])[0]
if qp:
    tab_name = next((t for t, k in TAB_KEYS.items() if k == qp), None)
    if tab_name:
        st.session_state.active_tab = tab_name

# ── Page layout: left sidebar + main content ──────────────────────────────────
sidebar_col, main_col = st.columns([1, 6])

with sidebar_col:
    st.markdown("""
<div class="left-sidebar">
  <div class="sidebar-section">
    <div class="sidebar-meta">ARCHIVE_01</div>
    <div class="sidebar-meta">OPERATOR_SESSION_ACTIVE</div>
  </div>
  <nav class="sidebar-nav">
    <div class="sidebar-nav-item sidebar-nav-active">
      <span class="sidebar-nav-icon">◈</span> INTELLIGENCE
    </div>
    <div class="sidebar-nav-item">
      <span class="sidebar-nav-icon">◉</span> Archive
    </div>
    <div class="sidebar-nav-item">
      <span class="sidebar-nav-icon">◎</span> Surveillance
    </div>
    <div class="sidebar-nav-item">
      <span class="sidebar-nav-icon">◆</span> Tactical
    </div>
  </nav>
  <div class="sidebar-spacer"></div>
  <div class="sidebar-bottom">
    <div class="sidebar-nav-item">
      <span class="sidebar-nav-icon">⚙</span> Settings
    </div>
    <button class="scan-btn">INITIATE SCAN</button>
  </div>
</div>
""", unsafe_allow_html=True)

with main_col:
    active = st.session_state.active_tab
    if active == "Earth Pulse":
        earth_pulse.render()
    elif active == "Geo Map":
        geo_map.render()
    elif active == "AI Signals":
        ai_signals.render()
    elif active == "Market":
        market.render()

# ── Footer status bar ─────────────────────────────────────────────────────────
st.markdown(f"""
<div class="status-bar">
  <span class="status-bar-left">Sovereign Intelligence Framework v4.0.2</span>
  <span class="status-bar-center">
    <span class="status-dot-green">●</span> SYSTEM_STABLE &nbsp;
    <span class="status-item">ENCRYPTION_AES256</span> &nbsp;
    <span class="status-item">LATENCY_12MS</span>
  </span>
  <span class="status-bar-right">{now_str} UTC</span>
</div>
""", unsafe_allow_html=True)
