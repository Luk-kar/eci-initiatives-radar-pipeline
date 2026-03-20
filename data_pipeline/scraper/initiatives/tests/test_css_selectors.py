import pytest
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
