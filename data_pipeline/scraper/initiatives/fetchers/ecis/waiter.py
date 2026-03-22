"""
WebDriver wait utilities for individual ECI detail pages.

This module provides synchronization functions to ensure that dynamic
content on European Citizens' Initiative (ECI) pages is fully loaded
before data extraction begins. It handles expected timeouts and guards
against rate limiting during the fetching process.
"""

# Third-party
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


# Local
from ...css_selectors import ECIinitiativeSelectors
from ...consts import WEBDRIVER_TIMEOUT_CONTENT
from ..._logger import logger
from ...log_messages import LOG_MESSAGES


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
        logger.debug(LOG_MESSAGES["timeline_loaded"])

    except TimeoutException:
        logger.warning(LOG_MESSAGES["timeline_not_found"])

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
            logger.debug(LOG_MESSAGES["content_loaded"].format(selector=selector))
            return True

        except TimeoutException:
            continue

    logger.warning(LOG_MESSAGES["no_content_found"])
    return False
