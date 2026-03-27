"""
ECI Initiative Details Extractor
Reads saved HTML response files and extracts structured data to CSV.
"""

from datetime import datetime

from data_pipeline.pipeline_shared.consts import TIMESTAMP_FORMAT
from .extractor import configure, run


def main():
    ts = datetime.now().strftime(TIMESTAMP_FORMAT)
    configure(timestamp_value=ts)
    run()


if __name__ == "__main__":
    main()
