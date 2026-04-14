"""
Streamlit Dashboard
===================
Opens at http://localhost:8501 — run with:
  streamlit run dashboard/app.py

Layout:
  Row 1 — 4 KPI cards: GTI score, volatility forecast, direction forecast, conflict count
  Row 2 — GTI 24h line chart  |  SPY candlestick chart
  Row 3 — Recent headlines feed with sentiment badges

Auto-refreshes every 60 seconds (meta-refresh).
Data is cached for 60 seconds (st.cache_data ttl).
"""

import sqlite3
from datetime import datetime, timedelta

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from config import GTI_DB, NEWS_DB, MARKET_DB, PREDICTIONS_DB, MAX_ROWS

# ── Page config ───────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Geopolitical Market Dashboard",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Auto-refresh every 60s
st.markdown('<meta http-equiv="refresh" content="60">', unsafe_allow_html=True)


# ── Data helpers ──────────────────────────────────────────────────────────

def _query(db_path: str, sql: str, params: tuple = ()) -> pd.DataFrame:
    """Safe SQLite query — returns empty DataFrame on any error."""
    try:
        conn = sqlite3.connect(db_path)
        df   = pd.read_sql_query(sql, conn, params=params)
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()


def _gti_color(score: float) -> str:
    if score < 0.3:
        return "#27ae60"
    if score < 0.6:
        return "#e67e22"
    return "#e74c3c"


def _gti_level(score: float) -> str:
    if score < 0.3:
        return "LOW TENSION"
    if score < 0.6:
        return "MODERATE"
    return "HIGH TENSION"


# ── Cached loaders ────────────────────────────────────────────────────────

@st.cache_data(ttl=60)
def load_gti_history(hours: int = 48) -> pd.DataFrame:
    cutoff = (datetime.utcnow() - timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M:%S")
    return _query(
        GTI_DB,
        f"SELECT * FROM gti_scores WHERE timestamp >= ? ORDER BY timestamp LIMIT {MAX_ROWS}",
        (cutoff,),
    )


@st.cache_data(ttl=60)
def load_latest_prediction() -> dict:
    df = _query(PREDICTIONS_DB, "SELECT * FROM predictions ORDER BY timestamp DESC LIMIT 1")
    return df.iloc[0].to_dict() if not df.empty else {}


@st.cache_data(ttl=60)
def load_market(symbol: str = "SPY", hours: int = 48) -> pd.DataFrame:
    cutoff = (datetime.utcnow() - timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M:%S")
    return _query(
        MARKET_DB,
        f"""SELECT * FROM ohlcv WHERE symbol=? AND timestamp >= ?
            ORDER BY timestamp LIMIT {MAX_ROWS}""",
        (symbol, cutoff),
    )


@st.cache_data(ttl=60)
def load_news(limit: int = 25) -> pd.DataFrame:
    return _query(
        NEWS_DB,
        f"""SELECT title, source, published_at, vader_compound, vader_label
            FROM rss_articles ORDER BY published_at DESC LIMIT {limit}""",
    )


# ── Main layout ───────────────────────────────────────────────────────────

st.title("🌐 Geopolitical Tension Index — Market Dashboard")
st.caption(f"UTC {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}  ·  refreshes every 60s")

gti_df = load_gti_history()
pred   = load_latest_prediction()

# ── KPI cards ─────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)

with c1:
    if not gti_df.empty:
        score = float(gti_df["gti_score"].iloc[-1])
        delta = _gti_level(score)
        st.metric("GTI Score", f"{score:.3f}", delta)
    else:
        st.metric("GTI Score", "—", "No data yet")

with c2:
    if pred:
        icon  = "⬆" if pred.get("vol_prediction") == "HIGH" else "⬇"
        label = pred.get("vol_prediction", "—")
        conf  = pred.get("vol_prob", 0)
        st.metric("Volatility (next hour)", f"{icon} {label}", f"{conf:.0%} confidence")
    else:
        st.metric("Volatility (next hour)", "—", "No model output")

with c3:
    if pred:
        icon  = "🟢" if pred.get("dir_prediction") == "UP" else "🔴"
        label = pred.get("dir_prediction", "—")
        conf  = pred.get("dir_prob", 0)
        st.metric("Direction (next hour)", f"{icon} {label}", f"{conf:.0%} confidence")
    else:
        st.metric("Direction (next hour)", "—", "No model output")

with c4:
    if not gti_df.empty:
        ct = int(gti_df["conflict_ct"].iloc[-1])
        st.metric("Conflict Events (6h window)", ct)
    else:
        st.metric("Conflict Events (6h window)", "—")

st.divider()

# ── Charts ────────────────────────────────────────────────────────────────
left, right = st.columns(2)

with left:
    st.subheader("GTI — 48h History")
    if not gti_df.empty:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=gti_df["timestamp"],
            y=gti_df["gti_score"],
            mode="lines+markers",
            name="GTI",
            line=dict(color="#3498db", width=2),
            marker=dict(size=4),
        ))
        fig.add_hrect(y0=0,   y1=0.3, fillcolor="#27ae60", opacity=0.07, line_width=0)
        fig.add_hrect(y0=0.3, y1=0.6, fillcolor="#e67e22", opacity=0.07, line_width=0)
        fig.add_hrect(y0=0.6, y1=1.0, fillcolor="#e74c3c", opacity=0.07, line_width=0)
        fig.add_hline(y=0.3, line_dash="dash", line_color="#27ae60", line_width=1)
        fig.add_hline(y=0.6, line_dash="dash", line_color="#e74c3c", line_width=1)
        fig.update_layout(
            yaxis=dict(range=[0, 1], title="GTI Score"),
            height=320,
            margin=dict(l=10, r=10, t=10, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No GTI data yet. Start the scheduler: `python scheduler.py`")

with right:
    st.subheader("SPY — 48h Candlestick")
    spy_df = load_market("SPY", 48)
    if not spy_df.empty:
        fig = go.Figure(go.Candlestick(
            x=spy_df["timestamp"],
            open=spy_df["open"],
            high=spy_df["high"],
            low=spy_df["low"],
            close=spy_df["close"],
            name="SPY",
            increasing_line_color="#27ae60",
            decreasing_line_color="#e74c3c",
        ))
        fig.update_layout(
            height=320,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis_rangeslider_visible=False,
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No market data yet. Run: `python ingestion/market_fetcher.py`")

st.divider()

# ── GTI component breakdown ───────────────────────────────────────────────
if not gti_df.empty and len(gti_df) > 1:
    with st.expander("GTI Component Breakdown", expanded=False):
        comp_cols = st.columns(3)
        latest = gti_df.iloc[-1]
        with comp_cols[0]:
            st.metric("Avg GDELT Tone",  f"{latest.get('avg_tone', 0):.2f}")
        with comp_cols[1]:
            st.metric("Avg VADER Score", f"{latest.get('vader_avg', 0):.3f}")
        with comp_cols[2]:
            st.metric("Conflict Events", int(latest.get("conflict_ct", 0)))

        fig2 = go.Figure()
        if "avg_tone" in gti_df.columns:
            fig2.add_trace(go.Scatter(
                x=gti_df["timestamp"], y=gti_df["avg_tone"],
                name="GDELT Tone", line=dict(color="#9b59b6"),
            ))
        if "vader_avg" in gti_df.columns:
            # Scale vader (-1,1) to similar range as tone
            fig2.add_trace(go.Scatter(
                x=gti_df["timestamp"],
                y=gti_df["vader_avg"] * 50,
                name="VADER ×50", line=dict(color="#e67e22", dash="dot"),
            ))
        fig2.update_layout(height=200, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ── News feed ─────────────────────────────────────────────────────────────
st.subheader("📰 Latest Headlines")
news_df = load_news(25)

if not news_df.empty:
    badge_map = {"negative": "🔴", "positive": "🟢", "neutral": "⚪"}
    for _, row in news_df.iterrows():
        badge   = badge_map.get(row.get("vader_label", "neutral"), "⚪")
        score   = row.get("vader_compound", 0.0)
        source  = row.get("source", "")
        pub     = row.get("published_at", "")[:16]
        st.markdown(
            f"{badge} **{row['title']}**  \n"
            f"<sub style='color:gray'>{source} &nbsp;·&nbsp; {pub} &nbsp;·&nbsp; "
            f"sentiment: {score:+.3f}</sub>",
            unsafe_allow_html=True,
        )
else:
    st.info("No headlines yet. Start the scheduler to begin collecting data.")

st.divider()
st.caption(
    "Data sources: GDELT · Reuters · BBC · Al Jazeera · AP · NewsAPI · yfinance  |  "
    "Model: LightGBM  |  NLP: VADER  |  Storage: SQLite"
)
