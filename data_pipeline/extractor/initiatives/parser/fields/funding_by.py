from pathlib import Path
from typing import Optional
from bs4 import BeautifulSoup


def extract_funding_by(soup: BeautifulSoup, html_file: Path) -> Optional[str]:
    """Extract the funding sources from the parsed HTML."""
    ...
