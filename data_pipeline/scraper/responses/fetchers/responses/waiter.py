"""
WebDriver wait utilities for Commission response pages.
"""

from selenium import webdriver

from ....scraper_shared.response_and_followup.waiter import (
    wait_for_page_content as _wait_for_page_content,
)
from ...consts import WEBDRIVER_TIMEOUT_CONTENT
from ...log_messages import LOG_MESSAGES
from ..._logger import logger


def wait_for_page_content(driver: webdriver.Chrome) -> bool:
    """Wait for Commission response page content to load."""
    return _wait_for_page_content(
        driver,
        timeout=WEBDRIVER_TIMEOUT_CONTENT,
        logger=logger,
        log_messages=LOG_MESSAGES,
    )
