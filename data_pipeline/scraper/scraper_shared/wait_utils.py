"""
Shared WebDriver wait utilities for all ECI scraper detail-page waiters.
"""

import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


def wait_for_any_selector(
    driver: webdriver.Chrome,
    selectors: list[str],
    timeout: float,
    by: str = By.CSS_SELECTOR,
    logger: logging.Logger | None = None,
    log_messages: dict | None = None,
) -> bool:
    """Return True as soon as any selector resolves; False if all time out.

    Iterates *selectors* in order, attempting each with a fresh WebDriverWait.
    Logs each success via ``log_messages["content_loaded"]`` (if provided) and
    logs a final warning via ``log_messages["no_content_found"]`` on total failure.

    Args:
        driver: Active Chrome WebDriver instance.
        selectors: CSS or XPath selector strings to probe in order.
        timeout: WebDriverWait timeout in seconds (applied per selector).
        by: Selenium ``By`` strategy — ``By.CSS_SELECTOR`` or ``By.XPATH``.
        logger: Optional logger; suppresses logging when None.
        log_messages: Dict with optional keys ``"content_loaded"`` (format arg:
                      ``selector``) and ``"no_content_found"``.

    Returns:
        True if any selector matched, False otherwise.
    """
    wait = WebDriverWait(driver, timeout)
    _log_messages = log_messages or {}

    for selector in selectors:

        try:
            wait.until(EC.presence_of_element_located((by, selector)))

            if logger and "content_loaded" in _log_messages:
                logger.debug(_log_messages["content_loaded"].format(selector=selector))
            return True

        except TimeoutException:
            continue

    if logger and "no_content_found" in _log_messages:

        logger.warning(_log_messages["no_content_found"])
    return False


def wait_for_selector(
    driver: webdriver.Chrome,
    selector: str,
    timeout: float,
    by: str = By.CSS_SELECTOR,
    logger: logging.Logger | None = None,
    on_success_msg: str | None = None,
    on_timeout_msg: str | None = None,
) -> bool:
    """Wait for a single selector; return True on success, False on timeout.

    Args:
        driver: Active Chrome WebDriver instance.
        selector: CSS or XPath selector string.
        timeout: WebDriverWait timeout in seconds.
        by: Selenium ``By`` strategy.
        logger: Optional logger.
        on_success_msg: Optional debug message logged on success.
        on_timeout_msg: Optional warning message logged on timeout.

    Returns:
        True if the element was found, False on TimeoutException.
    """
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, selector))
        )
        if logger and on_success_msg:
            logger.debug(on_success_msg)

        return True

    except TimeoutException:

        if logger and on_timeout_msg:
            logger.warning(on_timeout_msg)

        return False
