"""
Shared browser initialization and management utilities.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from .const import CHROME_OPTIONS


def initialize_browser(logger, log_messages: dict | None = None) -> webdriver.Chrome:
    """Initialize Chrome WebDriver with configured options.

    Args:
        logger: Logger instance to use for logging.
        log_messages: Optional dict with "browser_init" and "browser_success" keys.

    Returns:
        Configured Chrome WebDriver instance.
    """
    if log_messages is not None:
        if "browser_init" in log_messages:
            logger.info(log_messages["browser_init"])
    chrome_options = Options()
    for option in CHROME_OPTIONS:
        chrome_options.add_argument(option)

    driver = webdriver.Chrome(options=chrome_options)

    if log_messages is not None:
        if "browser_success" in log_messages:
            logger.debug(log_messages["browser_success"])

    return driver
