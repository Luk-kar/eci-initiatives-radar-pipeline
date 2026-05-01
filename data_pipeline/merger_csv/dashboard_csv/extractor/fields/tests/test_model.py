"""
Tests for data_pipeline.merger_csv.dashboard_csv.extractor.fields.model
"""

from dataclasses import fields
import pytest

from data_pipeline.merger_csv.dashboard_csv.extractor.fields.model import DashboardRow


class TestDashboardRow:
    """Tests for the DashboardRow output dataclass."""

    def test_dashboard_row_instantiation(self) -> None:
        """DashboardRow can be instantiated with all required fields."""

        row = DashboardRow(
            registration_number="2024/000001",
            title="Save the Bees",
            registration_year="2024",
            registration_date="2024-01-01",
            current_status="Collection Ongoing",
            objective="To protect bees in the EU",
            commission_answer_text="",
            initiative_url="https://europa.eu/citizens-initiative/initiatives/details/2024/000001",
            signatures_collected_by_country='{"Germany": {"signatures": 137874, "threshold": 74250, "percentage": 185.68}, "Austria": {"signatures": 24973, "threshold": 14250, "percentage": 175.25}, "Poland": {"signatures": 38000, "threshold": 36660, "percentage": 103.65}}',
            signatures_countries_threshold_met_count="3",
            signatures_collected="1120000",
            funding_total="150000",
            timeline_collection_closed="2025-01-01",
            timeline_collection_start="2024-01-01",
            law_passed="",
        )

        assert row.registration_number == "2024/000001"
        assert row.title == "Save the Bees"
        assert row.current_status == "Collection Ongoing"

    def test_field_order_and_presence(self) -> None:
        """
        Ensure the field order matches the legacy reference CSV schema.

        The CSV writer uses dataclasses.fields() which returns fields in
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

        actual_fields = [f.name for f in fields(DashboardRow)]

        assert actual_fields == expected_fields, (
            "Field order or presence has changed! The CSV writer depends on "
            "the declaration order in the dataclass."
        )

    def test_all_fields_are_strings(self) -> None:
        """
        Verify that all fields are strictly typed as strings.

        Since this dataclass represents a CSV row intended for text serialization,
        all types must be stringly-typed as defined by the model schema.
        """

        for f in fields(DashboardRow):
            assert (
                f.type == "str"
            ), f"Expected field '{f.name}' to be typed as 'str', got '{f.type}'"
