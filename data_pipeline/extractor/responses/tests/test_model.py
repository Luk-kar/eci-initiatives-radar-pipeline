"""Tests for responses.extractor.responses.model."""

import json

import pytest

from data_pipeline.extractor.responses.model import ECIResponseRecord


MINIMAL = {
    "registration_number": "2020/000001",
    "initiative_url": "https://ec.europa.eu/initiative/1",
    "response_url": "https://ec.europa.eu/response/1",
    "title": "Test Initiative",
}


class TestECIResponseRecord:
    def test_required_fields_only(self):

        record = ECIResponseRecord(**MINIMAL)
        assert record.registration_number == "2020/000001"
        assert record.commission_answer_text is None
        assert record.followup_events is None
        assert record.legislation_passed is None

    def test_all_fields(self):

        record = ECIResponseRecord(
            **MINIMAL,
            commission_answer_text="The Commission answers…",
            followup_additional_website="https://example.com",
            followup_events=["Event A", "Event B"],
            legislation_passed=["Regulation (EU) 2021/1"],
        )
        assert record.followup_events == ["Event A", "Event B"]
        assert record.legislation_passed == ["Regulation (EU) 2021/1"]

    def test_list_fields_serialized_as_json(self):

        record = ECIResponseRecord(
            **MINIMAL,
            followup_events=["Event A", "Event B"],
            legislation_passed=["Law 1"],
        )

        dumped = record.model_dump()

        assert dumped["followup_events"] == json.dumps(
            ["Event A", "Event B"], ensure_ascii=False
        )
        assert dumped["legislation_passed"] == json.dumps(["Law 1"], ensure_ascii=False)

    def test_none_list_fields_stay_none_in_dump(self):

        record = ECIResponseRecord(**MINIMAL)
        dumped = record.model_dump()

        assert dumped["followup_events"] is None
        assert dumped["legislation_passed"] is None

    def test_model_dump_keys_match_model_fields(self):

        record = ECIResponseRecord(**MINIMAL)

        assert set(record.model_dump().keys()) == set(
            ECIResponseRecord.model_fields.keys()
        )

    def test_missing_required_field_raises(self):

        with pytest.raises(Exception):
            ECIResponseRecord(registration_number="2020/000001")
