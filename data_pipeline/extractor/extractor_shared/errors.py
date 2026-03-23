"""
Custom exceptions for data pipeline extractor modules.
"""


class HTMLParseError(Exception):
    """Raised when a parse function fails to process an HTML file."""
