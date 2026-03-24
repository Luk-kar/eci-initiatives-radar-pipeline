from bs4 import BeautifulSoup


def extract_title(soup: BeautifulSoup) -> str:
    """Extract initiative title"""

    # Try meta tag first
    meta_title = soup.find("meta", {"name": "dcterms.title"})
    if meta_title and meta_title.get("content"):
        return meta_title["content"].strip()

    # Fall back to h1 tag
    h1_title = soup.find("h1", class_="ecl-page-header-core__title")
    if h1_title:
        return h1_title.get_text().strip()

    return ""
