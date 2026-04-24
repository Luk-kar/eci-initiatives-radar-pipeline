"""
Legislation Extraction Settings
Defines shared names and output metadata for the legislation pipeline step.
"""

from dataclasses import fields as dataclass_fields

from .extractor import LegislationResult

OUTPUT_FIELDNAMES: list[str] = [f.name for f in dataclass_fields(LegislationResult)]

RESPONSES_GLOB = "eci_responses_[0-9]*.csv"
FOLLOWUP_GLOB = "eci_responses_followup_[0-9]*.csv"

RESPONSES_COLS = ("registration_number", "commission_answer_text")
FOLLOWUP_COLS = ("registration_number", "followup_events")