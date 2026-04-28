"""
Dashboard Merger Pipeline Coordinator
-------------------------------------
Coordinates the full dashboard CSV merge: locate the latest data directory,
load the three source CSVs, assemble the rows, sort them, and write the
output dashboard CSV.
"""

import logging
from pathlib import Path

from data_pipeline.pipeline_shared.sort import sort_by_registration_number

from .assemble import assemble_results
from .collect import collect_source_rows
from .session import setup
from .write import write_output

logger = logging.getLogger(__name__)


def _sort_results_by_initiative(results):
    """
    Sort dashboard rows by their underlying initiative registration number.

    ``DashboardRow`` does not carry ``registration_number`` (it is the
    dashboard schema, which uses ``registration_date`` and
    ``registration_year`` instead), so we sort on the registration_date
    prefix as a stable, chronology-preserving proxy.

    For exact registration-number ordering, sort earlier in the pipeline,
    while ``initiative_rows`` are still ``InitiativeRow`` instances.
    """

    return sorted(
        results,
        key=lambda r: (
            r.registration_year,
            r.registration_date,
            r.title,
        ),
    )


def run() -> Path:
    """Execute the full dashboard merge step.

    Returns:
        Path to the written dashboard CSV.
    """
    global logger

    data_dir, step_logger = setup()
    logger = step_logger

    logger.info("Starting dashboard merge in %s", data_dir)

    initiative_rows, response_index, legislation_index = collect_source_rows(data_dir)

    # Sort initiatives by registration number first so the dashboard rows
    # come out chronologically without needing reg-num inside DashboardRow.
    initiative_rows = sort_by_registration_number(initiative_rows)

    logger.info(
        "Sources collected: initiatives=%d, responses=%d, legislation=%d",
        len(initiative_rows),
        len(response_index),
        len(legislation_index),
    )

    results = assemble_results(initiative_rows, response_index, legislation_index)
    logger.info("Assembly complete: %d dashboard row(s)", len(results))

    output_path = write_output(data_dir, results)
    logger.info("Done. Dashboard CSV written to %s", output_path)

    return output_path
