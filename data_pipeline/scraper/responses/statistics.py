"""
Completion summary display for the Commission responses scraper.
"""

import datetime
from typing import Dict, List

from .log_messages import LOG_MESSAGES
from ._logger import logger


def display_completion_summary(
    start_scraping: str,
    response_links: List[Dict[str, str]],
    failed_urls: List[str],
    downloaded_count: int,
    responses_dir: str,
) -> None:
    """Log a structured completion summary.

    Args:
        start_scraping: Timestamp string when scraping began.
        response_links: All response link dicts collected before download.
        failed_urls: List of URLs that could not be downloaded.
        downloaded_count: Number of successfully saved pages.
        responses_dir: Filesystem path where responses were saved.
    """
    total = len(response_links)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    logger.info(LOG_MESSAGES["divider_line"])
    logger.info(LOG_MESSAGES["scraping_complete"])
    logger.info(LOG_MESSAGES["divider_line"])
    logger.info(LOG_MESSAGES["completion_timestamp"], now)
    logger.info(LOG_MESSAGES["start_time"], start_scraping)
    logger.info(LOG_MESSAGES["total_links_found"], total)
    logger.info(LOG_MESSAGES["pages_downloaded"], downloaded_count, total)

    if failed_urls:
        logger.error(LOG_MESSAGES["failed_downloads"], len(failed_urls))
        for url in failed_urls:
            logger.error(LOG_MESSAGES["failed_url"], url)
    else:
        logger.info(LOG_MESSAGES["all_downloads_successful"])

    logger.info(LOG_MESSAGES["files_saved_in"], responses_dir)
    logger.info(LOG_MESSAGES["divider_line"])
