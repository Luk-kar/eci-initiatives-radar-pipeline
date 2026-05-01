"""
Tests for data_pipeline.merger_csv.dashboard_csv.extractor.fields.model
"""

import typing

import pytest

from data_pipeline.merger_csv.dashboard_csv.extractor.fields.model import DashboardRow


class TestDashboardRow:
    """Tests for the DashboardRow output dataclass/model."""

    def test_dashboard_row_instantiation(self) -> None:
        """DashboardRow can be instantiated with all required fields."""

        row = DashboardRow(
            registration_number="2024/000001",
            title="Save the Bees",
            registration_year="2024",
            # Dates updated to DD/MM/YYYY
            registration_date="01/01/2024",
            current_status="Collection Ongoing",
            objective="To protect bees in the EU",
            commission_answer_text="",
            # URL updated to match new domain and _en suffix regex
            initiative_url="https://citizens-initiative.europa.eu/initiatives/details/2024/000001_en",
            signatures_collected_by_country='{"Germany": {"signatures": 137874, "threshold": 74250, "percentage": 185.68}, "Austria": {"signatures": 24973, "threshold": 14250, "percentage": 175.25}, "Poland": {"signatures": 38000, "threshold": 36660, "percentage": 103.65}}',
            signatures_countries_threshold_met_count="3",
            # Numbers updated to use comma formatting
            signatures_collected="1,120,000",
            funding_total="150,000",
            # Dates updated to DD/MM/YYYY
            timeline_collection_closed="01/01/2025",
            timeline_collection_start="01/01/2024",
            law_passed="",
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
            "commission_answer_text",
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

    def test_all_fields_are_strings(self) -> None:
        """
        Verify that all fields are strictly typed as strings or string literals.
        """
        for field_name, field_info in DashboardRow.model_fields.items():

            annotation = field_info.annotation
            origin = typing.get_origin(annotation)

            if origin is typing.Literal:

                # If it's a Literal, ensure all literal arguments are strings
                all_args_are_strings = all(
                    isinstance(arg, str) for arg in typing.get_args(annotation)
                )
                assert (
                    all_args_are_strings
                ), f"Expected Literal args for {field_name} to be strings"
            else:
                # Otherwise, strictly check for str
                assert (
                    annotation == str
                ), f"Expected field {field_name} to be typed as str or Literal[str], got {annotation}"
