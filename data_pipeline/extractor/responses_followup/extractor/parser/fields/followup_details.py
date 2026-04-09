"""
Follow-up details extractor — extracts the dedicated follow-up website (if
present) and the flat list of follow-up events as plain text with links.
"""

import logging
import re
from typing import List, Optional

from bs4 import BeautifulSoup, Tag

from .utils import (
    find_answer_header,
    extract_element_with_links,
)

logger = logging.getLogger(__name__)

_STOP_SECTION_IDS: frozenset = frozenset({"related-links", "press-release", "video"})

_SKIP_PHRASES: frozenset = frozenset(
    {
        "share this page",
        "search for available translations",
    }
)

_RESPONSE_SECTION_IDS: frozenset = frozenset(
    {
        "response-of-the-commission",
        "answer-of-the-european-commission",
    }
)

_RESPONSE_SECTION_TEXTS: frozenset = frozenset(
    {
        "response of the commission",
        "answer of the european commission",
    }
)

# ── Step helpers ──────────────────────────────────────────────────────────────


def _find_response_h2(soup: BeautifulSoup, registration_number: str) -> Tag:
    """Locate the Commission-response h2 element.

    Uses a two-pass strategy:
    1. Match by id attribute (fast, precise).
    2. Fall back to matching by normalised raw text content, handling h2
       elements that carry no id at all.

    Both passes cover the 'Response of the Commission' and 'Answer of the
    European Commission' heading variants.

    Args:
        soup: BeautifulSoup object of the HTML document.
        registration_number: ECI registration number (used in error messages).

    Returns:
        The first matching h2 Tag.

    Raises:
        ValueError: If no matching h2 is found by either strategy.
    """
    # Pass 1 — id attribute
    for section_id in _RESPONSE_SECTION_IDS:
        response_h2 = soup.find("h2", id=section_id)
        if response_h2:
            return response_h2

    # Pass 2 — raw text content (no id present)
    for h2 in soup.find_all("h2"):
        if h2.get_text(strip=True).lower() in _RESPONSE_SECTION_TEXTS:
            return h2

    raise ValueError(
        f"No 'Response / Answer of the Commission' section found for "
        f"{registration_number}"
    )


def _find_followup_start_h2(response_h2: Tag, registration_number: str) -> Tag:
    """Find and validate the first follow-up section h2 after the response.

    Locates the first h2 with class 'ecl-u-type-heading-2' that follows the
    'Response of the Commission' h2, and ensures it is not itself a stop
    section.

    Args:
        response_h2: The 'Response of the Commission' h2 Tag.
        registration_number: ECI registration number (used in error messages).

    Returns:
        The first follow-up section h2 Tag.

    Raises:
        ValueError: If no follow-up section exists or the next h2 is a stop
            section.
    """

    # Pass 1 — ECL class (modern layout)
    start_h2 = response_h2.find_next("h2", class_="ecl-u-type-heading-2")

    # Pass 2 — bare h2 (flat legacy layout)
    if not start_h2:
        start_h2 = response_h2.find_next("h2")

    if not start_h2:
        raise ValueError(
            f"No content section found after 'Response of the Commission' "
            f"for {registration_number}"
        )
    if start_h2.get("id") in _STOP_SECTION_IDS:
        raise ValueError(
            f"No follow-up content section found after 'Response of the "
            f"Commission' for {registration_number}"
        )
    return start_h2


def _collect_content_elements(start_h2: Tag) -> List[str]:
    """Traverse the document from start_h2, collecting leaf <p> and <li> texts.

    Iterates depth-first from start_h2 onward, collecting text from leaf-level
    <p> and <li> elements across all follow-up sections until a stop-section
    h2 or a "Share this page" paragraph is reached.

    Skipping elements whose immediate parent is also <p> or <li> prevents
    duplicate text from nested structures (e.g. <li><p>…</p></li>).

    Args:
        start_h2: The first follow-up section h2 Tag to begin traversal from.

    Returns:
        List of raw text strings extracted from qualifying elements.
    """
    content_elements: List[str] = []
    current = start_h2.find_next()

    while current:
        if current.name == "h2":

            is_section_boundary = "ecl-u-type-heading-2" in current.get(
                "class", []
            ) or not current.get(
                "class"
            )  # flat legacy layout — bare h2

            if is_section_boundary and current.get("id") in _STOP_SECTION_IDS:
                break
            # Non-stop h2 (e.g. "Supporting measures") — continue collecting

        if current.name == "p" and "Share this page" in current.get_text(strip=True):
            break

        if current.name in ("p", "li"):
            parent_name = current.parent.name if current.parent else ""
            if parent_name not in ("p", "li"):
                text = extract_element_with_links(current)
                if text and not should_skip_text(text):
                    content_elements.append(text)

        current = current.find_next()

    return content_elements


def _build_followup_actions(
    content_elements: List[str],
    registration_number: str,
) -> List[str]:
    """Normalize and validate collected content elements into follow-up actions.

    Collapses internal whitespace in each element and raises if the result is
    empty.

    Args:
        content_elements: Raw text strings from _collect_content_elements.
        registration_number: ECI registration number (used in error messages).

    Returns:
        List of normalized follow-up action strings.

    Raises:
        ValueError: If content_elements is empty.
    """
    if not content_elements:
        raise ValueError(
            f"No valid follow-up actions found after 'Response of the "
            f"Commission' for {registration_number}"
        )
    return [re.sub(r"\s+", " ", element).strip() for element in content_elements]


# ── Public API ────────────────────────────────────────────────────────────────


def extract_followup_events(
    soup: BeautifulSoup,
    registration_number: str,
) -> Optional[List[str]]:
    """
    Extract follow-up actions from after the 'Response of the Commission'
    section.

    Skips all content directly under the 'Response of the Commission' h2 and
    collects <p> and <li> elements from every subsequent section
    (e.g. "Next steps", "Supporting measures",
    "Follow-up on the Commission's actions") until a stop-section header
    or the "Share this page" marker is reached.

    Stop-section IDs: 'related-links', 'press-release', 'video'.

    Args:
        soup: BeautifulSoup object of the HTML document.
        registration_number: ECI registration number (used in error messages).

    Returns:
        List of normalized follow-up action strings, or None if not found.

    Raises:
        ValueError: If a critical error occurs during extraction.
    """
    if not soup:
        raise TypeError(
            f"soup must be a BeautifulSoup object, got "
            f"{type(soup).__name__} for {registration_number}"
        )

    try:
        response_h2 = _find_response_h2(soup, registration_number)
        start_h2 = _find_followup_start_h2(response_h2, registration_number)
        content_elements = _collect_content_elements(start_h2)

        return _build_followup_actions(content_elements, registration_number)

    except Exception as e:

        raise ValueError(
            f"Error extracting follow-up events with dates for "
            f"{registration_number}: {str(e)}"
        ) from e


# ── Filtering helper ──────────────────────────────────────────────────────────


def should_skip_text(text: str) -> bool:
    """Return True if the text element should be discarded.

    Discards:
    - Empty or whitespace-only strings.
    - Known UI/navigation strings (e.g. social-share labels).
    - Fragments shorter than 3 characters.
    """
    if not text or not text.strip():
        return True

    stripped = text.strip()
    if stripped.lower() in _SKIP_PHRASES:
        return True

    if len(stripped) < 3:
        return True

    return False
