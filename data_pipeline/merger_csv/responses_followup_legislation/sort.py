"""
Legislation Result Sorting
Orders extracted ``LegislationResult`` rows by ``registration_number``
(earliest to latest).
"""

import logging

from .extractor import LegislationResult

logger = logging.getLogger(__name__)


def sort_results_by_registration_number(
    results: list[LegislationResult],
) -> list[LegislationResult]:
    """
    Return a new list of *results* sorted by ``registration_number`` ascending.

    Registration numbers follow the ``YYYY/NNNNNN`` format, so lexicographic
    ordering yields chronological order (earliest → latest).

    Args:
        results: Unordered legislation result rows.

    Returns:
        New list ordered by ``registration_number``.  Stable: ties (which
        should not occur in practice) preserve input order.
    """

    sorted_results = sorted(results, key=lambda r: r.registration_number)

    logger.info("Sorted %d result row(s) by registration_number", len(sorted_results))
    return sorted_results
