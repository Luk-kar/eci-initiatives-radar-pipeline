"""
Fetcher for Commission response pages.
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
from ...file_operations.page import save_response_page
from ...log_messages import LOG_MESSAGES
from ..._logger import logger
from .waiter import wait_for_page_content


def download_all_responses(
    driver: webdriver.Chrome,
    responses_dir: str,
    response_links: list,
) -> Tuple[list, list]:
    """Download all Commission response pages using an existing driver."""
    return download_pages(
        driver=driver,
        output_dir=responses_dir,
        items=response_links,
        get_url=lambda link: link["url"],
        single_download_fn=_download_single,
        build_record=_build_record,
        wait_between=WAIT_BETWEEN_DOWNLOADS,
        log_messages=LOG_MESSAGES,
        logger=logger,
    )


def download_single_response(
    driver: webdriver.Chrome,
    responses_dir: str,
    url: str,
    year: str,
    reg_number: str,
    max_retries: int = DEFAULT_MAX_RETRIES,
) -> bool:
    """Download a single Commission response page with retry logic."""
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


# ── Private helpers ────────────────────────────────────────────────────────────


def _download_single(
    driver: webdriver.Chrome,
    responses_dir: str,
    link_data: dict,
) -> bool:
    return download_single_response(
        driver,
        responses_dir,
        link_data["url"],
        link_data["year"],
        link_data["reg_number"],
    )


def _build_record(link_data: dict, success: bool) -> dict:
    return {
        "url_find_initiative": link_data["url"],
        "registration_number": link_data["reg_number"],
        "title": link_data.get("title", ""),
        "datetime": (
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") if success else ""
        ),
    }


def _attempt_download(
    driver: webdriver.Chrome,
    responses_dir: str,
    url: str,
    year: str,
    reg_number: str,
) -> str:
    """Single download attempt. Returns saved filename on success."""
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
