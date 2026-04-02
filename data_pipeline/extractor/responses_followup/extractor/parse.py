"""
Parse all collected HTML response files into field dicts.
"""

import logging
from pathlib import Path
from typing import Dict

from .parser import parse_HTML
from data_pipeline.extractor.extractor_shared.errors import HTMLParseError


logger = logging.getLogger(__name__)


def parse_html_files(html_files: Dict[str, Path]) -> Dict[str, dict]:
    """
    Parse each HTML response file and return extracted field dicts keyed by
    registration number.

    Returns:
        Dict mapping registration_number → parsed field dict.

    Raises:
        HTMLParseError: If any HTML file fails to parse.
    """
    parsed_data: Dict[str, dict] = {}

    for reg_number, html_path in html_files.items():
        try:
            parsed_data[reg_number] = parse_HTML(html_path, reg_number)
        except Exception as exc:
            raise HTMLParseError(f"Failed to parse HTML for {reg_number}") from exc

    return parsed_data
