# ⛏️ Extractor

Outlines the architecture, data models, and execution flow of the `data_pipeline/extractor` module. Parsing scraped European Citizens' Initiative (ECI) HTML files into structured CSV datasets.

## Module Architecture
The extractor module processes raw HTML files gathered during the scraping phase, extracts specific fields using BeautifulSoup, validates data integrity with Pydantic, and writes the results to CSV files. The module is divided into a shared utilities library and three distinct extraction pipelines.

## Extraction Pipelines

| Pipeline | Input HTML Directory | Output CSV Pattern | Core Pydantic Model | Description |
| :--- | :--- | :--- | :--- | :--- |
| `initiatives` | `initiatives/` | `eci_initiatives_<timestamp>.csv` | `ECIInitiativeDetailsRecord` | Parses core initiative details, timelines, objectives, and signature statistics. |
| `responses` | `responses/` | `eci_responses_<timestamp>.csv` | `ECIResponseRecord` | Merges previous metadata with the parsed Commission answer text and response-page follow-up details. |
| `responses_followup` | `responses_followup/` | `eci_responses_followup_<timestamp>.csv` | `ECIFollowupRecord` | Extracts content from dedicated follow-up websites, including Commission answer recap and follow-up events. |

## Data Flow
The extraction process follows a standardized, step-by-step pipeline across the submodules:
- **Collect**: Scans the targeted HTML directory and maps registration numbers (e.g., `2020000001`) to their respective file paths using regex validation.
- **Load Metadata**: Reads the upstream CSV (e.g., `eci_initiatives.csv`, `eci_responses_followup.csv` or `eci_responses.csv`) to inherit existing metadata like URLs and titles, ensuring continuity between scraping and extraction phases.
- **Parse**: Utilizes modular `BeautifulSoup` functions to navigate the HTML DOM and extract specific fields. Complex sections like timelines and signature tables are handled by dedicated field extractors in the `parser` directory.
- **Assemble**: Merges the inherited CSV metadata with the newly parsed HTML fields into a unified `Pydantic` record.
- **Write**: Serializes the validated `Pydantic` models into a final, timestamped CSV file, sorting the rows chronologically by registration number.

## Data Validation
The module relies heavily on Pydantic `BaseModel` classes to enforce data schemas. Built-in `field_validator` methods automatically sanitize numeric inputs, removing commas, asterisks, and whitespace before casting them to integers or floats (such as threshold counts and signature percentages). Complex nested structures, such as financial sponsors and timeline events, are actively serialized into JSON strings to maintain flat CSV compatibility.