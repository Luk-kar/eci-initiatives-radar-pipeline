"""
Legislation Extraction Settings & Bootstrap
-------------------------------------------
Defines shared names / output metadata for the legislation pipeline step,
and provides the ``setup()`` helper that locates the latest scrape run and
configures logging.
"""

import logging
from dataclasses import fields as dataclass_fields
from pathlib import Path

from data_pipeline.pipeline_shared.consts import (
    DATA_DIR,
    HTML_DOMAIN_EC_FOLLOWUP,
    LOG_DIR_NAME,
    LOG_LEGISLATION_PATTERN,
    RESPONSES_FOLLOWUP_DIR_NAME,
)
from data_pipeline.pipeline_shared.locate_run_dir import find_newest_scraped_data_dir
from data_pipeline.pipeline_shared.logger import get_logger

from .extractor import LegislationResult

# ── Output / column metadata ──────────────────────────────────────────────────
OUTPUT_FIELDNAMES: list[str] = [f.name for f in dataclass_fields(LegislationResult)]

RESPONSES_GLOB = "eci_responses_[0-9]*.csv"
FOLLOWUP_GLOB = "eci_responses_followup_[0-9]*.csv"

RESPONSES_COLS = ("registration_number", "commission_answer")
FOLLOWUP_COLS = ("registration_number", "followup_events")


# ── Session bootstrap ─────────────────────────────────────────────────────────
def setup() -> tuple[Path, logging.Logger]:
    """
    Locate the latest scrape session and configure logging.

    Returns:
        (data_dir, logger)
    """
    data_dir = find_newest_scraped_data_dir(
        DATA_DIR,
        RESPONSES_FOLLOWUP_DIR_NAME,
        HTML_DOMAIN_EC_FOLLOWUP,
    )

    logger = get_logger(data_dir / LOG_DIR_NAME, LOG_LEGISLATION_PATTERN)
    logger.info("Starting ECI follow-up legislation extraction")
    logger.info("Session: %s", data_dir.name)

    return data_dir, logger
