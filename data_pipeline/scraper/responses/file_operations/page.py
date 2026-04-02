"""
File operations for saving Commission response HTML pages.
"""

import os

# Shared
from ...scraper_shared.response_and_followup.file_operations.page import (
    save_response_page as _save_response_page,
)

# Local
from .._logger import logger


def save_response_page(
    responses_dir: str,
    year: str,
    reg_number: str,
    page_source: str,
    debug: bool = False,
) -> str:
    """Save a Commission response page HTML to disk."""

    return _save_response_page(
        responses_dir, year, reg_number, page_source, debug, logger=logger
    )
