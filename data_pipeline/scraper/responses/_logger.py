"""
Module-level logger for the Commission responses scraper.

No file handler is attached here — handlers are added at runtime
by __main__._setup_file_logging() after the timestamp directory
is located.
"""

import logging

logger = logging.getLogger("ECIResponsesScraper")
logger.setLevel(logging.DEBUG)
