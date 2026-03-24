from pathlib import Path
import re

from ...consts import RegistrationNumberFormat

from data_pipeline.pipeline_shared.consts import FilePatterns
from ....extractor_shared.errors import FieldValueError


def extract_registration_number(filename: str) -> str:
    """Extract registration number from filename. Mandatory — raises if unresolvable."""

    for pattern in (FilePatterns.FILENAME_REGEX, FilePatterns.HTML_FILENAME_PATTERN):

        match = re.match(pattern, filename)

        if match:

            year, number = match.groups()
            if year and number:
                return RegistrationNumberFormat.FORMAT_TEMPLATE.format(
                    year=year,
                    separator=RegistrationNumberFormat.SEPARATOR,
                    number=number,
                )

    raise FieldValueError(
        field="registration_number",
        value=filename,
        source=filename,
        message=(
            f"Cannot extract registration number from filename {filename!r}. "
            f"Expected pattern matching {FilePatterns.FILENAME_REGEX!r} "
            f"or {FilePatterns.HTML_FILENAME_PATTERN!r}."
        ),
    )
