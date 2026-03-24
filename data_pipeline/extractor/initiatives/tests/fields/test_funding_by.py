from pathlib import Path
import json

from bs4 import BeautifulSoup

from data_pipeline.extractor.initiatives.parser.fields.funding.by import (
    extract_funding_by,
)


def _soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")


def _call(html: str):
    """Helper to call extract_funding_by with dummy metadata."""

    return extract_funding_by(
        _soup(html),
        filepath=Path("2023000001_en.html"),
        title="Sample Initiative",
        url="https://citizens-initiative.europa.eu/initiatives/details/2023/000001_en",
    )


def test_funding_by_returns_none_when_no_matching_table():

    html = """
    <html><body>
      <table class="ecl-table">
        <tr class="ecl-table__row">
          <th class="ecl-table__header">Something else</th>
        </tr>
      </table>
    </body></html>
    """

    assert _call(html) is None


def test_funding_by_parses_single_valid_row():

    html = """
    <html><body>
      <table class="ecl-table">
        <thead class="ecl-table__head">
          <tr class="ecl-table__row">
            <th class="ecl-table__header">Name of sponsor</th>
            <th class="ecl-table__header">Date</th>
            <th class="ecl-table__header">Amount in EUR</th>
          </tr>
        </thead>
        <tbody class="ecl-table__body">
          <tr class="ecl-table__row">
            <td class="ecl-table__cell">Sponsor A</td>
            <td class="ecl-table__cell">01/01/2024</td>
            <td class="ecl-table__cell">10,000</td>
          </tr>
        </tbody>
      </table>
    </body></html>
    """

    raw = _call(html)
    assert raw is not None

    data = json.loads(raw)
    assert isinstance(data, list)
    assert data == [
        {
            "name_of_sponsor": "Sponsor A",
            "date": "01/01/2024",
            "amount_in_eur": "10,000",
        }
    ]


def test_funding_by_skips_rows_with_incorrect_cell_count():

    html = """
    <html><body>
      <table class="ecl-table">
        <thead class="ecl-table__head">
          <tr class="ecl-table__row">
            <!-- should be ignored -->
            <th class="ecl-table__header">Name of sponsor</th>
            <th class="ecl-table__header">Date</th>
            <th class="ecl-table__header">Amount in EUR</th>
          </tr>
        </thead>
        <tbody class="ecl-table__body">
          <tr class="ecl-table__row">
            <!-- should be ignored -->
            <td class="ecl-table__cell">Incomplete</td>
            <td class="ecl-table__cell">01/02/2024</td>
          </tr>
          <tr class="ecl-table__row">
            <!-- should be taken -->
            <td class="ecl-table__cell">Sponsor B</td>
            <td class="ecl-table__cell">02/02/2024</td>
            <td class="ecl-table__cell">5,000</td>
          </tr>
        </tbody>
      </table>
    </body></html>
    """

    raw = _call(html)
    assert raw is not None

    data = json.loads(raw)
    assert len(data) == 1
    assert data[0]["name_of_sponsor"] == "Sponsor B"
