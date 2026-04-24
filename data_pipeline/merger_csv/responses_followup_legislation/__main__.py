"""
main.py – ECI Legislation Extractor (pipeline step)
====================================================
Reads the two most-recently produced extractor CSVs:

    eci_responses_<timestamp>.csv
    eci_responses_followup_<timestamp>.csv

Joins them on ``registration_number``, feeds the combined text of
``commission_answer_text`` + ``followup_events`` into a spaCy ``Matcher``,
and writes the results to:

    eci_legislation_<timestamp>.csv

placed alongside the source files inside the latest timestamped run directory.

Usage
-----
As a module (preferred – keeps the package importable in tests):

    python -m data_pipeline.merger_csv.responses_followup.main

Or via the pyproject.toml entry-point (after ``pip install -e .``):

    eci-extract-legislation
"""

from __future__ import annotations

import ast
import csv
from dataclasses import fields as dataclass_fields
import logging
import sys
from datetime import datetime
from pathlib import Path

from data_pipeline.pipeline_shared.locate_run_dir import find_newest_scraped_data_dir
from data_pipeline.pipeline_shared.consts import (
    DATA_DIR,
    FILE_ENCODING,
    LOG_DIR_NAME,
    TIMESTAMP_FORMAT,
    FilePatterns,
    LOG_LEGISLATION_PATTERN,
    ECI_RESPONSES_FOLLOWUP_LEGISLATION_PATTERN,
    RESPONSES_FOLLOWUP_DIR_NAME,
    HTML_DOMAIN_EC_FOLLOWUP,
)
from data_pipeline.pipeline_shared.errors import RunDirectoryValidationError
from data_pipeline.pipeline_shared.logger import get_logger

from .extractor import LegislationResult, analyse_row, LegislationResult

# ── Module-level logger (populated after get_logger() is called in main()) ────
logger = logging.getLogger(__name__)

# ── Output CSV ────────────────────────────────────────────────────────────────
_OUTPUT_FIELDNAMES: list[str] = [f.name for f in dataclass_fields(LegislationResult)]

# ── Source-column documentation (not enforced here; used for clarity) ─────────
_RESPONSES_COLS = ("registration_number", "commission_answer_text")
_FOLLOWUP_COLS = ("registration_number", "followup_events")


# ═════════════════════════════════════════════════════════════════════════════
# Directory / file resolution
# ═════════════════════════════════════════════════════════════════════════════


def _find_latest_csv(data_dir: Path, glob: str) -> Path:
    """
    Return the most-recent CSV inside *data_dir* that matches *glob*.

    Because CSV filenames embed an ISO-8601-derived timestamp, lexicographic
    sort is equivalent to chronological sort.

    Args:
        data_dir: Directory to search.
        glob:     Shell glob string, e.g. ``"eci_responses_[0-9]*.csv"``.

    Returns:
        ``Path`` to the matching file with the latest (largest) name.

    Raises:
        ``FileNotFoundError``: when no match is found.
    """

    matches = sorted(data_dir.glob(glob))

    if not matches:
        raise FileNotFoundError(f"No files matching '{glob}' found in '{data_dir}'.")

    latest = matches[-1]
    logger.info("Resolved '%s'  →  %s", glob, latest.name)

    return latest


# ═════════════════════════════════════════════════════════════════════════════
# CSV I/O helpers
# ═════════════════════════════════════════════════════════════════════════════


def _load_csv(path: Path) -> list[dict]:
    """
    Read *path* with the stdlib ``csv.DictReader`` and return all rows.

    Args:
        path: Absolute path to the CSV file.

    Returns:
        ``list[dict]`` where each dict maps column name → cell value (str).
    """

    logger.info("Loading CSV: %s", path)

    with path.open(encoding=FILE_ENCODING, newline="") as fh:
        rows = list(csv.DictReader(fh))

    logger.debug("  → %d rows loaded from '%s'", len(rows), path.name)

    return rows


def _index_by_registration(
    rows: list[dict],
    key: str = "registration_number",
) -> dict[str, dict]:
    """
    Build an O(1)-lookup index from *rows* keyed on *key*.

    Rows that lack the key column are silently skipped with a warning.

    Args:
        rows: Source row list (from ``_load_csv``).
        key:  Column name to use as the dict key.

    Returns:
        ``dict[registration_number, row_dict]``.
    """
    index: dict[str, dict] = {}

    for i, row in enumerate(rows):

        reg = (row.get(key) or "").strip()

        if not reg:
            raise ValueError(
                f"Row {i} is missing required column '{key}'. "
                f"Source CSV is malformed. Row (truncated): {str(row)[:120]}"
            )

        index[reg] = row

    return index


# ═════════════════════════════════════════════════════════════════════════════
# Text joining helper
# ═════════════════════════════════════════════════════════════════════════════


def _merge_text_lists(responses_row: dict, followup_row: dict) -> list[str]:
    """
    Parse ``commission_answer_text`` and ``followup_events`` —
    both stored as Python list literals (e.g. ``"['text one', 'text two']"``) —
    and return a single concatenated list of their string items.

    Each element of the returned list is passed individually to spaCy so that
    per-item legislation flags map back to the original text fragments.

    Args:
        responses_row: Row dict from ``eci_responses_*.csv``.
        followup_row:  Matching row dict from ``eci_responses_followup_*.csv``
                       (may be an empty dict when no follow-up exists).

    Returns:
        Ordered ``list[str]`` of text fragments ready for NLP processing.
    """

    def _parse_list(raw: str, column: str) -> list[str]:
        try:
            parsed = ast.literal_eval(raw)
        except (ValueError, SyntaxError) as exc:
            raise ValueError(
                f"Column '{column}' is not a valid Python literal: {raw!r}"
            ) from exc

        if parsed is None:
            raise ValueError(
                f"Column '{column}' parsed to None – expected a list of strings."
            )

        if not isinstance(parsed, list):
            raise ValueError(
                f"Column '{column}' expected a list, got {type(parsed).__name__}: {raw!r}"
            )

        if not parsed:
            raise ValueError(
                f"Column '{column}' is an empty list – at least one text item is required."
            )

        items = [str(item).strip() for item in parsed]

        if not any(items):
            raise ValueError(
                f"Column '{column}' contains only empty strings: {parsed!r}"
            )

        return items

    # Mandatory – raise if absent or unparseable
    texts_a = _parse_list(
        responses_row["commission_answer_text"], "commission_answer_text"
    )

    # Optional – absent when no follow-up event exists for this initiative
    followup_raw = followup_row.get("followup_events")
    texts_b = _parse_list(followup_raw, "followup_events") if followup_raw else []

    return texts_a + texts_b


# ═════════════════════════════════════════════════════════════════════════════
# Output writer
# ═════════════════════════════════════════════════════════════════════════════


def _write_output(data_dir: Path, results: list[LegislationResult]) -> Path:
    """
    Serialise *results* to a timestamped CSV inside *data_dir*.

    The output filename follows the pattern ``eci_legislation_<timestamp>.csv``
    where ``<timestamp>`` matches ``TIMESTAMP_FORMAT`` (``%Y-%m-%d_%H-%M-%S``).

    ``Law_Passed`` is written as its Python ``list`` repr (e.g.
    ``"['span one', 'span two']"``); downstream consumers should parse with
    ``ast.literal_eval`` when reading.

    Args:
        data_dir: Directory in which to create the output file.
        results:  Ordered list of ``LegislationResult`` instances.

    Returns:
        Absolute ``Path`` to the written CSV.
    """

    timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)

    filename = ECI_RESPONSES_FOLLOWUP_LEGISLATION_PATTERN.format(timestamp=timestamp)
    output_path = data_dir / filename

    logger.info("Writing output CSV: %s", output_path)

    with output_path.open("w", encoding=FILE_ENCODING, newline="") as csv_file:

        writer = csv.DictWriter(csv_file, fieldnames=_OUTPUT_FIELDNAMES)
        writer.writeheader()

        for r in results:

            writer.writerow(
                {
                    "registration_number": r.registration_number,
                    "followup_events": r.followup_events,
                    "Law_Passed": r.Law_Passed,
                    "Is_Law_Passed": r.Is_Law_Passed,
                    "Rejected_Legislation": r.Rejected_Legislation,
                }
            )

    logger.info("Wrote %d row(s) → %s", len(results), output_path)
    return output_path


# ═════════════════════════════════════════════════════════════════════════════
# Core pipeline step
# ═════════════════════════════════════════════════════════════════════════════


def run(data_dir: Path) -> Path:
    """
    Execute the full legislation-extraction pipeline step.

    Steps
    -----
    1. Locate the most-recent ``eci_responses_*.csv`` and
       ``eci_responses_followup_*.csv`` files inside *data_dir*.
    2. Load both CSVs into memory using the stdlib ``csv`` module.
    3. Index follow-up rows by ``registration_number`` for O(1) joins.
    4. Analyse each initiative: merge texts → run regex extraction → collect results.
    5. Write ``eci_legislation_<timestamp>.csv`` and return its path.

    Args:
        data_dir: Resolved timestamped run directory (e.g.
                  ``data_pipeline/data/2026-04-09_15-38-52``).

    Returns:
        ``Path`` to the written output CSV.

    Raises:
        ``FileNotFoundError``: a required source CSV is missing.
        ``ValueError``:        a responses row is missing ``registration_number``.
    """
    # ── 1. Source CSVs ────────────────────────────────────────────────────────
    responses_csv = _find_latest_csv(data_dir, "eci_responses_[0-9]*.csv")
    followup_csv = _find_latest_csv(data_dir, "eci_responses_followup_[0-9]*.csv")

    # ── 2. Load into memory ───────────────────────────────────────────────────
    responses_rows = _load_csv(responses_csv)
    followup_rows = _load_csv(followup_csv)

    # ── 3. Index follow-up rows ───────────────────────────────────────────────
    followup_index = _index_by_registration(followup_rows)

    # ── 4. Analyse each initiative ────────────────────────────────────────────
    results: list[LegislationResult] = []

    for i, row in enumerate(responses_rows):
        reg_num = row["registration_number"].strip()

        if not reg_num:
            raise ValueError(
                f"Responses row {i} has an empty 'registration_number'. "
                f"Source CSV is malformed. Row (truncated): {str(row)[:120]}"
            )

        followup_row = followup_index.get(reg_num, {})
        text_items = _merge_text_lists(row, followup_row)
        result = analyse_row(reg_num, text_items)
        results.append(result)

    logger.info("Regex extraction complete. %d initiative(s) processed.", len(results))

    # ── 5. Write output ───────────────────────────────────────────────────────
    return _write_output(data_dir, results)


# ═════════════════════════════════════════════════════════════════════════════
# CLI entry point
# ═════════════════════════════════════════════════════════════════════════════


def main() -> None:
    """
    CLI entry point.

    Resolves the latest run directory first so the log file lands in
    ``data_pipeline/data/<timestamp>/logs/`` alongside all other pipeline
    logs.  Exit code 1 on any anticipated failure.
    """
    # ── Resolve run directory before logger so the log file path is known ─────
    try:
        data_dir = find_newest_scraped_data_dir(
            DATA_DIR,
            RESPONSES_FOLLOWUP_DIR_NAME,
            HTML_DOMAIN_EC_FOLLOWUP,
        )
    except RunDirectoryValidationError as exc:
        logging.getLogger(__name__).error("Failed to resolve run directory: %s", exc)
        sys.exit(1)

    # ── Bootstrap logger → data/2026-04-09_15-38-52/logs/ ────────────────────
    get_logger(data_dir / LOG_DIR_NAME, LOG_LEGISLATION_PATTERN)

    try:
        output_path = run(data_dir)
        logger.info("[eci-extract-legislation] Done → %s", output_path)
    except (FileNotFoundError, ValueError, OSError) as exc:
        logger.error("Pipeline step failed: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
