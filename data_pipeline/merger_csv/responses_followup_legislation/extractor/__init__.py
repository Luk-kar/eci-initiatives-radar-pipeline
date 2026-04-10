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
    - ``Law_Passed``           → ``fields.law_passed.extract``
    - ``Is_Law_Passed``        → ``fields.is_law_passed.extract`` (derived from Law_Passed)
    - ``Rejected_Legislation`` → ``fields.rejected_legislation.extract``

    Args:
        registration_number: Unique ECI identifier (e.g. ``"ECI(2019)000007"``).
        text_items:          Pre-merged list of text fragments from
                             ``_merge_text_lists`` in ``__main__.py``.

    Returns:
        Populated ``LegislationResult`` instance.
    """
    lp = _law_passed.extract(text_items)

    result = LegislationResult(
        registration_number=registration_number,
        Law_Passed=lp,
        Is_Law_Passed=_is_law_passed.extract(lp),
        Rejected_Legislation=_rejected_legislation.extract(text_items),
    )

    logger.debug(
        "%s → Is_Law_Passed=%s  Rejected=%s  spans=%d",
        registration_number,
        result.Is_Law_Passed,
        result.Rejected_Legislation,
        len(result.Law_Passed) if result.Law_Passed else 0,
    )
    return result
