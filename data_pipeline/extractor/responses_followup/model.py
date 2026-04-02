"""
ECI Initiative Details Record
Analysis-ready data model for Commission response extraction.
"""

import json
from typing import Optional, List

from pydantic import BaseModel, field_serializer


class ECIResponseRecord(BaseModel):
    """Analysis-ready record for one ECI initiative's response page."""

    # --- Core metadata (copied from responses_followup_list.csv) ---
    registration_number: str
    initiative_url: str
    response_url: str
    title: str

    # --- Extracted from response followup HTML ---
    commission_answer_text: List[str] = None
    followup_events: Optional[str] = None

    @field_serializer("followup_events")
    def serialize_list_as_json(self, value: Optional[List[str]]) -> Optional[str]:

        if value is None:
            return None

        return json.dumps(value, ensure_ascii=False)
