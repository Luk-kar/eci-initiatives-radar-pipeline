import pytest
from unittest.mock import MagicMock, patch
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from data_pipeline.scraper.initiatives.fetchers.listings.page_ops import (
    navigate_to_next_page,
    wait_for_listing_page_content,
    load_listing_url,
    save_debug_listing_page,
)

MODULE = "data_pipeline.scraper.initiatives.fetchers.listings.page_ops"


class TestNavigateToNextPage:

    def test_returns_true_and_clicks_next_button(self, mock_driver):

        mock_button = MagicMock()
        mock_driver.find_element.return_value = mock_button
        with patch(f"{MODULE}.time.sleep"), patch(
            f"{MODULE}.random.uniform", return_value=0.1
        ):
            result = navigate_to_next_page(mock_driver, current_page=1)

        assert result is True
        mock_driver.execute_script.assert_called_once_with(
            "arguments[0].click();", mock_button
        )

    def test_returns_false_when_next_button_absent(self, mock_driver):

        mock_driver.find_element.side_effect = NoSuchElementException()
        with patch(f"{MODULE}.time.sleep"), patch(
            f"{MODULE}.random.uniform", return_value=0.1
        ):
            result = navigate_to_next_page(mock_driver, current_page=3)

        assert result is False


class TestWaitForListingPageContent:

    def test_no_exception_when_content_found(self, mock_driver):

        with patch(f"{MODULE}.WebDriverWait") as mock_wdw, patch(
            f"{MODULE}.check_rate_limiting"
        ), patch(f"{MODULE}.random.uniform", return_value=0.1), patch(
            f"{MODULE}.time.sleep"
        ):
            mock_wdw.return_value.until.return_value = MagicMock()
            wait_for_listing_page_content(mock_driver, current_page=1)

    def test_no_exception_on_timeout_without_rate_limiting(self, mock_driver):

        with patch(f"{MODULE}.WebDriverWait") as mock_wdw, patch(
            f"{MODULE}.check_rate_limiting"
        ):
            mock_wdw.return_value.until.side_effect = TimeoutException()
            wait_for_listing_page_content(mock_driver, current_page=2)

    def test_propagates_exception_on_rate_limit(self, mock_driver):

        with patch(f"{MODULE}.WebDriverWait") as mock_wdw, patch(
            f"{MODULE}.check_rate_limiting",
            side_effect=Exception("Rate limiting detected"),
        ):
            mock_wdw.return_value.until.side_effect = TimeoutException()
            with pytest.raises(Exception, match="Rate limiting"):
                wait_for_listing_page_content(mock_driver, current_page=1)


class TestLoadListingUrl:

    def test_calls_driver_get_with_url(self, mock_driver):

        url = "https://example.com/find-initiative_en"
        with patch(f"{MODULE}.check_rate_limiting"), patch(
            f"{MODULE}.random.uniform", return_value=0.1
        ), patch(f"{MODULE}.time.sleep"):
            load_listing_url(mock_driver, url)

        mock_driver.get.assert_called_once_with(url)

    def test_check_rate_limiting_called_after_get(self, mock_driver):

        url = "https://example.com/find-initiative_en"
        call_order = []
        mock_driver.get.side_effect = lambda u: call_order.append("get")
        with patch(
            f"{MODULE}.check_rate_limiting",
            side_effect=lambda d: call_order.append("check"),
        ), patch(f"{MODULE}.random.uniform", return_value=0.1), patch(
            f"{MODULE}.time.sleep"
        ):
            load_listing_url(mock_driver, url)

        assert call_order == ["get", "check"]

    def test_raises_when_rate_limited(self, mock_driver):

        with patch(
            f"{MODULE}.check_rate_limiting", side_effect=Exception("429")
        ), patch(f"{MODULE}.random.uniform", return_value=0.1), patch(
            f"{MODULE}.time.sleep"
        ):
            with pytest.raises(Exception, match="429"):
                load_listing_url(mock_driver, "https://example.com/find-initiative_en")


class TestSaveDebugListingPage:

    def test_creates_file_in_debug_subdirectory(self, tmp_path):

        list_dir = tmp_path / "listings"
        list_dir.mkdir()
        filename = save_debug_listing_page(
            str(list_dir), current_page=1, page_source="<html/>"
        )
        assert (tmp_path / "debugging" / "listings" / filename).exists()

    def test_written_content_matches_page_source(self, tmp_path):

        list_dir = tmp_path / "listings"
        list_dir.mkdir()
        page_source = "<html>test content</html>"
        filename = save_debug_listing_page(
            str(list_dir), current_page=2, page_source=page_source
        )
        content = (tmp_path / "debugging" / "listings" / filename).read_text(
            encoding="utf-8"
        )
        assert content == page_source

    def test_filename_encodes_page_number(self, tmp_path):

        list_dir = tmp_path / "listings"
        list_dir.mkdir()
        filename = save_debug_listing_page(
            str(list_dir), current_page=5, page_source="<html/>"
        )
        assert "005" in filename
