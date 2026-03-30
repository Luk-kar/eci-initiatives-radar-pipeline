"""
Scan the responses HTML directory and build a reg_number → Path map.
"""

import re
import logging
from pathlib import Path
from typing import Dict

from data_pipeline.pipeline_shared.consts import FilePatterns


logger = logging.getLogger(__name__)


def collect_html_files(html_dir: Path) -> Dict[str, Path]:
    """
    Scan html_dir for response HTML files and derive reg numbers from filenames.

    Returns:
        Dict mapping registration_number → Path.

    Raises:
        FileNotFoundError: If no matching HTML files are found.
    """
    html_files = _scan_html_files(html_dir)

    if not html_files:
        raise FileNotFoundError(f"No HTML response files found in: {html_dir}")

    logger.info("Found %d HTML response files", len(html_files))
    return html_files


def _scan_html_files(html_dir: Path) -> Dict[str, Path]:
    """
    Walk year subdirectories under html_dir and map reg numbers to file paths.

    Filename pattern : ``2020_000001_en.html``
    Reg number       : ``2020/000001``
    """
    result: Dict[str, Path] = {}

    for html_file in html_dir.glob("*/*.html"):
        match = re.match(FilePatterns.FILENAME_REGEX, html_file.name)

        if not match:
            logger.debug("Skipping unrecognised filename: %s", html_file.name)
            continue

        year, number = match.group(1), match.group(2)
        result[f"{year}/{number}"] = html_file

    return result
