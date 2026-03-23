"""
ECI initiatives extractor.

Discovers all initiative HTML files under the initiatives directory,
delegates parsing to parser.py, and writes results to a CSV file.
"""

import logging
from pathlib import Path

from ..extractor_shared.extractor import extract_html_to_csv
from .parser import parse_initiative_page

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


def extract_initiatives(source_dir: Path, output_csv: Path) -> None:
    """
    Parse all initiative HTML files and write extracted data to a CSV.

    Wraps ``extract_html_to_csv`` with the initiatives-specific column
    schema and parser defined by ``INITIATIVES_CSV_COLUMNS`` and
    ``parse_initiative_page``.

    Args:
        source_dir:  Directory containing year-partitioned HTML files.
        output_csv:  Destination CSV path.
    """
    extract_html_to_csv(
        source_dir, output_csv, INITIATIVES_CSV_COLUMNS, parse_initiative_page
    )
