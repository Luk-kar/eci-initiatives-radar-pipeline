"""
Tests for ECI detail page synchronization utilities.

This module validates the explicit wait logic used to ensure dynamic
content is fully loaded on individual initiative pages. It tests the handling
of successful element locations, fallback mechanisms for missing content,
and timeout scenarios across various page selectors.
"""

from unittest.mock import MagicMock, patch

from selenium.common.exceptions import TimeoutException

from data_pipeline.scraper.initiatives.fetchers.ecis.waiter import wait_for_page_content

WAIT_UTILS = "data_pipeline.scraper.scraper_shared.wait_utils"

N_CONTENT_SELECTORS = 6


class TestWaitForPageContent:
    """
    Test suite for dynamic page content synchronization.

    Validates that the waiter function correctly probes for the primary
    initiative timeline and gracefully falls back to checking secondary
    content selectors. It ensures the function returns True when content
    is eventually found, and False when all selectors exhaust their timeouts.
    """

    def test_returns_true_when_timeline_and_first_content_found(self, mock_driver):

        with patch(f"{WAIT_UTILS}.WebDriverWait") as mock_wdw:
            mock_wdw.return_value.until.return_value = MagicMock()
            result = wait_for_page_content(mock_driver)

        assert result is True

    def test_returns_true_when_timeline_fails_but_first_content_found(
        self, mock_driver
    ):
        with patch(f"{WAIT_UTILS}.WebDriverWait") as mock_wdw:
            mock_wdw.return_value.until.side_effect = [TimeoutException(), MagicMock()]
            result = wait_for_page_content(mock_driver)

        assert result is True

    def test_returns_true_on_second_content_selector(self, mock_driver):

        with patch(f"{WAIT_UTILS}.WebDriverWait") as mock_wdw:

            mock_wdw.return_value.until.side_effect = [
                MagicMock(),  # timeline ok
                TimeoutException(),  # first content fails
                MagicMock(),  # second content succeeds
            ]
            result = wait_for_page_content(mock_driver)

        assert result is True

    def test_returns_false_when_timeline_found_but_all_content_fails(self, mock_driver):

        with patch(f"{WAIT_UTILS}.WebDriverWait") as mock_wdw:
            mock_wdw.return_value.until.side_effect = [MagicMock()] + [
                TimeoutException()
            ] * N_CONTENT_SELECTORS
            result = wait_for_page_content(mock_driver)

        assert result is False

    def test_returns_false_when_all_selectors_fail(self, mock_driver):

        with patch(f"{WAIT_UTILS}.WebDriverWait") as mock_wdw:
            mock_wdw.return_value.until.side_effect = TimeoutException()
            result = wait_for_page_content(mock_driver)

        assert result is False
