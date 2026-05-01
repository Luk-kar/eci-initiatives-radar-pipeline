#!/usr/bin/env python3
"""
ECI Data Models
Data structures for ECI initiative information
"""

from typing import Optional, Any

from pydantic import BaseModel, Json, Field, field_validator


class TimelineEvent(BaseModel):
    """
    Represents a single event in the ECI initiative's lifecycle timeline.

    Example JSON data:
    {
        "step": "Registered",
        "date": "10/05/2012"
    }

    If the date is not yet known, `date` may be null / missing.
    For example for `Collection ongoing` step
    """

    step: str
    date: Optional[str] = None


class Sponsor(BaseModel):
    """
    Represents a financial sponsor or donor supporting the initiative.

    Example JSON data:
    {
        "name_of_sponsor": "European Federation of Public Service Unions (EPSU)",
        "date": "28/11/2013",
        "amount_in_eur": "20,000"
    }
    """

    name_of_sponsor: str
    date: str
    amount_in_eur: str


class CountrySignatureStats(BaseModel):
    """
    Represents the signature collection statistics for a specific EU member state.

    Example JSON data (typically nested under a country code like "DE"):
    {
        "signatures": 150430,
        "threshold": 71695,
        "percentage": 209.82
    }
    """

    signatures: int
    threshold: int
    percentage: float

    @field_validator("signatures", "threshold", mode="before")
    @classmethod
    def clean_integer_strings(cls, value: Any) -> Any:
        if isinstance(value, str):
            # Remove commas, asterisks, and whitespace before casting to int
            return value.replace(",", "").replace("*", "").strip()
        return value

    @field_validator("percentage", mode="before")
    @classmethod
    def clean_float_strings(cls, value: Any) -> Any:
        if isinstance(value, str):
            # Remove commas, percent signs, and whitespace before casting to float
            return value.replace(",", "").replace("%", "").strip()
        return value


class ECIInitiativeDetailsRecord(BaseModel):
    """Data structure for ECI initiative information"""

    registration_number: str
    title: str
    objective: str
    annex: Optional[str]
    current_status: str
    initiative_url: str

    timeline_registered: str
    timeline_collection_start_date: Optional[str]
    timeline_collection_closed: Optional[str]
    timeline_verification_start: Optional[str]
    timeline_verification_end: Optional[str]
    timeline_response_commission_date: Optional[str]

    timeline: Json[list[TimelineEvent]]

    funding_total: Optional[str]
    funding_by: Optional[Json[list[Sponsor]]] = None

    signatures_collected: Optional[str]
    signatures_collected_by_country: Optional[
        Json[dict[str, CountrySignatureStats]]
    ] = None
    signatures_countries_threshold_met_count: Optional[str]

    response_url: Optional[str]
