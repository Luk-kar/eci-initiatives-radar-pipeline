import pytest
from bs4 import BeautifulSoup

from data_pipeline.extractor.extractor_shared.errors import FieldValueError
from data_pipeline.extractor.initiatives.parser.fields.current_status import (
    extract_current_status,
)


def _soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")


def test_extract_current_status_happy_path():

    html = """
    <html><body>
      <ol class="ecl-timeline">
        <li class="ecl-timeline__item ecl-timeline__item--current">
          <div class="ecl-timeline__title">Answered</div>
        </li>
      </ol>
    </body></html>
    """

    assert extract_current_status(_soup(html)) == "Answered"


def test_extract_current_status_raises_when_no_current_item():

    html = """
    <html><body>
      <ol class="ecl-timeline">
        <li class="ecl-timeline__item">
          <div class="ecl-timeline__title">Registered</div>
        </li>
      </ol>
    </body></html>
    """

    with pytest.raises(FieldValueError) as excinfo:
        extract_current_status(_soup(html))

    msg = str(excinfo.value)
    assert "no active timeline item" in msg


def test_extract_current_status_raises_when_title_missing():

    html = """
    <html><body>
      <ol class="ecl-timeline">
        <li class="ecl-timeline__item ecl-timeline__item--current">
          <div class="ecl-timeline__content">No title here</div>
        </li>
      </ol>
    </body></html>
    """

    with pytest.raises(FieldValueError) as excinfo:
        extract_current_status(_soup(html))

    msg = str(excinfo.value)
    assert "contains no title element" in msg
