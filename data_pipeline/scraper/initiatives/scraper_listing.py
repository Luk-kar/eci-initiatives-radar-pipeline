# Python Standard Library
import os
import random
import time
from typing import Tuple

# Third-party
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Shared
from ..scraper_shared.fetch_utils import (
    check_rate_limiting,
    download_with_retry,
    save_debug_page,
)

# Local
from .file_ops import save_listing_page
from .data_parser import parse_initiatives_list_data
from .css_selectors import ECIlistingSelectors
from .consts import (
    ROUTE_FIND_INITIATIVE,
    WAIT_DYNAMIC_CONTENT,
    WAIT_BETWEEN_PAGES,
    WEBDRIVER_TIMEOUT_DEFAULT,
    DEFAULT_MAX_RETRIES,
    RETRY_WAIT_BASE,
    LISTING_PAGE_MAIN_FILENAME,
    LOG_MESSAGES,
)
from ._logger import logger


def scrape_all_initiatives_on_all_pages(
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
    logger.info(f"Starting pagination scraping from: {url}")

    if not _load_first_listing_page(driver, url, list_dir):
        logger.error("❌ Failed to load first listing page. Aborting pagination.")
        return [], []

    return _scrape_paginated_listings(driver, base_url, list_dir, url)


def _load_first_listing_page(
    driver: webdriver.Chrome,
    url: str,
    list_dir: str,
) -> bool:
    """Load the first listing page with retry logic.

    Returns:
        bool: True if the page loaded successfully, False otherwise.
    """
    return download_with_retry(
        attempt_fn=lambda: _load_listing_url(driver, url),
        debug_fn=lambda: save_debug_page(
            driver,
            url,
            save_fn=lambda src: _save_debug_listing_page(list_dir, 1, src),
            logger=logger,
        ),
        url=url,
        max_retries=DEFAULT_MAX_RETRIES,
        retry_wait_base=random.uniform(*RETRY_WAIT_BASE),
        logger=logger,
    )


def _scrape_paginated_listings(
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
        f"Completed scraping {current_page} pages with "
        f"{len(all_initiative_data)} total initiatives"
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

    def _attempt() -> None:

        check_rate_limiting(driver)
        wait_for_listing_page_content(driver, current_page)

        page_source, page_path = save_listing_page(driver, list_dir, current_page)

        result["data"] = parse_initiatives_list_data(page_source, base_url)
        result["path"] = page_path

    success = download_with_retry(
        attempt_fn=_attempt,
        debug_fn=lambda: save_debug_page(
            driver,
            url,
            save_fn=lambda src: _save_debug_listing_page(list_dir, current_page, src),
            logger=logger,
        ),
        url=url,
        max_retries=DEFAULT_MAX_RETRIES,
        retry_wait_base=random.uniform(*RETRY_WAIT_BASE),
        logger=logger,
    )

    if not success:
        logger.error(f"❌ Failed to scrape listing page {current_page}")
        return [], ""

    return result["data"], result["path"]


def _load_listing_url(driver: webdriver.Chrome, url: str) -> None:
    """Load the listing URL and check for rate limiting.

    Raises:
        Exception: If the loaded page shows rate limiting indicators.
    """

    logger.info(f"Loading page: {url}")

    driver.get(url)

    time.sleep(random.uniform(*WAIT_DYNAMIC_CONTENT))
    check_rate_limiting(driver)


def _save_debug_listing_page(list_dir: str, current_page: int, page_source: str) -> str:
    """Save a listing page to the debugging subdirectory."""

    from ..scraper_shared.const import DEBUGGING_DIR_NAME
    from ..scraper_shared.fs_utils import ensure_dirs

    debug_dir = os.path.join(
        os.path.dirname(list_dir), DEBUGGING_DIR_NAME, os.path.basename(list_dir)
    )
    ensure_dirs(debug_dir)

    file_name = LISTING_PAGE_FILENAME_PATTERN.format(current_page)
    file_path = os.path.join(debug_dir, file_name)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(page_source)

    return file_name


def wait_for_listing_page_content(driver: webdriver.Chrome, current_page: int) -> None:
    """Wait for listing page elements to load.

    Raises:
        Exception: Propagates if the page source shows rate limiting,
                   so the retry loop can handle it.
    """

    wait = WebDriverWait(driver, WEBDRIVER_TIMEOUT_DEFAULT)

    try:
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ECIlistingSelectors.INITIATIVE_CARDS)
            )
        )
        logger.info(LOG_MESSAGES["page_loaded"].format(page=current_page))

        random_time = random.uniform(*WAIT_DYNAMIC_CONTENT)
        logger.debug(f"Waiting {random_time:.1f}s for dynamic content...")
        time.sleep(random_time)

    except Exception as e:

        # Re-raise rate limit timeouts — let retry handle them.
        # Swallow genuine "no content on this page" timeouts.
        check_rate_limiting(driver)
        logger.warning(
            f"No initiatives found or timeout on page {current_page}: "
            f"{e} — continuing with current content"
        )


def navigate_to_next_page(driver: webdriver.Chrome, current_page: int) -> bool:
    """Click the next-page button if present.

    Returns:
        bool: True if navigated to the next page, False if no more pages.
    """

    try:
        next_button = driver.find_element(
            By.CSS_SELECTOR, ECIlistingSelectors.NEXT_BUTTON
        )
        logger.info(
            LOG_MESSAGES["next_button_found"].format(
                page=current_page, next_page=current_page + 1
            )
        )

        driver.execute_script("arguments[0].click();", next_button)
        time.sleep(random.uniform(*WAIT_BETWEEN_PAGES))
        return True

    except Exception:
        logger.info(LOG_MESSAGES["last_page"].format(page=current_page))
        return False


def scrape_initiatives_page(
    driver: webdriver.Chrome, base_url: str, list_dir: str
) -> Tuple[str, str]:
    """Load the main listing page, wait for elements, and save HTML source."""

    url = base_url + ROUTE_FIND_INITIATIVE
    result: dict = {}

    def _attempt() -> None:

        _load_listing_url(driver, url)

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
            logger.info("Initiatives loaded successfully")

        except Exception as e:

            check_rate_limiting(driver)
            logger.warning(f"Timeout waiting for initiatives: {e} — continuing")

        page_source = driver.page_source
        main_page_path = os.path.join(list_dir, LISTING_PAGE_MAIN_FILENAME)

        with open(main_page_path, "w", encoding="utf-8") as f:
            f.write(BeautifulSoup(page_source, "html.parser").prettify())

        logger.info(f"Main page saved to: {main_page_path}")
        result["source"] = page_source
        result["path"] = main_page_path

    success = download_with_retry(
        attempt_fn=_attempt,
        debug_fn=lambda: save_debug_page(
            driver,
            url,
            save_fn=lambda src: _save_debug_listing_page(list_dir, 0, src),
            logger=logger,
        ),
        url=url,
        max_retries=DEFAULT_MAX_RETRIES,
        retry_wait_base=random.uniform(*RETRY_WAIT_BASE),
        logger=logger,
    )

    if not success:
        logger.error("❌ Failed to scrape main initiatives page")
        return "", ""

    return result["source"], result["path"]
