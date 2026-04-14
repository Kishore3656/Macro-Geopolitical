"""
Model Training
==============
Trains two LightGBM binary classifiers on historical feature data:

  Model 1 — Volatility Classifier  (lgbm_volatility.pkl)
    Predicts: will next-hour absolute return exceed the 20h rolling vol?
    Label 1 = high volatility, Label 0 = low volatility

  Model 2 — Direction Classifier   (lgbm_direction.pkl)
    Predicts: will price be higher next hour?
    Label 1 = up, Label 0 = down / flat

Why LightGBM?
  - CPU-native, no GPU needed
  - Trains in 2–4 minutes on 30 days of hourly data (~720 rows)
  - Small RAM footprint (~50–100MB peak)
  - Handles mixed feature types well (float + int + ratio columns)

Train/test split:
  Last 20% of rows used as held-out test (time-ordered, no shuffle).
  This prevents future data leaking into training — crucial for time series.

Usage:
  python prediction/train.py
  python prediction/train.py --days 60   # use more history
"""

import argparse
import os

import joblib
import lightgbm as lgb
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

from config import LGBM_VOL_PATH, LGBM_DIR_PATH
from prediction.features import build_feature_matrix, FEATURE_COLS

LGBM_PARAMS = {
    "objective":     "binary",
    "metric":        "binary_logloss",
    "num_leaves":    31,
    "learning_rate": 0.05,
    "n_estimators":  300,
    "min_child_samples": 10,
    "verbose":       -1,
    "n_jobs":        -1,
}


def _train_one(X_tr, y_tr, X_te, y_te, label: str) -> lgb.LGBMClassifier:
    model = lgb.LGBMClassifier(**LGBM_PARAMS)
    model.fit(
        X_tr, y_tr,
        eval_set=[(X_te, y_te)],
        callbacks=[lgb.early_stopping(50, verbose=False),
                   lgb.log_evaluation(period=-1)],
    )
    preds = model.predict(X_te)
    acc   = accuracy_score(y_te, preds)
    print(f"\n{label} — accuracy: {acc:.3f}  ({model.best_iteration_} trees)")
    print(classification_report(y_te, preds))
    return model


def train(lookback_days: int = 30):
    print(f"Building feature matrix ({lookback_days} days)...")
    df = build_feature_matrix(lookback_days=lookback_days)

    if df.empty:
        print("ERROR: No data. Run backfill first:")
        print("  python ingestion/gdelt_fetcher.py --backfill --days 30")
        print("  python ingestion/market_fetcher.py --backfill --days 30")
        return

    if len(df) < 50:
        print(f"ERROR: Only {len(df)} rows — need at least 50 to train.")
        return

    print(f"Training on {len(df)} rows, {len(FEATURE_COLS)} features.")

    X     = df[FEATURE_COLS]
    y_vol = df["target_vol"]
    y_dir = df["target_dir"]

    # Time-ordered split — no shuffle
    X_tr, X_te, yv_tr, yv_te = train_test_split(
        X, y_vol, test_size=0.2, shuffle=False
    )
    _, _, yd_tr, yd_te = train_test_split(
        X, y_dir, test_size=0.2, shuffle=False
    )

    os.makedirs(os.path.dirname(LGBM_VOL_PATH), exist_ok=True)

    print("\n── Volatility Model ─────────────────────────────")
    vol_model = _train_one(X_tr, yv_tr, X_te, yv_te, "Volatility")
    joblib.dump(vol_model, LGBM_VOL_PATH)
    print(f"Saved → {LGBM_VOL_PATH}")

    print("\n── Direction Model ──────────────────────────────")
    dir_model = _train_one(X_tr, yd_tr, X_te, yd_te, "Direction")
    joblib.dump(dir_model, LGBM_DIR_PATH)
    print(f"Saved → {LGBM_DIR_PATH}")

    print("\nTraining complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train LightGBM models")
    parser.add_argument("--days", type=int, default=30,
                        help="Days of history to use (default: 30)")
    args = parser.parse_args()
    train(args.days)
