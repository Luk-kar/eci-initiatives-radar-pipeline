# data_pipeline/extractor/responses/parser/fields/commission_answer.py
"""
Commission answer extractor — extracts the full text of the Commission's
response to the ECI, preserving inline hyperlinks as plain text with URLs.
"""

import logging
from typing import Optional
import re

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def extract_commission_answer(
    soup: BeautifulSoup, registration_number: str
) -> Optional[str]:
    """Extract main conclusions text from Communication, excluding factsheet downloads

    If the Answer section contains insufficient content (only decision date and document links),
    extract one additional paragraph from the Follow-up section.

    Raises:
        ValueError: If the Commission answer section cannot be found or extracted
    """

    # Find the "Answer of the European Commission" header
    answer_header = soup.find("h2", id="Answer-of-the-European-Commission")

    if not answer_header:

        # Alternative: find h2 containing the text
        answer_header = soup.find(
            lambda tag: tag.name == "h2"
            and "Answer of the European Commission" in tag.get_text()
        )

    if not answer_header:
        raise ValueError(
            "Could not find 'Answer of the European Commission' section for "
            f"{registration_number}"
        )

    # Collect all content between this header and the Follow-up header
    content_parts = []
    current = answer_header.find_next_sibling()
    followup_header = None

    while current:

        # Stop if we hit Follow-up or another major section
        if current.name == "h2":

            h2_id = current.get("id", "")
            h2_text = current.get_text(strip=True)
            if "Follow-up" in h2_text or h2_id == "Follow-up":
                followup_header = current
                break

            # Also stop at other major sections
            if h2_id and h2_id != "Answer-of-the-European-Commission":
                break

        if current.name == "h4":
            h4_text = current.get_text(strip=True)
            if "Follow-up" in h4_text:
                break

        # Skip factsheet file download components (ecl-file divs)
        if current.name == "div" and "ecl-file" in current.get("class", []):
            current = current.find_next_sibling()
            continue

        # Skip <ul> elements that only contain document links (Communication, Annex, etc.)
        if current.name == "ul" and _is_document_links_list(current):
            current = current.find_next_sibling()
            continue

        # Extract and format content from this element
        if current.name:
            element_text = _extract_element_with_links(current)
            if element_text:
                content_parts.append(element_text)

        current = current.find_next_sibling()

    if not content_parts:
        raise ValueError(
            "No content found in 'Answer of the European Commission' section for "
            f"{registration_number}"
        )

    # Check if content is insufficient (likely only decision date and document links)
    combined_text = "\n".join(content_parts).strip()

    # Heuristic: if the content is very short and contains only common patterns,
    # it's likely insufficient
    if _is_answer_insufficient(combined_text):
        # Try to extract one paragraph from Follow-up section
        if followup_header:
            followup_paragraph = _extract_first_followup_paragraph(followup_header)
            if followup_paragraph:
                content_parts.append(followup_paragraph)
                combined_text = "\n".join(content_parts).strip()

    return combined_text


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


def _is_answer_insufficient(text: str) -> bool:
    """Check if extracted answer text is insufficient.

    Answer is considered insufficient if it's very short and only contains:
    - Decision date
    - Document links or references

    Args:
        text: The extracted answer text

    Returns:
        True if answer is insufficient, False otherwise
    """
    # Remove whitespace and newlines for analysis
    normalized = re.sub(r"\s+", " ", text).strip()

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
            element_text = _extract_element_with_links(current)
            if element_text and len(element_text.strip()) > 20:  # Meaningful content
                return element_text

        current = current.find_next_sibling()

    return ""
