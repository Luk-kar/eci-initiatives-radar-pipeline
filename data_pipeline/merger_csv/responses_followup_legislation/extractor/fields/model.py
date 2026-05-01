"""
model.py
--------
Shared output dataclass for the legislation-extraction pipeline step.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class LegislationResult:
    registration_number: str
    commission_answer: list[str] | None = None  # For debugging
    followup_events: list[str] | None = None  # For debugging
    Law_Passed: list[str] | None = None
    """Matched text spans from LAW_MENTIONED patterns, or None if no match fired."""
    Is_Law_Passed: bool = False
    """True when Law_Passed is a non-empty list."""
    Rejected_Legislation: bool = False
    """True when any REJECTED_LEGISLATION pattern matched."""
