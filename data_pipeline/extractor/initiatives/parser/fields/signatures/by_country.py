import json
import logging
from pathlib import Path
from typing import Optional

from bs4 import BeautifulSoup

from .utils import get_signature_table_rows

logger = logging.getLogger(__name__)


def extract_signatures_by_country(
    soup: BeautifulSoup, filepath: Path, title: str, url: str
) -> Optional[str]:
    """Extract country-level signature data as JSON."""

    try:

        rows_data = get_signature_table_rows(soup, skip_total=True)
        if not rows_data:
            return None

        country_data = {}

        for country_text, signatures, threshold, percentage in rows_data:

            missing_fields = []

            if not signatures:
                missing_fields.append("signatures")
            if not threshold:
                missing_fields.append("threshold")
            if not percentage:
                missing_fields.append("percentage")

            if missing_fields:
                logger.warning(
                    f"Missing signature data - Country: {country_text}, "
                    f"URL: {url}, Initiative: {title}, File: {filepath.name}, "
                    f"Missing fields: {', '.join(missing_fields)}"
                )

            country_data[country_text] = {
                "signatures": signatures,
                "threshold": threshold,
                "percentage": percentage,
            }

        if country_data:
            return json.dumps(country_data, ensure_ascii=False, separators=(",", ":"))

    except Exception as e:
        logger.error(
            f"Error serializing country data to JSON - "
            f"URL: {url}, Initiative: {title}, File: {filepath.name}, "
            f"Error: {str(e)}"
        )

    return None
