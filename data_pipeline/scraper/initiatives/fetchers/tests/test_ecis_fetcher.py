import pytest
from unittest.mock import MagicMock, patch
from data_pipeline.scraper.initiatives.fetchers.ecis.fetcher import (
    download_all_initiatives,
    download_single_initiative,
    _attempt_download,
)

MODULE = "data_pipeline.scraper.initiatives.fetchers.ecis.fetcher"
URL = "https://host/2023/000001_en"
FILENAME = "2023_000001_en.html"


# ── Shared fixtures ────────────────────────────────────────────────────────────


@pytest.fixture
def no_sleep():
    with patch(f"{MODULE}.time.sleep"), patch(
        f"{MODULE}.random.uniform", return_value=0.1
    ):
        yield


@pytest.fixture
def attempt_patches():
    with patch(f"{MODULE}.check_rate_limiting"), patch(
        f"{MODULE}.random.uniform", return_value=0.1
    ), patch(f"{MODULE}.time.sleep"):
        yield


# ── TestDownloadAllInitiatives ─────────────────────────────────────────────────


class TestDownloadAllInitiatives:

    def test_all_succeed_no_failed_urls(self, mock_driver, tmp_path, no_sleep):

        data = [
            {"url": URL, "datetime": ""},
            {"url": "https://host/2022/000002_en", "datetime": ""},
        ]
        with patch(f"{MODULE}.download_single_initiative", return_value=True):
            updated, failed = download_all_initiatives(mock_driver, str(tmp_path), data)

        assert failed == []
        assert len(updated) == 2
        assert all(row["datetime"] for row in updated)

    def test_failed_url_recorded_datetime_not_set(
        self, mock_driver, tmp_path, no_sleep
    ):
        data = [
            {"url": URL, "datetime": ""},
            {"url": "https://host/2022/000002_en", "datetime": ""},
        ]
        with patch(f"{MODULE}.download_single_initiative", side_effect=[True, False]):
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

    def test_preserves_existing_row_fields(self, mock_driver, tmp_path, no_sleep):

        data = [{"url": URL, "datetime": "", "title": "Test ECI"}]
        with patch(f"{MODULE}.download_single_initiative", return_value=True):
            updated, _ = download_all_initiatives(mock_driver, str(tmp_path), data)

        assert updated[0]["title"] == "Test ECI"


# ── TestDownloadSingleInitiative ───────────────────────────────────────────────


class TestDownloadSingleInitiative:

    @pytest.mark.parametrize(
        "retry_result,expected",
        [
            (True, True),
            (False, False),
        ],
    )
    def test_returns_retry_result(self, mock_driver, tmp_path, retry_result, expected):

        with patch(f"{MODULE}.download_with_retry", return_value=retry_result), patch(
            f"{MODULE}.random.uniform", return_value=0.1
        ):
            result = download_single_initiative(mock_driver, str(tmp_path), URL)
        assert result is expected

    def test_custom_max_retries_forwarded(self, mock_driver, tmp_path):

        with patch(
            f"{MODULE}.download_with_retry", return_value=True
        ) as mock_retry, patch(f"{MODULE}.random.uniform", return_value=0.1):
            download_single_initiative(mock_driver, str(tmp_path), URL, max_retries=3)
        assert mock_retry.call_args.kwargs["max_retries"] == 3


# ── TestAttemptDownload ────────────────────────────────────────────────────────


class TestAttemptDownload:

    def test_returns_filename_on_success(self, mock_driver, tmp_path, attempt_patches):

        with patch(f"{MODULE}.wait_for_page_content", return_value=True), patch(
            f"{MODULE}.save_initiative_page", return_value=FILENAME
        ):
            result = _attempt_download(mock_driver, str(tmp_path), URL)
        assert result == FILENAME

    def test_navigates_to_correct_url(self, mock_driver, tmp_path, attempt_patches):

        with patch(f"{MODULE}.wait_for_page_content", return_value=True), patch(
            f"{MODULE}.save_initiative_page", return_value=FILENAME
        ):
            _attempt_download(mock_driver, str(tmp_path), URL)
        mock_driver.get.assert_called_once_with(URL)

    def test_returns_true_when_download_succeeds(self, mock_driver, tmp_path):
        with patch(f"{MODULE}.download_with_retry", return_value=True), patch(
            f"{MODULE}.random.uniform", return_value=0.1
        ):
            assert download_single_initiative(mock_driver, str(tmp_path), URL) is True

    def test_returns_false_when_download_fails(self, mock_driver, tmp_path):
        with patch(f"{MODULE}.download_with_retry", return_value=False), patch(
            f"{MODULE}.random.uniform", return_value=0.1
        ):
            assert download_single_initiative(mock_driver, str(tmp_path), URL) is False

    def test_raises_when_rate_limited(self, mock_driver, tmp_path, attempt_patches):
        with patch(f"{MODULE}.check_rate_limiting", side_effect=Exception("429")):
            with pytest.raises(Exception, match="429"):
                _attempt_download(mock_driver, str(tmp_path), URL)
