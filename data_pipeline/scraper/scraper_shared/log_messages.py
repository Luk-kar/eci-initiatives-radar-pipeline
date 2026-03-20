"""
Shared log messages for all ECI scrapers.

Module-specific messages (entity names, summary stats) stay in the
per-module log_messages.py. Anything here must read correctly in:
  - scraper/initiatives
  - scraper/responses
  - scraper/responses_followup_website
"""

SHARED_LOG_MESSAGES: dict = {
    # ── Lifecycle ──────────────────────────────────────────────────────────────
    "scraping_start": "Starting scraping at: {timestamp}",
    "browser_init": "Initializing browser...",
    "browser_success": "Browser initialized successfully",
    "browser_closed": "Browser closed",
    "pages_browser_closed": "Individual pages browser closed",
    # ── Orchestration ──────────────────────────────────────────────────────────
    "csv_timestamps_updated": "Updated CSV with download timestamps: {path}",
    "loading_page": "Loading page: {url}",
    "page_saved": "✅ Page {page} saved to: {path}",
    "dynamic_content_wait": "Waiting {wait_time:.1f}s for dynamic content...",
    # ── Page downloader ────────────────────────────────────────────────────────
    "processing_item": "Processing {index}/{total}: {url}",
    "awaiting_next_page": "Awaiting next page in: {wait_time:.2f}s",
    "download_complete": "Download completed. Failed URLs: {failed_count}",
    "downloading_html": "Downloading the html file...",
    "download_success": "✅ Successfully downloaded: {filename}",
    "rate_limit_retry": "⚠️ Received rate limiting. Retrying {retry}/{max_retries} in {wait_time:.1f} seconds...",
    # ── Content waiter ─────────────────────────────────────────────────────────
    "content_loaded": "Content loaded: {selector}",
    "no_content_found": "No main content elements found, but proceeding...",
    # ── File operations ────────────────────────────────────────────────────────
    "dirs_created": "Created directories: {list_dir}, {pages_dir}",
    "html_validation_warning": "⚠️ HTML validation warning for {filename}: {error_type}: {error}",
    "html_prettify_failed": "⚠️ Failed to prettify HTML for {filename}: {error}. Saving raw HTML without prettification.",
    # ── Data parser ────────────────────────────────────────────────────────────
    "parsing_complete": "✅ Found {count} entries",
}
