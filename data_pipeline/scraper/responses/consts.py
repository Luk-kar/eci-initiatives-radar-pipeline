"""
Constants and configuration for the Commission responses scraper.

Module-specific settings for scraping Commission response pages.
Common settings are imported from scraper_shared.consts.

Note on Fine-Tuning:
    The timing configurations (WAIT_BETWEEN_DOWNLOADS, RETRY_WAIT_BASE) and retry
    limits (DEFAULT_MAX_RETRIES) can be adjusted based on:
    - Server load and response times
    - Rate limiting policies of the target website
    - Network conditions and infrastructure changes

    If you experience frequent rate limiting or timeouts, consider increasing
    wait times and retry intervals. For faster, more stable servers, you may
    reduce these values to speed up scraping.
"""

from ..scraper_shared.consts import (
    BASE_URL,
    PIPELINE_DIR,
    DATA_DIR_NAME,
    LOG_DIR_NAME,
    CHROME_OPTIONS,
    WAIT_DYNAMIC_CONTENT,
    WEBDRIVER_TIMEOUT_DEFAULT,
    WEBDRIVER_TIMEOUT_CONTENT,
    MIN_HTML_LENGTH,
    RATE_LIMIT_INDICATORS,
    DEBUGGING_DIR_NAME,
    DEFAULT_MAX_RETRIES,
    INITIATIVE_PAGE_FILENAME_PATTERN,
)

# Module-specific Directory Names
RESPONSES_DIR_NAME = "responses"
INITIATIVE_PAGES_DIR_NAME = "initiatives"

# CSV Configuration
CSV_FILENAME = "responses_list.csv"
CSV_FIELDNAMES = [
    "url_response",
    "registration_number",
    "title",
    "datetime",
]

# Module-specific Timing Configuration (in seconds)
# Fine-tune these based on server response times and rate limiting behavior
WAIT_BETWEEN_DOWNLOADS = (1.5, 2.5)  # Delay between downloading response pages
RETRY_WAIT_BASE = (2.0, 2.5)  # Base time for retry exponential backoff
