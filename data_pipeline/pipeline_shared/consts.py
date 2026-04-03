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
RESPONSES_FOLLOWUP_DIR_NAME = "responses_followup"

# ── Scraper output subdirectory names ──────────────────────────────────────────
# Used by scraper to write, and by extractor/merger/renamer to read.
LISTINGS_DIR_NAME = "listings"

# ── HTML page filename pattern ─────────────────────────────────────────────────
# Produced by scraper, consumed by extractor.
# Example: 2023_000009_en.html
# {number} includes the language slug (e.g. "000009_en")
INITIATIVE_PAGE_FILENAME_PATTERN = "{year}_{number}.html"

# ============================================================================
# File Patterns and Naming
# ============================================================================


class FilePatterns:
    """Common file naming patterns and regex for matching files."""

    # HTML filename regex for extracting registration number
    # Matches: YYYY_NNNNNN_en.html (e.g., 2019_000007_en.html)
    FILENAME_REGEX = r"(\d{4})_(\d{6})\.html"
    HTML_FILENAME_PATTERN = r"(\d{4})_(\d{6})_([a-z]{2})\.html"  # More flexible version

    # Timestamp directory pattern for finding scraper session directories
    # Matches: YYYY-MM-DD_HH-MM-SS (e.g., 2026-02-05_18-30-45)
    TIMESTAMP_DIR_PATTERN = r"\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}"


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

# Formats
TIMESTAMP_FORMAT = "%Y-%m-%d_%H-%M-%S"
FILE_ENCODING = "utf-8"

# ── HTML content validation tokens ────────────────────────────────────────────
# Used by locate_run_dir to verify that sampled HTML files originate from the
# expected domain before extraction begins.
HTML_DOMAIN_ECI_PORTAL = "citizens-initiative.europa.eu"  # initiatives + responses
HTML_DOMAIN_EC_FOLLOWUP = "ec.europa.eu"  # responses_followup

ECI_RESPONSES_CSV_GLOB: str = "eci_responses_*.csv"
