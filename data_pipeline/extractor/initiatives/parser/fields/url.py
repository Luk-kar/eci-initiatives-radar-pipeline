def construct_url(reg_number: str) -> str:
    """Construct English URL from registration number"""

    if reg_number:
        year, number = reg_number.split("/")

        return URLConfig.INITIATIVE_DETAILS_URL_TEMPLATE.format(
            base_url=URLConfig.BASE_URL, year=year, number=number
        )
    return ""
