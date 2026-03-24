# datapipeline/extractor/initiatives/tests/fields/test_annex.py

from bs4 import BeautifulSoup

from data_pipeline.extractor.initiatives.parser.fields.annex import extract_annex


def _soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")


def test_extract_annex_returns_none_when_no_annex_section():
    html = """
    <html><body>
      <h2>Objectives</h2>
      <p>Some text</p>
    </body></html>
    """
    assert extract_annex(_soup(html)) is None


def test_extract_annex_collects_paragraphs_until_next_h2():
    html = """
    <html><body>
      <h2>Annex</h2>
      <p>First paragraph.</p>
      <p>Second paragraph.</p>
      <h2>Other section</h2>
      <p>Ignored.</p>
    </body></html>
    """
    result = extract_annex(_soup(html))
    assert result == "First paragraph. Second paragraph."


def test_extract_annex_handles_lists_and_strips_whitespace():
    html = """
    <html><body>
      <h2>ANNEX</h2>
      <ul>
        <li>Item one</li>
        <li>Item two</li>
      </ul>
      <p>Final paragraph.</p>
    </body></html>
    """
    result = extract_annex(_soup(html))
    # Order-preserving concatenation
    assert result == "Item one Item two Final paragraph."
