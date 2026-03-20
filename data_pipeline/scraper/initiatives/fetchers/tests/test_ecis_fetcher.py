import pytest
from unittest.mock import MagicMock, patch
from data_pipeline.scraper.initiatives.fetchers.ecis.fetcher import (
    download_all_initiatives,
    download_single_initiative,
    _attempt_download,
)

MODULE = "data_pipeline.scraper.initiatives.fetchers.ecis.fetcher"


class TestDownloadAllInitiatives:

    def test_all_succeed_no_failed_urls(self, mock_driver, tmp_path):
        data = [
            {"url": "https://host/2023/000001_en", "datetime": ""},
            {"url": "https://host/2022/000002_en", "datetime": ""},
        ]
        with patch(f"{MODULE}.download_single_initiative", return_value=True), patch(
            f"{MODULE}.random.uniform", return_value=0.1
        ), patch(f"{MODULE}.time.sleep"):
            updated, failed = download_all_initiatives(mock_driver, str(tmp_path), data)

        assert failed == []
        assert len(updated) == 2
        assert all(row["datetime"] for row in updated)

    def test_failed_url_recorded_datetime_not_set(self, mock_driver, tmp_path):
        data = [
            {"url": "https://host/2023/000001_en", "datetime": ""},
            {"url": "https://host/2022/000002_en", "datetime": ""},
        ]
        with patch(
            f"{MODULE}.download_single_initiative", side_effect=[True, False]
        ), patch(f"{MODULE}.random.uniform", return_value=0.1), patch(
            f"{MODULE}.time.sleep"
        ):
            updated, failed = download_all_initiatives(mock_driver, str(tmp_path), data)

        assert failed == ["https://host/2022/000002_en"]
        assert updated[0]["datetime"] != ""
        assert updated[1]["datetime"] == ""

    def test_empty_data_returns_empty_lists(self, mock_driver, tmp_path):
        with patch(f"{MODULE}.download_single_initiative") as mock_dl, patch(
            f"{MODULE}.time.sleep"
        ):
            updated, failed = download_all_initiatives(mock_driver, str(tmp_path), [])

        assert updated == []
        assert failed == []
        mock_dl.assert_not_called()

    def test_preserves_all_existing_row_fields(self, mock_driver, tmp_path):
        data = [
            {"url": "https://host/2023/000001_en", "datetime": "", "title": "Test ECI"}
        ]
        with patch(f"{MODULE}.download_single_initiative", return_value=True), patch(
            f"{MODULE}.random.uniform", return_value=0.1
        ), patch(f"{MODULE}.time.sleep"):
            updated, _ = download_all_initiatives(mock_driver, str(tmp_path), data)

        assert updated[0]["title"] == "Test ECI"


class TestDownloadSingleInitiative:

    def test_returns_true_on_success(self, mock_driver, tmp_path):
        with patch(f"{MODULE}.download_with_retry", return_value=True), patch(
            f"{MODULE}.random.uniform", return_value=0.1
        ):
            result = download_single_initiative(
                mock_driver, str(tmp_path), "https://host/2023/000001_en"
            )
        assert result is True

    def test_returns_false_when_all_retries_fail(self, mock_driver, tmp_path):
        with patch(f"{MODULE}.download_with_retry", return_value=False), patch(
            f"{MODULE}.random.uniform", return_value=0.1
        ):
            result = download_single_initiative(
                mock_driver, str(tmp_path), "https://host/2023/000001_en"
            )
        assert result is False

    def test_custom_max_retries_forwarded(self, mock_driver, tmp_path):
        with patch(
            f"{MODULE}.download_with_retry", return_value=True
        ) as mock_retry, patch(f"{MODULE}.random.uniform", return_value=0.1):
            download_single_initiative(
                mock_driver, str(tmp_path), "https://host/2023/000001_en", max_retries=3
            )
        assert mock_retry.call_args.kwargs["max_retries"] == 3


class TestAttemptDownload:

    def test_returns_filename_on_success(self, mock_driver, tmp_path):
        with patch(f"{MODULE}.check_rate_limiting"), patch(
            f"{MODULE}.wait_for_page_content", return_value=True
        ), patch(
            f"{MODULE}.save_initiative_page", return_value="2023_000001_en.html"
        ), patch(
            f"{MODULE}.random.uniform", return_value=0.1
        ), patch(
            f"{MODULE}.time.sleep"
        ):
            result = _attempt_download(
                mock_driver, str(tmp_path), "https://host/2023/000001_en"
            )

        assert result == "2023_000001_en.html"

    def test_navigates_to_correct_url(self, mock_driver, tmp_path):
        url = "https://host/2023/000001_en"
        with patch(f"{MODULE}.check_rate_limiting"), patch(
            f"{MODULE}.wait_for_page_content", return_value=True
        ), patch(
            f"{MODULE}.save_initiative_page", return_value="2023_000001_en.html"
        ), patch(
            f"{MODULE}.random.uniform", return_value=0.1
        ), patch(
            f"{MODULE}.time.sleep"
        ):
            _attempt_download(mock_driver, str(tmp_path), url)

        mock_driver.get.assert_called_once_with(url)

    def test_debug_true_when_content_not_found(self, mock_driver, tmp_path):
        with patch(f"{MODULE}.check_rate_limiting"), patch(
            f"{MODULE}.wait_for_page_content", return_value=False
        ), patch(
            f"{MODULE}.save_initiative_page", return_value="2023_000001_en.html"
        ) as mock_save, patch(
            f"{MODULE}.random.uniform", return_value=0.1
        ), patch(
            f"{MODULE}.time.sleep"
        ):
            _attempt_download(mock_driver, str(tmp_path), "https://host/2023/000001_en")

        assert mock_save.call_args.kwargs["debug"] is True

    def test_debug_false_when_content_found(self, mock_driver, tmp_path):
        with patch(f"{MODULE}.check_rate_limiting"), patch(
            f"{MODULE}.wait_for_page_content", return_value=True
        ), patch(
            f"{MODULE}.save_initiative_page", return_value="2023_000001_en.html"
        ) as mock_save, patch(
            f"{MODULE}.random.uniform", return_value=0.1
        ), patch(
            f"{MODULE}.time.sleep"
        ):
            _attempt_download(mock_driver, str(tmp_path), "https://host/2023/000001_en")

        assert mock_save.call_args.kwargs["debug"] is False

    def test_raises_when_rate_limited(self, mock_driver, tmp_path):
        with patch(
            f"{MODULE}.check_rate_limiting",
            side_effect=Exception("429 - Too Many Requests"),
        ), patch(f"{MODULE}.random.uniform", return_value=0.1), patch(
            f"{MODULE}.time.sleep"
        ):
            with pytest.raises(Exception, match="429"):
                _attempt_download(
                    mock_driver, str(tmp_path), "https://host/2023/000001_en"
                )
