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
    """Extract Commission response links from initiative page HTML files."""

    def extract_links_from_directory(self, base_dir: str) -> List[Dict[str, str]]:
        """Extract all Commission response links from an initiative pages directory.

        Args:
            base_dir: Directory containing <year>/<reg_number>_en.html files.

        Returns:
            List of dicts with 'url', 'year', 'reg_number', 'title'.
        """
        response_links: List[Dict[str, str]] = []
        base_path = Path(base_dir)

        for year_dir in base_path.iterdir():
            if not year_dir.is_dir():
                continue

            for html_file in year_dir.glob("*_en.html"):
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
                html_content = f.read()

            soup = BeautifulSoup(html_content, "html.parser")
            url = self._extract_response_commission_url(soup)

            if not url:
                return None

            metadata = self._extract_metadata_from_path(file_path)

            return {
                "url": url,
                "year": metadata["year"],
                "reg_number": metadata["reg_number"],
                "title": self._extract_title(soup),
                "datetime": "",
            }

        except Exception as e:
            logger.error(f"Error extracting link from {file_path}: {e}")
            return None

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract initiative title from parsed HTML."""
        title_el = soup.select_one("h1.ecl-page-header-core__title")
        if title_el:
            return title_el.get_text(strip=True)

        h1 = soup.find("h1")
        return h1.get_text(strip=True) if h1 else ""

    def _extract_metadata_from_path(self, file_path: str) -> Dict[str, str]:
        """Extract year and registration number from file path.

        E.g. initiatives/2019/000007_en.html → year='2019', reg_number='000007'
        """
        path = Path(file_path)
        return {
            "year": path.parent.name,
            "reg_number": path.stem.replace("_en", ""),
        }

    def _extract_response_commission_url(self, soup: BeautifulSoup) -> Optional[str]:
        """Find the 'Commission's answer and follow-up' anchor href.

        Handles both ASCII apostrophe (') and Unicode right single quotation (').
        """
        link = soup.find(
            "a",
            string=re.compile(r"Commission['\u2019]s answer and follow-up", re.I),
        )

        if link and link.get("href"):
            return link.get("href")

        return None
