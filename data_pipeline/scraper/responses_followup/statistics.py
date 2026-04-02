"""
Completion summary display for the Commission responses scraper.
"""

from typing import List, Dict

from ..scraper_shared.response_and_followup.statistics import (
    display_completion_summary as _display_completion_summary,
)
from .log_messages import LOG_MESSAGES
from ._logger import logger


def display_completion_summary(
    start_scraping: str,
    response_links: List[Dict[str, str]],
    failed_urls: List[str],
    downloaded_count: int,
    responses_dir: str,
) -> None:
    """Log a structured completion summary (delegates to shared implementation)."""
    _display_completion_summary(
        start_scraping,
        response_links,
        failed_urls,
        downloaded_count,
        responses_dir,
        log_messages=LOG_MESSAGES,
        logger=logger,
    )
