"""
Shared constants and configuration for ECI data extractors.
"""

# ============================================================================
# File Patterns and Naming
# ============================================================================


class FilePatterns:
    """Common file naming patterns and regex for matching files."""

    # HTML file patterns
    HTML_FILE_PATTERN = "*.html"
    HTML_FILE_GLOB_PATTERN = "**/*.html"
    HTML_FILE_EXTENSION = ".html"

    # HTML filename regex for extracting registration number
    # Matches: YYYY_NNNNNN_en.html (e.g., 2019_000007_en.html)
    FILENAME_REGEX = r"(\d{4})_(\d{6})_en\.html"
    HTML_FILENAME_PATTERN = r"(\d{4})_(\d{6})_([a-z]{2})\.html"  # More flexible version

    # Timestamp directory pattern for finding scraper session directories
    # Matches: YYYY-MM-DD_HH-MM-SS (e.g., 2026-02-05_18-30-45)
    TIMESTAMP_DIR_PATTERN = r"\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}"


# ============================================================================
# URL Configuration
# ============================================================================


class URLConfig:
    """Base URLs and URL templates for EU Citizens' Initiative website."""

    BASE_URL = "https://citizens-initiative.europa.eu"

    # URL template for initiative details page
    INITIATIVE_DETAILS_URL_TEMPLATE = (
        "{base_url}/initiatives/details/{year}/{number}_en"
    )


# ============================================================================
# Registration Number Format
# ============================================================================


class RegistrationNumberFormat:
    """Standard format for ECI registration numbers."""

    # Format: YYYY/NNNNNN (e.g., 2019/000007)
    SEPARATOR = "/"
    FORMAT_TEMPLATE = "{year}{separator}{number}"

    # Regex pattern to match registration numbers
    PATTERN = r"(\d{4})/(\d{6})"


# ============================================================================
# Content Extraction Limits
# ============================================================================


class ContentLimits:
    """Character limits for extracted content fields."""

    # Maximum characters for objective/description fields
    OBJECTIVE_MAX_LENGTH = 1100
