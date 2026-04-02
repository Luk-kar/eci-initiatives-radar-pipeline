"""
ECI Responses Extractor — public API.

Entry points:
    configure(timestamp) → output CSV filename
    run(output_csv_name, timestamp) → orchestrates all extraction steps
"""

import logging
from pathlib import Path

from data_pipeline.pipeline_shared.consts import ECI_RESPONSES_CSV_PATTERN

from .session import setup
from .collect import collect_html_files
from .load_metadata import load_metadata
from .parse import parse_html_files
from .assemble import build_records
from .write import write_csv


logger = logging.getLogger(__name__)


def configure(timestamp: str) -> str:
    """Return the output CSV filename for this run. Must be called before run()."""
    return ECI_RESPONSES_CSV_PATTERN.format(timestamp=timestamp)


def run(output_csv_name: str, timestamp: str) -> None:
    """Main execution function — orchestrates the four extraction steps."""
    global logger

    if timestamp is None or output_csv_name is None:
        raise RuntimeError("Extractor is not configured. Call configure() first.")

    html_dir, output_csv, initiatives_csv, step_logger = setup(
        timestamp, output_csv_name
    )
    logger = step_logger

    html_files = collect_html_files(html_dir)
    metadata = load_metadata(initiatives_csv, html_files)
    parsed_data = parse_html_files(html_files)
    records = build_records(metadata, parsed_data)

    write_csv(records, output_csv)
    logger.info("Done. %d records written to %s", len(records), output_csv)
