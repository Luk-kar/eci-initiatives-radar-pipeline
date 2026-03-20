import pytest
from unittest.mock import MagicMock, patch
from selenium.common.exceptions import TimeoutException
from data_pipeline.scraper.initiatives.fetchers.ecis.waiter import wait_for_page_content

MODULE = "data_pipeline.scraper.initiatives.fetchers.ecis.waiter"

N_CONTENT_SELECTORS = 6


class TestWaitForPageContent:

    def test_returns_true_when_timeline_and_first_content_found(self, mock_driver):

        with patch(f"{MODULE}.WebDriverWait") as mock_wdw:
            mock_wdw.return_value.until.return_value = MagicMock()
            result = wait_for_page_content(mock_driver)

        assert result is True

    def test_returns_true_when_timeline_fails_but_first_content_found(
        self, mock_driver
    ):
        with patch(f"{MODULE}.WebDriverWait") as mock_wdw:
            mock_wdw.return_value.until.side_effect = [TimeoutException(), MagicMock()]
            result = wait_for_page_content(mock_driver)

        assert result is True

    def test_returns_true_on_second_content_selector(self, mock_driver):

        with patch(f"{MODULE}.WebDriverWait") as mock_wdw:

            mock_wdw.return_value.until.side_effect = [
                MagicMock(),  # timeline ok
                TimeoutException(),  # first content fails
                MagicMock(),  # second content succeeds
            ]
            result = wait_for_page_content(mock_driver)

        assert result is True

    def test_returns_false_when_timeline_found_but_all_content_fails(self, mock_driver):

        with patch(f"{MODULE}.WebDriverWait") as mock_wdw:
            mock_wdw.return_value.until.side_effect = [MagicMock()] + [
                TimeoutException()
            ] * N_CONTENT_SELECTORS
            result = wait_for_page_content(mock_driver)

        assert result is False

    def test_returns_false_when_all_selectors_fail(self, mock_driver):

        with patch(f"{MODULE}.WebDriverWait") as mock_wdw:
            mock_wdw.return_value.until.side_effect = TimeoutException()
            result = wait_for_page_content(mock_driver)

        assert result is False
