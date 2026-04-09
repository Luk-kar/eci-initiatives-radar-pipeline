"""
Log messages for the Commission followup scraper.

Module-specific keys only. Shared keys (browser lifecycle, retry,
content waiter, download flow) are inherited from scraper_shared.
"""

from ..scraper_shared.log_messages import SHARED_LOG_MESSAGES

LOG_MESSAGES: dict = {
    **SHARED_LOG_MESSAGES,
    # ── Scraping lifecycle ─────────────────────────────────────────────────────
    "scraping_start": "Starting Commission followup scraping at: {timestamp}",
    "scraping_complete": "Commission followup scraping finished!",
    # ── Link extraction ────────────────────────────────────────────────────────
    "links_found": "Found {count} Commission followup links",
    "no_links_found": "No Commission followup links found in followup pages",
    "initiative_pages_missing": "Initiative pages directory not found: {path}",
    # ── Summary ────────────────────────────────────────────────────────────────
    "divider_line": "=" * 60,
    "completion_timestamp": "Scraping completed at {timestamp}",
    "start_time": "Start time: {start_scraping}",
    "total_links_found": "Total followup links found: {count}",
    "pages_downloaded": "Pages downloaded: {downloaded_count}/{total_count}",
    "failed_downloads": "Failed downloads: {failed_count}",
    "failed_url": "  - {failed_url}",
    "all_downloads_successful": "All downloads successful!",
    "files_saved_in": "Files saved in: {path}",
}
