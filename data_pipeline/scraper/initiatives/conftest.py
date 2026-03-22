"""
Pytest configuration for the initiatives test suite.

Uses pytest_configure / pytest_unconfigure hooks — not a fixture — because
directories would otherwise be created during test *collection* (module
imports happen before any fixture is set up).

pytest_configure fires before collection, so the patches are active when
test modules import _logger.py for the first time.
"""

import shutil
import tempfile
from unittest.mock import patch

_INITIATIVES_CONSTS = "data_pipeline.scraper.initiatives.consts"

# Created once when this conftest is loaded; cleaned up in pytest_unconfigure.
_TMP_DIR = tempfile.mkdtemp(prefix="eci_test_")

# Patcher objects — .start() / .stop() called by the hooks below.
_PATCHES = [
    patch(f"{_INITIATIVES_CONSTS}.LOG_DIR", f"{_TMP_DIR}/logs"),
    patch(f"{_INITIATIVES_CONSTS}.PIPELINE_DIR", _TMP_DIR),
]


def pytest_configure(config):
    """Start path patches before any test module is imported."""
    for p in _PATCHES:
        p.start()


def pytest_unconfigure(config):
    """Stop patches and delete the temp tree after the session ends."""
    for p in _PATCHES:
        p.stop()
    shutil.rmtree(_TMP_DIR, ignore_errors=True)
