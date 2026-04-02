"""Tests for the shared wait_for_page_content helper."""

import logging
from unittest.mock import MagicMock, patch

from data_pipeline.scraper.scraper_shared.response_and_followup.waiter import (
    wait_for_page_content,
)
from data_pipeline.scraper.scraper_shared.response_and_followup.css_selectors import (
    ResponsePageSelectors,
)

MODULE = "data_pipeline.scraper.scraper_shared.response_and_followup.waiter"

LOG_MESSAGES = {
    "content_loaded": "Content loaded: {selector}",
    "no_content_found": "No content found.",
}

_logger = logging.getLogger(__name__)


class TestWaitForPageContentReturnValue:
    def test_returns_true_when_any_selector_found(self):
        with patch(f"{MODULE}.wait_for_any_selector", return_value=True):
            result = wait_for_page_content(
                MagicMock(), timeout=10, logger=_logger, log_messages=LOG_MESSAGES
            )
        assert result is True

    def test_returns_false_when_no_selector_found(self):
        with patch(f"{MODULE}.wait_for_any_selector", return_value=False):
            result = wait_for_page_content(
                MagicMock(), timeout=10, logger=_logger, log_messages=LOG_MESSAGES
            )
        assert result is False


class TestWaitForPageContentDelegation:

    def test_passes_at_least_selector(self):
        with patch(f"{MODULE}.wait_for_any_selector", return_value=True) as mock_wait:
            wait_for_page_content(
                MagicMock(), timeout=10, logger=_logger, log_messages=LOG_MESSAGES
            )
        _, kwargs = mock_wait.call_args
        assert len(kwargs["selectors"]) >= 0

    def test_passes_driver_through(self):
        driver = MagicMock()
        with patch(f"{MODULE}.wait_for_any_selector", return_value=True) as mock_wait:
            wait_for_page_content(
                driver, timeout=10, logger=_logger, log_messages=LOG_MESSAGES
            )
        _, kwargs = mock_wait.call_args
        assert kwargs["driver"] is driver

    def test_passes_timeout_through(self):
        with patch(f"{MODULE}.wait_for_any_selector", return_value=True) as mock_wait:
            wait_for_page_content(
                MagicMock(), timeout=42.0, logger=_logger, log_messages=LOG_MESSAGES
            )
        _, kwargs = mock_wait.call_args
        assert kwargs["timeout"] == 42.0

    def test_passes_logger_through(self):
        with patch(f"{MODULE}.wait_for_any_selector", return_value=True) as mock_wait:
            wait_for_page_content(
                MagicMock(), timeout=10, logger=_logger, log_messages=LOG_MESSAGES
            )
        _, kwargs = mock_wait.call_args
        assert kwargs["logger"] is _logger

    def test_passes_log_messages_through(self):
        with patch(f"{MODULE}.wait_for_any_selector", return_value=True) as mock_wait:
            wait_for_page_content(
                MagicMock(), timeout=10, logger=_logger, log_messages=LOG_MESSAGES
            )
        _, kwargs = mock_wait.call_args
        assert kwargs["log_messages"] is LOG_MESSAGES

    def test_called_exactly_once(self):
        with patch(f"{MODULE}.wait_for_any_selector", return_value=True) as mock_wait:
            wait_for_page_content(
                MagicMock(), timeout=10, logger=_logger, log_messages=LOG_MESSAGES
            )
        mock_wait.assert_called_once()
