"""
current_status
--------------
Translate the raw ``current_status`` text scraped from the ECI portal into
the dashboard's controlled vocabulary, and upgrade it using the legislation
analysis flags when the Commission has already replied.

Target dashboard vocabulary (nine values):

* ``Awaiting Collection``
* ``Collection Ongoing``
* ``Collection Verification``
* ``Collection Unsuccessful``
* ``Awaiting Response``
* ``Commission Engaged``
* ``Law Passed``
* ``Rejected Legislation``
* ``Withdrawn``

Source vocabulary (raw, observed in ``eci_initiatives.current_status``):

* ``Registered``, ``Collection ongoing``, ``Collection closed``,
  ``Verification`` (sometimes with a trailing ``*`` and embedded newlines),
  ``Valid initiative``, ``Answered initiative``,
  ``Unsuccessful collection``, ``Withdrawn``.

For ``Answered initiative`` rows, the verdict is refined using the
legislation flags (``Is_Law_Passed`` / ``Rejected_Legislation``) produced
by the legislation merge step, so that the dashboard can distinguish
between *engaged*, *law passed*, and *rejected* outcomes.
"""

import logging
import re

logger = logging.getLogger(__name__)


# Source -> dashboard vocabulary mapping.
#
# "Answered initiative" maps to "Commission Engaged" as a default; the value
# is upgraded to "Law Passed" / "Rejected Legislation" inside ``extract`` when
# the corresponding legislation flag is set.
_STATUS_MAP: dict[str, str] = {
    "Registered": "Awaiting Collection",
    "Collection ongoing": "Collection Ongoing",
    "Collection closed": "Collection Verification",
    "Verification": "Collection Verification",
    "Valid initiative": "Awaiting Response",
    "Answered initiative": "Commission Engaged",
    "Unsuccessful collection": "Collection Unsuccessful",
    "Withdrawn": "Withdrawn",
}

_ANSWERED = "Answered initiative"

_WHITESPACE_RE = re.compile(r"\s+")


def _normalise(raw: str | None) -> str:
    """Strip whitespace, collapse internal whitespace, drop trailing ``*``."""

    if not raw:
        return ""

    cleaned = _WHITESPACE_RE.sub(" ", raw).strip()

    # Strip any number of trailing ``*`` markers (and re-strip whitespace
    # they may leave behind).
    return cleaned.rstrip("*").strip()


def extract(
    raw_status: str,
    is_law_passed: bool | None,
    rejected_legislation: bool | None,
) -> str:
    """Map the raw status to the dashboard vocabulary.

    Args:
        raw_status:           Value of ``eci_initiatives.current_status`` for
                              the initiative (whitespace and trailing ``*``
                              must be normalised before mapping).

        is_law_passed:        Legislation flag from
                              ``eci_responses_followup_legislation``;
                              ``None`` when the initiative has no legislation row.

        rejected_legislation: Legislation flag from
                              ``eci_responses_followup_legislation``;
                              ``None`` when the initiative has no legislation row.

    Returns:
        One of the nine canonical dashboard status labels.

    Raises:
        ValueError: ``raw_status`` does not normalise to a known source label.
    """

    normalised = _normalise(raw_status)

    try:
        mapped = _STATUS_MAP[normalised]

    except KeyError as exc:

        raise ValueError(
            f"Unknown raw current_status value: {raw_status!r} "
            f"(normalised: {normalised!r})"
        ) from exc

    if normalised != _ANSWERED:
        return mapped

    # "Answered initiative" — refine using the legislation flags.
    # Both flags are mandated for answered initiatives; missing values
    # signal an upstream contract violation in the legislation merge step.
    if is_law_passed is None or rejected_legislation is None:
        raise ValueError(
            "Answered initiative is missing legislation flags: \n"
            f"is_law_passed={is_law_passed!r}\n"
            f"rejected_legislation={rejected_legislation!r}\n"
        )

    if is_law_passed is True and rejected_legislation is True:
        raise ValueError(
            "Law cannot be passed for the initiative, when the commission rejected to do so earlier:\n"
            f"is_law_passed={is_law_passed!r}\n"
            f"rejected_legislation={rejected_legislation!r}\n"
        )

    # "Answered initiative" — refine using the legislation flags.
    if is_law_passed:
        return "Law Passed"

    if rejected_legislation:
        return "Rejected Legislation"

    return "Commission Engaged"
