`./page_creator/partials/lists/tests/test_currently_open.py`:
```
"""Tests for _filter and _sort logic in currently_open.py."""

import pandas as pd
import pytest

from page_creator.partials.lists.currently_open import _filter, _sort


@pytest.fixture
def base_df():
    return pd.DataFrame(
        {
            "current_status": [
                "Collection Ongoing",
                "Collection Ongoing",
                "Collection Unsuccessful",
                "Law Passed",
                "Collection Ongoing",
            ],
            "title": ["A", "B", "C", "D", "E"],
            "timeline_collection_start": [
                "01/06/2024",
                "01/01/2024",
                "01/03/2023",
                "01/04/2022",
                "01/09/2024",
            ],
            "timeline_collection_closed": [None, None, None, None, "15/09/2025"],
            "signatures_collected": [500_000, 200_000, 800_000, 1_200_000, 300_000],
            "signatures_threshold_met": [5, 3, 8, 13, 2],
            "url": ["u1", "u2", "u3", "u4", "u5"],
            "objective": ["o1", "o2", "o3", "o4", "o5"],
        }
    )


class TestFilter:
    def test_keeps_only_collection_ongoing(self, base_df):
        result = _filter(base_df)
        assert set(result["current_status"].unique()) == {"Collection Ongoing"}

    def test_excludes_other_statuses(self, base_df):
        result = _filter(base_df)
        assert "Collection Unsuccessful" not in result["current_status"].values
        assert "Law Passed" not in result["current_status"].values

    def test_correct_row_count(self, base_df):
        assert len(_filter(base_df)) == 3

    def test_returns_copy_not_original(self, base_df):
        result = _filter(base_df)
        result.loc[result.index[0], "title"] = "MODIFIED"
        assert base_df.loc[0, "title"] == "A"

    def test_empty_input_returns_empty(self):
        df = pd.DataFrame(columns=["current_status", "title"])
        assert _filter(df).empty

    def test_all_other_statuses_returns_empty(self, base_df):
        df = base_df[base_df["current_status"] != "Collection Ongoing"].copy()
        assert _filter(df).empty


class TestSort:
    def test_open_without_closed_date_come_first(self, base_df):

        filtered = _filter(base_df)
        sorted_df = _sort(filtered)
        # E has a closed date — it must appear last
        assert sorted_df.iloc[-1]["title"] == "E"

    def test_open_initiatives_ordered_by_start_date_ascending(self, base_df):

        filtered = _filter(base_df)
        sorted_df = _sort(filtered)
        open_only = sorted_df[sorted_df["timeline_collection_closed"].isna()]
        start_dates = pd.to_datetime(
            open_only["timeline_collection_start"], dayfirst=True
        )
        assert start_dates.is_monotonic_increasing

    def test_helper_columns_not_in_result(self, base_df):

        result = _sort(_filter(base_df))
        assert "_start_dt" not in result.columns
        assert "_has_closed" not in result.columns

    def test_index_is_reset(self, base_df):

        result = _sort(_filter(base_df))
        assert list(result.index) == list(range(len(result)))

    def test_all_rows_preserved_after_sort(self, base_df):

        filtered = _filter(base_df)
        sorted_df = _sort(filtered)
        assert len(sorted_df) == len(filtered)

    def test_single_row_unchanged(self):

        df = pd.DataFrame(
            {
                "current_status": ["Collection Ongoing"],
                "title": ["Only"],
                "timeline_collection_start": ["10/10/2024"],
                "timeline_collection_closed": [None],
                "signatures_collected": [100_000],
                "signatures_threshold_met": [1],
                "url": ["u"],
                "objective": ["o"],
            }
        )
        result = _sort(df)
        assert len(result) == 1
        assert result.iloc[0]["title"] == "Only"

```

`./page_creator/partials/lists/tests/test_got_response.py`:
```
"""Tests for _filter and _sort logic in got_response.py."""

import datetime

import pandas as pd
import pytest

from page_creator.partials.lists.got_response import _filter, _sort, _RESPONSE_STATUSES


@pytest.fixture
def base_df():
    return pd.DataFrame(
        {
            "current_status": [
                "Commission Engaged",
                "Rejected Legislation",
                "Law Passed",
                "Collection Unsuccessful",
                "Collection Ongoing",
                "Withdrawn",
                "Commission Engaged",
            ],
            "title": ["A", "B", "C", "D", "E", "F", "G"],
            "registration_date": [
                "01/03/2019",
                "01/06/2017",
                "15/11/2021",
                "01/01/2015",
                "10/05/2023",
                "20/08/2016",
                "05/02/2020",
            ],
            "url": [f"u{i}" for i in range(7)],
            "objective": [f"o{i}" for i in range(7)],
            "commission_answer_text": [f"ans{i}" for i in range(7)],
        }
    )


class TestFilter:
    def test_keeps_only_response_statuses(self, base_df):

        result = _filter(base_df)
        assert set(result["current_status"].unique()).issubset(_RESPONSE_STATUSES)

    def test_excludes_non_response_statuses(self, base_df):
        result = _filter(base_df)
        for excluded in ("Collection Unsuccessful", "Collection Ongoing", "Withdrawn"):
            assert excluded not in result["current_status"].values

    def test_correct_row_count(self, base_df):

        assert (
            len(_filter(base_df)) == 4
        )  # types: "Commission Engaged", "Rejected Legislation", "Law Passed"

    def test_empty_input_returns_empty(self):

        df = pd.DataFrame(columns=["current_status"])
        assert _filter(df).empty

    def test_all_excluded_statuses_returns_empty(self, base_df):

        df = base_df[~base_df["current_status"].isin(_RESPONSE_STATUSES)].copy()
        assert _filter(df).empty

    def test_response_statuses_constant_contents(self):

        assert _RESPONSE_STATUSES == frozenset(
            {"Commission Engaged", "Law Passed", "Rejected Legislation"}
        )


class TestSort:
    def test_sorted_by_registration_date_descending(self, base_df):

        result = _sort(_filter(base_df))
        dates = result["registration_date"].tolist()
        assert dates == sorted(dates, reverse=True)

    def test_registration_date_is_date_type(self, base_df):

        result = _sort(_filter(base_df))
        assert all(isinstance(d, datetime.date) for d in result["registration_date"])

    def test_index_is_reset(self, base_df):

        result = _sort(_filter(base_df))
        assert list(result.index) == list(range(len(result)))

    def test_row_count_unchanged_after_sort(self, base_df):

        filtered = _filter(base_df)
        assert len(_sort(filtered)) == len(filtered)

    def test_most_recent_first(self, base_df):

        result = _sort(_filter(base_df))
        # "C" (Law Passed) has 15/11/2021 — the most recent among the three
        assert result.iloc[0]["title"] == "C"

```

`./page_creator/partials/lists/tests/test_led_to_legislation.py`:
```
"""Tests for _filter and _sort logic in led_to_legislation.py."""

import datetime

import pandas as pd
import pytest

from page_creator.partials.lists.led_to_legislation import _filter, _sort


@pytest.fixture
def base_df():
    return pd.DataFrame(
        {
            "current_status": [
                "Law Passed",
                "Law Passed",
                "Commission Engaged",
                "Rejected Legislation",
                "Collection Unsuccessful",
            ],
            "title": ["A", "B", "C", "D", "E"],
            "registration_date": [
                "10/04/2018",
                "01/01/2015",
                "05/06/2019",
                "20/03/2017",
                "11/11/2020",
            ],
            "url": [f"u{i}" for i in range(5)],
            "objective": [f"o{i}" for i in range(5)],
            "legislation": [
                "Directive (EU) 2020/1234 adopted.",
                "Regulation (EU) 2016/5678 adopted.",
                None,
                None,
                None,
            ],
        }
    )


class TestFilter:
    def test_keeps_only_law_passed(self, base_df):

        result = _filter(base_df)
        assert set(result["current_status"].unique()) == {"Law Passed"}

    def test_excludes_other_statuses(self, base_df):

        result = _filter(base_df)
        for excluded in (
            "Commission Engaged",
            "Rejected Legislation",
            "Collection Unsuccessful",
        ):
            assert excluded not in result["current_status"].values

    def test_correct_row_count(self, base_df):

        assert len(_filter(base_df)) == 2

    def test_empty_input_returns_empty(self):

        df = pd.DataFrame(columns=["current_status"])
        assert _filter(df).empty

    def test_no_law_passed_rows_returns_empty(self, base_df):

        df = base_df[base_df["current_status"] != "Law Passed"].copy()
        assert _filter(df).empty


class TestSort:
    def test_sorted_by_registration_date_descending(self, base_df):

        result = _sort(_filter(base_df))
        dates = result["registration_date"].tolist()
        assert dates == sorted(dates, reverse=True)

    def test_registration_date_is_date_type(self, base_df):

        result = _sort(_filter(base_df))
        assert all(isinstance(d, datetime.date) for d in result["registration_date"])

    def test_index_is_reset(self, base_df):

        result = _sort(_filter(base_df))
        assert list(result.index) == list(range(len(result)))

    def test_most_recent_first(self, base_df):

        # "A" registered 10/04/2018 > "B" registered 01/01/2015
        result = _sort(_filter(base_df))
        assert result.iloc[0]["title"] == "A"

    def test_legislation_column_preserved(self, base_df):

        result = _sort(_filter(base_df))
        assert "legislation" in result.columns
        assert result.iloc[0]["legislation"] is not None

```

`./page_creator/partials/lists/tests/test_reached_signatures.py`:
```
"""Tests for _filter and _sort logic in reached_signatures.py."""

import datetime

import pandas as pd
import pytest

from page_creator.partials.lists.reached_signatures import _filter, _sort
from page_creator.partials.lists.utils import SIG_TARGET


@pytest.fixture
def base_df():
    return pd.DataFrame(
        {
            "current_status": [
                "Commission Engaged",
                "Rejected Legislation",
                "Commission Engaged",
                "Collection Unsuccessful",
                "Law Passed",
            ],
            "title": ["A", "B", "C", "D", "E"],
            "registration_date": [
                "01/01/2013",
                "01/01/2015",
                "01/01/2019",
                "01/01/2020",
                "01/01/2017",
            ],
            "signatures_collected": [
                1_884_790,  # above threshold
                1_173_130,  # above threshold
                800_000,  # below threshold
                236_000,  # below threshold
                1_050_000,  # above threshold
            ],
            "signatures_threshold_met": [13, 11, 3, 2, 7],
            "url": [f"u{i}" for i in range(5)],
            "objective": [f"o{i}" for i in range(5)],
        }
    )


class TestFilter:
    def test_keeps_only_rows_above_sig_target(self, base_df):

        result = _filter(base_df)
        assert all(result["signatures_collected"] >= SIG_TARGET)

    def test_excludes_rows_below_sig_target(self, base_df):

        result = _filter(base_df)
        assert "C" not in result["title"].values
        assert "D" not in result["title"].values

    def test_correct_row_count(self, base_df):

        assert len(_filter(base_df)) == 3

    def test_empty_input_returns_empty(self):

        df = pd.DataFrame(columns=["signatures_collected"])
        assert _filter(df).empty

    def test_all_below_threshold_returns_empty(self, base_df):

        df = base_df[base_df["signatures_collected"] < SIG_TARGET].copy()
        assert _filter(df).empty

    def test_exact_sig_target_is_included(self):

        df = pd.DataFrame(
            {
                "signatures_collected": [SIG_TARGET],
                "title": ["Exact"],
                "registration_date": ["01/01/2020"],
            }
        )
        assert len(_filter(df)) == 1

    def test_one_below_sig_target_is_excluded(self):

        df = pd.DataFrame(
            {
                "signatures_collected": [SIG_TARGET - 1],
                "title": ["AlmostThere"],
                "registration_date": ["01/01/2020"],
            }
        )
        assert _filter(df).empty


class TestSort:
    def test_sorted_by_registration_date_descending(self, base_df):

        result = _sort(_filter(base_df))
        dates = result["registration_date"].tolist()
        assert dates == sorted(dates, reverse=True)

    def test_registration_date_is_date_type(self, base_df):

        result = _sort(_filter(base_df))
        assert all(isinstance(d, datetime.date) for d in result["registration_date"])

    def test_index_is_reset(self, base_df):

        result = _sort(_filter(base_df))
        assert list(result.index) == list(range(len(result)))

    def test_most_recent_first(self, base_df):

        # E has 01/01/2017, A has 01/01/2013, B has 01/01/2015 → E is most recent
        result = _sort(_filter(base_df))
        assert result.iloc[0]["title"] == "E"

    def test_row_count_unchanged_after_sort(self, base_df):

        filtered = _filter(base_df)
        assert len(_sort(filtered)) == len(filtered)

```

`./page_creator/partials/lists/tests/test_total_initiatives.py`:
```
"""Tests for _sort logic in total_initiatives.py."""

import datetime

import pandas as pd
import pytest

from page_creator.partials.lists.total_initiatives import _sort


@pytest.fixture
def base_df():
    return pd.DataFrame(
        {
            "current_status": [
                "Collection Ongoing",
                "Law Passed",
                "Rejected Legislation",
                "Collection Unsuccessful",
                "Withdrawn",
            ],
            "title": ["A", "B", "C", "D", "E"],
            "registration_date": [
                "15/03/2023",
                "01/01/2015",
                "20/07/2019",
                "10/10/2012",
                "05/05/2017",
            ],
            "signatures_collected": [300_000, 1_200_000, 1_100_000, 500_000, None],
            "signatures_threshold_met": [3, 13, 10, 4, None],
            "url": [f"u{i}" for i in range(5)],
            "objective": [f"o{i}" for i in range(5)],
        }
    )


class TestSort:
    def test_no_rows_filtered_out(self, base_df):

        result = _sort(base_df)
        assert len(result) == len(base_df)

    def test_all_statuses_present(self, base_df):

        result = _sort(base_df)
        assert set(result["current_status"]) == set(base_df["current_status"])

    def test_sorted_by_registration_date_descending(self, base_df):

        result = _sort(base_df)
        dates = result["registration_date"].tolist()
        assert dates == sorted(dates, reverse=True)

    def test_registration_date_is_date_type(self, base_df):

        result = _sort(base_df)
        assert all(isinstance(d, datetime.date) for d in result["registration_date"])

    def test_most_recent_first(self, base_df):

        # "A" registered 15/03/2023 is the most recent
        result = _sort(base_df)
        assert result.iloc[0]["title"] == "A"

    def test_oldest_last(self, base_df):

        # "D" registered 10/10/2012 is the oldest
        result = _sort(base_df)
        assert result.iloc[-1]["title"] == "D"

    def test_index_is_reset(self, base_df):

        result = _sort(base_df)
        assert list(result.index) == list(range(len(result)))

    def test_does_not_mutate_original(self, base_df):

        original_dates = base_df["registration_date"].tolist()
        _sort(base_df)
        assert base_df["registration_date"].tolist() == original_dates

    def test_null_signatures_rows_preserved(self, base_df):

        result = _sort(base_df)
        assert result["signatures_collected"].isna().sum() == 1

    def test_single_row_unchanged(self):
        df = pd.DataFrame(
            {
                "title": ["Solo"],
                "registration_date": ["01/06/2021"],
                "current_status": ["Withdrawn"],
                "signatures_collected": [50_000],
                "signatures_threshold_met": [1],
                "url": ["u"],
                "objective": ["o"],
            }
        )
        result = _sort(df)
        assert len(result) == 1
        assert isinstance(result.iloc[0]["registration_date"], datetime.date)

    def test_null_signatures_renders_collection_not_started(self):
        df = pd.DataFrame(
            {
                "title": ["No Sigs"],
                "registration_date": ["01/06/2021"],
                "current_status": ["Collection Ongoing"],
                "signatures_collected": [None],
                "signatures_threshold_met": [None],
                "url": ["u"],
                "objective": ["o"],
            }
        )
        result = _sort(df)
        assert pd.isna(result.iloc[0]["signatures_collected"])
        assert pd.isna(result.iloc[0]["signatures_threshold_met"])

    def test_zero_signatures_does_not_render_collection_not_started(self):
        df = pd.DataFrame(
            {
                "title": ["Zero Sigs"],
                "registration_date": ["01/06/2021"],
                "current_status": ["Collection Ongoing"],
                "signatures_collected": [0],
                "signatures_threshold_met": [0],
                "url": ["u"],
                "objective": ["o"],
            }
        )
        result = _sort(df)
        assert result.iloc[0]["signatures_collected"] == 0
        assert result.iloc[0]["signatures_threshold_met"] == 0

```

