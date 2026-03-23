"""
Entry point for the ECI initiatives extractor.
...
"""

import argparse
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
)
from ._logger import setup_logger
from .extractor import extract_initiatives
from data_pipeline.pipeline_shared.locate_run_dir import (
    find_newest_scraped_data_dir,
)


def extract_eci_initiatives() -> str:
    """
    Run the initiatives extraction pipeline.

    Returns:
        Timestamp string used for output filenames.
    """
    timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)

    data_dir = PIPELINE_DIR / DATA_DIR_NAME

    # ── 1. Resolve run directory ───────────────────────────────────────────────
    run_dir = find_newest_scraped_data_dir(data_dir, INITIATIVES_DIR_NAME)

    # ── 2. Bootstrap logging into the run directory's logs/ folder ────────────
    log_dir_path = run_dir / LOG_DIR_NAME

    logger = setup_logger(log_dir_path, timestamp)

    logger.info("Run directory : %s", run_dir)

    # ── 3. Extract ─────────────────────────────────────────────────────────────
    initiatives_dir = run_dir / INITIATIVES_DIR_NAME
    output_csv = data_dir / ECI_INITIATIVES_CSV_PATTERN.format(timestamp=timestamp)

    logger.info("Input  : %s", initiatives_dir)
    logger.info("Output : %s", output_csv)

    extract_initiatives(initiatives_dir, output_csv)

    logger.info("Extraction complete")


if __name__ == "__main__":
    extract_eci_initiatives()
