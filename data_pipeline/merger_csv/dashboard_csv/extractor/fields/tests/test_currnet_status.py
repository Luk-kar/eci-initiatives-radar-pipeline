"""
Tests for ``data_pipeline.merger_csv.dashboard_csv.extractor.fields.current_status``.

Covered behaviour:
  * Direct mapping for every source vocabulary value.
  * Whitespace / trailing-asterisk normalisation (``Verification\n*``).
  * Empty / None ``raw_status`` raise ``ValueError``.
  * Unknown source values raise ``ValueError`` carrying the original
    and normalised forms.
  * ``Answered initiative`` upgrade rules (``Law Passed``,
    ``Rejected Legislation``, ``Commission Engaged``).
  * ``Answered initiative`` with missing legislation flags raises
    ``ValueError`` (mandated-bool contract).
  * ``Answered initiative`` with conflicting true legislation flags raises
    ``ValueError``.
  * Legislation flags are ignored for non-answered statuses, even when
    truthy (defence-in-depth: a stray flag must not corrupt the mapping).
"""

from typing import get_args

import pytest

from data_pipeline.merger_csv.dashboard_csv.extractor.fields import current_status
from data_pipeline.merger_csv.dashboard_csv.extractor.fields.current_status import (
    _STATUS_MAP,
    extract,
)

from data_pipeline.merger_csv.dashboard_csv.extractor.fields.model import DashboardRow

# (raw_status, expected_dashboard_label)
_NON_ANSWERED_CASES: list[tuple[str, str]] = [
    ("Registered", "Awaiting Collection"),
    ("Collection ongoing", "Collection Ongoing"),
    ("Collection closed", "Collection Verification"),
    ("Verification", "Collection Verification"),
    ("Valid initiative", "Awaiting Response"),
    ("Unsuccessful collection", "Collection Unsuccessful"),
    ("Withdrawn", "Withdrawn"),
]


class TestDirectMapping:
    """Tests for direct mapping of non-answered source values to the dashboard vocabulary."""

    @pytest.mark.parametrize("raw, expected", _NON_ANSWERED_CASES)
    def test_direct_mapping(self, raw: str, expected: str) -> None:
        """Every non-answered source value maps to its dashboard label."""

        assert extract(raw, None, None) == expected

    def test_status_map_covers_all_source_values(self) -> None:
        """Guard against silent drift between the docstring vocabulary and the map."""

        expected_keys = {
            "Registered",
            "Collection ongoing",
            "Collection closed",
            "Verification",
            "Valid initiative",
            "Answered initiative",
            "Unsuccessful collection",
            "Withdrawn",
        }
        assert set(_STATUS_MAP) == expected_keys

    def test_status_map_targets_only_canonical_dashboard_labels(self) -> None:
        """The mapping's range must stay inside the documented dashboard vocabulary.

        Note: ``Law Passed`` and ``Rejected Legislation`` are not values of the
        map — they are produced by the ``Answered initiative`` upgrade branch.
        """

        canonical = set(
            get_args(DashboardRow.model_fields["current_status"].annotation)
        )

        assert set(_STATUS_MAP.values()).issubset(canonical)


class TestNormalisation:
    """Tests for whitespace, asterisks, and general string normalisation."""

    @pytest.mark.parametrize(
        "raw",
        [
            "Verification",
            "Verification ",
            " Verification",
            "Verification*",
            "Verification *",
            "Verification **",
            "Verification\n                 \n                  *",
            "  Verification\n*  ",
            "\tVerification\t*\t",
        ],
    )
    def test_verification_normalisation(self, raw: str) -> None:
        """All observed and plausible whitespace/asterisk variants normalise correctly."""
        assert extract(raw, None, None) == "Collection Verification"

    def test_internal_whitespace_collapses(self) -> None:
        """Embedded multi-space runs collapse to a single space before lookup."""
        assert extract("Collection   ongoing", None, None) == "Collection Ongoing"

    @pytest.mark.parametrize(
        "raw, expected",
        [
            (None, ""),
            ("", ""),
            ("   ", ""),
            ("\n\t  ", ""),
            ("*", ""),
            ("**", ""),
            ("Withdrawn", "Withdrawn"),
            ("  Withdrawn  ", "Withdrawn"),
            ("Withdrawn*", "Withdrawn"),
            ("Verification\n*", "Verification"),
        ],
    )
    def test_normalise_unit(self, raw: str | None, expected: str) -> None:
        """_normalise unit-level coverage (kept thin — extract() exercises the rest)."""
        assert current_status._normalise(raw) == expected


class TestErrorHandling:
    """Tests for exception raising on empty, missing, or unknown status strings."""

    @pytest.mark.parametrize("raw", ["", "   ", "\n\t", "*", "  *  "])
    def test_empty_raw_status_raises(self, raw: str) -> None:
        """An empty (or whitespace-only / bare-asterisk) raw_status is rejected."""
        with pytest.raises(ValueError, match="Unknown raw current_status value"):
            extract(raw, None, None)

    def test_none_raw_status_raises(self) -> None:
        """``None`` normalises to ``""`` and is rejected with the same error."""
        with pytest.raises(ValueError, match="Unknown raw current_status value"):
            extract(None, None, None)  # type: ignore[arg-type]

    def test_unknown_status_error_carries_original_and_normalised(self) -> None:
        """The error message must surface both the raw and normalised forms for triage."""
        with pytest.raises(ValueError) as exc_info:
            extract("  Mystery  state  *  ", None, None)
        msg = str(exc_info.value)
        assert "'  Mystery  state  *  '" in msg  # original, repr-quoted
        assert "'Mystery state'" in msg  # normalised, repr-quoted

    def test_case_sensitivity_is_strict(self) -> None:
        """Source vocabulary is case-sensitive: lowercase variants are unknown."""
        with pytest.raises(ValueError, match="Unknown raw current_status value"):
            extract("withdrawn", None, None)


class TestAnsweredInitiativeUpgrade:
    """Tests for the special refinement logic applied to 'Answered initiative' rows."""

    @pytest.mark.parametrize(
        "is_law_passed, rejected_legislation, expected",
        [
            (False, False, "Commission Engaged"),
            (True, False, "Law Passed"),
            (False, True, "Rejected Legislation"),
        ],
    )
    def test_answered_initiative_upgrade(
        self, is_law_passed: bool, rejected_legislation: bool, expected: str
    ) -> None:
        """The legislation flags refine ``Answered initiative`` into a verdict."""
        assert (
            extract("Answered initiative", is_law_passed, rejected_legislation)
            == expected
        )

    def test_answered_initiative_both_flags_true_raises(self) -> None:
        """A ValueError is raised when both legislation flags logically contradict each other."""
        with pytest.raises(
            ValueError,
            match="Law cannot be passed for the initiative, when the commission rejected to do so earlier",
        ):
            extract("Answered initiative", True, True)

    def test_answered_initiative_upgrade_after_normalisation(self) -> None:
        """Whitespace and trailing-asterisk normalisation also applies to the answered branch."""
        assert extract("  Answered\tinitiative *  ", True, False) == "Law Passed"

    @pytest.mark.parametrize(
        "is_law_passed, rejected_legislation",
        [
            (None, None),
            (None, False),
            (None, True),
            (False, None),
            (True, None),
        ],
    )
    def test_answered_initiative_missing_flags_raises(
        self, is_law_passed: bool | None, rejected_legislation: bool | None
    ) -> None:
        """``None`` flags signal an upstream contract violation and must abort the row."""
        with pytest.raises(ValueError, match="missing legislation flags"):
            extract("Answered initiative", is_law_passed, rejected_legislation)

    def test_missing_flags_error_carries_both_values(self) -> None:
        """Both flag values must appear in the error message for fast triage."""
        with pytest.raises(ValueError) as exc_info:
            extract("Answered initiative", None, False)
        msg = str(exc_info.value)
        assert "is_law_passed=None" in msg
        assert "rejected_legislation=False" in msg


class TestDefenseInDepth:
    """Tests ensuring logical isolation between different branch paths."""

    @pytest.mark.parametrize("raw, expected", _NON_ANSWERED_CASES)
    def test_non_answered_ignores_legislation_flags(
        self, raw: str, expected: str
    ) -> None:
        """A stray legislation flag on a non-answered row must not change the label."""
        assert extract(raw, True, True) == expected
        assert extract(raw, False, False) == expected
        assert extract(raw, None, None) == expected
