"""
Follow-up details extractor — extracts the dedicated follow-up website (if
present) and the flat list of follow-up events as plain text with links.
"""

import logging
from typing import List, Optional

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class FollowUpDetailsExtractor:
    """Extracts follow-up section data from the response HTML."""

    def extract_additional_website(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Extract the dedicated follow-up website URL, if present.

        Args:
            soup: Parsed BeautifulSoup DOM of the response page.

        Returns:
            URL string of the follow-up website, or None if absent.
        """
        # TODO: implement — locate the follow-up website link in the DOM
        logger.debug(
            f"[{self.registration_number}] FollowUpDetailsExtractor.extract_additional_website: not yet implemented"
        )
        return None

    def extract_events(self, soup: BeautifulSoup) -> Optional[List[str]]:
        """
        Extract follow-up events as a flat list of plain-text descriptions
        with embedded links.

        Args:
            soup: Parsed BeautifulSoup DOM of the response page.

        Returns:
            List of event description strings, or None if the section is absent.
        """
        # TODO: implement — locate and iterate the follow-up events list in the DOM
        logger.debug(
            f"[{self.registration_number}] FollowUpDetailsExtractor.extract_events: not yet implemented"
        )
        return None
