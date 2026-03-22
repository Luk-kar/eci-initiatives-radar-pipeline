"""
Log messages for the ECI initiatives scraper.

All user-facing log strings live here. Format placeholders use {name} syntax
and are filled at call sites with .format(**kwargs).
"""

from ..scraper_shared.log_messages import SHARED_LOG_MESSAGES

LOG_MESSAGES: dict = {
    **SHARED_LOG_MESSAGES,
    # ── Orchestration ──────────────────────────────────────────────────────────
    "no_initiatives_found": "No initiatives found to classify or download",
    "initiative_data_saved": "Initiative data saved to: {path}",
    "download_phase_start": "Starting individual initiative pages download...",
    # ── Listing fetcher ────────────────────────────────────────────────────────
    "pagination_start": "Starting pagination scraping from: {url}",
    "first_page_failed": "❌ Failed to load first listing page. Aborting pagination.",
    "pagination_complete": (
        "Completed scraping {page_count} pages "
        "with {total_initiatives} total initiatives"
    ),
    "listing_page_failed": "❌ Failed to scrape listing page {page}",
    "listings_loaded": "Initiatives loaded successfully",
    "page_loaded": "Initiatives loaded successfully on page {page}",
    "main_page_saved": "Main page saved to: {path}",
    "main_page_failed": "❌ Failed to scrape main initiatives page",
    "listing_timeout": "Timeout waiting for initiatives: {error} — continuing",
    "next_button_found": (
        "Found 'Next' button on page {page}, navigating to page {next_page}"
    ),
    "last_page": (
        "No 'Next' button found on page {page}. " "This appears to be the last page."
    ),
    "listing_content_timeout": (
        "No initiatives found or timeout on page {page}: "
        "{error} — continuing with current content"
    ),
    # ── Data parser ────────────────────────────────────────────────────────────
    "parsing_listing": "Parsing saved listing page for initiatives links...",
    "processing_initiative": SHARED_LOG_MESSAGES["processing_item"],  # alias
    # ── ECI content waiter ─────────────────────────────────────────────────────
    "timeline_loaded": "Initiative progress timeline loaded",
    "timeline_not_found": (
        "Initiative progress timeline not found, "
        "should be in all initiatives.\ncontinuing..."
    ),
    # ── Summary ────────────────────────────────────────────────────────────────
    "summary_scraping": {
        "scraping_complete": "🎉 SCRAPING FINISHED! 🎉",
        "completion_timestamp": "Scraping completed at: {timestamp}",
        "start_time": "Start time: {start_scraping}",
        "total_pages_scraped": "Total pages scraped: {page_count}",
        "total_initiatives_found": "Total initiatives found: {total_initiatives}",
        "initiatives_by_category": "Initiatives by category (current_status):",
        "registered_status": "- Registered: {count}",
        "collection_ongoing_status": "- Collection ongoing: {count}",
        "valid_initiative_status": "- Valid initiative: {count}",
        "pages_downloaded": "Pages downloaded: {downloaded_count}/{total_initiatives}",
        "failed_downloads": "Failed downloads: {failed_count}",
        "failed_url": " - {failed_url}",
        "all_downloads_successful": "✅ All downloads successful!",
        "files_saved_in": "Files saved in: initiatives/{start_scraping}",
        "main_page_sources": "Main page sources:",
        "page_source": "  Page {page_num}: {path}",
        "divider_line": "=" * 60,
    },
}
