from typing import Optional
from bs4 import BeautifulSoup


def extract_response_commission_url(soup: BeautifulSoup) -> Optional[str]:
    """
    Extract the Commission's answer and follow-up page URL.

    Finds the <a> tag containing text "Commission's answer and follow-up"
    and returns its href attribute.

    Returns:
        URL to the initiative's follow-up page, or None if not found
    """

    # Find the link with text containing "Commission's answer and follow-up"
    link = soup.find(
        "a", string=re.compile(r"Commission['\u2019]s answer and follow-up", re.I)
    )

    if link and link.get("href"):
        return link.get("href")

    return None
