# Python Standard Library
import datetime
import random
import time
from typing import Tuple

# Third-party
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Shared
from ..scraper_shared.downloader import (
    check_rate_limiting,
    download_with_retry,
    save_debug_page,
)

# Local
from .css_selectors import ECIinitiativeSelectors
from .consts import (
    WAIT_DYNAMIC_CONTENT,
    WAIT_BETWEEN_DOWNLOADS,
    RETRY_WAIT_BASE,
    WEBDRIVER_TIMEOUT_CONTENT,
    DEFAULT_MAX_RETRIES,
    LOG_MESSAGES,
)
from .file_ops import save_initiative_page
from .scraper_logger import logger


def download_initiatives(
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

    # NOTE: driver lifecycle (init/quit) is managed by caller

    for i, row in enumerate(initiative_data):
        url = row["url"]
        logger.info(f"Processing {i+1}/{len(initiative_data)}: {url}")

        success = download_single_initiative(driver, pages_dir, url)

        if success:
            row["datetime"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            failed_urls.append(url)

        updated_data.append(row)

        wait_time = random.uniform(*WAIT_BETWEEN_DOWNLOADS)
        logger.info(f"Awaiting next page in: {wait_time:.2f}s")
        time.sleep(wait_time)

    logger.info(f"Download completed. Failed URLs: {len(failed_urls)}")
    return updated_data, failed_urls


def wait_for_page_content(driver: webdriver.Chrome) -> bool:
    """Wait for initiative page content to load.

    Returns:
        bool: True if main content was found, False otherwise.
    """

    wait = WebDriverWait(driver, WEBDRIVER_TIMEOUT_CONTENT)

    try:
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ECIinitiativeSelectors.INITIATIVE_PROGRESS)
            )
        )
        logger.debug("Initiative progress timeline loaded")
    except Exception:
        logger.warning(
            "Initiative progress timeline not found, "
            "should be in all initiatives.\ncontinuing..."
        )

    content_selectors_to_wait = [
        ECIinitiativeSelectors.OBJECTIVES,
        ECIinitiativeSelectors.ANNEX,
        ECIinitiativeSelectors.ORGANISERS,
        ECIinitiativeSelectors.REPRESENTATIVE,
        ECIinitiativeSelectors.SOURCES_OF_FUNDING,
        ECIinitiativeSelectors.SOCIAL_SHARE,
    ]

    for selector in content_selectors_to_wait:
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, selector)))
            logger.debug(f"Content loaded: {selector}")
            return True
        except Exception:
            continue

    logger.warning("No main content elements found, but proceeding...")
    return False


def _attempt_download(
    driver: webdriver.Chrome,
    pages_dir: str,
    url: str,
) -> str:
    """Perform a single download attempt. Returns the saved filename.

    Raises:
        Exception: On rate limiting or any page/save failure.
    """

    logger.info("Downloading the html file...")
    driver.get(url)

    time.sleep(random.uniform(*WAIT_DYNAMIC_CONTENT))
    check_rate_limiting(driver)
    content_found = wait_for_page_content(driver)

    file_name = save_initiative_page(
        pages_dir, url, driver.page_source, debug=not content_found
    )
    logger.info(LOG_MESSAGES["download_success"].format(filename=file_name))
    return file_name


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
