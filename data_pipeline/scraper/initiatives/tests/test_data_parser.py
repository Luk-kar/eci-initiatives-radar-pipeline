"""
Tests for the HTML data parser of the ECI initiatives scraper.

This module verifies the extraction of initiative information from listing pages.
It ensures that the parser correctly reads HTML content, identifies initiative
cards, and formats the extracted data into the expected structures.
"""

# Local
from data_pipeline.scraper.initiatives.html_parser import parse_initiatives_list_data

BASE_URL = "https://citizens-initiative.europa.eu"

_HREFS = [
    "/initiatives/details/2023/000001",
    "/initiatives/details/2022/000002",
    "/initiatives/details/2021/000003",
]


def _make_listing_html(hrefs: list[str]) -> str:
    """
    Matches:
      CONTENT_BLOCKS  = "div.ecl-content-block.ecl-content-item__content-block"
      INITIATIVE_CARDS = "div.ecl-content-block__title a.ecl-link"
    """
    cards = "\n".join(
        f'<div class="ecl-content-block ecl-content-item__content-block">'
        f'  <div class="ecl-content-block__title">'
        f'    <a class="ecl-link" href="{href}">Initiative {i}</a>'
        f"  </div>"
        f"</div>"
        for i, href in enumerate(hrefs, 1)
    )
    return f"<html><body>{cards}</body></html>"


class TestParseInitiativesListData:
    """
    Test suite for the `parse_initiatives_list_data` function.

    Validates that the parser correctly extracts initiative records from
    listing page HTML. It ensures proper handling of empty or invalid HTML,
    verifies that the correct number of items are extracted as dictionaries,
    and confirms that relative href attributes are accurately converted to
    absolute URLs using the provided base URL.
    """

    def test_returns_empty_list_for_empty_string(self):
        assert parse_initiatives_list_data("", BASE_URL) == []

    def test_returns_empty_for_bare_html(self):
        assert parse_initiatives_list_data("<html><body></body></html>", BASE_URL) == []

    def test_returns_empty_for_html_without_initiative_cards(self):
        html = "<html><body><p>No initiatives here.</p></body></html>"
        assert parse_initiatives_list_data(html, BASE_URL) == []

    def test_result_count_matches_card_count(self):
        result = parse_initiatives_list_data(_make_listing_html(_HREFS), BASE_URL)
        assert len(result) == len(_HREFS)

    def test_each_item_is_dict(self):
        result = parse_initiatives_list_data(_make_listing_html(_HREFS), BASE_URL)
        assert len(result) > 0
        for item in result:
            assert isinstance(item, dict)

    def test_each_item_has_url_key(self):
        result = parse_initiatives_list_data(_make_listing_html(_HREFS), BASE_URL)
        assert len(result) > 0
        for item in result:
            assert "url" in item, f"item missing 'url' key: {item}"

    def test_urls_are_absolute_strings(self):
        result = parse_initiatives_list_data(_make_listing_html(_HREFS[:1]), BASE_URL)
        assert len(result) > 0
        for item in result:
            assert isinstance(item["url"], str)
            assert item["url"].startswith("http")

    def test_relative_hrefs_resolved_with_base_url(self):
        result = parse_initiatives_list_data(_make_listing_html(_HREFS[:1]), BASE_URL)
        assert len(result) > 0
        assert result[0]["url"] == BASE_URL + _HREFS[0]

    def test_different_base_urls_produce_different_absolute_urls(self):
        html = _make_listing_html(_HREFS[:1])
        result_a = parse_initiatives_list_data(html, "https://host-a.example.com")
        result_b = parse_initiatives_list_data(html, "https://host-b.example.com")
        assert len(result_a) > 0 and len(result_b) > 0
        assert result_a[0]["url"] != result_b[0]["url"]


def make_listing_html_with_meta(hrefs: list[str], reg_numbers: list[str]) -> str:
    cards = "".join(
        f"""<div class="ecl-content-block ecl-content-item__content-block">
          <div class="ecl-content-block__title">
            <a class="ecl-link" href="{href}">Initiative {i}</a>
          </div>
          <span class="ecl-content-block__secondary-meta-label">
            Registration number: {reg}
          </span>
        </div>"""
        for i, (href, reg) in enumerate(zip(hrefs, reg_numbers), 1)
    )
    return f"<html><body>{cards}</body></html>"


class TestRegistrationNumberFormat:
    def test_eci_format_converted_to_slash_format(self):

        html = make_listing_html_with_meta([_HREFS[0]], ["ECI(2024)000006"])
        result = parse_initiatives_list_data(html, BASE_URL)

        assert result[0]["registration_number"] == "2024/000006"

    def test_unrecognized_format_left_unchanged(self):

        html = make_listing_html_with_meta([_HREFS[0]], ["UNKNOWN-FORMAT"])
        result = parse_initiatives_list_data(html, BASE_URL)

        assert result[0]["registration_number"] == "UNKNOWN-FORMAT"
