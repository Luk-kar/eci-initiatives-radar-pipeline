# LegislationResult columns


Describes the fields produced by the legislation-extraction pipeline step (`data_pipeline/merger_csv/responses_followup_legislation`), which combines the most recent `eci_responses_*.csv` and `eci_responses_followup_*.csv` per run, analyses the merged text, and emits one row per initiative.


## Column definitions


| Field | Type | Required? | Why mandatory / optional (Logical Intent) |
|---|---|---:|---|
| `registration_number` | `str` | Yes | The unique identifier for an initiative. Every analysed row must be attributable to a specific initiative, and this is the join key linking the Commission's response to its later follow-up. Analysis is meaningless without it, so the field is never optional. |
| `commission_answer` | `Optional[List[str]]` | No | Paragraphs of the Commission's main answer to the initiative. Carried into the output as provenance so a reader can see exactly which answer text was considered. Declared optional because the upstream response page may legitimately lack a recoverable answer section (older or atypical layouts), and this column should faithfully reflect that absence rather than fabricate content. |
| `followup_events` | `Optional[List[str]]` | No | Subsequent legislative or institutional events linked to the initiative. Carried into the output as provenance alongside the answer. An empty list is the normal outcome for initiatives with no published follow-up; the field is `Optional` so genuinely missing follow-up data can also be represented distinctly from "no events have happened yet." |
| `law_passed` | `Optional[List[str]]` | No | Concrete textual evidence that legislation has actually progressed (e.g., adoption, entry into force, publication). Optional because the absence of such evidence is itself a meaningful answer — most initiatives never reach this stage. Also unset when the Commission has explicitly rejected legislation, so that wording about a refused proposal is not mistaken for evidence that a law passed. |
| `Is_Law_Passed` | `bool` | Yes | The headline yes/no answer to "did downstream legislation actually pass?" Always present because every initiative deserves an explicit boolean conclusion rather than ambiguity from a missing value. Stays consistent with `law_passed`: `True` exactly when there is concrete evidence to show. |
| `Rejected_Legislation` | `bool` | Yes | The complementary headline answer to "did the Commission close the door on legislating here?" Always present for the same reason as `Is_Law_Passed` — readers expect a definite verdict. Distinguishes a true rejection from a partial rejection that is offset elsewhere in the same response by a commitment to bring forward a different proposal. |


## Expected Structure Notes


`LegislationResult` is only created for initiatives that already appear in `eci_responses_*.csv` — i.e. registrations that have reached the published-response lifecycle stage upstream. The legislation step joins those rows with `eci_responses_followup_*.csv` on `registration_number`; rows present only on the follow-up side are rejected by `collect.validate_followup_registration_numbers` before any analysis runs.

The two debugging-oriented columns (`commission_answer`, `followup_events`) preserve the **provenance** of the analysed text so that downstream consumers can audit which sentences led to a given `law_passed` / `Rejected_Legislation` verdict. They are populated independently and are **not** deduplicated against each other — an item that legitimately appears both in the Commission's answer and again in a follow-up event remains in both columns by design. Only within `followup_events` itself are duplicates dropped, because the same follow-up text frequently appears both embedded in the response page and on the dedicated follow-up site.

The three analysis columns (`law_passed`, `Is_Law_Passed`, `Rejected_Legislation`) are computed against the **deduplicated union** of `commission_answer` and `followup_events`. `Rejected_Legislation` is evaluated first; when it is `True`, `law_passed` is intentionally short-circuited to `None` to avoid surfacing partial-rejection wording as evidence of new legislation. `Is_Law_Passed` is then derived deterministically from `law_passed` and is therefore guaranteed consistent with it.

Output rows are sorted ascending by `registration_number` before being written, so the CSV is stable and diff-friendly across runs.
