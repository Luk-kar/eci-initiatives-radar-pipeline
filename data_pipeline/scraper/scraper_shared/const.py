"""
Shared constants and configuration for all ECI scrapers.

Contains browser settings, validation rules, rate limiting detection,
and other configuration values common to all scraper modules:
- initiatives
- responses
- responses_followup_website
"""

from pathlib import Path

# Script / project root
SCRIPT_DIR = Path(__file__).parent.parent.parent.parent.absolute()

# Shared directory names
DATA_DIR_NAME = "data"
LOG_DIR_NAME = "logs"

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
