from typing import Optional
from bs4 import BeautifulSoup


def extract_timeline_data(soup: BeautifulSoup) -> dict[str, Optional[str]]:
    """Extract all timeline fields from the parsed HTML.

    Returns:
        Dictionary with keys: ``timeline_registered``,
        ``timeline_collection_start_date``, ``timeline_collection_closed``,
        ``timeline_verification_start``, ``timeline_verification_end``,
        ``timeline_response_commission_date``, ``timeline``.
    """
    ...
