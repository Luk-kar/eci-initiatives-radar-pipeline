"""
signatures_collected_by_country
-------------------------------
Reshape the ``signatures_collected_by_country`` dictionary string into
formatted JSON for the dashboard.
"""

import ast
import json


def extract(signatures_raw: str | None) -> str:
    """Parse, format, and return valid JSON for the dashboard.

    Args:
        signatures_raw: Raw value of the ``signatures_collected_by_country`` column
                        (Python dict literal string, or empty / ``None``).

    Returns:
        A valid JSON string with formatted numbers (e.g. "57,643" and "404.51%"),
        or an empty string if the input is empty or invalid.

    Raises:
        ValueError: If parsing the string fails, or if numeric conversions fail.
        TypeError: If the parsed structure is not a dictionary.
    """

    if not signatures_raw or not str(signatures_raw).strip():
        return ""

    try:
        parsed_data = ast.literal_eval(signatures_raw)

    except (ValueError, SyntaxError) as exc:
        raise ValueError(
            f"Failed to parse signatures_collected_by_country literal: {signatures_raw!r}"
        ) from exc

    if not isinstance(parsed_data, dict):
        raise TypeError(
            f"Expected signatures_collected_by_country to parse into a dict, got {type(parsed_data).__name__}"
        )

    formatted_data = {}

    for country, stats in parsed_data.items():

        if not isinstance(stats, dict):
            raise TypeError(
                f"Expected stats for country {country!r} to be a dict, got {type(stats).__name__}"
            )

        formatted_stats = {}

        # Format signatures: int -> string with thousands comma
        if "signatures" in stats:

            signatures = stats["signatures"]

            try:
                # If signatures is None, int(None) will correctly raise a TypeError
                formatted_stats["signatures"] = f"{int(signatures):,}"

            except (ValueError, TypeError) as exc:
                raise ValueError(
                    f"Invalid signatures value for {country!r}: {signatures!r}"
                ) from exc

        # Format threshold: int -> string with thousands comma
        if "threshold" in stats:

            threshold = stats["threshold"]

            try:
                formatted_stats["threshold"] = f"{int(threshold):,}"

            except (ValueError, TypeError) as exc:
                raise ValueError(
                    f"Invalid threshold value for {country!r}: {threshold!r}"
                ) from exc

        # Format percentage: float -> string with % symbol
        if "percentage" in stats:

            percentage = stats["percentage"]

            try:
                formatted_stats["percentage"] = f"{float(percentage):g}%"

            except (ValueError, TypeError) as exc:
                raise ValueError(
                    f"Invalid percentage value for {country!r}: {percentage!r}"
                ) from exc

        formatted_data[country] = formatted_stats

    # Serialize back to valid JSON
    return json.dumps(formatted_data)
