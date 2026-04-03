"""Tests for responses.extractor.write."""

import csv
import json

import pytest

from data_pipeline.extractor.responses.model import ECIFollowupRecord
from data_pipeline.extractor.responses.extractor.write import write_csv


def _make_record(**kwargs):

    return ECIFollowupRecord(
        **{
            "registration_number": "2020/000001",
            "initiative_url": "https://ec.europa.eu/initiative/1",
            "response_url": "https://ec.europa.eu/response/1",
            "title": "Test Initiative",
            **kwargs,
        }
    )


class TestWriteCsv:

    def test_creates_output_file(self, tmp_path):

        out = tmp_path / "result.csv"
        write_csv([_make_record()], out)

        assert out.exists()

    def test_creates_parent_directories(self, tmp_path):

        out = tmp_path / "a" / "b" / "result.csv"
        write_csv([_make_record()], out)

        assert out.exists()

    def test_raises_on_empty_records(self, tmp_path):

        with pytest.raises(ValueError, match="No records to write"):
            write_csv([], tmp_path / "result.csv")

    def test_header_matches_model_fields(self, tmp_path):

        out = tmp_path / "result.csv"
        write_csv([_make_record()], out)

        with open(out, encoding="utf-8") as f:
            assert set(csv.DictReader(f).fieldnames) == set(
                ECIFollowupRecord.model_fields.keys()
            )

    def test_row_count_matches_records(self, tmp_path):

        out = tmp_path / "result.csv"
        write_csv(
            [_make_record(registration_number=f"2020/{i:06d}") for i in range(5)], out
        )

        with open(out, encoding="utf-8") as f:
            assert len(list(csv.DictReader(f))) == 5

    def test_list_fields_serialized_as_json_string(self, tmp_path):

        out = tmp_path / "result.csv"
        write_csv(
            [_make_record(followup_events=["A", "B"])],
            out,
        )

        with open(out, encoding="utf-8") as f:
            row = next(csv.DictReader(f))

        assert row["followup_events"] == json.dumps(["A", "B"], ensure_ascii=False)

    def test_none_fields_written_as_empty_string(self, tmp_path):

        out = tmp_path / "result.csv"
        write_csv([_make_record()], out)

        with open(out, encoding="utf-8") as f:
            row = next(csv.DictReader(f))

        assert row["commission_answer_text"] == ""
        assert row["followup_events"] == ""
