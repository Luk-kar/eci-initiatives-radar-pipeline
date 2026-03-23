from pathlib import Path
from typing import Optional
from bs4 import BeautifulSoup


def extract_signatures_by_country(
    self, soup: BeautifulSoup, file_path: Path, title: str, url: str
) -> Optional[str]:
    """Extract country-level signature data as JSON using common function"""

    try:
        # Use common function to get table rows
        rows_data = self._get_signature_table_rows(soup, skip_total=True)

        if not rows_data:
            return None

        country_data = {}

        for country_text, statements_of_support, threshold, percentage in rows_data:
            # Check for missing data and log warnings
            missing_fields = []
            if not statements_of_support:
                missing_fields.append("statements_of_support")
            if not threshold:
                missing_fields.append("threshold")
            if not percentage:
                missing_fields.append("percentage")

            if missing_fields:
                self.logger.warning(
                    f"Missing signature data - Country: {country_text}, "
                    f"URL: {url}, Initiative: {title}, File: {file_path.name}, "
                    f"Missing fields: {', '.join(missing_fields)}"
                )

            # Add country data (even if some fields are missing)
            country_data[country_text] = {
                "statements_of_support": statements_of_support,
                "threshold": threshold,
                "percentage": percentage,
            }

        # Return JSON string if we have data
        if country_data:
            return json.dumps(country_data, ensure_ascii=False, separators=(",", ":"))

    except Exception as e:
        self.logger.error(
            f"Error serializing country data to JSON - "
            f"URL: {url}, Initiative: {title}, File: {file_path.name}, "
            f"Error: {str(e)}"
        )

    return None
