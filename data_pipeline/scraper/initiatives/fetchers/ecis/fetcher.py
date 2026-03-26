"""
Fetcher for individual ECI detail pages.
"""

import datetime
import time
import random
from typing import Tuple

from selenium import webdriver

from ....scraper_shared.fetch_utils import (
    check_rate_limiting,
    download_pages,
    download_with_retry,
    save_debug_page,
)
from ...consts import (
    DEFAULT_MAX_RETRIES,
    RETRY_WAIT_BASE,
    WAIT_BETWEEN_DOWNLOADS,
    WAIT_DYNAMIC_CONTENT,
)
from ...file_operations import save_initiative_page
from ...log_messages import LOG_MESSAGES
from ..._logger import logger
from .waiter import wait_for_page_content


def download_all_initiatives(
    driver: webdriver.Chrome,
    pages_dir: str,
    initiative_data: list,
) -> Tuple[list, list]:
    """Download individual initiative pages using an existing driver."""
    return download_pages(
        driver=driver,
        output_dir=pages_dir,
        items=initiative_data,
        get_url=lambda row: row["url"],
        single_download_fn=_download_single,
        build_record=_build_record,
        wait_between=WAIT_BETWEEN_DOWNLOADS,
        log_messages=LOG_MESSAGES,
        logger=logger,
    )


def download_single_initiative(
    driver: webdriver.Chrome,
    pages_dir: str,
    url: str,
    max_retries: int = DEFAULT_MAX_RETRIES,
) -> bool:
    """Download a single initiative page with retry logic."""
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


# ── Private helpers ────────────────────────────────────────────────────────────


def _download_single(
    driver: webdriver.Chrome,
    pages_dir: str,
    row: dict,
) -> bool:
    return download_single_initiative(driver, pages_dir, row["url"])


def _build_record(row: dict, success: bool) -> dict:
    if success:
        row["datetime"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return row


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
