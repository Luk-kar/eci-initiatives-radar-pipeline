"""Shared error types for ECI data extractors."""

from __future__ import annotations

from pathlib import Path
from typing import Optional


class HTMLParseError(Exception):
    """Raised when an HTML initiative file cannot be parsed as a whole."""


class FieldValueError(ValueError):
    """Raised when a field extractor encounters an invalid or unexpected value.

    Subclasses :class:`ValueError` so that existing ``except ValueError``
    guards in the parser layer remain fully compatible.

    Attributes:
        field:  Canonical name of the failed field — matches the
                corresponding ``ECIInitiativeDetailsRecord`` attribute name
                (e.g. ``"registration_number"``, ``"title"``).
        value:  The raw fragment, filename, or extracted text that triggered
                the error.  ``None`` when nothing could be found at all.
        source: Stringified path or filename of the HTML file being processed,
                or ``None`` when the error originates outside a file context.

    Examples:
        >>> raise FieldValueError("registration_number", value="bad_name.html",
        ...                        source="2023/bad_name.html")
        FieldValueError: Invalid value for field 'registration_number':
            got 'bad_name.html' (source: 2023/bad_name.html)

        >>> raise FieldValueError("title", source="2023/2023000009en.html")
        FieldValueError: Invalid value for field 'title'
            (source: 2023/2023000009en.html)
    """

    def __init__(
        self,
        field: str,
        value: object = None,
        source: Optional[str | Path] = None,
        message: Optional[str] = None,
    ) -> None:

        self.field = field
        self.value = value
        self.source = str(source) if source is not None else None

        if message is None:
            message = self._build_message(self.field, self.value, self.source)

        super().__init__(message)

    def _build_message(field: str, value: object, source: Optional[str]) -> str:

        msg = f"Invalid value for field {field!r}"

        if value is not None:
            msg += f": got {value!r}"
        if source:
            msg += f" (source: {source})"

        return msg
