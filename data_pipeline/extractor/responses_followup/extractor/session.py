"""
Session bootstrap — locates the latest scrape run, configures logging,
and validates that all required input paths exist.
"""

import logging
from pathlib import Path
from typing import Optional
from datetime import datetime

from data_pipeline.pipeline_shared.consts import (
    DATA_DIR,
    LOG_DIR_NAME,
    RESPONSES_FOLLOWUP_DIR_NAME,
    LOG_EXTRACTOR_RESPONSES_FOLLOWUP_PATTERN,
    HTML_DOMAIN_EC_FOLLOWUP,
    ECI_RESPONSES_CSV_PATTERN,
    TIMESTAMP_FORMAT,
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
    """Return the latest eci_responses_*.csv in *session_path* (not in a subdirectory)."""
    
    # Creates: "eci_responses_%Y-%m-%d_%H-%M-%S.csv"
    expected_format = ECI_RESPONSES_CSV_PATTERN.format(timestamp=TIMESTAMP_FORMAT)
    
    candidates = []

    for filepath in session_path.iterdir():

        if filepath.is_file():

            try:
                # Validates the entire filename structure and timestamp in one pass
                datetime.strptime(filepath.name, expected_format)
                candidates.append(filepath)

            except ValueError:
                # Silently ignore files that don't match the exact structure
                continue
                
    if not candidates:
        raise FileNotFoundError(
            f"No responses CSV matching pattern '{ECI_RESPONSES_CSV_PATTERN}' "
            f"found in session directory: {session_path}"
        )

    latest_response_csv = sorted(candidates)[-1]
        
    return latest_response_csv