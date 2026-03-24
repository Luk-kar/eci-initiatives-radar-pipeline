from pathlib import Path
import logging
from typing import Optional, List, Tuple
import json

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def extract_signatures_by_country(
    soup: BeautifulSoup, file_path: Path, title: str, url: str
) -> Optional[str]:
    """Extract country-level signature data as JSON using common function"""

    try:
        # Use common function to get table rows
        rows_data = get_signature_table_rows(soup, skip_total=True)

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
        logger.error(
            f"Error serializing country data to JSON - "
            f"URL: {url}, Initiative: {title}, File: {file_path.name}, "
            f"Error: {str(e)}"
        )

    return None


def find_signatures_table(soup: BeautifulSoup) -> Optional[BeautifulSoup]:
    """Common inner function to find the signatures table with zebra styling"""
    # Look for table with specific classes
    signatures_table = soup.find(
        "table", class_="ecl-table ecl-table--zebra ecl-u-type-paragraph"
    )

    # Fallback to basic ecl-table if not found
    if not signatures_table:
        signatures_table = soup.find("table", class_="ecl-table")

    return signatures_table


def get_signature_table_rows(
    soup: BeautifulSoup, skip_total: bool = True
) -> List[Tuple]:
    """
    Extract rows from the signature collection table.

    Each row contains: country name, number of signatures, required threshold, and percentage achieved.

    Args:
        soup: BeautifulSoup parsed HTML document
        skip_total: If True, exclude the "Total number of signatories" summary row

    Returns:
        List of tuples, each containing (country_name, signatures_count, threshold_required, percentage_achieved)
    """

    # Find the signatures table in the HTML
    signatures_table = find_signatures_table(soup)
    if not signatures_table:
        return []

    # Store extracted data from each country row
    country_data = []

    # Find all table rows in the signatures table
    table_rows = signatures_table.find_all("tr", class_="ecl-table__row")

    for row in table_rows:

        cells = row.find_all("td", class_="ecl-table__cell")

        # Validate that row has exactly 4 columns (country, signatures, threshold, percentage)
        if len(cells) != 4:
            continue

        # Extract the country name from the first column
        country_name = cells[0].get_text().strip()

        # Skip the total summary row if requested
        if skip_total and "total number of signatories" in country_name.lower():
            continue

        # Skip rows with empty country names
        if not country_name:
            continue

        # Extract signature collection data from the remaining columns
        signatures_count = cells[1].get_text().strip()
        threshold_required = cells[2].get_text().strip()
        percentage_achieved = cells[3].get_text().strip()

        # Add this country's data to our results
        country_data.append(
            (
                country_name,
                signatures_count,
                threshold_required,
                percentage_achieved,
            )
        )

    return country_data
