"""
Pytest configuration and shared fixtures for the initiatives scraper tests.

This module provides common test fixtures used across the initiatives scraper
test suite. It includes mock objects and reusable components, such as a mocked
Selenium WebDriver instance, to facilitate isolated testing of web scraping
functionality without requiring actual browser execution.
"""

# Python
from unittest.mock import MagicMock
from selenium import webdriver

# Third-party
import pytest


@pytest.fixture
def mock_driver():
    """Provide a mocked WebDriver for scraper tests."""

    driver = MagicMock(spec=webdriver.Chrome)
    driver.page_source = "<html><body>content</body></html>"
    return driver
