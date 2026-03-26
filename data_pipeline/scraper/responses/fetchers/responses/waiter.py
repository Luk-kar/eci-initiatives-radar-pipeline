"""
WebDriver wait utilities for Commission response pages.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By

from ....scraper_shared.wait_utils import wait_for_any_selector
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
    return wait_for_any_selector(
        driver=driver,
        selectors=[
            ResponsePageSelectors.MAIN_CONTENT,
            ResponsePageSelectors.PAGE_HEADER_TITLE,
            ResponsePageSelectors.INITIATIVE_PROGRESS,
        ],
        timeout=WEBDRIVER_TIMEOUT_CONTENT,
        by=By.CSS_SELECTOR,
        logger=logger,
        log_messages=LOG_MESSAGES,
    )
