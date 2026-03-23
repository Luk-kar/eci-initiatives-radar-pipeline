#!/usr/bin/env python3
"""
ECI Data Models
Data structures for ECI initiative information
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ECIInitiativeDetailsRecord:
    """Data structure for ECI initiative information"""

    registration_number: str
    title: str
    objective: str
    annex: Optional[str]
    current_status: str
    url: str

    timeline_registered: Optional[str]
    timeline_collection_start_date: Optional[str]
    timeline_collection_closed: Optional[str]
    timeline_verification_start: Optional[str]
    timeline_verification_end: Optional[str]
    timeline_response_commission_date: Optional[str]

    timeline: Optional[str]

    funding_total: Optional[str]
    funding_by: Optional[str]

    signatures_collected: Optional[str]
    signatures_collected_by_country: Optional[str]
    signatures_threshold_met: Optional[str]

    response_commission_url: Optional[str]
