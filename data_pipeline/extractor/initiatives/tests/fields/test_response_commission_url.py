from bs4 import BeautifulSoup

from data_pipeline.extractor.initiatives.parser.fields.response_commission_url import (
    extract_response_commission_url,
)


def _soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")


def test_response_commission_url_returns_href_when_link_present():

    html = """
    <html><body>
      <a href="https://example.test/commission-answer"
         >Commission's answer and follow-up</a>
    </body></html>
    """

    result = extract_response_commission_url(_soup(html))
    assert result == "https://example.test/commission-answer"


def test_response_commission_url_handles_unicode_apostrophe():

    html = """
    <html><body>
      <a href="https://example.test/commission-answer-2">
        Commission’s answer and follow-up
      </a>
    </body></html>
    """

    result = extract_response_commission_url(_soup(html))
    assert result == "https://example.test/commission-answer-2"


def test_response_commission_url_returns_none_when_no_matching_link():

    html = """
    <html><body>
      <a href="https://example.test/other">Some other link</a>
    </body></html>
    """

    assert extract_response_commission_url(_soup(html)) is None
