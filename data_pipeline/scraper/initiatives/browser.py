from selenium import webdriver

from ..scraper_shared.browser import initialize_browser as _shared_initialize_browser
from .consts import LOG_MESSAGES
from ._logger import logger


def initialize_browser() -> webdriver.Chrome:
    """Initialize Chrome WebDriver with headless options.

    Delegates to shared browser initializer while preserving logging.
    """
    return _shared_initialize_browser(logger, LOG_MESSAGES)
