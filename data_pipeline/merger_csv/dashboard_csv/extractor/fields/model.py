"""
model.py
--------
Output Pydantic model for the dashboard merger.

Field order and naming match the columns of the legacy
``initiatives_<timestamp>.csv`` reference file used as the target schema.
"""

import json
import re
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class DashboardRow(BaseModel):
    """One row of the merged dashboard CSV (one initiative)."""

    registration_number: str = Field(pattern=r"^\d{4}/\d{6}$")
    title: str = Field(min_length=1)
    registration_year: str = Field(pattern=r"^(201[2-9]|20[2-9]\d)$")
    registration_date: str = Field(pattern=r"^\d{2}/\d{2}/\d{4}$")

    current_status: Literal[
        "Collection Unsuccessful",
        "Withdrawn",
        "Law Passed",
        "Rejected Legislation",
        "Collection Verification",
        "Commission Engaged",
        "Awaiting Response",
        "Collection Ongoing",
        "Awaiting Collection",
    ]

    objective: str = Field(min_length=1)
    commission_answer_text: str
    initiative_url: str = Field(
        pattern=r"^https://citizens-initiative\.europa\.eu/initiatives/details/\d{4}/\d{6}_en$"
    )
    signatures_collected_by_country: str
    signatures_countries_threshold_met_count: str
    signatures_collected: str
    funding_total: str
    timeline_collection_start: str
    timeline_collection_closed: str
    law_passed: str

    @field_validator("signatures_collected_by_country")
    @classmethod
    def validate_signatures_json(cls, v: str) -> str:

        if not v:
            return v

        try:
            parsed = json.loads(v)

            if not isinstance(parsed, dict):
                raise ValueError("Must be a JSON object")

        except json.JSONDecodeError:
            raise ValueError("Must be valid JSON")

        return v

    @field_validator("signatures_collected", "funding_total")
    @classmethod
    def validate_comma_formatted_numbers(cls, v: str) -> str:

        if not v:
            return v

        if not re.match(r"^\d{1,3}(,\d{3})*(\.\d+)?$", v):
            raise ValueError(f"Value '{v}' is not a valid comma-formatted number")

        return v

    @field_validator("timeline_collection_closed", "timeline_collection_start")
    @classmethod
    def validate_dates(cls, v: str) -> str:

        if not v:
            return v

        if not re.match(r"^\d{2}/\d{2}/\d{4}$", v):
            raise ValueError(f"Date '{v}' must be in DD/MM/YYYY format")

        return v
