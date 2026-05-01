"""
Orchestrates per-column regex extraction for a single ECI initiative.

``analyse_row`` is the only public entry point.  It delegates to the four
field modules under ``extractor/fields/`` and assembles the result into a
``LegislationResult`` dataclass.
"""

from __future__ import annotations

import logging

from .fields import is_law_passed as _is_law_passed
from .fields import law_passed as _law_passed
from .fields import rejected_legislation as _rejected_legislation
from .fields.model import LegislationResult

__all__ = ["analyse_row", "LegislationResult"]

logger = logging.getLogger(__name__)


def analyse_row(
    registration_number: str,
    text_items: list[str],
    *,
    commission_answer_items: list[str],
    followup_items: list[str],
) -> LegislationResult:
    """
    Run all field extractors and return a populated LegislationResult.
    """
    is_rejected = _rejected_legislation.extract(text_items)
    lp = _law_passed.extract(text_items, rejected_legislation=is_rejected)

    return LegislationResult(
        registration_number=registration_number,
        commission_answer=commission_answer_items,
        followup_events=followup_items,
        law_passed=lp,
        Is_Law_Passed=_is_law_passed.extract(lp),
        Rejected_Legislation=is_rejected,
    )
