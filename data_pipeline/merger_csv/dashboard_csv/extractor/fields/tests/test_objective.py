"""
Tests for data_pipeline.merger_csv.dashboard_csv.extractor.fields.objective.

Covered behaviour:
- None, empty string, and whitespace normalisation.
- Outer whitespace stripping.
- Collapsing of multiple internal newlines to a single newline.
"""

import pytest

from data_pipeline.merger_csv.dashboard_csv.extractor.fields.objective import extract


class TestExtractObjective:
    """Tests for the objective field extraction and cleaning logic."""

    @pytest.mark.parametrize(
        "raw",
        [None, "", "   ", "\t", "\n\n", " \n "],
    )
    def test_empty_or_none(self, raw: str | None) -> None:
        """Empty, whitespace-only, and None values return an empty string."""

        assert extract(raw) == ""

    def test_strips_outer_whitespace(self) -> None:
        """Leading and trailing whitespace is completely stripped."""

        raw = "   \n  To protect the environment.  \n\n  "
        assert extract(raw) == "To protect the environment."

    def test_collapses_multiple_newlines(self) -> None:
        """Multiple consecutive newlines are collapsed to a single newline."""

        raw = (
            "First objective point.\n"
            "\n"
            "\n"
            "Second objective point.\n"
            "\n"
            "Third objective point."
        )
        expected = (
            "First objective point.\n"
            "Second objective point.\n"
            "Third objective point."
        )
        assert extract(raw) == expected

    def test_normal_text_unaffected(self) -> None:
        """Standard text with single newlines remains intact."""

        raw = "Point 1.\nPoint 2.\nPoint 3."
        assert extract(raw) == raw
