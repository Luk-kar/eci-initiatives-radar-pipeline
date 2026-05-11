# 💾 Data Pipeline

A modular data pipeline for collecting, extracting, and preparing European Citizens’ Initiative (ECI) data from the official [EU portal](https://citizens-initiative.europa.eu/index_en)

The package is organized around reusable scraping, extraction, merging data, and shared pipeline utilities, with dedicated modules for `initiatives`, `Commission responses`, and `follow-up` content.

## Overview

The `data_pipeline` package contains the data acquisition and transformation layer for the ECI project.
It includes:

- Scrapers for:
  - initiative pages, 
  - Commission responses
  - follow-up websites
- Extractors that convert scraped HTML into structured CSV outputs using parser classes and Pydantic models.
- Shared helpers for logging, sorting, path discovery, browser utilities, HTML handling, and file operations.
- Tests: unit and end-to-end 

## Project structure

```text
data_pipeline/
│
│   # Build system and project dependency
├── pyproject.toml
│
│   # Auto-generated package metadata and entry points
├── eci_data_pipeline.egg-info/
│
├── README.data_pipeline.md <-- This doc
│
├── scraper/
│   ├── initiatives/
│   ├── responses/
│   ├── responses_followup/
│   └── scraper_shared/
│
├── extractor/
│   ├── initiatives/
│   ├── responses/
│   ├── responses_followup/
│   └── extractor_shared/
│
├── merger_csv/
│   ├── dashboard_csv/
│   └── responses_followup_legislation/
│
└── pipeline_shared/
```

## Installation

### Requirements

- `Python 3.10` or newer.

### Dependencies

The package currently declares these runtime dependencies:

- `selenium==4.35.0`: Browser automation for web scraping
- `beautifulsoup4==4.13.5`: HTML parsing and data extraction
- `pydantic==2.12.5`: Validates extracted data models
- `html5lib==1.1`: HTML5 parser for BeautifulSoup

### Install locally

First, install [`uv`](https://docs.astral.sh/uv/), an extremely fast Python package installer, and then install the package in editable mode:

```bash
# Install uv (macOS/Linux)
curl -LsSf https://astral.sh/uv/install.sh | sh
# Alternatively, using pip: pip install uv
```

```bash
## 1. Create a venv in data_pipeline/ (from root)
uv venv data_pipeline/.venv.data_pipeline

## 2. Activate it (still from root)
source data_pipeline/.venv.data_pipeline/bin/activate

## 3. Install the project in editable mode, pointing at the subdir
uv pip install -e data_pipeline
```

## Data flow

The data pipeline is executed sequentially across distinct stages for scraping, extraction, and final data merging:

Run the pipeline:
```bash
# 1. Scrape core ECI initiative pages
python3 -m data_pipeline.scraper.initiatives

# 2. Extract downloaded HTML into structured initiative data
python3 -m data_pipeline.extractor.initiatives

# 3. Scrape official Commission response pages
python3 -m data_pipeline.scraper.responses

# 4. Extract response details and follow-up links
python3 -m data_pipeline.extractor.responses

# 5. Scrape external follow-up websites linked in the responses
python3 -m data_pipeline.scraper.responses_followup

# 6. Extract content and structure from follow-up websites
python3 -m data_pipeline.extractor.responses_followup

# 7. Consolidate legislative document data from follow-ups
python3 -m data_pipeline.merger_csv.responses_followup_legislation

# 8. Prepare and format the final datasets for the UI dashboard
python3 -m data_pipeline.merger_csv.dashboard_csv
```

### Main extracted fields

For a field-by-field explanation of the datasets look for `README.columns.md` in each module.

See the final example: [`data_pipeline/merger_csv/dashboard_csv/README.columns.md`](data_pipeline/merger_csv/dashboard_csv/README.columns.md).

## Testing

Run tests with:

```bash
# Remember to load local environment:
# watch step: Install locally

# 1. Install the project in editable mode, pointing at the subdir
uv pip install -e data_pipeline[dev]

# 2. Run the test
pytest data_pipeline

# Run tests including end-to-end (e2e) pipeline execution
pytest data_pipeline --e2e
```

