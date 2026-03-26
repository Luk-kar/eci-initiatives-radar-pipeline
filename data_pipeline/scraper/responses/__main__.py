"""
Main entry point for the Commission responses scraper.
"""

import datetime
import logging
import os
from typing import List, Tuple

from .consts import (
    PIPELINE_DIR,
    DATA_DIR_NAME,
    LOG_DIR_NAME,
    RESPONSES_DIR_NAME,
    INITIATIVE_PAGES_DIR_NAME,
    CSV_FILENAME,
)
from .log_messages import LOG_MESSAGES
from .errors import MissingDataDirectoryError
from .html_parser import ResponseLinkExtractor
from .fetchers.responses import download_all_responses
from .browser import initialize_browser
from .file_operations.csv import write_responses_csv
from .statistics import display_completion_summary
from ._logger import logger
from ..scraper_shared.files_utils import ensure_dirs


def scrape_commission_responses() -> str:
    """Scrape Commission response pages for all known ECI initiatives.

    Reads from the latest timestamp directory produced by the initiatives
    scraper, downloads each Commission response page, and writes a CSV.

    Returns:
        Timestamp string of when scraping began.

    Raises:
        MissingDataDirectoryError: If no initiatives run directory is found.
    """
    timestamp_dir = _resolve_run_dir()
    _setup_file_logging(os.path.join(timestamp_dir, LOG_DIR_NAME))

    start_scraping = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    logger.info(LOG_MESSAGES["scraping_start"].format(timestamp=timestamp_dir))

    initiative_pages_dir = _resolve_initiative_pages_dir(timestamp_dir)
    if not initiative_pages_dir:
        return start_scraping

    responses_dir = _setup_responses_dir(timestamp_dir)

    response_links = _extract_response_links(initiative_pages_dir)
    if not response_links:
        return start_scraping

    csv_path = os.path.join(responses_dir, CSV_FILENAME)
    _write_initial_csv(csv_path, response_links)

    updated_data, failed_urls = _run_downloads(responses_dir, response_links)

    _finalise_csv(csv_path, updated_data)

    display_completion_summary(
        start_scraping, response_links, failed_urls, len(updated_data), responses_dir
    )

    return start_scraping


# ── Step functions ─────────────────────────────────────────────────────────────


def _resolve_run_dir() -> str:
    """Locate the newest timestamped run directory from the initiatives scraper.

    Raises:
        MissingDataDirectoryError: If the data dir or timestamp dirs are absent.
    """
    try:
        return _find_latest_timestamp_directory()
    except FileNotFoundError as e:
        raise MissingDataDirectoryError(
            expected_path=os.path.join(PIPELINE_DIR, DATA_DIR_NAME),
        ) from e


def _resolve_initiative_pages_dir(timestamp_dir: str) -> str | None:
    """Return the initiative pages directory path, or None if it does not exist.

    Args:
        timestamp_dir: Root of the current scraping run.
    """
    path = os.path.join(timestamp_dir, INITIATIVE_PAGES_DIR_NAME)

    if not os.path.isdir(path):
        logger.error(LOG_MESSAGES["initiative_pages_missing"].format(path=path))
        return None

    return path


def _setup_responses_dir(timestamp_dir: str) -> str:
    """Create and return the responses output directory.

    Args:
        timestamp_dir: Root of the current scraping run.
    """
    responses_dir = os.path.join(timestamp_dir, RESPONSES_DIR_NAME)
    ensure_dirs(responses_dir)
    return responses_dir


def _extract_response_links(initiative_pages_dir: str) -> list:
    """Extract Commission response links from all initiative HTML files.

    Args:
        initiative_pages_dir: Directory containing year-partitioned HTML files.
    """
    response_links = ResponseLinkExtractor().extract_links_from_directory(
        initiative_pages_dir
    )

    if not response_links:
        logger.warning(LOG_MESSAGES["no_links_found"])
    else:
        logger.info(LOG_MESSAGES["links_found"].format(count=len(response_links)))

    return response_links


def _run_downloads(
    responses_dir: str,
    response_links: list,
) -> Tuple[list, list]:
    """Initialise a browser, download all response pages, and close the browser.

    Args:
        responses_dir: Base directory for saving HTML files.
        response_links: List of dicts with 'url', 'year', 'reg_number', 'title'.

    Returns:
        Tuple of (updated_data, failed_urls).
    """
    driver = initialize_browser()

    try:
        return download_all_responses(driver, responses_dir, response_links)
    finally:
        driver.quit()
        logger.info(LOG_MESSAGES["browser_closed"])


def _finalise_csv(csv_path: str, updated_data: list) -> None:
    """Overwrite the CSV with download timestamps from a completed run.

    Args:
        csv_path: Path to the responses CSV file.
        updated_data: List of response dicts including populated datetimes.
    """
    write_responses_csv(csv_path, updated_data)
    logger.info(LOG_MESSAGES["csv_timestamps_updated"].format(path=csv_path))


# ── Internal helpers ───────────────────────────────────────────────────────────


def _setup_file_logging(log_dir: str) -> None:
    """Attach a file handler and (if absent) a console handler to the logger."""
    ensure_dirs(log_dir)

    if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(console)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(log_dir, f"scraper_responses_{timestamp}.log")
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
        )
    )
    logger.addHandler(file_handler)
    logger.info(f"Log file created: {log_file}")


def _find_latest_timestamp_directory() -> str:
    """Return the path to the most recent timestamped run directory.

    Raises:
        FileNotFoundError: If the data dir or any timestamp dirs are absent.
    """
    data_dir = os.path.join(PIPELINE_DIR, DATA_DIR_NAME)

    if not os.path.exists(data_dir):
        raise FileNotFoundError(f"Data directory does not exist: {data_dir}")

    entries = [
        d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))
    ]

    if not entries:
        raise FileNotFoundError(f"No timestamp directories found in: {data_dir}")

    entries.sort(reverse=True)
    return os.path.join(data_dir, entries[0])


def _write_initial_csv(csv_path: str, response_links: List[dict]) -> None:
    """Write initial CSV with empty datetimes as a pre-download checkpoint."""
    write_responses_csv(
        csv_path,
        [
            {
                "url_find_initiative": link["url"],
                "registration_number": link["reg_number"],
                "title": link.get("title", ""),
                "datetime": "",
            }
            for link in response_links
        ],
    )
    logger.info(f"Initial CSV created: {csv_path}")


if __name__ == "__main__":
    scrape_commission_responses()
