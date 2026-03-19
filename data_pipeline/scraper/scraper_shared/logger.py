"""
Shared logger factory for scraper modules.
"""

import datetime
import logging
import os
from typing import Optional

from .const import LOG_DIR_NAME, DATA_DIR_NAME, SCRIPT_DIR


def get_logger(name: str, log_dir: Optional[str] = None) -> logging.Logger:
    """Create or retrieve a configured logger with file and console handlers.

    This function replaces the ScraperLogger singleton. It relies on
    logging.getLogger(name) to ensure a single logger instance per name.

    Args:
        name: Logger name (e.g. "ECIScraper", "ECIResponsesScraper").
        log_dir: Directory where log files should be written. If not provided,
            logs will be written under SCRIPT_DIR/data/<timestamp>/logs/ and
            must be fully specified by the caller.

    Returns:
        Configured logging.Logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    if log_dir is None:
        # Fallback: create a timestamped log directory under shared data dir.
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_dir = os.path.join(SCRIPT_DIR, DATA_DIR_NAME, timestamp, LOG_DIR_NAME)

    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(log_dir, f"{name}_{timestamp}.log")

    # File handler (detailed)
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - "
        "%(funcName)s:%(lineno)d - %(message)s"
    )
    file_handler.setFormatter(file_formatter)

    # Console handler (simpler)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
