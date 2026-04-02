"""
Module-level logger for the Commission responses scraper.

No file handler is attached here — handlers are added at runtime
by __main__._setup_file_logging() after the timestamp directory
is located.
"""

from data_pipeline.pipeline_shared.consts import LOG_SCRAPER_RESPONSES_FOLLOWUP_PATTERN
from data_pipeline.pipeline_shared.logger import set_logger_and_its_level

logger = set_logger_and_its_level(LOG_SCRAPER_RESPONSES_FOLLOWUP_PATTERN)
