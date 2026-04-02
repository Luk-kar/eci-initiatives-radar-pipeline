"""Shared completion-summary display for Commission response scrapers."""

import datetime
import logging
from typing import Dict, List


def display_completion_summary(
    start_scraping: str,
    response_links: List[Dict[str, str]],
    failed_urls: List[str],
    downloaded_count: int,
    responses_dir: str,
    *,
    log_messages: dict,
    logger: logging.Logger,
) -> None:
    """Log a structured completion summary.

    Required ``log_messages`` keys:
        ``divider_line``, ``scraping_complete``, ``completion_timestamp``,
        ``start_time``, ``total_links_found``, ``pages_downloaded``,
        ``failed_downloads``, ``failed_url``, ``all_downloads_successful``,
        ``files_saved_in``.
    """
    total = len(response_links)

    logger.info(log_messages["divider_line"])
    logger.info(log_messages["scraping_complete"])
    logger.info(log_messages["divider_line"])
    logger.info(
        log_messages["completion_timestamp"].format(
            timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )
    logger.info(log_messages["start_time"].format(start_scraping=start_scraping))
    logger.info(log_messages["total_links_found"].format(count=total))
    logger.info(
        log_messages["pages_downloaded"].format(
            downloaded_count=downloaded_count, total_count=total
        )
    )

    if failed_urls:
        logger.error(
            log_messages["failed_downloads"].format(failed_count=len(failed_urls))
        )
        for url in failed_urls:
            logger.error(log_messages["failed_url"].format(failed_url=url))
    else:
        logger.info(log_messages["all_downloads_successful"])

    logger.info(log_messages["files_saved_in"].format(path=responses_dir))
    logger.info(log_messages["divider_line"])
