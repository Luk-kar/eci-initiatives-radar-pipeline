from bs4 import BeautifulSoup

from data_pipeline.extractor.initiatives.parser.fields.signatures.total import (
    extract_signatures_collected,
)


def _soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")


def test_signatures_collected_returns_none_when_no_table_and_no_counter():

    html = "<html><body><p>No signatures info here.</p></body></html>"
    assert extract_signatures_collected(_soup(html)) is None


def test_signatures_collected_reads_total_row_from_table():

    html = """
    <html><body>
      <table class="ecl-table">
        <tr class="ecl-table__row">
          <td class="ecl-table__cell">Total number of signatories</td>
          <td class="ecl-table__cell">1,145,525</td>
        </tr>
      </table>
    </body></html>
    """
    result = extract_signatures_collected(_soup(html))

    # Spaces removed, commas preserved
    assert result == "1,145,525"


def test_signatures_collected_ignores_rows_without_total_label():

    html = """
    <html><body>
      <table class="ecl-table">
        <tr class="ecl-table__row">
          <td class="ecl-table__cell">Germany</td>
          <td class="ecl-table__cell">150,430</td>
        </tr>
      </table>
    </body></html>
    """

    # No matching total row and no counter; expect None
    assert extract_signatures_collected(_soup(html)) is None


def test_signatures_collected_uses_fallback_counter_element():

    html = """
    <html><body>
      <div class="ecl-counter__value">
        1 234 567 signatories collected
      </div>
    </body></html>
    """

    result = extract_signatures_collected(_soup(html))
    # Fallback strips spaces and commas, then joins digits
    assert result == "1234567"
