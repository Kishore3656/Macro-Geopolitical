"""
Drift Detection
===============
Monitors model accuracy in real-time and triggers retraining when performance degrades.

How it works:
  1. Every 15 minutes, the predictor saves predictions to predictions.db
  2. Every 15 minutes (offset), outcome_resolver checks if predictions are 1+ hours old
  3. If old enough, it fetches the actual next-hour close and marks outcome
  4. Drift detector queries the last 50 resolved predictions and computes accuracy
  5. If accuracy < 0.52 or if last training was > 14 days ago, flag for retraining

The drift_detected flag is surfaced in /api/model/status for the dashboard.
"""

from datetime import datetime, timedelta
import sqlite3
from config import PREDICTIONS_DB
from ingestion.db import get_conn


class DriftDetector:
    """Monitor prediction accuracy and detect model degradation."""

    def __init__(self, window: int = 50, threshold: float = 0.52, min_samples: int = 30):
        """
        Parameters
        ----------
        window       : number of recent resolved predictions to evaluate
        threshold    : accuracy below this triggers retraining (0.52 = slightly-better-than-coin-flip)
        min_samples  : don't flag if fewer than this many resolved predictions exist
        """
        self.window = window
        self.threshold = threshold
        self.min_samples = min_samples

    def get_recent_accuracy(self, model_type: str) -> dict:
        """
        Query predictions.db for recent resolved predictions.

        Parameters
        ----------
        model_type  : "direction" or "volatility"

        Returns
        -------
        dict with keys:
            n           : number of resolved predictions in window
            accuracy    : float between 0 and 1
            drift_detected : bool (accuracy below threshold)
        """
        conn = get_conn(PREDICTIONS_DB)

        # Map model type to outcome column
        outcome_col = "actual_dir_outcome" if model_type == "direction" else "actual_vol_outcome"

        rows = conn.execute(
            f"""
            SELECT {outcome_col}
            FROM predictions
            WHERE outcome_resolved = 1 AND {outcome_col} IS NOT NULL
            ORDER BY timestamp DESC
            LIMIT ?
            """,
            (self.window,),
        ).fetchall()
        conn.close()

        if not rows:
            return {
                "n": 0,
                "accuracy": 0.0,
                "drift_detected": False,
                "reason": "no resolved predictions yet"
            }

        n = len(rows)
        # outcome is 1 (correct) or 0 (wrong)
        correct = sum(1 for r in rows if r[0] == 1)
        accuracy = correct / n if n > 0 else 0.0

        drift_detected = accuracy < self.threshold and n >= self.min_samples
        reason = f"accuracy {accuracy:.3f} below threshold {self.threshold}" if drift_detected else "ok"

        return {
            "n": n,
            "accuracy": round(accuracy, 4),
            "drift_detected": drift_detected,
            "reason": reason
        }

    def should_retrain(self, last_trained_at: datetime = None) -> tuple[bool, str]:
        """
        Check if retraining should be triggered.

        Parameters
        ----------
        last_trained_at  : datetime of last successful training, or None if never trained

        Returns
        -------
        (should_retrain: bool, reason: str)
        """
        if last_trained_at is None:
            return (True, "no models have been trained yet")

        # Check time since last training
        days_since = (datetime.utcnow() - last_trained_at).days
        if days_since > 14:
            return (True, f"last trained {days_since} days ago (threshold: 14 days)")

        # Check direction model accuracy
        dir_acc = self.get_recent_accuracy("direction")
        if dir_acc["drift_detected"]:
            return (True, f"direction model drift: {dir_acc['reason']}")

        # Check volatility model accuracy
        vol_acc = self.get_recent_accuracy("volatility")
        if vol_acc["drift_detected"]:
            return (True, f"volatility model drift: {vol_acc['reason']}")

        return (False, "models performing well")


def resolve_outcomes(lookback_hours: int = 1) -> int:
    """
    Resolve prediction outcomes for predictions that are at least lookback_hours old.

    For each unresolved prediction, fetch the actual next-hour close from market.db
    and mark whether the prediction was correct.

    Returns
    -------
    Number of outcomes resolved
    """
    from config import MARKET_DB

    conn = get_conn(PREDICTIONS_DB)
    conn_market = get_conn(MARKET_DB)

    # Find unresolved predictions older than lookback_hours
    cutoff = datetime.utcnow() - timedelta(hours=lookback_hours)
    cutoff_str = cutoff.strftime("%Y-%m-%d %H:%M:%S")

    unresolved = conn.execute(
        """
        SELECT id, timestamp, dir_prediction, vol_prediction, close
        FROM predictions
        WHERE outcome_resolved = 0 AND timestamp <= ?
        ORDER BY timestamp DESC
        LIMIT 1000
        """,
        (cutoff_str,),
    ).fetchall()

    if not unresolved:
        conn.close()
        conn_market.close()
        return 0

    resolved_count = 0

    for pred_row in unresolved:
        pred_id, pred_ts, dir_pred, vol_pred = pred_row[:4]

        # Find the actual next-hour close
        pred_dt = datetime.strptime(pred_ts, "%Y-%m-%d %H:%M:%S")
        next_hour = pred_dt + timedelta(hours=1)
        next_hour_str = next_hour.strftime("%Y-%m-%d %H:%M:%S")

        actual_row = conn_market.execute(
            """
            SELECT close
            FROM ohlcv
            WHERE symbol = 'SPY' AND timestamp = ?
            """,
            (next_hour_str,),
        ).fetchone()

        if actual_row is None:
            continue  # Next hour data not available yet

        actual_close_next = actual_row[0]

        # Get prediction timestamp close for direction calculation
        pred_close_row = conn_market.execute(
            """
            SELECT close
            FROM ohlcv
            WHERE symbol = 'SPY' AND timestamp = ?
            """,
            (pred_ts,),
        ).fetchone()

        if pred_close_row is None:
            continue

        pred_close = pred_close_row[0]

        # Evaluate predictions
        actual_dir = 1 if actual_close_next > pred_close else 0
        predicted_dir = 1 if dir_pred == "UP" else 0
        dir_outcome = 1 if actual_dir == predicted_dir else 0

        # For volatility, we need the actual volatility baseline (approximated)
        # For now, we'll use a simple metric: if actual return was high, outcome is 1
        actual_return = (actual_close_next - pred_close) / pred_close
        actual_vol = 1 if abs(actual_return) > 0.01 else 0  # Threshold: 1% return
        predicted_vol = 1 if vol_pred == "HIGH" else 0
        vol_outcome = 1 if actual_vol == predicted_vol else 0

        # Update prediction with outcomes
        conn.execute(
            """
            UPDATE predictions
            SET outcome_resolved = 1,
                actual_close_next = ?,
                actual_dir_outcome = ?,
                actual_vol_outcome = ?
            WHERE id = ?
            """,
            (actual_close_next, dir_outcome, vol_outcome, pred_id),
        )
        resolved_count += 1

    conn.commit()
    conn.close()
    conn_market.close()

    return resolved_count
