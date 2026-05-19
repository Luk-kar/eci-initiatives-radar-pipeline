class RateLimitError(Exception):
    """Raised when the scraper is blocked by rate limiting."""

    pass


class EmptyListingsError(RuntimeError):
    """
    Parsed listing pages yielded 0 entries
    """


class EmptyDownloadsError(RuntimeError):
    """Raised when no response HTML pages were successfully downloaded.

    Unlike EmptyListingsError (which fires on a blank pagination page),
    this fires after all download attempts for every known response URL
    have been exhausted — meaning the directory would be empty
    and the extractor would find nothing to parse.
    """
