"""
Tests for the HTML parser that extracts Commission response links
from saved initiative pages.

Validates link extraction, title parsing, edge cases (missing links,
malformed HTML, unreadable files), and directory-level aggregation.
"""

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from data_pipeline.scraper.responses.html_parser import ResponseLinkExtractor

# ── Shared HTML fixtures ───────────────────────────────────────────────────────

_RESPONSE_URL = "https://commission.europa.eu/strategy-and-policy/123"

HTML_WITH_LINK = f"""
<html><body>
  <h1 class="ecl-page-header-core__title">Save the Bees</h1>
  <a href="{_RESPONSE_URL}">Commission's answer and follow-up</a>
</body></html>
"""

HTML_WITH_UNICODE_APOSTROPHE = f"""
<html><body>
  <h1 class="ecl-page-header-core__title">Clean Air</h1>
  <a href="{_RESPONSE_URL}">Commission\u2019s answer and follow-up</a>
</body></html>
"""

HTML_WITHOUT_LINK = """
<html><body>
  <h1 class="ecl-page-header-core__title">No Response Yet</h1>
  <p>Some content without a Commission response link.</p>
</body></html>
"""

HTML_NO_TITLE = f"""
<html><body>
  <a href="{_RESPONSE_URL}">Commission's answer and follow-up</a>
</body></html>
"""


@pytest.fixture
def extractor():
    return ResponseLinkExtractor()


@pytest.fixture
def initiative_file(tmp_path):
    """Write a single initiative HTML file in year/reg_number_en.html layout."""

    def _write(year: str, reg_number: str, html: str) -> Path:
        year_dir = tmp_path / year
        year_dir.mkdir(parents=True, exist_ok=True)
        path = year_dir / f"{year}_{reg_number}.html"
        path.write_text(html, encoding="utf-8")
        return path

    return _write


# ── TestExtractLinksFromFile ───────────────────────────────────────────────────


class TestExtractLinksFromFile:
    """
    Validates single-file extraction: URL, year, reg_number, title fields.
    """

    def test_returns_dict_with_expected_keys(self, extractor, initiative_file):

        path = initiative_file("2023", "000007", HTML_WITH_LINK)
        result = extractor.extract_links_from_file(str(path))

        assert result is not None
        assert set(result.keys()) == {"url", "year", "reg_number", "title", "datetime"}

    def test_extracts_correct_url(self, extractor, initiative_file):

        path = initiative_file("2023", "000007", HTML_WITH_LINK)
        result = extractor.extract_links_from_file(str(path))

        assert result["url"] == _RESPONSE_URL

    def test_extracts_year_from_directory_name(self, extractor, initiative_file):

        path = initiative_file("2019", "000001", HTML_WITH_LINK)
        result = extractor.extract_links_from_file(str(path))

        assert result["year"] == "2019"

    def test_extracts_reg_number_from_filename(self, extractor, initiative_file):

        path = initiative_file("2023", "000007", HTML_WITH_LINK)
        result = extractor.extract_links_from_file(str(path))

        assert result["reg_number"] == "000007"

    def test_extracts_title_from_h1(self, extractor, initiative_file):

        path = initiative_file("2023", "000007", HTML_WITH_LINK)
        result = extractor.extract_links_from_file(str(path))

        assert result["title"] == "Save the Bees"

    def test_handles_unicode_apostrophe_in_link_text(self, extractor, initiative_file):

        path = initiative_file("2021", "000003", HTML_WITH_UNICODE_APOSTROPHE)
        result = extractor.extract_links_from_file(str(path))

        assert result is not None
        assert result["url"] == _RESPONSE_URL

    def test_returns_none_when_no_commission_link(self, extractor, initiative_file):

        path = initiative_file("2023", "000007", HTML_WITHOUT_LINK)
        result = extractor.extract_links_from_file(str(path))

        assert result is None

    def test_returns_empty_title_when_no_h1(self, extractor, initiative_file):

        path = initiative_file("2023", "000007", HTML_NO_TITLE)
        result = extractor.extract_links_from_file(str(path))

        assert result["title"] == ""

    def test_returns_none_on_unreadable_file(self, extractor, tmp_path):

        result = extractor.extract_links_from_file(str(tmp_path / "missing.html"))

        assert result is None

    def test_datetime_is_empty_string(self, extractor, initiative_file):

        path = initiative_file("2023", "000007", HTML_WITH_LINK)
        result = extractor.extract_links_from_file(str(path))

        assert result["datetime"] == ""


# ── TestExtractLinksFromDirectory ──────────────────────────────────────────────


class TestExtractLinksFromDirectory:
    """
    Validates directory-level aggregation across year-partitioned HTML files.
    """

    def test_returns_all_found_links(self, extractor, initiative_file):

        initiative_file("2023", "000007", HTML_WITH_LINK)
        initiative_file("2019", "000001", HTML_WITH_LINK)
        base_dir = str(initiative_file("2023", "000007", HTML_WITH_LINK).parent.parent)

        results = extractor.extract_links_from_directory(base_dir)

        assert len(results) >= 2

    def test_skips_files_without_commission_link(self, extractor, initiative_file):

        initiative_file("2023", "000007", HTML_WITH_LINK)
        initiative_file("2022", "000002", HTML_WITHOUT_LINK)
        base_dir = str(initiative_file("2023", "000007", HTML_WITH_LINK).parent.parent)

        results = extractor.extract_links_from_directory(base_dir)

        urls = [r["url"] for r in results]
        assert all(u == _RESPONSE_URL for u in urls)

    def test_returns_empty_list_for_empty_directory(self, extractor, tmp_path):

        results = extractor.extract_links_from_directory(str(tmp_path))

        assert results == []

    def test_ignores_non_directory_entries(self, extractor, tmp_path):

        (tmp_path / "stray_file.txt").write_text("ignored")
        results = extractor.extract_links_from_directory(str(tmp_path))

        assert results == []
