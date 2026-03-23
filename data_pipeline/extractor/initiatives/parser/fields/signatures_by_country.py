from pathlib import Path
from typing import Optional
from bs4 import BeautifulSoup


def extract_signatures_by_country(
    soup: BeautifulSoup, html_file: Path
) -> Optional[str]:
    """Extract the per-country signature breakdown from the parsed HTML."""
    ...
