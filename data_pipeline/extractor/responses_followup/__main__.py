"""
ECI Responses Follow-up Extractor
Reads saved HTML follow-up website files and extracts structured data to CSV.
"""

from datetime import datetime

from data_pipeline.pipeline_shared.consts import TIMESTAMP_FORMAT
from .extractor import configure, run


def main():
    timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
    output_csv_name = configure(timestamp=timestamp)
    run(output_csv_name, timestamp)


if __name__ == "__main__":
    main()
