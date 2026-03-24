from pathlib import Path
from typing import Optional
from bs4 import BeautifulSoup


def extract_funding_by(
    soup: BeautifulSoup, file_path: Path, title: str, url: str
) -> Optional[str]:
    """Extract funding sponsors data as JSON"""

    # Find funding table - look for table with sponsor headers
    funding_tables = soup.find_all("table", class_="ecl-table")
    funding_table = None

    for table in funding_tables:
        headers = table.find_all("th", class_="ecl-table__header")
        header_texts = [h.get_text().strip().lower() for h in headers]

        # Check if this is the funding table by looking for expected headers
        if "name of sponsor" in " ".join(header_texts) and "amount in eur" in " ".join(
            header_texts
        ):
            funding_table = table
            break

    if not funding_table:
        return None

    sponsors_data = []

    # Extract table rows (skip header)
    rows = funding_table.find_all("tr", class_="ecl-table__row")

    for row in rows:
        cells = row.find_all("td", class_="ecl-table__cell")

        if len(cells) != 3:  # Should have 3 cells: Name, Date, Amount
            continue

        sponsor_name = cells[0].get_text().strip()
        date = cells[1].get_text().strip()
        amount = cells[2].get_text().strip()

        # Check for missing data and log warnings
        missing_fields = []
        if not sponsor_name:
            missing_fields.append("name_of_sponsor")
        if not date:
            missing_fields.append("date")
        if not amount:
            missing_fields.append("amount_in_eur")

        if missing_fields:
            self.logger.warning(
                f"Missing funding data - Sponsor: {sponsor_name or 'UNKNOWN'}, "
                f"URL: {url}, Initiative: {title}, File: {file_path.name}, "
                f"Missing fields: {', '.join(missing_fields)}"
            )

        # Clean sponsor name (remove superscript references)
        clean_sponsor_name = re.sub(r"<sup>.*?</sup>", "", sponsor_name)
        clean_sponsor_name = re.sub(r"\s*\[\d+\]\s*", "", clean_sponsor_name).strip()

        # Add sponsor data (even if some fields are missing)
        sponsor_entry = {
            "name_of_sponsor": clean_sponsor_name,
            "date": date,
            "amount_in_eur": amount,
        }

        sponsors_data.append(sponsor_entry)
