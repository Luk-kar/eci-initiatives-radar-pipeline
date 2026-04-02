"""
Tests for Commission response follow-up page HTML save operations.
"""

from unittest.mock import patch

MODULE_SHARED = (
    "data_pipeline.scraper.scraper_shared" ".response_and_followup.file_operations.page"
)


def test_import_succeeds():
    from data_pipeline.scraper.responses_followup.file_operations.page import (
        save_response_page,
    )

    assert callable(save_response_page)


def test_delegates_to_shared_implementation(tmp_path):
    from data_pipeline.scraper.responses_followup.file_operations.page import (
        save_response_page,
    )

    with patch(f"{MODULE_SHARED}.validate_html"), patch(
        f"{MODULE_SHARED}.save_html"
    ) as mock_save, patch(f"{MODULE_SHARED}.ensure_dirs"):
        save_response_page(str(tmp_path), "2023", "000007", "<html/>")

    mock_save.assert_called_once()
