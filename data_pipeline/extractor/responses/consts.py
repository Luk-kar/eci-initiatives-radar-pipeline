# data_pipeline/extractor/responses/const.py
"""
Constants and configuration for the Commission responses extractor.
"""

from pathlib import Path

from data_pipeline.pipeline_shared.consts import (
    FilePatterns,
)

# Input CSV
CSV_FILENAME = "responses_list.csv"
CSV_INITIATIVES_FIELDNAMES_TO_EXTRACT = [
    "registration_number",
    "url",
    "response_commission_url",
    "title",
]

# File naming pattern for HTML response files
RESPONSE_PAGE_FILENAME_PATTERN = "{year}_{number}_en.html"

# Output CSV
OUTPUT_CSV_FIELDNAMES = [
    "registration_number",
    "initiative_url",
    "response_url",
    "title",
    "commission_answer_text",
    "followup_additional_website",
    "followup_events",
    "legislation_passed",
]
