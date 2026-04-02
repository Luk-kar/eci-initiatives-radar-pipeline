"""
File operations for saving Commission response HTML pages.
"""

from ...scraper_shared.response_and_followup.file_operations.page import (
    save_response_page as _save_response_page,
)
from .._logger import logger


def save_response_page(
    responses_dir: str,
    year: str,
    reg_number: str,
    page_source: str,
    debug: bool = False,
) -> str:
    """Save a Commission response follow-up page HTML to disk.

    See :func:`scraper_shared.response_and_followup.file_operations.page.save_response_page`
    for full documentation.
    """
    return _save_response_page(
        responses_dir, year, reg_number, page_source, debug, logger=logger
    )
