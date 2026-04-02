"""Tests for data_pipeline.extractor.responses.extractor.configure."""

from unittest.mock import patch

from data_pipeline.extractor.responses.extractor import configure

PATTERN = "eci_responses_{timestamp}.csv"


class TestConfigure:

    def test_returns_string(self):

        with patch(
            "data_pipeline.extractor.responses.extractor.ECI_RESPONSES_CSV_PATTERN",
            PATTERN,
        ):

            assert isinstance(configure("2026-03-30_14-00-00"), str)

    def test_timestamp_embedded_in_filename(self):
        timestamp = "2026-03-30_14-00-00"

        with patch(
            "data_pipeline.extractor.responses.extractor.ECI_RESPONSES_CSV_PATTERN",
            PATTERN,
        ):
            result = configure(timestamp)

        assert timestamp in result
        assert result.startswith("eci_responses_")
        assert result.endswith(".csv")
        assert result == f"eci_responses_{timestamp}.csv"

    def test_different_timestamps_produce_different_filenames(self):

        with patch(
            "data_pipeline.extractor.responses.extractor.ECI_RESPONSES_CSV_PATTERN",
            PATTERN,
        ):

            assert configure("2026-01-01_00-00-00") != configure("2026-03-30_14-00-00")
