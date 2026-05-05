import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from data_pipeline.pipeline_shared.consts import (
    DATA_DIR,
    INITIATIVES_DIR_NAME,
    ECI_DASHBOARD_CSV_PATTERN,
    FilePatterns,
)
from data_pipeline.pipeline_shared.locate_run_dir import find_newest_scraped_data_dir

_expected_filename_regex = (
    "^"
    + ECI_DASHBOARD_CSV_PATTERN.format(
        timestamp=f"({FilePatterns.TIMESTAMP_DIR_PATTERN})"
    ).replace(".", r"\.")
    + "$"
)
_TIMESTAMP_RE = re.compile(_expected_filename_regex)


def find_latest_csv() -> tuple[Path, str]:
    """Return the path and date string of the most recent dashboard CSV file
    from the newest valid timestamped run directory.

    Returns:
        A ``(path, date_str)`` tuple where ``date_str`` is ``YYYY-MM-DD``.
    """
    run_dir = find_newest_scraped_data_dir(DATA_DIR, INITIATIVES_DIR_NAME)

    glob_pattern = ECI_DASHBOARD_CSV_PATTERN.format(timestamp="*")
    candidates = sorted(run_dir.glob(glob_pattern), reverse=True)

    if not candidates:
        raise FileNotFoundError(
            f"No '{glob_pattern}' files found in run directory: {run_dir}"
        )

    for csv_path in candidates:
        match = _TIMESTAMP_RE.fullmatch(csv_path.name)
        if not match:
            continue

        try:
            pd.read_csv(csv_path, nrows=1)
        except Exception as exc:
            raise ValueError(
                f"CSV file appears corrupted and cannot be read: {csv_path}"
            ) from exc

        full_timestamp = match.group(1)
        return csv_path, full_timestamp[:10]

    raise ValueError(
        f"No files matching the pattern found in: {run_dir}. "
        f"Expected pattern: {ECI_DASHBOARD_CSV_PATTERN.format(timestamp='YYYY-MM-DD_HH-MM-SS')}"
    )
