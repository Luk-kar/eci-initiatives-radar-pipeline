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
) -> LegislationResult:
    """
    Run all field extractors against *text_items* and return a populated
    ``LegislationResult``.

    Each field is computed independently:
    - ``Rejected_Legislation`` → ``fields.rejected_legislation.extract``
    - ``Law_Passed``           → ``fields.law_passed.extract`` (skips if rejected)
    - ``Is_Law_Passed``        → ``fields.is_law_passed.extract`` (derived from Law_Passed)

    Args:
        registration_number: Unique ECI identifier (e.g. ``"ECI(2019)000007"``).
        text_items:          Pre-merged list of text fragments from
                             ``_merge_text_lists`` in ``__main__.py``.

    Returns:
        Populated ``LegislationResult`` instance.
    """
    # 1. Determine if the legislation was explicitly rejected
    is_rejected = _rejected_legislation.extract(text_items)

    # 2. Extract law passed, skipping the logic if the initiative was rejected
    lp = _law_passed.extract(text_items, rejected_legislation=is_rejected)

    result = LegislationResult(
        registration_number=registration_number,
        followup_events=text_items,
        Law_Passed=lp,
        Is_Law_Passed=_is_law_passed.extract(lp),
        Rejected_Legislation=is_rejected,
    )
    
    logger.info(
        "Analysed %s: rejected=%s, law_passed=%s, matched_items=%d",
        registration_number,
        result.Rejected_Legislation,
        result.Is_Law_Passed,
        len(result.Law_Passed) if result.Law_Passed else 0,
    )
    
    return result