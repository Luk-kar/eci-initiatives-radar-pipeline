## 1. Core Architecture (The Monorepo Concept)
The entire project will be hosted in a single GitHub repository (`eu-citizens-initiatives-tracker`).
* **No Database Required:** Data will be persistently stored directly in the repository's `data/` folder.
* **Serverless Execution:** Data extraction and processing will be orchestrated entirely by GitHub Actions, replacing Apache Airflow.
* **Zero Cost:** The infrastructure relies entirely on GitHub's free tier (Actions and Pages) and free API tiers, resulting in $0 monthly hosting costs.

## 2. Data Pipeline (GitHub Actions)
The pipeline will run on a scheduled cron job using standard GitHub-hosted Ubuntu runners.
* **Scraping Strategy:** Python `requests` and `BeautifulSoup` will scrape the `europa.eu` website for new or updated initiatives.
* **Anti-Blocking Measures:** 
  * ~~If the EU firewall blocks the shared Azure IPs used by GitHub Actions, the pipeline will utilize a free proxy pool (like ScraperAPI) to mask the runner's IP.~~
  * The pipeline will be configured to retry failed requests automatically.
* **Alerting:** If the Python script crashes, it will write the exact error string to `$GITHUB_OUTPUT`. A subsequent GitHub Actions step will email this specific error message to the developer.

## 3. Data Storage & Versioning Logic
To avoid abusing the EU servers (rate limiting) and to facilitate easy debugging, the pipeline will implement a strict data rotation and flagging system inside the `data/` folder.

* **The "MASTER" State File:** A master CSV file (`eci_master_state.csv`) will track the scraping status of every registration number.
  
* **Scraping Prevention (Flagging):** The script will **never scrape** an initiative again if it meets any of the following conditions:
  1. The signature collection is explicitly `closed` AND the signature count was `unsuccessful` (less than 1 million).
  2. The initiative successfully reached the `follow-up` stage and the Commission has issued its final legislative response (meaning the lifecycle is permanently locked). Only the `follow-up` will be scraped.
   
* **Timestamped Session Folders:** Instead of just keeping one master CSV, the pipeline will save the raw HTML files and the resulting CSVs of each run into a timestamped directory (e.g., `data/2026-02-26_14-00-00/`).
* **Merging Old with New:** For initiatives flagged as "do not scrape," the script will simply copy their data from the previous session's CSV and merge it with the freshly scraped data from the current session.
* **Auto-Cleanup (Rolling Window):** For debugging purposes, the repository will only store the last **3 sessions**. If a 4th session folder is created, the Python script will automatically delete the oldest timestamped directory before committing to GitHub.

~~## 4. Machine Learning (Few-Shot Classification)~~
~~New initiatives will be automatically categorized (e.g., "Environment", "Health") using an LLM.~~
~~* **Mechanism:** No model fine-tuning or retraining is required. The pipeline will use **Few-Shot Prompting** (In-Context Learning).~~
~~* **Implementation:** The Python script will dynamically read past examples from `eci_categories.csv` and inject them into the prompt sent to the API.~~
~~* **Provider:** Hugging Face Serverless Inference API (Free tier).~~

## 5. Security & Secrets Management
API keys and sensitive tokens will never be committed to the repository.
* **Production (GitHub):** Keys will be stored as encrypted **GitHub Actions Secrets** and injected into the pipeline as environment variables.
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
* **Hosting:** The dashboard will be hosted statically on **GitHub Pages**. 
* **Technology Choice:** Because standard Plotly Dash requires a persistent Python backend, the frontend will be built using a static/client-side approach:
~~* **Option A (stlite):** Streamlit compiled to WebAssembly. The browser downloads the latest CSV from the newest timestamped folder and runs Pandas/Plotly locally.~~
  * **Option B (Quarto / Plotly HTML):** The pipeline pre-calculates all charts and exports a static HTML file that GitHub Pages serves.