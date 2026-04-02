import pytest

from bs4 import BeautifulSoup

from data_pipeline.extractor.responses.extractor.parser.fields.followup_details import (
    extract_followup_additional_website,
)


def _soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")


class TestMatchingUrls:

    @pytest.mark.parametrize(
        "href",
        [
            "https://food.ec.europa.eu/animals/animal-welfare/eci/eci-end-cage-age_en",
            "https://food.ec.europa.eu/animals/animal-welfare/eci/eci-fur-free-europe_en",
            "https://ec.europa.eu/info/law/better-regulation/have-your-say/initiatives/eci/eci-water_en",
            "https://EXAMPLE.COM/eci/eci-animal-welfare_en",  # case-insensitive scheme
        ],
    )
    def test_returns_matching_dedicated_website(self, href):
        soup = _soup(f'<p>See the <a href="{href}">dedicated website</a>.</p>')
        assert extract_followup_additional_website(soup, "2020/000001") == href

    def test_returns_first_match_when_multiple_present(self):
        first = (
            "https://food.ec.europa.eu/animals/animal-welfare/eci/eci-end-cage-age_en"
        )
        second = "https://example.com/eci/eci-fur-free-europe_en"
        soup = _soup(
            f'<p><a href="{first}">first</a></p>'
            f'<p><a href="{second}">second</a></p>'
        )
        assert extract_followup_additional_website(soup, "2020/000001") == first


class TestNonMatchingUrls:

    @pytest.mark.parametrize(
        "href, reason",
        [
            (
                "https://example.com/eci/eci-something_de",
                "wrong language suffix",
            ),
            (
                "https://example.com/citizens-initiative_en",
                "missing eci/ path segment",
            ),
            (
                "https://example.com/eci/eci-something_en/extra",
                "extra path after _en",
            ),
            (
                "http://example.com/eci/eci-something_en",
                "http instead of https",
            ),
            (
                "https://example.com/eci/something_en",
                "missing eci- prefix on identifier",
            ),
            (
                "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32019R1381",
                "unrelated external link",
            ),
            (
                "https://ec.europa.eu/commission/presscorner/detail/en/ip_21_3297",
                "press release link",
            ),
        ],
    )
    def test_returns_none_for_non_matching_url(self, href, reason):
        soup = _soup(f'<p><a href="{href}">link</a></p>')
        assert extract_followup_additional_website(soup, "2019/000016") is None, reason

    def test_returns_none_when_no_links_present(self):
        soup = _soup("<p>No links here.</p>")
        assert extract_followup_additional_website(soup, "2019/000016") is None

    def test_returns_none_for_empty_soup(self):
        soup = _soup("")
        assert extract_followup_additional_website(soup, "2019/000016") is None

    def test_skips_anchor_with_empty_href(self):
        valid = (
            "https://food.ec.europa.eu/animals/animal-welfare/eci/eci-end-cage-age_en"
        )
        soup = _soup(f'<a href="">empty</a>' f'<a href="{valid}">dedicated</a>')
        assert extract_followup_additional_website(soup, "2020/000001") == valid

    def test_skips_anchor_without_href(self):
        valid = (
            "https://food.ec.europa.eu/animals/animal-welfare/eci/eci-end-cage-age_en"
        )
        soup = _soup(f'<a name="anchor">no href</a>' f'<a href="{valid}">dedicated</a>')
        assert extract_followup_additional_website(soup, "2020/000001") == valid


class TestEdgeCases:

    @pytest.mark.parametrize(
        "registration_number, href",
        [
            (
                "2018/000004",
                "https://food.ec.europa.eu/animals/animal-welfare/eci/eci-end-cage-age_en",
            ),
            (
                "2022/000002",
                "https://food.ec.europa.eu/animals/animal-welfare/eci/eci-fur-free-europe_en",
            ),
        ],
    )
    def test_real_world_dedicated_website(
        self, registration_number, href, eci_fixture_soup
    ):
        """Verify extraction against actual fixture HTML."""
        soup = eci_fixture_soup(registration_number)
        assert extract_followup_additional_website(soup, registration_number) == href

    @pytest.mark.parametrize(
        "registration_number",
        [
            "2012/000003",
            "2012/000005",
            "2012/000007",
            "2019/000007",
        ],
    )
    def test_real_world_no_dedicated_website(
        self, registration_number, eci_fixture_soup
    ):
        """Initiatives without a dedicated follow-up website return None."""
        soup = eci_fixture_soup(registration_number)
        assert extract_followup_additional_website(soup, registration_number) is None
