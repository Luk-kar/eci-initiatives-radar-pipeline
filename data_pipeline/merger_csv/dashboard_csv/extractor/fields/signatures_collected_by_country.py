"""
signatures_collected_by_country
-------------------------------
Reshape the per-country signatures payload from the source schema into the
dashboard schema.

Source (``eci_initiatives.signatures_collected_by_country``) — Python literal::

    {'Austria': {'signatures': 57643, 'threshold': 14250, 'percentage': 404.51}, ...}

Dashboard (``initiatives_*.csv``) — JSON with renamed keys and formatted
numbers::

    {"Austria": {"statements_of_support": "57,643",
                 "threshold": "14,250",
                 "percentage": "404.51%"}, ...}

Per-country key mapping:

* ``signatures``  → ``statements_of_support`` (int → ``"{:,}"``)
* ``threshold``   → ``threshold``             (int → ``"{:,}"``)
* ``percentage``  → ``percentage``            (float → ``"{:.2f}%"``)

Implementation deliberately omitted — see TODOs.
"""

import logging

logger = logging.getLogger(__name__)


def extract(raw_cell: str | None) -> str:
    """Return the JSON-encoded per-country payload in the dashboard schema.

    Args:
        raw_cell: Raw value of
                  ``eci_initiatives.signatures_collected_by_country`` for an
                  initiative.  May be ``None`` or empty for early-stage
                  initiatives that have not yet collected signatures.

    Returns:
        JSON string in the dashboard schema, or an empty string when no
        per-country data is available.

    Raises:
        NotImplementedError: This extractor is a placeholder.
    """
    # TODO: 1. handle None / empty -> return "".
    #       2. ast.literal_eval the source cell.
    #       3. for each country, rename keys and reformat numeric fields.
    #       4. json.dumps the result (no indent, default separators) so the
    #          output matches the reference CSV's serialisation.
    raise NotImplementedError(
        "signatures_collected_by_country extraction is not implemented yet."
    )
