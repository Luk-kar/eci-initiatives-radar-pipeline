from typing import Optional
from bs4 import BeautifulSoup


def extract_signatures_collected(self, soup: BeautifulSoup) -> Optional[str]:
    """
    Extract the total number of signatures collected for the initiative.

    This function attempts to find the total signature count using two methods:
    1. Primary: Searches for the "Total number of signatories" row in the signatures table
    2. Fallback: Looks for a standalone counter element on the page

    Note:
        The returned string preserves commas for readability but removes spaces.
        This matches the format displayed on the ECI website.
    """

    # Use common function to get table
    signatures_table = self._find_signatures_table(soup)

    if signatures_table:

        # Find all table rows
        rows = signatures_table.find_all("tr", class_="ecl-table__row")

        for row in rows:

            first_cell = row.find("td", class_="ecl-table__cell")
            if (
                first_cell
                and "total number of signatories" in first_cell.get_text().lower()
            ):

                cells = row.find_all("td", class_="ecl-table__cell")

                if len(cells) >= 2:

                    # Second cell contains the number
                    signatures_text = cells[1].get_text().strip()
                    if signatures_text and re.match(r"^[\d,\s]+$", signatures_text):
                        return signatures_text.replace(
                            " ", ""
                        )  # Keep commas for readability

    # Fallback to original counter method
    signatures_element = soup.find(class_="ecl-counter__value")

    if signatures_element:
        signatures_text = signatures_element.get_text().strip()
        numbers = re.findall(r"\d+", signatures_text.replace(",", "").replace(" ", ""))

        if numbers:
            return "".join(numbers)

    return None
