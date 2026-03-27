"""
Focused extractor classes for the ECI response page sections.
"""

from .commission_answer import CommissionAnswerExtractor
from .followup_details import FollowUpDetailsExtractor
from .legislation import LegislationPassedExtractor

__all__ = [
    "CommissionAnswerExtractor",
    "FollowUpDetailsExtractor",
    "LegislationPassedExtractor",
]
