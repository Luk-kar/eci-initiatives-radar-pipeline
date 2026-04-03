from ...consts import URLConfig, RegistrationNumberFormat
from ....extractor_shared.errors import FieldValueError


def construct_url(reg_number: str) -> str:
    """Construct English URL from registration number.

    Raises:
        FieldValueError: If ``reg_number`` is empty/None, or does not split
            into exactly year + number on the expected separator.
    """
    if not reg_number:
        raise FieldValueError(
            field="initiative_url",
            value=reg_number,
            message=(
                "Cannot construct URL: registration number is empty or None. "
                f"Expected format: {RegistrationNumberFormat.FORMAT_TEMPLATE!r}."
            ),
        )

    parts = reg_number.split(RegistrationNumberFormat.SEPARATOR)
    if len(parts) != 2:
        raise FieldValueError(
            field="initiative_url",
            value=reg_number,
            message=(
                f"Cannot construct URL: registration number {reg_number!r} "
                f"does not contain the expected separator "
                f"{RegistrationNumberFormat.SEPARATOR!r}."
            ),
        )

    year, number = parts
    return URLConfig.INITIATIVE_DETAILS_URL_TEMPLATE.format(
        base_url=URLConfig.BASE_URL, year=year, number=number
    )
