# data_pipeline/extractor/responses/__main__.py
#!/usr/bin/env python3
"""
ECI Initiative Details Extractor
Reads saved HTML response files and extracts structured data to CSV.
"""

from datetime import datetime

from data_pipeline.pipeline_shared.consts import TIMESTAMP_FORMAT
from .extractor import ECIResponseExtractor


def main():
    timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
    extractor = ECIResponseExtractor(timestamp=timestamp)
    extractor.run()


if __name__ == "__main__":
    main()
