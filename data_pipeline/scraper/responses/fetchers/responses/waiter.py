"""
WebDriver wait utilities for Commission response pages.
"""

# Third-party
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

# Local
from ...css_selectors import ResponsePageSelectors
from ...consts import WEBDRIVER_TIMEOUT_CONTENT
from ..._logger import logger
from ...log_messages import LOG_MESSAGES


def wait_for_page_content(driver: webdriver.Chrome) -> bool:
    """Wait for response page content to load.

    Tries selectors in order of preference, returning True as soon
    as any element is located.

    Returns:
        bool: True if any content element was found, False otherwise.
    """
    wait = WebDriverWait(driver, WEBDRIVER_TIMEOUT_CONTENT)

    selectors_to_try = [
        ResponsePageSelectors.MAIN_CONTENT,
        ResponsePageSelectors.PAGE_HEADER_TITLE,
        ResponsePageSelectors.INITIATIVE_PROGRESS,
    ]

    for selector in selectors_to_try:
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            logger.debug(LOG_MESSAGES["content_loaded"].format(selector=selector))
            return True

        except TimeoutException:
            continue

    logger.warning(LOG_MESSAGES["no_content_found"])
    return False
