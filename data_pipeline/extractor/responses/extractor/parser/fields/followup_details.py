# data_pipeline/extractor/responses/parser/fields/followup_details.py
"""
Follow-up details extractor — extracts the dedicated follow-up website (if
present) and the flat list of follow-up events as plain text with links.
"""

import logging
from typing import List, Optional
import re

from bs4 import BeautifulSoup

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
    # TODO: implement — locate and iterate the follow-up events list in the DOM
    logger.debug(
        f"[{registration_number}] extract_followup_events: not yet implemented"
    )
    return None
