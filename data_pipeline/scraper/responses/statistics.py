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

    logger.info(LOG_MESSAGES["divider_line"])
    logger.info(LOG_MESSAGES["scraping_complete"])
    logger.info(LOG_MESSAGES["divider_line"])
    logger.info(
        LOG_MESSAGES["completion_timestamp"].format(
            timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )
    logger.info(LOG_MESSAGES["start_time"].format(start_scraping=start_scraping))
    logger.info(LOG_MESSAGES["total_links_found"].format(count=total))
    logger.info(
        LOG_MESSAGES["pages_downloaded"].format(
            downloaded_count=downloaded_count, total_count=total
        )
    )

    if failed_urls:
        logger.error(
            LOG_MESSAGES["failed_downloads"].format(failed_count=len(failed_urls))
        )
        for url in failed_urls:
            logger.error(LOG_MESSAGES["failed_url"].format(failed_url=url))
    else:
        logger.info(LOG_MESSAGES["all_downloads_successful"])

    logger.info(LOG_MESSAGES["files_saved_in"].format(path=responses_dir))
    logger.info(LOG_MESSAGES["divider_line"])
