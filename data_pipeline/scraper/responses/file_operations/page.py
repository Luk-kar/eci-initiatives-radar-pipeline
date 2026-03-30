"""
File operations for saving Commission response HTML pages.
"""

import os

# Shared
from ...scraper_shared.html_utils import validate_html, save_html
from ...scraper_shared.files_utils import ensure_dirs
from ...scraper_shared.consts import DEBUGGING_DIR_NAME

# Local
from ..consts import INITIATIVE_PAGE_FILENAME_PATTERN
from .._logger import logger


def save_response_page(
    responses_dir: str,
    year: str,
    reg_number: str,
    page_source: str,
    debug: bool = False,
) -> str:
    """Save a Commission response page HTML to disk.

    Args:
        responses_dir: Base directory for response HTML files.
        year: Year extracted from the initiative path (e.g. "2019").
        reg_number: Registration number slug (e.g. "000007").
        page_source: Raw HTML string.
        debug: If True, save under a debugging subdirectory instead.

    Returns:
        Relative filename (e.g. "2019/000007_en.html").

    Raises:
        ValueError: If the HTML is too short.
        ParseError: If the HTML fails html5lib validation.
    """
    validate_html(page_source)

    filename = INITIATIVE_PAGE_FILENAME_PATTERN.format(year=year, number=reg_number)

    if debug:
        target_dir = os.path.join(
            os.path.dirname(responses_dir),
            DEBUGGING_DIR_NAME,
            os.path.basename(responses_dir),
            year,
        )
    else:
        target_dir = os.path.join(responses_dir, year)

    full_path = os.path.join(target_dir, os.path.basename(filename))

    ensure_dirs(target_dir)
    save_html(full_path, page_source)
    logger.debug(f"Saved response page: {filename}")

    return filename
