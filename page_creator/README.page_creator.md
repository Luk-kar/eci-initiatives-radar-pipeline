# 📊 Page Creator

A dedicated module for generating dynamic HTML snippets (partials) and JavaScript maps for the European Citizens’ Initiative (ECI) dashboard. 

The package consumes the final dataset produced by the `data_pipeline`, loads the most recent CSV data, and renders Plotly charts, key performance indicator (KPI) counters, data tables (lists), and update timestamps. These generated artifacts are then exported and embedded into the main static webpage.

## Overview

The `page_creator` package serves as the presentation layer generator.
It includes:

- **Chart Generators**: Renders Plotly visualizations (outcomes, signature maps, cohorts, top 10s).
- **List Generators**: Generates stylized HTML tables for different initiative statuses (e.g., ongoing, successful, withdrawn).
- **Counter Generators**: Produces KPI elements showing top-level summaries.
- **Data Loader**: Automatically discovers and loads the latest processed dashboard CSV from the `data_pipeline` run directories.
- **Artifact Exporter**: Exports the generated HTML partials and an auto-generated JavaScript `GENERATED_PARTIALS` map to integrate into the UI.
- **Tests**: Comprehensive `pytest` coverage for table rendering, utilities, and generators.

## Project structure

```text
page_creator/
│
│   # Build system and project dependency
├── pyproject.toml
│
├── README.page_creator.md <-- This doc
│
│   # Core application entry points and utilities
├── __main__.py             # Executable module entry point
├── config.py               # Shared Plotly layout and styling config
├── data_loader.py          # Finds and loads the latest dashboard CSV
├── generate_charts.py      # Registry for generators and export logic
├── paths.py                # Output directory path definitions
├── utils.py                # Shared HTML wrapper logic
│
│   # Generators divided by element type
├── partials/
│   ├── charts/             # Plotly chart generators (map, bubbles, cohorts, etc.)
│   ├── counters/           # KPI row generator
│   ├── date_stamp/         # Update timestamp generator
│   ├── lists/              # HTML table generators for ECI statuses
│   └── styles/             # Shared styling (colors)
│
└── tests/                  # Root-level test modules
```

## Installation

### Requirements

- `Python 3.11` or newer.

### Dependencies

The package requires the following main dependencies declared in `pyproject.toml`:
- `pandas`: For data manipulation and reading the pipeline CSVs.
- `plotly`: For generating interactive and responsive charts.

### Install locally

Using `uv` for fast installation in a virtual environment:

```bash
# 1. Create a venv in page_creator/ (from root)
uv venv page_creator/.venv.page_creator

# 2. Activate it (still from root)
source page_creator/.venv.page_creator/bin/activate

# 3. Install the project in editable mode
uv pip install -e page_creator
```

## App flow

The module automatically processes the latest available data to render the web artifacts:

1. **Load Data**: `data_loader.py` searches the `data_pipeline` output directories for the most recent run and loads the target dashboard CSV into a pandas DataFrame.
2. **Generate Elements**: The main script iterates through registered generator functions in `generate_charts.py` to produce HTML strings for charts, lists, counters, and date stamps.
3. **Export Partials**: The generated HTML snippets are saved to `page_to_export/generated/partials/`.
4. **Generate JS Map**: A JavaScript file (`generated.js`) is constructed, mapping each HTML partial to its corresponding DOM element ID.

Run the full generation process:
```bash
# Run the page creator module
python3 -m page_creator
```
Alternatively, using the installed script entry point:
```bash
generate
```

## Testing

The project uses `pytest` for unit testing across all partial generators and core utilities.

Run tests with:

```bash
# Run all tests
pytest page_creator
```