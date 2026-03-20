# Third-party
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Local
from ...css_selectors import ECIinitiativeSelectors
from ...consts import WEBDRIVER_TIMEOUT_CONTENT
from ..._logger import logger


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
