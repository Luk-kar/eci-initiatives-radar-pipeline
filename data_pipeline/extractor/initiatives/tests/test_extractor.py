"""
Tests for data_pipeline.extractor.initiatives.extractor.
"""

import csv
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from data_pipeline.extractor.extractor_shared.errors import HTMLParseError
from data_pipeline.extractor.initiatives.extractor import extract_initiatives
from data_pipeline.extractor.initiatives.model import ECIInitiativeDetailsRecord

from data_pipeline.pipeline_shared.consts import FILE_ENCODING
from data_pipeline.pipeline_shared.sort import sort_by_registration_number

_SHARED_SORT = (
    "data_pipeline.extractor.extractor_shared.extractor.sort_by_registration_number"
)
_PARSER_PARSE = "data_pipeline.extractor.initiatives.parser.ECIHTMLParser.parse"

# ── Helpers ────────────────────────────────────────────────────────────────────


def _make_year_dir(base: Path, year: str = "2023") -> Path:
    year_dir = base / year
    year_dir.mkdir(parents=True)
    return year_dir


def _write_html(year_dir: Path, name: str, content: str = "<html></html>") -> Path:
    html_file = year_dir / name
    html_file.write_text(content, encoding=FILE_ENCODING)
    return html_file


def _minimal_record() -> dict:
    return {name: "" for name in ECIInitiativeDetailsRecord.model_fields}


# ── extract_initiatives ────────────────────────────────────────────────────────


class TestExtractInitiatives:

    def test_raises_when_source_dir_missing(self, tmp_path):

        source_dir = tmp_path / "nonexistent"
        output_csv = tmp_path / "out.csv"

        with pytest.raises(FileNotFoundError, match="No HTML files found"):
            extract_initiatives(source_dir, output_csv)

    def test_raises_when_no_html_files(self, tmp_path):

        source_dir = tmp_path / "initiatives"
        _make_year_dir(source_dir)
        output_csv = tmp_path / "out.csv"

        with pytest.raises(FileNotFoundError, match="No HTML files found"):
            extract_initiatives(source_dir, output_csv)

    def test_raises_when_all_html_files_are_empty(self, tmp_path):

        source_dir = tmp_path / "initiatives"
        year_dir = _make_year_dir(source_dir)

        _write_html(year_dir, "2023_000001.html", content="")
        output_csv = tmp_path / "out.csv"

        with pytest.raises(FileNotFoundError, match="No HTML files found"):
            extract_initiatives(source_dir, output_csv)

    def test_creates_output_csv_with_correct_headers(self, tmp_path):

        source_dir = tmp_path / "initiatives"
        year_dir = _make_year_dir(source_dir)

        _write_html(year_dir, "2023_000001.html")
        output_csv = tmp_path / "out.csv"

        expected_columns = [name for name in ECIInitiativeDetailsRecord.model_fields]

        with patch(
            _PARSER_PARSE,
            return_value=_minimal_record(),
        ):
            extract_initiatives(source_dir, output_csv)

        assert output_csv.exists()
        with open(output_csv, encoding=FILE_ENCODING) as f:
            reader = csv.DictReader(f)
            assert reader.fieldnames == expected_columns

    def test_writes_one_row_per_html_file(self, tmp_path):

        source_dir = tmp_path / "initiatives"
        year_dir = _make_year_dir(source_dir)

        _write_html(year_dir, "2023_000001.html")
        _write_html(year_dir, "2023_000002.html")

        output_csv = tmp_path / "out.csv"

        with patch(
            _PARSER_PARSE,
            return_value=_minimal_record(),
        ):
            extract_initiatives(source_dir, output_csv)

        with open(output_csv, encoding=FILE_ENCODING) as f:
            rows = list(csv.DictReader(f))

        assert len(rows) == 2

    def test_creates_output_parent_dirs(self, tmp_path):
        source_dir = tmp_path / "initiatives"
        year_dir = _make_year_dir(source_dir)

        _write_html(year_dir, "2023_000001.html")
        output_csv = tmp_path / "nested" / "deep" / "out.csv"

        with patch(
            _PARSER_PARSE,
            return_value=_minimal_record(),
        ):
            extract_initiatives(source_dir, output_csv)

        assert output_csv.exists()

    def test_raises_html_parse_error_on_parse_failure(self, tmp_path):

        source_dir = tmp_path / "initiatives"
        year_dir = _make_year_dir(source_dir)

        _write_html(year_dir, "2023_000001.html")
        output_csv = tmp_path / "out.csv"

        with patch(
            _PARSER_PARSE,
            side_effect=ValueError("bad HTML"),
        ):
            with pytest.raises(HTMLParseError, match="Failed to parse"):
                extract_initiatives(source_dir, output_csv)

    def test_ignores_non_year_directories(self, tmp_path):

        source_dir = tmp_path / "initiatives"
        source_dir.mkdir()
        (source_dir / "misc").mkdir()

        _write_html(source_dir / "misc", "misc.html")
        output_csv = tmp_path / "out.csv"

        with pytest.raises(FileNotFoundError):
            extract_initiatives(source_dir, output_csv)

    def test_processes_multiple_years(self, tmp_path):

        source_dir = tmp_path / "initiatives"
        _write_html(_make_year_dir(source_dir, "2022"), "2022_000001.html")
        _write_html(_make_year_dir(source_dir, "2023"), "2023_000001.html")

        output_csv = tmp_path / "out.csv"

        with patch(
            _PARSER_PARSE,
            return_value=_minimal_record(),
        ):
            extract_initiatives(source_dir, output_csv)

        with open(output_csv, encoding=FILE_ENCODING) as f:
            rows = list(csv.DictReader(f))

        assert len(rows) == 2

    def test_missing_fields_default_to_empty_string(self, tmp_path):

        source_dir = tmp_path / "initiatives"
        year_dir = _make_year_dir(source_dir)

        _write_html(year_dir, "2023_000001.html")
        output_csv = tmp_path / "out.csv"

        with patch(
            _PARSER_PARSE,
            return_value={"registration_number": "ECI(2023)000001"},
        ):
            extract_initiatives(source_dir, output_csv)

        with open(output_csv, encoding=FILE_ENCODING) as f:
            row = list(csv.DictReader(f))[0]

        assert row["title"] == ""
        assert row["registration_number"] == "ECI(2023)000001"


# ── Row ordering guard ─────────────────────────────────────────────────────────


class TestRowOrderingByRegistrationNumber:
    """The extractor must hand rows to the writer ordered by registration_number."""

    _SCRAMBLED_BY_FILENAME = {
        "2021_000003.html": "2021/000003",
        "2012_000001.html": "2012/000001",
        "2017_000002.html": "2017/000002",
    }

    def _scrambled_parse(self, html_file: Path) -> dict:

        record = _minimal_record()
        record["registration_number"] = self._SCRAMBLED_BY_FILENAME[html_file.name]
        return record

    def _build_scrambled_tree(self, source_dir: Path) -> None:

        for filename, reg in self._SCRAMBLED_BY_FILENAME.items():

            year = reg.split("/", 1)[0]
            _write_html(_make_year_dir(source_dir, year), filename)

    def test_output_csv_rows_are_sorted_ascending_by_registration_number(
        self, tmp_path
    ):

        source_dir = tmp_path / "initiatives"
        self._build_scrambled_tree(source_dir)
        output_csv = tmp_path / "out.csv"

        with patch(_PARSER_PARSE, side_effect=self._scrambled_parse):
            extract_initiatives(source_dir, output_csv)

        with open(output_csv, encoding=FILE_ENCODING) as f:
            actual = [row["registration_number"] for row in csv.DictReader(f)]

        assert actual == ["2012/000001", "2017/000002", "2021/000003"]

    def test_extract_initiatives_invokes_shared_sort_helper(self, tmp_path):
        """Guard against silent regressions: the sort step must be wired in."""

        source_dir = tmp_path / "initiatives"
        self._build_scrambled_tree(source_dir)
        output_csv = tmp_path / "out.csv"

        with patch(_PARSER_PARSE, side_effect=self._scrambled_parse), patch(
            _SHARED_SORT, wraps=sort_by_registration_number
        ) as sort_spy:

            extract_initiatives(source_dir, output_csv)

        sort_spy.assert_called_once()
        passed_rows = sort_spy.call_args.args[0]
        assert {r["registration_number"] for r in passed_rows} == {
            "2012/000001",
            "2017/000002",
            "2021/000003",
        }
