"""
Main orchestration module for fetching ECI listing pages.

This module coordinates the high-level scraping workflow for the European
Citizens' Initiative (ECI) listing pages. It manages the pagination loop, handles
browser interactions, saves the raw HTML content, and extracts initiative data
to feed into the downstream data pipeline.
"""

# Python Standard Library
import os
import random
from typing import Tuple

# Third-party
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

# Shared
from data_pipeline.pipeline_shared.consts import FILE_ENCODING

from ....scraper_shared.fetch_utils import (
    check_rate_limiting,
    download_with_retry,
    save_debug_page,
)

# Local
from ...file_operations import save_listing_page
from ...html_parser import parse_initiatives_list_data
from ...css_selectors import ECIlistingSelectors
from ...consts import (
    ROUTE_FIND_INITIATIVE,
    WEBDRIVER_TIMEOUT_DEFAULT,
    DEFAULT_MAX_RETRIES,
    RETRY_WAIT_BASE,
    LISTING_PAGE_MAIN_FILENAME,
)
from ...log_messages import LOG_MESSAGES
from ..._logger import logger
from .page_ops import (
    navigate_to_next_page,
    wait_for_listing_page_content,
    load_listing_url,
    save_debug_listing_page,
)


def scrape_all_listings(
    driver: webdriver.Chrome, base_url: str, list_dir: str
) -> Tuple[list, list]:
    """Scrape all pages of initiatives by iterating through pagination.

    Args:
        driver: Chrome WebDriver instance
        base_url: Base URL of the site
        list_dir: Directory to save page HTML files

    Returns:
        Tuple containing:
        - List of all initiative data from all pages
        - List of paths to saved HTML files
    """

    url = base_url + ROUTE_FIND_INITIATIVE
    logger.info(LOG_MESSAGES["pagination_start"].format(url=url))

    if not _fetch_first_listing_page(driver, url, list_dir):
        logger.error(LOG_MESSAGES["first_page_failed"])
        return [], []

    return _paginate_and_scrape(driver, base_url, list_dir, url)


def _fetch_first_listing_page(
    driver: webdriver.Chrome,
    url: str,
    list_dir: str,
) -> bool:
    """Load the first listing page with retry logic.

    Returns:
        bool: True if the page loaded successfully, False otherwise.
    """

    return download_with_retry(
        attempt_fn=lambda: load_listing_url(driver, url),
        debug_fn=lambda: save_debug_page(
            driver,
            url,
            save_fn=lambda src: save_debug_listing_page(list_dir, 1, src),
            logger=logger,
        ),
        url=url,
        max_retries=DEFAULT_MAX_RETRIES,
        retry_wait_base=random.uniform(*RETRY_WAIT_BASE),
        logger=logger,
    )


def _paginate_and_scrape(
    driver: webdriver.Chrome,
    base_url: str,
    list_dir: str,
    url: str,
) -> Tuple[list, list]:
    """Iterate through all listing pages and collect initiative data.

    Returns:
        Tuple of (all_initiative_data, saved_page_paths).
    """

    all_initiative_data: list = []
    saved_page_paths: list = []
    current_page = 1

    while True:
        page_data, page_path = scrape_single_listing_page(
            driver, base_url, list_dir, current_page, url
        )
        all_initiative_data.extend(page_data)
        saved_page_paths.append(page_path)

        if navigate_to_next_page(driver, current_page):
            current_page += 1
        else:
            break

    logger.info(
        LOG_MESSAGES["pagination_complete"].format(
            page_count=current_page, total_initiatives=len(all_initiative_data)
        )
    )
    return all_initiative_data, saved_page_paths


def scrape_single_listing_page(
    driver: webdriver.Chrome,
    base_url: str,
    list_dir: str,
    current_page: int,
    url: str,
) -> Tuple[list, str]:
    """Scrape a single listing page with retry logic.

    NOTE: For pages 2+ (reached via JS pagination), retry re-checks the
    already-loaded page after back-off — it cannot re-navigate to that
    specific page number. Retry is still useful for transient rate limits
    that clear within the back-off window.
    """

    result: dict = {}

    def _fetch_parse_listing() -> None:
        check_rate_limiting(driver)
        wait_for_listing_page_content(driver, current_page)
        page_source, page_path = save_listing_page(driver, list_dir, current_page)
        result["data"] = parse_initiatives_list_data(page_source, base_url)
        result["path"] = page_path

    success = download_with_retry(
        attempt_fn=_fetch_parse_listing,
        debug_fn=lambda: save_debug_page(
            driver,
            url,
            save_fn=lambda src: save_debug_listing_page(list_dir, current_page, src),
            logger=logger,
        ),
        url=url,
        max_retries=DEFAULT_MAX_RETRIES,
        retry_wait_base=random.uniform(*RETRY_WAIT_BASE),
        logger=logger,
    )

    if not success:
        logger.error(LOG_MESSAGES["listing_page_failed"].format(page=current_page))
        return [], ""

    return result["data"], result["path"]


def save_main_listing_page(
    driver: webdriver.Chrome, base_url: str, list_dir: str
) -> Tuple[str, str]:
    """Load the main listing page, wait for elements, and save HTML source."""

    url = base_url + ROUTE_FIND_INITIATIVE
    result: dict = {}

    def _fetch_save_main() -> None:
        load_listing_url(driver, url)
        wait = WebDriverWait(driver, WEBDRIVER_TIMEOUT_DEFAULT)

        try:
            wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ECIlistingSelectors.INITIATIVE_CARDS)
                )
            )
            wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ECIlistingSelectors.PAGINATION_LINKS)
                )
            )
            logger.info(LOG_MESSAGES["listings_loaded"])

        except TimeoutException as e:
            check_rate_limiting(driver)
            logger.warning(LOG_MESSAGES["listing_timeout"].format(error=e))

        page_source = driver.page_source
        main_page_path = os.path.join(list_dir, LISTING_PAGE_MAIN_FILENAME)

        with open(main_page_path, "w", encoding=FILE_ENCODING) as f:
            f.write(BeautifulSoup(page_source, "html.parser").prettify())

        logger.info(LOG_MESSAGES["main_page_saved"].format(path=main_page_path))
        result["source"] = page_source
        result["path"] = main_page_path

    success = download_with_retry(
        attempt_fn=_fetch_save_main,
        debug_fn=lambda: save_debug_page(
            driver,
            url,
            save_fn=lambda src: save_debug_listing_page(list_dir, 0, src),
            logger=logger,
        ),
        url=url,
        max_retries=DEFAULT_MAX_RETRIES,
        retry_wait_base=random.uniform(*RETRY_WAIT_BASE),
        logger=logger,
    )

    if not success:
        logger.error(LOG_MESSAGES["main_page_failed"])
        return "", ""

    return result["source"], result["path"]
