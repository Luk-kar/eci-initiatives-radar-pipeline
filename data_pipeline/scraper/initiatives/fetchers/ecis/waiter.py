"""
WebDriver wait utilities for individual ECI detail pages.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By

from ....scraper_shared.wait_utils import wait_for_any_selector, wait_for_selector
from ...css_selectors import ECIinitiativeSelectors
from ...consts import WEBDRIVER_TIMEOUT_CONTENT
from ..._logger import logger
from ...log_messages import LOG_MESSAGES


def wait_for_page_content(driver: webdriver.Chrome) -> bool:
    """Wait for initiative page content to load.

    Phase 1: attempt the timeline selector (CSS) — failure is non-fatal.
    Phase 2: probe content selectors (XPath) — returns True on first match.

    Returns:
        bool: True if any content element was found, False otherwise.
    """
    wait_for_selector(
        driver=driver,
        selector=ECIinitiativeSelectors.INITIATIVE_PROGRESS,
        timeout=WEBDRIVER_TIMEOUT_CONTENT,
        by=By.CSS_SELECTOR,
        logger=logger,
        on_success_msg=LOG_MESSAGES["timeline_loaded"],
        on_timeout_msg=LOG_MESSAGES["timeline_not_found"],
    )

    return wait_for_any_selector(
        driver=driver,
        selectors=[
            ECIinitiativeSelectors.OBJECTIVES,
            ECIinitiativeSelectors.ANNEX,
            ECIinitiativeSelectors.ORGANISERS,
            ECIinitiativeSelectors.REPRESENTATIVE,
            ECIinitiativeSelectors.SOURCES_OF_FUNDING,
            ECIinitiativeSelectors.SOCIAL_SHARE,
        ],
        timeout=WEBDRIVER_TIMEOUT_CONTENT,
        by=By.XPATH,
        logger=logger,
        log_messages=LOG_MESSAGES,
    )
