"""
Tests for the configuration constants used by the Commission responses scraper.

Verifies that wait time tuples are correctly bounded, retry limits are
positive integers, and WebDriver timeouts are set to sane values.
"""

import pytest

from data_pipeline.scraper.responses.consts import (
    WAIT_BETWEEN_DOWNLOADS,
    RETRY_WAIT_BASE,
    DEFAULT_MAX_RETRIES,
    WEBDRIVER_TIMEOUT_DEFAULT,
    WEBDRIVER_TIMEOUT_CONTENT,
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
