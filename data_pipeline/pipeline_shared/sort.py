"""
Registration-Number Sorting
---------------------------
Shared helper that orders ECI pipeline records by ``registration_number``
(earliest → latest).

Registration numbers follow the ``YYYY/NNNNNN`` format, so plain
lexicographic ordering equals chronological ordering.  This module is the
single source of truth for that invariant across pipeline stages.
"""

from __future__ import annotations

import logging
from typing import Any, Iterable, TypeVar

logger = logging.getLogger(__name__)


T = TypeVar("T")


def _registration_number_of(item: Any) -> str:
    """Return ``item.registration_number`` for dataclass/pydantic rows,
    falling back to ``item['registration_number']`` for plain dicts.

    Raises:
        KeyError / AttributeError:  If the record exposes neither — callers
            must produce records that carry a registration number.
    """

    value = getattr(item, "registration_number", None)
    if value is not None:
        return value
    return item["registration_number"]


def sort_by_registration_number(results: Iterable[T]) -> list[T]:
    """
    Return a new list of *results* sorted by ``registration_number`` ascending.

    Works for any record type exposing ``registration_number`` as either an
    attribute (dataclass / pydantic model) or a mapping key (``dict`` row).

    Args:
        results: Unordered records.  Not mutated.

    Returns:
        New list ordered by ``registration_number``.  Stable: ties
        (which should not occur in real data) preserve input order.
    """

    sorted_results = sorted(results, key=_registration_number_of)

    logger.info("Sorted %d result row(s) by registration_number", len(sorted_results))
    return sorted_results
