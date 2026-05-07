"""
Database backup and restore utilities.
Creates timestamped backups of all SQLite databases with retention policy.
"""

import os
import shutil
import glob
from datetime import datetime
from pathlib import Path

from config import GTI_DB, NEWS_DB, MARKET_DB, PREDICTIONS_DB
from logging_setup import get_logger

logger = get_logger("backup")


def backup_all_databases(backup_dir: str = "backups", keep_days: int = 7) -> str:
    """
    Create timestamped backups of all databases.

    Parameters
    ----------
    backup_dir : str
        Directory to store backups
    keep_days : int
        Number of days of backups to keep

    Returns
    -------
    str
        Path to backup directory created
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, timestamp)
    os.makedirs(backup_path, exist_ok=True)

    logger.info("Starting database backup | backup_dir=%s", backup_path)

    databases = {
        "news": NEWS_DB,
        "market": MARKET_DB,
        "gti": GTI_DB,
        "predictions": PREDICTIONS_DB,
    }

    backed_up = []
    for db_name, db_path in databases.items():
        if os.path.exists(db_path):
            backup_file = os.path.join(backup_path, f"{db_name}.db")
            try:
                shutil.copy2(db_path, backup_file)
                size_mb = os.path.getsize(backup_file) / (1024 * 1024)
                logger.info("Backed up %s | file=%s | size_mb=%.2f", db_name, backup_file, size_mb)
                backed_up.append(db_name)
            except Exception as e:
                logger.error("Backup failed for %s | error=%s", db_name, str(e))
        else:
            logger.warning("Database not found, skipping backup | db=%s | path=%s", db_name, db_path)

    logger.info("Backup complete | databases_backed_up=%s", ", ".join(backed_up))

    # Clean old backups
    _cleanup_old_backups(backup_dir, keep_days)

    return backup_path


def _cleanup_old_backups(backup_dir: str, keep_days: int):
    """Remove backups older than keep_days."""
    import time

    now = time.time()
    for backup_folder in glob.glob(os.path.join(backup_dir, "*")):
        if os.path.isdir(backup_folder):
            mtime = os.path.getmtime(backup_folder)
            age_days = (now - mtime) / (24 * 3600)

            if age_days > keep_days:
                try:
                    shutil.rmtree(backup_folder)
                    logger.info("Removed old backup | backup=%s | age_days=%.1f", backup_folder, age_days)
                except Exception as e:
                    logger.error("Failed to remove old backup | backup=%s | error=%s", backup_folder, str(e))


def restore_from_backup(backup_timestamp: str, backup_dir: str = "backups"):
    """
    Restore databases from a timestamped backup.

    Parameters
    ----------
    backup_timestamp : str
        Timestamp of backup to restore (e.g., "20260507_143022")
    backup_dir : str
        Backup directory

    Returns
    -------
    bool
        True if restore successful
    """
    backup_path = os.path.join(backup_dir, backup_timestamp)

    if not os.path.exists(backup_path):
        logger.error("Backup not found | backup=%s", backup_path)
        return False

    logger.info("Starting restore from backup | backup=%s", backup_path)

    databases = {
        "news": NEWS_DB,
        "market": MARKET_DB,
        "gti": GTI_DB,
        "predictions": PREDICTIONS_DB,
    }

    restored = []
    for db_name, db_path in databases.items():
        backup_file = os.path.join(backup_path, f"{db_name}.db")

        if os.path.exists(backup_file):
            try:
                # Create backup of current DB before overwriting
                if os.path.exists(db_path):
                    current_backup = f"{db_path}.backup"
                    shutil.copy2(db_path, current_backup)
                    logger.info("Created backup of current %s | backup=%s", db_name, current_backup)

                shutil.copy2(backup_file, db_path)
                logger.info("Restored %s from backup | file=%s", db_name, backup_file)
                restored.append(db_name)
            except Exception as e:
                logger.error("Restore failed for %s | error=%s", db_name, str(e))
        else:
            logger.warning("Backup file not found, skipping restore | db=%s | file=%s", db_name, backup_file)

    logger.info("Restore complete | databases_restored=%s", ", ".join(restored))
    return len(restored) == len(databases)


def list_available_backups(backup_dir: str = "backups") -> list[str]:
    """List available backups with timestamps."""
    if not os.path.exists(backup_dir):
        return []

    backups = sorted(
        [d for d in os.listdir(backup_dir) if os.path.isdir(os.path.join(backup_dir, d))]
    )
    return backups


if __name__ == "__main__":
    from logging_setup import setup_logging

    setup_logging()

    print("Available backups:")
    for backup in list_available_backups():
        print(f"  {backup}")

    backup_path = backup_all_databases()
    print(f"\nBackup created: {backup_path}")

    # List backups again
    print("\nAvailable backups after backup:")
    for backup in list_available_backups():
        print(f"  {backup}")
