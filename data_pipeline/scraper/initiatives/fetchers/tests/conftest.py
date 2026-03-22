"""
Pytest configuration and shared fixtures for the fetchers test suite.

This module provides common mock objects and data structures used to
test the ECI listing and detail page fetchers, such as mocked Selenium
WebDrivers, fake HTML responses, and pre-configured temporary directories.
"""

import pytest
from selenium import webdriver

from unittest.mock import MagicMock


@pytest.fixture
def mock_driver():
    driver = MagicMock(spec=webdriver.Chrome)
    driver.page_source = "<html><body>content</body></html>"
    return driver
