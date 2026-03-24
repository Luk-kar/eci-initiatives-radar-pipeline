from pathlib import Path
import re

from ...consts import FilePatterns


def extract_registration_number(filename: str) -> str:
    """Extract registration number from filename pattern YYYY_NNNNNN_en.html"""

    pattern = FilePatterns.FILENAME_REGEX
    match = re.match(pattern, filename)

    if match:

        year, number = match.groups()
        return f"{year}/{number}"

    return ""
