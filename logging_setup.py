"""
Production-grade logging configuration for the trading bot.
Supports file rotation, console output, structured logging.
"""

import logging
import logging.handlers
import os
from datetime import datetime


def setup_logging(
    level: int = logging.INFO,
    log_dir: str = "logs",
    max_bytes: int = 10485760,  # 10MB
    backup_count: int = 7,
) -> logging.Logger:
    """
    Configure centralized logging with file rotation and console output.

    Parameters
    ----------
    level : int
        Logging level (logging.DEBUG, INFO, WARNING, ERROR, CRITICAL)
    log_dir : str
        Directory for log files
    max_bytes : int
        Max log file size before rotation
    backup_count : int
        Number of backup log files to keep

    Returns
    -------
    logging.Logger
        Configured logger instance
    """
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger("trading_bot")
    logger.setLevel(level)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # File handler with rotation
    log_file = os.path.join(log_dir, "trading_bot.log")
    fh = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
    )
    fh.setLevel(level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.info("Logging initialized | level=%s | file=%s", logging.getLevelName(level), log_file)

    return logger


def get_logger(name: str) -> logging.Logger:
    """Get logger for a specific module."""
    return logging.getLogger(f"trading_bot.{name}")


if __name__ == "__main__":
    logger = setup_logging(logging.DEBUG)

    logger.debug("This is a DEBUG message")
    logger.info("This is an INFO message")
    logger.warning("This is a WARNING message")
    logger.error("This is an ERROR message")

    print("\nLog file created: logs/trading_bot.log")
