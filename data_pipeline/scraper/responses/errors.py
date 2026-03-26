"""
Custom exceptions for the Commission responses scraper.
"""

from ..scraper_shared.exceptions import RateLimitError

__all__ = ["RateLimitError", "MissingDataDirectoryError"]


class MissingDataDirectoryError(FileNotFoundError):
    """
    Raised when the required data directory structure is not found.

    This typically occurs when the responses scraper is run before
    the initiatives scraper has created the timestamp directory.
    """

    def __init__(self, expected_path: str, hint: str | None = None):
        self.expected_path = expected_path
        self.hint = (
            hint
            or "Run the initiatives scraper first to create the timestamp directory."
        )

        message = (
            f"Cannot find required data directory.\n"
            f"Expected: {expected_path}\n"
            f"Hint: {self.hint}"
        )

        super().__init__(message)
