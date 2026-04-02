"""Shared helper for saving a Commission response or follow-up page HTML to disk."""

import logging
import os

from ...html_utils import save_html, validate_html
from ...files_utils import ensure_dirs
from ...consts import DEBUGGING_DIR_NAME, INITIATIVE_PAGE_FILENAME_PATTERN


def save_response_page(
    responses_dir: str,
    year: str,
    reg_number: str,
    page_source: str,
    debug: bool = False,
    *,
    logger: logging.Logger,
) -> str:
    """Save a Commission response (or follow-up) page HTML to disk.

    Args:
        responses_dir: Base directory for response HTML files.
        year: Year extracted from the initiative path (e.g. ``"2019"``).
        reg_number: Registration-number slug (e.g. ``"000007"``).
        page_source: Raw HTML string.
        debug: If ``True``, save under a debugging subdirectory instead.
        logger: Caller-supplied logger (keyword-only).

    Returns:
        Relative filename (e.g. ``"2019_000007_en.html"``).

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
