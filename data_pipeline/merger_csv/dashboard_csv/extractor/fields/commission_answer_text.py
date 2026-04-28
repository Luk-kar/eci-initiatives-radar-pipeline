"""
commission_answer_text
----------------------
Convert the raw ``commission_answer_text`` cell loaded from
``eci_responses_*.csv`` (a stringified Python list of paragraph strings)
into the single, narrative paragraph used in the dashboard CSV.

The reference output (``initiatives_*.csv``) shows one concise paragraph per
initiative, not a verbatim concatenation of the raw paragraphs, so this
extractor is expected to combine parsing with a summarisation step
(e.g. an LLM call) that reduces multi-paragraph Commission answers to a
single readable sentence/paragraph.

Implementation deliberately omitted — see TODOs.
"""

import logging

logger = logging.getLogger(__name__)


def extract(raw_cell: str | None) -> str:
    """Return the dashboard-ready commission answer text.

    Args:
        raw_cell: Raw value of the ``commission_answer_text`` column for an
                  initiative, or ``None`` / empty string when the Commission
                  has not yet answered the initiative.

    Returns:
        Single-paragraph narrative summary, or an empty string when the
        initiative has no Commission answer.

    Raises:
        NotImplementedError: This extractor is a placeholder.
    """
    # TODO: 1. handle None / empty -> return "".
    #       2. parse the Python list literal with ast.literal_eval.
    #       3. summarise the parsed paragraphs into a single narrative
    #          paragraph that matches the example file's tone.
    raise NotImplementedError(
        "commission_answer_text extraction is not implemented yet."
    )
