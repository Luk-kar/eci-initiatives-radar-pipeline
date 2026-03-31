import logging
from typing import Optional

from bs4 import BeautifulSoup, Tag

# ---------------------------------------------------------------------------
# Header location
# ---------------------------------------------------------------------------


def _find_answer_header(soup: BeautifulSoup) -> Optional[Tag]:
    """Locate the Answer heading by id first, then by text fallback."""

    header = soup.find("h2", id="Answer-of-the-European-Commission")

    if not header:
        header = soup.find(
            lambda tag: tag.name == "h2"
            and "Answer of the European Commission" in tag.get_text()
        )
    return header


def _extract_element_with_links(element) -> str:
    """Extract text while preserving links in markdown format."""

    if not element.name:
        return ""

    if element.name == "div" and "ecl-file" in element.get("class", []):
        return ""

    if element.name == "a":
        link_text = element.get_text(strip=True)
        href = element.get("href", "")
        return f"[{link_text}]({href})"

    # For all other elements: walk descendants, but skip text nodes
    # that are already captured as part of an <a> tag.
    if element.find("a"):
        text_parts = []
        for child in element.descendants:
            if hasattr(child, "name") and child.name == "a":
                link_text = child.get_text(strip=True)
                href = child.get("href", "")
                if link_text:
                    text_parts.append(f"[{link_text}]({href})")
            elif isinstance(child, str) and child.parent.name != "a":
                text = child.strip()
                if text:
                    text_parts.append(text)
        return " ".join(text_parts)

    return element.get_text(strip=True)
