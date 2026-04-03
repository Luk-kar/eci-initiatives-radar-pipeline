# data_pipeline/extractor/responses/parser/fields/__init__.py
"""
Focused extractor functions for the ECI response page sections.
"""

from .commission_answer import extract_commission_answer
from .followup_details import (
    extract_followup_events,
)

__all__ = [
    "extract_commission_answer",
    "extract_followup_events",
]
