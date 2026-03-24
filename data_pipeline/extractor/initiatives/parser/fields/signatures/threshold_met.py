import logging
import re
from typing import Optional

from bs4 import BeautifulSoup

from .utils import get_signature_table_rows

logger = logging.getLogger(__name__)


def extract_signatures_threshold_met(soup: BeautifulSoup) -> Optional[str]:
    """Extract number of countries with threshold met (percentage >= 100)."""
    try:
        rows_data = get_signature_table_rows(soup, skip_total=True)
        if not rows_data:
            return None

        countries_met_threshold = 0
        for _country, _statements, _threshold, percentage in rows_data:
            percentage_match = re.search(r"([\d.]+)", percentage)
            if percentage_match:
                percentage_value = float(percentage_match.group(1))
                if percentage_value >= 100.0:
                    countries_met_threshold += 1

        return str(countries_met_threshold)

    except Exception as e:
        logger.error(f"Error extracting threshold met countries: {str(e)}")

    return None
