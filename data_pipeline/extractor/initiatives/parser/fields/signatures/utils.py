from typing import Optional, List, Tuple

from bs4 import BeautifulSoup


def find_signatures_table(soup: BeautifulSoup) -> Optional[BeautifulSoup]:
    """Find the signatures table with zebra styling."""
    signatures_table = soup.find(
        "table", class_="ecl-table ecl-table--zebra ecl-u-type-paragraph"
    )
    if not signatures_table:
        signatures_table = soup.find("table", class_="ecl-table")
    return signatures_table


def get_signature_table_rows(
    soup: BeautifulSoup, skip_total: bool = True
) -> List[Tuple[str, str, str, str]]:
    """Extract rows from the signature collection table.

    Each row contains country name, number of signatures, required threshold,
    and percentage achieved.

    Args:
        soup: BeautifulSoup parsed HTML document.
        skip_total: If True, exclude the "Total number of signatories" summary row.

    Returns:
        List of tuples (country_name, signatures_count, threshold_required,
        percentage_achieved).
    """
    signatures_table = find_signatures_table(soup)
    if not signatures_table:
        return []

    country_data: List[Tuple[str, str, str, str]] = []
    table_rows = signatures_table.find_all("tr", class_="ecl-table__row")

    for row in table_rows:
        cells = row.find_all("td", class_="ecl-table__cell")
        if len(cells) != 4:
            continue

        country_name = cells[0].get_text().strip()

        if skip_total and "total number of signatories" in country_name.lower():
            continue
        if not country_name:
            continue

        signatures_count = cells[1].get_text().strip()
        threshold_required = cells[2].get_text().strip()
        percentage_achieved = cells[3].get_text().strip()

        country_data.append(
            (country_name, signatures_count, threshold_required, percentage_achieved)
        )

    return country_data
