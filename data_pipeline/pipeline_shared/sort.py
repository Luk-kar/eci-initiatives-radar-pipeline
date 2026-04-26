"""Shared helper: order any record-like sequence by ``registration_number``."""

import logging
from typing import Protocol, TypeVar

logger = logging.getLogger(__name__)


class _HasRegistrationNumber(Protocol):
    registration_number: str


T = TypeVar("T", bound=_HasRegistrationNumber)


def sort_by_registration_number(records: list[T]) -> list[T]:
    """
    Return *records* sorted ascending by ``registration_number``.

    Registration numbers follow ``YYYY/NNNNNN``, so lexicographic ordering
    yields chronological order (earliest → latest).  The sort is stable.
    """
    sorted_records = sorted(records, key=lambda r: r.registration_number)
    logger.info("Sorted %d record(s) by registration_number", len(sorted_records))
    return sorted_records
