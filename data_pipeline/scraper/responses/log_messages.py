"""
Log messages for the Commission responses scraper.

Module-specific keys live here. Shared keys (browser lifecycle, retry,
content waiter, etc.) are inherited from scraper_shared.log_messages.
"""

from ..scraper_shared.log_messages import SHARED_LOG_MESSAGES

LOG_MESSAGES: dict = {
    **SHARED_LOG_MESSAGES,
    # ── Scraping lifecycle ─────────────────────────────────────────────────────
    "scraping_start": "Starting Commission responses scraping at: {timestamp}",
    "scraping_complete": "Commission responses scraping finished!",
    # ── Link extraction ────────────────────────────────────────────────────────
    "links_found": "Found {count} Commission response links",
    "no_links_found": "No Commission response links found in initiative pages",
    # ── Orchestration ──────────────────────────────────────────────────────────
    "processing_response": "Processing {index}/{total}: {url}",
    "initiative_pages_missing": "Initiative pages directory not found: {path}",
    # ── Summary ────────────────────────────────────────────────────────────────
    "divider_line": "=" * 60,
    "completion_timestamp": "Scraping completed at {timestamp}",
    "start_time": "Start time: {start_scraping}",
    "total_links_found": "Total response links found: {count}",
    "pages_downloaded": "Pages downloaded: {downloaded_count}/{total_count}",
    "failed_downloads": "Failed downloads: {failed_count}",
    "failed_url": "  - {failed_url}",
    "all_downloads_successful": "All downloads successful!",
    "files_saved_in": "Files saved in: {path}",
}
