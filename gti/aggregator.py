"""
GTI Aggregator
==============
Combines three data signals into a single Geopolitical Tension Index (GTI)
score, normalized to 0.0 – 1.0.

  0.0 = completely calm world
  1.0 = maximum recorded tension

How the score is built:
  Signal 1 — GDELT Conflict Ratio (weight 0.50)
    Fraction of GDELT events in the last N hours where GoldsteinScale < -5.
    GoldsteinScale measures event intensity: deeply negative = military force,
    coups, wars. We count how many events fall below the conflict threshold
    and divide by total events to get a ratio.

  Signal 2 — GDELT Tone (weight 0.30)
    Average AvgTone across all GDELT events in the window.
    AvgTone ranges -100 (most negative) to +100 (most positive).
    We invert and normalize: (−tone + 100) / 200 → [0,1]
    Deeply negative media tone = high tension.

  Signal 3 — VADER RSS Sentiment (weight 0.20)
    Average VADER compound score across recent RSS headlines.
    Compound ranges −1 (most negative) to +1 (most positive).
    We invert and normalize: (−compound + 1) / 2 → [0,1]

Final GTI = 0.50 * conflict_ratio + 0.30 * tone_norm + 0.20 * vader_norm

Usage:
  python gti/aggregator.py
"""

from datetime import datetime, timedelta

from config import (
    GTI_DB, NEWS_DB,
    GTI_WINDOW_HOURS, GTI_CONFLICT_THRESHOLD,
    MAX_ROWS,
)
from ingestion.db import get_conn


def _clamp(val: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, val))


def compute_gti(window_hours: int = None) -> dict:
    """
    Compute the current GTI score from the last `window_hours` of data.
    Returns a dict with gti_score, conflict_ct, avg_tone, vader_avg.
    """
    window_hours = window_hours or GTI_WINDOW_HOURS
    cutoff = (datetime.utcnow() - timedelta(hours=window_hours)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # ── Signal 1 & 2: GDELT ──────────────────────────────────────────────
    conn = get_conn(NEWS_DB)
    gdelt_rows = conn.execute(
        f"""SELECT goldstein_scale, avg_tone
            FROM gdelt_events
            WHERE timestamp >= ?
            LIMIT {MAX_ROWS}""",
        (cutoff,),
    ).fetchall()
    conn.close()

    if gdelt_rows:
        scales = [
            r["goldstein_scale"]
            for r in gdelt_rows
            if r["goldstein_scale"] is not None
        ]
        tones = [
            r["avg_tone"]
            for r in gdelt_rows
            if r["avg_tone"] is not None
        ]

        conflict_ct    = sum(1 for s in scales if s < GTI_CONFLICT_THRESHOLD)
        conflict_ratio = conflict_ct / max(len(scales), 1)

        avg_tone_raw = sum(tones) / len(tones) if tones else 0.0
        tone_norm    = _clamp((-avg_tone_raw + 100.0) / 200.0)
    else:
        conflict_ct    = 0
        conflict_ratio = 0.0
        avg_tone_raw   = 0.0
        tone_norm      = 0.5   # neutral fallback

    # ── Signal 3: VADER RSS ───────────────────────────────────────────────
    conn = get_conn(NEWS_DB)
    rss_rows = conn.execute(
        f"""SELECT vader_compound
            FROM rss_articles
            WHERE fetched_at >= ?
            LIMIT {MAX_ROWS}""",
        (cutoff,),
    ).fetchall()
    conn.close()

    if rss_rows:
        compounds = [
            r["vader_compound"]
            for r in rss_rows
            if r["vader_compound"] is not None
        ]
        vader_avg_raw = sum(compounds) / len(compounds) if compounds else 0.0
        vader_norm    = _clamp((-vader_avg_raw + 1.0) / 2.0)
    else:
        vader_avg_raw = 0.0
        vader_norm    = 0.5   # neutral fallback

    # ── Weighted GTI ─────────────────────────────────────────────────────
    gti = _clamp(
        conflict_ratio * 0.50
        + tone_norm    * 0.30
        + vader_norm   * 0.20
    )

    return {
        "gti_score":   round(gti,           4),
        "conflict_ct": conflict_ct,
        "avg_tone":    round(avg_tone_raw,   4),
        "vader_avg":   round(vader_avg_raw,  4),
    }


def save_gti(result: dict):
    """Persist a GTI result to the gti_scores table."""
    ts   = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    conn = get_conn(GTI_DB)
    conn.execute(
        """INSERT OR REPLACE INTO gti_scores
           (timestamp, gti_score, conflict_ct, avg_tone, vader_avg)
           VALUES (?,?,?,?,?)""",
        (
            ts,
            result["gti_score"],
            result["conflict_ct"],
            result["avg_tone"],
            result["vader_avg"],
        ),
    )
    conn.commit()
    conn.close()

    level = (
        "LOW"      if result["gti_score"] < 0.3 else
        "MODERATE" if result["gti_score"] < 0.6 else
        "HIGH"
    )
    print(
        f"GTI [{ts}]  score={result['gti_score']:.4f}  level={level}"
        f"  conflicts={result['conflict_ct']}"
        f"  tone={result['avg_tone']:.2f}"
        f"  vader={result['vader_avg']:.3f}"
    )


def run() -> dict:
    """Compute GTI and save it. Called by scheduler every 15 minutes."""
    result = compute_gti()
    save_gti(result)
    return result


if __name__ == "__main__":
    run()
