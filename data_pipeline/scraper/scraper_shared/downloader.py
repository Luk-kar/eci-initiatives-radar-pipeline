# Python Standard Library
import time
import logging
from enum import Enum, auto
from typing import Callable

# Third-party
from selenium import webdriver

# Shared
from .consts import RATE_LIMIT_INDICATORS, MIN_HTML_LENGTH


class RetryOutcome(Enum):
    CONTINUE = auto()
    EXHAUSTED = auto()
    ABORT = auto()


def check_rate_limiting(driver: webdriver.Chrome) -> None:
    """Raise if the current page shows rate limiting indicators."""

    if any(indicator in driver.page_source for indicator in RATE_LIMIT_INDICATORS):
        raise Exception(RATE_LIMIT_INDICATORS[3])


def log_download_error(url: str, e: Exception, logger: logging.Logger) -> None:
    """Log a download error with a category label based on the error message."""

    error_type = type(e).__name__
    error_msg = str(e).lower()
    prefix = f"{url}:\n{error_type}:\n{e}"

    if "chrome not reachable" in error_msg or "session not created" in error_msg:

        logger.error(f"❌ Browser crash/connection error downloading:\n{prefix}")
    elif "timeout" in error_msg:

        logger.error(f"❌ Timeout error downloading:\n{prefix}")
    elif "permission" in error_msg or "access" in error_msg:

        logger.error(f"❌ Permission/access error downloading:\n{prefix}")
    elif "network" in error_msg or "connection" in error_msg:

        logger.error(f"❌ Network error downloading:\n{prefix}")
    elif "disk" in error_msg or "space" in error_msg:

        logger.error(f"❌ Disk space error downloading:\n{prefix}")
    else:

        logger.error(f"❌ Unknown error downloading:\n{prefix}")


def handle_retry_exception(
    e: Exception,
    url: str,
    retry_count: int,
    max_retries: int,
    retry_wait_base: float,
    logger: logging.Logger,
) -> tuple[RetryOutcome, int]:
    """Classify the exception and apply retry back-off if rate-limited.

    Returns:
        Tuple of (outcome, updated retry_count).
    """

    error_msg = str(e)
    is_rate_limited = any(indicator in error_msg for indicator in RATE_LIMIT_INDICATORS)
    logger.debug(f"🔍 Exception details for {url}: {type(e).__name__}: {error_msg}")

    if not is_rate_limited:
        logger.error(f"❌ Non-retryable error downloading:\n{url}:\n{e}")
        return RetryOutcome.ABORT, retry_count

    retry_count += 1

    if retry_count <= max_retries:

        wait_time = retry_wait_base * (retry_count**2)
        logger.warning(
            f"⚠️  Rate limiting detected. Retrying {retry_count}/{max_retries} "
            f"in {wait_time:.1f}s..."
        )
        time.sleep(wait_time)

        return RetryOutcome.CONTINUE, retry_count

    log_download_error(url, e, logger)
    return RetryOutcome.EXHAUSTED, retry_count


def save_debug_page(
    driver: webdriver.Chrome,
    url: str,
    save_fn: Callable[[str], str],  # fn(page_source) -> filename
    logger: logging.Logger,
) -> None:
    """Attempt to save the last loaded page source to the debugging directory."""

    try:
        page_source = driver.page_source

        if len(page_source) < MIN_HTML_LENGTH:
            logger.warning("⚠️  Last page source too short to save for debugging.")
            return

        file_name = save_fn(page_source)
        logger.info(f"🐛 Debug page saved: {file_name}")

    except Exception as e:
        logger.warning(f"⚠️  Could not save debug page for {url}: {e}")


def download_with_retry(
    attempt_fn: Callable[[], str],  # fn() -> filename, raises on failure
    debug_fn: Callable[[], None],  # called once after exhaustion
    url: str,
    max_retries: int,
    retry_wait_base: float,
    logger: logging.Logger,
) -> bool:
    """Generic retry loop for a single page download.

    Returns:
        bool: True if successful, False if all retries exhausted or aborted.
    """

    retry_count = 0

    while retry_count <= max_retries:

        try:
            attempt_fn()
            return True

        except Exception as e:

            outcome, retry_count = handle_retry_exception(
                e, url, retry_count, max_retries, retry_wait_base, logger
            )

            if outcome is RetryOutcome.ABORT:
                return False

            if outcome is RetryOutcome.EXHAUSTED:
                break

    logger.error(f"❌ Exhausted all {max_retries} retries for: {url}")
    debug_fn()

    return False
