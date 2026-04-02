"""
Session bootstrap — locates the latest scrape run, configures logging,
and validates that all required input paths exist.
"""

import logging
from pathlib import Path

from data_pipeline.pipeline_shared.consts import (
    DATA_DIR,
    LOG_DIR_NAME,
    RESPONSES_DIR_NAME,
    LOG_EXTRACTOR_RESPONSES_PATTERN,
)
from data_pipeline.pipeline_shared.logger import get_logger
from data_pipeline.pipeline_shared.locate_run_dir import find_newest_scraped_data_dir


def setup(
    timestamp: str, output_csv_name: str
) -> tuple[Path, Path, Path, logging.Logger]:
    """
    Locate the latest scrape session, configure logging, build all relevant
    paths, and validate that required inputs exist.

    Returns:
        (html_dir, output_csv, initiatives_csv, logger)
    """
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

    return html_dir, output_csv, initiatives_csv, logger


def _find_latest_initiatives_csv(session_path: Path):
    """
    Return the most recent eci_initiatives_*.csv in the session directory.

    The pattern matches files like ``eci_initiatives_2026-03-24_18-16-07.csv``.
    If multiple exist, the lexicographically largest name (latest timestamp) wins.
    """
    matches = sorted(session_path.glob("eci_initiatives_*.csv"))
    return matches[-1] if matches else None
