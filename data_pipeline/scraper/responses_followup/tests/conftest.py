"""
Pytest configuration and shared fixtures for the responses test suite.

Uses pytest_configure / pytest_unconfigure hooks — not fixtures — so that
PIPELINE_DIR is patched before any test module imports consts.py and
freezes the path at collection time.
"""

import shutil
import tempfile
from unittest.mock import MagicMock, patch

import pytest
from selenium import webdriver

_RESPONSES_CONSTS = "data_pipeline.scraper.responses.consts"

_TMP_DIR = tempfile.mkdtemp(prefix="eci_responses_test_")

_PATCHES = [
    patch(f"{_RESPONSES_CONSTS}.PIPELINE_DIR", _TMP_DIR),
]


def pytest_configure(config):
    for p in _PATCHES:
        p.start()


def pytest_unconfigure(config):
    for p in _PATCHES:
        p.stop()
    shutil.rmtree(_TMP_DIR, ignore_errors=True)


@pytest.fixture
def mock_driver():
    driver = MagicMock(spec=webdriver.Chrome)
    driver.page_source = "<html><body>content</body></html>"
    return driver
