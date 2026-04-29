"""
registration_year
-----------------
Extract the registration year from the initiative's registration number.
"""

import re

# Expected pattern: 4 digits, a single slash, followed by 1 or more digits (e.g., "2012/000001")
_PATTERN = re.compile(r"^\d{4}/\d+$")


def extract(registration_number: str | None) -> str:
    """Return the registration year parsed from the registration number.

    Args:
        registration_number: The raw registration number from the initiative.

    Returns:
        The extracted 4-digit year as a string.

    Raises:
        ValueError: If the registration number is empty, missing a '/',
                    has multiple '/', or fails to match the YYYY/NNNNNN pattern.
    """

    if not registration_number or not registration_number.strip():
        raise ValueError(
            f"Registration number cannot be empty or None. Got: {registration_number!r}"
        )

    if registration_number.count("/") == 0:
        raise ValueError(
            f"Registration number must contain a '/'. Got: {registration_number!r}"
        )

    if registration_number.count("/") > 1:
        raise ValueError(
            f"Registration number must contain exactly one '/'. Got: {registration_number!r}"
        )

    if not _PATTERN.match(registration_number):
        raise ValueError(
            f"Registration number does not follow the expected pattern (YYYY/NNNNNN). "
            f"Got: {registration_number!r}"
        )

    return registration_number.split("/")[0]
