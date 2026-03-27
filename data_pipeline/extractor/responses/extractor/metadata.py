# data_pipeline/extractor/responses/parser/extractors/metadata.py
"""
Metadata extractor — copies response_url and initiative_url from the CSV row.
No HTML parsing required; both values are scraped upstream and stored in
responses_list.csv.
"""

from typing import Dict

from ..consts import CSV_INITIATIVES_FIELDNAMES_TO_EXTRACT


def extract_metadata(csv_record: dict) -> Dict[str, str]:
    """
    Extract metadata fields from a responses_list.csv row.

    Args:
        csv_record: Row dict loaded from responses_list.csv.

    Returns:
        Dict containing only the keys defined in
        ``CSV_INITIATIVES_FIELDNAMES_TO_EXTRACT``, falling back to an
        empty string for any missing key.
    """

    return {field: csv_record[field] for field in CSV_INITIATIVES_FIELDNAMES_TO_EXTRACT}
