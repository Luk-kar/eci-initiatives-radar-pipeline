"""Tests for responses_followup.extractor.parser.fields.commission_answer."""

import pytest

from bs4 import BeautifulSoup, Tag

# FIX: import from responses_followup (not responses)
from data_pipeline.extractor.responses_followup.extractor.parser.fields.commission_answer import (
    extract_commission_answer,
)

from .conftest import ECI_FIXTURES


def _soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")


def _tag(html: str) -> Tag:
    return _soup(html).find()


# Reusable banner HTML that appears in real fixtures (2022_000002 style).
_BANNER = """
<figure class="ecl-banner__picture-container">
  <picture class="ecl-picture ecl-banner__picture">
    <img alt="Footer banner" src="/hero-banner-bg.png">
  </picture>
</figure>
"""


class TestExtractCommissionAnswer:

    @pytest.mark.parametrize("reg_num,soup", ECI_FIXTURES)
    def test_returns_non_empty_list(self, reg_num, soup):

        result = extract_commission_answer(soup, reg_num)

        assert isinstance(result, list)
        assert len(result) > 0
        assert all(isinstance(item, str) for item in result)
        for section in result:
            assert len(section) > 15

    def test_missing_header_raises(self):

        with pytest.raises(ValueError, match="Could not find"):
            extract_commission_answer(_soup("<p>No answer section.</p>"), "2012/000099")

    def test_empty_answer_section_raises(self):
        """Answer section exists but has no content before the next h2."""

        soup = _soup(
            """
            <h2>Response of the Commission</h2>
            <h2>Follow-up</h2>
            <p>In the Communication adopted on 28/05/2014, the Commission explains that it
            has decided not to submit a legislative proposal.</p>
            """
            + _BANNER
        )
        with pytest.raises(ValueError, match="No content found"):
            extract_commission_answer(soup, "2012/000099")

    def test_only_skippable_elements_in_section_raises(self):
        """Banner wrapped in data-inpage-navigation-source-area is skipped; raises if that's all."""

        soup = _soup(
            """
            <h2>Response of the Commission</h2>
            <div data-inpage-navigation-source-area="h2">
              <figure class="ecl-banner__picture-container">
                <picture class="ecl-picture ecl-banner__picture">
                  <img alt="Footer banner" src="/hero-banner-bg.png">
                </picture>
              </figure>
            </div>
            <h2>Follow-up</h2>
            """
        )
        with pytest.raises(ValueError, match="No content found"):
            extract_commission_answer(soup, "2012/000099")

    def test_does_not_include_followup_section_text(self):

        soup = _soup(
            """
            <h2>Response of the Commission</h2>
            <p>This is the actual answer body with enough text to pass the length check.</p>
            <h2>Follow-up</h2>
            <p>SENTINEL_FOLLOWUP_TEXT</p>
            """
            + _BANNER
        )

        result = extract_commission_answer(soup, "2012/000099")

        assert any("SENTINEL_FOLLOWUP_TEXT" not in item for item in result)

    def test_answer_ends_at_first_subsequent_h2(self):

        soup = _soup(
            """
            <h2>Response of the Commission</h2>
            <p>SENTINEL_ANSWER_TEXT is the content that should be extracted here.</p>
            <h2>Follow-up</h2>
            <p>SENTINEL_FOLLOWUP_TEXT</p>
            """
            + _BANNER
        )
        result = extract_commission_answer(soup, "2012/000099")
        assert any("SENTINEL_ANSWER_TEXT" in item for item in result)
        assert not any("SENTINEL_FOLLOWUP_TEXT" in item for item in result)
