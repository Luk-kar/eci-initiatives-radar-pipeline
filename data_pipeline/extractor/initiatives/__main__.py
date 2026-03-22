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

from data_pipeline.consts import (
    DATA_DIR_NAME,
    ECI_INITIATIVES_CSV_PATTERN,
    INITIATIVES_DIR_NAME,
    LOG_DIR_NAME,
    LOG_EXTRACTOR_INITIATIVES_PATTERN,
    PROJECT_DIR,
    DATA_PIPELINE_DIR_NAME,
)
from data_pipeline.extractor.initiatives.extractor import extract_initiatives
from data_pipeline.extractor.initiatives.validator import (
    RunDirectoryValidationError,
    find_newest_run_dir,
    validate_run_dir,
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
                 ``PROJECT_DIR / DATA_DIR_NAME`` is used.

    Returns:
        Timestamp string used for output filenames.

    Raises:
        RunDirectoryValidationError: If the run directory fails validation.
        SystemExit: On unrecoverable errors (logged before exit).
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    data_dir = PROJECT_DIR / DATA_PIPELINE_DIR_NAME / DATA_DIR_NAME

    # ── 1. Resolve run directory ───────────────────────────────────────────────
    run_dir = find_newest_run_dir(data_dir)

    # ── 2. Bootstrap logging into the run directory's logs/ folder ────────────
    log_path = (
        run_dir
        / LOG_DIR_NAME
        / LOG_EXTRACTOR_INITIATIVES_PATTERN.format(timestamp=timestamp)
    )

    print(str(log_path))
    _setup_logging(log_path)
    logger = logging.getLogger(__name__)

    logger.info("Run directory : %s", run_dir)

    # ── 3. Validate run directory structure and HTML content ───────────────────
    try:
        validate_run_dir(run_dir)
    except RunDirectoryValidationError as exc:
        logger.error("Run directory validation failed: %s", exc)
        raise

    # ── 4. Extract ─────────────────────────────────────────────────────────────
    initiatives_dir = run_dir / INITIATIVES_DIR_NAME
    output_csv = data_dir / ECI_INITIATIVES_CSV_PATTERN.format(timestamp=timestamp)

    logger.info("Input  : %s", initiatives_dir)
    logger.info("Output : %s", output_csv)

    extract_initiatives(initiatives_dir, output_csv)

    logger.info("Extraction complete — timestamp: %s", timestamp)
    return timestamp


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract ECI initiative data from scraped HTML files."
    )
    parser.add_argument(
        "--run-dir",
        type=Path,
        default=None,
        metavar="DIR",
        help=(
            "Explicit run directory to process "
            "(default: newest under data_pipeline/data/)."
        ),
    )
    return parser.parse_args()


if __name__ == "__main__":

    try:
        extract_eci_initiatives()
    except RunDirectoryValidationError as exc:
        sys.exit(f"[ERROR] {exc}")
