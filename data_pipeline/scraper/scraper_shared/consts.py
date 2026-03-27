"""
Shared constants and configuration for all ECI scrapers.

Contains browser settings, validation rules, rate limiting detection,
and other configuration values common to all scraper modules:
- initiatives
- responses
- responses_followup
"""

from ...pipeline_shared.consts import (  # data_pipeline
    PIPELINE_DIR,
    INITIATIVES_DIR_NAME,
    LISTINGS_DIR_NAME,
    INITIATIVE_PAGE_FILENAME_PATTERN,
    LOG_DIR_NAME,
    DATA_DIR_NAME,
    DEBUGGING_DIR_NAME,
)

# Shared browser configuration
CHROME_OPTIONS = [
    "--headless",
    "--no-sandbox",
    "--disable-dev-shm-usage",
]

# Shared timing / waits (used or re‑exported by per‑scraper consts)
WAIT_DYNAMIC_CONTENT = (1.5, 1.9)
WEBDRIVER_TIMEOUT_DEFAULT = 15
WEBDRIVER_TIMEOUT_CONTENT = 20
DEFAULT_MAX_RETRIES = 5

# Shared HTML validation
MIN_HTML_LENGTH = 10_000  # example value in your codebase
RATE_LIMIT_INDICATORS = [
    "429 - Too Many Requests",
    "Too many requests",
    "temporarily unavailable",
    "Rate limiting detected",
]

# Shared base URL
BASE_URL = "https://citizens-initiative.europa.eu"
