"""
Dashboard Merger Source Collection
----------------------------------
Locates, loads, filters, and dataclass-wraps the three source CSVs:

* ``eci_initiatives_*.csv``
* ``eci_responses_*.csv`` (only ``commission_answer``)
* ``eci_responses_followup_legislation_*.csv`` (without ``commission_answer``)
"""

import logging
from pathlib import Path

from .io import (
    filter_columns,
    find_latest_csv,
    load_csv,
    validate_csv_exists,
)
from .input_models import InitiativeRow, LegislationRow, ResponseRow
from .session import (
    INITIATIVE_COLS,
    INITIATIVES_GLOB,
    LEGISLATION_COLS,
    LEGISLATION_GLOB,
    RESPONSE_COLS,
    RESPONSES_GLOB,
)

logger = logging.getLogger(__name__)


# ── Per-source loaders ────────────────────────────────────────────────────────
def _load_initiatives(data_dir: Path) -> list[InitiativeRow]:
    csv_path = find_latest_csv(data_dir, INITIATIVES_GLOB)
    validate_csv_exists(csv_path)

    rows = filter_columns(
        load_csv(csv_path), INITIATIVE_COLS, source_label="eci_initiatives"
    )
    return [InitiativeRow(**row) for row in rows]


def _load_responses(data_dir: Path) -> list[ResponseRow]:
    csv_path = find_latest_csv(data_dir, RESPONSES_GLOB)
    validate_csv_exists(csv_path)

    rows = filter_columns(
        load_csv(csv_path), RESPONSE_COLS, source_label="eci_responses"
    )
    return [ResponseRow(**row) for row in rows]


def _load_legislation(data_dir: Path) -> list[LegislationRow]:
    csv_path = find_latest_csv(data_dir, LEGISLATION_GLOB)
    validate_csv_exists(csv_path)

    rows = filter_columns(
        load_csv(csv_path),
        LEGISLATION_COLS,
        source_label="eci_responses_followup_legislation",
    )
    return [LegislationRow(**row) for row in rows]


# ── Indexing helper ───────────────────────────────────────────────────────────
def _index_by_registration(rows: list, source_label: str) -> dict[str, object]:
    """Index dataclass rows by ``registration_number``.

    Raises:
        ValueError: if a row has an empty registration number, or two rows
                    share one (which would silently lose data).
    """

    index: dict[str, object] = {}

    for i, row in enumerate(rows):
        reg = (getattr(row, "registration_number", "") or "").strip()
        if not reg:
            raise ValueError(
                f"{source_label}: row {i} has an empty registration_number."
            )
        if reg in index:
            raise ValueError(f"{source_label}: duplicate registration_number {reg!r}.")
        index[reg] = row

    return index


# ── Public entry point ────────────────────────────────────────────────────────
def collect_source_rows(
    data_dir: Path,
) -> tuple[
    list[InitiativeRow],
    dict[str, ResponseRow],
    dict[str, LegislationRow],
]:
    """Load, narrow, and index the three source CSVs.

    Args:
        data_dir: Timestamped run directory containing the source CSVs.

    Returns:
        ``(initiative_rows, response_index, legislation_index)``

        * ``initiative_rows`` — every row from ``eci_initiatives``, in source
          order. Treated as the authoritative list of initiatives by the
          assemble step.
        * ``response_index`` — ``ResponseRow`` keyed by registration number;
          only initiatives that have reached the answer stage appear here.
        * ``legislation_index`` — ``LegislationRow`` keyed by registration
          number; populated for the same subset as ``response_index``.
    """

    initiative_rows = _load_initiatives(data_dir)
    response_rows = _load_responses(data_dir)
    legislation_rows = _load_legislation(data_dir)

    response_index: dict[str, ResponseRow] = _index_by_registration(
        response_rows, "eci_responses"
    )  # type: ignore[assignment]

    legislation_index: dict[str, LegislationRow] = _index_by_registration(
        legislation_rows, "eci_responses_followup_legislation"
    )  # type: ignore[assignment]

    logger.info(
        "Collected %d initiative(s), %d response row(s), %d legislation row(s)",
        len(initiative_rows),
        len(response_index),
        len(legislation_index),
    )

    return initiative_rows, response_index, legislation_index
