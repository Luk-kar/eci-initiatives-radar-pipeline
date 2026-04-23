"""
is_law_passed.py
----------------
Derivation logic for the ``Is_Law_Passed`` output column.

This is intentionally a thin module: ``Is_Law_Passed`` is fully determined by
whether ``Law_Passed`` is a non-empty list or ``None``.  Keeping it separate
makes the field boundary explicit and testable in isolation.
"""

from __future__ import annotations


def extract(law_passed: list[str] | None) -> bool:
    """
    Derive ``Is_Law_Passed`` from the ``Law_Passed`` field.

    Args:
        law_passed: Value already computed by ``law_passed.extract()``.

    Returns:
        ``True`` when *law_passed* contains at least one valid, non-empty string.
        ``False`` otherwise (e.g., None, [], [" "], [None]).
    """
    if not law_passed:
        return False
        
    # Returns True if any item exists and contains characters other than whitespace
    return any(item and item.strip() for item in law_passed)