"""Tests for responses_followup.extractor.parser.fields.followup_details."""

import pytest
from bs4 import BeautifulSoup

from data_pipeline.extractor.responses_followup.extractor.parser.fields.followup_details import (
    extract_followup_events,
)
from .conftest import ECI_FIXTURES


def _soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")


# ── Guard / type-error tests ──────────────────────────────────────────────────


class TestExtractFollowupEventsInputValidation:
    """
    Verifies that extract_followup_events rejects invalid or incomplete
    inputs before any HTML traversal takes place.  Covers: None soup
    (TypeError), empty document, document with no response-of-the-commission
    section, and document whose only h2 is a follow-up heading with no
    matching response header.
    """

    def test_raises_type_error_on_none_soup(self):

        with pytest.raises(TypeError, match="BeautifulSoup"):
            extract_followup_events(None, "2016_000001")

    def test_raises_when_no_response_section(self):

        soup = _soup("<p>Any content.</p>")
        with pytest.raises(ValueError, match="2016_000001"):
            extract_followup_events(soup, "2016_000001")

    def test_raises_for_empty_soup(self):

        soup = _soup("")
        with pytest.raises(ValueError, match="2016_000001"):
            extract_followup_events(soup, "2016_000001")

    def test_raises_when_followup_heading_only_no_response(self):

        html = """
            <div class="ecl">
              <h2>Follow-up</h2>
              <p>On 9 February 2024, Commissioner met with organisers.</p>
            </div>
        """
        with pytest.raises(ValueError, match="2016_000001"):
            extract_followup_events(_soup(html), "2016_000001")


# ── Modern ECL layout (2018_000004) ───────────────────────────────────────────


class TestExtractFollowupEventsModernLayout:
    """
    Exercises the ECL wrapper layout where every section lives inside its own
    div.ecl-u-mb-2xl.  h2 elements carry class='ecl-u-type-heading-2', so
    _find_followup_start_h2 resolves to the 'Next steps' h2 and collection
    continues through 'Supporting measures' before halting at 'press-release'.

    The follow-up h3/ul block is nested inside the response wrapper and
    therefore precedes start_h2 in document order — it is never collected.
    """

    REG = "2018_000004"

    def test_returns_list(self, eci_fixture_soup):

        result = extract_followup_events(eci_fixture_soup(self.REG), self.REG)

        assert isinstance(result, list)

    def test_returns_non_empty_list(self, eci_fixture_soup):

        result = extract_followup_events(eci_fixture_soup(self.REG), self.REG)

        assert len(result) > 0

    def test_exact_item_count(self, eci_fixture_soup):

        # Next steps <p> + Supporting measures <p> = 2 items
        result = extract_followup_events(eci_fixture_soup(self.REG), self.REG)

        assert len(result) == 2

    def test_contains_next_steps_text(self, eci_fixture_soup):

        result = extract_followup_events(eci_fixture_soup(self.REG), self.REG)

        assert any("phase out cages" in item for item in result)

    def test_contains_supporting_measures_text(self, eci_fixture_soup):

        result = extract_followup_events(eci_fixture_soup(self.REG), self.REG)

        assert any("Best Practice Hens" in item for item in result)

    def test_all_items_are_non_empty_strings(self, eci_fixture_soup):

        result = extract_followup_events(eci_fixture_soup(self.REG), self.REG)

        assert all(isinstance(item, str) and item.strip() for item in result)

    def test_no_excess_whitespace(self, eci_fixture_soup):

        result = extract_followup_events(eci_fixture_soup(self.REG), self.REG)

        assert all("  " not in item for item in result)

    def test_each_item_has_minimum_meaningful_length(self, eci_fixture_soup):

        result = extract_followup_events(eci_fixture_soup(self.REG), self.REG)

        assert all(len(item) > 20 for item in result)

    def test_items_are_distinct(self, eci_fixture_soup):

        result = extract_followup_events(eci_fixture_soup(self.REG), self.REG)

        assert len(result) == len(set(result))

    # Stop-section boundary checks

    def test_stops_before_press_release(self, eci_fixture_soup):

        result = extract_followup_events(eci_fixture_soup(self.REG), self.REG)

        assert not any("ip_21_3297" in item for item in result)

    def test_stops_before_video(self, eci_fixture_soup):

        result = extract_followup_events(eci_fixture_soup(self.REG), self.REG)

        assert not any("vimeo" in item for item in result)

    def test_stops_before_related_links(self, eci_fixture_soup):

        result = extract_followup_events(eci_fixture_soup(self.REG), self.REG)

        assert not any("animal-welfare_en" in item for item in result)

    # Content that must be absent (follow-up h3/ul block predates start_h2)

    def test_does_not_collect_pre_start_followup_block(self, eci_fixture_soup):

        result = extract_followup_events(eci_fixture_soup(self.REG), self.REG)

        assert not any("stakeholder consultations" in item for item in result)

    def test_does_not_collect_content_nested_inside_response_wrapper(
        self, eci_fixture_soup
    ):
        """Items inside the response div that precede start_h2 are never visited
        by _collect_content_elements, which only walks forward from start_h2."""

        result = extract_followup_events(eci_fixture_soup(self.REG), self.REG)

        assert not any("EFSA adopted" in item for item in result)


# ── Flat legacy layout fallback ───────────────────────────────────────────────


class TestExtractFollowupEventsFlatLayout:
    """
    Exercises the bare-h2 legacy layout where section headings carry no
    class attribute.  _find_followup_start_h2 falls back to pass 2 (any h2)
    and collection continues until a stop-section id is reached, also via the
    bare-h2 stop condition in _collect_content_elements.
    """

    REG = "2012_000001"  # Fake one as a proof of concept

    def test_returns_list(self, eci_fixture_soup):

        result = extract_followup_events(eci_fixture_soup(self.REG), self.REG)
        assert isinstance(result, list)

    def test_returns_non_empty_list(self, eci_fixture_soup):

        result = extract_followup_events(eci_fixture_soup(self.REG), self.REG)
        assert len(result) > 0

    def test_all_items_are_non_empty_strings(self, eci_fixture_soup):

        result = extract_followup_events(eci_fixture_soup(self.REG), self.REG)
        assert all(isinstance(item, str) and item.strip() for item in result)

    def test_no_duplicate_items(self, eci_fixture_soup):

        result = extract_followup_events(eci_fixture_soup(self.REG), self.REG)
        assert len(result) == len(set(result))

    def test_stops_before_related_links(self, eci_fixture_soup):

        result = extract_followup_events(eci_fixture_soup(self.REG), self.REG)
        assert not any("EU water policy" in item for item in result)


# ── Parametrised contract over every fixture ──────────────────────────────────


class TestExtractFollowupEventsAllFixtures:
    """
    Parametrised smoke tests that run against every entry in ECI_FIXTURES.

    Every fixture is expected to produce a valid result — layout variants
    differ in structure but all contain a recognisable response section and
    at least one follow-up section before any stop-section id.
    """

    @pytest.mark.parametrize("registration_number, soup", ECI_FIXTURES)
    def test_returns_list(self, registration_number, soup):

        result = extract_followup_events(soup, registration_number)
        assert isinstance(result, list)

    @pytest.mark.parametrize("registration_number, soup", ECI_FIXTURES)
    def test_list_is_non_empty(self, registration_number, soup):

        result = extract_followup_events(soup, registration_number)
        assert len(result) > 0

    @pytest.mark.parametrize("registration_number, soup", ECI_FIXTURES)
    def test_all_items_are_non_empty_strings(self, registration_number, soup):

        result = extract_followup_events(soup, registration_number)
        assert all(isinstance(item, str) and item.strip() for item in result)

    @pytest.mark.parametrize("registration_number, soup", ECI_FIXTURES)
    def test_no_duplicate_items(self, registration_number, soup):

        result = extract_followup_events(soup, registration_number)
        assert len(result) == len(set(result))

    @pytest.mark.parametrize("registration_number, soup", ECI_FIXTURES)
    def test_no_excess_whitespace(self, registration_number, soup):

        result = extract_followup_events(soup, registration_number)
        assert all("  " not in item for item in result)
