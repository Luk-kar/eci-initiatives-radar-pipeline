"""Tests for the shared display_completion_summary helper."""

import logging
from unittest.mock import MagicMock, call

from data_pipeline.scraper.scraper_shared.response_and_followup.statistics import (
    display_completion_summary,
)

LOG_MESSAGES = {
    "divider_line": "=" * 60,
    "scraping_complete": "Scraping complete!",
    "completion_timestamp": "Completed at {timestamp}",
    "start_time": "Start: {start_scraping}",
    "total_links_found": "Total links: {count}",
    "pages_downloaded": "Downloaded: {downloaded_count}/{total_count}",
    "failed_downloads": "Failed: {failed_count}",
    "failed_url": "  - {failed_url}",
    "all_downloads_successful": "All downloads successful!",
    "files_saved_in": "Saved in: {path}",
}

LINKS = [{"url": "https://example.com/1"}, {"url": "https://example.com/2"}]


class TestDisplayCompletionSummaryNoFailures:

    def test_logs_scraping_complete(self):

        logger = MagicMock(spec=logging.Logger)
        display_completion_summary(
            "2024-01-01T12:00:00",
            LINKS,
            [],
            2,
            "/out",
            log_messages=LOG_MESSAGES,
            logger=logger,
        )
        logger.info.assert_any_call(LOG_MESSAGES["scraping_complete"])

    def test_logs_all_downloads_successful(self):

        logger = MagicMock(spec=logging.Logger)
        display_completion_summary(
            "2024-01-01T12:00:00",
            LINKS,
            [],
            2,
            "/out",
            log_messages=LOG_MESSAGES,
            logger=logger,
        )
        logger.info.assert_any_call(LOG_MESSAGES["all_downloads_successful"])

    def test_does_not_call_logger_error(self):

        logger = MagicMock(spec=logging.Logger)
        display_completion_summary(
            "2024-01-01T12:00:00",
            LINKS,
            [],
            2,
            "/out",
            log_messages=LOG_MESSAGES,
            logger=logger,
        )
        logger.error.assert_not_called()

    def test_logs_correct_total_count(self):

        logger = MagicMock(spec=logging.Logger)
        display_completion_summary(
            "2024-01-01T12:00:00",
            LINKS,
            [],
            2,
            "/out",
            log_messages=LOG_MESSAGES,
            logger=logger,
        )
        logger.info.assert_any_call(LOG_MESSAGES["total_links_found"].format(count=2))

    def test_logs_pages_downloaded(self):

        logger = MagicMock(spec=logging.Logger)
        display_completion_summary(
            "2024-01-01T12:00:00",
            LINKS,
            [],
            2,
            "/out",
            log_messages=LOG_MESSAGES,
            logger=logger,
        )
        logger.info.assert_any_call(
            LOG_MESSAGES["pages_downloaded"].format(downloaded_count=2, total_count=2)
        )

    def test_logs_files_saved_in(self):

        logger = MagicMock(spec=logging.Logger)
        display_completion_summary(
            "2024-01-01T12:00:00",
            LINKS,
            [],
            2,
            "/out",
            log_messages=LOG_MESSAGES,
            logger=logger,
        )
        logger.info.assert_any_call(LOG_MESSAGES["files_saved_in"].format(path="/out"))

    def test_logs_start_time(self):

        logger = MagicMock(spec=logging.Logger)
        display_completion_summary(
            "2024-01-01T12:00:00",
            LINKS,
            [],
            2,
            "/out",
            log_messages=LOG_MESSAGES,
            logger=logger,
        )
        logger.info.assert_any_call(
            LOG_MESSAGES["start_time"].format(start_scraping="2024-01-01T12:00:00")
        )


class TestDisplayCompletionSummaryWithFailures:

    def test_logs_failed_count(self):

        logger = MagicMock(spec=logging.Logger)
        display_completion_summary(
            "2024-01-01T12:00:00",
            LINKS,
            ["https://fail.com"],
            1,
            "/out",
            log_messages=LOG_MESSAGES,
            logger=logger,
        )
        logger.error.assert_any_call(
            LOG_MESSAGES["failed_downloads"].format(failed_count=1)
        )

    def test_logs_each_failed_url(self):

        logger = MagicMock(spec=logging.Logger)
        display_completion_summary(
            "2024-01-01T12:00:00",
            LINKS,
            ["https://fail1.com", "https://fail2.com"],
            0,
            "/out",
            log_messages=LOG_MESSAGES,
            logger=logger,
        )
        logger.error.assert_any_call(
            LOG_MESSAGES["failed_url"].format(failed_url="https://fail1.com")
        )
        logger.error.assert_any_call(
            LOG_MESSAGES["failed_url"].format(failed_url="https://fail2.com")
        )

    def test_does_not_log_all_downloads_successful(self):

        logger = MagicMock(spec=logging.Logger)
        display_completion_summary(
            "2024-01-01T12:00:00",
            LINKS,
            ["https://fail.com"],
            1,
            "/out",
            log_messages=LOG_MESSAGES,
            logger=logger,
        )
        for c in logger.info.call_args_list:
            assert c != call(LOG_MESSAGES["all_downloads_successful"])

    def test_logs_partial_downloaded_count(self):

        logger = MagicMock(spec=logging.Logger)
        display_completion_summary(
            "2024-01-01T12:00:00",
            LINKS,
            ["https://fail.com"],
            1,
            "/out",
            log_messages=LOG_MESSAGES,
            logger=logger,
        )
        logger.info.assert_any_call(
            LOG_MESSAGES["pages_downloaded"].format(downloaded_count=1, total_count=2)
        )

    def test_multiple_failures_each_logged_separately(self):

        failed = [f"https://fail{i}.com" for i in range(3)]
        logger = MagicMock(spec=logging.Logger)
        display_completion_summary(
            "2024-01-01T12:00:00",
            LINKS,
            failed,
            0,
            "/out",
            log_messages=LOG_MESSAGES,
            logger=logger,
        )
        error_calls = [str(c) for c in logger.error.call_args_list]
        url_calls = [c for c in error_calls if "fail" in c and "failed_count" not in c]
        assert len(url_calls) == 3
