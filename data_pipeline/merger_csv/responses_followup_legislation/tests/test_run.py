import logging
from pathlib import Path

from data_pipeline.merger_csv.responses_followup_legislation import run as run_module
from data_pipeline.merger_csv.responses_followup_legislation.extractor import (
    LegislationResult,
)


class TestRun:
    def test_run_coordinates_collection_assembly_and_writing(
        self, monkeypatch, tmp_path: Path
    ):
        """
        Verify that the pipeline step runs source collection, result assembly,
        and output writing in the expected sequence.
        """

        responses_rows = [
            {
                "registration_number": "2012/000001",
                "commission_answer_text": "['Answer 1']",
            }
        ]

        followup_rows = [
            {
                "registration_number": "2012/000001",
                "followup_events": "['Follow-up 1']",
            }
        ]

        assembled_results = [
            LegislationResult(
                registration_number="2012/000001",
                followup_events=["Answer 1", "Follow-up 1"],
                Law_Passed=["Follow-up 1"],
                Is_Law_Passed=True,
                Rejected_Legislation=False,
            )
        ]

        sorted_results = list(reversed(assembled_results))

        output_path = tmp_path / "output.csv"

        calls: list[tuple[str, object]] = []

        def fake_setup():
            calls.append(("setup", None))
            return tmp_path, logging.getLogger("test_run")

        def fake_collect_source_rows(data_dir):
            calls.append(("collect_source_rows", data_dir))
            return responses_rows, followup_rows

        def fake_assemble_results(arg_responses_rows, arg_followup_rows):
            calls.append(("assemble_results", (arg_responses_rows, arg_followup_rows)))
            return assembled_results

        def fake_write_output(data_dir, results):
            calls.append(("write_output", (data_dir, results)))
            return output_path

        def fake_sort_by_registration_number(results):
            calls.append(("sort_by_registration_number", results))
            return sorted_results

        monkeypatch.setattr(run_module, "setup", fake_setup)
        monkeypatch.setattr(run_module, "collect_source_rows", fake_collect_source_rows)
        monkeypatch.setattr(run_module, "assemble_results", fake_assemble_results)
        monkeypatch.setattr(
            run_module,
            "sort_by_registration_number",
            fake_sort_by_registration_number,
        )
        monkeypatch.setattr(run_module, "write_output", fake_write_output)

        actual = run_module.run()

        assert actual == output_path
        assert calls == [
            ("setup", None),
            ("collect_source_rows", tmp_path),
            ("assemble_results", (responses_rows, followup_rows)),
            ("sort_by_registration_number", assembled_results),
            ("write_output", (tmp_path, sorted_results)),
        ]
