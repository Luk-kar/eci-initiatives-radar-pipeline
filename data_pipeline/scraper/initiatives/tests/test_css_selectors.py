"""
Tests for CSS selectors used in the ECI initiative scraper.

This module validates the CSS selectors defined in the scraper's constants,
ensuring that all selectors are correctly formatted, non-empty, and unique.
Proper validation of these selectors is essential for reliably extracting
data points from the European Citizens' Initiative (ECI) pages.
"""

# Third-party
import pytest

# Local
from data_pipeline.scraper.initiatives.css_selectors import (
    ECIinitiativeSelectors,
    ECIlistingSelectors,
)

_INITIATIVE_ATTRS = [
    "INITIATIVE_PROGRESS",
    "OBJECTIVES",
    "ANNEX",
    "ORGANISERS",
    "REPRESENTATIVE",
    "SOURCES_OF_FUNDING",
    "SOCIAL_SHARE",
]

_LISTING_ATTRS = [
    "INITIATIVE_CARDS",
    "PAGINATION_LINKS",
    "NEXT_BUTTON",
]


class TestECIinitiativeSelectors:
    """
    Test suite for individual ECI initiative page CSS selectors.

    Validates that each selector used for extracting initiative details
    (e.g., progress, objectives, organisers) is a valid, non-empty string
    without leading/trailing whitespace, and that no duplicate selectors
    exist across attributes.
    """

    @pytest.mark.parametrize("attr", _INITIATIVE_ATTRS)
    def test_attribute_is_nonempty_string(self, attr):

        value = getattr(ECIinitiativeSelectors, attr)
        assert isinstance(value, str), f"{attr} must be str"
        assert len(value) > 0, f"{attr} must not be empty"

    @pytest.mark.parametrize("attr", _INITIATIVE_ATTRS)
    def test_attribute_has_no_leading_or_trailing_whitespace(self, attr):

        value = getattr(ECIinitiativeSelectors, attr)
        assert value == value.strip()

    def test_all_selectors_are_unique(self):

        values = [getattr(ECIinitiativeSelectors, a) for a in _INITIATIVE_ATTRS]
        assert len(values) == len(set(values)), "All selectors must be unique"


class TestECIlistingSelectors:
    """
    Test suite for ECI listing page CSS selectors.

    Validates that each selector used for navigating and extracting data
    from the initiatives listing pages (e.g., initiative cards, pagination links,
    next buttons) is a valid, non-empty string without leading or trailing
    whitespace, and that all selectors are unique.
    """

    @pytest.mark.parametrize("attr", _LISTING_ATTRS)
    def test_attribute_is_nonempty_string(self, attr):

        value = getattr(ECIlistingSelectors, attr)
        assert isinstance(value, str), f"{attr} must be str"
        assert len(value) > 0, f"{attr} must not be empty"

    @pytest.mark.parametrize("attr", _LISTING_ATTRS)
    def test_attribute_has_no_leading_or_trailing_whitespace(self, attr):

        value = getattr(ECIlistingSelectors, attr)
        assert value == value.strip()

    def test_all_selectors_are_unique(self):

        values = [getattr(ECIlistingSelectors, a) for a in _LISTING_ATTRS]
        assert len(values) == len(set(values)), "All selectors must be unique"
