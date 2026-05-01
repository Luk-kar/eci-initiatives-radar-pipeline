"""
objective
---------
Clean and normalize the objective text for the dashboard.
"""

from .utils._regex import normalize_newlines


def extract(raw_objective: str | None) -> str:
    """
    Return the dashboard-ready objective text.
    Strips outer whitespace and collapses multiple internal newlines.
    """
    if not raw_objective or not str(raw_objective).strip():
        return ""

    cleaned = raw_objective.strip()
    return normalize_newlines(cleaned)
