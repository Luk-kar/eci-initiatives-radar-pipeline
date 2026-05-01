"""
model.py
--------
Output Pydantic model for the dashboard merger.

Field order and naming match the columns of the legacy
``initiatives_<timestamp>.csv`` reference file used as the target schema.
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator


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

    # Empty string allowed, or digits (0, 1, 2...) for natural numbers
    signatures_countries_threshold_met_count: str = Field(pattern=r"^(|\d+)$")

    signatures_collected: str
    funding_total: str
    timeline_collection_closed: str
    timeline_collection_start: str
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

            for country_key, stats in parsed.items():

                if not country_key or not str(country_key).strip():
                    raise ValueError("Country keys must be non-empty strings")

                if not isinstance(stats, dict):
                    raise ValueError(
                        f"Stats for {country_key} must be a JSON object (dict)"
                    )

                required_keys = {"signatures", "threshold", "percentage"}
                if not required_keys.issubset(stats.keys()):
                    raise ValueError(
                        f"Stats for {country_key} is missing required keys. Needs: {required_keys}"
                    )

                for key in required_keys:
                    val = stats[key]
                    if val is None or str(val).strip() == "":
                        raise ValueError(
                            f"Value for '{key}' in '{country_key}' cannot be empty"
                        )

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

    @model_validator(mode="after")
    def validate_cross_field_dependencies(self) -> DashboardRow:
        """Validate logical dependencies between multiple fields."""

        # 1. registration_year must be a part of the registration_number
        if self.registration_year and self.registration_number:

            if self.registration_year not in self.registration_number:
                raise ValueError(
                    f"Registration year '{self.registration_year}' is not found "
                    f"in registration number '{self.registration_number}'"
                )

        # 2. registration_date's year should be included in registration_number
        if self.registration_date and self.registration_number:

            # registration_date format is already validated as DD/MM/YYYY by field_validator
            date_year = self.registration_date.split("/")[2]

            if date_year not in self.registration_number:
                raise ValueError(
                    f"The year '{date_year}' from registration_date is not found "
                    f"in registration number '{self.registration_number}'"
                )

        # 3. timeline_collection dates ordering
        if self.timeline_collection_start and self.timeline_collection_closed:

            try:
                start_dt = datetime.strptime(self.timeline_collection_start, "%d/%m/%Y")
                closed_dt = datetime.strptime(
                    self.timeline_collection_closed, "%d/%m/%Y"
                )

                if start_dt > closed_dt:
                    raise ValueError(
                        f"Collection start date '{self.timeline_collection_start}' cannot be "
                        f"later than collection closed date '{self.timeline_collection_closed}'"
                    )
            except ValueError:
                # If date format is malformed, field_validators will catch it before this runs,
                # but a try/except blocks runtime crashes in edge cases.
                pass

        return self
