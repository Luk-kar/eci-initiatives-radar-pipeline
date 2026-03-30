# data_pipeline/extractor/responses/extractor/__init__.py
"""
ECI Initiative Details Extractor

Reads HTML response files from disk, derives registration numbers from
filenames, filters metadata from the latest initiatives CSV, and extracts an
analysis-ready dataset into CSV format.
"""

import csv
import re
import logging
from pathlib import Path
from typing import Dict, List, Optional, Set

from ..model import ECIResponseRecord
from .copy_fields.metadata import extract_metadata
from .parser import parse_HTML
from data_pipeline.pipeline_shared.consts import (
    DATA_DIR,
    LOG_DIR_NAME,
    RESPONSES_DIR_NAME,
    ECI_RESPONSES_CSV_PATTERN,
    LOG_EXTRACTOR_RESPONSES_PATTERN,
    FilePatterns,
    FILE_ENCODING,
)
from data_pipeline.pipeline_shared.logger import get_logger
from data_pipeline.pipeline_shared.locate_run_dir import find_newest_scraped_data_dir
from data_pipeline.pipeline_shared.errors import RunDirectoryValidationError
from data_pipeline.extractor.extractor_shared.errors import HTMLParseError


logger = logging.getLogger(__name__)


def configure(timestamp: str) -> str:
    """
    Configure module-level extractor context.

    Must be called before run().

    Args:
        timestamp: Timestamp string used in output filenames and logging.
    """
    return ECI_RESPONSES_CSV_PATTERN.format(timestamp=timestamp)


def run(output_csv_name: str, timestamp: str) -> None:
    """Main execution function — orchestrates the four extraction steps."""
    global logger

    if timestamp is None or output_csv_name is None:
        raise RuntimeError("Extractor is not configured. Call configure() first.")

    html_dir, output_csv, initiatives_csv = _setup(timestamp, output_csv_name)

    html_files = _collect_html_files(html_dir)

    metadata = _load_metadata(initiatives_csv, html_files)
    parsed_data = _parse_html_files(html_files)

    records = _build_records(metadata, parsed_data)

    _write_csv(records, output_csv)
    logger.info("Done. %d records written to %s", len(records), output_csv)


# ── Setup ──────────────────────────────────────────────────────────────────────


def _setup(timestamp: str, output_csv_name: str) -> tuple[Path, Path, Path]:
    """
    Locate the latest scrape session, configure logging, build all relevant
    paths, and validate that required inputs exist.

    Returns:
        (html_dir, output_csv, initiatives_csv)
    """
    global logger

    session_path = find_newest_scraped_data_dir(DATA_DIR, RESPONSES_DIR_NAME)

    logger = get_logger(session_path / LOG_DIR_NAME, LOG_EXTRACTOR_RESPONSES_PATTERN)
    logger.info("Starting ECI responses extraction")
    logger.info("Session: %s", session_path.name)

    html_dir = session_path / RESPONSES_DIR_NAME
    output_csv = session_path / output_csv_name
    initiatives_csv = _find_latest_initiatives_csv(session_path)

    if not html_dir.exists():
        raise FileNotFoundError(f"HTML directory not found: {html_dir}")

    if not initiatives_csv or not initiatives_csv.exists():
        raise FileNotFoundError(f"No initiatives CSV found in: {session_path}")

    return html_dir, output_csv, initiatives_csv


# ── Step 1 — collect HTML files ───────────────────────────────────────────────


def _collect_html_files(html_dir: Path) -> Dict[str, Path]:
    """
    Scan html_dir for response HTML files and derive reg numbers from filenames.

    Returns:
        Dict mapping registration_number → Path.

    Raises:
        FileNotFoundError: If no matching HTML files are found.
    """
    html_files = _scan_html_files(html_dir)

    if not html_files:
        raise FileNotFoundError(f"No HTML response files found in: {html_dir}")

    logger.info("Found %d HTML response files", len(html_files))
    return html_files


def _scan_html_files(html_dir: Path) -> Dict[str, Path]:
    """
    Walk year subdirectories under html_dir and map reg numbers to file paths.

    Filename pattern : ``2020_000001.html``
    Reg number       : ``2020/000001``
    """
    result: Dict[str, Path] = {}

    for html_file in html_dir.glob("*/*.html"):
        match = re.match(FilePatterns.FILENAME_REGEX, html_file.name)

        if not match:
            raise NameError("Unrecognised filename: %s", html_file.name)

        year, number = match.group(1), match.group(2)
        result[f"{year}/{number}"] = html_file

    return result


# ── Step 2 — load and validate metadata ───────────────────────────────────────


def _load_metadata(
    initiatives_csv: Path,
    html_files: Dict[str, Path],
) -> Dict[str, dict]:
    """
    Load initiatives CSV rows filtered to reg numbers found on disk,
    then assert every HTML file has a matching CSV record.

    Returns:
        Dict mapping registration_number → CSV row dict.

    Raises:
        FileNotFoundError: If any HTML file has no matching CSV record.
    """
    metadata = _load_responses_metadata(
        initiatives_csv, reg_numbers=set(html_files.keys())
    )
    logger.info("Matched %d CSV records to HTML files", len(metadata))

    unmatched = set(html_files.keys()) - set(metadata.keys())
    if unmatched:
        raise FileNotFoundError(
            f"{len(unmatched)} HTML files have no matching CSV record: {sorted(unmatched)}"
        )

    return metadata


# ── Step 3 — parse HTML and assemble records ───────────────────────────────────


def _parse_html_files(html_files: Dict[str, Path]) -> Dict[str, dict]:
    """
    Parse each HTML response file and return extracted field dicts keyed by
    registration number.

    Returns:
        Dict mapping registration_number → parsed field dict.

    Raises:
        HTMLParseError: If any HTML file fails to parse.
    """
    parsed_data: Dict[str, dict] = {}

    for reg_number, html_path in html_files.items():
        try:
            parsed_data[reg_number] = parse_HTML(html_path, reg_number)
        except Exception as exc:
            raise HTMLParseError(f"Failed to parse HTML for {reg_number}") from exc

    return parsed_data


# ── Step 4 — assemble records ─────────────────────────────────────────────────


def _build_records(
    metadata_by_reg: Dict[str, dict],
    parsed_by_reg: Dict[str, dict],
) -> List[ECIResponseRecord]:
    """
    Merge loaded CSV metadata with parsed HTML fields into ECIResponseRecords.

    Args:
        metadata_by_reg: Raw CSV row dicts keyed by registration_number.
        parsed_by_reg:   HTML-extracted fields keyed by registration_number.

    Returns:
        List of fully assembled ECIResponseRecords.
    """

    records: List[ECIResponseRecord] = []

    for reg_number, parsed in parsed_by_reg.items():

        csv_row = metadata_by_reg[reg_number]
        metadata = extract_metadata(csv_row)

        records.append(ECIResponseRecord(**metadata.model_dump(), **parsed))

    return records


# ── Private helpers ────────────────────────────────────────────────────────────


def _find_latest_initiatives_csv(session_path: Path) -> Optional[Path]:
    """
    Return the most recent eci_initiatives_*.csv in the session directory.

    The pattern matches files like ``eci_initiatives_2026-03-24_18-16-07.csv``.
    If multiple exist, the lexicographically largest name (latest timestamp) wins.
    """
    matches = sorted(session_path.glob("eci_initiatives_*.csv"))
    return matches[-1] if matches else None


def _process_single(
    reg_number: str, csv_record: dict, html_path: Path
) -> Optional[ECIResponseRecord]:
    """Parse one HTML file and return a populated record."""

    try:
        metadata = extract_metadata(csv_record)
        parsed = parse_HTML(html_path, reg_number)

        return ECIResponseRecord(
            **metadata.model_dump(),
            **parsed,
        )

    except Exception as exc:
        raise HTMLParseError(f"Failed to process {reg_number}") from exc


def _load_responses_metadata(csv_path: Path, reg_numbers: Set[str]) -> Dict[str, dict]:
    """
    Load the initiatives CSV filtered to the given set of reg numbers.

    Args:
        csv_path:     Path to the latest eci_initiatives_*.csv in the
                      session directory.
        reg_numbers:  Set of registration numbers derived from HTML filenames.
                      Only rows whose ``registration_number`` is in this set
                      are kept.

    Returns:
        Dict mapping registration_number → row dict.
    """
    metadata: Dict[str, dict] = {}

    with open(csv_path, encoding=FILE_ENCODING) as f:
        for row in csv.DictReader(f):
            reg_num = row["registration_number"]
            if reg_num and reg_num in reg_numbers:
                metadata[reg_num] = row

    return metadata


def _write_csv(records: List[ECIResponseRecord], output_csv: Path) -> None:
    """Serialize records and write to CSV."""
    if not records:
        raise ValueError("No records to write.")

    output_csv.parent.mkdir(parents=True, exist_ok=True)

    with open(output_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(ECIResponseRecord.model_fields))
        writer.writeheader()

        for record in records:
            writer.writerow(record.model_dump())

    logger.info("Wrote %d rows to %s", len(records), output_csv)
