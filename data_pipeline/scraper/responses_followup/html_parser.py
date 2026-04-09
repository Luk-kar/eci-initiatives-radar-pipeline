"""
HTML parser for extracting Commission response links from initiative pages.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional

from bs4 import BeautifulSoup

from data_pipeline.pipeline_shared.consts import FILE_ENCODING

from ._logger import logger
from .log_messages import LOG_MESSAGES


class ResponseLinkExtractor:
    """Extract Commission response links from responses page HTML files."""

    def extract_links_from_directory(self, base_dir: str) -> List[Dict[str, str]]:
        """Extract all Commission follow-up links from an responses pages directory.

        Args:
            base_dir: Directory containing <year>/<reg_number>.html files.

        Returns:
            List of dicts with 'url', 'year', 'reg_number', 'title'.
        """
        response_links: List[Dict[str, str]] = []
        base_path = Path(base_dir)

        for year_dir in base_path.iterdir():
            if not year_dir.is_dir():
                continue

            for html_file in year_dir.glob("*.html"):
                link_data = self.extract_links_from_file(str(html_file))
                if link_data:
                    response_links.append(link_data)

        logger.info(LOG_MESSAGES["parsing_complete"].format(count=len(response_links)))
        return response_links

    def extract_links_from_file(self, file_path: str) -> Optional[Dict[str, str]]:
        """Extract Commission response link and metadata from a single HTML file.

        Args:
            file_path: Path to an initiative HTML file.

        Returns:
            Dict with 'url', 'year', 'reg_number', 'title', or None if no link found.
        """
        try:
            with open(file_path, "r", encoding=FILE_ENCODING) as f:
                soup = BeautifulSoup(f.read(), "html.parser")

            url = self._extract_response_commission_url(soup)

            if not url:
                return None

            path = Path(file_path)

            return {
                "url": url,
                "year": path.parent.name,
                "reg_number": path.stem.replace("_en", ""),
                "title": self._extract_title(soup),
                "datetime": "",
            }

        except (OSError, ValueError) as e:
            logger.error(f"Error extracting link from {file_path}: {e}")
            return None

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract initiative title from parsed HTML."""
        el = soup.select_one("h1.ecl-page-header-core__title") or soup.find("h1")
        return el.get_text(strip=True) if el else ""

    def _extract_response_commission_url(self, soup: BeautifulSoup) -> Optional[str]:
        """Find the 'Commission's answer and follow-up' anchor href.

        Handles both ASCII apostrophe (') and Unicode right single quotation (').
        """
        link = soup.find(
            "a",
            string=re.compile(r"Commission['\u2019]s answer and follow-up", re.I),
        )

        return link.get("href") if link and link.get("href") else None
