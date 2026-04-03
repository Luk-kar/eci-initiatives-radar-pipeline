# data_pipeline/extractor/responses/parser/extractors/metadata.py
"""
Metadata extractor — copies response_url and initiative_url from the CSV row.
No HTML parsing required; both values are scraped upstream and stored in
responses_list.csv.
"""

from typing import Dict

from .model import ECIInitiativeInheritedRecord


def extract_metadata(csv_record: dict) -> ECIInitiativeInheritedRecord:
    return ECIInitiativeInheritedRecord(
        registration_number=csv_record["registration_number"],
        initiative_url=csv_record["initiative_url"],
        response_url=csv_record["response_url"],
        title=csv_record["title"],
    )
