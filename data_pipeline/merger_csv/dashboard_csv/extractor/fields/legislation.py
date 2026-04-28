"""
legislation
-----------
Compose the dashboard's ``legislation`` narrative from the structured flags
produced by the legislation merge step.

Inputs come from ``eci_responses_followup_legislation_*.csv``:

* ``Law_Passed``           — Python list literal of matched-text spans
                             (populated when ``Is_Law_Passed`` is ``True``).
* ``Is_Law_Passed``        — ``"True"`` / ``"False"`` flag.
* ``Rejected_Legislation`` — ``"True"`` / ``"False"`` flag.

Selection rule (matches the reference ``initiatives_*.csv``):

* ``Is_Law_Passed == True``        → narrate from ``Law_Passed``.
* ``Rejected_Legislation == True`` → narrate from the response text that
                                     describes the rejection.
* otherwise                        → empty string.

The output is a single plain-text paragraph with all Markdown link syntax
flattened to its label only (so links are gone).

Implementation deliberately omitted — see TODOs.
"""

import logging

logger = logging.getLogger(__name__)


def extract(
    law_passed_raw: str | None,
    is_law_passed: bool,
    rejected_legislation: bool,
) -> str:
    """Return the dashboard ``legislation`` narrative.

    Args:
        law_passed_raw:        Raw value of the ``Law_Passed`` column
                               (Python list literal, or empty / ``None``).
        is_law_passed:         Parsed ``Is_Law_Passed`` flag.
        rejected_legislation:  Parsed ``Rejected_Legislation`` flag.

    Returns:
        Plain-text legislation narrative, or an empty string when neither
        flag is set.

    Raises:
        NotImplementedError: This extractor is a placeholder.
    """
    # TODO: 1. early-return "" when both flags are False.
    #       2. parse law_passed_raw as a Python list literal.
    #       3. flatten Markdown links ([label](url) -> label).
    #       4. join the spans into a single paragraph; pick the
    #          rejection narrative when rejected_legislation is True.
    raise NotImplementedError("legislation extraction is not implemented yet.")
