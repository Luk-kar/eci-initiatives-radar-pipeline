"""
ECI initiatives extractor.

Discovers all initiative HTML files under the initiatives directory,
delegates parsing to parser.py, and writes results to a CSV file.
"""

import csv
import logging
from pathlib import Path

from data_pipeline.extractor.initiatives.parser import parse_initiative_page

logger = logging.getLogger(__name__)

INITIATIVES_CSV_COLUMNS = [
    "registration_number",
    "title",
    "objective",
    "annex",
    "current_status",
    "url",
    "timeline_registered",
    "timeline_collection_start_date",
    "timeline_collection_closed",
    "timeline_response_commission_date",
    "timeline",
    "funding_total",
    "signatures_collected",
    "signatures_collected_by_country",
    "signatures_threshold_met",
    "response_commission_url",
]


def _find_html_files(initiatives_dir: Path) -> list[Path]:
    """
    Walk year subdirectories under initiatives_dir and collect all HTML files.

    Expected layout:
        initiatives_dir/
            {year}/
                {year}_{number}.html
                ...
    """
    if not initiatives_dir.exists():
        logger.warning("Initiatives directory not found: %s", initiatives_dir)
        return []

    html_files = [
        html_file
        for year_dir in sorted(initiatives_dir.iterdir())
        if year_dir.is_dir() and year_dir.name.isdigit() and len(year_dir.name) == 4
        for html_file in sorted(year_dir.glob("*.html"))
    ]

    logger.info("Found %d initiative HTML files", len(html_files))
    return html_files


def extract_initiatives(initiatives_dir: Path, output_csv: Path) -> None:
    """
    Parse all initiative HTML files and write extracted data to a CSV.

    Args:
        initiatives_dir: Directory containing year-partitioned HTML files.
        output_csv:      Destination CSV path.
    """
    html_files = _find_html_files(initiatives_dir)
    output_csv.parent.mkdir(parents=True, exist_ok=True)

    rows_written = 0
    rows_failed = 0

    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=INITIATIVES_CSV_COLUMNS)
        writer.writeheader()

        for html_file in html_files:
            logger.debug("Parsing: %s", html_file)
            try:
                parsed = parse_initiative_page(html_file)
                writer.writerow(
                    {col: parsed.get(col, "") for col in INITIATIVES_CSV_COLUMNS}
                )
                rows_written += 1
            except Exception:
                logger.exception("Failed to parse: %s", html_file)
                rows_failed += 1

    logger.info("Wrote %d rows to %s", rows_written, output_csv)
    if rows_failed:
        logger.warning("Failed to parse %d file(s)", rows_failed)
