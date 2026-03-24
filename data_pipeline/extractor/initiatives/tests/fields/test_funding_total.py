from bs4 import BeautifulSoup

from data_pipeline.extractor.initiatives.parser.fields.funding.total import (
    extract_funding_total,
)


def _soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")


def test_funding_total_returns_none_when_no_matching_text():

    html = """
    <html><body>
      <p>Completely unrelated paragraph.</p>
      <p class="ecl-u-type-paragraph">No funding here either.</p>
    </body></html>
    """

    assert extract_funding_total(_soup(html)) is None


def test_funding_total_matches_direct_paragraph_with_label():

    html = """
    <html><body>
      <p>Total amount of support and funding: €12,345.00</p>
    </body></html>
    """

    result = extract_funding_total(_soup(html))
    assert result == "12,345.00"


def test_funding_total_uses_fallback_ecl_paragraphs():

    html = """
    <html><body>
      <p class="ecl-u-type-paragraph ecl-u-type-bold">
        Total amount of support and funding  €17,360.00
      </p>
    </body></html>
    """

    result = extract_funding_total(_soup(html))
    assert result == "17,360.00"
