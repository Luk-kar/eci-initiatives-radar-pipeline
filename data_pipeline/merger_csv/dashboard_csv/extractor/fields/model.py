"""
model.py
--------
Output dataclass for the dashboard merger.

Field order and naming match the columns of the legacy
``initiatives_<timestamp>.csv`` reference file used as the target schema.
The CSV writer emits columns in dataclass-declaration order via
``dataclasses.fields()``, so do not reorder fields without updating the
downstream renamer / dashboard consumers.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DashboardRow:
    """One row of the merged dashboard CSV (one initiative)."""

    registration_number: str
    title: str
    registration_year: str
    registration_date: str
    current_status: str
    objective: str
    commission_answer_text: str
    initiative_url: str
    signatures_collected_by_country: str
    signatures_threshold_met: str
    signatures_collected: str
    funding_total: str
    timeline_collection_closed: str
    timeline_collection_start: str
    law_passed: str
