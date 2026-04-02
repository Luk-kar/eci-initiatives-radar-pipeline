"""Shared WebDriver waiter for Commission response and follow-up pages."""

import logging
from selenium import webdriver
from selenium.webdriver.common.by import By

from ..wait_utils import wait_for_any_selector
from .css_selectors import ResponsePageSelectors


def wait_for_page_content(
    driver: webdriver.Chrome,
    *,
    timeout: float,
    logger: logging.Logger,
    log_messages: dict,
) -> bool:
    """Wait for a Commission response or follow-up page to finish loading."""
    return wait_for_any_selector(
        driver=driver,
        selectors=[
            ResponsePageSelectors.MAIN_CONTENT,
            ResponsePageSelectors.PAGE_HEADER_TITLE,
        ],
        timeout=timeout,
        by=By.CSS_SELECTOR,
        logger=logger,
        log_messages=log_messages,
    )
