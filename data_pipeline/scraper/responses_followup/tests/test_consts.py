"""
Tests for configuration constants in the Commission responses follow-up scraper.
"""

import fnmatch

import pytest

from data_pipeline.scraper.responses_followup.consts import (
    WAIT_BETWEEN_DOWNLOADS,
    RETRY_WAIT_BASE,
    DEFAULT_MAX_RETRIES,
    WEBDRIVER_TIMEOUT_DEFAULT,
    WEBDRIVER_TIMEOUT_CONTENT,
    RESPONSES_CSV_GLOB,
    FOLLOWUP_URL_COLUMN,
    RESPONSES_DIR_NAME,
)

_WAIT_TUPLES = [
    ("WAIT_BETWEEN_DOWNLOADS", WAIT_BETWEEN_DOWNLOADS),
    ("RETRY_WAIT_BASE", RETRY_WAIT_BASE),
]


class TestWaitTuples:
    """
    Validates wait time constants are two-element tuples with a valid range.
    """

    @pytest.mark.parametrize("name,constant", _WAIT_TUPLES)
    def test_is_two_element_tuple(self, name, constant):

        assert isinstance(constant, tuple), f"{name} must be a tuple"
        assert len(constant) == 2, f"{name} must have exactly 2 elements"

    @pytest.mark.parametrize("name,constant", _WAIT_TUPLES)
    def test_lower_bound_less_than_upper_bound(self, name, constant):
        assert constant[0] < constant[1], f"{name}[0] must be < {name}[1]"

    @pytest.mark.parametrize("name,constant", _WAIT_TUPLES)
    def test_both_values_non_negative(self, name, constant):

        assert constant[0] >= 0, f"{name}[0] must be >= 0"
        assert constant[1] > 0, f"{name}[1] must be > 0"


class TestNumericConsts:
    """
    Validates scalar numeric constants are positive and correctly typed.
    """

    def test_default_max_retries_is_positive_int(self):
        assert isinstance(DEFAULT_MAX_RETRIES, int)
        assert DEFAULT_MAX_RETRIES > 0

    def test_webdriver_timeout_default_is_positive(self):
        assert WEBDRIVER_TIMEOUT_DEFAULT > 0

    def test_webdriver_timeout_content_is_positive(self):
        assert WEBDRIVER_TIMEOUT_CONTENT > 0


# class TestStringConsts:

#     def test_responses_csv_glob_matches_extractor_output(self):
#         assert fnmatch.fnmatch(
#             "eci_responses_2026-03-31_16-26-53.csv", RESPONSES_CSV_GLOB
#         )

#     def test_followup_url_column_is_non_empty_string(self):
#         assert isinstance(FOLLOWUP_URL_COLUMN, str)
#         assert FOLLOWUP_URL_COLUMN.strip()

#     def test_responses_dir_name_is_responses_followup(self):
#         assert RESPONSES_DIR_NAME == "responses_followup"
