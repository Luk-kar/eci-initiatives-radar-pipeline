## 1. Core Architecture (Split Repository Pattern)
The project will be divided into two separate personal GitHub repositories to keep the logic divided from the data/presentation:
1. **Logic Repo (`eci-pipeline`):** Houses the Python scraping code and the GitHub Actions workflow.
2. **Data Repo (`eci-dashboard`):** Houses the resulting data (`data/` folder) and the GitHub Pages static site.
* **No Database Required:** Data will be persistently stored directly in the Data Repo's `data/` folder.
* **Serverless Execution:** Data extraction and processing will be orchestrated entirely by GitHub Actions in the Logic Repo, which will push the final data to the Data Repo.
* **Zero Cost:** The infrastructure relies entirely on GitHub's free tier (Actions and Pages) and free API tiers, resulting in $0 monthly hosting costs.

## 2. Data Pipeline (GitHub Actions)
The pipeline will run on a scheduled weekly cron job using standard GitHub-hosted Ubuntu runners.
* **Scraping Strategy:** Python `requests` and `BeautifulSoup` will scrape the `europa.eu` website for new or updated initiatives.
* **Anti-Blocking Measures:** 
  * ~~If the EU firewall blocks the shared Azure IPs used by GitHub Actions, the pipeline will utilize a free proxy pool (like ScraperAPI) to mask the runner's IP.~~
  * The pipeline will be configured to retry failed requests automatically.
* **Alerting:** If the Python script crashes, it will write the exact error string to `$GITHUB_OUTPUT`. A subsequent GitHub Actions step will email this specific error message to the developer.

## 3. Data Storage & Versioning Logic
To avoid abusing the EU servers (rate limiting) and to facilitate easy debugging, the pipeline will implement a strict data rotation and caching system using GitHub Artifacts.

* **Raw Data Storage (GitHub Artifacts):** Raw HTML files and intermediate logs will no longer bloat the Git repository. The GitHub Actions pipeline will dynamically generate a timestamped name using `$GITHUB_OUTPUT` (e.g., `eci-raw-data-2026-02-27-10-45`) and upload the raw folder as a **GitHub Actions Artifact**.
* **Historical HTML Caching (Intelligent Scraping):** At the start of a run, the pipeline will download all available current artifacts. The Python logic inside will choose the correct artifact and parse the valid historical HTMLs for closed initiatives locally. If no artifacts exist (or files are missing), it will automatically fallback to scraping all of them directly from the web. The scrape will be executed on a weekly basis, as the ECI regulatory process and signature counts are slow-moving metrics that do not require daily updates.
* **Auto-Cleanup (Artifact Retention):** To prevent hitting the 500MB free-tier limit for Actions Storage, the upload action will be configured with `retention-days: 7(days) * 4(weeks) * 2(months) = 56 days total`. On the basis of the weekly scraping. GitHub will automatically delete older raw scrapes, eliminating the need for custom Python cleanup logic.

~~## 4. Machine Learning (Few-Shot Classification)~~
~~New initiatives will be automatically categorized (e.g., "Environment", "Health") using an LLM.~~
~~* **Mechanism:** No model fine-tuning or retraining is required. The pipeline will use **Few-Shot Prompting** (In-Context Learning).~~
~~* **Implementation:** The Python script will dynamically read past examples from `eci_categories.csv` and inject them into the prompt sent to the API.~~
~~* **Provider:** Hugging Face Serverless Inference API (Free tier).~~

## 5. Security & Secrets Management
API keys and sensitive tokens will never be committed to the repository.
* **Production (GitHub):** Keys will be stored as encrypted **GitHub Actions Secrets** (including the `DATA_REPO_PAT` needed to push across repositories) and injected into the pipeline as environment variables.
* **Local Development (Rybnik):** Keys will be stored in a local `.env` file (which must be added to `.gitignore`).
* **Code Parity:** The Python script will use `python-dotenv` and `os.environ.get()` to seamlessly fetch the keys in both environments without changing the code.
* **Handoff Protocol:** Because GitHub strips Secrets when a repo is transferred or forked, the `README.md` must clearly document which keys the new owner needs to generate.

## 6. The Dashboard (Frontend)
The dashboard will be designed for the "average EU citizen" and will fit within a 1 to 1.5 screen layout.
* **Key Content:** 
  * KPI row (Total initiatives, open, successful, led to law).
  * Signatures collected vs. 1M threshold (Scatter/Bar charts).
  * Commission response outcomes (Donut chart).
  * ECI registration timeline (Area chart).
* **Data Nuances:**
  * It must account for registration number changes resulting from court litigation (e.g., *Minority SafePack* shifting from a 2013 to a 2017 registration number).
* **Hosting:** The dashboard will be hosted statically on **GitHub Pages** (served from the Data Repo). 
* **Technology Choice:** Because standard Plotly Dash requires a persistent Python backend, the frontend will be built using a static/client-side approach:
~~* **Option A (stlite):** Streamlit compiled to WebAssembly. The browser downloads the latest CSV from the newest timestamped folder and runs Pandas/Plotly locally.~~
  * **Option B (Quarto / Plotly HTML):** The pipeline pre-calculates all charts and exports a static HTML file that GitHub Pages serves.
