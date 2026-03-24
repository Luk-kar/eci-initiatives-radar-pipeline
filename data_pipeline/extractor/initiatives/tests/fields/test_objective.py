from bs4 import BeautifulSoup
import pytest

from data_pipeline.extractor.initiatives.parser.fields.objective import (
    extract_objective,
)
from data_pipeline.extractor.extractor_shared.errors import FieldValueError


def _soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")


def test_objective_extracts_single_paragraph_after_heading():

    html = """
    <html><body>
      <h2>Objectives</h2>
      <p>The main objective is to protect biodiversity.</p>
      <h2>Next section</h2>
    </body></html>
    """

    result = extract_objective(_soup(html))
    assert result == "The main objective is to protect biodiversity."


def test_objective_concatenates_multiple_paragraphs_until_next_h2():

    html = """
    <html><body>
      <h2>Objective</h2>
      <p>First part of the objective.</p>
      <p>Second part continues the explanation.</p>
      <div>Non-paragraph element should be ignored.</div>
      <h2>Other section</h2>
    </body></html>
    """

    result = extract_objective(_soup(html))
    # Function appends a space after each paragraph, then strips at the end.
    assert result == (
        "First part of the objective. Second part continues the explanation."
    )


def test_objective_raises_when_heading_missing():

    html = """
    <html><body>
      <h2>Background</h2>
      <p>Some text, but no 'Objectives' heading.</p>
    </body></html>
    """

    with pytest.raises(FieldValueError) as excinfo:
        extract_objective(_soup(html))
    msg = str(excinfo.value)

    assert "no 'Objectives' heading found in page" in msg


def test_objective_raises_when_no_paragraphs_before_next_h2():

    html = """
    <html><body>
      <h2>Objectives</h2>
      <div>Content but not in a paragraph.</div>
      <h2>Another section</h2>
    </body></html>
    """

    with pytest.raises(FieldValueError) as excinfo:
        extract_objective(_soup(html))

    msg = str(excinfo.value)
    assert "contains no paragraph text before the next section" in msg
