"""
GeoMarket Intelligence — Full Multi-Screen Dashboard v2
========================================================
Inspired by web-code.tech: dark globe-centric UI with multiple pages.

Screens / Tabs:
  1. EARTH PULSE  — Choropleth globe hero + live GTI + news feed + country click
  2. GEO MAP      — Full-screen geographic map with arc-type filters
  3. AI SIGNALS   — Model predictions + GTI components + signal breakdown
  4. MARKET       — SPY / VIX / GLD candlestick charts + currency impact panel

Run:  streamlit run dashboard/app.py
"""

import sqlite3
import time
from datetime import datetime, timedelta
import os

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import requests
import json
import streamlit.components.v1 as components

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

# ── Session state defaults ─────────────────────────────────────────────────
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
#  GLOBAL CSS  —  dark space-age aesthetic matching web-code.tech
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Share+Tech+Mono&family=Orbitron:wght@400;600;800&display=swap');

:root {
  --bg0:    #04080f;
  --bg1:    #080e1a;
  --bg2:    #0c1424;
  --bg3:    #111c30;
  --border: #1b2d45;
  --accent: #00c8ff;
  --green:  #00ff9d;
  --warn:   #ffb800;
  --danger: #ff3b5c;
  --muted:  #3a5070;
  --text:   #a8c4dc;
  --bright: #d8eaf8;
}

html, body, .stApp { background: var(--bg0) !important; color: var(--text) !important; }
* { font-family: 'Rajdhani', sans-serif !important; box-sizing: border-box; }
code, .mono { font-family: 'Share Tech Mono', monospace !important; }

#MainMenu, footer, header, [data-testid="stToolbar"] { visibility: hidden !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stVerticalBlock"] { gap: 0 !important; }
div[data-testid="column"] { padding: 0 !important; }
div[data-testid="stMetric"] { display: none !important; }
.stPlotlyChart { border-radius: 4px; overflow: hidden; background: var(--bg0) !important; }
.js-plotly-plot .plotly .main-svg { background: transparent !important; }
div[data-testid="stCustomComponentV1"] { background: var(--bg0) !important; border: none !important; outline: none !important; }
div[data-testid="stCustomComponentV1"] > iframe { background: var(--bg0) !important; border: none !important; outline: none !important; box-shadow: none !important; }
iframe { border: none !important; outline: none !important; }

/* Multiselect dark theme */
div[data-baseweb="select"] { background: var(--bg2) !important; }
div[data-baseweb="tag"] { background: rgba(0,200,255,0.15) !important; }
.stMultiSelect label { color: var(--muted) !important; font-size: 0.6rem !important; letter-spacing: 0.12em !important; }

/* ──────── NAVBAR ──────── */
.navbar {
  display: flex; align-items: center;
  background: var(--bg1); border-bottom: 1px solid var(--border);
  padding: 0 1.8rem; height: 52px; position: sticky; top: 0; z-index: 200;
}
.nav-logo {
  font-family: 'Orbitron', sans-serif !important;
  font-size: 1rem; font-weight: 800; letter-spacing: 0.15em; color: #fff;
  margin-right: 2.5rem; white-space: nowrap;
}
.nav-logo span { color: var(--accent); }
.nav-tab-row { display: flex; gap: 0; flex: 1; }
.ntab {
  padding: 0 1.3rem; height: 52px; line-height: 50px;
  font-size: 0.7rem; font-weight: 700; letter-spacing: 0.18em;
  text-transform: uppercase; color: var(--muted);
  border-bottom: 2px solid transparent; cursor: pointer; white-space: nowrap;
}
.ntab.active { color: var(--accent); border-bottom-color: var(--accent); }
.nav-right { margin-left: auto; display: flex; align-items: center; gap: 1.5rem; }
.nav-gti {
  font-family: 'Orbitron', sans-serif !important;
  font-size: 0.95rem; font-weight: 700; color: #fff;
}
.nav-gti-lbl { font-size: 0.55rem; letter-spacing: 0.12em; margin-left: 4px; }
.live-pip {
  display: flex; align-items: center; gap: 5px;
  font-size: 0.62rem; font-weight: 700; letter-spacing: 0.12em; color: var(--green);
}
.pip { width: 6px; height: 6px; border-radius: 50%; background: var(--green);
       animation: blink 1.8s ease-in-out infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.2} }
.nav-time { font-family: 'Share Tech Mono', monospace !important;
            font-size: 0.68rem; color: var(--muted); }

/* ──────── BOTTOM STATUS BAR ──────── */
.statusbar {
  position: fixed; bottom: 0; left: 0; right: 0;
  background: var(--bg1); border-top: 1px solid var(--border);
  height: 30px; display: flex; align-items: center;
  padding: 0 1.8rem; gap: 2.5rem; z-index: 200;
  font-size: 0.58rem; letter-spacing: 0.08em; color: var(--muted);
}
.sb-val { color: var(--bright); font-family: 'Share Tech Mono', monospace !important; }

/* ──────── PANEL LABELS ──────── */
.plbl {
  font-size: 0.56rem; letter-spacing: 0.22em; text-transform: uppercase;
  color: var(--muted); margin-bottom: 0.5rem;
}
.sec-hdr {
  font-size: 0.58rem; letter-spacing: 0.22em; text-transform: uppercase;
  color: var(--muted); border-left: 2px solid var(--accent);
  padding-left: 0.5rem; margin-bottom: 0.8rem; margin-top: 0.2rem;
}

/* ──────── SIDE PANELS ──────── */
.lpanel, .rpanel {
  background: var(--bg1); border-right: 1px solid var(--border);
  padding: 1rem 0.9rem; overflow-y: auto;
  min-height: calc(100vh - 84px);
}
.rpanel { border-right: none; border-left: 1px solid var(--border); }
.cpanel { padding: 1rem 1.2rem; overflow-y: auto; min-height: calc(100vh - 84px); }

/* ──────── STAT BLOCKS ──────── */
.sblock {
  background: var(--bg2); border: 1px solid var(--border);
  border-radius: 5px; padding: 0.7rem 0.8rem; margin-bottom: 0.6rem;
}
.sval {
  font-family: 'Orbitron', sans-serif !important;
  font-size: 1.35rem; font-weight: 600; color: var(--bright); line-height: 1.1;
}
.slbl { font-size: 0.58rem; color: var(--muted); letter-spacing: 0.08em; margin-top: 2px; }

/* ──────── BIG GTI NUMBER ──────── */
.gti-big {
  font-family: 'Orbitron', sans-serif !important;
  font-size: 3rem; font-weight: 800; color: #fff; line-height: 1;
  text-align: center; text-shadow: 0 0 20px rgba(0,200,255,0.4);
}
.gti-badge {
  display: inline-block; font-size: 0.6rem; font-weight: 700;
  letter-spacing: 0.18em; padding: 2px 10px; border-radius: 2px; margin-top: 4px;
}
.gb-low  { background:rgba(0,255,157,0.12); color:var(--green); }
.gb-mod  { background:rgba(255,184,0,0.12);  color:var(--warn);  }
.gb-high { background:rgba(255,59,92,0.12);  color:var(--danger);}

/* ──────── NEWS ITEMS ──────── */
.ni {
  display:flex; gap:0.6rem; align-items:flex-start;
  padding:0.6rem 0; border-bottom:1px solid var(--border);
}
.ni:last-child { border-bottom:none; }
.ndot { flex-shrink:0; width:6px; height:6px; border-radius:50%; margin-top:6px; }
.dp { background:var(--green); }
.dn { background:var(--danger); }
.dz { background:var(--muted); }
.ntitle { font-size:0.77rem; color:var(--bright); line-height:1.45; }
.nmeta  { font-size:0.57rem; color:var(--muted); margin-top:1px;
          font-family:'Share Tech Mono',monospace !important; }
.nscore {
  flex-shrink:0; font-size:0.62rem; font-weight:700; padding:1px 6px;
  border-radius:2px; margin-top:2px;
  font-family:'Share Tech Mono',monospace !important;
}
.sp { background:rgba(0,255,157,0.1); color:var(--green); }
.sn { background:rgba(255,59,92,0.1); color:var(--danger); }
.sz { background:rgba(58,80,112,0.2); color:var(--muted);  }

/* ──────── TICKER CARDS (right panel) ──────── */
.tcard {
  background: var(--bg2); border: 1px solid var(--border);
  border-radius: 5px; padding: 0.75rem 0.85rem; margin-bottom: 0.55rem;
  position: relative;
}
.tcard::before {
  content:''; position:absolute; top:0; left:0; right:0; height:2px;
  border-radius:5px 5px 0 0;
}
.tup::before   { background:var(--green); }
.tdown::before { background:var(--danger); }
.twat::before  { background:var(--warn); }
.tneu::before  { background:var(--muted); }
.tpair { font-family:'Orbitron',sans-serif !important; font-size:0.82rem;
         font-weight:600; color:var(--bright); letter-spacing:0.04em; }
.ttype { font-size:0.54rem; color:var(--muted); letter-spacing:0.14em; margin-top:1px; }
.tsig  { display:inline-block; font-size:0.65rem; font-weight:700; letter-spacing:0.1em;
         padding:2px 8px; border-radius:2px; margin-top:5px; }
.gup  { background:rgba(0,255,157,0.12); color:var(--green);  }
.gdn  { background:rgba(255,59,92,0.12);  color:var(--danger); }
.gwt  { background:rgba(255,184,0,0.12);  color:var(--warn);   }
.gnu  { background:rgba(58,80,112,0.3);   color:var(--muted);  }
.treason { font-size:0.59rem; color:var(--muted); margin-top:4px; line-height:1.4; }
.tct     { font-size:0.56rem; color:var(--muted); margin-top:2px; }

/* ──────── SIGNAL ROW (left panel) ──────── */
.sigrow {
  display:flex; align-items:center; justify-content:space-between;
  padding:0.4rem 0; border-bottom:1px solid var(--border); font-size:0.72rem;
}
.sigrow:last-child { border-bottom:none; }
.ssym { font-weight:700; color:var(--bright); }
.gup-t  { color:var(--green);  font-weight:700; }
.gdn-t  { color:var(--danger); font-weight:700; }
.gwt-t  { color:var(--warn);   font-weight:700; }
.gnu-t  { color:var(--muted);  font-weight:700; }

/* ──────── CHART WRAPPERS ──────── */
.ccard { background:var(--bg1); border:1px solid var(--border); border-radius:5px;
         padding:0.8rem; margin-bottom:0.8rem; }
.cempty { height:160px; display:flex; align-items:center; justify-content:center;
          color:var(--border); font-size:0.68rem; letter-spacing:0.12em; }

/* ──────── GEO MAP FILTER PANEL ──────── */
.filtpanel {
  background:var(--bg1); border:1px solid var(--border); border-radius:5px;
  padding:0.8rem; margin-bottom:0.8rem;
}
.filt-row { display:flex; align-items:center; gap:0.5rem; margin-bottom:0.4rem;
             font-size:0.68rem; color:var(--muted); }
.filt-dot { width:8px; height:8px; border-radius:50%; flex-shrink:0; }

/* ──────── AI SIGNALS ──────── */
.signal-gauge-wrap { display:flex; flex-direction:column; align-items:center; padding:0.5rem 0; }
.conf-bar-bg { background:var(--bg3); border-radius:3px; height:6px; width:100%; margin-top:4px; }
.conf-bar-fill { border-radius:3px; height:6px; }

/* ──────── COUNTRY DETAIL PANEL ──────── */
.country-hdr {
  font-family: 'Orbitron', sans-serif !important;
  font-size: 1.1rem; font-weight: 700; color: #fff; margin-bottom: 0.4rem;
}
.risk-factor-row {
  display:flex; gap:6px; padding:5px 0; border-bottom:1px solid var(--border);
  align-items:flex-start;
}
.back-hint { font-size:0.58rem; color:var(--muted); margin-bottom:0.8rem; }

/* ──────── TABS for sub-views ──────── */
div[role="tab"] {
  font-family: 'Rajdhani', sans-serif !important;
  font-weight: 700 !important; letter-spacing: 0.12em !important;
  font-size: 0.72rem !important; text-transform: uppercase;
  color: var(--muted) !important;
}
div[aria-selected="true"] { color: var(--accent) !important; }
div[data-baseweb="tab-highlight"] { background-color: var(--accent) !important; }
div[data-baseweb="tab-border"] { background-color: var(--border) !important; }

/* Hide streamlit button default style for back button */
div[data-testid="stButton"] button {
  background: rgba(0,200,255,0.08) !important;
  border: 1px solid var(--accent) !important;
  color: var(--accent) !important;
  font-size: 0.62rem !important;
  font-weight: 700 !important;
  letter-spacing: 0.12em !important;
  border-radius: 3px !important;
  padding: 3px 12px !important;
  margin-bottom: 0.8rem;
}
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
            FROM gdelt_events
            WHERE timestamp >= ?
            LIMIT {MAX_ROWS}""",
        (cut,))

@st.cache_data(ttl=60)
def load_country_headlines(fips_code: str, n: int = 10) -> pd.DataFrame:
    cut = (datetime.utcnow()-timedelta(hours=48)).strftime("%Y-%m-%d %H:%M:%S")
    return _q(NEWS_DB,
        f"""SELECT event_code, goldstein_scale, avg_tone, num_articles
            FROM gdelt_events
            WHERE (actor1_country=? OR actor2_country=?)
            AND timestamp >= ?
            ORDER BY num_articles DESC
            LIMIT {n}""",
        (fips_code, fips_code, cut))


# ═══════════════════════════════════════════════════════════════════════════
#  CURRENCY / COMMODITY IMPACT ENGINE
# ═══════════════════════════════════════════════════════════════════════════
IMPACT_RULES = [
    {"asset":"USD/JPY","name":"US Dollar / Yen",      "type":"FX",
     "kw":["federal reserve","fed rate","fomc","powell","cpi","inflation","treasury","us economy","dollar","interest rate"],
     "neg":-1,"pos":+1},
    {"asset":"EUR/USD","name":"Euro / Dollar",        "type":"FX",
     "kw":["ecb","european central bank","eurozone","eu sanctions","russia gas","germany","euro","europe"],
     "neg":-1,"pos":+1},
    {"asset":"GBP/USD","name":"Pound / Dollar",       "type":"FX",
     "kw":["bank of england","boe","sterling","pound","uk gdp","uk inflation","brexit","britain"],
     "neg":-1,"pos":+1},
    {"asset":"USD/CNH","name":"Dollar / Yuan",        "type":"FX",
     "kw":["china","pboc","yuan","renminbi","taiwan","beijing","xi jinping","hong kong","chinese"],
     "neg":+1,"pos":-1},
    {"asset":"XAU/USD","name":"Gold / Dollar",        "type":"COMMODITY",
     "kw":["gold","war","conflict","nuclear","sanctions","safe haven","inflation hedge","crisis","military","attack"],
     "neg":+1,"pos":-1},
    {"asset":"OIL/USD","name":"Crude Oil",            "type":"COMMODITY",
     "kw":["opec","oil","crude","brent","wti","saudi","iran","pipeline","middle east","iraq","libya","energy","petroleum"],
     "neg":+1,"pos":+1},
    {"asset":"XAG/USD","name":"Silver",               "type":"COMMODITY",
     "kw":["silver","precious metal","industrial demand","solar","manufacturing"],
     "neg":+1,"pos":-1},
    {"asset":"SPY","name":"US Equities (S&P500)",     "type":"EQUITY",
     "kw":["s&p","nasdaq","dow","earnings","gdp growth","rate cut","stimulus","jobs report","employment","stock market"],
     "neg":-1,"pos":+1},
    {"asset":"VIX","name":"Volatility Index",         "type":"EQUITY",
     "kw":["volatility","risk","uncertainty","crash","sell-off","turmoil","fear","panic","market fear"],
     "neg":+1,"pos":-1},
    {"asset":"BTC/USD","name":"Bitcoin",              "type":"CRYPTO",
     "kw":["bitcoin","crypto","btc","digital asset","sec crypto","cbdc","defi","crypto regulation","ethereum"],
     "neg":-1,"pos":+1},
    {"asset":"ETH/USD","name":"Ethereum",             "type":"CRYPTO",
     "kw":["ethereum","eth","defi","smart contract","web3","layer 2","polygon","blockchain"],
     "neg":-1,"pos":+1},
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
#  GEO ORIGIN MAPPING  (for news scatter fallback)
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


# ═══════════════════════════════════════════════════════════════════════════
#  FIPS ↔ ISO3 COUNTRY MAPPING  (GDELT uses FIPS-2, Plotly needs ISO-3)
# ═══════════════════════════════════════════════════════════════════════════
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
    "BM": "MMR", "CB": "KHM", "LA": "LAO", "SG": "SGP", "RP": "PHL",
    "NZ": "NZL", "NP": "NPL", "BG": "BGD", "CE": "LKA",
    "TI": "TJK", "UZ": "UZB", "KZ": "KAZ", "KG": "KGZ", "TX": "TKM",
    "AJ": "AZE", "AM": "ARM", "GG": "GEO", "BE": "BLR", "MD": "MDA",
    "LG": "LVA", "LH": "LTU", "EN": "EST", "SW": "SWE", "NO": "NOR",
    "DA": "DNK", "NL": "NLD", "LU": "LUX", "SZ": "CHE", "PL": "PRT",
    "MN": "MNG", "TW": "TWN", "HK": "HKG", "SB": "SRB", "HR": "HRV",
    "BK": "BIH", "MK": "MKD", "AL": "ALB", "MJ": "MNE", "LO": "SVK",
    "SI": "SVN", "FI": "FIN", "IC": "ISL", "EI": "IRL", "PO": "PRT",
    "BU": "BGR", "BO": "BOL", "EC": "ECU", "PE": "PER", "CI": "CHL",
    "UY": "URY", "PA": "PRY", "AC": "ATG", "BB": "BRB", "BH": "BHS",
    "JM": "JAM", "TD": "TTO", "CU": "CUB", "HA": "HTI", "DR": "DOM",
}

ISO3_TO_FIPS = {v: k for k, v in FIPS_TO_ISO3.items()}

ISO3_TO_COUNTRY_NAME = {
    "USA": "United States", "RUS": "Russia", "GBR": "United Kingdom",
    "CHN": "China", "FRA": "France", "DEU": "Germany", "ISR": "Israel",
    "IRN": "Iran", "IRQ": "Iraq", "SYR": "Syria", "UKR": "Ukraine",
    "EGY": "Egypt", "SAU": "Saudi Arabia", "AFG": "Afghanistan",
    "PAK": "Pakistan", "IND": "India", "JPN": "Japan", "KOR": "South Korea",
    "TUR": "Turkey", "LBY": "Libya", "SDN": "Sudan", "YEM": "Yemen",
    "NGA": "Nigeria", "ETH": "Ethiopia", "SOM": "Somalia", "MAR": "Morocco",
    "DZA": "Algeria", "TUN": "Tunisia", "ARE": "UAE", "QAT": "Qatar",
    "KWT": "Kuwait", "LBN": "Lebanon", "JOR": "Jordan", "BRA": "Brazil",
    "MEX": "Mexico", "VEN": "Venezuela", "COL": "Colombia", "ARG": "Argentina",
    "ESP": "Spain", "ITA": "Italy", "POL": "Poland", "GRC": "Greece",
    "ROU": "Romania", "HUN": "Hungary", "CZE": "Czech Republic",
    "AUS": "Australia", "CAN": "Canada", "ZAF": "South Africa",
    "KEN": "Kenya", "GHA": "Ghana", "IDN": "Indonesia", "THA": "Thailand",
    "MYS": "Malaysia", "PHL": "Philippines", "VNM": "Vietnam",
    "MMR": "Myanmar", "SGP": "Singapore", "NPL": "Nepal", "BGD": "Bangladesh",
    "LKA": "Sri Lanka", "KAZ": "Kazakhstan", "UZB": "Uzbekistan",
    "AZE": "Azerbaijan", "ARM": "Armenia", "GEO": "Georgia",
    "BLR": "Belarus", "SWE": "Sweden", "NOR": "Norway", "DNK": "Denmark",
    "NLD": "Netherlands", "CHE": "Switzerland", "FIN": "Finland",
    "IRL": "Ireland", "PRT": "Portugal", "BGR": "Bulgaria",
    "HRV": "Croatia", "SRB": "Serbia", "MNG": "Mongolia",
    "TWN": "Taiwan", "CUB": "Cuba", "HTI": "Haiti",
}

ISO3_TO_COUNTRY_KEYWORDS = {
    "USA": ["united states","us economy","federal reserve","washington","congress","dollar","wall street"],
    "RUS": ["russia","moscow","kremlin","putin","ukraine war","russian"],
    "CHN": ["china","beijing","xi jinping","taiwan","hong kong","chinese","pboc","yuan"],
    "ISR": ["israel","tel aviv","gaza","hamas","netanyahu","idf"],
    "IRN": ["iran","tehran","ayatollah","nuclear deal","iranian"],
    "SYR": ["syria","damascus","syrian","aleppo"],
    "UKR": ["ukraine","kyiv","zelensky","donbas","ukrainian"],
    "GBR": ["britain","uk economy","london","sunak","sterling","bank of england"],
    "DEU": ["germany","berlin","german","bundesbank","angela","scholz"],
    "FRA": ["france","paris","macron","french","ecb"],
    "SAU": ["saudi","riyadh","aramco","opec","mbs"],
    "IRQ": ["iraq","baghdad","iraqi","mosul"],
    "PAK": ["pakistan","islamabad","karachi","imf pakistan"],
    "IND": ["india","delhi","modi","rupee","reserve bank india"],
    "JPN": ["japan","tokyo","yen","boj","bank of japan","japanese"],
    "KOR": ["south korea","seoul","won currency","korean"],
    "TUR": ["turkey","ankara","erdogan","lira","turkish"],
    "EGY": ["egypt","cairo","suez","egyptian pound"],
    "LBN": ["lebanon","beirut","hezbollah","lebanese"],
    "YEM": ["yemen","houthi","sanaa","yemeni"],
    "NGA": ["nigeria","lagos","abuja","naira","boko haram"],
    "ZAF": ["south africa","johannesburg","rand currency","south african"],
    "BRA": ["brazil","brasilia","bolsonaro","lula","real currency","brazilian"],
    "MEX": ["mexico","mexico city","peso","mexican"],
    "VEN": ["venezuela","caracas","maduro","bolivar"],
    "ARG": ["argentina","buenos aires","peso argentina","milei"],
}


def classify_arc_type(event_code) -> str:
    """Map GDELT CAMEO event code to arc type category."""
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
    else:
        return "Diplomatic"


def build_country_tension_df(gdelt_df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate per-country tension score (0–100) from GDELT events."""
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
            "lat":  lat + (hash(title)              % 9)*0.25 - 1.0,
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
#  HELPERS
# ═══════════════════════════════════════════════════════════════════════════
def gti_meta(score_100: float):
    """Return (label, css_class, hex_color) for a 0–100 GTI score."""
    if score_100 >= 80: return "CRITICAL",  "gb-high", "#ff3b5c"
    if score_100 >= 60: return "HIGH",      "gb-high", "#ff3b5c"
    if score_100 >= 35: return "ELEVATED",  "gb-mod",  "#ffb800"
    return                     "LOW",       "gb-low",  "#00ff9d"

PLOT_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Share Tech Mono, monospace", color="#3a5070", size=10),
)
_AX = dict(gridcolor="#111c30", showline=False, zeroline=False)
_M8 = dict(l=8, r=8, t=8, b=8)   # default margin for most charts

SIG_LBL  = {"up":"▲ BULLISH","down":"▼ BEARISH","watch":"⚠ WATCH","neutral":"— NEUTRAL"}
SIG_CLS  = {"up":"gup","down":"gdn","watch":"gwt","neutral":"gnu"}
CARD_CLS = {"up":"tup","down":"tdown","watch":"twat","neutral":"tneu"}


def build_choropleth_globe(country_tension_df: pd.DataFrame,
                            proj_type: str = "orthographic",
                            proj_lon: float = 20.0,
                            proj_lat: float = 20.0,
                            height: int = 460) -> go.Figure:
    """Build a choropleth map/globe with countries colored by tension level."""
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
            [0.00, "#0d1f35"],   # no tension — dark bg
            [0.35, "#00ff9d"],   # LOW  (<35) — green
            [0.60, "#ffb800"],   # ELEVATED (35-60) — amber
            [0.80, "#ff6b35"],   # HIGH (60-80) — orange-red
            [1.00, "#ff3b5c"],   # CRITICAL (>80) — red
        ],
        zmin=0, zmax=100,
        showscale=False,
        marker=dict(line=dict(color="#1b2d45", width=0.5)),
        text=hover_txt,
        hovertemplate="%{text}<extra></extra>",
    ))

    geo_cfg = dict(
        showland=True,       landcolor="#0c1424",
        showocean=True,      oceancolor="#04080f",
        showcoastlines=True, coastlinecolor="#1e3a5a",
        showcountries=False,
        showframe=False,
        bgcolor="rgba(0,0,0,0)",
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
    # Override paper/plot background to solid dark so the iframe shows dark
    fig.layout.paper_bgcolor = "#04080f"
    fig.layout.plot_bgcolor  = "#04080f"
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

vol_pred = pred.get("vol_prediction","—")
vol_conf = pred.get("vol_prob", 0)
dir_pred = pred.get("dir_prediction","—")
dir_conf = pred.get("dir_prob", 0)

pos_ct = int((news_df["vader_label"]=="positive").sum()) if not news_df.empty else 0
neg_ct = int((news_df["vader_label"]=="negative").sum()) if not news_df.empty else 0
neu_ct = int((news_df["vader_label"]=="neutral").sum())  if not news_df.empty else 0
total_news = pos_ct + neg_ct + neu_ct

# Load GDELT country tension (used in Tab 1 + Tab 2)
gdelt_raw_df  = load_gdelt_country_tension(48)
country_df    = build_country_tension_df(gdelt_raw_df)

# ═══════════════════════════════════════════════════════════════════════════
#  STITCH MCP "WINDOWS" UI INTEGRATION
# ═══════════════════════════════════════════════════════════════════════════

# 1. Prepare the live data payload for the Stitch UI
live_data = {
    "gti_score": score_100,
    "conflict_count": conflict_ct,
    "volatility_prediction": vol_pred,
    "volatility_confidence": vol_conf,
    "direction_prediction": dir_pred,
    "direction_confidence": dir_conf,
    "latest_headlines": news_df[["title", "source", "vader_label"]].head(15).to_dict(orient="records") if not news_df.empty else []
}

# 2. Fetch the "windows" UI directly from Stitch MCP
api_url = "https://stitch.googleapis.com/mcp/ui/windows"
headers = {"X-Goog-Api-Key": os.getenv("STITCH_API_KEY", "")}

try:
    response = requests.get(api_url, headers=headers, timeout=10)
    response.raise_for_status()
    ui_payload = response.json()
except Exception as e:
    ui_payload = {"error": str(e)}

# 3. Render the dynamic UI
if "error" in ui_payload:
    st.error(f"Failed to load the Windows UI from Stitch MCP: {ui_payload['error']}")
    st.info("Make sure STITCH_API_KEY is set in your .env file.")
    st.json(live_data)
else:
    # Handle both string (raw HTML) and JSON dictionary responses
    if isinstance(ui_payload, str):
        html_content, css_content, js_content = ui_payload, "", ""
    else:
        html_content = ui_payload.get("html", "<div style='color:white; font-family: sans-serif;'>UI loaded, but no HTML found.</div>")
        css_content = ui_payload.get("css", "")
        js_content = ui_payload.get("js", "")

    # Inject the working data directly into the window object for the JS to consume
    injected_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ margin: 0; padding: 0; background-color: transparent; }}
            {css_content}
        </style>
        <script>
            // Expose real backend data to the Stitch UI component
            window.GeoMarketData = {json.dumps(live_data)};
        </script>
    </head>
    <body>
        {html_content}
        <script>{js_content}</script>
    </body>
    </html>
    """
    components.html(injected_html, height=850, scrolling=True)

# ── Non-blocking 60-second auto-refresh ───────────────────────────────────
if time.time() - st.session_state.get("last_refresh", time.time()) > 60:
    st.session_state["last_refresh"] = time.time()
    st.rerun()

# Stop execution here to entirely replace the old manual UI with the new Stitch UI
st.stop()

# ═══════════════════════════════════════════════════════════════════════════
#  NAVBAR  (always visible)
# ═══════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="navbar">
  <div class="nav-logo">GEO<span>MARKET</span></div>
  <div class="nav-tab-row" id="navtabs">
    <div class="ntab active">&#9670;&nbsp;EARTH PULSE</div>
    <div class="ntab">&#9670;&nbsp;GEO MAP</div>
    <div class="ntab">&#9670;&nbsp;AI SIGNALS</div>
    <div class="ntab">&#9670;&nbsp;MARKET</div>
  </div>
  <div class="nav-right">
    <div class="nav-gti">
      {score_100:.1f}
      <span class="nav-gti-lbl" style="color:{lev_col}">{lev_lbl}</span>
    </div>
    <div class="live-pip"><div class="pip"></div>LIVE</div>
    <div class="nav-time">{now_str}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Streamlit native tab switcher (functional) ────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🌍  EARTH PULSE",
    "🗺  GEO MAP",
    "🤖  AI SIGNALS",
    "📈  MARKET",
])


# ═══════════════════════════════════════════════════════════════════════════
#  TAB 1 — EARTH PULSE  (Choropleth Globe + GTI + News + Country Click)
# ═══════════════════════════════════════════════════════════════════════════
with tab1:
    left, center, right = st.columns([1.15, 3.7, 1.4])

    # ── LEFT: Live metrics ───────────────────────────────────────────────
    with left:
        st.markdown(f"""
        <div class="lpanel">
          <div class="plbl">Geopolitical Tension Index</div>
          <div style="text-align:center;padding:0.6rem 0 0.8rem">
            <div class="gti-big">{score_100:.1f}</div>
            <div><span class="gti-badge {lev_cls}">{lev_lbl}</span></div>
          </div>

          <div class="sblock">
            <div class="slbl">CONFLICT EVENTS (6H WINDOW)</div>
            <div class="sval">{conflict_ct}</div>
            <div class="slbl">GDELT Goldstein scale &lt; −5.0</div>
          </div>

          <div class="sblock">
            <div class="slbl">GDELT MEDIA TONE</div>
            <div class="sval" style="font-size:1.1rem">{avg_tone:+.2f}</div>
            <div class="slbl">−100 (negative) to +100 (positive)</div>
          </div>

          <div class="sblock">
            <div class="slbl">VADER HEADLINE SENTIMENT</div>
            <div class="sval" style="font-size:1.1rem">{vader_avg:+.3f}</div>
            <div class="slbl">{pos_ct} pos · {neg_ct} neg · {neu_ct} neu</div>
          </div>

          <div class="sblock">
            <div class="slbl">MODEL: VOLATILITY</div>
            <div class="sval" style="font-size:1rem;color:{'#ff3b5c' if vol_pred=='HIGH' else '#00ff9d'}">{vol_pred}</div>
            <div class="slbl">Confidence {vol_conf:.0%}</div>
          </div>

          <div class="sblock">
            <div class="slbl">MODEL: DIRECTION (1H)</div>
            <div class="sval" style="font-size:1rem;color:{'#00ff9d' if dir_pred=='UP' else '#ff3b5c'}">
              {'▲' if dir_pred=='UP' else '▼'} {dir_pred}
            </div>
            <div class="slbl">Confidence {dir_conf:.0%}</div>
          </div>

          <div class="plbl" style="margin-top:1rem">Risk Level</div>
          <div class="filtpanel">
            <div class="filt-row"><div class="filt-dot" style="background:#ff3b5c"></div>CRITICAL ≥80</div>
            <div class="filt-row"><div class="filt-dot" style="background:#ff6b35"></div>HIGH ≥60</div>
            <div class="filt-row"><div class="filt-dot" style="background:#ffb800"></div>ELEVATED ≥35</div>
            <div class="filt-row"><div class="filt-dot" style="background:#00ff9d"></div>LOW &lt;35</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── CENTER: Choropleth Globe + News Feed ─────────────────────────────
    with center:
        st.markdown('<div class="cpanel">', unsafe_allow_html=True)
        st.markdown('<div class="sec-hdr">GLOBAL TENSION MAP — click any country for market signals</div>', unsafe_allow_html=True)

        fig_globe = build_choropleth_globe(country_df, proj_type="orthographic",
                                            proj_lon=20.0, proj_lat=20.0, height=460)

        if _HAS_PLOTLY_EVENTS:
            clicked = plotly_events(
                fig_globe,
                click_event=True,
                override_height=460,
                key="globe_click_tab1",
            )
            if clicked:
                loc = clicked[0].get("location", "")
                if loc and loc != st.session_state.get("selected_country_iso3"):
                    st.session_state["selected_country_iso3"] = loc
                    st.session_state["selected_country_name"] = ISO3_TO_COUNTRY_NAME.get(loc, loc)
                    st.rerun()
        else:
            st.plotly_chart(fig_globe, use_container_width=True,
                            config={"displayModeBar": False}, key="globe_chart_tab1")
            st.markdown(
                '<div style="font-size:0.59rem;color:#3a5070;text-align:center;margin:-6px 0 4px">'
                'Install <code>streamlit-plotly-events</code> to enable country click</div>',
                unsafe_allow_html=True)

        # Country count indicator
        n_countries = len(country_df) if not country_df.empty else 0
        st.markdown(
            f'<div style="font-size:0.59rem;color:#3a5070;text-align:center;margin:-4px 0 10px">'
            f'{n_countries} countries · GDELT 48h · drag to rotate</div>',
            unsafe_allow_html=True)

        # News headlines feed
        gdf_all = build_geo_df(news_df) if not news_df.empty else pd.DataFrame()
        if not gdf_all.empty:
            st.markdown('<div class="sec-hdr" style="margin-top:0.8rem">LATEST HEADLINES</div>', unsafe_allow_html=True)
            html = '<div class="ccard" style="max-height:240px;overflow-y:auto;padding:0.6rem 0.8rem">'
            for _, row in gdf_all.head(28).iterrows():
                lbl  = row["label"]
                comp = row["compound"]
                src  = row["source"][:20]
                pub  = row["pub"]
                ttl  = row["title"]
                dc   = "dp" if lbl=="positive" else ("dn" if lbl=="negative" else "dz")
                sc   = "sp" if comp>0.05 else ("sn" if comp<-0.05 else "sz")
                html += (f'<div class="ni">'
                         f'<div class="ndot {dc}"></div>'
                         f'<div class="news-body" style="flex:1">'
                         f'<div class="ntitle">{ttl}</div>'
                         f'<div class="nmeta">{src} · {pub}</div></div>'
                         f'<div class="nscore {sc}">{comp:+.2f}</div></div>')
            html += "</div>"
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.markdown('<div class="ccard"><div class="cempty">NO NEWS DATA — START SCHEDULER</div></div>',
                        unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # ── RIGHT: Country detail OR default GTI / asset signals ─────────────
    with right:
        st.markdown('<div class="rpanel">', unsafe_allow_html=True)

        selected_iso3 = st.session_state.get("selected_country_iso3")

        if selected_iso3:
            # ── COUNTRY DETAIL VIEW ────────────────────────────────────
            country_name = st.session_state.get("selected_country_name", selected_iso3)

            # Tension for this country
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
            <div class="country-hdr">{country_name}</div>
            <div style="margin-bottom:0.8rem">
              <span class="gti-badge {c_cls}">{c_lbl} · {ctension:.0f}/100</span>
            </div>
            <div class="filtpanel" style="font-size:0.63rem;color:var(--text);line-height:2">
              <div style="display:flex;justify-content:space-between">
                <span style="color:var(--muted)">Conflicts</span>
                <span style="color:#ff3b5c;font-weight:700">{c_conflicts}</span>
              </div>
              <div style="display:flex;justify-content:space-between">
                <span style="color:var(--muted)">Events (48h)</span>
                <span style="color:var(--bright)">{c_events}</span>
              </div>
              <div style="display:flex;justify-content:space-between">
                <span style="color:var(--muted)">Avg Tone</span>
                <span style="color:{'#ff3b5c' if c_tone<0 else '#00ff9d'}">{c_tone:+.2f}</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # Market signals for this country
            st.markdown('<div class="plbl" style="margin-top:0.8rem">MARKET SIGNALS</div>',
                        unsafe_allow_html=True)
            kws = ISO3_TO_COUNTRY_KEYWORDS.get(selected_iso3, [])
            if kws and not news_df.empty:
                pattern = "|".join(kws)
                country_news = news_df[
                    news_df["title"].str.lower().str.contains(pattern, na=False, regex=True)
                ]
            else:
                country_news = news_df.head(20) if not news_df.empty else pd.DataFrame()

            country_impacts = analyze_impact(country_news)
            shown = 0
            html = ""
            for item in country_impacts:
                if item["match_ct"] == 0:
                    continue
                s = item["signal"]
                html += (f'<div class="tcard {CARD_CLS[s]}">'
                         f'<div class="tpair">{item["asset"]}</div>'
                         f'<div class="ttype">{item["type"]}</div>'
                         f'<div><span class="tsig {SIG_CLS[s]}">{SIG_LBL[s]}</span></div>'
                         f'<div class="treason">{item["reason"]}</div>'
                         f'</div>')
                shown += 1
                if shown >= 3:
                    break
            if not html:
                html = '<div class="back-hint">No matching signals for this country</div>'
            st.markdown(html, unsafe_allow_html=True)

            # Risk factors from GDELT events for this country
            fips = ISO3_TO_FIPS.get(selected_iso3, "")
            if fips:
                events_df = load_country_headlines(fips, n=8)
                if not events_df.empty:
                    st.markdown('<div class="plbl" style="margin-top:0.8rem">RISK FACTORS</div>',
                                unsafe_allow_html=True)
                    for _, ev in events_df.iterrows():
                        arc = classify_arc_type(str(ev.get("event_code", "")))
                        gs  = ev.get("goldstein_scale", 0)
                        try:
                            gs = float(gs)
                        except (ValueError, TypeError):
                            gs = 0.0
                        sev = "CRITICAL" if gs < -8 else ("HIGH" if gs < -5 else "MEDIUM")
                        sev_col = "#ff3b5c" if sev=="CRITICAL" else ("#ffb800" if sev=="HIGH" else "#3a5070")
                        arc_icon = {"Military":"⚔","Sanctions":"🚫","Trade":"📦","Diplomatic":"🤝"}.get(arc,"·")
                        st.markdown(f"""
                        <div class="risk-factor-row">
                          <span style="font-size:0.55rem;color:{sev_col};font-weight:700;min-width:52px">{sev}</span>
                          <span style="font-size:0.62rem;color:#a8c4dc">{arc_icon} {arc} · GS {gs:.1f}</span>
                        </div>
                        """, unsafe_allow_html=True)

            # Back button
            if st.button("← BACK TO SIGNALS", key="back_btn_tab1"):
                st.session_state["selected_country_iso3"] = None
                st.session_state["selected_country_name"] = None
                st.rerun()

        else:
            # ── DEFAULT: GTI History + Asset Impact Cards ──────────────
            st.markdown('<div class="sec-hdr">GTI HISTORY — 48H</div>', unsafe_allow_html=True)
            if not gti_df.empty:
                fig_gti = go.Figure()
                fig_gti.add_hrect(y0=0,  y1=35,  fillcolor="rgba(0,255,157,0.04)", line_width=0)
                fig_gti.add_hrect(y0=35, y1=60,  fillcolor="rgba(255,184,0,0.04)", line_width=0)
                fig_gti.add_hrect(y0=60, y1=80,  fillcolor="rgba(255,107,53,0.04)", line_width=0)
                fig_gti.add_hrect(y0=80, y1=100, fillcolor="rgba(255,59,92,0.06)",  line_width=0)
                fig_gti.add_trace(go.Scatter(
                    x=gti_df["timestamp"], y=gti_df["gti_score"] * 100,
                    mode="lines", name="GTI Score",
                    line=dict(color="#00c8ff", width=2),
                    fill="tozeroy", fillcolor="rgba(0,200,255,0.06)",
                ))
                if "vader_avg" in gti_df.columns:
                    vn = ((-gti_df["vader_avg"]+1)/2).clip(0,1) * 100
                    fig_gti.add_trace(go.Scatter(x=gti_df["timestamp"], y=vn,
                        mode="lines", name="VADER (norm)",
                        line=dict(color="#ff6b35",width=1,dash="dot"), opacity=0.5))
                fig_gti.add_hline(y=35, line_dash="dot", line_color="rgba(0,255,157,0.3)", line_width=1)
                fig_gti.add_hline(y=60, line_dash="dot", line_color="rgba(255,184,0,0.3)",  line_width=1)
                fig_gti.add_hline(y=80, line_dash="dot", line_color="rgba(255,59,92,0.3)",   line_width=1)
                fig_gti.update_layout(**PLOT_BASE, margin=_M8, height=220,
                    xaxis={**_AX},
                    yaxis=dict(range=[0,100], gridcolor="#111c30", zeroline=False, title="GTI"),
                    showlegend=False, hovermode="x unified")
                st.plotly_chart(fig_gti, use_container_width=True,
                                config={"displayModeBar":False}, key="gti_chart_tab1")
            else:
                st.markdown('<div class="ccard"><div class="cempty">NO GTI DATA</div></div>',
                            unsafe_allow_html=True)

            st.markdown('<div class="plbl" style="margin-top:1.5rem">TOP ASSET IMPACTS</div>',
                        unsafe_allow_html=True)
            html = '<div style="font-size:0.57rem;color:#3a5070;margin-bottom:0.7rem;line-height:1.5">Highest match count triggers</div>'
            for item in impacts[:5]:
                s = item["signal"]
                html += (f'<div class="tcard {CARD_CLS[s]}">'
                         f'<div class="tpair">{item["asset"]}</div>'
                         f'<div class="ttype">{item["type"]} · {item["name"]}</div>'
                         f'<div><span class="tsig {SIG_CLS[s]}">{SIG_LBL[s]}</span></div>'
                         f'<div class="treason">{item["reason"]}</div>'
                         f'<div class="tct">{item["match_ct"]} trigger{"s" if item["match_ct"]!=1 else ""}</div>'
                         f'</div>')
            st.markdown(html, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
#  TAB 2 — GEO MAP  (Choropleth map + arc-type filters + city chart)
# ═══════════════════════════════════════════════════════════════════════════
with tab2:
    left2, center2 = st.columns([1, 4])

    with left2:
        st.markdown('<div class="lpanel">', unsafe_allow_html=True)

        # Risk level legend
        st.markdown("""
        <div class="plbl">Risk Level</div>
        <div class="filtpanel">
          <div class="filt-row"><div class="filt-dot" style="background:#ff3b5c"></div>CRITICAL ≥80</div>
          <div class="filt-row"><div class="filt-dot" style="background:#ff6b35"></div>HIGH ≥60</div>
          <div class="filt-row"><div class="filt-dot" style="background:#ffb800"></div>ELEVATED ≥35</div>
          <div class="filt-row"><div class="filt-dot" style="background:#00ff9d"></div>LOW &lt;35</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Arc type filter (native Streamlit widget, must be outside html block)
        st.markdown('<div style="padding:0 0.9rem;background:var(--bg1);border-right:1px solid var(--border)">', unsafe_allow_html=True)
        arc_filter = st.multiselect(
            "ARC TYPES",
            options=["Military", "Sanctions", "Trade", "Diplomatic"],
            default=st.session_state["arc_filter"],
            key="arc_filter_widget",
        )
        st.session_state["arc_filter"] = arc_filter

        st.markdown(f"""
        <div class="plbl" style="margin-top:0.8rem">Total Headlines</div>
        <div class="sblock"><div class="sval">{total_news}</div><div class="slbl">Last 80 articles</div></div>

        <div class="plbl" style="margin-top:0.8rem">Sentiment Split</div>
        <div class="sblock" style="font-size:0.65rem;color:#a8c4dc;line-height:2">
          <div style="display:flex;justify-content:space-between">
            <span style="color:var(--green)">POS</span>
            <span>{pos_ct}</span>
          </div>
          <div style="display:flex;justify-content:space-between">
            <span style="color:var(--danger)">NEG</span>
            <span>{neg_ct}</span>
          </div>
          <div style="display:flex;justify-content:space-between">
            <span style="color:var(--muted)">NEU</span>
            <span>{neu_ct}</span>
          </div>
        </div>

        <div class="plbl" style="margin-top:0.8rem">Active Conflicts</div>
        <div class="sblock">
          <div class="sval" style="color:#ff3b5c">{conflict_ct}</div>
          <div class="slbl">GDELT events · 6h window</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with center2:
        st.markdown('<div class="cpanel">', unsafe_allow_html=True)
        st.markdown('<div class="sec-hdr">GLOBAL TENSION MAP — country choropleth by arc type</div>',
                    unsafe_allow_html=True)

        # Build filtered country df based on arc type selection
        if not gdelt_raw_df.empty and arc_filter:
            gdelt_filtered = gdelt_raw_df.copy()
            gdelt_filtered["arc_type"] = gdelt_filtered["event_code"].apply(classify_arc_type)
            gdelt_filtered = gdelt_filtered[gdelt_filtered["arc_type"].isin(arc_filter)]
            country_df_filtered = build_country_tension_df(gdelt_filtered)
        elif not arc_filter:
            country_df_filtered = pd.DataFrame()
        else:
            country_df_filtered = country_df.copy()

        fig_map2 = build_choropleth_globe(
            country_df_filtered,
            proj_type="natural earth",
            height=520,
        )

        if _HAS_PLOTLY_EVENTS:
            clicked_map = plotly_events(
                fig_map2,
                click_event=True,
                override_height=520,
                key="map_click_tab2",
            )
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
            f'<div style="font-size:0.59rem;color:#3a5070;text-align:center;margin:-6px 0 10px">'
            f'{n_filtered} countries shown · Filter: {arc_label}</div>',
            unsafe_allow_html=True)

        # City breakdown bar chart (from news sources)
        if not news_df.empty:
            gdf3 = build_geo_df(news_df)
            if not gdf3.empty:
                city_counts = gdf3.groupby("city").agg(
                    total=("compound","count"),
                    avg_sent=("compound","mean")
                ).reset_index().sort_values("total", ascending=False).head(12)

                bar_colors = city_counts["avg_sent"].apply(
                    lambda c: "#00ff9d" if c>0.05 else ("#ff3b5c" if c<-0.05 else "#3a5070"))

                st.markdown('<div class="sec-hdr" style="margin-top:0.5rem">HEADLINES BY SOURCE CITY</div>',
                            unsafe_allow_html=True)
                fig_bar = go.Figure(go.Bar(
                    x=city_counts["city"], y=city_counts["total"],
                    marker_color=bar_colors,
                    text=city_counts["avg_sent"].apply(lambda x: f"{x:+.2f}"),
                    textposition="outside",
                    textfont=dict(size=9, color="#3a5070"),
                ))
                fig_bar.update_layout(**PLOT_BASE, margin=_M8, height=200,
                    yaxis=dict(gridcolor="#111c30", zeroline=False, showline=False),
                    xaxis=dict(gridcolor="rgba(0,0,0,0)", showline=False, zeroline=False))
                st.plotly_chart(fig_bar, use_container_width=True,
                                config={"displayModeBar":False}, key="city_bar_tab2")

        st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
#  TAB 3 — AI SIGNALS  (Model output + feature importance + signal history)
# ═══════════════════════════════════════════════════════════════════════════
with tab3:
    c1, c2, c3 = st.columns([1.2, 2.4, 1.6])

    with c1:
        st.markdown(f"""
        <div class="lpanel">
          <div class="plbl">Latest Model Output</div>

          <div class="sblock" style="text-align:center;padding:1rem">
            <div class="slbl">VOLATILITY FORECAST</div>
            <div style="font-family:'Orbitron',sans-serif;font-size:2rem;font-weight:800;
                        color:{'#ff3b5c' if vol_pred=='HIGH' else '#00ff9d'};margin:8px 0">
              {vol_pred}
            </div>
            <div style="background:var(--bg3);border-radius:3px;height:6px;width:100%">
              <div style="background:{'#ff3b5c' if vol_pred=='HIGH' else '#00ff9d'};
                          border-radius:3px;height:6px;width:{vol_conf*100:.0f}%"></div>
            </div>
            <div class="slbl" style="margin-top:4px">Confidence: {vol_conf:.0%}</div>
          </div>

          <div class="sblock" style="text-align:center;padding:1rem;margin-top:0.5rem">
            <div class="slbl">DIRECTION FORECAST</div>
            <div style="font-family:'Orbitron',sans-serif;font-size:2rem;font-weight:800;
                        color:{'#00ff9d' if dir_pred=='UP' else '#ff3b5c'};margin:8px 0">
              {'▲' if dir_pred=='UP' else '▼'} {dir_pred}
            </div>
            <div style="background:var(--bg3);border-radius:3px;height:6px;width:100%">
              <div style="background:{'#00ff9d' if dir_pred=='UP' else '#ff3b5c'};
                          border-radius:3px;height:6px;width:{dir_conf*100:.0f}%"></div>
            </div>
            <div class="slbl" style="margin-top:4px">Confidence: {dir_conf:.0%}</div>
          </div>

          <div class="plbl" style="margin-top:0.8rem">GTI Input Features</div>
          <div class="sblock">
            <div class="slbl">GTI SCORE</div>
            <div class="sval">{score_100:.1f}</div>
          </div>
          <div class="sblock">
            <div class="slbl">CONFLICT COUNT</div>
            <div class="sval">{conflict_ct}</div>
          </div>
          <div class="sblock">
            <div class="slbl">GDELT AVG TONE</div>
            <div class="sval" style="font-size:1rem">{avg_tone:+.2f}</div>
          </div>
          <div class="sblock">
            <div class="slbl">VADER AVG COMPOUND</div>
            <div class="sval" style="font-size:1rem">{vader_avg:+.3f}</div>
          </div>

          <div class="plbl" style="margin-top:0.8rem">GTI Weights</div>
          <div class="sblock" style="font-size:0.65rem;color:#a8c4dc;line-height:2">
            <div style="display:flex;justify-content:space-between">
              <span>Conflict ratio</span><span style="color:#00c8ff">50%</span>
            </div>
            <div style="display:flex;justify-content:space-between">
              <span>GDELT tone</span><span style="color:#00c8ff">30%</span>
            </div>
            <div style="display:flex;justify-content:space-between">
              <span>VADER RSS</span><span style="color:#00c8ff">20%</span>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="cpanel">', unsafe_allow_html=True)

        # GTI components over time (0-100 scale)
        st.markdown('<div class="sec-hdr">GTI COMPONENT BREAKDOWN — 48H</div>', unsafe_allow_html=True)
        if not gti_df.empty:
            fig_comp = go.Figure()
            fig_comp.add_trace(go.Scatter(
                x=gti_df["timestamp"], y=gti_df["gti_score"] * 100,
                mode="lines", name="GTI (composite)",
                line=dict(color="#00c8ff", width=2.5),
            ))
            if "avg_tone" in gti_df.columns:
                tn = ((-gti_df["avg_tone"]+100)/200).clip(0,1) * 100
                fig_comp.add_trace(go.Scatter(x=gti_df["timestamp"], y=tn,
                    mode="lines", name="Tone signal (30% weight)",
                    line=dict(color="#9b59b6", width=1.5)))
            if "vader_avg" in gti_df.columns:
                vn = ((-gti_df["vader_avg"]+1)/2).clip(0,1) * 100
                fig_comp.add_trace(go.Scatter(x=gti_df["timestamp"], y=vn,
                    mode="lines", name="VADER signal (20% weight)",
                    line=dict(color="#ff6b35", width=1.5)))
            if "conflict_ct" in gti_df.columns:
                mx = max(gti_df["conflict_ct"].max(), 1)
                fig_comp.add_trace(go.Scatter(x=gti_df["timestamp"],
                    y=(gti_df["conflict_ct"]/mx).clip(0,1) * 100,
                    mode="lines", name="Conflict ratio (50% weight)",
                    line=dict(color="#ffb800", width=1.5)))
            fig_comp.add_hline(y=35, line_dash="dot", line_color="rgba(0,255,157,0.3)", line_width=1)
            fig_comp.add_hline(y=60, line_dash="dot", line_color="rgba(255,184,0,0.3)",  line_width=1)
            fig_comp.add_hline(y=80, line_dash="dot", line_color="rgba(255,59,92,0.3)",   line_width=1)
            fig_comp.update_layout(**PLOT_BASE, margin=_M8, height=260,
                xaxis={**_AX},
                yaxis=dict(range=[0,100], gridcolor="#111c30", zeroline=False, title="Score (0-100)"),
                legend=dict(orientation="h", y=1.1, font=dict(size=9,color="#3a5070"),
                            bgcolor="rgba(0,0,0,0)"),
                hovermode="x unified")
            st.plotly_chart(fig_comp, use_container_width=True,
                            config={"displayModeBar":False}, key="ai_comp_chart")
        else:
            st.markdown('<div class="ccard"><div class="cempty">NO DATA</div></div>', unsafe_allow_html=True)

        # Prediction history
        st.markdown('<div class="sec-hdr">PREDICTION HISTORY — 48H</div>', unsafe_allow_html=True)
        if not pred_h.empty:
            fig_pred = go.Figure()
            fig_pred.add_trace(go.Scatter(
                x=pred_h["timestamp"], y=pred_h["vol_prob"],
                mode="lines+markers", name="Vol Prob (HIGH)",
                line=dict(color="#ff3b5c", width=1.5),
                marker=dict(size=4),
            ))
            fig_pred.add_trace(go.Scatter(
                x=pred_h["timestamp"], y=pred_h["dir_prob"],
                mode="lines+markers", name="Dir Prob (UP)",
                line=dict(color="#00ff9d", width=1.5),
                marker=dict(size=4),
            ))
            fig_pred.add_hline(y=0.5, line_dash="dot", line_color="rgba(255,255,255,0.15)", line_width=1)
            fig_pred.update_layout(**PLOT_BASE, margin=_M8, height=200,
                xaxis={**_AX},
                yaxis=dict(range=[0,1], gridcolor="#111c30", zeroline=False),
                legend=dict(orientation="h", y=1.1, font=dict(size=9,color="#3a5070"),
                            bgcolor="rgba(0,0,0,0)"),
                hovermode="x unified")
            st.plotly_chart(fig_pred, use_container_width=True,
                            config={"displayModeBar":False}, key="ai_pred_chart")
        else:
            st.markdown('<div class="ccard"><div class="cempty">NO PREDICTION HISTORY — RUN BACKFILL</div></div>',
                        unsafe_allow_html=True)

        # Sentiment distribution
        st.markdown('<div class="sec-hdr">SENTIMENT BREAKDOWN — CURRENT BATCH</div>', unsafe_allow_html=True)
        fig_sent = go.Figure()
        fig_sent.add_trace(go.Bar(x=[pos_ct], y=[""], orientation="h",
            name="Positive", marker_color="rgba(0,255,157,0.7)",
            text=[f"▲ {pos_ct} POS"], textposition="inside",
            textfont=dict(size=10,color="#fff")))
        fig_sent.add_trace(go.Bar(x=[neu_ct], y=[""], orientation="h",
            name="Neutral", marker_color="rgba(58,80,112,0.5)",
            text=[f"⚫ {neu_ct} NEU"], textposition="inside",
            textfont=dict(size=10,color="#fff")))
        fig_sent.add_trace(go.Bar(x=[neg_ct], y=[""], orientation="h",
            name="Negative", marker_color="rgba(255,59,92,0.7)",
            text=[f"▼ {neg_ct} NEG"], textposition="inside",
            textfont=dict(size=10,color="#fff")))
        fig_sent.update_layout(**PLOT_BASE, barmode="stack", height=80,
            showlegend=False, margin=dict(l=4,r=4,t=4,b=4),
            yaxis=dict(showticklabels=False, gridcolor="rgba(0,0,0,0)", showline=False, zeroline=False),
            xaxis=dict(showticklabels=False, gridcolor="rgba(0,0,0,0)", showgrid=False, showline=False, zeroline=False))
        st.plotly_chart(fig_sent, use_container_width=True,
                        config={"displayModeBar":False}, key="ai_sent_chart")

        st.markdown('</div>', unsafe_allow_html=True)

    with c3:
        html = '<div class="rpanel"><div class="plbl">FULL IMPACT ANALYSIS</div>'
        html += '<div style="font-size:0.57rem;color:#3a5070;margin-bottom:0.7rem;line-height:1.5">Keyword × VADER · 11 assets tracked</div>'
        for item in impacts:
            s = item["signal"]
            mc = item["match_ct"]
            html += (f'<div class="tcard {CARD_CLS[s]}" style="margin-bottom:0.5rem">'
                     f'<div style="display:flex;justify-content:space-between;align-items:flex-start">'
                     f'<div><div class="tpair">{item["asset"]}</div>'
                     f'<div class="ttype">{item["type"]}</div></div>'
                     f'<span class="tsig {SIG_CLS[s]}">{SIG_LBL[s]}</span></div>'
                     f'<div class="treason" style="margin-top:5px">{item["reason"]}</div>'
                     f'<div class="tct">{mc} trigger{"s" if mc!=1 else ""} · {item["name"]}</div>'
                     f'</div>')
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
#  TAB 4 — MARKET  (SPY / VIX / GLD charts + returns analysis)
# ═══════════════════════════════════════════════════════════════════════════
with tab4:
    # ── Top row: 3 symbol cards ──────────────────────────────────────────
    mc1, mc2, mc3 = st.columns(3)

    def mkt_card(df: pd.DataFrame, sym: str, col: str):
        if df.empty:
            return (f'<div class="sblock"><div class="slbl">{sym}</div>'
                    f'<div class="sval">—</div><div class="slbl">No data</div></div>')
        try:
            last  = float(df["close"].iloc[-1])
            first = float(df["close"].iloc[0])
            chg   = (last-first)/first*100
            color = "#00ff9d" if chg>=0 else "#ff3b5c"
            arrow = "▲" if chg>=0 else "▼"
            return (f'<div class="sblock">'
                    f'<div class="slbl">{sym}</div>'
                    f'<div class="sval" style="font-size:1.6rem">{last:.2f}</div>'
                    f'<div style="font-size:0.75rem;color:{color};font-weight:700;margin-top:2px">'
                    f'{arrow} {abs(chg):.2f}% (48h)</div></div>')
        except Exception:
            return (f'<div class="sblock"><div class="slbl">{sym}</div>'
                    f'<div class="sval">—</div><div class="slbl">Error</div></div>')

    with mc1:
        st.markdown(f'<div style="padding:0.8rem 0.5rem">{mkt_card(spy_df,"SPY","#00c8ff")}</div>',
                    unsafe_allow_html=True)
    with mc2:
        st.markdown(f'<div style="padding:0.8rem 0.5rem">{mkt_card(vix_df,"VIX","#ffb800")}</div>',
                    unsafe_allow_html=True)
    with mc3:
        st.markdown(f'<div style="padding:0.8rem 0.5rem">{mkt_card(gld_df,"GLD","#ffb800")}</div>',
                    unsafe_allow_html=True)

    # ── SPY Candlestick full width ───────────────────────────────────────
    st.markdown('<div style="padding:0 0.5rem">', unsafe_allow_html=True)
    st.markdown('<div class="sec-hdr">SPY — S&P 500 ETF · 48H CANDLESTICK</div>', unsafe_allow_html=True)
    if not spy_df.empty:
        try:
            fig_spy = go.Figure(go.Candlestick(
                x=spy_df["timestamp"],
                open=spy_df["open"], high=spy_df["high"],
                low=spy_df["low"],   close=spy_df["close"],
                increasing=dict(line=dict(color="#00ff9d"), fillcolor="rgba(0,255,157,0.3)"),
                decreasing=dict(line=dict(color="#ff3b5c"), fillcolor="rgba(255,59,92,0.3)"),
            ))
            if "volume" in spy_df.columns:
                fig_spy.add_trace(go.Bar(
                    x=spy_df["timestamp"], y=spy_df["volume"],
                    name="Volume", yaxis="y2",
                    marker_color="rgba(0,200,255,0.15)",
                ))
                fig_spy.update_layout(yaxis2=dict(overlaying="y", side="right",
                    showgrid=False, showticklabels=False,
                    range=[0, spy_df["volume"].max()*5]))
            fig_spy.update_layout(**PLOT_BASE, margin=_M8, height=320,
                xaxis=dict(**_AX, rangeslider_visible=False),
                yaxis={**_AX},
                hovermode="x unified")
            st.plotly_chart(fig_spy, use_container_width=True,
                            config={"displayModeBar":False}, key="mkt_spy_chart")
        except Exception:
            st.markdown('<div class="ccard"><div class="cempty" style="height:320px">SPY DATA ERROR</div></div>',
                        unsafe_allow_html=True)
    else:
        st.markdown('<div class="ccard"><div class="cempty" style="height:320px">NO SPY DATA — RUN market_fetcher.py</div></div>',
                    unsafe_allow_html=True)

    # ── VIX and GLD side by side ─────────────────────────────────────────
    mv1, mv2 = st.columns(2)
    with mv1:
        st.markdown('<div class="sec-hdr">VIX — CBOE VOLATILITY INDEX · 48H</div>', unsafe_allow_html=True)
        if not vix_df.empty:
            try:
                fig_vix = go.Figure()
                fig_vix.add_hrect(y0=0,  y1=20, fillcolor="rgba(0,255,157,0.04)",  line_width=0)
                fig_vix.add_hrect(y0=20, y1=30, fillcolor="rgba(255,184,0,0.04)",  line_width=0)
                fig_vix.add_hrect(y0=30, y1=100,fillcolor="rgba(255,59,92,0.04)",  line_width=0)
                fig_vix.add_trace(go.Scatter(
                    x=vix_df["timestamp"], y=vix_df["close"],
                    mode="lines", line=dict(color="#ffb800", width=2),
                    fill="tozeroy", fillcolor="rgba(255,184,0,0.06)",
                ))
                fig_vix.add_hline(y=20, line_dash="dot", line_color="rgba(255,184,0,0.3)", line_width=1)
                fig_vix.add_hline(y=30, line_dash="dot", line_color="rgba(255,59,92,0.3)",  line_width=1)
                fig_vix.update_layout(**PLOT_BASE, margin=_M8, height=240,
                    xaxis={**_AX}, yaxis={**_AX}, hovermode="x unified")
                st.plotly_chart(fig_vix, use_container_width=True,
                                config={"displayModeBar":False}, key="mkt_vix_chart")
            except Exception:
                st.markdown('<div class="ccard"><div class="cempty">VIX DATA ERROR</div></div>',
                            unsafe_allow_html=True)
        else:
            st.markdown('<div class="ccard"><div class="cempty">NO VIX DATA</div></div>',
                        unsafe_allow_html=True)

    with mv2:
        st.markdown('<div class="sec-hdr">GLD — GOLD ETF · 48H</div>', unsafe_allow_html=True)
        if not gld_df.empty:
            try:
                fig_gld = go.Figure()
                fig_gld.add_trace(go.Scatter(
                    x=gld_df["timestamp"], y=gld_df["close"],
                    mode="lines", line=dict(color="#ffb800", width=2),
                    fill="tozeroy", fillcolor="rgba(255,184,0,0.06)",
                ))
                if "high" in gld_df.columns and "low" in gld_df.columns:
                    fig_gld.add_trace(go.Scatter(
                        x=pd.concat([gld_df["timestamp"], gld_df["timestamp"][::-1]]),
                        y=pd.concat([gld_df["high"], gld_df["low"][::-1]]),
                        fill="toself", fillcolor="rgba(255,184,0,0.04)",
                        line=dict(color="rgba(255,255,255,0)"), name="H/L band",
                    ))
                fig_gld.update_layout(**PLOT_BASE, margin=_M8, height=240,
                    xaxis={**_AX}, yaxis={**_AX},
                    hovermode="x unified", showlegend=False)
                st.plotly_chart(fig_gld, use_container_width=True,
                                config={"displayModeBar":False}, key="mkt_gld_chart")
            except Exception:
                st.markdown('<div class="ccard"><div class="cempty">GLD DATA ERROR</div></div>',
                            unsafe_allow_html=True)
        else:
            st.markdown('<div class="ccard"><div class="cempty">NO GLD DATA</div></div>',
                        unsafe_allow_html=True)

    # ── GTI vs SPY Returns scatter ───────────────────────────────────────
    if not spy_df.empty and not gti_df.empty:
        try:
            st.markdown('<div class="sec-hdr" style="margin-top:0.3rem">GTI SCORE vs SPY RETURNS — CORRELATION VIEW</div>',
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
                                   on="timestamp", direction="nearest")
            merged = merged.dropna()

            if not merged.empty:
                scatter_col = merged["return"].apply(
                    lambda r: "#00ff9d" if r>0 else "#ff3b5c")
                fig_scatter = go.Figure(go.Scatter(
                    x=merged["gti_score"] * 100,
                    y=merged["return"],
                    mode="markers",
                    marker=dict(color=scatter_col, size=7, opacity=0.7,
                                line=dict(width=0.5, color="rgba(255,255,255,0.1)")),
                    text=merged["timestamp"].astype(str),
                    hovertemplate="GTI: %{x:.1f}<br>Return: %{y:.3f}%<extra></extra>",
                ))
                fig_scatter.add_vline(x=35, line_dash="dot", line_color="rgba(0,255,157,0.3)", line_width=1)
                fig_scatter.add_vline(x=60, line_dash="dot", line_color="rgba(255,184,0,0.3)",  line_width=1)
                fig_scatter.add_vline(x=80, line_dash="dot", line_color="rgba(255,59,92,0.3)",   line_width=1)
                fig_scatter.add_hline(y=0,  line_dash="dot", line_color="rgba(255,255,255,0.1)", line_width=1)
                fig_scatter.update_layout(**PLOT_BASE, margin=_M8, height=260,
                    xaxis=dict(title="GTI Score (0–100)", range=[0,100],
                               gridcolor="#111c30", zeroline=False, showline=False),
                    yaxis=dict(title="SPY Return %", gridcolor="#111c30", zeroline=False, showline=False))
                st.plotly_chart(fig_scatter, use_container_width=True,
                                config={"displayModeBar":False}, key="mkt_scatter_chart")
        except Exception:
            pass

    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
#  BOTTOM STATUS BAR  (always visible)
# ═══════════════════════════════════════════════════════════════════════════
next_ref = (now_utc + timedelta(seconds=60)).strftime("%H:%M:%S")
st.markdown(f"""
<div class="statusbar">
  <div>SOURCES <span class="sb-val">GDELT · Reuters · BBC · AP · Al Jazeera</span></div>
  <div>MODEL <span class="sb-val">LightGBM · VADER NLP · APScheduler</span></div>
  <div>STORAGE <span class="sb-val">SQLite Local</span></div>
  <div>GTI <span class="sb-val">{score_100:.1f}</span></div>
  <div>COUNTRIES <span class="sb-val">{len(country_df) if not country_df.empty else 0}</span></div>
  <div>ARTICLES <span class="sb-val">{total_news}</span></div>
  <div style="margin-left:auto">NEXT REFRESH <span class="sb-val">{next_ref} UTC</span></div>
</div>
""", unsafe_allow_html=True)


# ── Non-blocking 60-second auto-refresh ───────────────────────────────────
if time.time() - st.session_state["last_refresh"] > 60:
    st.session_state["last_refresh"] = time.time()
    st.rerun()
