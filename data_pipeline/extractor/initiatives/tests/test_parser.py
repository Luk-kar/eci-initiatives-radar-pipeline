"""
Tests for data_pipeline.extractor.initiatives.parser.ECIHTMLParser.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from bs4 import BeautifulSoup

from data_pipeline.extractor.initiatives.model import ECIInitiativeDetailsRecord
from data_pipeline.extractor.initiatives.parser import ECIHTMLParser

from data_pipeline.pipeline_shared.consts import FILE_ENCODING

FIXTURES_DIR = Path(__file__).parent / "fixtures"

_PARSER_MODULE = "data_pipeline.extractor.initiatives.parser"


class TestECIHTMLParserCsvColumns:

    def test_csv_columns_matches_model_fields(self):

        expected = list(ECIInitiativeDetailsRecord.model_fields)

        assert ECIHTMLParser.csv_columns == expected

    def test_csv_columns_is_class_attribute(self):

        assert "csv_columns" in ECIHTMLParser.__dict__

    def test_csv_columns_not_empty(self):

        assert len(ECIHTMLParser.csv_columns) > 0


class TestECIHTMLParserParse:

    @pytest.fixture()
    def parser(self):
        return ECIHTMLParser()

    @pytest.fixture()
    def sample_html(self, tmp_path) -> Path:

        src = FIXTURES_DIR / "2020_000001.html"
        dest = tmp_path / "2023" / "2023_000008.html"
        dest.parent.mkdir(parents=True)
        dest.write_text(src.read_text(encoding=FILE_ENCODING), encoding=FILE_ENCODING)

        return dest

    def test_parse_returns_dict(self, parser, sample_html):

        with patch.multiple(
            _PARSER_MODULE,
            extract_registration_number=MagicMock(return_value="ECI(2018)000008"),
            extract_title=MagicMock(return_value="Save bees and farmers"),
            extract_objective=MagicMock(return_value="To protect biodiversity"),
            extract_annex=MagicMock(return_value=None),
            extract_current_status=MagicMock(return_value="Answer given"),
            construct_url=MagicMock(return_value="https://europa.eu/eci/000008"),
            extract_timeline_data=MagicMock(
                return_value={
                    "timeline_registered": "10/05/2018",
                    "timeline": '[{"step":"Registered","date":"10/05/2018"}]',
                }
            ),
            extract_funding_total=MagicMock(return_value=None),
            extract_funding_by=MagicMock(return_value=None),
            extract_signatures_collected=MagicMock(return_value="1145525"),
            extract_signatures_by_country=MagicMock(return_value=None),
            extract_signatures_countries_threshold_met_count=MagicMock(
                return_value=None
            ),
            extract_response_commission_url=MagicMock(return_value=None),
        ):
            result = parser.parse(sample_html)

        assert isinstance(result, dict)

    def test_parse_result_contains_all_csv_columns(self, parser, sample_html):
        with patch.multiple(
            _PARSER_MODULE,
            extract_registration_number=MagicMock(return_value="ECI(2018)000008"),
            extract_title=MagicMock(return_value="Save bees and farmers"),
            extract_objective=MagicMock(return_value="To protect biodiversity"),
            extract_annex=MagicMock(return_value=None),
            extract_current_status=MagicMock(return_value="Answer given"),
            construct_url=MagicMock(return_value="https://europa.eu/eci/000008"),
            extract_timeline_data=MagicMock(
                return_value={
                    "timeline_registered": "10/05/2018",
                    "timeline": '[{"step":"Registered","date":"10/05/2018"}]',
                }
            ),
            extract_funding_total=MagicMock(return_value=None),
            extract_funding_by=MagicMock(return_value=None),
            extract_signatures_collected=MagicMock(return_value="1145525"),
            extract_signatures_by_country=MagicMock(return_value=None),
            extract_signatures_countries_threshold_met_count=MagicMock(
                return_value=None
            ),
            extract_response_commission_url=MagicMock(return_value=None),
        ):
            result = parser.parse(sample_html)

        # All CSV columns should be present in the result
        for column in parser.csv_columns:
            assert column in result

    def test_parse_raises_value_error_on_missing_file(self, parser, tmp_path):

        missing = tmp_path / "2023" / "2023_000099.html"

        with pytest.raises(ValueError, match="Error parsing"):
            parser.parse(missing)

    def test_parse_raises_value_error_on_malformed_html(self, parser, tmp_path):

        bad_html = tmp_path / "2023" / "2023_000001.html"
        bad_html.parent.mkdir(parents=True)
        bad_html.write_text("<not valid", encoding=FILE_ENCODING)

        with patch(
            f"{_PARSER_MODULE}.extract_title",
            side_effect=RuntimeError("boom"),
        ):
            with pytest.raises(ValueError, match="Error parsing"):
                parser.parse(bad_html)

    def test_parse_chains_original_exception(self, parser, tmp_path):

        bad_html = tmp_path / "2023" / "2023_000001.html"
        bad_html.parent.mkdir(parents=True)
        bad_html.write_text("<html></html>", encoding=FILE_ENCODING)

        original = RuntimeError("original cause")

        with patch(
            f"{_PARSER_MODULE}.extract_title",
            side_effect=original,
        ):
            with pytest.raises(ValueError) as exc_info:
                parser.parse(bad_html)

        if exc_info.value.__cause__ is not original:
            raise exc_info.value.__cause__

        assert exc_info.value.__cause__ is original
