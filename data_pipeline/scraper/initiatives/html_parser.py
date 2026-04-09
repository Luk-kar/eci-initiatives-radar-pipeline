"""
HTML parsing module for extracting ECI initiative data.

This module processes raw HTML content saved from the scraper,
locating initiative listings, parsing relative URLs into absolute ones,
and structuring the extracted data into lists of dictionaries for
downstream processing and storage.
"""

# Python Standard Library
import re
from typing import Dict

# Third-party
from bs4 import BeautifulSoup

# Local
from .css_selectors import ECIlistingSelectors
from ._logger import logger
from .log_messages import LOG_MESSAGES


def parse_initiatives_list_data(
    page_source: str, base_url: str
) -> list[Dict[str, str]]:
    """Parse HTML page source and extract initiatives data."""

    logger.info(LOG_MESSAGES["parsing_listing"])

    soup = BeautifulSoup(page_source, "html.parser")
    initiative_data: list[Dict[str, str]] = []

    for content_block in soup.select(ECIlistingSelectors.CONTENT_BLOCKS):

        title_link = content_block.select_one(ECIlistingSelectors.INITIATIVE_CARDS)
        if not title_link or not title_link.get("href"):
            continue

        href = title_link.get("href")
        if not href.startswith("/initiatives/details/"):
            continue

        full_url = base_url + href

        current_status = ""
        registration_number = ""
        signature_collection = ""

        meta_labels = content_block.select(ECIlistingSelectors.META_LABELS)

        for label in meta_labels:
            text = label.get_text(strip=True)

            if text.startswith("Current status:"):
                current_status = text.replace("Current status:", "").strip()

            elif text.startswith("Registration number:"):
                raw = text.replace("Registration number:", "").strip()
                registration_number = re.sub(r"^ECI\((\d{4})\)(\d+)$", r"\1/\2", raw)

            elif "signature collection" in text.lower():
                signature_collection = text.strip()

        initiative_data.append(
            {
                "url": full_url,
                "current_status": current_status,
                "registration_number": registration_number,
                "signature_collection": signature_collection,
                "datetime": "",
            }
        )

    logger.info(LOG_MESSAGES["parsing_complete"].format(count=len(initiative_data)))
    return initiative_data
