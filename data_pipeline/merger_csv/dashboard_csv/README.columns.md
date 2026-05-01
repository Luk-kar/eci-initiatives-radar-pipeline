# DashboardRow columns

Describes the fields produced by the final dashboard merger pipeline step (`data_pipeline/merger_csv/dashboard_csv`), which combines the `eci_initiatives_*.csv`, `eci_responses_*.csv`, and `eci_responses_followup_legislation_*.csv` datasets to produce a single dashboard-ready `eci_dashboard_*.csv` file containing one row per initiative.

## Column definitions

| Field | Type | Required? | Why mandatory / optional (Logical Intent) |
|---|---|---:|---|
| `registration_number` | `str` | Yes | The unique identifier for an initiative. The primary key used to join the three upstream datasets. Sourced from `eci_initiatives`. Must follow the `YYYY/NNNNNN` format. |
| `title` | `str` | Yes | The official title of the initiative. Mandatory because it's the primary human-readable identifier. |
| `registration_year` | `str` | Yes | The year the initiative was registered. Extracted from the `registration_number`. Essential for filtering and grouping by year on the dashboard. |
| `registration_date` | `str` | Yes | The exact date the initiative was registered (`DD/MM/YYYY`). Mapped from `timeline_registered`. Mandatory for chronological sorting and display. |
| `current_status` | `Literal[...]` | Yes | The synthesized status of the initiative (e.g., "Collection Unsuccessful", "Law Passed"). Derived from the raw status and legislation outcomes. Mandatory to inform users of the initiative's current standing. |
| `objective` | `str` | Yes | A text description of the initiative's goals. Must be non-empty to provide context on the dashboard. |
| `commission_answer` | `str` | No | Extracted main answer from the Commission (from `eci_responses`). Empty string if the Commission has not answered yet or if the answer is missing. |
| `initiative_url` | `str` | Yes | The URL to the official details page on the ECI portal. Mandatory for linking out to the source. |
| `signatures_collected_by_country` | `str` | No | JSON-formatted string detailing signatures per country. Empty string if collection data is unavailable. Must be valid JSON if provided. |
| `signatures_countries_threshold_met_count` | `str` | No | The count of countries that met the signature threshold. |
| `signatures_collected` | `str` | No | The total number of signatures collected, as a comma-formatted number (e.g., "1,234"). |
| `funding_total` | `str` | No | Total funding received, as a comma-formatted number. |
| `timeline_collection_closed` | `str` | No | The date the signature collection period closed (`DD/MM/YYYY`). Empty string if not closed yet. |
| `timeline_collection_start` | `str` | No | The date the signature collection period started (`DD/MM/YYYY`). Renamed from `timeline_collection_start_date`. |
| `law_passed` | `str` | No | Textual evidence that legislation has progressed, extracted from the upstream legislation dataset. Empty string if no law has passed or if there is no legislation data. |

## Expected Structure Notes

`DashboardRow` is created for every initiative present in the authoritative `eci_initiatives_*.csv`. It performs a left join against the responses and legislation datasets using `registration_number`.

If an initiative lacks a response or legislation follow-up, the missing fields are safely handled and typically output as empty strings to maintain a consistent dashboard schema without null values. Complex fields undergo validation to ensure they match expected formats (e.g., date formats, valid JSON for signatures by country, comma-formatted numbers for totals).

Output rows are assembled in the order they appear in the source initiatives dataset.