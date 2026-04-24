"""Tests for responses_followup.extractor.load_metadata."""

import csv
from unittest.mock import patch

import pytest

from data_pipeline.extractor.responses_followup.extractor.load_metadata import (
    _load_responses_metadata,
    load_metadata,
)

FILE_ENCODING = "utf-8"

FIELDNAMES = [
    "registration_number",
    "initiative_url",
    "response_url",
    "followup_url",
    "title",
]


def _write_csv(path, rows):

    with open(path, "w", newline="", encoding=FILE_ENCODING) as f:

        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


# Helper to build a minimal valid CSV row with current field names
def _row(reg, initiative_url="u", response_url="r", followup_url="f", title="T"):
    return {
        "registration_number": reg,
        "initiative_url": initiative_url,
        "response_url": response_url,
        "followup_url": followup_url,
        "title": title,
    }


class TestLoadResponsesMetadata:

    def test_filters_by_reg_numbers(self, tmp_path):

        csv_path = tmp_path / "initiatives.csv"
        _write_csv(
            csv_path,
            [
                _row(
                    "2020/000001",
                    initiative_url="u1",
                    response_url="r1",
                    followup_url="f1",
                    title="T1",
                ),
                _row(
                    "2020/000002",
                    initiative_url="u2",
                    response_url="r2",
                    followup_url="f2",
                    title="T2",
                ),
            ],
        )

        result = _load_responses_metadata(csv_path, reg_numbers={"2020/000001"})

        assert "2020/000001" in result
        assert "2020/000002" not in result

    def test_returns_full_row(self, tmp_path):

        csv_path = tmp_path / "initiatives.csv"
        _write_csv(
            csv_path,
            [
                _row(
                    "2020/000001",
                    initiative_url="u1",
                    response_url="r1",
                    followup_url="f1",
                    title="T1",
                )
            ],
        )

        result = _load_responses_metadata(csv_path, reg_numbers={"2020/000001"})

        row = result["2020/000001"]
        assert row["registration_number"] == "2020/000001"

        assert row["initiative_url"] == "u1"
        assert row["response_url"] == "r1"
        assert row["followup_url"] == "f1"
        assert row["title"] == "T1"

    def test_empty_reg_numbers_returns_empty(self, tmp_path):

        csv_path = tmp_path / "initiatives.csv"
        _write_csv(
            csv_path,
            [
                _row(
                    "2020/000001",
                    initiative_url="u1",
                    response_url="r1",
                    followup_url="f1",
                    title="T1",
                )
            ],
        )

        result = _load_responses_metadata(csv_path, reg_numbers=set())

        assert result == {}


class TestLoadMetadata:

    def test_raises_when_html_has_no_csv_match(self, tmp_path):

        csv_path = tmp_path / "initiatives.csv"
        _write_csv(
            csv_path,
            [
                _row(
                    "2020/000001",
                    initiative_url="u1",
                    response_url="r1",
                    followup_url="f1",
                    title="T1",
                )
            ],
        )

        html_files = {
            "2020/000001": tmp_path / "2020_000001_en.html",
            "2020/000099": tmp_path / "2020_000099_en.html",
        }

        with pytest.raises(FileNotFoundError, match="no matching CSV record"):
            load_metadata(csv_path, html_files)

    def test_happy_path_returns_metadata(self, tmp_path):

        csv_path = tmp_path / "initiatives.csv"
        _write_csv(
            csv_path,
            [
                _row(
                    "2020/000001",
                    initiative_url="u1",
                    response_url="r1",
                    followup_url="f1",
                    title="T1",
                )
            ],
        )

        html_files = {"2020/000001": tmp_path / "2020_000001_en.html"}

        result = load_metadata(csv_path, html_files)

        assert result["2020/000001"]["title"] == "T1"
