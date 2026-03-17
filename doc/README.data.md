Here is the complete updated minimal data mapping for `plan_sketch_updated`:

***

## 1. KPI Cards (Top Row)

| Card | Source CSV | Column(s) | Logic |
|---|---|---|---|
| **Total Initiatives** | `eci_initiatives` | `registration_number` | `COUNT(*)` all rows |
| **Currently Open** | `eci_initiatives` | `current_status` | `COUNT` where `current_status` = `"Open for collection"` |
| **Reached 1M Signatures** | `eci_initiatives` | `signatures_collected` | `COUNT` where `signatures_collected >= 1,000,000` |
| **Got EU Response** | `eci_initiatives` | `response_commission_url` | `COUNT` where value is not null/empty |
| **Led to Legislation** | `eci_merger_responses_and_followup` | `final_outcome_status` | `COUNT` where value = `"Law Active"` |

***

## 2. Signatures Collected by Initiative (Horizontal Bar Chart)

From **`eci_initiatives`** only:

| Column | Purpose |
|---|---|
| `title` | Bar label (y-axis) |
| `signatures_collected` | Bar length (x-axis) |
| `signatures_threshold_met` | Color — **green** if `True`, **red** if `False` |

The dashed vertical reference line is a **hardcoded value at 1,000,000** — not pulled from any column.

***

## 3. Initiative Outcomes After Submission (Donut Chart)

Pre-filter: only initiatives where `signatures_collected >= 1,000,000`.
Join key: `eci_initiatives.registration_number` → `eci_merger_responses_and_followup.registration_number`

| Segment | Source | Column | Logic |
|---|---|---|---|
| **Law Active / Passed** | `eci_merger_responses_and_followup` | `final_outcome_status` | value = `"Law Active"` |
| **Commission Engaged** | `eci_merger_responses_and_followup` | `final_outcome_status` + `commission_promised_new_law` | value contains `"Proposal Made"` / `"Alternative Actions"` / `"Already Covered"`, OR `commission_promised_new_law = True` |
| **Awaiting Response** | `eci_initiatives` | `current_status` | value = `"Valid initiative"` AND `response_commission_url` is null |
| **Rejected** | `eci_merger_responses_and_followup` | `final_outcome_status` | value starts with `"Rejected - "` |

***

## 4. Currently Open — List (first section below top row)

From **`eci_initiatives`** only:

| Column | Purpose |
|---|---|
| `title` | Initiative name |
| `current_status` | Filter: `"Open for collection"` |
| `timeline_collection_closed` | "X days left" countdown |
| `signatures_collected` | Progress indicator |
| `url` | Clickable link |

***

## 5. ECI Registrations per Year 2012–2025 (Line/Area Chart)

From **`eci_initiatives`** only:

| Column | Purpose |
|---|---|
| `timeline_registered` | Extract **year**, group by year → `COUNT` per year (first line) |
| `timeline_response_commission_date` | Extract year, group → `COUNT` per year (second line, answered initiatives) |

***

## 6. Map with Total Signatures Count (Choropleth)

From **`eci_initiatives`** only:

| Column | Purpose |
|---|---|
| `signatures_collected_by_country` | Parse JSON → sum `statements_of_support` per country across all initiatives → map fill value |

No join needed.

***

## 7. Reached 1M Signatures — List

From **`eci_initiatives`**:

| Column | Purpose |
|---|---|
| `title` | Initiative name |
| `signatures_collected` | Display total count |
| `signatures_collected` | Filter: `>= 1,000,000` |
| `final_outcome` | Outcome label |
| `url` | Clickable link |

***

## 8. Got EU Response — List

Join: `eci_initiatives` + `eci_merger_responses_and_followup` on `registration_number`:

| Column | Source | Purpose |
|---|---|---|
| `title` | `eci_initiatives` | Initiative name |
| `response_commission_url` | `eci_initiatives` | Filter: not null |
| `timeline_response_commission_date` | `eci_initiatives` | Response date |
| `final_outcome_status` | `eci_merger_responses_and_followup` | Outcome label |
| `url` | `eci_initiatives` | Clickable link |

***

## 9. Led to Legislation — List

Join: `eci_initiatives` + `eci_merger_responses_and_followup` on `registration_number`:

| Column | Source | Purpose |
|---|---|---|
| `title` | `eci_initiatives` | Initiative name |
| `final_outcome_status` | `eci_merger_responses_and_followup` | Filter: `"Law Active"` |
| `law_implementation_date` | `eci_merger_responses_and_followup` | Date law entered into force |
| `laws_actions` | `eci_merger_responses_and_followup` | Summary of enacted legislation |
| `url` | `eci_initiatives` | Clickable link |

***

## 10. Total Initiatives — List (bottom, with scroller)

From **`eci_initiatives`** only:

| Column | Purpose |
|---|---|
| `title` | Initiative name |
| `registration_number` | ID / sort key |
| `current_status` | Status label |
| `timeline_registered` | Registration year |
| `url` | Clickable link |

Add a **scroller** if row count exceeds a display threshold (127 rows expected).

```
Awaiting Response
Collection Ongoing
Commission Engaged
Law Passed
Rejected Legislation
Collection Unsuccessful
Withdrawn
```