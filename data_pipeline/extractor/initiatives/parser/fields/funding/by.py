import json
import logging
import re
from pathlib import Path
from typing import Optional

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def extract_funding_by(
    soup: BeautifulSoup, filepath: Path, title: str, url: str
) -> Optional[str]:
    """Extract funding sponsors data as JSON."""

    funding_tables = soup.find_all("table", class_="ecl-table")
    funding_table = None

    for table in funding_tables:

        headers = table.find_all("th", class_="ecl-table__header")
        header_texts = " ".join(h.get_text().strip().lower() for h in headers)

        if "name of sponsor" in header_texts and "amount in eur" in header_texts:
            funding_table = table
            break

    if not funding_table:
        return None

    sponsors_data = []
    rows = funding_table.find_all("tr", class_="ecl-table__row")

    for row in rows:
        cells = row.find_all("td", class_="ecl-table__cell")
        if len(cells) != 3:
            continue

        sponsor_name = cells[0].get_text().strip()
        date = cells[1].get_text().strip()
        amount = cells[2].get_text().strip()

        missing_fields = []
        if not sponsor_name:
            missing_fields.append("name_of_sponsor")

        if not date:
            missing_fields.append("date")

        if not amount:
            missing_fields.append("amount_in_eur")

        if missing_fields:

            logger.warning(
                f"Missing funding data - Sponsor: {sponsor_name or 'UNKNOWN'}, "
                f"URL: {url}, Initiative: {title}, File: {filepath.name}, "
                f"Missing fields: {', '.join(missing_fields)}"
            )

        clean_sponsor_name = re.sub(r"<sup.?</sup>", "", sponsor_name)
        clean_sponsor_name = re.sub(r"\*+", "", clean_sponsor_name).strip()

        sponsor_entry = {
            "name_of_sponsor": clean_sponsor_name,
            "date": date,
            "amount_in_eur": amount,
        }
        sponsors_data.append(sponsor_entry)

    return (
        json.dumps(sponsors_data, ensure_ascii=False, separators=(",", ":"))
        if sponsors_data
        else None
    )
