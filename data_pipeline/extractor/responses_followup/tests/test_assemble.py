"""Tests for ...extractor.assemble."""

import pytest

from data_pipeline.extractor.responses.extractor.assemble import build_records
from data_pipeline.extractor.responses.model import ECIFollowupRecord

METADATA = {
    "2020/000001": {
        "registration_number": "2020/000001",
        "url": "https://ec.europa.eu/initiative/1",
        "response_commission_url": "https://ec.europa.eu/response/1",
        "title": "Save The Bees",
    }
}
PARSED = {
    "2020/000001": {
        "commission_answer_text": ["The Commission will act."],
        "followup_additional_website": None,
        "followup_events": None,
    }
}


class TestBuildRecords:

    def test_returns_list_of_eci_response_records(self):

        assert all(
            isinstance(r, ECIFollowupRecord) for r in build_records(METADATA, PARSED)
        )

    def test_metadata_fields_copied(self):

        r = build_records(METADATA, PARSED)[0]

        assert r.registration_number == "2020/000001"
        assert r.title == "Save The Bees"
        assert r.initiative_url == "https://ec.europa.eu/initiative/1"
        assert r.response_url == "https://ec.europa.eu/response/1"

    def test_parsed_fields_merged(self):

        assert build_records(METADATA, PARSED)[0].commission_answer_text == [
            "The Commission will act."
        ]

    def test_multiple_records(self):
        """
        build_records should return one ECIFollowupRecord per entry in parsed_data.
        Verifies that the function iterates over all parsed entries, not just the first.
        """

        metadata = {
            **METADATA,
            "2021/000002": {
                "registration_number": "2021/000002",
                "url": "u2",
                "response_commission_url": "r2",
                "title": "Clean Air",
            },
        }
        parsed = {
            **PARSED,
            "2021/000002": {
                "commission_answer_text": None,
                "followup_additional_website": None,
                "followup_events": None,
            },
        }

        assert len(build_records(metadata, parsed)) == 2

    def test_empty_parsed_returns_empty_list(self):

        result = build_records(METADATA, {})

        assert result == []

    def test_missing_metadata_key_raises(self):

        parsed = {
            "2020/MISSING": {
                "commission_answer_text": None,
                "followup_additional_website": None,
                "followup_events": None,
            }
        }

        with pytest.raises(KeyError):
            build_records(METADATA, parsed)
