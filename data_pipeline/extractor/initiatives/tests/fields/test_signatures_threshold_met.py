from bs4 import BeautifulSoup

from data_pipeline.extractor.initiatives.parser.fields.signatures.threshold_met import (
    extract_signatures_threshold_met,
)


def _soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")


def test_signatures_threshold_met_returns_none_when_no_table():

    html = "<html><body><p>No signatures table here.</p></body></html>"
    assert extract_signatures_threshold_met(_soup(html)) is None


def test_signatures_threshold_met_counts_countries_with_percentage_at_least_100():

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
          <td class="ecl-table__cell">99.9%</td>
        </tr>
        <tr class="ecl-table__row">
          <td class="ecl-table__cell">Italy</td>
          <td class="ecl-table__cell">60,000</td>
          <td class="ecl-table__cell">45,000</td>
          <td class="ecl-table__cell">100%</td>
        </tr>
      </table>
    </body></html>
    """
    # Germany (209.82%) and Italy (100%) count; France (99.9%) does not.
    result = extract_signatures_threshold_met(_soup(html))
    assert result == "2"


def test_signatures_threshold_met_handles_non_numeric_percentage_gracefully():

    html = """
    <html><body>
      <table class="ecl-table">
        <tr class="ecl-table__row">
          <td class="ecl-table__cell">Spain</td>
          <td class="ecl-table__cell">50,000</td>
          <td class="ecl-table__cell">40,000</td>
          <td class="ecl-table__cell">N/A</td>
        </tr>
      </table>
    </body></html>
    """
    # Regex will fail to find a number in "N/A", so this row is ignored.
    result = extract_signatures_threshold_met(_soup(html))
    assert result == "0"
