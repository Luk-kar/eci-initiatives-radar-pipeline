# 🔀 Merger CSV

Outlines the architecture, data models, and execution flow of the `data_pipeline/merger_csv` module. Merging and analyzing extracted European Citizens' Initiative (ECI) CSV files into a unified dashboard dataset.

## Overview

The `merger_csv` directory contains the complete pipeline for taking the structured CSV datasets produced by the extractor layer (`initiatives`, `responses`, and `responses_followup_legislation`) and consolidating them into a single analytical view. It joins the data on `registration_number`, cleans and standardizes the fields, and produces `dashboard.csv` which feeds interactive visualizations.

## Project Structure

```text
merger_csv/
│
├── README.merger_csv.md       <-- This doc
│
└── dashboard_csv/             # Core merger module
    ├── __main__.py            # Execution entry point 
    ├── run.py                 # Main execution workflow
    ├── session.py             # Configures processing paths and directories
    ├── collect.py             # Locates, loads, and deduplicates source CSVs
    ├── assemble.py            # Joins source datasets and generates DashboardRow objects
    ├── write.py               # Serializes the final output to dashboard.csv
    ├── io.py                  # Pydantic-based generic CSV loading/writing functions
    ├── input_models.py        # Pydantic schemas for the incoming source CSV files
    │
    ├── extractor/             # Translates and cleans individual fields
    │   ├── __init__.py        # Orchestrates field translation (analyse_row)
    │   ├── fields/            # Logic for transforming specific complex fields
    │   │   ├── current_status.py
    │   │   ├── law_passed.py
    │   │   ├── objective.py
    │   │   ├── registration_year.py
    │   │   ├── commission_answer.py
    │   │   ├── signatures_collected_by_country.py
    │   │   └── model.py       # Defines DashboardRow Pydantic schema
    │   │
    │   └── utils/             # Helper utilities (e.g. regex for year extraction)
    │
    └── tests/                 # Unit and E2E tests for the merger pipeline
```

## Data Validation

The module relies heavily on Pydantic `BaseModel` classes to enforce data schemas both on input and output.
- **Input validation**: Source files are loaded into `InitiativeRow`, `ResponseRow`, and `LegislationRow` schemas that ignore extra fields and enforce correct data types (e.g., date parsing, integer parsing for thresholds).
- **Output validation**: The derived row is validated against the strict `DashboardRow` schema which represents exactly the columns necessary for the downstream visualizations.