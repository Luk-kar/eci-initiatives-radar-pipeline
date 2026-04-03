"""
Session bootstrap — locates the latest scrape run, configures logging,
and validates that all required input paths exist.
"""

import logging
from pathlib import Path
from typing import Optional

from data_pipeline.pipeline_shared.consts import (
    DATA_DIR,
    LOG_DIR_NAME,
    RESPONSES_FOLLOWUP_DIR_NAME,
    LOG_EXTRACTOR_RESPONSES_FOLLOWUP_PATTERN,
    HTML_DOMAIN_EC_FOLLOWUP,
    ECI_RESPONSES_CSV_GLOB,
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
        (html_dir, output_csv, followup_list_csv, logger)
    """

    session_path = find_newest_scraped_data_dir(
        DATA_DIR,
        RESPONSES_FOLLOWUP_DIR_NAME,
        domain=HTML_DOMAIN_EC_FOLLOWUP,
    )

    logger = get_logger(
        session_path / LOG_DIR_NAME, LOG_EXTRACTOR_RESPONSES_FOLLOWUP_PATTERN
    )
    logger.info("Starting ECI responses follow-up extraction")
    logger.info("Session: %s", session_path.name)

    html_dir = session_path / RESPONSES_FOLLOWUP_DIR_NAME
    output_csv = session_path / output_csv_name
    followup_list_csv = _find_responses_csv(session_path)

    if not html_dir.exists():
        raise FileNotFoundError(f"HTML directory not found: {html_dir}")

    if followup_list_csv is None or not followup_list_csv.exists():
        raise FileNotFoundError(
            f"'{RESPONSES_FOLLOWUP_LIST_CSV}' not found in: {session_path}"
        )

    return html_dir, output_csv, followup_list_csv, logger


def _find_responses_csv(session_path: Path) -> Optional[Path]:
    """Return the latest eci_responses_*.csv in *session_path* (not in a subdirectory).

    Filenames embed a timestamp (eci_responses_2026-04-02_12-39-21.csv), so a
    lexicographic sort on the name is also a chronological sort.

    Returns:
        Path to the most recent match, or None if none found.
    """
    candidates = sorted(session_path.glob(ECI_RESPONSES_CSV_GLOB))
    return candidates[-1] if candidates else None
