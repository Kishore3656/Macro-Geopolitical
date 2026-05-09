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

Model versioning:
  Each trained model is saved with a timestamp (YYYYMMDD_HHMMSS) to an archive folder.
  The latest model is also saved as the live .pkl file.
  model_registry.json tracks all versions with accuracy scores.

Usage:
  python prediction/train.py
  python prediction/train.py --days 60   # use more history
"""

import argparse
import json
import os
import sys
from datetime import datetime

import joblib
import lightgbm as lgb
from sklearn.metrics import accuracy_score, classification_report, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split, cross_val_score

# Add backend directory to path for imports when run as subprocess
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import LGBM_VOL_PATH, LGBM_DIR_PATH
from prediction.features import build_feature_matrix, FEATURE_COLS

LGBM_PARAMS = {
    "objective":     "binary",
    "metric":        "binary_logloss",
    "num_leaves":    63,
    "learning_rate": 0.03,
    "n_estimators":  500,
    "min_child_samples": 5,
    "subsample":     0.8,
    "colsample_bytree": 0.8,
    "max_depth":     8,
    "lambda_l1":     1.0,
    "lambda_l2":     1.0,
    "verbose":       -1,
    "n_jobs":        -1,
}

MODEL_ARCHIVE_DIR = os.path.join(os.path.dirname(LGBM_VOL_PATH), "archive")
MODEL_REGISTRY_PATH = os.path.join(os.path.dirname(LGBM_VOL_PATH), "model_registry.json")


def _train_one(X_tr, y_tr, X_te, y_te, label: str) -> tuple[lgb.LGBMClassifier, float, float]:
    model = lgb.LGBMClassifier(**LGBM_PARAMS)
    model.fit(
        X_tr, y_tr,
        eval_set=[(X_te, y_te)],
        callbacks=[lgb.early_stopping(50, verbose=False),
                   lgb.log_evaluation(period=-1)],
    )
    preds_te = model.predict(X_te)
    preds_tr = model.predict(X_tr)
    acc_te = accuracy_score(y_te, preds_te)
    acc_tr = accuracy_score(y_tr, preds_tr)

    # Additional metrics
    prec_te = precision_score(y_te, preds_te, zero_division=0)
    rec_te = recall_score(y_te, preds_te, zero_division=0)
    f1_te = f1_score(y_te, preds_te, zero_division=0)

    print(f"\n{label} — train: {acc_tr:.3f}  test: {acc_te:.3f}  ({model.best_iteration_} trees)")
    print(f"Test metrics — Precision: {prec_te:.3f}, Recall: {rec_te:.3f}, F1: {f1_te:.3f}")
    print(classification_report(y_te, preds_te, zero_division=0))
    return model, acc_tr, acc_te


def _save_versioned(model: lgb.LGBMClassifier, live_path: str, model_type: str,
                    train_acc: float, test_acc: float, lookback_days: int,
                    trigger: str = "manual", n_rows: int = 0):
    """Save model to both live path and archive with timestamp."""
    os.makedirs(MODEL_ARCHIVE_DIR, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    archive_name = f"{os.path.splitext(os.path.basename(live_path))[0]}_{timestamp}.pkl"
    archive_path = os.path.join(MODEL_ARCHIVE_DIR, archive_name)

    joblib.dump(model, live_path)
    joblib.dump(model, archive_path)
    print(f"Saved → {live_path}")
    print(f"Archived → {archive_path}")

    # Update registry
    registry = {"volatility": [], "direction": []} if model_type == "volatility" else {"volatility": [], "direction": []}
    if os.path.exists(MODEL_REGISTRY_PATH):
        with open(MODEL_REGISTRY_PATH, "r") as f:
            registry = json.load(f)

    entry = {
        "version": timestamp,
        "trained_at": datetime.utcnow().isoformat() + "Z",
        "lookback_days": lookback_days,
        "train_accuracy": round(train_acc, 4),
        "test_accuracy": round(test_acc, 4),
        "n_rows": n_rows,
        "trigger": trigger,
    }

    key = "volatility" if "vol" in live_path.lower() else "direction"
    registry[key].insert(0, entry)
    # Keep only last 10 versions per model
    registry[key] = registry[key][:10]

    with open(MODEL_REGISTRY_PATH, "w") as f:
        json.dump(registry, f, indent=2)
    print(f"Updated registry → {MODEL_REGISTRY_PATH}")


def train(lookback_days: int = 30, trigger: str = "manual", df=None):
    if df is None:
        print(f"Building feature matrix ({lookback_days} days)...")
        df = build_feature_matrix(lookback_days=lookback_days)

    if df.empty:
        print("ERROR: No data. Run backfill first:")
        print("  python ingestion/gdelt_fetcher.py --backfill --days 30")
        print("  python ingestion/market_fetcher.py --backfill --days 30")
        return

    if len(df) < 50:
        print(f"[!] Only {len(df)} rows — using minimum viable training set.")
        if len(df) < 20:
            print(f"ERROR: Only {len(df)} rows — need at least 20 to train.")
            return

    print(f"Training on {len(df)} rows, {len(FEATURE_COLS)} features. Trigger: {trigger}")

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
    vol_model, vol_acc_tr, vol_acc_te = _train_one(X_tr, yv_tr, X_te, yv_te, "Volatility")
    _save_versioned(vol_model, LGBM_VOL_PATH, "volatility",
                    vol_acc_tr, vol_acc_te, lookback_days, trigger, len(df))

    print("\n── Direction Model ──────────────────────────────")
    dir_model, dir_acc_tr, dir_acc_te = _train_one(X_tr, yd_tr, X_te, yd_te, "Direction")
    _save_versioned(dir_model, LGBM_DIR_PATH, "direction",
                    dir_acc_tr, dir_acc_te, lookback_days, trigger, len(df))

    print("\nTraining complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train LightGBM models")
    parser.add_argument("--days", type=int, default=30,
                        help="Days of history to use (default: 30)")
    parser.add_argument("--trigger", type=str, default="manual",
                        help="Trigger reason (manual, weekly, drift, startup)")
    args = parser.parse_args()
    train(args.days, args.trigger)
