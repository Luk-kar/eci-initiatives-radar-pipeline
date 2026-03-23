"""
Pipeline-wide constants for the ECI data pipeline.

Shared across all pipeline stages:
- scraper (initiatives, responses, responses_followup)
- extractor
- csv_merger
- csv_renamer
"""

from pathlib import Path

# ── Project root ───────────────────────────────────────────────────────────────
PIPELINE_DIR = Path(__file__).parent.parent.absolute()
PROJECT_DIR = PIPELINE_DIR.parent.absolute()

# ── Top-level output directory ─────────────────────────────────────────────────
DATA_PIPELINE_DIR_NAME = "data_pipeline"
DATA_DIR_NAME = "data"
LOG_DIR_NAME = "logs"
DEBUGGING_DIR_NAME = "debugging"

# ── Paths ──────────────────────────────────────────────────────────────────────

DATA_DIR = PIPELINE_DIR / DATA_DIR_NAME

# ── Scraper output subdirectory modules ────────────────────────────────────────
INITIATIVES_DIR_NAME = "initiatives"
RESPONSES_DIR_NAME = "responses"
RESPONSES_FOLLOWUP_DIR_NAME = "responses_followup_website"

# ── Scraper output subdirectory names ──────────────────────────────────────────
# Used by scraper to write, and by extractor/merger/renamer to read.
LISTINGS_DIR_NAME = "listings"
RESPONSES_DIR_NAME = "responses"
RESPONSES_FOLLOWUP_DIR_NAME = "responses_followup"

# ── HTML page filename pattern ─────────────────────────────────────────────────
# Produced by scraper, consumed by extractor.
# Example: 2023_000009_en.html
# {number} includes the language slug (e.g. "000009_en")
INITIATIVE_PAGE_FILENAME_PATTERN = "{year}_{number}.html"

# ── Extractor CSV output filename patterns ─────────────────────────────────────
# Produced by extractor, consumed by merger and renamer.
ECI_INITIATIVES_CSV_PATTERN = "eci_initiatives_{timestamp}.csv"
ECI_RESPONSES_CSV_PATTERN = "eci_responses_{timestamp}.csv"
ECI_RESPONSES_FOLLOWUP_CSV_PATTERN = "eci_responses_followup_{timestamp}.csv"

# ── Merger CSV output filename pattern ─────────────────────────────────────────
# Produced by merger, consumed by renamer.
ECI_MERGER_CSV_PATTERN = "eci_merger_responses_and_followup_{timestamp}.csv"

# ── Renaming CSV files' fields or columns when needed ──────────────────────────
ECI_DASHBOARD_CSV_PATTERN = "eci_dashboard_{timestamp}.csv"

# ── Log filename patterns ──────────────────────────────────────────────────────
LOG_SCRAPER_INITIATIVES_PATTERN = "scraper_initiatives_{timestamp}.log"
LOG_SCRAPER_RESPONSES_PATTERN = "scraper_responses_{timestamp}.log"
LOG_SCRAPER_RESPONSES_FOLLOWUP_PATTERN = "scraper_responses_followup_{timestamp}.log"
LOG_EXTRACTOR_INITIATIVES_PATTERN = "extractor_initiatives_{timestamp}.log"
LOG_EXTRACTOR_RESPONSES_PATTERN = "extractor_responses_{timestamp}.log"
LOG_EXTRACTOR_RESPONSES_FOLLOWUP_PATTERN = (
    "extractor_responses_followup_{timestamp}.log"
)
LOG_MERGER_PATTERN = "merger_responses_and_followup_{timestamp}.log"
LOG_DASHBOARD_PATTERN = "dashboard_{timestamp}.log"


TIMESTAMP_FORMAT = "%Y-%m-%d_%H-%M-%S"
