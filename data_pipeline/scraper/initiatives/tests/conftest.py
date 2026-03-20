import pytest
from unittest.mock import MagicMock
from selenium import webdriver


@pytest.fixture
def mock_driver():
    driver = MagicMock(spec=webdriver.Chrome)
    driver.page_source = "<html><body>content</body></html>"
    return driver
