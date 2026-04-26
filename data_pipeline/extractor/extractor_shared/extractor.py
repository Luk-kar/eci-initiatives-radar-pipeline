"""
Shared HTML-to-CSV extraction utilities for data pipeline extractor modules.
...
"""

import csv
import logging
from pathlib import Path
from typing import Protocol

from .errors import HTMLParseError
from data_pipeline.pipeline_shared.consts import FILE_ENCODING
from data_pipeline.pipeline_shared.sort import (
    sort_by_registration_number,
)

logger = logging.getLogger(__name__)


class HTMLParserProtocol(Protocol):
    """Structural interface required by ``extract_html_to_csv``."""

    csv_columns: list[str]

    def parse(self, html_file: Path) -> dict:
        """Parse a single HTML file and return a column-keyed dict."""
        ...


def _find_html_files(source_dir: Path) -> list[Path]:
    """
    Walk year subdirectories under source_dir and collect all non-empty HTML
    files.

    Expected layout:
        source_dir/
            {year}/
                {year}_{number}.html
                ...
    """

    if not source_dir.exists():
        logger.warning("Directory not found: %s", source_dir)
        return []

    html_files = [
        html_file
        for year_dir in sorted(source_dir.iterdir())
        if year_dir.is_dir() and year_dir.name.isdigit() and len(year_dir.name) == 4
        for html_file in sorted(year_dir.glob("*.html"))
        if html_file.stat().st_size > 0
    ]

    logger.info("Found %d HTML files", len(html_files))
    return html_files


def _parse_html_files(
    html_files: list[Path],
    parser: HTMLParserProtocol,
) -> list[dict]:
    """
    Parse each HTML file via ``parser`` and return the resulting rows in a list.

    Raises:
        HTMLParseError: If ``parser.parse`` raises for any HTML file;
                        the original exception is chained via ``__cause__``.
    """

    rows: list[dict] = []

    for html_file in html_files:
        logger.debug("Parsing: %s", html_file)

        try:
            parsed = parser.parse(html_file)
            rows.append({col: parsed.get(col, "") for col in parser.csv_columns})
        except Exception as exc:
            logger.exception("Failed to parse: %s", html_file)
            raise HTMLParseError(f"Failed to parse: {html_file}") from exc

    return rows


def _write_rows_to_csv(
    output_csv: Path,
    rows: list[dict],
    parser: HTMLParserProtocol,
) -> int:
    """Open *output_csv* and write *rows* using the parser's column schema."""

    with open(output_csv, "w", newline="", encoding=FILE_ENCODING) as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=parser.csv_columns)
        writer.writeheader()
        writer.writerows(rows)

    return len(rows)


def extract_html_to_csv(
    source_dir: Path,
    output_csv: Path,
    parser: HTMLParserProtocol,
) -> None:
    """
    Parse all HTML files under source_dir and write extracted data to a CSV,
    ordered by ``registration_number`` (earliest → latest).

    Args:
        source_dir: Directory containing year-partitioned HTML files.
        output_csv: Destination CSV path.
        parser:     Object implementing ``HTMLParserProtocol`` — supplies both
                    the column schema (``parser.csv_columns``) and the
                    per-file parse logic (``parser.parse``).

    Raises:
        FileNotFoundError: If no HTML files are found under ``source_dir``.
        HTMLParseError:    If ``parser.parse`` raises for any HTML file;
                           the original exception is chained via ``__cause__``.
    """

    html_files = _find_html_files(source_dir)

    if not html_files:
        raise FileNotFoundError(f"No HTML files found in: {source_dir}")

    output_csv.parent.mkdir(parents=True, exist_ok=True)

    rows = _parse_html_files(html_files, parser)
    sorted_rows = sort_by_registration_number(rows)

    rows_written = _write_rows_to_csv(output_csv, sorted_rows, parser)

    logger.info("Wrote %d rows to %s", rows_written, output_csv)
