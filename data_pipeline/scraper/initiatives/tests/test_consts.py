"""
Tests for the configuration constants used by the ECI initiatives scraper.

This module verifies that all timeout values, retry limits, and randomized
wait time ranges are correctly defined with valid types and logical bounds.
This ensures the scraper operates with safe, predictable delays and timeouts.
"""

# Third-party
import pytest

# Local
from data_pipeline.scraper.initiatives.consts import (
    WAIT_DYNAMIC_CONTENT,
    WAIT_BETWEEN_DOWNLOADS,
    WAIT_BETWEEN_PAGES,
    RETRY_WAIT_BASE,
    DEFAULT_MAX_RETRIES,
    WEBDRIVER_TIMEOUT_DEFAULT,
    WEBDRIVER_TIMEOUT_CONTENT,
)

_WAIT_TUPLES = [
    ("WAIT_DYNAMIC_CONTENT", WAIT_DYNAMIC_CONTENT),
    ("WAIT_BETWEEN_DOWNLOADS", WAIT_BETWEEN_DOWNLOADS),
    ("WAIT_BETWEEN_PAGES", WAIT_BETWEEN_PAGES),
    ("RETRY_WAIT_BASE", RETRY_WAIT_BASE),
]


class TestWaitTuples:
    """
    Test suite for randomized wait time configurations.

    Validates that wait time constants (like WAIT_DYNAMIC_CONTENT) are properly
    formatted as two-element tuples representing lower and upper bounds. It ensures
    both values are non-negative and that the lower bound is strictly less than
    the upper bound.
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
    Test suite for scalar numeric configuration constants.

    Validates that individual threshold limits, such as maximum retries and
    WebDriver timeouts, are properly defined as positive integers or numbers.
    """

    def test_default_max_retries_is_positive_int(self):
        assert isinstance(DEFAULT_MAX_RETRIES, int)
        assert DEFAULT_MAX_RETRIES > 0

    def test_webdriver_timeout_default_is_positive(self):
        assert WEBDRIVER_TIMEOUT_DEFAULT > 0

    def test_webdriver_timeout_content_is_positive(self):
        assert WEBDRIVER_TIMEOUT_CONTENT > 0
