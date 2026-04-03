"""Tests for responses_followup.model."""

import json

import pytest

from data_pipeline.extractor.responses_followup.model import ECIFollowupRecord


MINIMAL = {
    "registration_number": "2020/000001",
    "initiative_url": "https://ec.europa.eu/initiative/1",
    "response_url": "https://ec.europa.eu/response/1",
    "followup_url": "https://ec.europa.eu/followup/1",
    "title": "Test Initiative",
    "commission_answer_text": ["The Commission will act on this matter."],
}


class TestECIFollowupRecord:

    def test_required_fields_only(self):

        record = ECIFollowupRecord(**MINIMAL)

        assert record.registration_number == "2020/000001"
        assert record.commission_answer_text == [
            "The Commission will act on this matter."
        ]
        assert record.followup_events is None

    def test_all_fields(self):

        record = ECIFollowupRecord(
            **MINIMAL,
            followup_events=["Event A", "Event B"],
        )
        assert record.followup_events == ["Event A", "Event B"]

    def test_list_fields_serialized_as_json(self):

        record = ECIFollowupRecord(
            **MINIMAL,
            followup_events=["Event A", "Event B"],
        )

        dumped = record.model_dump()

        assert dumped["followup_events"] == json.dumps(
            ["Event A", "Event B"], ensure_ascii=False
        )

    def test_none_list_fields_stay_none_in_dump(self):

        record = ECIFollowupRecord(**MINIMAL)
        dumped = record.model_dump()

        assert dumped["followup_events"] is None

    def test_model_dump_keys_match_model_fields(self):

        record = ECIFollowupRecord(**MINIMAL)

        assert set(record.model_dump().keys()) == set(
            ECIFollowupRecord.model_fields.keys()
        )

    def test_missing_required_field_raises(self):

        with pytest.raises(Exception):
            ECIFollowupRecord(registration_number="2020/000001")
