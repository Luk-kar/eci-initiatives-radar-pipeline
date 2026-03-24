"""
Shared HTML-to-CSV extraction utilities for data pipeline extractor modules.
...
"""

import csv
import logging
from pathlib import Path
from typing import Protocol

from .errors import HTMLParseError

logger = logging.getLogger(__name__)


class HTMLParserProtocol(Protocol):
    """Structural interface required by ``extract_html_to_csv``."""

    csv_columns: list[str]

    def parse(self, html_file: Path) -> dict:
        """Parse a single HTML file and return a column-keyed dict."""
        ...


def _find_html_files(source_dir: Path) -> list[Path]:
    """
    Walk year subdirectories under source_dir and collect all non-empty HTML files.

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


def _write_rows_to_csv(
    output_csv: Path,
    html_files: list[Path],
    parser: HTMLParserProtocol,
) -> int:
    """
    Open output_csv, parse each HTML file via parser, and write results as rows.

    Args:
        output_csv: Destination CSV path (parent directory must already exist).
        html_files: Ordered list of HTML files to process.
        parser:     Object implementing ``HTMLParserProtocol``.

    Returns:
        Number of rows written.

    Raises:
        HTMLParseError: If ``parser.parse`` raises for any HTML file;
                        the original exception is chained via ``__cause__``.
    """
    rows_written = 0

    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=parser.csv_columns)
        writer.writeheader()

        for html_file in html_files:
            logger.debug("Parsing: %s", html_file)
            try:
                parsed = parser.parse(html_file)
                writer.writerow(
                    {col: parsed.get(col, "") for col in parser.csv_columns}
                )
                rows_written += 1
            except Exception as exc:
                logger.exception("Failed to parse: %s", html_file)
                raise HTMLParseError(f"Failed to parse: {html_file}") from exc

    return rows_written


def extract_html_to_csv(
    source_dir: Path,
    output_csv: Path,
    parser: HTMLParserProtocol,
) -> None:
    """
    Parse all HTML files under source_dir and write extracted data to a CSV.

    Args:
        source_dir: Directory containing year-partitioned HTML files.
        output_csv: Destination CSV path.
        parser:     Object implementing ``HTMLParserProtocol`` — supplies both
                    the column schema (``parser.csv_columns``) and the per-file
                    parse logic (``parser.parse``).

    Raises:
        FileNotFoundError: If no HTML files are found under ``source_dir``.
        HTMLParseError:    If ``parser.parse`` raises for any HTML file;
                           the original exception is chained via ``__cause__``.
    """
    html_files = _find_html_files(source_dir)

    if not html_files:
        raise FileNotFoundError(f"No HTML files found in: {source_dir}")

    output_csv.parent.mkdir(parents=True, exist_ok=True)

    rows_written = _write_rows_to_csv(output_csv, html_files, parser)

    logger.info("Wrote %d rows to %s", rows_written, output_csv)
