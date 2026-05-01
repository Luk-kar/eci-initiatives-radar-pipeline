"""
ECI Response Follow-up Record
Analysis-ready data model for Commission response follow-up website extraction.
"""

import json
from typing import Optional, List

from pydantic import BaseModel, field_serializer


class ECIFollowupRecord(BaseModel):
    """Analysis-ready record for one ECI initiative's follow-up website page."""

    # --- Core metadata (copied from responses_followup_list.csv) ---
    registration_number: str
    initiative_url: str  # For debug purposes
    response_url: str  # For debug purposes
    followup_url: str
    title: str

    # --- Extracted from response followup HTML ---
    # List instead of a single string to keep text partitioned by HTML code
    commission_answer: List[str]
    followup_events: Optional[List[str]] = None

    @field_serializer("followup_events")
    def serialize_list_as_json(self, value: Optional[List[str]]) -> Optional[str]:

        if value is None:
            return None

        return json.dumps(value, ensure_ascii=False)
