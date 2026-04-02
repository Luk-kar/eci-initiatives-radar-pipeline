import pytest

from bs4 import BeautifulSoup, NavigableString, Tag

from data_pipeline.extractor.responses.extractor.parser.fields.commission_answer import (
    extract_commission_answer,
)

from .conftest import ECI_FIXTURES


def _soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")


def _tag(html: str) -> Tag:
    return _soup(html).find()


# ---------------------------------------------------------------------------
# extract_commission_answer — integration
# ---------------------------------------------------------------------------


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

        soup = _soup(
            """
            <h2>Answer of the European Commission</h2>
            <h2>Follow-up</h2>
            <p>Some follow-up text that is long enough to be meaningful.</p>
        """
        )
        with pytest.raises(ValueError, match="No content found"):
            extract_commission_answer(soup, "2012/000099")

    def test_only_skippable_elements_in_section_raises(self):

        soup = _soup(
            """
            <h2>Answer of the European Commission</h2>
            <div data-inpage-navigation-source-area="h2"><p>chrome</p></div>
            <h2>Follow-up</h2>
        """
        )
        with pytest.raises(ValueError, match="No content found"):
            extract_commission_answer(soup, "2012/000099")

    def test_does_not_include_followup_section_text(self):
        soup = _soup(
            """
            <h2>Answer of the European Commission</h2>
            <p>This is the actual answer body with enough text to pass the length check.</p>
            <h2>Follow-up</h2>
            <p>SENTINEL_FOLLOWUP_TEXT</p>
        """
        )

        result = extract_commission_answer(soup, "2012/000099")

        assert any("SENTINEL_FOLLOWUP_TEXT" not in item for item in result)

    def test_answer_ends_at_first_subsequent_h2(self):
        soup = _soup(
            """
            <h2>Answer of the European Commission</h2>
            <p>SENTINEL_ANSWER_TEXT is the content that should be extracted here.</p>
            <h2>Follow-up</h2>
            <p>SENTINEL_FOLLOWUP_TEXT</p>
        """
        )
        result = extract_commission_answer(soup, "2012/000099")
        assert any("SENTINEL_ANSWER_TEXT" in item for item in result)
        assert not any("SENTINEL_FOLLOWUP_TEXT" in item for item in result)
