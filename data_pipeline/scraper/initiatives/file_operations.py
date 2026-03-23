"""
File operation utilities for saving scraped ECI pages.

This module handles creating directories, constructing file paths,
and writing raw HTML content to disk. It includes logic for saving both
individual initiative detail pages and main listing pages, while also
supporting debugging modes.
"""

# Python Standard Library
import os
from typing import Dict, Tuple

# Third-party
from selenium import webdriver
from html5lib.html5parser import ParseError

# Shared
from ..scraper_shared.files_utils import ensure_dirs, write_csv
from ..scraper_shared.html_utils import validate_html, save_html
from ..scraper_shared.exceptions import RateLimitError

# Local
from .consts import (
    CSV_FIELDNAMES,
    MIN_HTML_LENGTH,
    RATE_LIMIT_INDICATORS,
    LISTING_PAGE_FILENAME_PATTERN,
    INITIATIVE_PAGE_FILENAME_PATTERN,
)
from ._logger import logger
from .log_messages import LOG_MESSAGES


def setup_scraping_dirs(list_dir: str, pages_dir: str) -> None:
    """Create necessary directories for scraping output."""

    ensure_dirs(list_dir, pages_dir)
    logger.debug(
        LOG_MESSAGES["dirs_created"].format(list_dir=list_dir, pages_dir=pages_dir)
    )


def save_listing_page(
    driver: webdriver.Chrome, list_dir: str, current_page: int
) -> Tuple[str, str]:
    """Save listing page source and return page source and file path."""

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
        raise RateLimitError("429 - Rate limited (found in page source)")

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

    file_name = INITIATIVE_PAGE_FILENAME_PATTERN.format(year=year, number=number)
    file_path = os.path.join(year_dir, file_name)

    try:
        validate_html(page_source, MIN_HTML_LENGTH)

    except (ValueError, ParseError) as e:

        logger.warning(
            LOG_MESSAGES["html_validation_warning"].format(
                filename=file_name, error_type=type(e).__name__, error=e
            )
        )
    try:
        save_html(file_path, page_source)

    except OSError as e:

        logger.warning(
            LOG_MESSAGES["html_prettify_failed"].format(filename=file_name, error=e)
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
