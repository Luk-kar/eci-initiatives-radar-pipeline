"""
Orchestration module for fetching Commission response pages.

Mirrors the structure of scraper/initiatives/fetchers/ecis/fetcher.py:
functional helpers, shared retry/debug utilities, module-level logger.
"""

# Python Standard Library
import datetime
import random
import time
from typing import Tuple

# Third-party
from selenium import webdriver

# Shared
from ....scraper_shared.fetch_utils import (
    check_rate_limiting,
    download_with_retry,
    save_debug_page,
)

# Local
from ...consts import (
    WAIT_DYNAMIC_CONTENT,
    WAIT_BETWEEN_DOWNLOADS,
    RETRY_WAIT_BASE,
    DEFAULT_MAX_RETRIES,
)
from ...log_messages import LOG_MESSAGES
from ...file_operations.page import save_response_page
from ..._logger import logger
from .waiter import wait_for_page_content


def download_all_responses(
    driver: webdriver.Chrome,
    responses_dir: str,
    response_links: list,
) -> Tuple[list, list]:
    """Download all Commission response pages using an existing driver.

    Args:
        driver: Existing Chrome WebDriver instance.
        responses_dir: Base directory for saving HTML files.
        response_links: List of dicts with 'url', 'year', 'reg_number', 'title'.

    Returns:
        Tuple of (updated_data, failed_urls).
    """
    updated_data: list = []
    failed_urls: list = []

    for i, link_data in enumerate(response_links):
        url = link_data["url"]
        year = link_data["year"]
        reg_number = link_data["reg_number"]

        logger.info(
            LOG_MESSAGES["processing_item"].format(
                index=i + 1, total=len(response_links), url=url
            )
        )

        success = download_single_response(driver, responses_dir, url, year, reg_number)

        updated_data.append(
            {
                "url_find_initiative": url,
                "registration_number": reg_number,
                "title": link_data.get("title", ""),
                "datetime": (
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    if success
                    else ""
                ),
            }
        )

        if not success:
            failed_urls.append(url)

        wait_time = random.uniform(*WAIT_BETWEEN_DOWNLOADS)
        logger.info(LOG_MESSAGES["awaiting_next_page"].format(wait_time=wait_time))
        time.sleep(wait_time)

    logger.info(LOG_MESSAGES["download_complete"].format(failed_count=len(failed_urls)))
    return updated_data, failed_urls


def download_single_response(
    driver: webdriver.Chrome,
    responses_dir: str,
    url: str,
    year: str,
    reg_number: str,
    max_retries: int = DEFAULT_MAX_RETRIES,
) -> bool:
    """Download a single Commission response page with retry logic.

    Returns:
        bool: True if successful, False if all retries exhausted.
    """
    return download_with_retry(
        attempt_fn=lambda: _attempt_download(
            driver, responses_dir, url, year, reg_number
        ),
        debug_fn=lambda: save_debug_page(
            driver,
            url,
            save_fn=lambda src: save_response_page(
                responses_dir, year, reg_number, src, debug=True
            ),
            logger=logger,
        ),
        url=url,
        max_retries=max_retries,
        retry_wait_base=random.uniform(*RETRY_WAIT_BASE),
        logger=logger,
    )


def _attempt_download(
    driver: webdriver.Chrome,
    responses_dir: str,
    url: str,
    year: str,
    reg_number: str,
) -> str:
    """Single download attempt. Returns the saved filename on success.

    Raises:
        Exception: On rate limiting or any page/save failure.
    """
    logger.info(LOG_MESSAGES["downloading_html"])
    driver.get(url)

    time.sleep(random.uniform(*WAIT_DYNAMIC_CONTENT))
    check_rate_limiting(driver)
    content_found = wait_for_page_content(driver)

    filename = save_response_page(
        responses_dir, year, reg_number, driver.page_source, debug=not content_found
    )
    logger.info(LOG_MESSAGES["download_success"].format(filename=filename))
    return filename
