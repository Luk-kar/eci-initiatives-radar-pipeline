"""
Main orchestration module for fetching individual ECI detail pages.

This module coordinates the scraping workflow for specific European
Citizens' Initiative (ECI) records. It navigates to provided URLs,
handles browser interactions and dynamic waits, and saves the fully
rendered HTML pages for downstream data extraction.
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
from ...file_operations import save_initiative_page
from ..._logger import logger
from .waiter import wait_for_page_content


def download_all_initiatives(
    driver: webdriver.Chrome,
    pages_dir: str,
    initiative_data: list,
) -> Tuple[list, list]:
    """Download individual initiative pages using Selenium, reusing an existing driver.

    Args:
        driver: Existing Chrome WebDriver instance
        pages_dir: Directory path for saving HTML pages
        initiative_data: List of initiative dictionaries

    Returns:
        Tuple containing updated data list and list of failed URLs
    """
    updated_data: list = []
    failed_urls: list = []

    for i, row in enumerate(initiative_data):
        url = row["url"]
        logger.info(
            LOG_MESSAGES["processing_initiative"].format(
                index=i + 1, total=len(initiative_data), url=url
            )
        )

        success = download_single_initiative(driver, pages_dir, url)

        if success:
            row["datetime"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            failed_urls.append(url)

        updated_data.append(row)

        wait_time = random.uniform(*WAIT_BETWEEN_DOWNLOADS)
        logger.info(LOG_MESSAGES["awaiting_next_page"].format(wait_time=wait_time))
        time.sleep(wait_time)

    logger.info(LOG_MESSAGES["download_complete"].format(failed_count=len(failed_urls)))
    return updated_data, failed_urls


def download_single_initiative(
    driver: webdriver.Chrome,
    pages_dir: str,
    url: str,
    max_retries: int = DEFAULT_MAX_RETRIES,
) -> bool:
    """Download a single initiative page with retry logic.

    Returns:
        bool: True if successful, False if all retries exhausted.
    """
    return download_with_retry(
        attempt_fn=lambda: _attempt_download(driver, pages_dir, url),
        debug_fn=lambda: save_debug_page(
            driver,
            url,
            save_fn=lambda src: save_initiative_page(pages_dir, url, src, debug=True),
            logger=logger,
        ),
        url=url,
        max_retries=max_retries,
        retry_wait_base=random.uniform(*RETRY_WAIT_BASE),
        logger=logger,
    )


def _attempt_download(
    driver: webdriver.Chrome,
    pages_dir: str,
    url: str,
) -> str:
    """Perform a single download attempt. Returns the saved filename.

    Raises:
        Exception: On rate limiting or any page/save failure.
    """
    logger.info(LOG_MESSAGES["downloading_html"])
    driver.get(url)

    time.sleep(random.uniform(*WAIT_DYNAMIC_CONTENT))
    check_rate_limiting(driver)
    content_found = wait_for_page_content(driver)

    file_name = save_initiative_page(
        pages_dir, url, driver.page_source, debug=not content_found
    )
    logger.info(LOG_MESSAGES["download_success"].format(filename=file_name))
    return file_name
