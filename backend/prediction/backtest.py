"""
Backtest
========
Evaluates trained model accuracy on held-out historical data.
Prints accuracy, precision, recall, F1 for both classifiers.

Re-run monthly to check for model drift. If accuracy drops significantly
below initial training scores, retrain with:
  python prediction/train.py --days 60

Usage:
  python prediction/backtest.py
  python prediction/backtest.py --days 60
"""

import argparse
import os

import joblib
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

from config import LGBM_VOL_PATH, LGBM_DIR_PATH
from prediction.features import build_feature_matrix, FEATURE_COLS


def run_backtest(lookback_days: int = 30):
    for path in [LGBM_VOL_PATH, LGBM_DIR_PATH]:
        if not os.path.exists(path):
            print(f"Model not found: {path}")
            print("Run: python prediction/train.py")
            return

    df = build_feature_matrix(lookback_days=lookback_days)
    if df.empty or len(df) < 50:
        print(f"Not enough data ({len(df)} rows). Run backfill first.")
        return

    X     = df[FEATURE_COLS]
    y_vol = df["target_vol"]
    y_dir = df["target_dir"]

    # Time-ordered split — same as training
    _, X_te, _, yv_te = train_test_split(X, y_vol, test_size=0.2, shuffle=False)
    _, _,    _, yd_te = train_test_split(X, y_dir, test_size=0.2, shuffle=False)

    vol_model = joblib.load(LGBM_VOL_PATH)
    dir_model = joblib.load(LGBM_DIR_PATH)

    print(f"\nBacktest on {len(X_te)} held-out rows ({lookback_days}d lookback)\n")

    print("── Volatility Model ─────────────────────────────────")
    vol_pred = vol_model.predict(X_te)
    print(f"Accuracy: {accuracy_score(yv_te, vol_pred):.3f}")
    print(classification_report(yv_te, vol_pred,
                                 target_names=["Low Vol", "High Vol"],
                                 zero_division=0))

    print("── Direction Model ──────────────────────────────────")
    dir_pred = dir_model.predict(X_te)
    print(f"Accuracy: {accuracy_score(yd_te, dir_pred):.3f}")
    print(classification_report(yd_te, dir_pred,
                                 target_names=["Down", "Up"],
                                 zero_division=0))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backtest trained models")
    parser.add_argument("--days", type=int, default=30)
    args = parser.parse_args()
    run_backtest(args.days)
