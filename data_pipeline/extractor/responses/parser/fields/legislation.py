"""
Legislation passed extractor — extracts all laws that have been adopted or
entered into force, as a flat list of plain-text descriptions.
"""

import logging
from typing import List, Optional

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class LegislationPassedExtractor:
    """Extracts passed/enacted legislation entries from the response HTML."""

    def extract(self, soup: BeautifulSoup) -> Optional[List[str]]:
        """
        Extract all legislation passed entries from the parsed HTML.

        Args:
            soup: Parsed BeautifulSoup DOM of the response page.

        Returns:
            List of plain-text law descriptions, or None if no legislation
            section is found.
        """
        # TODO: implement — locate legislation section(s) in the DOM,
        #       collect all adopted/entered-into-force law entries as plain text
        logger.debug(
            f"[{self.registration_number}] LegislationPassedExtractor: not yet implemented"
        )
        return None
