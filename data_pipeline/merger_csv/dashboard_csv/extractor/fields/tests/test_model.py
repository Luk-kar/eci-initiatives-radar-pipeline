"""
Tests for data_pipeline.merger_csv.dashboard_csv.extractor.fields.model
"""

import typing

import pytest
from pydantic import ValidationError

from data_pipeline.merger_csv.dashboard_csv.extractor.fields.model import DashboardRow


class TestDashboardRow:
    """Tests for the DashboardRow output dataclass/model."""

    def test_dashboard_row_instantiation(self) -> None:
        """DashboardRow can be instantiated with all required fields."""

        row = DashboardRow(
            registration_number="2024/000001",
            title="Save the Bees",
            registration_year=2024,
            registration_date="01/01/2024",
            current_status="Collection Ongoing",
            objective="To protect bees in the EU",
            commission_answer="",
            initiative_url="https://citizens-initiative.europa.eu/initiatives/details/2024/000001_en",
            signatures_collected_by_country="{'Germany': {'signatures': 137874, 'threshold': 74250, 'percentage': 185.68}}",
            signatures_countries_threshold_met_count=3,
            signatures_collected=1120000,
            funding_total=150000,
            timeline_collection_closed="01/01/2025",
            timeline_collection_start="01/01/2024",
            law_passed=None,  # <-- was ""
        )

        assert row.registration_number == "2024/000001"
        assert row.title == "Save the Bees"
        assert row.current_status == "Collection Ongoing"

    def test_field_order_and_presence(self) -> None:
        """
        Ensure the field order matches the legacy reference CSV schema.

        The CSV writer uses the model fields which returns fields in
        declaration order. Changing this order breaks downstream consumers.
        """
        expected_fields = [
            "registration_number",
            "title",
            "registration_year",
            "registration_date",
            "current_status",
            "objective",
            "commission_answer",
            "initiative_url",
            "signatures_collected_by_country",
            "signatures_countries_threshold_met_count",
            "signatures_collected",
            "funding_total",
            "timeline_collection_closed",
            "timeline_collection_start",
            "law_passed",
        ]

        # Updated to use Pydantic's internal model_fields
        actual_fields = list(DashboardRow.model_fields.keys())

        assert actual_fields == expected_fields, (
            "Field order or presence has changed! "
            "The CSV writer depends on the declaration order in the model."
        )


class TestDashboardRowTypes:

    STR_FIELDS = (
        "registration_number",
        "title",
        "registration_date",
        "current_status",
        "objective",
        "commission_answer",
        "initiative_url",
        "signatures_collected_by_country",
        "timeline_collection_closed",
        "timeline_collection_start",
    )

    LIST_STR_FIELDS = ("law_passed",)

    OPTIONAL_INT_FIELDS = (
        "signatures_countries_threshold_met_count",
        "signatures_collected",
    )

    REQUIRED_INT_FIELDS = ("registration_year",)

    FLOAT_FIELDS = ("funding_total",)

    def test_all_model_fields_are_accounted_for(self) -> None:

        expected_fields = (
            self.STR_FIELDS
            + self.LIST_STR_FIELDS
            + self.OPTIONAL_INT_FIELDS
            + self.REQUIRED_INT_FIELDS
            + self.FLOAT_FIELDS
        )

        actual_fields = list(DashboardRow.model_fields.keys())

        assert sorted(actual_fields) == sorted(expected_fields)

    def test_string_fields_are_typed_correctly(self) -> None:
        """
        Verify that designated string fields are strictly typed as strings or string literals.
        """
        for field_name in self.STR_FIELDS:
            field_info = DashboardRow.model_fields.get(field_name)
            assert (
                field_info is not None
            ), f"Field {field_name} is missing from the model"

            annotation = field_info.annotation
            origin = typing.get_origin(annotation)

            if origin is typing.Literal:
                all_args_are_strings = all(
                    isinstance(arg, str) for arg in typing.get_args(annotation)
                )
                assert (
                    all_args_are_strings
                ), f"Expected Literal args for {field_name} to be strings"
            else:
                assert annotation in (
                    str,
                    str | None,
                    typing.Optional[str],
                ), f"Expected field {field_name} to be typed as str, str | None, or Literal[str], got {annotation}"

    def test_optional_int_fields_are_typed_correctly(self) -> None:
        """
        Verify that designated integer fields are strictly typed as optional ints.
        """
        for field_name in self.OPTIONAL_INT_FIELDS:
            field_info = DashboardRow.model_fields.get(field_name)
            assert (
                field_info is not None
            ), f"Field {field_name} is missing from the model"

            annotation = field_info.annotation
            assert annotation in (
                int | None,
                typing.Optional[int],
            ), f"Expected field {field_name} to be typed as int | None, got {annotation}"

    def test_required_int_fields_are_typed_correctly(self) -> None:
        """
        Verify that designated required integer fields are strictly typed as ints.
        """
        for field_name in self.REQUIRED_INT_FIELDS:
            field_info = DashboardRow.model_fields.get(field_name)
            assert (
                field_info is not None
            ), f"Field {field_name} is missing from the model"

            annotation = field_info.annotation
            assert (
                annotation is int
            ), f"Expected field {field_name} to be typed as strict int, got {annotation}"

    def test_float_fields_are_typed_correctly(self) -> None:
        """
        Verify that designated float fields are strictly typed as optional floats.
        """
        for field_name in self.FLOAT_FIELDS:
            field_info = DashboardRow.model_fields.get(field_name)
            assert (
                field_info is not None
            ), f"Field {field_name} is missing from the model"

            annotation = field_info.annotation
            assert annotation in (
                float | None,
                typing.Optional[float],
            ), f"Expected field {field_name} to be typed as float | None, got {annotation}"

    def test_list_str_fields_are_typed_correctly(self) -> None:
        """law_passed and similar fields must be typed as list[str] | None."""
        import typing

        for field_name in self.LIST_STR_FIELDS:
            field_info = DashboardRow.model_fields.get(field_name)
            assert (
                field_info is not None
            ), f"Field {field_name!r} is missing from the model"
            annotation = field_info.annotation
            # Accept list[str] | None or Optional[list[str]]
            args = typing.get_args(annotation)
            assert list[str] in args or list in [
                typing.get_origin(a) for a in args if a is not type(None)
            ], f"Expected {field_name!r} to be list[str] | None, got {annotation}"


# Mock valid fields for everything EXCEPT what we are testing
@pytest.fixture
def mock_dashboard_row():
    return {
        "registration_number": "2024/000001",
        "title": "Valid Title",
        "registration_year": 2024,
        "registration_date": "01/01/2024",
        "current_status": "Collection Ongoing",
        "objective": "Valid Objective",
        "initiative_url": "https://citizens-initiative.europa.eu/initiatives/details/2024/000001_en",
        "timeline_collection_closed": "01/01/2025",
        "timeline_collection_start": "01/01/2024",
        "law_passed": None,
    }


class TestSignaturesCollected:

    @pytest.mark.parametrize(
        "valid_input, expected",
        [
            ("1,120,000", 1120000),
            ("0", 0),
            (42, 42),
            (" 500 ", 500),
        ],
    )
    def test_valid_natural_numbers(self, mock_dashboard_row, valid_input, expected):

        # Override just the field we care about
        mock_dashboard_row["signatures_collected"] = valid_input
        row = DashboardRow(**mock_dashboard_row)

        assert row.signatures_collected == expected

    @pytest.mark.parametrize("empty_input", [None, "", "   "])
    def test_empty_values_return_none(self, mock_dashboard_row, empty_input):

        mock_dashboard_row["signatures_collected"] = empty_input
        row = DashboardRow(**mock_dashboard_row)

        assert row.signatures_collected is None

    @pytest.mark.parametrize(
        "invalid_input",
        [
            "-1",
            "-50,000",
            "123.45",
            "NaN",
            "unknown",
        ],
    )
    def test_invalid_inputs_raise_errors(self, mock_dashboard_row, invalid_input):
        mock_dashboard_row["signatures_collected"] = invalid_input

        with pytest.raises(ValidationError) as exc_info:
            DashboardRow(**mock_dashboard_row)

        error_str = str(exc_info.value).lower()

        assert "must be a valid integer" in error_str or "natural number" in error_str
