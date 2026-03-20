import pytest
import os

from unittest.mock import MagicMock, patch
from data_pipeline.scraper.initiatives.fetchers.listings.fetcher import (
    scrape_all_listings,
    scrape_single_listing_page,
    save_main_listing_page,
)

MODULE = "data_pipeline.scraper.initiatives.fetchers.listings.fetcher"
BASE_URL = "https://citizens-initiative.europa.eu"
ROUTE = "/find-initiative_en"


def _fake_retry_calls_attempt(attempt_fn, **kwargs):
    attempt_fn()
    return True


class TestScrapeAllListings:

    def test_returns_empty_when_first_page_fails(self, mock_driver, tmp_path):

        with patch(f"{MODULE}._fetch_first_listing_page", return_value=False):
            data, paths = scrape_all_listings(mock_driver, BASE_URL, str(tmp_path))

        assert data == []
        assert paths == []

    def test_single_page_no_next_button(self, mock_driver, tmp_path):

        fake_data = [{"url": "https://host/2023/000001_en"}]
        with patch(f"{MODULE}._fetch_first_listing_page", return_value=True), patch(
            f"{MODULE}.scrape_single_listing_page", return_value=(fake_data, "/p1.html")
        ), patch(f"{MODULE}.navigate_to_next_page", return_value=False):
            data, paths = scrape_all_listings(mock_driver, BASE_URL, str(tmp_path))

        assert data == fake_data
        assert paths == ["/p1.html"]

    def test_multi_page_collects_all_data_and_paths(self, mock_driver, tmp_path):

        page1 = [{"url": "https://host/2023/000001_en"}]
        page2 = [{"url": "https://host/2022/000002_en"}]
        with patch(f"{MODULE}._fetch_first_listing_page", return_value=True), patch(
            f"{MODULE}.scrape_single_listing_page",
            side_effect=[
                (page1, "/p1.html"),
                (page2, "/p2.html"),
            ],
        ), patch(f"{MODULE}.navigate_to_next_page", side_effect=[True, False]):
            data, paths = scrape_all_listings(mock_driver, BASE_URL, str(tmp_path))

        assert len(data) == 2
        assert paths == ["/p1.html", "/p2.html"]


class TestScrapeSingleListingPage:

    def test_returns_data_and_path_on_success(self, mock_driver, tmp_path):

        fake_initiatives = [{"url": "https://host/2023/000001_en"}]
        with patch(
            f"{MODULE}.download_with_retry", side_effect=_fake_retry_calls_attempt
        ), patch(f"{MODULE}.check_rate_limiting"), patch(
            f"{MODULE}.wait_for_listing_page_content"
        ), patch(
            f"{MODULE}.save_listing_page", return_value=("source_html", "/p1.html")
        ), patch(
            f"{MODULE}.parse_initiatives_list_data", return_value=fake_initiatives
        ), patch(
            f"{MODULE}.random.uniform", return_value=0.1
        ):
            data, path = scrape_single_listing_page(
                mock_driver, BASE_URL, str(tmp_path), 1, BASE_URL + ROUTE
            )

        assert data == fake_initiatives
        assert path == "/p1.html"

    def test_returns_empty_on_failure(self, mock_driver, tmp_path):

        with patch(f"{MODULE}.download_with_retry", return_value=False), patch(
            f"{MODULE}.random.uniform", return_value=0.1
        ):
            data, path = scrape_single_listing_page(
                mock_driver, BASE_URL, str(tmp_path), 1, BASE_URL + ROUTE
            )

        assert data == []
        assert path == ""

    def test_parse_called_with_correct_base_url(self, mock_driver, tmp_path):

        with patch(
            f"{MODULE}.download_with_retry", side_effect=_fake_retry_calls_attempt
        ), patch(f"{MODULE}.check_rate_limiting"), patch(
            f"{MODULE}.wait_for_listing_page_content"
        ), patch(
            f"{MODULE}.save_listing_page", return_value=("source", "/p1.html")
        ), patch(
            f"{MODULE}.parse_initiatives_list_data", return_value=[]
        ) as mock_parse, patch(
            f"{MODULE}.random.uniform", return_value=0.1
        ):
            scrape_single_listing_page(
                mock_driver, BASE_URL, str(tmp_path), 1, BASE_URL + ROUTE
            )

        mock_parse.assert_called_once_with("source", BASE_URL)


class TestSaveMainListingPage:

    def test_returns_source_and_path_on_success(self, mock_driver, tmp_path):

        with patch(
            f"{MODULE}.download_with_retry", side_effect=_fake_retry_calls_attempt
        ), patch(f"{MODULE}.load_listing_url"), patch(
            f"{MODULE}.WebDriverWait"
        ) as mock_wdw, patch(
            f"{MODULE}.check_rate_limiting"
        ), patch(
            f"{MODULE}.random.uniform", return_value=0.1
        ):
            mock_wdw.return_value.until.return_value = MagicMock()
            source, path = save_main_listing_page(mock_driver, BASE_URL, str(tmp_path))

        assert source != ""
        assert path != ""

    def test_returns_empty_strings_on_failure(self, mock_driver, tmp_path):

        with patch(f"{MODULE}.download_with_retry", return_value=False), patch(
            f"{MODULE}.random.uniform", return_value=0.1
        ):
            source, path = save_main_listing_page(mock_driver, BASE_URL, str(tmp_path))

        assert source == ""
        assert path == ""

    def test_saved_file_exists_on_success(self, mock_driver, tmp_path):

        with patch(
            f"{MODULE}.download_with_retry", side_effect=_fake_retry_calls_attempt
        ), patch(f"{MODULE}.load_listing_url"), patch(
            f"{MODULE}.WebDriverWait"
        ) as mock_wdw, patch(
            f"{MODULE}.check_rate_limiting"
        ), patch(
            f"{MODULE}.random.uniform", return_value=0.1
        ):
            mock_wdw.return_value.until.return_value = MagicMock()
            _, path = save_main_listing_page(mock_driver, BASE_URL, str(tmp_path))

        assert path != "" and os.path.exists(path)
