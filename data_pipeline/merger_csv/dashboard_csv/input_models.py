"""
Dashboard CSV — Source Row Models
---------------------------------
Dataclasses that mirror the **filtered** rows read from each of the three
source CSVs consumed by the dashboard merger:

* ``InitiativeRow``  ← ``eci_initiatives_*.csv`` (subset of columns)
* ``ResponseRow``    ← ``eci_responses_*.csv`` (only ``commission_answer``)
* ``LegislationRow`` ← ``eci_responses_followup_legislation_*.csv``
                       (``commission_answer`` is omitted because it has
                       already been read from the responses CSV)

The output row dataclass (``DashboardRow``) lives next to the field
extractors at :mod:`.extractor.fields.model` to mirror the directory
convention established by the legislation merger step.
"""

from __future__ import annotations

from dataclasses import dataclass


# ── eci_initiatives_*.csv ─────────────────────────────────────────────────────
@dataclass
class InitiativeRow:
    """A single row read from ``eci_initiatives_*.csv``.

    Only the columns required downstream are kept; auxiliary columns such as
    ``annex``, ``funding_by``, the verification timestamps, ``timeline``,
    and ``response_url`` are dropped at load time.
    """

    registration_number: str
    title: str
    objective: str
    current_status: str
    initiative_url: str
    timeline_registered: str
    timeline_collection_start_date: str
    timeline_collection_closed: str
    funding_total: str
    signatures_collected: str
    signatures_collected_by_country: str
    signatures_threshold_met: str


# ── eci_responses_*.csv ───────────────────────────────────────────────────────
@dataclass
class ResponseRow:
    """A single row read from ``eci_responses_*.csv``.

    Only ``commission_answer`` is retained alongside the join key.
    Follow-up information already lives in the legislation merge output
    and is read from there.
    """

    registration_number: str
    commission_answer: str


# ── eci_responses_followup_legislation_*.csv ──────────────────────────────────
@dataclass
class LegislationRow:
    """A single row read from ``eci_responses_followup_legislation_*.csv``.

    The ``commission_answer`` column is intentionally **not** materialised
    here because the same content is already loaded from
    ``eci_responses_*.csv`` (see :class:`ResponseRow`).
    """

    registration_number: str
    followup_events: str
    law_passed: str
    is_law_passed: str
    rejected_legislation: str
