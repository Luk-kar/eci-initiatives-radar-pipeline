"""
Commission answer extractor — extracts the full text of the Commission's
response to the ECI, preserving inline hyperlinks as plain text with URLs.
"""

import logging
from typing import Optional

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class CommissionAnswerExtractor:
    """Extracts the Commission's answer text from the response HTML."""

    def extract(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Extract the full Commission answer text from the parsed HTML.

        Args:
            soup: Parsed BeautifulSoup DOM of the response page.

        Returns:
            Full answer text with inline links preserved, or None if the
            section is not found.
        """
        # TODO: implement — locate the Commission answer section in the DOM
        #       and extract text, preserving hyperlinks as plain text with URLs
        logger.debug(
            f"[{self.registration_number}] CommissionAnswerExtractor: not yet implemented"
        )
        return None
