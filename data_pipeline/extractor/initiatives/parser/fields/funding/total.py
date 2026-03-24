import re
from typing import Optional

from bs4 import BeautifulSoup


def extract_funding_total(soup: BeautifulSoup) -> Optional[str]:
    """Extract total funding amount from paragraph."""

    funding_paragraph = soup.find(
        "p", string=re.compile(r"Total amount of support and funding", re.I)
    )

    if not funding_paragraph:

        for p in soup.find_all("p", class_="ecl-u-type-paragraph"):

            if "total amount of support and funding" in p.get_text().lower():
                funding_paragraph = p
                break

    if funding_paragraph:

        text = funding_paragraph.get_text()
        amount_match = re.search(r"€([\d,\.]+)", text)

        if amount_match:
            return amount_match.group(1)

    return None
