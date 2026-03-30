"""Tests for responses.copy_fields.metadata."""

import pytest

from data_pipeline.extractor.responses.extractor.copy_fields.metadata import (
    extract_metadata,
)
from data_pipeline.extractor.responses.extractor.copy_fields.model import (
    ECIInitiativeInheritedRecord,
)

CSV_ROW = {
    "registration_number": "2020/000001",
    "url": "https://ec.europa.eu/initiative/1",
    "response_commission_url": "https://ec.europa.eu/response/1",
    "title": "Save The Bees",
}


class TestExtractMetadata:

    def test_returns_correct_type(self):

        result = extract_metadata(CSV_ROW)

        assert isinstance(result, ECIInitiativeInheritedRecord)

    def test_fields_mapped_correctly(self):

        result = extract_metadata(CSV_ROW)

        assert result.registration_number == "2020/000001"
        assert result.initiative_url == "https://ec.europa.eu/initiative/1"
        assert result.response_url == "https://ec.europa.eu/response/1"
        assert result.title == "Save The Bees"

    def test_missing_key_raises(self):

        with pytest.raises(KeyError):
            extract_metadata({"registration_number": "2020/000001"})

    def test_different_row_values(self):

        row = {
            "registration_number": "2021/000042",
            "url": "https://ec.europa.eu/initiative/42",
            "response_commission_url": "https://ec.europa.eu/response/42",
            "title": "Clean Air Now",
        }
        result = extract_metadata(row)

        assert result.registration_number == "2021/000042"
        assert result.title == "Clean Air Now"
