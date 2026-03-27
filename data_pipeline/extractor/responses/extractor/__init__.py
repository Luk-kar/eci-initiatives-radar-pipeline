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
from .metadata import extract_metadata
from ..parser import parse_HTML
from ..consts import OUTPUT_CSV_FIELDNAMES
from data_pipeline.pipeline_shared.consts import (
    DATA_DIR,
    LOG_DIR_NAME,
    RESPONSES_DIR_NAME,
    ECI_INITIATIVES_CSV_PATTERN,  # kept for consistency, even if pattern not used directly
    ECI_RESPONSES_CSV_PATTERN,
    FilePatterns,
)
from .._logger import setup_logger


logger: Optional[logging.Logger] = None
data_root: Path = DATA_DIR
timestamp: Optional[str] = None
output_csv_name: Optional[str] = None


def configure(timestamp_value: str, data_root_override: Optional[Path] = None) -> None:
    """
    Configure module-level extractor context.

    Must be called before run().

    Args:
        timestamp_value: Timestamp string used in output filenames and logging.
        data_root_override: Optional override for the pipeline data root.
    """
    global timestamp, data_root, output_csv_name
    timestamp = timestamp_value
    data_root = data_root_override or DATA_DIR
    output_csv_name = ECI_RESPONSES_CSV_PATTERN.format(timestamp=timestamp_value)


def run() -> None:
    """Main execution function."""
    global logger

    if timestamp is None or output_csv_name is None:
        raise RuntimeError("Extractor is not configured. Call configure() first.")

    session_path = _find_latest_scrape_session()

    if not session_path:
        raise FileNotFoundError(f"No scraping session found in: {data_root}")

    log_dir = session_path / LOG_DIR_NAME
    logger = setup_logger(log_dir_path=log_dir, timestamp=timestamp)

    logger.info("Starting ECI initiative details extraction")
    logger.info(f"Session: {session_path.name}")

    html_dir = session_path / RESPONSES_DIR_NAME
    output_csv = session_path / output_csv_name

    initiatives_csv = _find_latest_initiatives_csv(session_path)

    logger.info(html_dir)

    if not html_dir.exists():
        raise FileNotFoundError(f"HTML directory not found: {html_dir}")

    logger.info(initiatives_csv)

    if not initiatives_csv or not initiatives_csv.exists():
        raise FileNotFoundError(f"No initiatives CSV found in: {session_path}")

    # Step 1: scan HTML files, derive reg numbers from filenames
    html_files_by_reg = _collect_html_files(html_dir)
    number_of_responses = len(html_files_by_reg)
    if not number_of_responses:
        raise FileNotFoundError(f"No HTML response files found in: {html_dir}")
    logger.info(f"Found {number_of_responses} HTML response files")

    # Step 2: filter CSV metadata to only the reg numbers found on disk
    metadata_by_reg = _load_responses_metadata(
        initiatives_csv, reg_numbers=set(html_files_by_reg.keys())
    )
    logger.info(f"Matched {len(metadata_by_reg)} CSV records to HTML files")

    unmatched = set(html_files_by_reg.keys()) - set(metadata_by_reg.keys())

    if unmatched:
        raise FileNotFoundError(
            f"{len(unmatched)} HTML files have no matching CSV record: {sorted(unmatched)}"
        )

    # Steps 3–5: parse, extract, assemble records
    records: List[ECIResponseRecord] = []

    for reg_number, html_path in html_files_by_reg.items():
        csv_record = metadata_by_reg.get(reg_number)

        if not csv_record:
            raise ValueError(f"No CSV metadata for {reg_number}, skipping")

        record = _process_single(reg_number, csv_record, html_path)

        if record:
            records.append(record)

    _write_csv(records, output_csv)
    logger.info(f"Done. {len(records)} records written to {output_csv}")


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
            response_url=metadata.get("response_commission_url", ""),
            initiative_url=metadata.get("initiative_url", ""),
            registration_number=reg_number,
            title=metadata.get("title", ""),
            **parsed,
        )

    except Exception as e:
        logger.error(f"Failed to process {reg_number}: {e}", exc_info=True)
        return None


def _collect_html_files(html_dir: Path) -> Dict[str, Path]:
    """
    Scan html_dir for response HTML files and derive reg numbers from filenames.

    Files are organised in year subdirectories:
        ``responses/2021/2021_000006_en.html``

    Filename pattern: ``2020_000001_en.html``
    Reg number:       ``2020/000001``

    Returns:
        Dict mapping registration_number → Path for every matched file.
    """
    result: Dict[str, Path] = {}

    for html_file in html_dir.glob("*/*.html"):
        match = re.match(FilePatterns.FILENAME_REGEX, html_file.name)
        if not match:
            logger.debug(f"Skipping unrecognised filename: {html_file.name}")
            continue
        year, number = match.group(1), match.group(2)
        reg_number = f"{year}/{number}"
        result[reg_number] = html_file

    return result


def _find_latest_scrape_session() -> Optional[Path]:
    """Return the most recent session directory."""
    try:
        session_dirs = [
            d
            for d in data_root.iterdir()
            if d.is_dir() and re.match(FilePatterns.TIMESTAMP_DIR_PATTERN, d.name)
        ]
        return max(session_dirs, key=lambda x: x.name) if session_dirs else None

    except Exception as e:
        if logger:
            logger.error(f"Error finding session: {e}")
        return None


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

    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            reg_num = row["registration_number"]
            if reg_num and reg_num in reg_numbers:
                metadata[reg_num] = row

    return metadata


def _write_csv(records: List[ECIResponseRecord], output_csv: Path) -> None:
    """Serialize records and write to CSV."""
    if not records:
        logger.warning("No records to write.")
        return

    output_csv.parent.mkdir(parents=True, exist_ok=True)

    with open(output_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_CSV_FIELDNAMES)
        writer.writeheader()

        for record in records:
            writer.writerow(record.model_dump())

    logger.info(f"Wrote {len(records)} rows to {output_csv}")
