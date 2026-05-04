"""Tests for build_initiative_row, build_sig_threshold_row, and related helpers."""

import pandas as pd
import pytest

from page_creator.partials.lists.utils.rows import (
    build_initiative_row,
    build_sig_threshold_row,
    build_sig_threshold_rows,
    build_response_row,
    build_response_rows,
    build_card_title,
    generate_response_card,
    generate_sig_threshold_card,
    HEADERS_WITH_SIGNATURES,
)

# ── Shared fixtures ───────────────────────────────────────────────────────────


@pytest.fixture
def base_row():
    return pd.Series(
        {
            "title": "Stop Plastic Pollution",
            "initiative_url": "https://eci.ec.europa.eu/001",
            "registration_date": "1 Jan 2020",
            "objective": "Reduce single-use plastic across the EU.",
            "signatures_collected": 1_200_000,
            "signatures_countries_threshold_met_count": 9,
        }
    )


@pytest.fixture
def response_row():
    return pd.Series(
        {
            "title": "Save the Bees",
            "initiative_url": "https://eci.ec.europa.eu/002",
            "registration_date": "5 Mar 2019",
            "objective": "Protect pollinators across the EU.",
            "commission_answer": "The Commission acknowledges the initiative.",
        }
    )


@pytest.fixture
def response_df():
    return pd.DataFrame(
        {
            "title": ["Save the Bees", "Ban Glyphosate"],
            "initiative_url": [
                "https://eci.ec.europa.eu/002",
                "https://eci.ec.europa.eu/003",
            ],
            "registration_date": ["05/03/2019", "10/06/2017"],
            "objective": ["Protect pollinators.", "Remove glyphosate from EU."],
            "commission_answer": ["Response A.", "Response B."],
            "signatures_collected": [1_100_000, 1_300_000],
            "signatures_countries_threshold_met_count": [11, 10],
        }
    )


# ── Existing tests (kept as-is) ───────────────────────────────────────────────


class TestBuildInitiativeRow:
    def test_contains_title(self, base_row):
        result = build_initiative_row(base_row)
        assert "Stop Plastic Pollution" in result

    def test_contains_url_as_href(self, base_row):
        result = build_initiative_row(base_row)
        assert 'href="https://eci.ec.europa.eu/001"' in result

    def test_contains_registration_date(self, base_row):
        result = build_initiative_row(base_row)
        assert "1 Jan 2020" in result

    def test_contains_truncated_objective(self, base_row):
        result = build_initiative_row(base_row)
        assert "Reduce single-use plastic" in result

    def test_opens_in_new_tab(self, base_row):
        result = build_initiative_row(base_row)
        assert 'target="_blank"' in result

    def test_extra_cells_appended(self, base_row):
        result = build_initiative_row(base_row, extra_cells="<td>Extra</td>")
        assert "<td>Extra</td>" in result

    def test_no_extra_cells_by_default(self, base_row):
        result = build_initiative_row(base_row)
        assert result.count("<td>") == 3  # title, date, objective


# ── New tests ─────────────────────────────────────────────────────────────────


class TestBuildResponseRow:
    def test_contains_title(self, response_row):
        result = build_response_row(response_row)
        assert "Save the Bees" in result

    def test_contains_truncated_response(self, response_row):
        result = build_response_row(response_row)
        assert "The Commission acknowledges" in result

    def test_response_in_td(self, response_row):
        result = build_response_row(response_row)
        assert "<td>The Commission acknowledges the initiative.</td>" in result

    def test_long_response_is_truncated(self, response_row):
        response_row = response_row.copy()
        response_row["commission_answer"] = "A" * 300
        result = build_response_row(response_row)
        assert "A" * 300 not in result
        assert "A" * 100 in result  # truncated but not empty

    def test_contains_url_as_href(self, response_row):
        result = build_response_row(response_row)
        assert 'href="https://eci.ec.europa.eu/002"' in result

    def test_is_table_row(self, response_row):
        result = build_response_row(response_row)
        assert "<tr>" in result and "</tr>" in result


class TestBuildResponseRows:
    def test_returns_all_rows(self, response_df):
        result = build_response_rows(response_df)
        assert "Save the Bees" in result
        assert "Ban Glyphosate" in result

    def test_empty_dataframe_returns_empty_string(self):
        empty_df = pd.DataFrame(
            columns=[
                "title",
                "initiative_url",
                "registration_date",
                "objective",
                "commission_answer",
            ]
        )
        assert build_response_rows(empty_df) == ""

    def test_single_row_returns_one_tr(self, response_df):
        result = build_response_rows(response_df.iloc[:1])
        assert result.count("<tr>") == 1

    def test_two_rows_returns_two_trs(self, response_df):
        result = build_response_rows(response_df)
        assert result.count("<tr>") == 2


class TestBuildCardTitle:
    def test_contains_emoji(self):
        result = build_card_title("🏛️", "Commission Engaged", 4, "#9CCC65")
        assert "🏛️" in result

    def test_contains_label(self):
        result = build_card_title("🏛️", "Commission Engaged", 4, "#9CCC65")
        assert "Commission Engaged" in result

    def test_contains_count(self):
        result = build_card_title("🏛️", "Commission Engaged", 4, "#9CCC65")
        assert ">4<" in result

    def test_contains_color(self):
        result = build_card_title("🏛️", "Commission Engaged", 4, "#9CCC65")
        assert "color:#9CCC65" in result

    def test_is_h3(self):
        result = build_card_title("✅", "Law Passed", 2, "#3CA371")
        assert result.startswith('<h3 class="card__title">')
        assert result.endswith("</h3>")

    def test_zero_count(self):
        result = build_card_title("❌", "Rejected Legislation", 0, "#F44336")
        assert ">0<" in result

    def test_count_in_span(self):
        result = build_card_title("⌛", "Awaiting Response", 3, "#9E9E9E")
        assert '<span class="card__count"' in result


class TestGenerateResponseCard:
    def test_returns_string(self, response_df):
        title = build_card_title("📬", "Got EU Response", len(response_df), "#006064")
        result = generate_response_card(
            response_df,
            title,
            ["Initiative", "Registration", "Objective", "Response"],
            "#006064",
            "No response yet.",
        )
        assert isinstance(result, str)

    def test_contains_title(self, response_df):
        title = build_card_title("📬", "Got EU Response", len(response_df), "#006064")
        result = generate_response_card(
            response_df,
            title,
            ["Initiative", "Registration", "Objective", "Response"],
            "#006064",
            "No response yet.",
        )
        assert "Got EU Response" in result

    def test_empty_df_shows_empty_message(self):
        empty_df = pd.DataFrame(
            columns=[
                "title",
                "initiative_url",
                "registration_date",
                "objective",
                "commission_answer",
            ]
        )
        title = build_card_title("📬", "Got EU Response", 0, "#006064")
        result = generate_response_card(
            empty_df,
            title,
            ["Initiative", "Registration", "Objective", "Response"],
            "#006064",
            "No response yet.",
        )
        assert "No response yet." in result

    def test_empty_df_does_not_render_table(self):
        empty_df = pd.DataFrame(
            columns=[
                "title",
                "initiative_url",
                "registration_date",
                "objective",
                "commission_answer",
            ]
        )
        title = build_card_title("📬", "Got EU Response", 0, "#006064")
        result = generate_response_card(
            empty_df,
            title,
            ["Initiative", "Registration", "Objective", "Response"],
            "#006064",
            "No response yet.",
        )
        assert "<table" not in result

    def test_non_empty_df_renders_table(self, response_df):
        title = build_card_title("📬", "Got EU Response", len(response_df), "#006064")
        result = generate_response_card(
            response_df,
            title,
            ["Initiative", "Registration", "Objective", "Response"],
            "#006064",
            "No response yet.",
        )
        assert "<table" in result


class TestGenerateSigThresholdCard:
    def test_returns_string(self, response_df):
        title = build_card_title(
            "✅", "Reached 1M Signatures", len(response_df), "#527445"
        )
        result = generate_sig_threshold_card(
            response_df, title, "#527445", "None found."
        )
        assert isinstance(result, str)

    def test_contains_title(self, response_df):
        title = build_card_title(
            "✅", "Reached 1M Signatures", len(response_df), "#527445"
        )
        result = generate_sig_threshold_card(
            response_df, title, "#527445", "None found."
        )
        assert "Reached 1M Signatures" in result

    def test_empty_df_shows_empty_message(self):
        empty_df = pd.DataFrame(
            columns=[
                "title",
                "initiative_url",
                "registration_date",
                "objective",
                "signatures_collected",
                "signatures_countries_threshold_met_count",
            ]
        )
        title = build_card_title("✅", "Reached 1M Signatures", 0, "#527445")
        result = generate_sig_threshold_card(empty_df, title, "#527445", "None found.")
        assert "None found." in result

    def test_empty_df_does_not_render_table(self):
        empty_df = pd.DataFrame(
            columns=[
                "title",
                "initiative_url",
                "registration_date",
                "objective",
                "signatures_collected",
                "signatures_countries_threshold_met_count",
            ]
        )
        title = build_card_title("✅", "Reached 1M Signatures", 0, "#527445")
        result = generate_sig_threshold_card(empty_df, title, "#527445", "None found.")
        assert "<table" not in result

    def test_non_empty_df_renders_table(self, response_df):
        title = build_card_title(
            "✅", "Reached 1M Signatures", len(response_df), "#527445"
        )
        result = generate_sig_threshold_card(
            response_df, title, "#527445", "None found."
        )
        assert "<table" in result
