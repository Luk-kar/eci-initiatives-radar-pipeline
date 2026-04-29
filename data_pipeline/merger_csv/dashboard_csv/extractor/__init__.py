"""
Per-row orchestrator for the dashboard merger.

``analyse_row`` is the single public entry point.  It reads the simple
"direct copy" / "rename" / "type cast" fields inline, and delegates the
fields that require non-trivial logic to the dedicated extractor modules
under :mod:`data_pipeline.merger_csv.responses_followup_legislation.extractor.fields`.

Why those modules live in the legislation directory, not next to this one:
the project has standardised on a single ``extractor/fields/`` directory
for **all** column-level extraction logic, so dashboard-specific extractors
sit alongside the law_passed-specific ones rather than being duplicated
in a sibling module. See task requirement 6.
"""

import logging

from data_pipeline.merger_csv.dashboard_csv.extractor.fields import (
    commission_answer_text,
    current_status,
    law_passed,
    registration_year,
    signatures_collected_by_country,
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
    # Provide a fallback value (e.g., False) if legislation is None
    is_law_passed = _parse_bool(legislation.Is_Law_Passed) if legislation else False
    rejected = _parse_bool(legislation.Rejected_Legislation) if legislation else False

    # ── Delegated, complex fields ─────────────────────────────────────────────
    return DashboardRow(
        registration_number=initiative.registration_number,
        title=initiative.title,
        registration_year=registration_year.extract(initiative.registration_number),
        registration_date=initiative.timeline_registered,
        current_status=current_status.extract(
            raw_status=initiative.current_status,
            is_law_passed=is_law_passed,
            rejected_legislation=rejected,
        ),
        objective=initiative.objective,
        commission_answer_text=commission_answer_text.extract(
            response.commission_answer_text if response else "",
        ),
        initiative_url=initiative.initiative_url,
        signatures_collected_by_country=signatures_collected_by_country.extract(
            initiative.signatures_collected_by_country,
        ),
        # Column rename: fro explicity
        signatures_countries_threshold_met_count=initiative.signatures_threshold_met,
        signatures_collected=initiative.signatures_collected,
        funding_total=initiative.funding_total,
        timeline_collection_closed=initiative.timeline_collection_closed,
        # Column rename: timeline_collection_start_date -> timeline_collection_start.
        timeline_collection_start=initiative.timeline_collection_start_date,
        law_passed=law_passed.extract(
            legislation.Law_Passed if legislation else "",
        ),
    )
