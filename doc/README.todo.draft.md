1. Local Workspace & Environment Setup (Split Repo Simulation)
Instead of two GitHub repositories, create two adjacent sibling directories to mimic the separation of logic and data.

Directory Structure: Create eci-pipeline/ (Logic) and eci-dashboard/ (Data/Frontend) in the same parent folder.

Dependency Management: Inside eci-pipeline/, initialize a virtual environment (using uv, as per your previous workflows) and install requests, beautifulsoup4, python-dotenv, pandas, and your visualization library (e.g., plotly or quarto).

Secrets Management: Create a .env file inside eci-pipeline/ to hold dummy variables (e.g., DATA_REPO_PAT=local_test) and add it to .gitignore. Ensure your script uses python-dotenv and os.environ.get() so the transition to GitHub Secrets later is seamless.

2. Refactoring the Scraper (Logic Repo)
Port the extraction logic from your old Luk-kar repository, but transition the architecture to fit the new serverless requirements.

Switch to Lightweight Requests: Replace any previous Selenium or heavy Airflow DAG logic with pure requests and BeautifulSoup. Reuse your old HTML parsing logic (e.g., CSS selectors for signatures, policy areas, and commission outcomes).

Anti-Blocking Implementation: Configure a requests.Session() mounted with a urllib3 Retry adapter to automatically handle connection drops or rate-limiting from europa.eu.

Cross-Repo Data Writing: Configure the local scraper to output the final processed CSVs directly to the sibling directory: ../eci-dashboard/data/.

3. Simulating GitHub Artifacts (Intelligent Caching)
The most complex part of the new architecture is the artifact-based caching. You need to simulate GitHub Actions' artifact storage locally.

Local Artifact Directory: Create an artifacts/ folder inside eci-pipeline/ to represent the GitHub Actions storage.

Timestamped Saves: Modify your script to generate a timestamp (e.g., raw-data-YYYY-MM-DD) and save all raw HTML responses into artifacts/raw-data-YYYY-MM-DD/.

Fallback Logic: At the start of the script, check if artifacts/ contains previous folders.

If a valid folder exists, load the historical HTML files for closed initiatives directly from disk.

If the folder is empty or files are missing, trigger the fallback to scrape all historical initiatives directly from the web.

Auto-Cleanup Mock: Write a tiny utility function that deletes folders in artifacts/ older than 56 days to ensure your local disk mirrors the GitHub retention-days behavior.

4. Static Dashboard Generation (Data Repo)
Reuse your data transformation logic to pre-calculate the required metrics, but output them as a static file rather than a dynamic server app.

Static HTML Export (Option B): Write a Python script (or Quarto document) that reads the fresh CSVs from ../eci-dashboard/data/.

Chart Generation: Generate the Plotly charts specified in the requirements (KPI row, Signature scatter/bars, Commission outcomes donut, Registration timeline). Export them directly to an index.html file in the eci-dashboard/ root.

Edge Case Handling: Ensure your data processing step includes the logic from your previous project to handle litigation nuances, such as mapping Minority SafePack to its correct 2017 registration number despite the 2013 origins.

5. Local Orchestration (Simulating GitHub Actions)
Replace the GitHub Actions .yml file with a local bash script (run_pipeline.sh) to test the execution flow and error handling.

Execution Flow: The bash script should activate your virtual environment, execute the Python scraper, and then execute the dashboard generation script.

Alerting Simulation: Catch the exit code ($?) of the Python scraper. If it crashes (exit code 1), have the bash script print a mock email alert to the terminal mimicking the $GITHUB_OUTPUT failure notification.