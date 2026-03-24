from bs4 import BeautifulSoup
import pytest

from data_pipeline.extractor.initiatives.parser.fields.title import extract_title
from data_pipeline.extractor.extractor_shared.errors import FieldValueError


def _soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")


def test_title_uses_meta_dcterms_title_when_available():
    html = """
    <html><head>
      <meta name="dcterms.title" content="Meta Title Initiative" />
    </head>
    <body>
      <h1 class="ecl-page-header-core__title">H1 Title</h1>
    </body></html>
    """
    result = extract_title(_soup(html))
    assert result == "Meta Title Initiative"


def test_title_falls_back_to_h1_when_meta_missing_or_empty():
    html = """
    <html><head>
      <meta name="dcterms.title" content="" />
    </head>
    <body>
      <h1 class="ecl-page-header-core__title">
        H1 Title From Header
      </h1>
    </body></html>
    """
    result = extract_title(_soup(html))
    assert result == "H1 Title From Header"


def test_title_raises_when_neither_meta_nor_h1_present():
    html = "<html><body><p>No title here</p></body></html>"
    with pytest.raises(FieldValueError):
        extract_title(_soup(html))
