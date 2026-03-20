# Python Standard Library
import datetime
from typing import Dict, Tuple
import os

# Third-party
from selenium import webdriver

# Local
from .fetchers.listings import scrape_all_listings
from .fetchers.ecis import download_all_initiatives
from .file_ops import setup_scraping_dirs, write_initiatives_csv
from .statistics import display_completion_summary
from .browser import initialize_browser
from .consts import (
    START_SCRAPING,
    SCRIPT_DIR,
    BASE_URL,
    DATA_DIR_NAME,
    LISTINGS_DIR_NAME,
    PAGES_DIR_NAME,
    CSV_FILENAME,
    LOG_MESSAGES,
)
from ._logger import logger


def scrape_eci_initiatives() -> str:
    """Main function to scrape European Citizens' Initiative data.

    Returns:
        str: Timestamp string of when scraping started
    """

    logger.info(LOG_MESSAGES["scraping_start"].format(timestamp=START_SCRAPING))

    list_dir, pages_dir = _setup_directories()
    driver = initialize_browser()

    try:
        all_initiatives_catalog, saved_page_listing_paths = _run_listings_phase(
            driver, list_dir
        )
        failed_urls = _run_ecis_pages_phase(
            driver, list_dir, pages_dir, all_initiatives_catalog
        )
    finally:
        driver.quit()
        logger.info(LOG_MESSAGES["browser_closed"])

    display_completion_summary(
        START_SCRAPING,
        all_initiatives_catalog,
        saved_page_listing_paths,
        failed_urls,
    )

    return START_SCRAPING


def _setup_directories() -> Tuple[str, str]:
    """Create and return (list_dir, pages_dir) for this scraping run."""

    list_dir = os.path.join(
        SCRIPT_DIR, DATA_DIR_NAME, START_SCRAPING, LISTINGS_DIR_NAME
    )
    pages_dir = os.path.join(SCRIPT_DIR, DATA_DIR_NAME, START_SCRAPING, PAGES_DIR_NAME)
    setup_scraping_dirs(list_dir, pages_dir)

    return list_dir, pages_dir


def _run_listings_phase(
    driver: webdriver.Chrome,
    list_dir: str,
) -> Tuple[list, list]:
    """Phase 1: scrape all listing pages and return initiative catalog and saved paths."""

    all_initiatives_catalog, saved_page_listing_paths = scrape_all_listings(
        driver, BASE_URL, list_dir
    )
    return all_initiatives_catalog, saved_page_listing_paths


def _run_ecis_pages_phase(
    driver: webdriver.Chrome,
    list_dir: str,
    pages_dir: str,
    all_initiatives_catalog: list,
) -> list:
    """Phase 2: save catalog to CSV and download individual initiative pages.

    Returns:
        list: Failed URLs that could not be downloaded.
    """

    if not all_initiatives_catalog:
        logger.warning("No initiatives found to classify or download")
        return []

    return _save_and_download_initiatives(
        driver, list_dir, pages_dir, all_initiatives_catalog
    )


def _save_and_download_initiatives(
    driver: webdriver.Chrome,
    list_dir: str,
    pages_dir: str,
    initiative_data: list[Dict[str, str]],
) -> list:
    """Save initiative data to CSV and download individual pages.

    Returns:
        list: Failed URLs that could not be downloaded.
    """

    url_list_file = os.path.join(list_dir, CSV_FILENAME)

    write_initiatives_csv(url_list_file, initiative_data)
    logger.info(f"Initiative data saved to: {url_list_file}")

    logger.info("Starting individual initiative pages download...")
    updated_data, failed_urls = download_all_initiatives(
        driver, pages_dir, initiative_data
    )

    write_initiatives_csv(url_list_file, updated_data)
    logger.info(f"Updated CSV with download timestamps: {url_list_file}")

    return failed_urls


if __name__ == "__main__":
    scrape_eci_initiatives()
