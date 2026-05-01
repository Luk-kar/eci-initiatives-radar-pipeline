from __future__ import annotations

import pytest

from data_pipeline.merger_csv.responses_followup_legislation import collect


class TestIndexByRegistration:

    def test_index_by_registration_creates_lookup(self, responses_rows):

        actual = collect.index_by_registration(responses_rows)

        assert set(actual.keys()) == {"2012/000001", "2012/000002"}
        assert actual["2012/000001"]["commission_answer"] == (
            "['Commission answer 1', 'Commission answer 2']"
        )

    def test_index_by_registration_raises_for_missing_registration_number(self):

        rows = [
            {
                "registration_number": "",
                "commission_answer": "['Answer 1']",
            }
        ]

        with pytest.raises(ValueError, match="missing required column"):
            collect.index_by_registration(rows)


class TestValidateFollowupRegistrationNumbers:

    def test_validate_followup_registration_numbers_accepts_matching_rows(
        self,
        responses_rows,
        followup_rows,
    ):
        responses_index = collect.index_by_registration(responses_rows)

        collect.validate_followup_registration_numbers(followup_rows, responses_index)

    def test_validate_followup_registration_numbers_raises_for_unknown_registration(
        self,
        responses_rows,
    ):
        responses_index = collect.index_by_registration(responses_rows)
        unknown_followup_rows = [
            {
                "registration_number": "2099/999999",
                "followup_events": "['Unknown follow-up']",
            }
        ]

        with pytest.raises(ValueError, match="not found in eci_responses"):
            collect.validate_followup_registration_numbers(
                unknown_followup_rows,
                responses_index,
            )


class TestCollectSourceRows:

    def test_collect_source_rows_resolves_validates_and_loads_files(
        self, monkeypatch, tmp_path
    ):
        """
        Verify that source collection resolves the expected input files, validates them,
        and loads both response and follow-up rows.
        """

        responses_path = tmp_path / "eci_responses_2026-04-24_10-00-00.csv"
        followup_path = tmp_path / "eci_responses_followup_2026-04-24_10-00-00.csv"

        calls: list[tuple[str, object]] = []

        def fake_find_latest_csv(data_dir, glob_pattern):

            calls.append(("find_latest_csv", glob_pattern))
            if "followup" in glob_pattern:
                return followup_path
            return responses_path

        def fake_validate_csv_exists(path):

            calls.append(("validate_csv_exists", path.name))

        def fake_load_csv(path):

            calls.append(("load_csv", path.name))
            if path == responses_path:
                return [
                    {
                        "registration_number": "2012/000001",
                        "commission_answer": "['Answer 1']",
                    }
                ]
            return [
                {
                    "registration_number": "2012/000001",
                    "followup_events": "['Follow-up 1']",
                }
            ]

        monkeypatch.setattr(collect, "find_latest_csv", fake_find_latest_csv)
        monkeypatch.setattr(collect, "validate_csv_exists", fake_validate_csv_exists)
        monkeypatch.setattr(collect, "load_csv", fake_load_csv)

        responses_rows, followup_rows = collect.collect_source_rows(tmp_path)

        assert responses_rows == [
            {
                "registration_number": "2012/000001",
                "commission_answer": "['Answer 1']",
            }
        ]
        assert followup_rows == [
            {
                "registration_number": "2012/000001",
                "followup_events": "['Follow-up 1']",
            }
        ]
        assert calls == [
            ("find_latest_csv", collect.RESPONSES_GLOB),
            ("find_latest_csv", collect.FOLLOWUP_GLOB),
            ("validate_csv_exists", responses_path.name),
            ("validate_csv_exists", followup_path.name),
            ("load_csv", responses_path.name),
            ("load_csv", followup_path.name),
        ]
