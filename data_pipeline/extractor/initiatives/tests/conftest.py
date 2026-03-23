"""
Pytest configuration for the initiatives extractor test suite.

Uses pytest_configure / pytest_unconfigure hooks — not a fixture — because
directories would otherwise be created during test *collection* (module
imports happen before any fixture is set up).

pytest_configure fires before collection, so the patches are active when
test modules import from data_pipeline for the first time.
"""

import shutil
import tempfile
from unittest.mock import patch

_EXTRACTOR_MAIN = "data_pipeline.extractor.initiatives.__main__"
_SHARED_CONSTS = "data_pipeline.pipeline_shared.consts"

_TMP_DIR = tempfile.mkdtemp(prefix="eci_extractor_test_")

_PATCHES = [
    patch(f"{_SHARED_CONSTS}.PIPELINE_DIR", _TMP_DIR),
    patch(f"{_SHARED_CONSTS}.DATA_DIR", f"{_TMP_DIR}/data"),
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
