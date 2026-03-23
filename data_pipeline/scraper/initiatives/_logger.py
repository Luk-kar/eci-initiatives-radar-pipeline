"""
Logging configuration for the ECI scraper module.

This internal module sets up and provides a pre-configured logger instance
specifically tailored for tracking the execution flow, warnings, and errors
across the European Citizens' Initiative scraping pipeline.
"""

from data_pipeline.pipeline_shared.logger import get_logger
from data_pipeline.pipeline_shared.consts import LOG_SCRAPER_INITIATIVES_PATTERN
from .consts import LOG_DIR


logger = get_logger(LOG_DIR, LOG_SCRAPER_INITIATIVES_PATTERN)
