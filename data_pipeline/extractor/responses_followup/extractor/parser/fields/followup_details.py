"""
Follow-up details extractor — extracts the dedicated follow-up website (if
present) and the flat list of follow-up events as plain text with links.
"""

import logging
from typing import List, Optional, Dict, Union
import re


from bs4 import BeautifulSoup, Tag


from .utils import (
    find_answer_header,
    extract_element_with_links,
)


logger = logging.getLogger(__name__)


def extract_followup_events(
    soup: BeautifulSoup,
    registration_number: str,
) -> Optional[List[Dict[str, Union[List[str], str]]]]:
    """
    Extract follow-up actions with associated dates from after the
    'Response of the Commission' section.

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
        List of dictionaries with structure:
            [
                {
                    "dates": ["2020-01-01", "2021-01-01"],
                    "action": "Following up on its commitment..."
                },
                ...
            ]
        Returns None if no Response of the Commission section exists or
        no valid actions are found.

    Raises:
        ValueError: If a critical error occurs during extraction.
    """
    try:
        # Step 1: Locate the 'Response of the Commission' h2
        response_h2 = soup.find("h2", id="response-of-the-commission")
        if not response_h2:
            raise ValueError(
                f"No 'Response of the Commission' section found for "
                f"{registration_number}"
            )

        # Step 2: Find the first follow-up section h2 directly after the response
        start_h2 = response_h2.find_next("h2", class_="ecl-u-type-heading-2")
        if not start_h2:
            raise ValueError(
                f"No content section found after 'Response of the Commission' "
                f"for {registration_number}"
            )

        # IDs of h2 sections that signal the end of follow-up content
        stop_section_ids = {"related-links", "press-release", "video"}

        # Step 3: Validate that the first follow-up h2 is not itself a stop section
        if start_h2.get("id") in stop_section_ids:
            raise ValueError(
                f"No follow-up content section found after 'Response of the "
                f"Commission' for {registration_number}"
            )

        # Step 4: Traverse the document from start_h2 onward in depth-first order,
        #         collecting leaf <p> and <li> elements from all follow-up sections
        #         until a stop section or "Share this page" marker is reached.
        content_elements: List[str] = []
        current = start_h2.find_next()

        while current:
            # Stop when the next section-level h2 is a stop section
            if current.name == "h2" and "ecl-u-type-heading-2" in current.get(
                "class", []
            ):
                if current.get("id") in stop_section_ids:
                    break
                # Non-stop h2 (e.g. "Supporting measures") — continue collecting

            # Stop on the social-share "Share this page" paragraph
            if current.name == "p" and "Share this page" in current.get_text(
                strip=True
            ):
                break

            # Collect leaf-level <p> and <li> elements only.
            # Skipping elements whose immediate parent is also <p> or <li>
            # prevents duplicate text from nested structures (e.g. <li><p>…</p></li>).
            if current.name in ("p", "li"):
                parent_name = current.parent.name if current.parent else ""
                if parent_name not in ("p", "li"):
                    text = extract_element_with_links(current)
                    if text and not should_skip_text(text):
                        content_elements.append(text)

            current = current.find_next()

        # Step 5: Build and return the structured result
        if not content_elements:
            raise ValueError(
                f"No valid follow-up actions found after 'Response of the "
                f"Commission' for {registration_number}"
            )

        followup_actions = []
        for element_text in content_elements:
            normalized = re.sub(r"\s+", " ", element_text).strip()
            followup_actions.append(normalized)

        return followup_actions

    except Exception as e:
        raise ValueError(
            f"Error extracting follow-up events with dates for "
            f"{registration_number}: {str(e)}"
        ) from e


_SKIP_PHRASES: frozenset = frozenset(
    {
        "share this page",
        "search for available translations",
    }
)


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
