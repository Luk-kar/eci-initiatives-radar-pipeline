# data_pipeline/extractor/initiatives/tests/fields/test_signatures_by_country.py

import json
from pathlib import Path

from bs4 import BeautifulSoup

from data_pipeline.extractor.initiatives.parser.fields.signatures.by_country import (
    extract_signatures_by_country,
)


def _soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")


def _call(html: str):
    return extract_signatures_by_country(
        _soup(html),
        filepath=Path("2023_000001_en.html"),
        title="Sample Initiative",
        url="https://citizens-initiative.europa.eu/initiatives/details/2023/000001_en",
    )


def test_signatures_by_country_returns_none_when_no_table():

    html = "<html><body><p>No signatures table here.</p></body></html>"
    assert _call(html) is None


def test_signatures_by_country_serializes_country_rows_to_json():

    html = """
    <html><body>
      <table class="ecl-table">
        <tr class="ecl-table__row">
          <td class="ecl-table__cell">Germany</td>
          <td class="ecl-table__cell">150,430</td>
          <td class="ecl-table__cell">71,695</td>
          <td class="ecl-table__cell">209.82%</td>
        </tr>
        <tr class="ecl-table__row">
          <td class="ecl-table__cell">France</td>
          <td class="ecl-table__cell">80,000</td>
          <td class="ecl-table__cell">55,000</td>
          <td class="ecl-table__cell">145.45%</td>
        </tr>
      </table>
    </body></html>
    """
    raw = _call(html)
    assert raw is not None

    data = json.loads(raw)
    assert set(data.keys()) == {"Germany", "France"}
    assert data["Germany"] == {
        "signatures": "150,430",
        "threshold": "71,695",
        "percentage": "209.82%",
    }
    assert data["France"]["signatures"] == "80,000"


def test_signatures_by_country_includes_countries_with_missing_fields():

    # Missing percentage for France; extractor should still include the country
    html = """
    <html><body>
      <table class="ecl-table">
        <tr class="ecl-table__row">
          <td class="ecl-table__cell">France</td>
          <td class="ecl-table__cell">80,000</td>
          <td class="ecl-table__cell">55,000</td>
          <td class="ecl-table__cell"></td>
        </tr>
      </table>
    </body></html>
    """
    raw = _call(html)
    assert raw is not None

    data = json.loads(raw)
    assert data["France"] == {
        "signatures": "80,000",
        "threshold": "55,000",
        "percentage": "",
    }
