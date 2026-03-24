"""
Entry point for the ECI initiatives extractor.
...
"""

import logging
import sys
from datetime import datetime
from pathlib import Path

from data_pipeline.pipeline_shared.consts import (
    DATA_DIR_NAME,
    ECI_INITIATIVES_CSV_PATTERN,
    INITIATIVES_DIR_NAME,
    LOG_DIR_NAME,
    LOG_EXTRACTOR_INITIATIVES_PATTERN,
    PIPELINE_DIR,
    DATA_PIPELINE_DIR_NAME,
    TIMESTAMP_FORMAT,
    DATA_DIR,
)
from ._logger import setup_logger
from .extractor import extract_initiatives
from data_pipeline.pipeline_shared.locate_run_dir import (
    find_newest_scraped_data_dir,
)


# ── Step functions ─────────────────────────────────────────────────────────────


def _resolve_run_dir() -> Path:
    """Locate the newest scraped data directory for initiatives."""
    return find_newest_scraped_data_dir(DATA_DIR, INITIATIVES_DIR_NAME)


def _setup_logging(run_dir: Path, timestamp: str) -> logging.Logger:
    """Bootstrap logging into the run directory's logs/ folder."""
    log_dir_path = run_dir / LOG_DIR_NAME
    return setup_logger(log_dir_path, timestamp)


def _run_extraction(
    run_dir: Path,
    timestamp: str,
    logger: logging.Logger,
) -> None:
    """Resolve I/O paths and run the initiatives extractor."""
    initiatives_dir = run_dir / INITIATIVES_DIR_NAME
    output_csv = run_dir / ECI_INITIATIVES_CSV_PATTERN.format(timestamp=timestamp)

    logger.info("Input  : %s", initiatives_dir)
    logger.info("Output : %s", output_csv)

    extract_initiatives(initiatives_dir, output_csv)


# ── Entry point ────────────────────────────────────────────────────────────────


def extract_eci_initiatives() -> None:
    """Run the initiatives extraction pipeline."""
    timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)

    run_dir = _resolve_run_dir()
    logger = _setup_logging(run_dir, timestamp)

    logger.info("Run directory : %s", run_dir)

    _run_extraction(run_dir, timestamp, logger)

    logger.info("Extraction complete")


if __name__ == "__main__":
    extract_eci_initiatives()
