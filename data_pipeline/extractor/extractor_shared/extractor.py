"""
Shared HTML-to-CSV extraction utilities for data pipeline extractor modules.

Provides two building blocks used by domain-specific extractors:

- ``_find_html_files`` — walks a year-partitioned directory tree and returns
  all non-empty HTML files in deterministic order.
- ``extract_html_to_csv`` — drives the full extraction loop: discovers files,
  delegates parsing to a caller-supplied function, and writes results to a CSV.

Domain extractors (e.g. ``data_pipeline.extractor.initiatives``) are expected
to wrap ``extract_html_to_csv`` with their own column schema and parse function
rather than calling it directly.
"""

import csv
import logging
from pathlib import Path

from .errors import HTMLParseError

logger = logging.getLogger(__name__)


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


def extract_html_to_csv(
    source_dir: Path,
    output_csv: Path,
    csv_columns: list[str],
    parse_function: callable,
) -> None:
    """
    Parse all HTML files under source_dir and write extracted data to a CSV.

    Args:
        source_dir:  Directory containing year-partitioned HTML files.
        output_csv:  Destination CSV path.
        csv_columns: Ordered list of column names for the output CSV header
                     and row mapping.
        parse_function:
                     Callable that accepts a ``Path`` to an HTML file and
                     returns a ``dict`` mapping column names to extracted
                     values.
    """
    html_files = _find_html_files(source_dir)

    if not html_files:
        raise FileNotFoundError(f"No HTML files found in: {source_dir}")

    output_csv.parent.mkdir(parents=True, exist_ok=True)

    rows_written = 0

    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:

        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()

        for html_file in html_files:

            logger.debug("Parsing: %s", html_file)

            try:
                parsed = parse_function(html_file, csv_columns)
                writer.writerow({col: parsed.get(col, "") for col in csv_columns})

                rows_written += 1

            except Exception as exc:

                logger.exception("Failed to parse: %s", html_file)
                raise HTMLParseError(f"Failed to parse: {html_file}") from exc

        logger.info("Wrote %d rows to %s", rows_written, output_csv)
