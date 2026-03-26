"""
Tests for Chrome WebDriver initialisation in the Commission responses scraper.

Validates that initialize_browser delegates correctly to the shared
browser initialiser, passing the module logger and LOG_MESSAGES.
"""

from unittest.mock import call, patch

import pytest

from data_pipeline.scraper.responses.browser import initialize_browser

MODULE = "data_pipeline.scraper.responses.browser"


class TestInitializeBrowser:
    """
    Validates that initialize_browser delegates to the shared initialiser
    with the correct logger and log_messages arguments.
    """

    def test_delegates_to_shared_initializer(self):

        with patch(f"{MODULE}._shared_initialize_browser") as mock_init:
            initialize_browser()

        mock_init.assert_called_once()

    def test_returns_driver_from_shared_initializer(self):

        with patch(f"{MODULE}._shared_initialize_browser") as mock_init:
            result = initialize_browser()

        assert result is mock_init.return_value
