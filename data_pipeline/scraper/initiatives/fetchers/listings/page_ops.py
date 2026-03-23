"""
Page-level browser operations for ECI listing scraping.

This module provides helpers for loading listing pages, moving through
pagination, and coordinating WebDriver interactions required to collect
initiative listing content.
"""

# Python Standard Library
import os
import random
import time

# Third-party
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Shared
from ....scraper_shared.fetch_utils import check_rate_limiting
from ....scraper_shared.consts import DEBUGGING_DIR_NAME
from ....scraper_shared.files_utils import ensure_dirs

# Local
from ...css_selectors import ECIlistingSelectors
from ...consts import (
    WAIT_DYNAMIC_CONTENT,
    WAIT_BETWEEN_PAGES,
    WEBDRIVER_TIMEOUT_DEFAULT,
    LISTING_PAGE_FILENAME_PATTERN,
)
from ...log_messages import LOG_MESSAGES
from ..._logger import logger


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

    except NoSuchElementException:

        logger.info(LOG_MESSAGES["last_page"].format(page=current_page))
        return False


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
        logger.debug(LOG_MESSAGES["dynamic_content_wait"].format(wait_time=random_time))
        time.sleep(random_time)

    except TimeoutException as e:
        # Re-raise rate limit timeouts — let retry handle them.
        # Swallow genuine "no content on this page" timeouts.

        check_rate_limiting(driver)
        logger.warning(
            LOG_MESSAGES["listing_content_timeout"].format(page=current_page, error=e)
        )


def load_listing_url(driver: webdriver.Chrome, url: str) -> None:
    """Load the listing URL and check for rate limiting.

    Raises:
        Exception: If the loaded page shows rate limiting indicators.
    """

    logger.info(LOG_MESSAGES["loading_page"].format(url=url))
    driver.get(url)
    time.sleep(random.uniform(*WAIT_DYNAMIC_CONTENT))
    check_rate_limiting(driver)


def save_debug_listing_page(list_dir: str, current_page: int, page_source: str) -> str:
    """Save a listing page to the debugging subdirectory."""

    debug_dir = os.path.join(
        os.path.dirname(list_dir), DEBUGGING_DIR_NAME, os.path.basename(list_dir)
    )
    ensure_dirs(debug_dir)

    file_name = LISTING_PAGE_FILENAME_PATTERN.format(current_page)
    file_path = os.path.join(debug_dir, file_name)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(page_source)

    return file_name
