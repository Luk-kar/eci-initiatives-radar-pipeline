"""
Log messages for the Commission responses scraper.

Module-specific keys only. Shared keys (browser lifecycle, retry,
content waiter, download flow) are inherited from scraper_shared.
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
    "initiative_pages_missing": "Initiative pages directory not found: {path}",
    # ── Summary ────────────────────────────────────────────────────────────────
    "divider_line": "=" * 60,
    "completion_timestamp": "Completion timestamp: %s",
    "start_time": "Start time: %s",
    "total_links_found": "Total response links found: %s",
    "pages_downloaded": "Pages downloaded: %s / %s",
    "all_downloads_successful": "All downloads successful!",
    "failed_downloads": "Failed downloads: %s",
    "failed_url": "  - %s",
    "files_saved_in": "Files saved in: %s",
}
