"""
model.py
--------
Output Pydantic model for the dashboard merger.

Field order and naming match the columns of the legacy
``initiatives_<timestamp>.csv`` reference file used as the target schema.
"""

# to pass in tests the:
# NameError: name 'DashboardRow' is not defined
from __future__ import annotations

import ast
import json
import re
from datetime import datetime
import math
from typing import Literal, Any

from pydantic import BaseModel, Field, field_validator, model_validator


class DashboardRow(BaseModel):
    """One row of the merged dashboard CSV (one initiative)."""

    registration_number: str = Field(pattern=r"^\d{4}/\d{6}$")
    title: str = Field(min_length=1)
    registration_year: int = Field(ge=2012, le=2099)
    registration_date: str = Field(pattern=r"^\d{2}/\d{2}/\d{4}$")

    current_status: Literal[
        "Awaiting Collection",
        "Collection Ongoing",
        "Collection Verification",
        "Collection Unsuccessful",
        "Insufficient Verified Signatures",
        "Awaiting Response",
        "Commission Engaged",
        "Law Passed",
        "Rejected Legislation",
        "Withdrawn",
    ]

    objective: str = Field(min_length=1)
    commission_answer: str | None = None

    initiative_url: str = Field(
        pattern=r"^https://citizens-initiative\.europa\.eu/initiatives/details/\d{4}/\d{6}_en$"
    )

    signatures_collected_by_country: str | None = None
    signatures_countries_threshold_met_count: int | None = None
    signatures_collected: int | None = None
    funding_total: float | None = None
    timeline_collection_closed: str | None = None
    timeline_collection_start: str | None = None
    law_passed: list[str] | None = None

    @field_validator("signatures_collected_by_country")
    @classmethod
    def validate_signatures_dict_string(cls, v: str | None) -> str | None:

        if not v or not str(v).strip():
            return None

        try:

            parsed = ast.literal_eval(v)

            if not isinstance(parsed, dict):
                raise ValueError("Must be a stringified dictionary object")

            for country_key, stats in parsed.items():

                if not country_key or not str(country_key).strip():
                    raise ValueError("Country keys must be non-empty strings")

                if not isinstance(stats, dict):
                    raise ValueError(f"Stats for {country_key} must be a dictionary")

                required_keys = {"signatures", "threshold", "percentage"}
                if not required_keys.issubset(stats.keys()):
                    raise ValueError(
                        f"Stats for {country_key} is missing required keys. Needs: {required_keys}"
                    )

                # Ensure values are strictly numbers
                for key in required_keys:
                    val = stats[key]
                    if val is None:
                        raise ValueError(
                            f"Value for '{key}' in '{country_key}' cannot be None"
                        )
                    if not isinstance(val, (int, float)):
                        raise ValueError(
                            f"Value for '{key}' in '{country_key}' must be numeric"
                        )

            # Return the original string exactly as it is
            return v

        except (ValueError, SyntaxError) as exc:
            # literal_eval throws ValueError or SyntaxError on malformed strings
            raise ValueError(f"Must be a valid stringified dictionary: {exc}")

    @field_validator(
        "signatures_collected",
        "signatures_countries_threshold_met_count",
        mode="before",
    )
    @classmethod
    def validate_natural_number_fields(cls, v: Any) -> int | None:

        # 1. Can be empty value if the campaign not started
        # registered but for some reasons organization
        # didn't start collecting in designated time
        if v is None or (isinstance(v, str) and not v.strip()):
            return None

        # 2. Parse the value, allowing for comma-formatted strings
        try:
            if isinstance(v, str):
                v_clean = v.replace(",", "").strip()
                val = int(v_clean)
            else:
                val = int(v)
        except (ValueError, TypeError) as exc:
            raise ValueError(
                f"signatures_collected must be a valid integer, got {v!r}"
            ) from exc

        # 3. Enforce natural number constraint (>= 0)
        if val < 0:
            raise ValueError(
                f"signatures_collected must be a natural number (>= 0), got {val}"
            )

        return val

    @field_validator("funding_total", mode="before")
    @classmethod
    def validate_funding_float(cls, v: Any) -> float | None:
        # 1. Can be None (Empty values if campaign has no funding data)
        if v is None or (isinstance(v, str) and not v.strip()):
            return None

        # 2. Strict parsing for floats
        try:
            if isinstance(v, str):
                v_clean = v.replace(",", "").strip()
                val = float(v_clean)
            else:
                val = float(v)
        except (ValueError, TypeError) as exc:
            raise ValueError(f"funding_total must be a valid float, got {v!r}") from exc

        # 3. Reject NaN and Infinity which python float() natively allows
        if math.isnan(val) or math.isinf(val):
            raise ValueError(
                f"funding_total must be a standard number, cannot be NaN or Infinity. Got {v!r}"
            )

        # 4. Enforce exactly 0 or a positive float
        if val < 0:
            raise ValueError(
                f"funding_total must be 0 or a positive float (>= 0), got {val}"
            )

        return val

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

            if str(self.registration_year) not in self.registration_number:
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
