import pytest

from data_pipeline.extractor.initiatives.parser.fields.registration_number import (
    extract_registration_number,
)
from data_pipeline.extractor.extractor_shared.errors import FieldValueError


def test_registration_number_parses_en_filename():
    # Matches FilePatterns.FILENAME_REGEX: (\d{4})_(\d{6})_en\.html
    result = extract_registration_number("2023_000001_en.html")
    assert result == "2023/000001"


def test_registration_number_rejects_generic_lang_filename_for_now():
    # HTML_FILENAME_PATTERN captures 3 groups, but the extractor currently
    # assumes only (year, number), so such filenames are not yet supported.
    with pytest.raises(FieldValueError):
        extract_registration_number("2020_000001_fr.html")


def test_registration_number_formats_separator_correctly():
    result = extract_registration_number("2019_000007_en.html")
    assert result == "2019/000007"


def test_registration_number_raises_for_unrecognised_filename():
    with pytest.raises(FieldValueError) as excinfo:
        extract_registration_number("not_a_valid_filename.html")
    msg = str(excinfo.value)
    assert "Cannot extract registration number" in msg
    assert "not_a_valid_filename.html" in msg


def test_registration_number_raises_for_missing_lang_suffix():
    # Looks close but missing '_xx' language; should fail
    with pytest.raises(FieldValueError):
        extract_registration_number("2023_000001.html")
