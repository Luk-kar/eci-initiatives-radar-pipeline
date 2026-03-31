# data_pipeline/extractor/responses/parser/fields/followup_details.py
"""
Follow-up details extractor — extracts the dedicated follow-up website (if
present) and the flat list of follow-up events as plain text with links.
"""

import logging
from typing import List, Optional
import re

from bs4 import BeautifulSoup

from .utils import _find_answer_header, _extract_element_with_links

logger = logging.getLogger(__name__)


def extract_followup_additional_website(
    soup: BeautifulSoup, registration_number
) -> Optional[str]:
    """Extract the URL of the dedicated follow-up website for an ECI initiative.

    Searches for anchor tags with href attributes matching the pattern:
    https://.../eci/eci-{identifier}_en

    Note: Other referenced sites have too unpredictable a structure to enable
    reliable and maintainable extraction.

    This pattern identifies official EU Citizens' Initiative dedicated websites
    that provide detailed follow-up information about the initiative.

    Args:
        soup: BeautifulSoup parsed HTML document

    Returns:
        URL string of the dedicated website if found, None otherwise.
        Example return value: "https://ec.europa.eu/info/law/better-regulation/
        initiatives/eci/eci-water_en"

    Raises:
        ValueError: If critical error occurs during URL extraction

    Examples:
        Matching URLs:
        - https://ec.europa.eu/citizens-initiative/initiatives/details/eci/eci-water_en
        - https://example.com/eci/eci-animal-welfare_en

        Non-matching URLs:
        - https://example.com/eci/eci-something_de (wrong language code)
        - https://example.com/citizens-initiative_en (missing "eci-" prefix)
    """
    # Regex pattern explanation:
    # - ^https://     : URL must start with https://
    # - .*eci/        : followed by any characters, then "eci/"
    # - eci-          : literal "eci-" prefix for initiative identifier
    # - [^/]+         : one or more non-slash characters (the initiative ID)
    # - _en$          : ends with "_en" (English language code)
    DEDICATED_WEBSITE_URL_PATTERN = re.compile(
        r"^https://.*eci/eci-[^/]+_en$", re.IGNORECASE
    )

    try:
        # Find all anchor tags with href attributes
        links = soup.find_all("a", href=True)

        # Iterate through links to find matching dedicated website URL
        for link in links:

            href = link.get("href", "").strip()

            # Skip empty or missing hrefs
            if not href:
                continue

            # Check if href matches the dedicated website pattern
            if DEDICATED_WEBSITE_URL_PATTERN.search(href):
                # Return the first matching URL found
                return href

        # No matching dedicated website link found (this is acceptable)
        return None

    except Exception as e:
        raise ValueError(
            f"Error extracting dedicated website URL for {registration_number}: {str(e)}"
        ) from e


def extract_followup_events(
    soup: BeautifulSoup, registration_number: str
) -> Optional[List[str]]:
    """
    Extract follow-up events as a flat list of plain-text descriptions
    with embedded links.

    Args:
        soup:                Parsed BeautifulSoup DOM of the response page.
        registration_number: Used for debug logging.

    Returns:
        List of event description strings, or None if the section is absent.
    """

    try:
        # Step 1: Locate the target section
        response_h2 = _find_answer_header(soup)

        if not response_h2:
            raise ValueError(
                f"No 'Response of the Commission' section found for {registration_number}"
            )

        # Step 2: Find the next h2 that starts the content
        start_h2 = response_h2.find_next(
            lambda tag: tag.name in ("h2", "h4")
            and any(
                phrase in tag.get_text()
                for phrase in ("Follow-up", "Updates on the Commission's proposals")
            )
        )

        if not start_h2:
            logger.warning(
                "⚠️ No content 'Follow-up' section found after 'Response of the Commission' for "
                f"{registration_number}"
            )
            return None

        # Step 3: Extract content elements between start_h2 and stop sections
        stop_section_ids = {"related-links", "press-release", "video"}
        content_elements = []
        current_element = start_h2.find_next()

        while current_element:

            if (
                current_element.name == "h2"
                and "ecl-u-type-heading-2" in current_element.get("class", [])
                and current_element.get("id") in stop_section_ids
            ):
                break

            if current_element.name in ["p", "li"]:

                text = _extract_element_with_links(current_element)

                if text and not _should_skip_text(text):
                    content_elements.append(text)

            current_element = current_element.find_next()

        # Step 4: Normalise and return
        if not content_elements:
            raise ValueError(
                f"No valid follow-up actions found in 'Response of the Commission' section "
                f"for {registration_number}"
            )

        normalized_content = [re.sub(r"\s+", " ", text) for text in content_elements]
        return normalized_content

    except Exception as e:
        raise ValueError(
            f"Error extracting follow-up events for {registration_number}:\n{str(e)}"
        ) from e


def _should_skip_text(text: str) -> bool:
    """
    Determine if text should be skipped (generic intro or subsection header).

    Args:
        text: Text content to check

    Returns:
        True if text should be skipped, False otherwise
    """

    skip_patterns = [
        "provides regularly updated information",
        "provides information on the follow-up",
        "this section provides",
    ]

    text_lower = text.lower()

    for pattern in skip_patterns:

        if pattern in text_lower:
            return True

    # Also skip if it's just a subsection header (ends with colon)
    if text.endswith(":"):
        return True
