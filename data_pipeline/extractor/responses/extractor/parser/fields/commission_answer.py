# data_pipeline/extractor/responses/parser/fields/commission_answer.py
"""
Commission answer extractor — extracts the full text of the Commission's
response to the ECI, preserving inline hyperlinks as plain text with URLs.
"""

import logging
from typing import Optional, List
import re

from bs4 import BeautifulSoup, Tag

from .utils import find_answer_header, extract_element_with_links

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def extract_commission_answer(
    soup: BeautifulSoup, registration_number: str
) -> Optional[List[str]]:
    """Extract main conclusions text from Communication, excluding factsheet downloads.

    If the Answer section contains insufficient content (only decision date and document links),
    extract one additional paragraph from the Follow-up section.

    Raises:
        ValueError: If the Commission answer section cannot be found or extracted
    """
    answer_header = find_answer_header(soup)

    if not answer_header:
        raise ValueError(
            "Could not find 'Answer of the European Commission' section for "
            f"{registration_number}"
        )

    content_parts, followup_header = _collect_answer_content(answer_header)

    if not content_parts:
        raise ValueError(
            "No content found in 'Answer of the European Commission' section for "
            f"{registration_number}"
        )

    if _is_answer_insufficient(content_parts) and followup_header:

        content_parts = _supplement_with_followup(content_parts, followup_header)

    return content_parts


# ---------------------------------------------------------------------------
# Section traversal
# ---------------------------------------------------------------------------


def _is_section_boundary(tag: Tag) -> tuple[bool, bool]:
    """Return (is_boundary, is_followup) for a given sibling tag."""

    if tag.name == "h2":

        h2_id = tag.get("id", "")
        h2_text = tag.get_text(strip=True)

        is_followup = "Follow-up" in h2_text or h2_id == "Follow-up"
        is_other = h2_id and h2_id != "Answer-of-the-European-Commission"

        return (is_followup or is_other), is_followup

    if tag.name == "h4" and "Follow-up" in tag.get_text(strip=True):
        return True, True

    return False, False


def _should_skip(tag: Tag) -> bool:
    """Return True for non-content elements: factsheet downloads, banners, document link lists."""

    if tag.name == "div" and "ecl-file" in tag.get("class", []):
        return True

    if tag.name == "div" and tag.get("data-inpage-navigation-source-area"):
        return True

    if tag.name == "ul" and _is_document_links_list(tag):
        return True

    return False


def _collect_answer_content(answer_header: Tag) -> tuple[list[str], Optional[Tag]]:
    """Walk siblings from the Answer header, accumulate text, and return the Follow-up header if found."""

    content_parts = []
    followup_header = None
    current = answer_header.find_next_sibling()

    while current:

        is_boundary, is_followup = _is_section_boundary(current)

        if is_boundary:

            if is_followup:
                followup_header = current

            break

        if not _should_skip(current) and current.name:

            element_text = extract_element_with_links(current)

            if element_text:
                content_parts.append(element_text)

        current = current.find_next_sibling()

    return content_parts, followup_header


def _supplement_with_followup(
    content_parts: list[str], followup_header: Tag
) -> list[str]:
    """Append the first Follow-up paragraph to the Answer content parts."""

    followup_paragraph = _extract_first_followup_paragraph(followup_header)

    if followup_paragraph:
        content_parts.append(followup_paragraph)

    return content_parts


# ---------------------------------------------------------------------------
# Content classification
# ---------------------------------------------------------------------------


def _is_document_links_list(ul_element) -> bool:
    """Check if a <ul> element contains only document links (Communication, Annex, etc.)

    Args:
        ul_element: BeautifulSoup <ul> element

    Returns:
        True if the list only contains document links, False otherwise
    """
    if not ul_element or ul_element.name != "ul":
        return False

    list_items = ul_element.find_all("li", recursive=False)

    if not list_items:
        return False

    # Check if all list items contain only document link text
    document_link_patterns = [
        r"^\s*Communication\s*$",
        r"^\s*Annex(es)?\s*$",
        r"^\s*Staff Working Document\s*$",
        r"^\s*SWD\s*$",
    ]

    for li in list_items:
        li_text = li.get_text(strip=True)

        # Check if text matches any document link pattern
        is_doc_link = False
        for pattern in document_link_patterns:
            if re.match(pattern, li_text, re.IGNORECASE):
                is_doc_link = True
                break

        if not is_doc_link:
            return False  # Contains non-document content

    return True  # All items are document links


def _is_answer_insufficient(content_parts: List[str]) -> bool:
    """Check if extracted answer text is insufficient.

    Answer is considered insufficient if it's very short and only contains:
    - Decision date
    - Document links or references

    Args:
        text: The extracted answer text

    Returns:
        True if answer is insufficient, False otherwise
    """
    text_one_string = "\n".join(content_parts).strip()

    # Remove whitespace and newlines for analysis
    normalized = re.sub(r"\s+", " ", text_one_string).strip()

    # Check length - if very short (less than 250 chars), might be insufficient
    if len(normalized) > 250:
        return False

    # Check if it contains typical insufficient content patterns
    has_decision_date = bool(re.search(r"Decision\s+date:", normalized, re.IGNORECASE))
    has_doc_reference = bool(
        re.search(r"Official\s+documents\s+related\s+to", normalized, re.IGNORECASE)
    )

    # Count meaningful sentences (excluding common metadata phrases)
    # Remove decision date line
    text_cleaned = re.sub(
        r"Decision\s+date:[^\n]*", "", normalized, flags=re.IGNORECASE
    )
    # Remove official documents line
    text_cleaned = re.sub(
        r"Official\s+documents\s+related\s+to[^\n]*",
        "",
        text_cleaned,
        flags=re.IGNORECASE,
    )
    # Clean up extra whitespace
    text_cleaned = re.sub(r"\s+", " ", text_cleaned).strip()

    # If after removing metadata, there's very little content left, it's insufficient
    if has_decision_date and has_doc_reference and len(text_cleaned) < 30:
        return True

    # Also check if it's ONLY a decision date
    if has_decision_date and len(text_cleaned) < 30:
        return True

    return False


# ---------------------------------------------------------------------------
# Text extraction
# ---------------------------------------------------------------------------


def _extract_first_followup_paragraph(followup_header) -> str:
    """Extract the first meaningful paragraph from Follow-up section.

    Args:
        followup_header: BeautifulSoup element representing the Follow-up h2 header

    Returns:
        Text of the first paragraph, or empty string if none found
    """
    current = followup_header.find_next_sibling()

    while current:
        # Stop at next h2 section
        if current.name == "h2":
            break

        # Skip factsheet file download components
        if current.name == "div" and "ecl-file" in current.get("class", []):

            current = current.find_next_sibling()
            continue

        # Extract first meaningful paragraph
        if current.name == "p":

            element_text = extract_element_with_links(current)
            if element_text and len(element_text.strip()) > 20:  # Meaningful content
                return element_text

        current = current.find_next_sibling()

    return ""
