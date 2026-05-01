"""
ECI Initiative Details Record
Analysis-ready data model for Commission response extraction.
"""

import json
from typing import Optional, List

from pydantic import BaseModel, field_serializer


class ECIResponseRecord(BaseModel):
    """Analysis-ready record for one ECI initiative's response page."""

    # --- Core metadata (copied from responses_list.csv) ---
    registration_number: str
    initiative_url: str  # For debug purposes
    response_url: str
    title: str

    # --- Extracted from response HTML ---
    # List instead of a single string to keep text partitioned by HTML code
    commission_answer: Optional[List[str]] = None
    followup_url: Optional[str] = None

    # List fields — serialized as JSON strings for flat CSV compatibility
    # List instead of a single string to keep text partitioned by HTML code
    followup_events: Optional[List[str]] = None

    @field_serializer("followup_events")
    def serialize_list_as_json(self, value: Optional[List[str]]) -> Optional[str]:

        if value is None:
            return None

        return json.dumps(value, ensure_ascii=False)
