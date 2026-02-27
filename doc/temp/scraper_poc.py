import os
import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path


def main():
    print("🚀 Starting ECI Scraper POC...")

    # ---------------------------------------------------------
    # 1. FAILURE MODE (Test GitHub Actions Alerting)
    # ---------------------------------------------------------
    if os.environ.get("FORCE_CRASH", "").lower() == "true":
        print("💥 Crash mode activated via environment variable.")
        raise ValueError("Simulated scraping failure for GitHub Actions alerting POC!")

    # ---------------------------------------------------------
    # 2. SCRAPING MODE (Test Target URL)
    # ---------------------------------------------------------
    url = "https://citizens-initiative.europa.eu/initiatives/details/2024/000007_en"
    print(f"🌐 Fetching data from: {url}")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ECI-Tracker-POC/1.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to fetch the URL: {e}")
        raise

    # Store the raw HTML text
    raw_html = response.text

    # Parse the HTML to get the basic info
    soup = BeautifulSoup(raw_html, "html.parser")
    page_title = soup.title.string.strip() if soup.title else "Unknown Title"

    # Clean the reg number for a valid filename (e.g. ECI_2024_000007)
    reg_number = "ECI(2024)000007"
    safe_reg_number = reg_number.replace("(", "_").replace(")", "_")

    print(f"✅ Successfully scraped page: '{page_title}'")

    # ---------------------------------------------------------
    # 3. DATA STORAGE (Test Timestamped Folders & Saving)
    # ---------------------------------------------------------
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Create the nested directory structure
    output_dir = Path("data") / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"📁 Created directory: {output_dir}")

    # --- SAVE HTML FILE ---
    html_path = output_dir / f"{safe_reg_number}.html"
    with open(html_path, mode="w", encoding="utf-8") as f:
        f.write(raw_html)
    print(f"💾 Raw HTML saved to {html_path}")

    # --- SAVE CSV FILE ---
    csv_path = output_dir / "eci_poc_data.csv"
    with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["registration_number", "scraped_title", "timestamp_scraped", "source_url"]
        )
        writer.writerow([reg_number, page_title, timestamp, url])
    print(f"💾 CSV Data saved to {csv_path}")

    print("🎉 POC Script completed successfully!")


if __name__ == "__main__":
    main()
