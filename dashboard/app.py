"""
GeoMarket Intelligence — Tactical Archive UI
=============================================
Design: "Sovereign Intelligence Framework" — Monastic Brutalism
- Palette: Midnight Tonal Scale + Amber (#ffb867) accent
- Typography: Barlow Condensed (logo) · Newsreader (narrative) · JetBrains Mono (data)
- Layout: heavy side panels + central workspace, hard corners (0px radius)
- Tonal depth instead of borders/shadows
"""

import sqlite3
import time
from datetime import datetime, timedelta
import os

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

try:
    from streamlit_plotly_events import plotly_events
    _HAS_PLOTLY_EVENTS = True
except ImportError:
    _HAS_PLOTLY_EVENTS = False

from config import GTI_DB, NEWS_DB, MARKET_DB, PREDICTIONS_DB, MAX_ROWS

# ═══════════════════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ═══════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="GeoMarket Intelligence",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

for _key, _default in [
    ("selected_country_iso3", None),
    ("selected_country_name", None),
    ("arc_filter", ["Military", "Sanctions", "Trade", "Diplomatic"]),
    ("risk_filter", ["CRITICAL", "HIGH", "ELEVATED", "LOW"]),
    ("last_refresh", time.time()),
]:
    if _key not in st.session_state:
        st.session_state[_key] = _default

# ═══════════════════════════════════════════════════════════════════════════
#  DESIGN TOKENS — Tactical Archive / Sovereign Intelligence Framework
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700&family=Newsreader:ital,wght@0,400;0,600;1,400&family=JetBrains+Mono:wght@400;600&family=Space+Grotesk:wght@400;600&display=swap');

:root {
  /* Midnight Tonal Scale */
  --base:          #0c0e14;
  --nav:           #1e1f26;
  --panel:         #1e1f26;
  --card:          #282a30;
  --hover:         #33343b;
  --ghost:         rgba(83,68,53,0.15);
  --outline:       #534435;

  /* Amber Pulse */
  --amber:         #ffb867;
  --amber-dim:     #d4840a;
  --amber-dark:    #673d00;
  --amber-glow:    rgba(255,184,103,0.12);
  --amber-glow2:   rgba(255,184,103,0.06);

  /* Signals */
  --pos:           #9dd3aa;
  --neg:           #ffb4ab;
  --neutral:       #8a8ea0;

  /* Text */
  --txt-hi:        #e2e2eb;
  --txt-mid:       #b8bcd0;
  --txt-low:       #8a8ea0;
  --txt-dim:       #534957;
}

html, body, .stApp { background: var(--base) !important; color: var(--txt-mid) !important; }
* { box-sizing: border-box; }

/* Typography */
.mono { font-family: 'JetBrains Mono', monospace !important; }
.serif { font-family: 'Newsreader', Georgia, serif !important; }
.data-num { font-family: 'JetBrains Mono', monospace !important; font-weight: 600; }
.data-lbl { font-family: 'Space Grotesk', sans-serif !important; font-size: 0.62rem;
            letter-spacing: 0.14em; text-transform: uppercase; color: var(--txt-low); }

/* Override Streamlit defaults */
#MainMenu, footer, header, [data-testid="stToolbar"] { visibility: hidden !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stVerticalBlock"] { gap: 0 !important; }
div[data-testid="column"] { padding: 0 !important; }
div[data-testid="stMetric"] { display: none !important; }
.stPlotlyChart { overflow: hidden; background: transparent !important; }
.js-plotly-plot .plotly .main-svg { background: transparent !important; }
iframe { border: none !important; outline: none !important; }

/* Multiselect dark theme */
div[data-baseweb="select"] { background: var(--card) !important; border-radius: 0 !important; }
div[data-baseweb="tag"] { background: var(--amber-glow) !important; color: var(--amber) !important; border-radius: 0 !important; }
.stMultiSelect label { font-family: 'Space Grotesk', sans-serif !important; color: var(--txt-low) !important;
                       font-size: 0.62rem !important; letter-spacing: 0.14em !important; text-transform: uppercase !important; }

/* ─── NAVBAR ─── */
.navbar {
  display: flex; align-items: center;
  background: var(--nav); border-bottom: 1px solid var(--outline);
  padding: 0 1.5rem; height: 52px; position: sticky; top: 0; z-index: 200;
}
.nav-logo {
  font-family: 'Barlow Condensed', sans-serif !important;
  font-size: 1.05rem; font-weight: 700; letter-spacing: 0.20em; color: var(--txt-hi);
  margin-right: 2.5rem; white-space: nowrap; text-transform: uppercase;
}
.nav-logo span { color: var(--amber); }
.nav-tab-row { display: flex; gap: 0; flex: 1; }
.ntab {
  padding: 0 1.6rem; height: 52px; line-height: 50px;
  font-family: 'Space Grotesk', sans-serif !important;
  font-size: 0.68rem; font-weight: 600; letter-spacing: 0.16em;
  text-transform: uppercase; color: var(--txt-low);
  border-bottom: 2px solid transparent; cursor: pointer; white-space: nowrap;
  transition: color 0.1s;
}
.ntab.active { color: var(--amber); border-bottom-color: var(--amber); }
.nav-right { margin-left: auto; display: flex; align-items: center; gap: 1.5rem; }
.nav-gti {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.92rem; font-weight: 600; color: var(--txt-hi); display: flex; align-items: center; gap: 6px;
}
.nav-gti-badge {
  font-size: 0.55rem; letter-spacing: 0.12em; padding: 2px 7px;
  font-family: 'Space Grotesk', sans-serif !important; font-weight: 700;
  text-transform: uppercase;
}
.live-pip {
  display: flex; align-items: center; gap: 5px;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.60rem; font-weight: 600; letter-spacing: 0.10em; color: var(--amber);
}
.pip { width: 6px; height: 6px; border-radius: 50%; background: var(--amber);
       animation: blink 2s linear infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.2} }
.nav-time { font-family: 'JetBrains Mono', monospace !important;
            font-size: 0.65rem; color: var(--txt-low); }
/* amber pulse glow on live-pip */
.pip-wrap { position:relative; }
.pip-wrap::after {
  content:''; position:absolute; inset:-8px; border-radius:50%;
  background: var(--amber); opacity:0.10;
  animation: blink 2s linear infinite;
}

/* ─── STATUS BAR ─── */
.statusbar {
  position: fixed; bottom: 0; left: 0; right: 0;
  background: var(--nav); border-top: 1px solid var(--outline);
  height: 28px; display: flex; align-items: center;
  padding: 0 1.5rem; gap: 2rem; z-index: 200;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.58rem; letter-spacing: 0.06em; color: var(--txt-dim);
}
.sb-lbl { color: var(--txt-dim); }
.sb-val { color: var(--txt-low); }
.sb-live { color: var(--amber); font-weight: 600; }

/* ─── PANELS ─── */
.lpanel {
  background: var(--panel); border-right: 1px solid var(--ghost);
  padding: 1.1rem 0.9rem; overflow-y: auto;
  min-height: calc(100vh - 84px);
}
.rpanel {
  background: var(--panel); border-left: 1px solid var(--ghost);
  padding: 1.1rem 0.9rem; overflow-y: auto;
  min-height: calc(100vh - 84px);
}
.cpanel { padding: 1.1rem 1.2rem; overflow-y: auto; min-height: calc(100vh - 84px); }

/* ─── LEFT SIDEBAR LABELS ─── */
.arch-label {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.60rem; letter-spacing: 0.08em; color: var(--txt-dim);
  margin-bottom: 1.2rem; line-height: 1.6;
}
.nav-group-lbl {
  font-family: 'Space Grotesk', sans-serif !important;
  font-size: 0.55rem; letter-spacing: 0.16em; text-transform: uppercase;
  color: var(--txt-dim); margin-bottom: 0.4rem; margin-top: 0.8rem;
}
.side-nav-item {
  display: flex; align-items: center; gap: 0.5rem;
  font-family: 'Space Grotesk', sans-serif !important;
  font-size: 0.78rem; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase;
  color: var(--txt-low); padding: 0.45rem 0.6rem; margin-bottom: 0.15rem;
  cursor: pointer; transition: background 0.1s;
}
.side-nav-item.active { background: var(--amber-glow); color: var(--amber); }
.side-nav-icon { width: 14px; height: 14px; opacity: 0.7; }

/* ─── BIG GTI DISPLAY ─── */
.gti-mega {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 3.2rem; font-weight: 600; color: var(--txt-hi); line-height: 1;
  letter-spacing: -0.02em; margin: 0.3rem 0;
}
.gti-status-row { display: flex; align-items: center; gap: 0.4rem; margin-bottom: 0.4rem; }
.gti-sys-lbl {
  font-family: 'Space Grotesk', sans-serif !important;
  font-size: 0.60rem; letter-spacing: 0.18em; text-transform: uppercase; color: var(--txt-dim);
}
.gti-badge {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.57rem; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase;
  padding: 2px 8px; border-radius: 0;
}
.gb-low  { background: rgba(157,211,170,0.12); color: var(--pos); }
.gb-mod  { background: rgba(255,184,103,0.12); color: var(--amber); }
.gb-high { background: rgba(255,180,171,0.12); color: var(--neg); }

/* ─── SECTION HEADERS ─── */
.sec-hdr {
  font-family: 'Space Grotesk', sans-serif !important;
  font-size: 0.60rem; letter-spacing: 0.20em; text-transform: uppercase;
  color: var(--txt-dim); border-left: 2px solid var(--amber);
  padding-left: 0.5rem; margin: 0.8rem 0 0.6rem;
}
.sec-hdr-icon { color: var(--amber); margin-right: 4px; }

/* ─── DATA CARDS ─── */
.dcard {
  background: var(--card);
  border-top: 2px solid var(--amber-dim);
  padding: 0.65rem 0.8rem; margin-bottom: 0.5rem;
}
.dcard-hi { border-top-color: var(--neg); }
.dcard-ok { border-top-color: var(--pos); }
.dcard-neu { border-top-color: var(--neutral); }
.dcard-watch { border-top-color: var(--amber); }

.dcard-lbl {
  font-family: 'Space Grotesk', sans-serif !important;
  font-size: 0.58rem; letter-spacing: 0.16em; text-transform: uppercase; color: var(--txt-dim);
  margin-bottom: 3px;
}
.dcard-val {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 1.25rem; font-weight: 600; color: var(--txt-hi); line-height: 1.1;
}
.dcard-sub {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.60rem; color: var(--txt-dim); margin-top: 3px;
}
.dcard-pct { font-size: 0.72rem; font-weight: 600; }

/* ─── SIGNAL COMPONENTS (left panel) ─── */
.sig-block {
  background: var(--card); margin-bottom: 0.5rem; padding: 0.7rem 0.8rem;
}
.sig-name {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.68rem; font-weight: 600; letter-spacing: 0.06em;
  color: var(--amber); margin-bottom: 0.3rem;
}
.sig-val {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 1.5rem; font-weight: 600; color: var(--txt-hi); text-align: right;
}
.sig-bar-track { background: var(--hover); height: 4px; margin-top: 6px; }
.sig-bar-fill  { height: 4px; }
.sig-desc {
  font-family: 'Newsreader', serif !important;
  font-size: 0.72rem; color: var(--txt-low); margin-top: 6px; line-height: 1.5;
  font-style: italic;
}

/* ─── VOLATILITY BADGE ─── */
.vol-block {
  background: var(--card); padding: 0.6rem 0.8rem; margin-bottom: 0.5rem;
  border-left: 3px solid var(--amber-dim);
}
.vol-lbl { font-family: 'Space Grotesk', sans-serif !important;
           font-size: 0.58rem; letter-spacing: 0.16em; text-transform: uppercase;
           color: var(--txt-dim); margin-bottom: 2px; }
.vol-val-hi { font-family: 'JetBrains Mono', monospace !important;
               font-size: 1rem; font-weight: 600; color: var(--neg); }
.vol-val-lo { font-family: 'JetBrains Mono', monospace !important;
               font-size: 1rem; font-weight: 600; color: var(--pos); }

/* ─── RISK LEGEND ─── */
.risk-row {
  display: flex; align-items: center; gap: 0.5rem; padding: 0.25rem 0;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.62rem; color: var(--txt-low); letter-spacing: 0.06em;
}
.risk-pip { width: 8px; height: 8px; flex-shrink: 0; }

/* ─── NEWS FEED ─── */
.news-scroll { max-height: 280px; overflow-y: auto; }
.ni {
  display: flex; gap: 0.5rem; align-items: flex-start;
  padding: 0.55rem 0; border-bottom: 1px solid var(--ghost);
}
.ni:last-child { border-bottom: none; }
.n-dot { flex-shrink: 0; width: 5px; height: 5px; margin-top: 8px; }
.n-title {
  font-family: 'Newsreader', serif !important;
  font-size: 0.80rem; color: var(--txt-hi); line-height: 1.45;
}
.n-meta {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.56rem; color: var(--txt-dim); margin-top: 2px; letter-spacing: 0.04em;
}
.n-score {
  flex-shrink: 0; font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.62rem; font-weight: 600; padding: 2px 6px; margin-top: 2px;
}
.sp { background: rgba(157,211,170,0.10); color: var(--pos); }
.sn { background: rgba(255,180,171,0.10); color: var(--neg); }
.sz { color: var(--neutral); }

/* ─── ASSET CARDS (right panel) ─── */
.acard {
  background: var(--card); padding: 0.7rem 0.8rem; margin-bottom: 0.45rem;
  border-left: 3px solid var(--neutral); display: flex; justify-content: space-between; align-items: flex-start;
}
.acard-up   { border-left-color: var(--pos); }
.acard-down { border-left-color: var(--neg); }
.acard-watch { border-left-color: var(--amber); }
.a-pair { font-family: 'JetBrains Mono', monospace !important;
          font-size: 0.78rem; font-weight: 600; color: var(--txt-hi); }
.a-type { font-family: 'Space Grotesk', sans-serif !important;
          font-size: 0.54rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--txt-dim); }
.a-sig  { font-family: 'JetBrains Mono', monospace !important;
          font-size: 0.62rem; font-weight: 600; padding: 2px 8px; }
.sig-up   { background: rgba(157,211,170,0.10); color: var(--pos); }
.sig-dn   { background: rgba(255,180,171,0.10); color: var(--neg); }
.sig-wt   { background: rgba(255,184,103,0.10); color: var(--amber); }
.sig-nu   { background: rgba(138,142,160,0.10); color: var(--neutral); }

/* ─── TABS (Streamlit native) ─── */
div[role="tab"] {
  font-family: 'Space Grotesk', sans-serif !important;
  font-weight: 600 !important; letter-spacing: 0.14em !important;
  font-size: 0.70rem !important; text-transform: uppercase !important;
  color: var(--txt-dim) !important;
}
div[aria-selected="true"] { color: var(--amber) !important; }
div[data-baseweb="tab-highlight"] { background-color: var(--amber) !important; }
div[data-baseweb="tab-border"] { background-color: var(--ghost) !important; }

/* ─── BUTTONS ─── */
div[data-testid="stButton"] button {
  background: transparent !important;
  border: 1px solid var(--outline) !important;
  color: var(--txt-low) !important;
  font-family: 'Space Grotesk', sans-serif !important;
  font-size: 0.60rem !important; font-weight: 700 !important;
  letter-spacing: 0.16em !important; text-transform: uppercase !important;
  border-radius: 0 !important; padding: 4px 12px !important;
  transition: background 0.1s !important;
}
div[data-testid="stButton"] button:hover {
  background: var(--amber-glow) !important;
  color: var(--amber) !important; border-color: var(--amber) !important;
}

/* ─── CTA BUTTON ─── */
.cta-btn {
  display: block; width: 100%;
  background: var(--amber-dim); color: #000;
  font-family: 'Space Grotesk', sans-serif !important;
  font-size: 0.68rem; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase;
  text-align: center; padding: 10px 0; border: none; cursor: pointer;
  margin-top: 1rem;
  box-shadow: 0 0 20px rgba(255,184,103,0.10);
  animation: amberglow 2s linear infinite;
}
@keyframes amberglow { 0%,100%{box-shadow:0 0 16px rgba(255,184,103,0.10)}
                       50%{box-shadow:0 0 28px rgba(255,184,103,0.22)} }

/* ─── MARKET CARDS (top row) ─── */
.mkt-hdr {
  display: flex; justify-content: space-between; align-items: flex-start;
  margin-bottom: 0.2rem;
}
.mkt-sym { font-family: 'Barlow Condensed', sans-serif !important;
           font-size: 1.1rem; font-weight: 700; letter-spacing: 0.06em; color: var(--amber); }
.mkt-sub { font-family: 'Space Grotesk', sans-serif !important;
           font-size: 0.56rem; letter-spacing: 0.12em; color: var(--txt-dim); text-transform: uppercase; }
.mkt-price { font-family: 'JetBrains Mono', monospace !important;
             font-size: 1.5rem; font-weight: 600; color: var(--txt-hi); }
.mkt-chg-up { font-family: 'JetBrains Mono', monospace !important;
              font-size: 0.72rem; font-weight: 600; color: var(--pos); }
.mkt-chg-dn { font-family: 'JetBrains Mono', monospace !important;
              font-size: 0.72rem; font-weight: 600; color: var(--neg); }

/* ─── MARKET TAC CARD (top tiles) ─── */
.tac-card {
  background: var(--card); padding: 0.8rem 1rem; margin-bottom: 0.1rem;
}
.tac-card-active { border-top: 2px solid var(--amber); }

/* ─── COUNTRY DETAIL ─── */
.c-name {
  font-family: 'Barlow Condensed', sans-serif !important;
  font-size: 1.4rem; font-weight: 700; letter-spacing: 0.04em; color: var(--txt-hi);
  margin-bottom: 0.4rem;
}
.detail-row {
  display: flex; justify-content: space-between; align-items: center;
  padding: 0.4rem 0; border-bottom: 1px solid var(--ghost);
  font-family: 'JetBrains Mono', monospace !important; font-size: 0.65rem;
}
.detail-row:last-child { border-bottom: none; }

/* ─── AI SIGNALS — feature importance bars ─── */
.feat-row { margin-bottom: 0.55rem; }
.feat-lbl { font-family: 'Space Grotesk', sans-serif !important;
            font-size: 0.60rem; letter-spacing: 0.12em; text-transform: uppercase;
            color: var(--txt-low); display: flex; justify-content: space-between; }
.feat-pct { font-family: 'JetBrains Mono', monospace !important;
            font-size: 0.62rem; color: var(--amber); }
.feat-track { background: var(--hover); height: 3px; margin-top: 4px; }
.feat-fill  { height: 3px; background: var(--amber); }

/* ─── FULL IMPACT PANEL ─── */
.impact-cat-lbl {
  font-family: 'Space Grotesk', sans-serif !important;
  font-size: 0.56rem; letter-spacing: 0.18em; text-transform: uppercase;
  color: var(--txt-dim); margin: 0.6rem 0 0.3rem; border-bottom: 1px solid var(--ghost);
  padding-bottom: 3px;
}
.impact-row {
  display: flex; justify-content: space-between; align-items: center;
  padding: 0.4rem 0.5rem; margin-bottom: 0.25rem;
  background: var(--card);
}
.impact-sym { font-family: 'JetBrains Mono', monospace !important;
              font-size: 0.72rem; font-weight: 600; color: var(--txt-hi); }
.impact-arrow { font-family: 'JetBrains Mono', monospace !important;
                font-size: 1rem; font-weight: 700; }
.arr-up   { color: var(--pos); }
.arr-dn   { color: var(--neg); }
.arr-neu  { color: var(--neutral); }
.arr-wt   { color: var(--amber); }

/* ─── GEO MAP filter ─── */
.filtpanel {
  background: var(--card); padding: 0.7rem 0.8rem; margin-bottom: 0.6rem;
}

/* Scrollbar styling */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--base); }
::-webkit-scrollbar-thumb { background: var(--outline); border-radius: 0; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
#  DATA LAYER
# ═══════════════════════════════════════════════════════════════════════════
def _q(db: str, sql: str, params: tuple = ()) -> pd.DataFrame:
    try:
        conn = sqlite3.connect(db)
        df   = pd.read_sql_query(sql, conn, params=params)
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()

@st.cache_data(ttl=60)
def load_gti(hours: int = 48) -> pd.DataFrame:
    cut = (datetime.utcnow()-timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M:%S")
    return _q(GTI_DB,
        f"SELECT * FROM gti_scores WHERE timestamp>=? ORDER BY timestamp LIMIT {MAX_ROWS}",
        (cut,))

@st.cache_data(ttl=60)
def load_pred() -> dict:
    df = _q(PREDICTIONS_DB, "SELECT * FROM predictions ORDER BY timestamp DESC LIMIT 1")
    return df.iloc[0].to_dict() if not df.empty else {}

@st.cache_data(ttl=60)
def load_pred_history() -> pd.DataFrame:
    cut = (datetime.utcnow()-timedelta(hours=48)).strftime("%Y-%m-%d %H:%M:%S")
    return _q(PREDICTIONS_DB,
        f"SELECT * FROM predictions WHERE timestamp>=? ORDER BY timestamp LIMIT {MAX_ROWS}",
        (cut,))

@st.cache_data(ttl=60)
def load_market(sym: str, hours: int = 48) -> pd.DataFrame:
    cut = (datetime.utcnow()-timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M:%S")
    return _q(MARKET_DB,
        f"SELECT * FROM ohlcv WHERE symbol=? AND timestamp>=? ORDER BY timestamp LIMIT {MAX_ROWS}",
        (sym, cut))

@st.cache_data(ttl=60)
def load_news(n: int = 80) -> pd.DataFrame:
    return _q(NEWS_DB,
        f"SELECT title,source,published_at,vader_compound,vader_label "
        f"FROM rss_articles ORDER BY published_at DESC LIMIT {n}")

@st.cache_data(ttl=120)
def load_gdelt_country_tension(hours: int = 48) -> pd.DataFrame:
    cut = (datetime.utcnow()-timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M:%S")
    return _q(NEWS_DB,
        f"""SELECT actor1_country, actor2_country, goldstein_scale, avg_tone, event_code
            FROM gdelt_events WHERE timestamp >= ? LIMIT {MAX_ROWS}""",
        (cut,))

@st.cache_data(ttl=60)
def load_country_headlines(fips_code: str, n: int = 10) -> pd.DataFrame:
    cut = (datetime.utcnow()-timedelta(hours=48)).strftime("%Y-%m-%d %H:%M:%S")
    return _q(NEWS_DB,
        f"""SELECT event_code, goldstein_scale, avg_tone, num_articles
            FROM gdelt_events
            WHERE (actor1_country=? OR actor2_country=?) AND timestamp >= ?
            ORDER BY num_articles DESC LIMIT {n}""",
        (fips_code, fips_code, cut))


# ═══════════════════════════════════════════════════════════════════════════
#  IMPACT ENGINE
# ═══════════════════════════════════════════════════════════════════════════
IMPACT_RULES = [
    {"asset":"XAU/USD","name":"Gold",            "type":"COMMODITY",
     "kw":["gold","war","conflict","nuclear","sanctions","safe haven","inflation","crisis","military","attack"],
     "neg":+1,"pos":-1},
    {"asset":"USD/JPY","name":"Dollar / Yen",    "type":"FX",
     "kw":["federal reserve","fed rate","fomc","powell","cpi","inflation","treasury","dollar","interest rate"],
     "neg":-1,"pos":+1},
    {"asset":"EUR/USD","name":"Euro / Dollar",   "type":"FX",
     "kw":["ecb","european central bank","eurozone","eu sanctions","russia gas","germany","euro"],
     "neg":-1,"pos":+1},
    {"asset":"USD/CNH","name":"Dollar / Yuan",   "type":"FX",
     "kw":["china","pboc","yuan","taiwan","beijing","xi jinping","hong kong","chinese"],
     "neg":+1,"pos":-1},
    {"asset":"GBP/USD","name":"Pound / Dollar",  "type":"FX",
     "kw":["bank of england","boe","sterling","pound","uk gdp","uk inflation","britain"],
     "neg":-1,"pos":+1},
    {"asset":"BTC/CORE","name":"Bitcoin",        "type":"CRYPTO",
     "kw":["bitcoin","crypto","btc","digital asset","sec crypto","cbdc","defi","crypto regulation"],
     "neg":-1,"pos":+1},
    {"asset":"SPX_500","name":"S&P 500",         "type":"EQUITY",
     "kw":["s&p","nasdaq","dow","earnings","gdp growth","rate cut","stimulus","jobs report","stock market"],
     "neg":-1,"pos":+1},
    {"asset":"NAS_100","name":"NASDAQ 100",      "type":"EQUITY",
     "kw":["nasdaq","tech","technology","rate cut","fed pivot","ai","silicon valley","big tech"],
     "neg":-1,"pos":+1},
    {"asset":"OIL/USD","name":"Crude Oil",       "type":"COMMODITY",
     "kw":["opec","oil","crude","brent","wti","saudi","iran","pipeline","middle east","energy"],
     "neg":+1,"pos":+1},
    {"asset":"XAG/USD","name":"Silver",          "type":"COMMODITY",
     "kw":["silver","precious metal","industrial demand","solar","manufacturing"],
     "neg":+1,"pos":-1},
    {"asset":"VIX",    "name":"Volatility",      "type":"EQUITY",
     "kw":["volatility","risk","uncertainty","crash","sell-off","turmoil","fear","panic"],
     "neg":+1,"pos":-1},
]

def analyze_impact(news_df: pd.DataFrame) -> list:
    if news_df.empty:
        return [{**r,"signal":"neutral","match_ct":0,"reason":"No data"} for r in IMPACT_RULES]
    headlines = [(str(row["title"]).lower(), float(row.get("vader_compound",0)))
                 for _,row in news_df.iterrows()]
    out = []
    for rule in IMPACT_RULES:
        matches, score_sum = [], 0.0
        for tl, compound in headlines:
            if any(kw in tl for kw in rule["kw"]):
                matches.append(tl)
                score_sum += compound
        if not matches:
            out.append({**rule,"signal":"neutral","match_ct":0,"reason":"No recent triggers"})
            continue
        avg = score_sum / len(matches)
        direction = rule["neg"] if avg<=-0.05 else (rule["pos"] if avg>=0.05 else 0)
        signal = "up" if direction==+1 else ("down" if direction==-1 else "watch")
        reason = (matches[0][:60]+"…") if len(matches[0])>60 else matches[0]
        out.append({**rule,"signal":signal,"match_ct":len(matches),"reason":reason})
    out.sort(key=lambda x: -x["match_ct"])
    return out


# ═══════════════════════════════════════════════════════════════════════════
#  GEO + COUNTRY MAPS
# ═══════════════════════════════════════════════════════════════════════════
SOURCE_GEO = {
    "reuters":         (51.50,  -0.12, "London"),
    "bbc":             (51.50,  -0.12, "London"),
    "al jazeera":      (25.29,  51.53, "Doha"),
    "associated press":(40.71, -74.00, "New York"),
    "ap ":             (40.71, -74.00, "New York"),
    "bloomberg":       (40.71, -74.00, "New York"),
    "cnbc":            (40.71, -74.00, "New York"),
    "xinhua":          (39.90, 116.40, "Beijing"),
    "tass":            (55.75,  37.62, "Moscow"),
    "france24":        (48.86,   2.35, "Paris"),
    "deutsche welle":  (50.73,   7.10, "Bonn"),
    "times of india":  (28.61,  77.20, "Delhi"),
    "kyodo":           (35.68, 139.69, "Tokyo"),
    "nikkei":          (35.68, 139.69, "Tokyo"),
    "haaretz":         (32.08,  34.78, "Tel Aviv"),
    "jerusalem post":  (32.08,  34.78, "Tel Aviv"),
    "dawn":            (24.86,  67.01, "Karachi"),
    "korea times":     (37.57, 126.98, "Seoul"),
    "middle east eye": (25.20,  55.27, "Dubai"),
}
DEFAULT_GEO = (20.0, 0.0, "Global")

def geo(source: str):
    sl = source.lower()
    for k, v in SOURCE_GEO.items():
        if k in sl: return v
    return DEFAULT_GEO

FIPS_TO_ISO3 = {
    "US": "USA", "RS": "RUS", "UK": "GBR", "CH": "CHN", "FR": "FRA",
    "GM": "DEU", "IS": "ISR", "IR": "IRN", "IZ": "IRQ", "SY": "SYR",
    "UP": "UKR", "EG": "EGY", "SA": "SAU", "AF": "AFG", "PK": "PAK",
    "IN": "IND", "JA": "JPN", "KS": "KOR", "TU": "TUR", "LY": "LBY",
    "SU": "SDN", "YM": "YEM", "NI": "NGA", "ET": "ETH", "SO": "SOM",
    "MO": "MAR", "AL": "DZA", "TN": "TUN", "AE": "ARE", "QA": "QAT",
    "KU": "KWT", "LE": "LBN", "JO": "JOR", "BR": "BRA", "MX": "MEX",
    "VE": "VEN", "CO": "COL", "AR": "ARG", "SP": "ESP", "IT": "ITA",
    "PO": "POL", "GR": "GRC", "RO": "ROU", "HU": "HUN", "EZ": "CZE",
    "AU": "AUS", "CA": "CAN", "SF": "ZAF", "KE": "KEN", "GH": "GHA",
    "CI": "CIV", "ML": "MLI", "BF": "BFA", "TD": "TCD", "CF": "CAF",
    "CG": "COD", "AO": "AGO", "MZ": "MOZ", "ZI": "ZWE", "BC": "BWA",
    "TZ": "TZA", "UG": "UGA", "RW": "RWA", "BI": "BDI", "SN": "SEN",
    "ID": "IDN", "TH": "THA", "MY": "MYS", "PH": "PHL", "VM": "VNM",
    "BM": "MMR", "CB": "KHM", "LA": "LAO", "SG": "SGP",
    "NZ": "NZL", "NP": "NPL", "BG": "BGD", "CE": "LKA",
    "TI": "TJK", "UZ": "UZB", "KZ": "KAZ", "KG": "KGZ", "TX": "TKM",
    "AJ": "AZE", "AM": "ARM", "GG": "GEO", "BE": "BLR", "MD": "MDA",
    "LG": "LVA", "LH": "LTU", "EN": "EST", "SW": "SWE", "NO": "NOR",
    "DA": "DNK", "NL": "NLD", "LU": "LUX", "SZ": "CHE",
    "MN": "MNG", "TW": "TWN", "HK": "HKG", "SB": "SRB", "HR": "HRV",
    "BK": "BIH", "MK": "MKD", "MJ": "MNE", "LO": "SVK",
    "SI": "SVN", "FI": "FIN", "IC": "ISL", "EI": "IRL",
    "BU": "BGR", "BO": "BOL", "EC": "ECU", "PE": "PER",
    "UY": "URY", "PA": "PRY", "CU": "CUB", "HA": "HTI", "DR": "DOM",
}
ISO3_TO_FIPS = {v: k for k, v in FIPS_TO_ISO3.items()}

ISO3_TO_COUNTRY_NAME = {
    "USA":"United States","RUS":"Russia","GBR":"United Kingdom","CHN":"China",
    "FRA":"France","DEU":"Germany","ISR":"Israel","IRN":"Iran","IRQ":"Iraq",
    "SYR":"Syria","UKR":"Ukraine","EGY":"Egypt","SAU":"Saudi Arabia",
    "AFG":"Afghanistan","PAK":"Pakistan","IND":"India","JPN":"Japan",
    "KOR":"South Korea","TUR":"Turkey","LBY":"Libya","SDN":"Sudan",
    "YEM":"Yemen","NGA":"Nigeria","ETH":"Ethiopia","SOM":"Somalia",
    "MAR":"Morocco","DZA":"Algeria","TUN":"Tunisia","ARE":"UAE",
    "QAT":"Qatar","KWT":"Kuwait","LBN":"Lebanon","JOR":"Jordan",
    "BRA":"Brazil","MEX":"Mexico","VEN":"Venezuela","COL":"Colombia",
    "ARG":"Argentina","ESP":"Spain","ITA":"Italy","POL":"Poland",
    "GRC":"Greece","ROU":"Romania","HUN":"Hungary","CZE":"Czech Republic",
    "AUS":"Australia","CAN":"Canada","ZAF":"South Africa",
    "KEN":"Kenya","GHA":"Ghana","IDN":"Indonesia","THA":"Thailand",
    "MYS":"Malaysia","PHL":"Philippines","VNM":"Vietnam","MMR":"Myanmar",
    "SGP":"Singapore","NPL":"Nepal","BGD":"Bangladesh","LKA":"Sri Lanka",
    "KAZ":"Kazakhstan","UZB":"Uzbekistan","AZE":"Azerbaijan",
    "ARM":"Armenia","GEO":"Georgia","BLR":"Belarus","SWE":"Sweden",
    "NOR":"Norway","DNK":"Denmark","NLD":"Netherlands","CHE":"Switzerland",
    "FIN":"Finland","IRL":"Ireland","PRT":"Portugal","BGR":"Bulgaria",
    "HRV":"Croatia","SRB":"Serbia","MNG":"Mongolia","TWN":"Taiwan",
    "CUB":"Cuba","HTI":"Haiti",
}

ISO3_TO_COUNTRY_KEYWORDS = {
    "USA":["united states","us economy","federal reserve","washington","congress","dollar","wall street"],
    "RUS":["russia","moscow","kremlin","putin","ukraine war","russian"],
    "CHN":["china","beijing","xi jinping","taiwan","hong kong","chinese","pboc","yuan"],
    "ISR":["israel","tel aviv","gaza","hamas","netanyahu","idf"],
    "IRN":["iran","tehran","ayatollah","nuclear deal","iranian"],
    "SYR":["syria","damascus","syrian","aleppo"],
    "UKR":["ukraine","kyiv","zelensky","donbas","ukrainian"],
    "GBR":["britain","uk economy","london","sunak","sterling","bank of england"],
    "DEU":["germany","berlin","german","bundesbank","scholz"],
    "FRA":["france","paris","macron","french","ecb"],
    "SAU":["saudi","riyadh","aramco","opec","mbs"],
    "IRQ":["iraq","baghdad","iraqi","mosul"],
    "PAK":["pakistan","islamabad","karachi","imf pakistan"],
    "IND":["india","delhi","modi","rupee","reserve bank india"],
    "JPN":["japan","tokyo","yen","boj","bank of japan","japanese"],
    "KOR":["south korea","seoul","won currency","korean"],
    "TUR":["turkey","ankara","erdogan","lira","turkish"],
    "EGY":["egypt","cairo","suez","egyptian pound"],
    "LBN":["lebanon","beirut","hezbollah","lebanese"],
    "YEM":["yemen","houthi","sanaa","yemeni"],
    "NGA":["nigeria","lagos","abuja","naira","boko haram"],
    "ZAF":["south africa","johannesburg","rand currency"],
    "BRA":["brazil","brasilia","bolsonaro","lula","real currency"],
    "MEX":["mexico","mexico city","peso","mexican"],
    "ARG":["argentina","buenos aires","peso argentina","milei"],
}

def classify_arc_type(event_code) -> str:
    if not event_code:
        return "Diplomatic"
    try:
        code = int(str(event_code)[:3])
    except (ValueError, TypeError):
        return "Diplomatic"
    if 50 <= code <= 69:
        return "Trade"
    elif (100 <= code <= 119) or (160 <= code <= 169) or code >= 200:
        return "Sanctions"
    elif code >= 120:
        return "Military"
    return "Diplomatic"

def build_country_tension_df(gdelt_df: pd.DataFrame) -> pd.DataFrame:
    if gdelt_df.empty:
        return pd.DataFrame()
    country_data: dict = {}
    for _, row in gdelt_df.iterrows():
        for field in ["actor1_country", "actor2_country"]:
            fips = str(row.get(field, "") or "").strip().upper()
            if not fips or fips == "NAN" or len(fips) != 2:
                continue
            iso3 = FIPS_TO_ISO3.get(fips)
            if not iso3:
                continue
            if iso3 not in country_data:
                country_data[iso3] = {"conflict": 0, "total": 0, "tone_sum": 0.0}
            gs   = row.get("goldstein_scale")
            tone = row.get("avg_tone")
            country_data[iso3]["total"] += 1
            if gs is not None:
                try:
                    if float(gs) < -5.0:
                        country_data[iso3]["conflict"] += 1
                except (ValueError, TypeError):
                    pass
            if tone is not None:
                try:
                    country_data[iso3]["tone_sum"] += float(tone)
                except (ValueError, TypeError):
                    pass
    rows = []
    for iso3, d in country_data.items():
        total = max(d["total"], 1)
        conflict_ratio = d["conflict"] / total
        avg_tone = d["tone_sum"] / total
        tone_norm = max(0.0, min(1.0, (-avg_tone + 100.0) / 200.0))
        raw = 0.6 * conflict_ratio + 0.4 * tone_norm
        rows.append({
            "iso3": iso3,
            "tension": round(raw * 100, 1),
            "conflict_ct": d["conflict"],
            "total_events": total,
            "avg_tone": round(avg_tone, 2),
        })
    return pd.DataFrame(rows) if rows else pd.DataFrame()

def build_geo_df(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in df.iterrows():
        lat, lon, city = geo(str(row.get("source","")))
        comp  = float(row.get("vader_compound",0))
        title = str(row.get("title",""))
        rows.append({
            "lat":  lat + (hash(title) % 9)*0.25 - 1.0,
            "lon":  lon + (hash(str(row.get("source",""))) % 9)*0.25 - 1.0,
            "city": city,
            "compound": comp,
            "label": str(row.get("vader_label","neutral")),
            "title": title[:55],
            "source": str(row.get("source","")),
            "pub":   str(row.get("published_at",""))[:16],
        })
    return pd.DataFrame(rows) if rows else pd.DataFrame()


# ═══════════════════════════════════════════════════════════════════════════
#  PLOT CONFIG — Tactical Archive dark theme
# ═══════════════════════════════════════════════════════════════════════════
PLOT_BASE = dict(
    paper_bgcolor="#0c0e14",
    plot_bgcolor="#0c0e14",
    font=dict(family="JetBrains Mono, monospace", color="#8a8ea0", size=10),
)
_AX  = dict(gridcolor="#1e1f26", showline=False, zeroline=False)
_M8  = dict(l=8, r=8, t=8, b=8)
_M12 = dict(l=12, r=12, t=8, b=8)

AMBER    = "#ffb867"
AMBER_DIM = "#d4840a"
POS      = "#9dd3aa"
NEG      = "#ffb4ab"
NEU_COL  = "#8a8ea0"

SIG_LBL = {"up":"↑  BULLISH","down":"↓  BEARISH","watch":"⚡ WATCH","neutral":"—  NEUTRAL"}
SIG_CLS = {"up":"sig-up","down":"sig-dn","watch":"sig-wt","neutral":"sig-nu"}
ARR_CLS = {"up":"arr-up","down":"arr-dn","watch":"arr-wt","neutral":"arr-neu"}


def gti_meta(score_100: float):
    if score_100 >= 80: return "CRITICAL_THREAT",  "gb-high", NEG
    if score_100 >= 60: return "HIGH_THREAT",       "gb-high", NEG
    if score_100 >= 35: return "ELEVATED_WATCH",    "gb-mod",  AMBER
    return                     "NOMINAL_STABLE",    "gb-low",  POS


def build_choropleth_globe(
    country_tension_df: pd.DataFrame,
    proj_type: str = "orthographic",
    proj_lon: float = 20.0,
    proj_lat: float = 20.0,
    height: int = 460
) -> go.Figure:
    if not country_tension_df.empty:
        iso3_vals = country_tension_df["iso3"].tolist()
        z_vals    = country_tension_df["tension"].tolist()
        hover_txt = [
            f"<b>{ISO3_TO_COUNTRY_NAME.get(r['iso3'], r['iso3'])}</b>"
            f"<br>Tension: {r['tension']:.0f}/100"
            f"<br>Conflicts: {r['conflict_ct']}"
            f"<br>Events: {r['total_events']}"
            for _, r in country_tension_df.iterrows()
        ]
    else:
        iso3_vals = ["USA"]
        z_vals    = [0]
        hover_txt = ["No GDELT data loaded"]

    fig = go.Figure(go.Choropleth(
        locations=iso3_vals,
        z=z_vals,
        locationmode="ISO-3",
        colorscale=[
            [0.00, "#111319"],
            [0.35, "#1e3a2a"],
            [0.60, "#5c3800"],
            [0.80, "#8b2800"],
            [1.00, "#b22020"],
        ],
        zmin=0, zmax=100,
        showscale=False,
        marker=dict(line=dict(color="#1e1f26", width=0.5)),
        text=hover_txt,
        hovertemplate="%{text}<extra></extra>",
    ))

    geo_cfg = dict(
        showland=True,       landcolor="#111319",
        showocean=True,      oceancolor="#0c0e14",
        showcoastlines=True, coastlinecolor="#282a30",
        showcountries=False,
        showframe=False,
        bgcolor="#0c0e14",
    )
    if proj_type == "orthographic":
        geo_cfg["projection"] = dict(
            type="orthographic",
            rotation=dict(lon=proj_lon, lat=proj_lat, roll=0)
        )
    else:
        geo_cfg["projection_type"] = proj_type
        geo_cfg["lataxis"] = dict(range=[-70, 80])
        geo_cfg["lonaxis"] = dict(range=[-180, 180])

    fig.update_layout(
        **PLOT_BASE,
        margin=dict(l=0, r=0, t=0, b=0),
        height=height,
        geo=geo_cfg,
        dragmode="orbit",
        uirevision="globe_constant",
        clickmode="event",
    )
    return fig


# ═══════════════════════════════════════════════════════════════════════════
#  LOAD ALL DATA
# ═══════════════════════════════════════════════════════════════════════════
gti_df   = load_gti(48)
pred     = load_pred()
pred_h   = load_pred_history()
news_df  = load_news(80)
spy_df   = load_market("SPY", 48)
vix_df   = load_market("VIX", 48)
gld_df   = load_market("GLD", 48)
impacts  = analyze_impact(news_df)
now_utc  = datetime.utcnow()
now_str  = now_utc.strftime("%H:%M:%S UTC")
date_str = now_utc.strftime("%Y-%m-%d")

score       = float(gti_df["gti_score"].iloc[-1]) if not gti_df.empty else 0.0
score_100   = round(score * 100, 1)
conflict_ct = int(gti_df["conflict_ct"].iloc[-1]) if not gti_df.empty else 0
avg_tone    = float(gti_df["avg_tone"].iloc[-1])  if not gti_df.empty else 0.0
vader_avg   = float(gti_df["vader_avg"].iloc[-1]) if not gti_df.empty else 0.0
lev_lbl, lev_cls, lev_col = gti_meta(score_100)

vol_pred = str(pred.get("vol_prediction","—"))
vol_conf = float(pred.get("vol_prob", 0) or 0)
dir_pred = str(pred.get("dir_prediction","—"))
dir_conf = float(pred.get("dir_prob", 0) or 0)

pos_ct = int((news_df["vader_label"]=="positive").sum()) if not news_df.empty else 0
neg_ct = int((news_df["vader_label"]=="negative").sum()) if not news_df.empty else 0
neu_ct = int((news_df["vader_label"]=="neutral").sum())  if not news_df.empty else 0
total_news = pos_ct + neg_ct + neu_ct

gdelt_raw_df = load_gdelt_country_tension(48)
country_df   = build_country_tension_df(gdelt_raw_df)


# ═══════════════════════════════════════════════════════════════════════════
#  NAVBAR
# ═══════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="navbar">
  <div class="nav-logo">GEOMARKET&nbsp;<span>INTELLIGENCE</span></div>
  <div class="nav-tab-row" id="navtabs">
    <div class="ntab active">EARTH PULSE</div>
    <div class="ntab">GEO MAP</div>
    <div class="ntab">AI SIGNALS</div>
    <div class="ntab">MARKET</div>
  </div>
  <div class="nav-right">
    <div class="nav-gti">
      &#9889;&nbsp;GTI SCORE:&nbsp;{score_100:.1f}
      <span class="nav-gti-badge {lev_cls}">{lev_lbl}</span>
    </div>
    <div class="live-pip"><div class="pip-wrap"><div class="pip"></div></div>&nbsp;LIVE</div>
    <div class="nav-time">{now_str}</div>
  </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "EARTH PULSE",
    "GEO MAP",
    "AI SIGNALS",
    "MARKET",
])


# ═══════════════════════════════════════════════════════════════════════════
#  TAB 1 — EARTH PULSE
# ═══════════════════════════════════════════════════════════════════════════
with tab1:
    left, center, right = st.columns([1.15, 3.7, 1.4])

    # ── LEFT PANEL ────────────────────────────────────────────────────────
    with left:
        st.markdown(f"""
        <div class="lpanel">
          <div class="arch-label">ARCHIVE_01<br>OPERATOR_SESSION_ACTIVE</div>

          <div class="side-nav-item active">&#9632;&nbsp;&nbsp;INTELLIGENCE</div>
          <div class="side-nav-item">&#9632;&nbsp;&nbsp;ARCHIVE</div>
          <div class="side-nav-item">&#9632;&nbsp;&nbsp;SURVEILLANCE</div>
          <div class="side-nav-item">&#9632;&nbsp;&nbsp;TACTICAL</div>
          <div class="side-nav-item">&#9632;&nbsp;&nbsp;SETTINGS</div>

          <div style="margin-top:1.5rem">
            <div class="gti-status-row">
              <span class="gti-sys-lbl">SYSTEM_STATUS: GTI_INDEX</span>
            </div>
            <div class="gti-mega">{score_100:.1f}</div>
            <div style="margin-top:6px">
              <span class="gti-badge {lev_cls}">{lev_lbl}</span>
            </div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.62rem;
                        color:var(--amber);margin-top:4px">
              {avg_tone:+.1f}% (24H)
            </div>
          </div>

          <div class="sec-hdr" style="margin-top:1.2rem">SIGNAL_COMPONENTS</div>
        </div>
        """, unsafe_allow_html=True)

        # Signal components rendered as Streamlit metrics (styled via CSS)
        conflict_norm = min(conflict_ct / max(conflict_ct + 1, 1) * 100, 100)
        tone_norm_pct = round(max(0, min(100, (-avg_tone + 100.0) / 2.0)), 1)
        vader_norm = round(((-vader_avg + 1) / 2) * 100, 2)

        def _sig(name, val, bar_pct, desc, col):
            pct = min(bar_pct, 100)
            return f"""
            <div class="sig-block">
              <div style="display:flex;justify-content:space-between;align-items:flex-start">
                <div class="sig-name">{name}</div>
                <div class="sig-val">{val}</div>
              </div>
              <div class="sig-bar-track">
                <div class="sig-bar-fill" style="width:{pct:.0f}%;background:{col}"></div>
              </div>
              <div class="sig-desc">{desc}</div>
            </div>
            """

        conflict_desc = "Escalation detected. Kinetic events above threshold." if conflict_ct > 5 else "Conflict events within normal range."
        tone_desc = "Negative media tone dominant." if avg_tone < 0 else "Neutral/defensive posture observed."
        vader_desc = "Social clusters showing negative recovery trends." if vader_avg < 0 else "Positive signal aggregate detected."
        vol_desc = f"VOLATILITY: {vol_pred} · {vol_conf:.0%} confidence"
        vol_col = NEG if vol_pred == "HIGH" else POS
        vol_bar_html = ''.join(f'<div style="flex:1;height:10px;background:{NEG if i<int(vol_conf*5) else "var(--hover)"};margin-right:2px"></div>' for i in range(5))

        st.markdown(f"""
        <div style="padding:0 0.9rem">
          {_sig("CONFLICT", f"{conflict_ct}", conflict_norm, conflict_desc, NEG)}
          {_sig("TONE_INDEX", f"{tone_norm_pct:.1f}", tone_norm_pct, tone_desc, AMBER)}
          {_sig("VADER_SENTIMENT", f"{vader_avg:+.2f}", abs(vader_norm), vader_desc, AMBER_DIM)}
          <div class="sig-block" style="border-left:3px solid {vol_col}">
            <div style="display:flex;justify-content:space-between;align-items:center">
              <div class="sig-name">VOLATILITY</div>
              <div class="gti-badge {'gb-high' if vol_pred=='HIGH' else 'gb-low'}">{vol_pred}</div>
            </div>
            <div style="display:flex;gap:3px;margin-top:7px">
              {vol_bar_html}
            </div>
          </div>
        </div>
        <div style="padding:0 0.9rem;margin-top:0.8rem">
          <div class="sec-hdr">RISK LEGEND</div>
          <div class="risk-row"><div class="risk-pip" style="background:#b22020"></div>CRITICAL_THREAT (75-100)</div>
          <div class="risk-row"><div class="risk-pip" style="background:#8b2800"></div>ELEVATED_WATCH (40-74)</div>
          <div class="risk-row"><div class="risk-pip" style="background:#1e3a2a"></div>NOMINAL_STABLE (0-39)</div>
        </div>
        <div style="padding:0 0.9rem;margin-top:1.2rem">
          <div class="cta-btn">INITIATE_SCAN</div>
        </div>
        """, unsafe_allow_html=True)

    # ── CENTER PANEL ──────────────────────────────────────────────────────
    with center:
        st.markdown('<div class="cpanel">', unsafe_allow_html=True)
        st.markdown(
            '<div style="font-family:\'Barlow Condensed\',sans-serif;font-size:2.8rem;'
            'font-weight:700;letter-spacing:0.10em;color:var(--txt-hi);line-height:1;'
            'margin-bottom:2px">EARTH PULSE</div>'
            '<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.65rem;'
            'letter-spacing:0.15em;color:var(--txt-dim);margin-bottom:0.8rem">'
            'REAL-TIME_GEOPOLITICAL_FEED</div>',
            unsafe_allow_html=True
        )

        fig_globe = build_choropleth_globe(country_df, proj_type="orthographic",
                                           proj_lon=20.0, proj_lat=20.0, height=480)
        if _HAS_PLOTLY_EVENTS:
            clicked = plotly_events(fig_globe, click_event=True,
                                    override_height=480, key="globe_click_tab1")
            if clicked:
                loc = clicked[0].get("location", "")
                if loc and loc != st.session_state.get("selected_country_iso3"):
                    st.session_state["selected_country_iso3"] = loc
                    st.session_state["selected_country_name"] = ISO3_TO_COUNTRY_NAME.get(loc, loc)
                    st.rerun()
        else:
            st.plotly_chart(fig_globe, use_container_width=True,
                            config={"displayModeBar": False}, key="globe_chart_tab1")

        n_countries = len(country_df) if not country_df.empty else 0
        st.markdown(
            f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.58rem;'
            f'color:var(--txt-dim);text-align:center;margin:-4px 0 8px">'
            f'COORDINATE_GRID_ACTIVE_V4 · {n_countries} COUNTRIES · GDELT 48H</div>',
            unsafe_allow_html=True
        )

        # Latest Headlines
        st.markdown('<div class="sec-hdr">LATEST HEADLINES</div>', unsafe_allow_html=True)
        gdf_all = build_geo_df(news_df) if not news_df.empty else pd.DataFrame()
        if not gdf_all.empty:
            html = '<div class="news-scroll">'
            for _, row in gdf_all.head(24).iterrows():
                lbl  = row["label"]
                comp = row["compound"]
                src  = row["source"][:18]
                pub  = row["pub"]
                ttl  = row["title"]
                dot_c = POS if lbl=="positive" else (NEG if lbl=="negative" else NEU_COL)
                sc    = "sp" if comp>0.05 else ("sn" if comp<-0.05 else "sz")
                sc_txt = f"+{comp:.2f}" if comp > 0 else f"{comp:.2f}"
                html += (f'<div class="ni">'
                         f'<div class="n-dot" style="background:{dot_c}"></div>'
                         f'<div style="flex:1">'
                         f'<div class="n-title">{ttl}</div>'
                         f'<div class="n-meta">{pub} UTC &nbsp;&bull;&nbsp; {src}</div>'
                         f'</div>'
                         f'<div class="n-score {sc}">{sc_txt}</div>'
                         f'</div>')
            html += '</div>'
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.markdown(
                '<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.65rem;'
                'color:var(--txt-dim);padding:1.5rem;text-align:center">'
                'NO FEED DATA — START SCHEDULER</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # ── RIGHT PANEL ───────────────────────────────────────────────────────
    with right:
        st.markdown('<div class="rpanel">', unsafe_allow_html=True)

        # GTI HISTORY CHART — ALWAYS AT TOP
        st.markdown('<div class="sec-hdr">48H GTI HISTORY</div>', unsafe_allow_html=True)
        if not gti_df.empty:
            fig_gti = go.Figure()
            fig_gti.add_hrect(y0=0,  y1=35,  fillcolor="rgba(157,211,170,0.03)", line_width=0)
            fig_gti.add_hrect(y0=35, y1=60,  fillcolor="rgba(255,184,103,0.03)", line_width=0)
            fig_gti.add_hrect(y0=60, y1=100, fillcolor="rgba(255,180,171,0.04)", line_width=0)
            fig_gti.add_trace(go.Scatter(
                x=gti_df["timestamp"], y=gti_df["gti_score"] * 100,
                mode="lines", line=dict(color=AMBER, width=2),
                fill="tozeroy", fillcolor="rgba(255,184,103,0.07)",
            ))
            fig_gti.add_hline(y=35, line_dash="dot", line_color="rgba(157,211,170,0.3)", line_width=1)
            fig_gti.add_hline(y=60, line_dash="dot", line_color="rgba(255,184,103,0.3)", line_width=1)
            fig_gti.update_layout(**PLOT_BASE, margin=_M8, height=220,
                xaxis={**_AX}, yaxis=dict(range=[0,100], **_AX),
                showlegend=False, hovermode="x unified")
            st.plotly_chart(fig_gti, use_container_width=True,
                            config={"displayModeBar":False}, key="gti_chart_tab1")
        else:
            st.markdown(
                '<div style="height:80px;display:flex;align-items:center;justify-content:center;'
                'font-family:JetBrains Mono,monospace;font-size:0.62rem;color:var(--txt-dim)">'
                'NO GTI DATA</div>', unsafe_allow_html=True)

        st.markdown('<div style="margin-top:0.8rem"></div>', unsafe_allow_html=True)

        selected_iso3 = st.session_state.get("selected_country_iso3")

        if selected_iso3:
            country_name = st.session_state.get("selected_country_name", selected_iso3)
            if not country_df.empty and selected_iso3 in country_df["iso3"].values:
                crow = country_df[country_df["iso3"] == selected_iso3].iloc[0]
                ctension = crow["tension"]
                c_conflicts = int(crow["conflict_ct"])
                c_events    = int(crow["total_events"])
                c_tone      = float(crow["avg_tone"])
            else:
                ctension, c_conflicts, c_events, c_tone = 0, 0, 0, 0.0
            c_lbl, c_cls, c_col = gti_meta(ctension)

            st.markdown(f"""
            <div class="c-name">{country_name.upper()}</div>
            <div style="margin-bottom:0.8rem">
              <span class="gti-badge {c_cls}">{c_lbl} · {ctension:.0f}/100</span>
            </div>
            <div style="background:var(--card);padding:0.6rem 0.8rem;margin-bottom:0.5rem">
              <div class="detail-row">
                <span style="color:var(--txt-dim)">CONFLICTS</span>
                <span style="color:{NEG};font-weight:700">{c_conflicts}</span>
              </div>
              <div class="detail-row">
                <span style="color:var(--txt-dim)">EVENTS (48H)</span>
                <span style="color:var(--txt-hi)">{c_events}</span>
              </div>
              <div class="detail-row">
                <span style="color:var(--txt-dim)">AVG_TONE</span>
                <span style="color:{NEG if c_tone<0 else POS}">{c_tone:+.2f}</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="sec-hdr">MARKET SIGNALS</div>', unsafe_allow_html=True)
            kws = ISO3_TO_COUNTRY_KEYWORDS.get(selected_iso3, [])
            if kws and not news_df.empty:
                pattern = "|".join(kws)
                country_news = news_df[news_df["title"].str.lower().str.contains(pattern, na=False, regex=True)]
            else:
                country_news = news_df.head(20) if not news_df.empty else pd.DataFrame()

            country_impacts = analyze_impact(country_news)
            html = ""
            shown = 0
            for item in country_impacts:
                if item["match_ct"] == 0:
                    continue
                s = item["signal"]
                arr = "↑" if s=="up" else ("↓" if s=="down" else "⚡" if s=="watch" else "—")
                html += (f'<div class="acard acard-{s}">'
                         f'<div>'
                         f'<div class="a-pair">{item["asset"]}</div>'
                         f'<div class="a-type">{item["type"]}</div>'
                         f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.58rem;'
                         f'color:var(--txt-dim);margin-top:4px">{item["reason"][:48]}</div>'
                         f'</div>'
                         f'<div><span class="a-sig {SIG_CLS[s]}">{arr}</span></div>'
                         f'</div>')
                shown += 1
                if shown >= 4:
                    break
            if not html:
                html = '<div style="color:var(--txt-dim);font-size:0.62rem">No matching signals</div>'
            st.markdown(html, unsafe_allow_html=True)

            fips = ISO3_TO_FIPS.get(selected_iso3, "")
            if fips:
                events_df = load_country_headlines(fips, n=8)
                if not events_df.empty:
                    st.markdown('<div class="sec-hdr" style="margin-top:0.8rem">RISK FACTORS</div>',
                                unsafe_allow_html=True)
                    risk_html = ""
                    for _, ev in events_df.iterrows():
                        arc = classify_arc_type(str(ev.get("event_code", "")))
                        gs  = ev.get("goldstein_scale", 0)
                        try: gs = float(gs)
                        except: gs = 0.0
                        sev = "CRITICAL" if gs < -8 else ("HIGH" if gs < -5 else "MEDIUM")
                        sev_col = NEG if sev=="CRITICAL" else (AMBER if sev=="HIGH" else NEU_COL)
                        risk_html += (f'<div style="display:flex;gap:6px;padding:4px 0;'
                                      f'border-bottom:1px solid var(--ghost);'
                                      f'font-family:JetBrains Mono,monospace;font-size:0.60rem">'
                                      f'<span style="color:{sev_col};font-weight:700;min-width:52px">{sev}</span>'
                                      f'<span style="color:var(--txt-mid)">{arc} · GS {gs:.1f}</span>'
                                      f'</div>')
                    st.markdown(risk_html, unsafe_allow_html=True)

            if st.button("← BACK", key="back_btn_tab1"):
                st.session_state["selected_country_iso3"] = None
                st.session_state["selected_country_name"] = None
                st.rerun()

        else:
            st.markdown('<div class="sec-hdr">LATEST HEADLINES</div>',
                        unsafe_allow_html=True)
            for item in impacts[:5]:
                s = item["signal"]
                arr = "↑" if s=="up" else ("↓" if s=="down" else "⚡" if s=="watch" else "—")
                arrow_col = POS if s=="up" else (NEG if s=="down" else AMBER if s=="watch" else NEU_COL)
                st.markdown(
                    f'<div class="acard acard-{s}">'
                    f'<div>'
                    f'<div class="a-pair">{item["asset"]}</div>'
                    f'<div class="a-type">{item["type"]} · {item["name"]}</div>'
                    f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.58rem;'
                    f'color:var(--txt-dim);margin-top:4px;line-height:1.4">'
                    f'{item["reason"][:52]}</div>'
                    f'</div>'
                    f'<span class="a-sig {SIG_CLS[s]}">{arr}</span>'
                    f'</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
#  TAB 2 — GEO MAP
# ═══════════════════════════════════════════════════════════════════════════
with tab2:
    left2, center2, right2 = st.columns([1, 3.5, 1.15])

    with left2:
        st.markdown(f"""
        <div class="lpanel">
          <div class="arch-label">ARCHIVE_01<br>OPERATOR_SESSION_ACTIVE</div>
          <div class="side-nav-item">&#9632;&nbsp;&nbsp;INTELLIGENCE</div>
          <div class="side-nav-item active">&#9632;&nbsp;&nbsp;GEO MAP</div>
          <div class="side-nav-item">&#9632;&nbsp;&nbsp;SURVEILLANCE</div>
          <div class="side-nav-item">&#9632;&nbsp;&nbsp;TACTICAL</div>
          <div class="side-nav-item">&#9632;&nbsp;&nbsp;SETTINGS</div>

          <div class="sec-hdr" style="margin-top:1.2rem">RISK_LEGEND</div>
          <div style="padding:0 0.4rem">
            <div class="risk-row"><div class="risk-pip" style="background:#b22020"></div>CRITICAL_THREAT (75-100)</div>
            <div class="risk-row"><div class="risk-pip" style="background:#8b2800"></div>ELEVATED_WATCH (40-74)</div>
            <div class="risk-row"><div class="risk-pip" style="background:#1e3a2a"></div>NOMINAL_STABLE (0-39)</div>
          </div>

          <div class="sec-hdr" style="margin-top:1rem">SUMMARY_STATS</div>
          <div class="dcard">
            <div class="dcard-lbl">TOTAL HEADLINES</div>
            <div class="dcard-val">{total_news}</div>
            <div class="dcard-sub">LAST 80 ARTICLES</div>
          </div>
          <div class="dcard">
            <div class="dcard-lbl">SENTIMENT SPLIT</div>
            <div style="display:flex;gap:0.8rem;margin-top:4px">
              <div><div style="font-family:'JetBrains Mono',monospace;font-size:0.9rem;color:{POS}">{pos_ct}</div>
                   <div class="dcard-sub">POS</div></div>
              <div><div style="font-family:'JetBrains Mono',monospace;font-size:0.9rem;color:{NEU_COL}">{neu_ct}</div>
                   <div class="dcard-sub">NEU</div></div>
              <div><div style="font-family:'JetBrains Mono',monospace;font-size:0.9rem;color:{NEG}">{neg_ct}</div>
                   <div class="dcard-sub">NEG</div></div>
            </div>
          </div>
          <div class="dcard dcard-hi">
            <div class="dcard-lbl">ACTIVE CONFLICTS</div>
            <div class="dcard-val" style="color:{NEG}">{conflict_ct}</div>
            <div class="dcard-sub">GDELT · 6H WINDOW</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Arc type filter
        st.markdown('<div style="padding:0 0.9rem;background:var(--panel);'
                    'border-right:1px solid var(--ghost)">', unsafe_allow_html=True)
        arc_filter = st.multiselect(
            "ARC_TYPES",
            options=["Military", "Sanctions", "Trade", "Diplomatic"],
            default=st.session_state["arc_filter"],
            key="arc_filter_widget",
        )
        st.session_state["arc_filter"] = arc_filter
        st.markdown('</div>', unsafe_allow_html=True)

    with center2:
        st.markdown('<div class="cpanel">', unsafe_allow_html=True)
        st.markdown(
            '<div style="font-family:\'Barlow Condensed\',sans-serif;font-size:1.8rem;'
            'font-weight:700;letter-spacing:0.08em;color:var(--txt-hi);margin-bottom:0.4rem">'
            'TACTICAL MAP</div>', unsafe_allow_html=True)

        if not gdelt_raw_df.empty and arc_filter:
            gdelt_filtered = gdelt_raw_df.copy()
            gdelt_filtered["arc_type"] = gdelt_filtered["event_code"].apply(classify_arc_type)
            gdelt_filtered = gdelt_filtered[gdelt_filtered["arc_type"].isin(arc_filter)]
            country_df_filtered = build_country_tension_df(gdelt_filtered)
        elif not arc_filter:
            country_df_filtered = pd.DataFrame()
        else:
            country_df_filtered = country_df.copy()

        fig_map2 = build_choropleth_globe(country_df_filtered, proj_type="natural earth", height=500)

        if _HAS_PLOTLY_EVENTS:
            clicked_map = plotly_events(fig_map2, click_event=True,
                                        override_height=500, key="map_click_tab2")
            if clicked_map:
                loc = clicked_map[0].get("location", "")
                if loc:
                    st.session_state["selected_country_iso3"] = loc
                    st.session_state["selected_country_name"] = ISO3_TO_COUNTRY_NAME.get(loc, loc)
        else:
            st.plotly_chart(fig_map2, use_container_width=True,
                            config={"displayModeBar": False}, key="map_chart_tab2")

        n_filtered = len(country_df_filtered) if not country_df_filtered.empty else 0
        arc_label  = ", ".join(arc_filter) if arc_filter else "none"
        st.markdown(
            f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.56rem;'
            f'color:var(--txt-dim);text-align:center;margin:-4px 0 8px">'
            f'{n_filtered} COUNTRIES · FILTER: {arc_label}</div>', unsafe_allow_html=True)

        # City breakdown bar chart
        if not news_df.empty:
            gdf3 = build_geo_df(news_df)
            if not gdf3.empty:
                city_counts = gdf3.groupby("city").agg(
                    total=("compound","count"),
                    avg_sent=("compound","mean")
                ).reset_index().sort_values("total", ascending=False).head(12)
                bar_colors = city_counts["avg_sent"].apply(
                    lambda c: POS if c>0.05 else (NEG if c<-0.05 else NEU_COL))
                st.markdown('<div class="sec-hdr">ACTIVE CONFLICT INDICATORS</div>',
                            unsafe_allow_html=True)
                fig_bar = go.Figure(go.Bar(
                    x=city_counts["city"], y=city_counts["total"],
                    marker_color=bar_colors,
                    text=city_counts["avg_sent"].apply(lambda x: f"{x:+.2f}"),
                    textposition="outside",
                    textfont=dict(size=9, color=NEU_COL),
                ))
                fig_bar.update_layout(**PLOT_BASE, margin=_M8, height=200,
                    yaxis=dict(**_AX), xaxis=dict(**_AX))
                st.plotly_chart(fig_bar, use_container_width=True,
                                config={"displayModeBar":False}, key="city_bar_tab2")
        st.markdown('</div>', unsafe_allow_html=True)

    with right2:
        st.markdown('<div class="rpanel">', unsafe_allow_html=True)
        # Show top tension countries
        st.markdown('<div class="sec-hdr">TOP TENSION COUNTRIES</div>', unsafe_allow_html=True)
        if not country_df.empty:
            top_countries = country_df.sort_values("tension", ascending=False).head(8)
            for _, row in top_countries.iterrows():
                name = ISO3_TO_COUNTRY_NAME.get(row["iso3"], row["iso3"])
                lbl_c, cls_c, col_c = gti_meta(float(row["tension"]))
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;align-items:center;
                            padding:0.45rem 0.5rem;background:var(--card);margin-bottom:0.3rem">
                  <div>
                    <div style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;
                                font-weight:600;color:var(--txt-hi)">{name}</div>
                    <div style="font-family:'Space Grotesk',sans-serif;font-size:0.54rem;
                                letter-spacing:0.10em;color:var(--txt-dim)">{row['iso3']}</div>
                  </div>
                  <div style="font-family:'JetBrains Mono',monospace;font-size:0.80rem;
                              font-weight:600;color:{col_c}">{row['tension']:.0f}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(
                '<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.62rem;'
                'color:var(--txt-dim)">NO GDELT DATA</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
#  TAB 3 — AI SIGNALS
# ═══════════════════════════════════════════════════════════════════════════
with tab3:
    c1, c2, c3 = st.columns([1.2, 2.5, 1.5])

    # ── LEFT: Model Output ────────────────────────────────────────────────
    with c1:
        vol_col = NEG if vol_pred == "HIGH" else POS
        dir_col = POS if dir_pred == "UP" else NEG
        vol_pct = f"{vol_conf*100:.0f}%"
        dir_pct = f"{dir_conf*100:.0f}%"
        # feature importance (fixed weights from GTI model)
        feats = [
            ("MACRO_STABILITY",    42, min(score_100/2 + 20, 100)),
            ("GEOPOLITICAL_RISK",  28, min(score_100 * 0.8, 100)),
            ("SENTIMENT_AGGREGATE",15, abs(vader_avg)*100),
            ("LIQUIDITY_DEPTH",    10, 50.0),
            ("SOCIAL_VOLUME",       5, min(total_news/100*50, 100)),
        ]

        feat_html = ""
        for fn, fw, fv in feats:
            feat_html += f"""
            <div class="feat-row">
              <div class="feat-lbl"><span>{fn}</span><span class="feat-pct">{fw}%</span></div>
              <div class="feat-track"><div class="feat-fill" style="width:{min(fv,100):.0f}%"></div></div>
            </div>"""

        st.markdown(f"""
        <div class="lpanel">
          <div class="arch-label">ARCHIVE_01<br>OPERATOR_SESSION_ACTIVE</div>
          <div class="nav-group-lbl">PRIMARY MODULES</div>
          <div class="side-nav-item active">&#9632;&nbsp;&nbsp;INTELLIGENCE</div>
          <div class="side-nav-item">&#9632;&nbsp;&nbsp;ARCHIVE</div>
          <div class="side-nav-item">&#9632;&nbsp;&nbsp;SURVEILLANCE</div>
          <div class="side-nav-item">&#9632;&nbsp;&nbsp;TACTICAL</div>
          <div class="side-nav-item">&#9632;&nbsp;&nbsp;SETTINGS</div>

          <div class="sec-hdr" style="margin-top:1.2rem">MODEL OUTPUT</div>

          <div class="dcard dcard-watch">
            <div class="dcard-lbl">PROJECTED VOLATILITY</div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:1.6rem;
                        font-weight:700;color:{vol_col};margin:4px 0">{vol_conf*100:.2f}%</div>
            <div class="dcard-sub">→ {vol_pred}</div>
          </div>

          <div class="dcard dcard-ok">
            <div class="dcard-lbl">MARKET DIRECTION</div>
            <div style="font-family:'Barlow Condensed',sans-serif;font-size:1.6rem;
                        font-weight:700;color:{dir_col};letter-spacing:0.06em;margin:4px 0">
              {'▲' if dir_pred=='UP' else '▼'} {dir_pred}</div>
            <div class="dcard-sub">{dir_pct} CONF.</div>
          </div>

          <div class="sec-hdr" style="margin-top:0.8rem">GTI INPUT FEATURES</div>
          <div style="padding:0 0.3rem">
            {feat_html}
          </div>

          <div style="margin-top:1rem;padding:0 0.3rem">
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.56rem;
                        color:var(--txt-dim)">LAST_UPDATE: {now_str}</div>
          </div>

          <div style="padding:0 0.3rem;margin-top:1rem">
            <div class="cta-btn">INITIATE SCAN &#9654;</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── CENTER: Charts ────────────────────────────────────────────────────
    with c2:
        st.markdown('<div class="cpanel">', unsafe_allow_html=True)

        # GTI Component Breakdown
        st.markdown(
            '<div style="font-family:\'Newsreader\',serif;font-size:1.2rem;font-weight:600;'
            'color:var(--txt-hi);margin-bottom:2px">GTI Component Breakdown</div>'
            '<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.60rem;'
            'letter-spacing:0.12em;color:var(--txt-dim);margin-bottom:0.6rem">'
            'TIME-SERIES ATTRIBUTION ANALYSIS [24H]</div>',
            unsafe_allow_html=True
        )

        if not gti_df.empty:
            fig_comp = go.Figure()
            fig_comp.add_trace(go.Scatter(
                x=gti_df["timestamp"], y=gti_df["gti_score"] * 100,
                mode="lines", name="MACRO",
                line=dict(color=AMBER, width=2.5),
            ))
            if "avg_tone" in gti_df.columns:
                tn = ((-gti_df["avg_tone"]+100)/200).clip(0,1) * 100
                fig_comp.add_trace(go.Scatter(x=gti_df["timestamp"], y=tn,
                    mode="lines", name="QUANT",
                    line=dict(color=POS, width=1.5)))
            if "conflict_ct" in gti_df.columns:
                mx = max(gti_df["conflict_ct"].max(), 1)
                fig_comp.add_trace(go.Scatter(x=gti_df["timestamp"],
                    y=(gti_df["conflict_ct"]/mx).clip(0,1) * 100,
                    mode="lines", name="CONFLICT",
                    line=dict(color=NEG, width=1.5, dash="dot")))
            fig_comp.update_layout(**PLOT_BASE, margin=_M12, height=270,
                xaxis={**_AX},
                yaxis=dict(range=[0,100], **_AX),
                legend=dict(orientation="h", y=1.12, font=dict(size=9, color=NEU_COL),
                            bgcolor="rgba(0,0,0,0)"),
                hovermode="x unified")
            st.plotly_chart(fig_comp, use_container_width=True,
                            config={"displayModeBar":False}, key="ai_comp_chart")
        else:
            st.markdown(
                '<div style="height:100px;display:flex;align-items:center;justify-content:center;'
                'font-family:JetBrains Mono,monospace;font-size:0.62rem;color:var(--txt-dim)">'
                'AWAITING DATA</div>', unsafe_allow_html=True)

        # Prediction history
        st.markdown(
            '<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.60rem;'
            'letter-spacing:0.14em;text-transform:uppercase;color:var(--txt-dim);'
            'margin:0.8rem 0 0.4rem">PREDICTION HISTORY [SIMULATION MODE]</div>',
            unsafe_allow_html=True
        )
        if not pred_h.empty:
            fig_pred = go.Figure()
            fig_pred.add_trace(go.Scatter(
                x=pred_h["timestamp"], y=pred_h["vol_prob"],
                mode="lines+markers", name="VOL PROB",
                line=dict(color=NEG, width=1.5), marker=dict(size=3),
            ))
            fig_pred.add_trace(go.Scatter(
                x=pred_h["timestamp"], y=pred_h["dir_prob"],
                mode="lines+markers", name="DIR PROB",
                line=dict(color=POS, width=1.5), marker=dict(size=3),
            ))
            fig_pred.add_hline(y=0.5, line_dash="dot",
                               line_color="rgba(255,255,255,0.1)", line_width=1)
            fig_pred.update_layout(**PLOT_BASE, margin=_M8, height=200,
                xaxis={**_AX}, yaxis=dict(range=[0,1], **_AX),
                legend=dict(orientation="h", y=1.1, font=dict(size=9, color=NEU_COL),
                            bgcolor="rgba(0,0,0,0)"),
                hovermode="x unified")
            st.plotly_chart(fig_pred, use_container_width=True,
                            config={"displayModeBar":False}, key="ai_pred_chart")
        else:
            st.markdown(
                '<div style="height:120px;background:var(--card);display:flex;flex-direction:column;'
                'align-items:center;justify-content:center;margin-bottom:0.8rem">'
                '<div style="font-size:2rem;opacity:0.3">&#9730;</div>'
                '<div style="font-family:JetBrains Mono,monospace;font-size:0.62rem;color:var(--txt-dim);'
                'text-align:center;margin-top:6px;line-height:1.6">'
                'HISTORY LOG EMPTY.<br>INITIATE TACTICAL SCAN TO POPULATE<br>PREDICTION DATASET.</div>'
                '</div>', unsafe_allow_html=True)

        # Sentiment momentum bar
        st.markdown(
            f'<div style="display:flex;justify-content:space-between;margin:0.3rem 0">'
            f'<span style="font-family:JetBrains Mono,monospace;font-size:0.60rem;color:var(--txt-dim)">SENTIMENT MOMENTUM</span>'
            f'<span style="font-family:JetBrains Mono,monospace;font-size:0.60rem">'
            f'<span style="color:{POS}">{pos_ct}% POSITIVE</span> / '
            f'<span style="color:var(--neutral)">{neu_ct} NEUTRAL</span> / '
            f'<span style="color:{NEG}">{neg_ct}% NEGATIVE</span></span>'
            f'</div>',
            unsafe_allow_html=True
        )
        fig_sent = go.Figure()
        total_s = max(pos_ct + neg_ct + neu_ct, 1)
        fig_sent.add_trace(go.Bar(x=[pos_ct/total_s*100], y=[""], orientation="h",
            name="POS", marker_color="rgba(157,211,170,0.7)"))
        fig_sent.add_trace(go.Bar(x=[neu_ct/total_s*100], y=[""], orientation="h",
            name="NEU", marker_color="rgba(138,142,160,0.35)"))
        fig_sent.add_trace(go.Bar(x=[neg_ct/total_s*100], y=[""], orientation="h",
            name="NEG", marker_color="rgba(255,180,171,0.7)"))
        fig_sent.update_layout(**PLOT_BASE, barmode="stack", height=55,
            showlegend=False, margin=dict(l=4,r=4,t=2,b=2),
            yaxis=dict(showticklabels=False, **{k:v for k,v in _AX.items()}),
            xaxis=dict(showticklabels=False, showgrid=False, zeroline=False))
        st.plotly_chart(fig_sent, use_container_width=True,
                        config={"displayModeBar":False}, key="ai_sent_chart")

        st.markdown('</div>', unsafe_allow_html=True)

    # ── RIGHT: Full impact analysis ───────────────────────────────────────
    with c3:
        st.markdown('<div class="rpanel">', unsafe_allow_html=True)
        st.markdown(
            '<div style="font-family:\'Barlow Condensed\',sans-serif;font-size:1.1rem;'
            'font-weight:700;letter-spacing:0.08em;color:var(--txt-hi);margin-bottom:0.6rem">'
            'FULL IMPACT<br>ANALYSIS</div>', unsafe_allow_html=True)

        # Group by signal / category
        categories = {
            "ASSET CATEGORY: BULLISH": [i for i in impacts if i["signal"]=="up"],
            "ASSET CATEGORY: NEUTRAL": [i for i in impacts if i["signal"]=="watch" or i["signal"]=="neutral"],
            "ASSET CATEGORY: BEARISH": [i for i in impacts if i["signal"]=="down"],
        }
        cat_badges = {
            "ASSET CATEGORY: BULLISH": ("SIG_HIGH",  "rgba(157,211,170,0.12)", POS),
            "ASSET CATEGORY: NEUTRAL": ("SIG_WATCH",  "rgba(255,184,103,0.12)", AMBER),
            "ASSET CATEGORY: BEARISH": ("SIG_EXTREME","rgba(255,180,171,0.12)", NEG),
        }
        for cat_lbl, items in categories.items():
            if not items:
                continue
            badge_txt, badge_bg, badge_fg = cat_badges[cat_lbl]
            st.markdown(
                f'<div style="display:flex;justify-content:space-between;align-items:center;'
                f'margin:0.7rem 0 0.3rem">'
                f'<div style="font-family:Space Grotesk,sans-serif;font-size:0.55rem;'
                f'letter-spacing:0.14em;text-transform:uppercase;color:var(--txt-dim)">{cat_lbl}</div>'
                f'<div style="font-family:JetBrains Mono,monospace;font-size:0.55rem;'
                f'padding:2px 6px;background:{badge_bg};color:{badge_fg}">{badge_txt}</div>'
                f'</div>', unsafe_allow_html=True
            )
            for item in items:
                s = item["signal"]
                arr = "↗" if s=="up" else ("↘" if s=="down" else "—")
                arr_c = POS if s=="up" else (NEG if s=="down" else NEU_COL)
                st.markdown(
                    f'<div class="impact-row">'
                    f'<div>'
                    f'<div class="impact-sym">{item["asset"]}</div>'
                    f'<div style="font-family:Space Grotesk,sans-serif;font-size:0.50rem;'
                    f'letter-spacing:0.10em;color:var(--txt-dim)">{item["type"]}</div>'
                    f'</div>'
                    f'<div style="font-family:JetBrains Mono,monospace;font-size:1rem;'
                    f'font-weight:700;color:{arr_c}">{arr}</div>'
                    f'</div>', unsafe_allow_html=True
                )

        st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
#  TAB 4 — MARKET
# ═══════════════════════════════════════════════════════════════════════════
with tab4:
    def mkt_tile(df: pd.DataFrame, sym: str, sub: str):
        if df.empty:
            return f"""
            <div class="tac-card tac-card-active">
              <div class="mkt-hdr">
                <div><div class="mkt-sym">{sym}</div><div class="mkt-sub">{sub}</div></div>
                <div class="gti-badge gb-mod">NO DATA</div>
              </div>
              <div class="mkt-price">—</div>
            </div>"""
        try:
            last  = float(df["close"].iloc[-1])
            first = float(df["close"].iloc[0])
            chg   = (last-first)/first*100
            arrow = "▲" if chg>=0 else "▼"
            chg_cls = "mkt-chg-up" if chg>=0 else "mkt-chg-dn"
            return f"""
            <div class="tac-card tac-card-active">
              <div class="mkt-hdr">
                <div><div class="mkt-sym">{sym}</div><div class="mkt-sub">{sub}</div></div>
              </div>
              <div class="mkt-price">{last:.2f}</div>
              <div class="{chg_cls}">{arrow} {abs(chg):.2f}%&nbsp;<span style="font-size:0.58rem;
                font-weight:400;opacity:0.7">48H</span></div>
            </div>"""
        except Exception:
            return f'<div class="tac-card"><div class="mkt-sym">{sym}</div><div class="mkt-price">—</div></div>'

    mc1, mc2, mc3 = st.columns(3)
    with mc1:
        st.markdown(mkt_tile(spy_df, "SPY", "S&P 500 ETF · TACTICAL SURVEILLANCE"),
                    unsafe_allow_html=True)
    with mc2:
        st.markdown(mkt_tile(vix_df, "VOLATILITY · VIX", "CBOE FEAR GAUGE"),
                    unsafe_allow_html=True)
    with mc3:
        st.markdown(mkt_tile(gld_df, "COMMODITY · GLD", "GOLD TRUST ETF"),
                    unsafe_allow_html=True)

    # SPY Candlestick
    st.markdown('<div style="padding:0 0.5rem">', unsafe_allow_html=True)
    st.markdown('<div class="sec-hdr">SPY — S&P 500 ETF · TACTICAL SURVEILLANCE</div>',
                unsafe_allow_html=True)
    if not spy_df.empty:
        try:
            fig_spy = go.Figure(go.Candlestick(
                x=spy_df["timestamp"],
                open=spy_df["open"], high=spy_df["high"],
                low=spy_df["low"],   close=spy_df["close"],
                increasing=dict(line=dict(color=POS), fillcolor="rgba(157,211,170,0.2)"),
                decreasing=dict(line=dict(color=NEG), fillcolor="rgba(255,180,171,0.2)"),
            ))
            if "volume" in spy_df.columns:
                fig_spy.add_trace(go.Bar(
                    x=spy_df["timestamp"], y=spy_df["volume"],
                    name="Volume", yaxis="y2",
                    marker_color="rgba(255,184,103,0.10)",
                ))
                fig_spy.update_layout(yaxis2=dict(overlaying="y", side="right",
                    showgrid=False, showticklabels=False,
                    range=[0, spy_df["volume"].max()*5]))
            fig_spy.update_layout(**PLOT_BASE, margin=_M8, height=300,
                xaxis=dict(**_AX, rangeslider_visible=False),
                yaxis={**_AX}, hovermode="x unified")
            st.plotly_chart(fig_spy, use_container_width=True,
                            config={"displayModeBar":False}, key="mkt_spy_chart")
        except Exception:
            st.markdown(
                '<div style="height:200px;background:var(--card);display:flex;'
                'align-items:center;justify-content:center;'
                'font-family:JetBrains Mono,monospace;font-size:0.65rem;color:var(--txt-dim)">'
                'AWAITING HIGH-FIDELITY DATA · INITIATE SCAN</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            '<div style="height:200px;background:var(--card);display:flex;flex-direction:column;'
            'align-items:center;justify-content:center">'
            '<div style="font-size:2rem;opacity:0.3">&#9730;</div>'
            '<div style="font-family:JetBrains Mono,monospace;font-size:0.62rem;color:var(--txt-dim);'
            'text-align:center;margin-top:8px;line-height:1.6">'
            'AWAITING AUTHORISATION FOR HIGH-FIDELITY DATA<br>ANALYSIS. RUN market_fetcher.py</div>'
            '</div>', unsafe_allow_html=True)

    # VIX + GLD side by side
    mv1, mv2 = st.columns(2)
    with mv1:
        st.markdown('<div class="sec-hdr">VIX — VOLATILITY INDEX · 48H</div>',
                    unsafe_allow_html=True)
        if not vix_df.empty:
            try:
                fig_vix = go.Figure()
                fig_vix.add_hrect(y0=0,  y1=20, fillcolor="rgba(157,211,170,0.03)", line_width=0)
                fig_vix.add_hrect(y0=20, y1=30, fillcolor="rgba(255,184,103,0.03)", line_width=0)
                fig_vix.add_hrect(y0=30, y1=100,fillcolor="rgba(255,180,171,0.03)", line_width=0)
                fig_vix.add_trace(go.Scatter(
                    x=vix_df["timestamp"], y=vix_df["close"],
                    mode="lines", line=dict(color=AMBER, width=2),
                    fill="tozeroy", fillcolor="rgba(255,184,103,0.07)",
                ))
                fig_vix.add_hline(y=20, line_dash="dot", line_color="rgba(255,184,103,0.3)", line_width=1)
                fig_vix.add_hline(y=30, line_dash="dot", line_color="rgba(255,180,171,0.3)", line_width=1)
                fig_vix.update_layout(**PLOT_BASE, margin=_M8, height=220,
                    xaxis={**_AX}, yaxis={**_AX}, hovermode="x unified", showlegend=False)
                st.plotly_chart(fig_vix, use_container_width=True,
                                config={"displayModeBar":False}, key="mkt_vix_chart")
            except Exception:
                st.markdown(
                    '<div style="height:120px;background:var(--card);display:flex;align-items:center;'
                    'justify-content:center;font-family:JetBrains Mono,monospace;font-size:0.62rem;'
                    'color:var(--txt-dim)">VIX DATA ERROR</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                '<div style="height:120px;background:var(--card);display:flex;align-items:center;'
                'justify-content:center;font-family:JetBrains Mono,monospace;font-size:0.62rem;'
                'color:var(--txt-dim)">NO VIX DATA</div>', unsafe_allow_html=True)

    with mv2:
        st.markdown('<div class="sec-hdr">GLD — GOLD ETF · 48H</div>', unsafe_allow_html=True)
        if not gld_df.empty:
            try:
                fig_gld = go.Figure()
                fig_gld.add_trace(go.Scatter(
                    x=gld_df["timestamp"], y=gld_df["close"],
                    mode="lines", line=dict(color=AMBER, width=2),
                    fill="tozeroy", fillcolor="rgba(255,184,103,0.07)",
                ))
                if "high" in gld_df.columns and "low" in gld_df.columns:
                    fig_gld.add_trace(go.Scatter(
                        x=pd.concat([gld_df["timestamp"], gld_df["timestamp"][::-1]]),
                        y=pd.concat([gld_df["high"], gld_df["low"][::-1]]),
                        fill="toself", fillcolor="rgba(255,184,103,0.04)",
                        line=dict(color="rgba(0,0,0,0)"), name="H/L band",
                    ))
                fig_gld.update_layout(**PLOT_BASE, margin=_M8, height=220,
                    xaxis={**_AX}, yaxis={**_AX},
                    hovermode="x unified", showlegend=False)
                st.plotly_chart(fig_gld, use_container_width=True,
                                config={"displayModeBar":False}, key="mkt_gld_chart")
            except Exception:
                st.markdown(
                    '<div style="height:120px;background:var(--card);display:flex;align-items:center;'
                    'justify-content:center;font-family:JetBrains Mono,monospace;font-size:0.62rem;'
                    'color:var(--txt-dim)">GLD DATA ERROR</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                '<div style="height:120px;background:var(--card);display:flex;align-items:center;'
                'justify-content:center;font-family:JetBrains Mono,monospace;font-size:0.62rem;'
                'color:var(--txt-dim)">NO GLD DATA</div>', unsafe_allow_html=True)

    # GTI vs SPY scatter
    if not spy_df.empty and not gti_df.empty:
        try:
            st.markdown('<div class="sec-hdr" style="margin-top:0.3rem">'
                        'GTI SCORE vs SPY RETURNS — CORRELATION VIEW</div>',
                        unsafe_allow_html=True)
            spy_ret = spy_df.copy()
            spy_ret["return"] = spy_ret["close"].pct_change() * 100
            spy_ret = spy_ret.dropna(subset=["return"])
            gti_ts = gti_df[["timestamp","gti_score"]].copy()
            gti_ts["timestamp"] = pd.to_datetime(gti_ts["timestamp"])
            spy_ts = spy_ret[["timestamp","return"]].copy()
            spy_ts["timestamp"] = pd.to_datetime(spy_ts["timestamp"])
            merged = pd.merge_asof(spy_ts.sort_values("timestamp"),
                                   gti_ts.sort_values("timestamp"),
                                   on="timestamp", direction="nearest").dropna()
            if not merged.empty:
                scatter_col = merged["return"].apply(lambda r: POS if r>0 else NEG)
                fig_scatter = go.Figure(go.Scatter(
                    x=merged["gti_score"] * 100, y=merged["return"],
                    mode="markers",
                    marker=dict(color=scatter_col, size=6, opacity=0.65,
                                line=dict(width=0.5, color="rgba(255,255,255,0.08)")),
                    hovertemplate="GTI: %{x:.1f}<br>Return: %{y:.3f}%<extra></extra>",
                ))
                fig_scatter.add_vline(x=35, line_dash="dot", line_color="rgba(157,211,170,0.25)", line_width=1)
                fig_scatter.add_vline(x=60, line_dash="dot", line_color="rgba(255,184,103,0.25)", line_width=1)
                fig_scatter.add_hline(y=0,  line_dash="dot", line_color="rgba(255,255,255,0.08)", line_width=1)
                fig_scatter.update_layout(**PLOT_BASE, margin=_M12, height=240,
                    xaxis=dict(title="GTI Score (0–100)", range=[0,100], **_AX),
                    yaxis=dict(title="SPY Return %", **_AX))
                st.plotly_chart(fig_scatter, use_container_width=True,
                                config={"displayModeBar":False}, key="mkt_scatter_chart")
        except Exception:
            pass

    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
#  STATUS BAR
# ═══════════════════════════════════════════════════════════════════════════
next_ref = (now_utc + timedelta(seconds=60)).strftime("%H:%M:%S")
st.markdown(f"""
<div class="statusbar">
  <span class="sb-live">■ SYSTEM_STABLE</span>
  <span><span class="sb-lbl">FRAMEWORK</span>&nbsp;<span class="sb-val">SOVEREIGN INTELLIGENCE V4.0.2</span></span>
  <span><span class="sb-lbl">ENCRYPTION</span>&nbsp;<span class="sb-val">AES256</span></span>
  <span><span class="sb-lbl">GTI</span>&nbsp;<span class="sb-val">{score_100:.1f}</span></span>
  <span><span class="sb-lbl">COUNTRIES</span>&nbsp;<span class="sb-val">{len(country_df) if not country_df.empty else 0}</span></span>
  <span><span class="sb-lbl">ARTICLES</span>&nbsp;<span class="sb-val">{total_news}</span></span>
  <span style="margin-left:auto"><span class="sb-lbl">LATENCY</span>&nbsp;<span class="sb-val">12MS</span>&nbsp;
  &nbsp;<span class="sb-lbl">REFRESH</span>&nbsp;<span class="sb-val">{next_ref} UTC</span></span>
</div>
""", unsafe_allow_html=True)

if time.time() - st.session_state["last_refresh"] > 60:
    st.session_state["last_refresh"] = time.time()
    st.rerun()
