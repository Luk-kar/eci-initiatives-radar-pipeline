"""
data_pipeline.merger_csv.page_dashboard.extractor.fields
=========================================================
Per-column extraction modules for the dashboard merger.

Each module owns a single dashboard column whose value cannot be derived by
direct copy / rename / type cast from the source CSVs. Simple fields are
handled inline by :func:`data_pipeline.merger_csv.page_dashboard.extractor.analyse_row`.

All modules below are placeholders and raise ``NotImplementedError``.
"""

from . import (
    current_status,
    commission_answer_text,
    legislation,
    url,
    signatures_collected_by_country,
)

__all__ = [
    "current_status",
    "commission_answer_text",
    "legislation",
    "url",
    "signatures_collected_by_country",
]
