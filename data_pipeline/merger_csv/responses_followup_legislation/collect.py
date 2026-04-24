"""
Legislation Extraction Source Collection
Prepares response and follow-up rows for legislation analysis.
"""

import logging
from pathlib import Path

from .io import find_latest_csv, load_csv, validate_csv_exists
from .session import FOLLOWUP_GLOB, RESPONSES_GLOB

logger = logging.getLogger(__name__)


def index_by_registration(
    rows: list[dict[str, str]],
    key: str = "registration_number",
) -> dict[str, dict[str, str]]:
    """
    Index rows by ``registration_number``.

    Args:
        rows: Source CSV rows.
        key:  Dict key containing the registration number.

    Returns:
        Mapping ``registration_number -> row``.

    Raises:
        ValueError: if a row is missing the key or contains an empty registration number.
    """
    index: dict[str, dict[str, str]] = {}

    for i, row in enumerate(rows):
        reg = (row.get(key) or "").strip()

        if not reg:
            raise ValueError(
                f"Row {i} is missing required column {key!r}. "
                f"Source CSV is malformed. Row={str(row)[:120]}"
            )

        index[reg] = row

    return index


def validate_followup_registration_numbers(
    followup_rows: list[dict[str, str]],
    responses_index: dict[str, dict[str, str]],
    key: str = "registration_number",
) -> None:
    """
    Ensure every registration number in follow-up rows exists in responses rows.

    Args:
        followup_rows:   Rows from ``eci_responses_followup_*.csv``.
        responses_index: Indexed rows from ``eci_responses_*.csv``.
        key:             Join key.

    Raises:
        ValueError: if follow-up contains unknown registration numbers.
    """
    unknown = sorted(
        {
            reg
            for row in followup_rows
            if (reg := (row.get(key) or "").strip()) and reg not in responses_index
        }
    )

    if unknown:
        raise ValueError(
            "eci_responses_followup contains "
            f"{len(unknown)} registration number(s) not found in eci_responses: {unknown}"
        )


def collect_source_rows(data_dir: Path) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """
    Resolve, validate, and load the two source CSVs.

    Args:
        data_dir: Timestamped run directory.

    Returns:
        Tuple ``(responses_rows, followup_rows)``.
    """
    responses_csv = find_latest_csv(data_dir, RESPONSES_GLOB)
    followup_csv = find_latest_csv(data_dir, FOLLOWUP_GLOB)

    validate_csv_exists(responses_csv)
    validate_csv_exists(followup_csv)

    responses_rows = load_csv(responses_csv)
    followup_rows = load_csv(followup_csv)

    responses_index = index_by_registration(responses_rows)
    validate_followup_registration_numbers(followup_rows, responses_index)

    logger.info(
        "Collected %d responses row(s) and %d follow-up row(s)",
        len(responses_rows),
        len(followup_rows),
    )

    return responses_rows, followup_rows