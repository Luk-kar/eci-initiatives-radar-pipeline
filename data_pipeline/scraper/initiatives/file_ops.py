# Python Standard Library
import os
import random
import time
from typing import Dict, List, Tuple

# Third-party
from selenium import webdriver

# Shared
from ..scraper_shared.fs_utils import ensure_dirs, write_csv
from ..scraper_shared.html_utils import validate_html, save_html

# Local
from .consts import (
    WAIT_DYNAMIC_CONTENT,
    CSV_FIELDNAMES,
    MIN_HTML_LENGTH,
    RATE_LIMIT_INDICATORS,
    LISTING_PAGE_FILENAME_PATTERN,
    LOG_MESSAGES,
)
from .scraper_logger import logger


def setup_scraping_dirs(list_dir: str, pages_dir: str) -> None:
    """Create necessary directories for scraping output."""
    ensure_dirs(list_dir, pages_dir)
    logger.debug(f"Created directories: {list_dir}, {pages_dir}")


def save_listing_page(
    driver: webdriver.Chrome, list_dir: str, current_page: int
) -> Tuple[str, str]:
    """Save listing page source and return page source and file path."""
    # Additional wait for dynamic content
    random_time = random.uniform(*WAIT_DYNAMIC_CONTENT)
    logger.debug(f"Waiting {random_time:.1f}s for dynamic content...")
    time.sleep(random_time)

    # Get page source and save it
    page_source = driver.page_source
    page_filename = LISTING_PAGE_FILENAME_PATTERN.format(current_page)
    page_path = os.path.join(list_dir, page_filename)

    # Validate then prettify+save
    validate_html(page_source, MIN_HTML_LENGTH)
    save_html(page_path, page_source)

    logger.info(LOG_MESSAGES["page_saved"].format(page=current_page, path=page_path))
    return page_source, page_path


def save_initiative_page(
    pages_dir: str,
    url: str,
    page_source: str,
    debug: bool = False,
) -> str:
    """Save initiative page source to file and return filename.

    Args:
        pages_dir: Base directory for initiative pages.
        url: Initiative URL used to derive year/filename.
        page_source: Raw HTML content to save.
        debug: If True, save under the debugging directory instead.
    """

    if not debug and any(
        indicator in page_source for indicator in RATE_LIMIT_INDICATORS[:2]
    ):
        raise Exception("429 - Rate limited (found in page source)")

    parts = url.rstrip("/").split("/")
    year = parts[-2]
    number = parts[-1]

    if debug:

        # data/<timestamp>/debugging/initiatives/<year>/
        run_dir = os.path.dirname(pages_dir)
        module_dir = os.path.basename(pages_dir)
        year_dir = os.path.join(run_dir, DEBUGGING_DIR_NAME, module_dir, year)

    else:
        # data/<timestamp>/initiatives/<year>/
        year_dir = os.path.join(pages_dir, year)

    ensure_dirs(year_dir)

    file_name = f"{year}_{number}.html"
    file_path = os.path.join(year_dir, file_name)

    try:
        validate_html(page_source, MIN_HTML_LENGTH)
    except Exception as e:
        logger.warning(
            f"⚠️  HTML validation warning for {file_name}: {type(e).__name__}: {e}"
        )

    try:
        save_html(file_path, page_source)
    except Exception as e:
        logger.warning(
            f"⚠️  Failed to prettify HTML for {file_name}: {str(e)}. "
            "Saving raw HTML without prettification."
        )
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(page_source)

    return file_name


def write_initiatives_csv(
    file_path: str, initiative_data: list[Dict[str, str]]
) -> None:
    """Write initiative data to CSV file.

    Args:
        file_path: Full path to the CSV file
        initiative_data: List of initiative dictionaries to write
    """
    write_csv(file_path, CSV_FIELDNAMES, initiative_data)
