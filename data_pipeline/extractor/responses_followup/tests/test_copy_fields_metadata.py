"""Tests for responses_followup.extractor.copy_fields.metadata."""

import pytest

from data_pipeline.extractor.responses_followup.extractor.copy_fields.metadata import (
    extract_metadata,
)
# FIX 1: the model class was renamed from ECIInitiativeInheritedRecord to
#         ECIResponseInheritedRecord; the old name does not exist in the module.
from data_pipeline.extractor.responses_followup.extractor.copy_fields.model import (
    ECIResponseInheritedRecord,
)

# FIX 2: CSV_ROW keys updated to match what extract_metadata() now reads:
#   'url'                     → 'initiative_url'
#   'response_commission_url' → 'response_url'
#   (new)                       'followup_url'   — required by ECIResponseInheritedRecord
CSV_ROW = {
    "registration_number": "2020/000001",
    "initiative_url": "https://ec.europa.eu/initiative/1",
    "response_url": "https://ec.europa.eu/response/1",
    "followup_url": "https://ec.europa.eu/followup/1",
    "title": "Save The Bees",
}


class TestExtractMetadata:

    def test_returns_correct_type(self):

        result = extract_metadata(CSV_ROW)

        # FIX 1: assert against ECIResponseInheritedRecord (not ECIInitiativeInheritedRecord)
        assert isinstance(result, ECIResponseInheritedRecord)

    def test_fields_mapped_correctly(self):

        result = extract_metadata(CSV_ROW)

        assert result.registration_number == "2020/000001"
        # FIX 2: assertions use current field names on the model
        assert result.initiative_url == "https://ec.europa.eu/initiative/1"
        assert result.response_url == "https://ec.europa.eu/response/1"
        assert result.followup_url == "https://ec.europa.eu/followup/1"
        assert result.title == "Save The Bees"

    def test_missing_key_raises(self):

        with pytest.raises(KeyError):
            extract_metadata({"registration_number": "2020/000001"})

    def test_different_row_values(self):

        row = {
            "registration_number": "2021/000042",
            "initiative_url": "https://ec.europa.eu/initiative/42",
            "response_url": "https://ec.europa.eu/response/42",
            "followup_url": "https://ec.europa.eu/followup/42",
            "title": "Clean Air Now",
        }
        result = extract_metadata(row)

        assert result.registration_number == "2021/000042"
        assert result.title == "Clean Air Now"
        assert result.followup_url == "https://ec.europa.eu/followup/42"
