"""Render all dashboard partials from ECI data and write them to ``page_to_export/partials/``."""

# Python
import re
import sys
from pathlib import Path

# Third
import pandas as pd

# Ensure the project root is on sys.path regardless of the working directory
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# local
from page_creator.partials.charts import (
    generate_chart_outcomes,
    generate_chart_signatures_cohorts,
    generate_chart_ecis_year,
    generate_chart_signatures_map,
    generate_chart_top_10_signatures,
    generate_chart_bubble_finance_plot,
)
from page_creator.partials.counters import generate_kpi_row
from page_creator.partials.lists import (
    generate_collection_ongoing,
    generate_got_response,
    generate_law_passed,
    generate_reached_signatures,
    generate_total_initiatives,
    generate_awaiting_response,
    generate_collection_unsuccessful,
    generate_commission_engaged,
    generate_rejected_legislation,
    generate_withdrawn,
)
from page_creator.partials.date_stamp.last_data_update import generate_last_data_update

_TIMESTAMP_RE = re.compile(r"^initiatives_(\d{4}-\d{2}-\d{2})_\d{2}-\d{2}-\d{2}\.csv$")


def _find_latest_csv(data_dir: Path) -> tuple[Path, str]:
    """Return the path and date string of the most recent ``initiatives_*.csv`` file.

    Args:
        data_dir: Directory to search for CSV files.

    Returns:
        A ``(path, date_str)`` tuple where ``date_str`` is ``YYYY-MM-DD``.

    Raises:
        FileNotFoundError: If ``data_dir`` does not exist.
        FileNotFoundError: If no matching ``initiatives_*.csv`` files are found.
        ValueError:        If the winning filename has a malformed timestamp.
        ValueError:        If the CSV file cannot be parsed (empty or corrupted).
    """
    if not data_dir.exists():
        raise FileNotFoundError(f"Data directory not found: {data_dir}")

    candidates = sorted(data_dir.glob("initiatives_*.csv"), reverse=True)

    if not candidates:
        raise FileNotFoundError(f"No 'initiatives_*.csv' files found in: {data_dir}")

    for csv_path in candidates:
        match = _TIMESTAMP_RE.fullmatch(csv_path.name)
        if not match:
            continue

        # Validate the file is readable and non-empty
        try:
            pd.read_csv(csv_path, nrows=1)
        except Exception as exc:
            raise ValueError(
                f"CSV file appears corrupted and cannot be read: {csv_path}"
            ) from exc

        return csv_path, match.group(1)

    raise ValueError(
        f"No 'initiatives_*.csv' files with a valid timestamp found in: {data_dir}. "
        "Expected format: initiatives_YYYY-MM-DD_HH-MM-SS.csv"
    )


DATA_DIR = Path(__file__).parent / "data"
CSV_PATH, DATA_DATE = _find_latest_csv(DATA_DIR)
PARTIALS_DIR = Path(__file__).parent / "partials"
OUT_DIR = Path(__file__).parent.parent / "page_to_export" / "partials"

GENERATED_JS = (
    Path(__file__).parent.parent
    / "page_to_export"
    / "script"
    / "elements"
    / "generated.js"
)


_PREFIX_MAP: dict[str, str] = {
    "counters": "",
    "lists": "list",
    "charts": "chart",
    "date_stamp": "",
}


_EXCLUDE = frozenset({"__init__.py", "helpers.py", "utils.py"})

_GENERATORS = [
    generate_kpi_row,
    generate_collection_ongoing,
    generate_chart_outcomes,
    generate_chart_signatures_cohorts,
    generate_chart_ecis_year,
    generate_chart_signatures_map,
    generate_chart_top_10_signatures,
    generate_chart_bubble_finance_plot,
    generate_got_response,
    generate_law_passed,
    generate_reached_signatures,
    generate_total_initiatives,
    generate_awaiting_response,
    generate_collection_unsuccessful,
    generate_commission_engaged,
    generate_rejected_legislation,
    generate_withdrawn,
]

_PATTERN = re.compile(r"^generate_(.+)$")


def _fn_to_key(fn) -> str:
    """Derive an HTML filename from a generator function using its module path.

    The subdir (last component of fn.__module__) is resolved against _PREFIX_MAP
    to determine the filename prefix. Any leading '{prefix}_' embedded in the
    function name is stripped to avoid duplication.

    Examples:
        generate_chart_outcomes    (charts/)   → chart_outcomes.html
        generate_collection_ongoing    (lists/)    → list_collection_ongoing.html
        generate_kpi_row           (counters/) → kpi_row.html
    """
    subdir = fn.__module__.split(".")[-2]
    if subdir not in _PREFIX_MAP:
        raise ValueError(
            f"Function '{fn.__name__}' lives in module '{fn.__module__}'; "
            f"subdir '{subdir}' is not registered in _PREFIX_MAP "
            f"(known subdirs: {list(_PREFIX_MAP)})."
        )
    prefix = _PREFIX_MAP[subdir]

    match = _PATTERN.fullmatch(fn.__name__)
    if not match:
        raise ValueError(
            f"Generator '{fn.__name__}' does not follow the required "
            "'generate_{element_name}' naming pattern."
        )
    raw = match.group(1)

    # Strip the prefix segment already embedded in the function name
    # e.g. 'chart_outcomes' with prefix 'chart' → 'outcomes'
    # but 'collection_ongoing' with prefix 'list'  → 'collection_ongoing' (no match, keep as-is)
    element = raw.removeprefix(f"{prefix}_") if prefix else raw

    return f"{prefix}_{element}.html" if prefix else f"{element}.html"


def _discover_slot_map() -> dict[str, str]:
    slot_map: dict[str, str] = {}
    for subdir, prefix in _PREFIX_MAP.items():
        for py_file in sorted((PARTIALS_DIR / subdir).glob("*.py")):
            if py_file.name in _EXCLUDE:
                continue
            stem = py_file.stem
            stem_dashes = stem.replace("_", "-")
            html_name = f"{prefix}_{stem}.html" if prefix else f"{stem}.html"
            slot_id = (
                f"{prefix}-{stem_dashes}-slot" if prefix else f"{stem_dashes}-slot"
            )
            slot_map[html_name] = slot_id
    return slot_map


def _build_generated_js(slot_map: dict[str, str]) -> str:
    entries = "\n".join(
        f'    ["partials/{filename}", "{slot_id}"],'
        for filename, slot_id in slot_map.items()
    )
    return (
        "// AUTO-GENERATED by page_creator/generate_charts.py — do not edit manually.\n"
        f"const GENERATED_PARTIALS = [\n{entries}\n];\n"
    )


def generate_partials_a_map_html_name_function(df):
    """
    Build a mapping of HTML filenames to rendered HTML strings for all registered generators.
    """

    return {_fn_to_key(fn): fn(df) for fn in _GENERATORS}


def main() -> None:
    """Load the CSV, render all partials, and write HTML files and the JS slot map."""

    df = pd.read_csv(CSV_PATH)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    GENERATED_JS.parent.mkdir(parents=True, exist_ok=True)

    slot_map = _discover_slot_map()

    partials: dict[str, str] = generate_partials_a_map_html_name_function(df)
    partials["last_data_update.html"] = generate_last_data_update(DATA_DATE)

    for filename, html in partials.items():
        path = OUT_DIR / filename
        path.write_text(html, encoding="utf-8")
        print(f"  wrote {path}  ({path.stat().st_size:,} bytes)")

    GENERATED_JS.write_text(_build_generated_js(slot_map), encoding="utf-8")
    print(f"  wrote {GENERATED_JS}  ({GENERATED_JS.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
