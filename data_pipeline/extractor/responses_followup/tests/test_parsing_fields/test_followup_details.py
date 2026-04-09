"""Tests for responses_followup.extractor.parser.fields.followup_details.

NOTE: extract_followup_events is currently a placeholder stub (returns [""]
for every input).  These tests verify the placeholder contract so that when
the real implementation lands, any behavioural change is caught immediately.
The old tests for extract_followup_additional_website have been removed — that
function no longer exists in this module.
"""

import pytest

from bs4 import BeautifulSoup

from data_pipeline.extractor.responses_followup.extractor.parser.fields.followup_details import (
    extract_followup_events,
)


def _soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")


class TestExtractFollowupEvents:

    def test_raises_on_none_soup(self):
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
        soup = _soup(html)
        with pytest.raises(ValueError, match="2016_000001"):
            extract_followup_events(soup, "2016_000001")
