"""
Shared filesystem and CSV utilities for scrapers.
"""

import csv
import os
from typing import Iterable, List, Dict


def ensure_dirs(*paths: str) -> None:
    """Create all given directories if they do not exist."""
    for path in paths:
        os.makedirs(path, exist_ok=True)


def build_timestamped_run_dirs(
    pipeline_dir: str,
    data_dir_name: str,
    timestamp: str,
    *subdirs: str,
) -> dict[str, str]:
    """Build and return a dict of timestamped directories.

    Args:
        pipeline_dir: Project root or base script directory.
        data_dir_name: Name of the shared data folder (e.g. "data").
        timestamp: Timestamp string (YYYY-MM-DD_HH-MM-SS).
        subdirs: Subdirectory names to create under the timestamp dir.

    Returns:
        Mapping of subdir name → full path.
    """
    base = os.path.join(pipeline_dir, data_dir_name, timestamp)
    paths: dict[str, str] = {}
    for name in subdirs:
        full = os.path.join(base, name)
        paths[name] = full
    return paths


def write_csv(
    file_path: str,
    fieldnames: List[str],
    rows: Iterable[Dict[str, str]],
) -> None:
    """Write an iterable of dict rows to CSV with the given fieldnames.

    Args:
        file_path: Full path to the CSV file.
        fieldnames: CSV column names.
        rows: Iterable of dictionaries matching the fieldnames.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
