"""
data_pipeline.merger_csv.responses_followup_legislation.fields
==============================================================
Per-column extraction modules for the legislation pipeline step.

Public API
----------
Each submodule exposes a single ``extract()`` function and, where applicable,
a ``PATTERNS`` list for inspection or extension.

    from data_pipeline.merger_csv.responses_followup_legislation.fields import (
        law_passed,
        is_law_passed,
        rejected_legislation,
    )
    from data_pipeline.merger_csv.responses_followup_legislation.fields.model import (
        LegislationResult,
    )
"""

from . import is_law_passed, law_passed, rejected_legislation
from .model import LegislationResult

__all__ = [
    "LegislationResult",
    "law_passed",
    "is_law_passed",
    "rejected_legislation",
]
