# 🇪🇺⚙️ ECI Pipeline — European Citizens' Initiative Tracker

<p align="center">
  <img src="doc/images/eci_participation_campaign.jpg" alt="ECI Pipeline promo" /><br/>
  <sub>Source: European Citizens' Initiative | European Commission (CC BY 4.0)</sub>
</p>

A fully automated, end-to-end data pipeline and dashboard system for tracking [**European Citizens' Initiatives (ECIs)**](https://citizens-initiative.europa.eu/index_en) — from raw HTML scraping of the official EU portal through to a live, published static dashboard.

Published via [**GitHub Pages**](https://luk-kar.github.io/eci-initiatives-radar/)

> **Live dashboard repo →** [`eci-initiatives-radar-dashboard`](https://github.com/Luk-kar/eci-initiatives-radar-dashboard) *(updated automatically every Saturday)*
---

*The main goal is to build independent tools that improve public understanding of how institutions operate and help verify whether real-world practice matches declared goals.*

*The project is also intended to be reusable, so it can serve as a starting point for related any public-transparency initiatives.*

## 🏗️ Architecture Overview

The project is composed of four tightly integrated layers, each living in its own directory.

The design is intentionally lightweight — no database, no microservices, no message queue.
ECI data changes slowly (at most a handful of new initiatives per run so far), so a weekly batch
job writing to static files is a better fit than a live API or a streaming pipeline.
The entire system is a linear script chain: scrape → extract → merge → render → publish.

The trade-off is deliberate: the dashboard is always a few days behind the source portal,
but the system needs no server to keep running, no infrastructure to maintain, and no
on-call response when something breaks at 3 AM. A smaller dependency footprint also means
the pipeline runs on any machine with Python and a browser — nothing to install beyond the
packages declared in each `pyproject.toml`.

```
eci-pipeline/
│
├── .github/                  # CI/CD — GitHub Actions workflow
│   ├── workflows/
│   │   └── run_pipeline.yml  # Scheduled end-to-end pipeline runner
│   └── commands/             # Provider-agnostic Bash scripts
│       ├── set_up_enviro.sh
│       ├── run_pipeline.sh
│       └── give_path_latest_data.sh
│
├── data_pipeline/            # Data acquisition and transformation (Python)
│   ├── scraper/              # Selenium + BeautifulSoup scrapers
│   ├── extractor/            # HTML → structured CSV converters
│   ├── merger_csv/           # CSV join, clean, and final dataset builder
│   └── pipeline_shared/      # Shared helpers (logging, paths, browser utils)
│
├── page_creator/             # Presentation layer generator (Python)
│   ├── partials/             # Plotly charts, KPI counters, HTML tables
│   ├── data_loader.py        # Finds and loads the latest pipeline CSV
│   └── generate_charts.py    # Generator registry and export logic
│
└── page_to_export/           # Static dashboard UI (HTML/CSS/JS)
    ├── index.html            # Main layout with placeholder slots
    ├── generated/            # ← populated at runtime by page_creator
    └── static/               # Version-controlled assets (styles, scripts, images)
```

---

## 🔀 Data Flow

```
EU Portal (live HTML)
        │
        ▼
 [1] data_pipeline/scraper         — Selenium + BS4 download raw HTML pages
        │  initiatives / responses / follow-up sites
        ▼
 [2] data_pipeline/extractor       — Pydantic-validated HTML → CSV records
        │
        ▼
 [3] data_pipeline/merger_csv      — Join, clean → dashboard.csv
        │
        ▼
 [4] page_creator                  — Plotly charts + HTML partials + JS map
        │
        ▼
 [5] page_to_export/generated/     — Static artifacts ready to serve
        │
        ▼
 [6] eci-initiatives-radar-dashboard  — GitHub Pages (auto PR via Actions)
```

---

## 📦 Modules

### 💾 [`data_pipeline/`](./data_pipeline/README.data_pipeline.md)

Collects and transforms ECI data through **8 sequential pipeline stages**:

| Stage | Command | What it does |
|-------|---------|--------------|
| 1 | `python3 -m data_pipeline.scraper.initiatives` | Scrape core ECI initiative pages |
| 2 | `python3 -m data_pipeline.extractor.initiatives` | Extract initiative data → CSV |
| 3 | `python3 -m data_pipeline.scraper.responses` | Scrape Commission response pages |
| 4 | `python3 -m data_pipeline.extractor.responses` | Extract response details + follow-up links |
| 5 | `python3 -m data_pipeline.scraper.responses_followup` | Scrape external follow-up websites |
| 6 | `python3 -m data_pipeline.extractor.responses_followup` | Extract follow-up content |
| 7 | `python3 -m data_pipeline.merger_csv.responses_followup_legislation` | Consolidate legislative data |
| 8 | `python3 -m data_pipeline.merger_csv.dashboard_csv` | Build final `dashboard.csv` |

**Key dependencies:**
- `selenium==4.35.0` — browser automation for navigating and downloading ECI portal pages
- `beautifulsoup4==4.13.5` — HTML parsing to locate and extract structured data from downloaded pages
- `pydantic==2.12.5` — runtime validation and type-checking of extracted data models before CSV output
- `html5lib==1.1` — HTML5-compliant parser backend used by BeautifulSoup for robust malformed-markup handling

**Requires:** Python 3.10+

---

### 📊 [`page_creator/`](./page_creator/README.page_creator.md)

Consumes `dashboard.csv` and generates all dynamic UI artifacts:

- **Plotly charts** — outcomes, signature maps, cohorts, top-10 rankings
- **KPI counters** — top-level summary figures
- **HTML tables** — status-filtered initiative lists (ongoing, successful, withdrawn)
- **`generated.js`** — auto-built JS map linking each partial to its DOM slot

Run the full generation:

```bash
python3 -m page_creator
# or, using the installed entry point:
generate
```

**Key dependencies:**
- `pandas` — loads the latest `dashboard.csv` into a DataFrame and handles all data filtering and aggregation for each generator
- `plotly` — renders interactive, embeddable HTML charts (maps, bubble plots, cohort timelines, top-10 rankings) exported as self-contained HTML snippets
**Requires:** Python 3.11+

---

### 🌐 [`page_to_export/`](./page_to_export/README.page_export.md)

The final, static dashboard ready to be deployed. Combines:

- **`index.html`** — layout skeleton with named slots
- **`generated/`** — Plotly partials and JS map written by `page_creator` at runtime
- **`static/`** — version-controlled CSS, scripts (scroll-to-top, countdown timer, partial loader), and images

Serve locally for development:

```bash
cd page_to_export
python3 -m http.server 8000
# open http://localhost:8000
```

> ⚠️ Opening `index.html` directly in a browser will not work — it requires a local HTTP server to resolve the dynamically fetched partials.

---

### 🔄 [`.github/`](./.github/README.workflows.md)

Orchestrates the entire system on a **weekly schedule (every Saturday)** or on manual dispatch via GitHub Actions. The workflow runs 11 steps end-to-end:

| Step | Action |
|------|--------|
| 0–1 | Checkout repo + restore cached virtual environments |
| 2 | Set up `data_pipeline` and `page_creator` envs via `set_up_enviro.sh` |
| 3 | Random short delay to stagger runner load |
| 4 | Run all 8 pipeline stages via `run_pipeline.sh` |
| 5–7 | Resolve latest run directory, compress to `.tar.gz`, upload artifact (kept 30 days) |
| 8–9 | Checkout dashboard repo + sync `page_to_export/` via `rsync` |
| 10 | Open a Pull Request in the dashboard repo linking back to this run |

Any step failure halts the job immediately.

---

## ⚙️ Installation

Both Python packages are installed using [`uv`](https://docs.astral.sh/uv/), an extremely fast package installer.

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Install `data_pipeline`

```bash
uv venv data_pipeline/.venv.data_pipeline
source data_pipeline/.venv.data_pipeline/bin/activate
uv pip install -e data_pipeline
```

### Install `page_creator`

```bash
uv venv page_creator/.venv.page_creator
source page_creator/.venv.page_creator/bin/activate
uv pip install -e page_creator
```

---

## 🚀 Running the Full Pipeline Locally

```bash
# 1. Activate the data_pipeline environment
source data_pipeline/.venv.data_pipeline/bin/activate

# 2. Run all 8 pipeline stages
python3 -m data_pipeline.scraper.initiatives
python3 -m data_pipeline.extractor.initiatives
python3 -m data_pipeline.scraper.responses
python3 -m data_pipeline.extractor.responses
python3 -m data_pipeline.scraper.responses_followup
python3 -m data_pipeline.extractor.responses_followup
python3 -m data_pipeline.merger_csv.responses_followup_legislation
python3 -m data_pipeline.merger_csv.dashboard_csv

# 3. Switch to the page_creator environment
deactivate
source page_creator/.venv.page_creator/bin/activate

# 4. Generate dashboard artifacts
python3 -m page_creator

# 5. Serve locally
cd page_to_export && python3 -m http.server 8000
```

---

## 🧪 Testing

```bash
# data_pipeline unit tests
uv pip install -e data_pipeline[dev]
pytest data_pipeline

# data_pipeline including end-to-end execution
pytest data_pipeline --e2e

# page_creator unit tests
pytest page_creator
```

---

## 🔑 One-time CI/CD Setup

Before the GitHub Actions workflow can open Pull Requests into the dashboard repo, three things must be configured:

1. **Create a Fine-Grained PAT** with `Contents` (read/write) and `Pull requests` (read/write) access scoped to `eci-initiatives-radar-dashboard`.
2. **Add the PAT as a repository secret** named `DASHBOARD_REPO_PAT` in this pipeline repo.
3. **Create the `automated-pr` label** in the dashboard repo (Issues → Labels → New label).

Optionally, configure **GitHub Pages** in the dashboard repo (Settings → Pages → Deploy from branch).

Full instructions: [`.github/README.workflows.md`](./.github/README.workflows.md)

---

## 🚚 Porting to Another CI Provider

The three scripts in `.github/commands/` are plain Bash with no GitHub-specific logic and run identically on any Linux runner. Only `run_pipeline.yml` is provider-specific. Key equivalences:

| GitHub Actions | GitLab CI |
|----------------|-----------|
| `on: / schedule:` | `rules: / schedule:` |
| `runs-on:` | `image: / tags:` |
| `actions/cache` | `cache: paths:` |
| `actions/upload-artifact` | `artifacts: paths: + expire_in:` |
| `create-pull-request` | `glab mr create` (CLI v18.11) |
| `secrets.*` | CI/CD variable (masked + protected) |

---

## 📋 Data Documentation

Column-by-column field descriptions are available in each module's `README.columns.md`. The final output schema is documented at:

[`data_pipeline/merger_csv/dashboard_csv/README.columns.md`](./data_pipeline/merger_csv/dashboard_csv/README.columns.md)

## 📜 LICENSE

Just look at [`LICENSE`](LICENSE)