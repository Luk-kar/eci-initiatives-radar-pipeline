"""
Per-row orchestrator for the dashboard merger.

``analyse_row`` is the single public entry point.  It reads the simple
"direct copy" / "rename" / "type cast" fields inline, and delegates the
fields that require non-trivial logic to the dedicated extractor modules
under :mod:`data_pipeline.merger_csv.responses_followup_legislation.extractor.fields`.

Why those modules live in the legislation directory, not next to this one:
the project has standardised on a single ``extractor/fields/`` directory
for **all** column-level extraction logic, so dashboard-specific extractors
sit alongside the legislation-specific ones rather than being duplicated
in a sibling module. See task requirement 6.
"""

from __future__ import annotations

import logging

from data_pipeline.merger_csv.dashboard_csv.extractor.fields import (
    commission_answer_text as _commission_answer_text,
    current_status as _current_status,
    legislation as _legislation,
    signatures_collected_by_country as _signatures_collected_by_country,
    url as _url,
)

from ..input_models import InitiativeRow, LegislationRow, ResponseRow
from .fields.model import DashboardRow

__all__ = ["analyse_row", "DashboardRow"]

logger = logging.getLogger(__name__)


def _parse_bool(value: str | None) -> bool:
    """Parse a stringified boolean from the legislation CSV.

    The merge step writes Python ``True`` / ``False`` literals via
    ``csv.DictWriter``, so we accept both forms case-insensitively.
    """
    if not value:
        return False
    return value.strip().lower() == "true"


def analyse_row(
    initiative: InitiativeRow,
    response: ResponseRow | None,
    legislation: LegislationRow | None,
) -> DashboardRow:
    """Assemble a single ``DashboardRow`` from the joined source rows.

    Simple fields (direct copy, rename, type cast, whitespace cleanup) are
    handled inline. Fields that require non-trivial logic delegate to the
    placeholder modules — those raise ``NotImplementedError`` until they are
    implemented.

    Args:
        initiative:  The authoritative ``InitiativeRow`` from
                     ``eci_initiatives_*.csv``.
        response:    Optional matching ``ResponseRow`` from
                     ``eci_responses_*.csv`` — ``None`` when the Commission
                     has not answered yet.
        legislation: Optional matching ``LegislationRow`` from
                     ``eci_responses_followup_legislation_*.csv`` —
                     ``None`` for the same reason.

    Returns:
        A populated ``DashboardRow``.
    """
    # ── Legislation flags (used by current_status / legislation) ──────────────
    is_law_passed = _parse_bool(legislation.Is_Law_Passed) if legislation else False
    rejected = _parse_bool(legislation.Rejected_Legislation) if legislation else False

    # ── Simple, inline-handled fields ─────────────────────────────────────────
    # registration_date is already DD/MM/YYYY in the source.
    registration_date = initiative.timeline_registered

    # Year prefix of registration_number is the most reliable source.
    registration_year = (
        initiative.registration_number.split("/", 1)[0]
        if "/" in initiative.registration_number
        else ""
    )

    # Whitespace cleanup for the multiline objective text.
    objective = " ".join(initiative.objective.split()) if initiative.objective else ""

    # ── Delegated, complex fields ─────────────────────────────────────────────
    return DashboardRow(
        title=initiative.title,
        registration_year=registration_year,
        registration_date=registration_date,
        current_status=_current_status.extract(
            raw_status=initiative.current_status,
            is_law_passed=is_law_passed if legislation else None,
            rejected_legislation=rejected if legislation else None,
        ),
        objective=objective,
        commission_answer_text=_commission_answer_text.extract(
            response.commission_answer_text if response else None,
        ),
        url=_url.extract(initiative.initiative_url),
        signatures_collected_by_country=_signatures_collected_by_country.extract(
            initiative.signatures_collected_by_country,
        ),
        signatures_threshold_met=initiative.signatures_threshold_met,
        signatures_collected=initiative.signatures_collected,
        funding_total=initiative.funding_total,
        timeline_collection_closed=initiative.timeline_collection_closed,
        # Column rename: timeline_collection_start_date -> timeline_collection_start.
        timeline_collection_start=initiative.timeline_collection_start_date,
        legislation=_legislation.extract(
            law_passed_raw=legislation.Law_Passed if legislation else None,
            is_law_passed=is_law_passed,
            rejected_legislation=rejected,
        ),
    )
