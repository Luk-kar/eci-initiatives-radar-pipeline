import pytest
from bs4 import BeautifulSoup

from data_pipeline.extractor.initiatives.parser.fields.current_status import (
    extract_current_status,
)
from data_pipeline.extractor.extractor_shared.errors import FieldValueError


# ── helpers ───────────────────────────────────────────────────────────────────

def _make_soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")


# ── normal path ───────────────────────────────────────────────────────────────

def test_returns_current_marked_item():

    html = """
    <ol class="ecl-timeline">
      <li class="ecl-timeline__item">
        <div class="ecl-timeline__title">Registered</div>
      </li>
      <li class="ecl-timeline__item ecl-timeline__item--current">
        <div class="ecl-timeline__title">Collection ongoing</div>
      </li>
      <li class="ecl-timeline__item">
        <div class="ecl-timeline__title">  </div>
        <div class="ecl-timeline__content">15/07/2026</div>
      </li>
    </ol>
    """
    assert extract_current_status(_make_soup(html)) == "Collection ongoing"


def test_raises_when_current_item_has_no_title_element():

    html = """
    <ol class="ecl-timeline">
      <li class="ecl-timeline__item ecl-timeline__item--current">
        <!-- no ecl-timeline__title div at all -->
      </li>
    </ol>
    """
    
    with pytest.raises(FieldValueError, match="no title element"):
        extract_current_status(_make_soup(html))


# ── fallback: no --current marker ─────────────────────────────────────────────

def test_fallback_returns_last_nonempty_title(caplog):
    """Mirrors the real 2025/000005 corrupted page structure."""

    html = """
    <ol class="ecl-timeline">
      <li class="ecl-timeline__item">
        <div class="ecl-timeline__title">Registered</div>
        <div class="ecl-timeline__content">25/11/2025</div>
      </li>
      <li class="ecl-timeline__item">
        <div class="ecl-timeline__title">Collection start date</div>
        <div class="ecl-timeline__content">13/01/2026</div>
      </li>
      <li class="ecl-timeline__item">
        <div class="ecl-timeline__title"></div>
        <div class="ecl-timeline__content">15/07/2026</div>
      </li>
    </ol>
    """

    with caplog.at_level("WARNING"):
        result = extract_current_status(_make_soup(html))

    assert result == "Collection start date"
    assert "Falling back to last non-empty title in timeline." in caplog.text


def test_raises_when_all_titles_empty():
    html = """
    <ol class="ecl-timeline">
      <li class="ecl-timeline__item">
        <div class="ecl-timeline__title">  </div>
        <div class="ecl-timeline__content">01/01/2025</div>
      </li>
      <li class="ecl-timeline__item">
        <div class="ecl-timeline__title"></div>
        <div class="ecl-timeline__content">15/07/2026</div>
      </li>
    </ol>
    """

    with pytest.raises(FieldValueError, match="no non-empty title found"):
        extract_current_status(_make_soup(html))


def test_raises_when_no_timeline_items_at_all():

    html = "<div>No timeline here</div>"
    with pytest.raises(FieldValueError, match="no active timeline item"):
        extract_current_status(_make_soup(html))