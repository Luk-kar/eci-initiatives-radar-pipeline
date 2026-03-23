"""
Entry point for the ECI initiatives extractor.

Automatically discovers the newest timestamped run directory under
``data_pipeline/data/``, validates its structure, then extracts
initiative data and writes results to a CSV file.

Usage:
    python -m data_pipeline.extractor.initiatives
    python -m data_pipeline.extractor.initiatives --run-dir data/2026-03-22_15-51-04
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
)
from data_pipeline.extractor.initiatives.extractor import extract_initiatives
from data_pipeline.pipeline_shared.locate_run_dir import (
    find_newest_scraped_data_dir,
)


def _setup_logging(log_path: Path) -> None:

    log_path.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def extract_eci_initiatives() -> str:
    """
    Run the initiatives extraction pipeline.

    Args:
        run_dir: Explicit timestamped run directory, e.g.
                 ``data_pipeline/data/2026-03-22_15-51-04``.
                 If ``None``, the newest directory under
                 ``PIPELINE_DIR / DATA_DIR_NAME`` is used.

    Returns:
        Timestamp string used for output filenames.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    data_dir = PIPELINE_DIR / DATA_DIR_NAME

    # ── 1. Resolve run directory ───────────────────────────────────────────────
    run_dir = find_newest_scraped_data_dir(data_dir, INITIATIVES_DIR_NAME)

    # ── 2. Bootstrap logging into the run directory's logs/ folder ────────────
    log_path = (
        run_dir
        / LOG_DIR_NAME
        / LOG_EXTRACTOR_INITIATIVES_PATTERN.format(timestamp=timestamp)
    )

    _setup_logging(log_path)
    logger = logging.getLogger(__name__)

    logger.info("Run directory : %s", run_dir)

    # ── 3. Extract ─────────────────────────────────────────────────────────────
    initiatives_dir = run_dir / INITIATIVES_DIR_NAME
    output_csv = data_dir / ECI_INITIATIVES_CSV_PATTERN.format(timestamp=timestamp)

    logger.info("Input  : %s", initiatives_dir)
    logger.info("Output : %s", output_csv)

    extract_initiatives(initiatives_dir, output_csv)

    logger.info("Extraction complete — timestamp: %s", timestamp)
    return timestamp


if __name__ == "__main__":

    extract_eci_initiatives()
