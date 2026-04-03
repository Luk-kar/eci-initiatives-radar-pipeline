"""
Commission answer extractor — extracts the full text of the Commission\'s
response to the ECI, preserving inline hyperlinks as plain text with URLs.
"""

import logging
from typing import Optional, List

from bs4 import BeautifulSoup, Tag

from .utils import extract_element_with_links

logger = logging.getLogger(__name__)

_RESPONSE_HEADER_ID = "response-of-the-commission"
_RESPONSE_HEADER_TEXT = "Response of the Commission"
_HEADING_TAGS = frozenset({"h1", "h2", "h3", "h4", "h5", "h6"})


def extract_commission_answer(
    soup: BeautifulSoup,
    registration_number: str,
) -> Optional[List[str]]:
    """Extract the full text of the \'Response of the Commission\' section,
    preserving inline hyperlinks.

    The section is identified by an h2 with id=\'response-of-the-commission\'
    (or matching text).  Collection stops as soon as the next heading tag
    (h1–h6) is encountered.

    Raises:
        ValueError: If the section cannot be found or contains no content.
    """

    response_h2 = _find_response_header(soup)

    if not response_h2:

        raise ValueError(
            "Could not find 'Response of the Commission' section for "
            f"{registration_number}"
        )

    content_parts = _collect_response_content(response_h2)

    if not content_parts:

        raise ValueError(
            "No content found in 'Response of the Commission' section for "
            f"{registration_number}"
        )

    return content_parts


# ---------------------------------------------------------------------------
# Header location
# ---------------------------------------------------------------------------


def _find_response_header(soup: BeautifulSoup) -> Optional[Tag]:
    """Locate the h2 tag for \'Response of the Commission\'.

    Prefers the stable id-based lookup; falls back to an exact text match.
    """

    h2 = soup.find("h2", id=_RESPONSE_HEADER_ID)

    if h2:
        return h2

    for candidate in soup.find_all("h2"):

        if candidate.get_text(strip=True) == _RESPONSE_HEADER_TEXT:
            return candidate

    return None


# ---------------------------------------------------------------------------
# Content extraction
# ---------------------------------------------------------------------------


def _collect_response_content(response_h2: Tag) -> List[str]:
    """Collect content after the Response h2, stopping at the next heading tag.

    Supports two DOM layouts:

    Container-based (ECL)::

        div.ecl-u-mb-2xl
          a#paragraph_NNN
          div                     ← wrapper_div
            div.ecl               ← header block  (holds response_h2)
            div.ecl               ← content block (paragraphs, lists, …)

    Flat (fallback)::

        <h2 id="response-of-the-commission">…</h2>
        <p>…</p>
        <ul>…</ul>
        <h2 id="next-section">…</h2>

    In both cases the scan halts the moment an h1–h6 is encountered.
    """

    header_ecl_div = response_h2.parent  # immediate parent of the h2
    wrapper_div = header_ecl_div.parent if header_ecl_div else None

    content_parts: List[str] = []

    if wrapper_div:
        content_parts = _walk_wrapper_children(header_ecl_div, wrapper_div)

    # Fallback: flat layout — h2 and content are direct siblings
    if not content_parts:

        logger.debug(
            "Container-based traversal yielded nothing; "
            "falling back to flat sibling walk"
        )
        content_parts = _walk_next_siblings(response_h2)

    return content_parts


def _walk_wrapper_children(
    header_ecl_div: Tag,
    wrapper_div: Tag,
) -> List[str]:
    """Walk children of wrapper_div after the header block.

    Stops as soon as a child block itself contains any heading tag (h1–h6),
    which signals the start of the next section.
    """

    content_parts: List[str] = []
    after_header = False

    for child in wrapper_div.children:

        if not isinstance(child, Tag):
            continue

        if child is header_ecl_div:
            after_header = True
            continue

        if not after_header:
            continue

        # Any heading inside this block marks a new section — stop here.
        if child.find(_HEADING_TAGS):
            break

        for element in child.children:

            if not isinstance(element, Tag):
                continue

            text = extract_element_with_links(element)

            if text:
                content_parts.append(text)

    return content_parts


def _walk_next_siblings(response_h2: Tag) -> List[str]:
    """Fallback: collect direct next-siblings of response_h2 until a heading."""

    content_parts: List[str] = []

    for sibling in response_h2.find_next_siblings():

        # Stop on a bare heading sibling OR a block that wraps a heading.
        if sibling.name in _HEADING_TAGS or sibling.find(_HEADING_TAGS):
            break

        text = extract_element_with_links(sibling)

        if text:
            content_parts.append(text)

    return content_parts
