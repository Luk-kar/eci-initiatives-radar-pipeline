from typing import Optional
from bs4 import BeautifulSoup


def extract_response_commission_url(soup: BeautifulSoup) -> Optional[str]:
    """Extract the Commission response URL from the parsed HTML."""
    ...
