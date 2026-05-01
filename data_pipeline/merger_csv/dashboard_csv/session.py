"""
Dashboard Merger Settings & Bootstrap
-------------------------------------
Defines source-file globs, per-CSV column allow-lists, and the ``setup()``
helper used by ``run.py`` to locate the latest data directory and configure
logging for the dashboard merger step.
"""

import logging
from pathlib import Path

from data_pipeline.pipeline_shared.consts import (
    DATA_DIR,
    LOG_DASHBOARD_PATTERN,
    LOG_DIR_NAME,
)
from data_pipeline.pipeline_shared.logger import get_logger

from .extractor.fields.model import DashboardRow
from .io import find_latest_data_dir

# ── Source-file glob patterns ─────────────────────────────────────────────────
# The numeric prefix ([0-9]) prevents ``eci_responses_*`` from accidentally
# matching the ``eci_responses_followup_*`` family.
INITIATIVES_GLOB = "eci_initiatives_[0-9]*.csv"
RESPONSES_GLOB = "eci_responses_[0-9]*.csv"
LEGISLATION_GLOB = "eci_responses_followup_legislation_[0-9]*.csv"

# ── Column allow-lists per source CSV ─────────────────────────────────────────
# Loaded rows are filtered down to these columns before any analysis runs;
# everything else is dropped to keep the in-memory representation lean and to
# avoid carrying unused upstream columns into the dataclasses.

INITIATIVE_COLS: tuple[str, ...] = (
    "registration_number",
    "title",
    "objective",
    "current_status",
    "initiative_url",
    "timeline_registered",
    "timeline_collection_start_date",
    "timeline_collection_closed",
    "funding_total",
    "signatures_collected",
    "signatures_collected_by_country",
    "signatures_threshold_met",
)

# Only the answer paragraphs are needed from eci_responses; the rest of the
# columns (initiative_url, response_url, title, followup_url, followup_events)
# are duplicated elsewhere or unused by the dashboard schema.
RESPONSE_COLS: tuple[str, ...] = (
    "registration_number",
    "commission_answer",
)

# commission_answer is intentionally **excluded** here because the same
# information is sourced from eci_responses (see RESPONSE_COLS).
LEGISLATION_COLS: tuple[str, ...] = (
    "registration_number",
    "followup_events",
    "law_passed",
    "Is_Law_Passed",
    "Rejected_Legislation",
)

# ── Output column metadata ────────────────────────────────────────────────────
OUTPUT_FIELDNAMES: list[str] = list(DashboardRow.model_fields.keys())


# ── Session bootstrap ─────────────────────────────────────────────────────────
def setup() -> tuple[Path, logging.Logger]:
    """Locate the latest data directory and configure logging.

    Unlike the legislation step, the dashboard merger consumes only CSV files
    (not HTML pages), so the directory finder skips HTML content validation.

    Returns:
        Tuple ``(data_dir, logger)``.
    """
    data_dir = find_latest_data_dir(DATA_DIR)

    logger = get_logger(data_dir / LOG_DIR_NAME, LOG_DASHBOARD_PATTERN)
    logger.info("Starting ECI dashboard CSV merge")
    logger.info("Session: %s", data_dir.name)

    return data_dir, logger
