"""
Log messages for the ECI initiatives scraper.

All user-facing log strings live here. Format placeholders use {name} syntax
and are filled at call sites with .format(**kwargs).
"""

LOG_MESSAGES: dict = {
    # ── Lifecycle ──────────────────────────────────────────────────────────────
    "scraping_start": "Starting scraping at: {timestamp}",
    "browser_init": "Initializing browser...",
    "browser_success": "Browser initialized successfully",
    "browser_closed": "Browser closed",
    "pages_browser_closed": "Individual pages browser closed",
    # ── Main orchestration ─────────────────────────────────────────────────────
    "no_initiatives_found": "No initiatives found to classify or download",
    "initiative_data_saved": "Initiative data saved to: {path}",
    "download_phase_start": "Starting individual initiative pages download...",
    "csv_timestamps_updated": "Updated CSV with download timestamps: {path}",
    # ── Listing fetcher ────────────────────────────────────────────────────────
    "pagination_start": "Starting pagination scraping from: {url}",
    "first_page_failed": "❌ Failed to load first listing page. Aborting pagination.",
    "pagination_complete": "Completed scraping {page_count} pages with {total_initiatives} total initiatives",
    "listing_page_failed": "❌ Failed to scrape listing page {page}",
    "listings_loaded": "Initiatives loaded successfully",
    "main_page_saved": "Main page saved to: {path}",
    "main_page_failed": "❌ Failed to scrape main initiatives page",
    "listing_timeout": "Timeout waiting for initiatives: {error} — continuing",
    "loading_page": "Loading page: {url}",
    "page_loaded": "Initiatives loaded successfully on page {page}",
    "page_saved": "✅ Page {page} saved to: {path}",
    "next_button_found": "Found 'Next' button on page {page}, navigating to page {next_page}",
    "last_page": "No 'Next' button found on page {page}. This appears to be the last page.",
    "dynamic_content_wait": "Waiting {wait_time:.1f}s for dynamic content...",
    "listing_content_timeout": "No initiatives found or timeout on page {page}: {error} — continuing with current content",
    # ── ECI pages fetcher ──────────────────────────────────────────────────────
    "processing_initiative": "Processing {index}/{total}: {url}",
    "awaiting_next_page": "Awaiting next page in: {wait_time:.2f}s",
    "download_complete": "Download completed. Failed URLs: {failed_count}",
    "downloading_html": "Downloading the html file...",
    "download_success": "✅ Successfully downloaded: {filename}",
    "rate_limit_retry": "⚠️  Received rate limiting. Retrying {retry}/{max_retries} in {wait_time:.1f} seconds...",
    # ── Content waiter ─────────────────────────────────────────────────────────
    "timeline_loaded": "Initiative progress timeline loaded",
    "timeline_not_found": "Initiative progress timeline not found, should be in all initiatives.\ncontinuing...",
    "content_loaded": "Content loaded: {selector}",
    "no_content_found": "No main content elements found, but proceeding...",
    # ── File operations ────────────────────────────────────────────────────────
    "dirs_created": "Created directories: {list_dir}, {pages_dir}",
    "html_validation_warning": "⚠️  HTML validation warning for {filename}: {error_type}: {error}",
    "html_prettify_failed": "⚠️  Failed to prettify HTML for {filename}: {error}. Saving raw HTML without prettification.",
    # ── Data parser ────────────────────────────────────────────────────────────
    "parsing_listing": "Parsing saved listing page for initiatives links...",
    "parsing_complete": "✅ Found {count} initiative entries",
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
