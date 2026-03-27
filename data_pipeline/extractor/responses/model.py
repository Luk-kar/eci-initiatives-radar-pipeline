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
    response_url: str
    initiative_url: str
    registration_number: str
    title: str

    # --- Extracted from response HTML ---
    commission_answer_text: Optional[str] = None
    followup_additional_website: Optional[str] = None

    # List fields — serialized as JSON strings for flat CSV compatibility
    followup_events: Optional[List[str]] = None  # plain-text descriptions with links
    legislation_passed: Optional[List[str]] = None  # plain-text law descriptions

    @field_serializer("followup_events", "legislation_passed")
    def serialize_list_as_json(self, value: Optional[List[str]]) -> Optional[str]:

        if value is None:
            return None

        return json.dumps(value, ensure_ascii=False)
