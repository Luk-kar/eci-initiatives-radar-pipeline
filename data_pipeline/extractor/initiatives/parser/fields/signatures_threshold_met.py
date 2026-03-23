from typing import Optional
from bs4 import BeautifulSoup


def extract_signatures_threshold_met(self, soup: BeautifulSoup) -> Optional[str]:
    """
    Extract number of countries with threshold met (percentage >= 100%)
    Uses common inner function to extract signature table data
    """
    try:
        # Get all rows from signature table
        rows_data = self._get_signature_table_rows(soup, skip_total=True)

        if not rows_data:
            return None

        # Count countries with percentage >= 100%
        countries_met_threshold = 0

        for country, statements, threshold, percentage in rows_data:

            # Extract numeric percentage value
            percentage_match = re.search(r"([\d.]+)%", percentage)

            if percentage_match:

                percentage_value = float(percentage_match.group(1))

                if percentage_value >= 100.0:
                    countries_met_threshold += 1

        return str(countries_met_threshold) if countries_met_threshold > 0 else "0"

    except Exception as e:

        self.logger.error(f"Error extracting threshold met countries: {str(e)}")
        return None
