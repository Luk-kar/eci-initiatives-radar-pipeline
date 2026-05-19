class RateLimitError(Exception):
    """Raised when the scraper is blocked by rate limiting."""

    pass


class EmptyListingsError(RuntimeError):
    """
    Parsed listing pages yielded 0 entries
    """
