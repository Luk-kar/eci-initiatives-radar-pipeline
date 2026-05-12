# 🕸️ Scraper

The automated data collection layer of the European Citizens’ Initiative (ECI) Dashboard. This module acts as the core extraction engine, orchestrating Selenium WebDrivers and BeautifulSoup parsers to collect, process, and structure initiative data from the ECI web portals.

## Overview

The `scraper` directory contains the complete pipeline for downloading initiative information, official Commission responses, and follow-up updates. It separates scraping tasks into specialized sub-modules (initiatives, responses, and follow-ups) while relying on a robust shared library for browser initialization, file saving, HTML validation, and error handling.

## Project structure

```text
scraper/
│
├── README.scraper.md          <-- This doc
│
├── initiatives/               # Module for scraping ECI listings and detail pages
│   ├── fetchers/              # Browser operations for listings and details
│   ├── fileoperations.py      # HTML validation and saving utilities
│   ├── htmlparser.py          # Extracts data points from raw HTML
│   ├── main.py                # Execution entry point for initiatives
│   └── statistics.py          # Generation of run summary reports
│
├── responses/                 # Module for scraping Commission responses
│   ├── fetchers/              # WebDriver logic for downloading responses
│   ├── fileoperations/        # HTML and CSV savers for responses
│   ├── htmlparser.py          # Parses initiative pages for response links
│   └── main.py                # Execution entry point for responses
│
├── responses_followup/        # Module for scraping additional follow-ups
│   ├── fetchers/              # WebDriver logic for downloading follow-ups
│   ├── fileoperations/        # HTML and CSV savers for follow-ups
│   ├── htmlparser.py          # Parses response pages for follow-up links
│   └── main.py                # Execution entry point for follow-ups
│
└── scraper_shared/            # Common utilities across all scrapers
    ├── browser.py             # Shared Chrome WebDriver initialization
    ├── filesutils.py          # Directory setup and CSV writing operations
    ├── htmlutils.py           # HTML parsing and validation tools
    ├── logmessages.py         # Shared logging templates and messages
    └── response_and_followup/ # Shared logic specifically for responses and follow-ups
```