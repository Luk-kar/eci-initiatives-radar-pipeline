from pathlib import Path


def extract_registration_number(self, filename: str) -> str:
    """Extract registration number from filename pattern YYYY_NNNNNN_en.html"""

    pattern = FilePatterns.FILENAME_REGEX
    match = re.match(pattern, filename)

    if match:

        year, number = match.groups()
        return f"{year}/{number}"

    return ""
