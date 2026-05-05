"""
Dashboard Merger Assembly
-------------------------
Joins the three source datasets on ``registration_number`` and produces one
``DashboardRow`` per initiative by delegating to ``extractor.analyse_row``.
"""

from __future__ import annotations

import logging

from .extractor import DashboardRow, analyse_row
from .input_models import InitiativeRow, LegislationRow, ResponseRow

logger = logging.getLogger(__name__)


def assemble_results(
    initiative_rows: list[InitiativeRow],
    response_index: dict[str, ResponseRow],
    legislation_index: dict[str, LegislationRow],
) -> list[DashboardRow]:
    """
    Produce one ``DashboardRow`` per initiative.

    The list of initiatives is authoritative — every row in
    ``eci_initiatives`` becomes one row in the dashboard, regardless of
    whether it has a matching response or legislation entry.

    Args:
        initiative_rows:   Rows loaded from ``eci_initiatives``.
        response_index:    ``ResponseRow`` keyed by ``registration_number``.
        legislation_index: ``LegislationRow`` keyed by ``registration_number``.

    Returns:
        Assembled ``DashboardRow`` objects, in source order.

    Raises:
        ValueError: If an initiative has an empty registration number.
    """

    results: list[DashboardRow] = []
    total = len(initiative_rows)

    for i, initiative in enumerate(initiative_rows, start=1):

        regnum = (initiative.registration_number or "").strip()
        if not regnum:
            raise ValueError(
                f"Initiative row {i} has an empty registration_number. "
                f"Source CSV is malformed."
            )

        response = response_index.get(regnum)
        legislation = legislation_index.get(regnum)

        logger.info(
            "Assembling dashboard row for %s (%d/%d) " "[response=%s, legislation=%s]",
            regnum,
            i,
            total,
            "yes" if response else "no",
            "yes" if legislation else "no",
        )

        results.append(analyse_row(initiative, response, legislation))

    results_sanitized = _exclude_non_public_initiatives(results)

    logger.info("Assembled %d dashboard row(s)", len(results_sanitized))
    return results_sanitized


def _exclude_non_public_initiatives(rows: list[DashboardRow]) -> list[DashboardRow]:
    """Exclude initiatives that were never made public on the ECI portal.

    Registration-refused initiatives are rejected by the Commission before
    registration is granted and never enter the public ECI lifecycle.

    They can appear in the source data if the ECI portal incorrectly
    lists them alongside registered initiatives.
    """
    before = len(rows)

    filtered = [row for row in rows if row.current_status != "Registration Refused"]

    if filtered:
        logger.info(
            "Excluded %d registration-refused initiative(s) from the dashboard output",
            before - len(filtered),
        )

    return filtered
