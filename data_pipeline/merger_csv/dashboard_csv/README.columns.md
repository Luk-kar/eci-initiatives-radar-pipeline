# DashboardRow columns

Describes the fields produced by the final dashboard merger pipeline step (`data_pipeline/merger_csv/dashboard_csv`), which combines the `eci_initiatives_*.csv`, `eci_responses_*.csv`, and `eci_responses_followup_legislation_*.csv` datasets to produce a single dashboard-ready `eci_dashboard_*.csv` file containing one row per initiative.

## Column definitions

| Field                                    | Type                     | Required?             | Why mandatory / optional                                                             | Example value                                                                                                               |
| ---------------------------------------- | ------------------------ | --------------------- | ----------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| registration_number                      | string  | Yes  | The unique identifier for an initiative; primary join key; must follow YYYY/NNNNNN.  | 2012/000001                                                                           |
| title                                    | string  | Yes  | The official title of the initiative and main human-readable identifier.             | Fraternité 2020 - Mobility. Progress. Europe.                                         |
| registration_year                        | Int64   | Yes  | The year the initiative was registered, used for filtering and grouping.             | 2012                                                                                  |
| registration_date                        | datetime| Yes  | The registration date in DD/MM/YYYY format.                                          | 09/05/2012                                                                            |
| current_status                           | string  | Yes  | The synthesized current status of the initiative.                                    | Collection Unsuccessful                                                               |
| objective                                | string  | Yes  | A text description of the initiative's goals.                                        | F2020 wants to enhance EU exchange programmes...                                      |
| commission_answer                        | string  | No   | Main answer extracted from the Commission response; empty string if unavailable.     | The Commission committed, in particular, to taking the following actions: ...         |
| initiative_url                           | string  | Yes  | Link to the official initiative page on the ECI portal.                              | https://citizens-initiative.europa.eu/initiatives/details/2012/000001_en              |
| signatures_collected_by_country          | json    | No   | JSON-formatted signatures by country; empty string if unavailable.                   | {"Austria": {"signatures": "57,643", "threshold": "14,250", "percentage": "404.51%"}, "Belgium": { ... }, ... } |
| signatures_countries_threshold_met_count | Int64   | No   | Count of countries that met the threshold.                                           | 12                                                                                    |
| signatures_collected                     | string  | No   | Total signatures as a comma-formatted number.                                        | 1,659,543                                                                             |
| funding_total                            | string  | No   | Total funding received as a formatted string.                                        | 140,000.00                                                                            |
| timeline_collection_closed               | datetime| No   | Date the collection period closed in DD/MM/YYYY format.                              | 01/11/2013                                                                            |
| timeline_collection_start                | datetime| No   | Date the collection period started in DD/MM/YYYY format.                             | 10/05/2012                                                                            |
| law_passed                               | string  | No   | Textual evidence that legislation progressed; empty string if none.                  | An amendment to the Drinking Water Directive came into force on 28 October 2015.      |

## Schema Configuration (`columns_types.json`)

To assist with automated parsing and data loading (e.g., via `pandas`), a machine-readable schema map is provided in [`columns_types.json`](./columns_types.json). 

## Expected Structure Notes

`DashboardRow` is created for every initiative present in the authoritative `eci_initiatives_*.csv`. It performs a left join against the responses and legislation datasets using `registration_number`.

If an initiative lacks a response or legislation follow-up, the missing fields are safely handled and typically output as empty strings to maintain a consistent dashboard schema without null values. Complex fields undergo validation to ensure they match expected formats (e.g., date formats, valid JSON for signatures by country, comma-formatted numbers for totals).

Output rows are assembled in the order they appear in the source initiatives dataset.