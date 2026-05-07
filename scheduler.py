"""
Scheduler
=========
Orchestrates all background data collection and prediction jobs using APScheduler.
Keep this terminal running while the system is live.

Job schedule:
  Every 5 min   — RSS fetcher     (Reuters, BBC, AJ, AP headlines)
  Every 15 min  — GDELT fetcher   (geopolitical event data)
  Every 15 min  — NewsAPI fetcher (English headlines, 100/day limit enforced)
  Every 15 min  — Market fetcher  (SPY, VIX, GLD hourly OHLCV)
  Every 15 min  — GTI aggregator  (runs 2 min after ingestion)
  Every 15 min  — Predictor       (runs 3 min after GTI)

On startup, all jobs run once immediately so the dashboard has data right away.

Usage:
  python scheduler.py
  Ctrl+C to stop
"""

import logging
import sys
import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

from config import GDELT_POLL_MINS, RSS_POLL_MINS, NEWSAPI_POLL_MINS, MARKET_POLL_MINS, NEWSAPI_KEY

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  [%(levelname)s]  %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger("scheduler")


# ── Job wrappers — each catches exceptions so one failure won't stop others ──

def job_rss():
    try:
        from ingestion.rss_fetcher import fetch_all
        fetch_all()
    except Exception as e:
        log.error(f"RSS job failed: {e}")


def job_gdelt():
    try:
        from ingestion.gdelt_fetcher import fetch_latest
        fetch_latest()
    except Exception as e:
        log.error(f"GDELT job failed: {e}")


def job_newsapi():
    try:
        from ingestion.newsapi_fetcher import fetch_headlines
        fetch_headlines()
    except Exception as e:
        log.error(f"NewsAPI job failed: {e}")


def job_market():
    try:
        from ingestion.market_fetcher import fetch_latest as fetch_mkt
        fetch_mkt()
    except Exception as e:
        log.error(f"Market job failed: {e}")


def job_gti():
    try:
        from gti.aggregator import run
        run()
    except Exception as e:
        log.error(f"GTI job failed: {e}")


def job_predict():
    try:
        from prediction.predict import run_inference
        run_inference()
    except Exception as e:
        log.error(f"Prediction job failed: {e}")


def job_train(trigger: str = "manual"):
    try:
        import subprocess
        log.info(f"Starting model retraining (trigger: {trigger})...")
        subprocess.run([sys.executable, "prediction/train.py", "--trigger", trigger], check=True)
        log.info("Model retraining complete.")
    except Exception as e:
        log.error(f"Training job failed: {e}")


def job_resolve_outcomes():
    try:
        from prediction.drift import resolve_outcomes
        n = resolve_outcomes(lookback_hours=1)
        if n > 0:
            log.info(f"Resolved {n} prediction outcomes")
    except Exception as e:
        log.error(f"Outcome resolution job failed: {e}")


def job_drift_check():
    try:
        from prediction.drift import DriftDetector
        import os
        from config import LGBM_VOL_PATH, LGBM_DIR_PATH
        from ingestion.db import get_conn
        from config import PREDICTIONS_DB
        import json

        if not os.path.exists(LGBM_VOL_PATH) or not os.path.exists(LGBM_DIR_PATH):
            log.info("Models don't exist yet, skipping drift check")
            return

        detector = DriftDetector()

        # Get last training time from model registry
        registry_path = os.path.join(os.path.dirname(LGBM_VOL_PATH), "model_registry.json")
        last_trained_at = None
        if os.path.exists(registry_path):
            with open(registry_path, "r") as f:
                registry = json.load(f)
                if registry.get("direction") and len(registry["direction"]) > 0:
                    trained_at_str = registry["direction"][0]["trained_at"]
                    last_trained_at = datetime.datetime.fromisoformat(trained_at_str.replace("Z", "+00:00"))

        should_retrain, reason = detector.should_retrain(last_trained_at)

        if should_retrain:
            log.warning(f"Drift detected: {reason} — triggering retraining")
            job_train(trigger="drift")
        else:
            log.debug(f"Drift check passed: {reason}")

    except Exception as e:
        log.error(f"Drift check job failed: {e}")


def job_initial_backfill_and_train():
    """Run once on startup if models don't exist — backfill + initial training."""
    import os
    from config import LGBM_VOL_PATH, LGBM_DIR_PATH

    if os.path.exists(LGBM_VOL_PATH) and os.path.exists(LGBM_DIR_PATH):
        log.info("Models exist, skipping initial backfill+train")
        return

    log.info("=" * 55)
    log.info("  No trained models found — starting backfill...")
    log.info("=" * 55)

    try:
        from ingestion.gdelt_fetcher import fetch_latest as fetch_gdelt
        from ingestion.market_fetcher import fetch_latest as fetch_mkt

        # Backfill GDELT
        log.info("Backfilling GDELT (30 days)...")
        import subprocess
        subprocess.run([sys.executable, "ingestion/gdelt_fetcher.py", "--backfill", "--days", "30"], check=True)

        # Backfill market (fetches SPY, VIX, GLD)
        log.info("Backfilling market data (30 days)...")
        subprocess.run([sys.executable, "ingestion/market_fetcher.py", "--backfill", "--days", "30"], check=True)

        # Train models
        log.info("Training models...")
        job_train(trigger="startup")

        log.info("=" * 55)
        log.info("  Initial setup complete. Models are ready.")
        log.info("=" * 55)
    except Exception as e:
        log.error(f"Initial backfill+train failed: {e}")


def main():
    scheduler = BlockingScheduler(timezone="UTC")

    # Ingestion jobs
    scheduler.add_job(
        job_rss, IntervalTrigger(minutes=RSS_POLL_MINS), id="rss",
        name="RSS Fetcher", misfire_grace_time=60,
    )
    scheduler.add_job(
        job_gdelt, IntervalTrigger(minutes=GDELT_POLL_MINS), id="gdelt",
        name="GDELT Fetcher", misfire_grace_time=60,
    )
    if NEWSAPI_KEY:
        scheduler.add_job(
            job_newsapi, IntervalTrigger(minutes=NEWSAPI_POLL_MINS), id="newsapi",
            name="NewsAPI Fetcher", misfire_grace_time=60,
        )
    else:
        log.warning("NEWSAPI_KEY not set — NewsAPI job disabled")
    scheduler.add_job(
        job_market, IntervalTrigger(minutes=MARKET_POLL_MINS), id="market",
        name="Market Fetcher", misfire_grace_time=60,
    )

    # GTI runs 2 min after the ingestion wave (start_date offset trick)
    gti_start    = datetime.datetime.utcnow() + datetime.timedelta(minutes=2)
    predict_start = datetime.datetime.utcnow() + datetime.timedelta(minutes=3)

    scheduler.add_job(
        job_gti, IntervalTrigger(minutes=GDELT_POLL_MINS, start_date=gti_start),
        id="gti", name="GTI Aggregator", misfire_grace_time=60,
    )
    scheduler.add_job(
        job_predict, IntervalTrigger(minutes=GDELT_POLL_MINS, start_date=predict_start),
        id="predict", name="Predictor", misfire_grace_time=60,
    )

    # Outcome resolution (runs every 15 min)
    scheduler.add_job(
        job_resolve_outcomes, IntervalTrigger(minutes=GDELT_POLL_MINS),
        id="resolve_outcomes", name="Outcome Resolution", misfire_grace_time=60,
    )

    # Drift detection (runs every 4 hours)
    scheduler.add_job(
        job_drift_check, IntervalTrigger(hours=4),
        id="drift_check", name="Drift Detection", misfire_grace_time=300,
    )

    # Weekly model retraining
    scheduler.add_job(
        job_train, IntervalTrigger(days=7), id="train", name="Model Retraining", misfire_grace_time=3600
    )

    log.info("=" * 55)
    log.info("  Geo-Market Scheduler started")
    log.info(f"  RSS:     every {RSS_POLL_MINS} min")
    log.info(f"  GDELT:   every {GDELT_POLL_MINS} min")
    log.info(f"  NewsAPI: every {NEWSAPI_POLL_MINS} min")
    log.info(f"  Market:  every {MARKET_POLL_MINS} min")
    log.info(f"  GTI:     every {GDELT_POLL_MINS} min (+2 min offset)")
    log.info(f"  Predict: every {GDELT_POLL_MINS} min (+3 min offset)")
    log.info("  Press Ctrl+C to stop")
    log.info("=" * 55)

    # Run everything once immediately so dashboard has data on first open
    # Check if models exist; if not, backfill and train
    job_initial_backfill_and_train()

    log.info("Running all jobs once on startup...")
    startup_jobs = [
        ("RSS",    job_rss),
        ("GDELT",  job_gdelt),
        ("Market", job_market),
        ("GTI",    job_gti),
        ("Predict", job_predict),
    ]
    if NEWSAPI_KEY:
        startup_jobs.insert(2, ("NewsAPI", job_newsapi))
    for name, fn in startup_jobs:
        log.info(f"  → {name}")
        fn()

    log.info("Startup complete. Entering scheduled loop.")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        log.info("Scheduler stopped.")


if __name__ == "__main__":
    main()
