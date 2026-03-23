"""
Shared logger factory for data pipeline modules.
"""

import logging
from datetime import datetime
from pathlib import Path

from .consts import TIMESTAMP_FORMAT


def get_logger(log_dir: Path, log_filename_pattern: str) -> logging.Logger:
    """Create or retrieve a configured logger with file and console handlers.

    The logger name is derived from *log_filename_pattern* by stripping the
    ``_{timestamp}.log`` suffix, e.g. ``scraper_initiatives_{timestamp}.log``
    becomes ``scraper_initiatives``.  This keeps ``logging.getLogger`` idempotent:
    calling ``get_logger`` twice with the same pattern returns the same instance
    without adding duplicate handlers.

    Args:
        log_dir: Directory where the log file will be written.  Created
            automatically if it does not exist.
        log_filename_pattern: Filename template containing a ``{timestamp}``
            placeholder, e.g. ``LOG_SCRAPER_INITIATIVES_PATTERN``.

    Returns:
        Configured ``logging.Logger`` instance.
    """

    logger = set_logger_and_its_level(log_filename_pattern)

    if logger.handlers:
        return logger

    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
    log_file = log_dir / log_filename_pattern.format(timestamp=timestamp)

    # File handler (detailed)
    file_handler = set_file_handler(log_file)

    # Console handler (simpler)
    console_handler = set_console_handler()

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def set_logger_and_its_level(log_filename_pattern: str) -> logging.Logger:
    """Instantiate a named logger and set its level to DEBUG."""

    logger_name = log_filename_pattern.replace("_{timestamp}.log", "")
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    return logger


def set_file_handler(log_file: Path) -> logging.FileHandler:
    """Create a DEBUG-level file handler with a detailed formatter."""

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - "
            "%(funcName)s:%(lineno)d - %(message)s"
        )
    )
    return file_handler


def set_console_handler() -> logging.StreamHandler:
    """Create an INFO-level console handler with a simple formatter."""

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    return console_handler
