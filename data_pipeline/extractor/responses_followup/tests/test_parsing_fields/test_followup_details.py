"""Tests for responses_followup.extractor.parser.fields.followup_details.

NOTE: extract_followup_events is currently a placeholder stub (returns [""]
for every input).  These tests verify the placeholder contract so that when
the real implementation lands, any behavioural change is caught immediately.
The old tests for extract_followup_additional_website have been removed — that
function no longer exists in this module.
"""

import pytest

from bs4 import BeautifulSoup

# FIX: import from responses_followup (not responses)
# FIX: import extract_followup_events — extract_followup_additional_website
#      was removed from the module
from data_pipeline.extractor.responses_followup.extractor.parser.fields.followup_details import (
    extract_followup_events,
)


def _soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")


class TestExtractFollowupEventsPlaceholder:
    """
    Smoke tests for the placeholder implementation.

    extract_followup_events currently ignores its arguments and returns [""].
    The first positional argument binds to 'self' (a leftover from the class
    method era); the second argument binds to 'soup'.  Both are accepted
    without error.
    """

    def test_returns_a_list(self):
        """Placeholder always returns a list."""
        result = extract_followup_events(None, _soup("<p>Any content.</p>"))
        assert isinstance(result, list)

    def test_returns_list_for_empty_soup(self):
        result = extract_followup_events(None, _soup(""))
        assert isinstance(result, list)

    def test_returns_list_for_rich_html(self):
        html = """
            <div class="ecl">
              <h2>Follow-up</h2>
              <p>On 9 February 2024, Commissioner met with organisers.</p>
            </div>
        """
        result = extract_followup_events(None, _soup(html))
        assert isinstance(result, list)

    def test_does_not_raise(self):
        """Placeholder must never raise regardless of input."""
        extract_followup_events(None, _soup("<p>Anything.</p>"))
