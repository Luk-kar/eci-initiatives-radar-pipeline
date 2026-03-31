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
    """Helper to extract text while preserving links in markdown format"""

    if not element.name:
        return ""

    # Skip ecl-file components completely
    if element.name == "div" and "ecl-file" in element.get("class", []):
        return ""

    # For elements with links, convert to markdown
    if element.name == "a":

        link_text = element.get_text(strip=True)
        href = element.get("href", "")

        return f"[{link_text}]({href})"

    # For list items, extract with links
    if element.name == "li":

        text_parts = []

        for child in element.children:

            if hasattr(child, "name"):

                if child.name == "a":

                    link_text = child.get_text(strip=True)
                    href = child.get("href", "")
                    text_parts.append(f"[{link_text}]({href})")

                else:

                    child_text = child.get_text(strip=True)

                    if child_text:
                        text_parts.append(child_text)
            else:
                child_text = str(child).strip()

                if child_text:
                    text_parts.append(child_text)

        return " ".join(text_parts)

    # For paragraphs and other elements, process children to preserve links
    if element.find("a"):

        text_parts = []

        for child in element.descendants:

            if isinstance(child, str):

                text = child.strip()

                if text and text not in ["", "\n"]:
                    text_parts.append(text)

            elif hasattr(child, "name") and child.name == "a":

                link_text = child.get_text(strip=True)
                href = child.get("href", "")

                if link_text:
                    text_parts.append(f"[{link_text}]({href})")

        return " ".join(text_parts)

    # Default: return plain text
    return element.get_text(strip=True)
