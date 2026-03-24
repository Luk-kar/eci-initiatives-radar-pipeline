"""
Shared constants and configuration for ECI data extractors.
"""

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
