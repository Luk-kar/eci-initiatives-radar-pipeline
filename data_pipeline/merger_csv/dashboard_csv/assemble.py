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

    logger.info("Assembled %d dashboard row(s)", len(results))
    return results
