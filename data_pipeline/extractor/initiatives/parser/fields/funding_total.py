from typing import Optional
from bs4 import BeautifulSoup


def extract_funding_total(soup: BeautifulSoup) -> Optional[str]:
    """Extract the total funding amount from the parsed HTML."""
    ...
