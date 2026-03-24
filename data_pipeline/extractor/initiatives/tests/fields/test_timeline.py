import json

from bs4 import BeautifulSoup
import pytest

from data_pipeline.extractor.initiatives.parser.fields.timeline import (
    extract_timeline_data,
)
from data_pipeline.extractor.extractor_shared.errors import FieldValueError


def _soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")


def test_timeline_extracts_basic_fields_and_json():

    html = """
    <html><body>
      <ol class="ecl-timeline">
        <li class="ecl-timeline__item">
          <div class="ecl-timeline__title">Registered</div>
          <div class="ecl-timeline__content">10/05/2018</div>
        </li>
        <li class="ecl-timeline__item">
          <div class="ecl-timeline__title">Collection start date</div>
          <div class="ecl-timeline__content">10/11/2018</div>
        </li>
        <li class="ecl-timeline__item">
          <div class="ecl-timeline__title">Collection closed</div>
          <div class="ecl-timeline__content">10/11/2019</div>
        </li>
      </ol>
    </body></html>
    """

    data = extract_timeline_data(_soup(html))
    assert data["timeline_registered"] == "10/05/2018"
    assert data["timeline_collection_start_date"] == "10/11/2018"
    assert data["timeline_collection_closed"] == "10/11/2019"

    timeline_json = json.loads(data["timeline"])
    steps = [e["step"] for e in timeline_json]
    assert steps == [
        "Registered",
        "Collection start date",
        "Collection closed",
    ]


def test_timeline_sets_verification_end_based_on_sequence():

    html = """
    <html><body>
      <ol class="ecl-timeline">
        <li class="ecl-timeline__item">
          <div class="ecl-timeline__title">Verification</div>
          <div class="ecl-timeline__content">01/01/2022</div>
        </li>
        <li class="ecl-timeline__item">
          <div class="ecl-timeline__title">Valid initiative</div>
          <div class="ecl-timeline__content">15/02/2022</div>
        </li>
        <li class="ecl-timeline__item">
          <div class="ecl-timeline__title">Answered initiative</div>
          <div class="ecl-timeline__content">01/06/2022</div>
        </li>
      </ol>
    </body></html>
    """

    data = extract_timeline_data(_soup(html))
    # _process_verification_end should pick the 'Valid initiative' date.
    assert data["timeline_verification_end"] == "15/02/2022", data


def test_timeline_raises_when_timeline_present_but_no_recognised_titles():

    html = """
    <html><body>
      <ol class="ecl-timeline">
        <li class="ecl-timeline__item">
          <div class="ecl-timeline__title">Some unknown step</div>
          <div class="ecl-timeline__content">01/01/2020</div>
        </li>
      </ol>
    </body></html>
    """

    with pytest.raises(FieldValueError) as excinfo:
        extract_timeline_data(_soup(html))
    msg = str(excinfo.value)
    assert "no recognisable fields" in msg
