#!/usr/bin/env python
"""
Complete Setup & Training Pipeline
===================================
Orchestrates the entire process:
  1. Initialize all databases
  2. Backfill historical data (GDELT, market data, RSS)
  3. Build feature matrix
  4. Train ML models with improved hyperparameters
  5. Display training results and model quality metrics

Usage:
  python setup_and_train.py                    # Default: 60 days
  python setup_and_train.py --days 90          # Custom: 90 days
  python setup_and_train.py --skip-backfill    # Skip data fetch (use existing)
"""

import sys
import argparse
import time
from datetime import datetime

# Add backend to path
sys.path.insert(0, 'backend')

from ingestion.db import init_all
from prediction.features import build_feature_matrix, FEATURE_COLS
from prediction.train import train


def print_header(text: str):
    """Pretty-print section headers."""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Complete ML setup & training pipeline"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=60,
        help="Days of historical data to use for training (default: 60)"
    )
    parser.add_argument(
        "--skip-backfill",
        action="store_true",
        help="Skip data backfill and use existing data"
    )
    args = parser.parse_args()

    start_time = time.time()

    try:
        # Step 1: Initialize databases
        print_header("STEP 1: Initialize Databases")
        print(f"Creating database schema...")
        init_all()
        print("✓ Databases initialized\n")

        # Step 2: Backfill historical data
        if not args.skip_backfill:
            print_header("STEP 2: Backfill Historical Data")
            print(f"Fetching {args.days} days of historical data...")
            print("(This may take 2-5 minutes. Go grab some ☕)\n")

            try:
                # Import and run backfill for each data source
                print("📊 Fetching market data (Yahoo Finance)...")
                from ingestion.market_fetcher import backfill_market_data
                backfill_market_data(lookback_days=args.days)
                print("✓ Market data fetched\n")

                print("🌍 Fetching geopolitical events (GDELT)...")
                from ingestion.gdelt_fetcher import backfill_gdelt
                backfill_gdelt(lookback_days=args.days)
                print("✓ GDELT events fetched\n")

                print("📰 Fetching news headlines (RSS)...")
                from ingestion.rss_fetcher import backfill_rss
                backfill_rss(lookback_days=args.days)
                print("✓ RSS headlines fetched\n")

                print("🎯 Computing GTI scores...")
                from gti.aggregator import aggregate_gti
                aggregate_gti()
                print("✓ GTI scores computed\n")

            except Exception as e:
                print(f"⚠ Data backfill error (non-fatal): {e}")
                print("Attempting to continue with existing data...\n")
        else:
            print_header("STEP 2: Skipped (using existing data)")

        # Step 3: Build feature matrix
        print_header("STEP 3: Build Feature Matrix")
        print(f"Building feature matrix from {args.days} days of data...")
        df = build_feature_matrix(lookback_days=args.days)

        if df.empty:
            print("❌ ERROR: No data available for training!")
            print("Please ensure backfill completed successfully.")
            return 1

        print(f"✓ Built feature matrix: {len(df)} rows × {len(FEATURE_COLS)} features\n")
        print(f"Features used:")
        for i, col in enumerate(FEATURE_COLS, 1):
            print(f"  {i:2d}. {col}")
        print()

        # Step 4: Train models
        print_header("STEP 4: Train Improved ML Models")
        print(f"Training on {len(df)} samples with enhanced hyperparameters...\n")

        train(lookback_days=args.days, trigger="setup_pipeline")

        elapsed = time.time() - start_time
        print_header("✓ TRAINING COMPLETE")
        print(f"Total time: {elapsed:.1f} seconds\n")
        print("Models ready for inference! Next steps:")
        print("  1. Start the scheduler:  .\\start-scheduler.ps1")
        print("  2. Start the API:        .\\start-api.ps1")
        print("  3. Start frontend:       .\\start-frontend.ps1")
        print("  4. Open http://localhost:3000\n")

        return 0

    except Exception as e:
        print_header("❌ ERROR")
        print(f"Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
