from typing import Optional, List, Tuple
import logging
import re

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def extract_signatures_threshold_met(soup: BeautifulSoup) -> Optional[str]:
    """
    Extract number of countries with threshold met (percentage >= 100%)
    Uses common inner function to extract signature table data
    """
    try:
        # Get all rows from signature table
        rows_data = get_signature_table_rows(soup, skip_total=True)

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

        logger.error(f"Error extracting threshold met countries: {str(e)}")
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
