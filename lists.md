`./page_creator/partials/lists/currently_open.py`:
```
"""Renders a scrollable table of ECI initiatives currently open for signature collection."""

# Third-party
import pandas as pd

# Local
from page_creator.utils import wrap_card
from page_creator.partials.lists.utils import (
    build_table,
    progress_bar,
    sig_cell,
    threshold_cell,
    truncate,
    SCROLL_THRESHOLD,
)

_STATUS = "Collection Ongoing"
_HEADERS = ["Initiative", "Objective", "Days Left", "Signatures", "Countries Threshold"]


def _filter(df: pd.DataFrame) -> pd.DataFrame:
    """Filter for initiatives with ``_STATUS`` status.

    Args:
        df: The full ECI initiatives DataFrame.

    Returns:
        Filtered DataFrame containing only ``_STATUS`` rows.
    """
    return df[df["current_status"] == _STATUS].copy()


def _sort(df: pd.DataFrame) -> pd.DataFrame:
    """Sort open initiatives by start date ascending, with closed ones pushed last.

    Args:
        df: Filtered DataFrame of open initiatives.

    Returns:
        Sorted DataFrame with temporary helper columns dropped.
    """
    df["_start_dt"] = pd.to_datetime(
        df["timeline_collection_start"], dayfirst=True, errors="raise"
    )
    df["_has_closed"] = df["timeline_collection_closed"].notna() & (
        df["timeline_collection_closed"].str.strip() != ""
    )

    return (
        df.sort_values(["_has_closed", "_start_dt"], ascending=[True, True])
        .drop(columns=["_start_dt", "_has_closed"])
        .reset_index(drop=True)
    )


def _days_left_cell(date_start: str, date_closed: str) -> str:
    """Return a ``<td>`` element containing the JS-rendered days-left label and progress bar.

    Args:
        date_start:  Collection start date string (DD/MM/YYYY), or empty string.
        date_closed: Collection closed date string (DD/MM/YYYY), or empty string.

    Returns:
        A ``<td class="days-left-cell">`` HTML string.
    """
    if date_start:

        start_dt = pd.to_datetime(date_start, dayfirst=True, errors="coerce")
        deadline_dt = start_dt + pd.DateOffset(months=12)
        now_dt = pd.Timestamp.now()

        total_secs = (deadline_dt - start_dt).total_seconds()
        elapsed_secs = (now_dt - start_dt).total_seconds()

        pct = min(max(elapsed_secs / total_secs * 100, 0), 100)
        bar = progress_bar(pct, "days-left")
    else:
        bar = ""

    return (
        f'<td class="days-left-cell" data-start="{date_start}" data-closed="{date_closed}">'
        f'<span class="days-left-cell__label"></span>'
        f"{bar}"
        f"</td>"
    )


def _build_row(row: pd.Series) -> str:
    """Return a fully assembled ``<tr>`` for a single open initiative.

    Args:
        row: A DataFrame row. Must contain ``title``, ``url``, ``objective``,
             ``timeline_collection_start``, ``timeline_collection_closed``,
             ``signatures_collected``, and ``signatures_threshold_met``.

    Returns:
        A ``<tr>...</tr>`` HTML string.
    """
    url = row.get("url") or "#"
    objective = truncate(row.get("objective", ""))

    date_start = row.get("timeline_collection_start", "")
    date_closed = row.get("timeline_collection_closed", "")
    date_start = "" if pd.isna(date_start) else str(date_start).strip()
    date_closed = "" if pd.isna(date_closed) else str(date_closed).strip()

    return f"""
        <tr>
          <td><a href="{url}" target="_blank" rel="noopener noreferrer">{row["title"]}</a></td>
          <td>{objective}</td>
          {_days_left_cell(date_start, date_closed)}
          <td>{sig_cell(row["signatures_collected"])}</td>
          <td>{threshold_cell(row["signatures_threshold_met"])}</td>
        </tr>"""


def _build_rows(open_df: pd.DataFrame) -> str:
    """Iterate over all open initiatives and concatenate their row HTML.

    Args:
        open_df: Filtered and sorted DataFrame of open initiatives.

    Returns:
        Concatenated ``<tr>`` HTML string for all rows.
    """
    return "".join(_build_row(row) for _, row in open_df.iterrows())


def generate_currently_open(df: pd.DataFrame) -> str:
    """Return an HTML card containing a table of all currently open ECI initiatives.

    Filters for rows with ``current_status == 'Collection Ongoing'``, sorted by
    collection start date ascending, with closed initiatives pushed to the bottom.
    Each row shows the initiative title (linked to its page), a truncated objective,
    a JavaScript-rendered days-left cell, a signature progress bar, and a
    country-threshold progress bar.

    Args:
        df: The full ECI initiatives DataFrame. Must contain ``current_status``,
            ``title``, ``url``, ``objective``, ``signatures_collected``,
            ``signatures_threshold_met``, ``timeline_collection_start``, and
            ``timeline_collection_closed`` columns.

    Returns:
        An HTML string wrapping the table in a ``card`` div, or a card with a
        fallback message if no initiatives are currently open.
    """
    df_filter = _filter(df)
    df_open = _sort(df_filter)

    if df_open.empty:
        return wrap_card(
            "\n\nNo initiatives currently open for signature collection.\n\n"
        )

    title = f"\n\nCurrently Open ({len(df_open)})\n\n"
    body = build_table(
        _HEADERS, _build_rows(df_open), scrollable=len(df_open) > SCROLL_THRESHOLD
    )

    return wrap_card(title + body)

```

`./page_creator/partials/lists/got_response.py`:
```
"""Renders a scrollable table of ECI initiatives that received an EU Commission response."""

import pandas as pd

from page_creator.utils import wrap_card
from page_creator.partials.lists.utils import (
    build_initiative_row,
    normalise_registration_date,
    truncate,
    wrap_table_card,
)
from page_creator.partials.styles.colors import kpi_colors as colors

_RESPONSE_STATUSES = frozenset(
    ["Commission Engaged", "Law Passed", "Rejected Legislation"]
)
_HEADERS = ["Initiative", "Registration", "Objective", "Response"]


def _filter(df: pd.DataFrame) -> pd.DataFrame:
    """Filter for initiatives that received a Commission response.

    Args:
        df: The full ECI initiatives DataFrame.

    Returns:
        Filtered DataFrame containing only ``_RESPONSE_STATUSES`` rows.
    """
    return df[df["current_status"].isin(_RESPONSE_STATUSES)]


def _sort(df: pd.DataFrame) -> pd.DataFrame:
    """Normalise dates and sort by registration date descending.

    Args:
        df: Filtered DataFrame of initiatives with a Commission response.

    Returns:
        Sorted and date-normalised DataFrame.
    """
    return (
        normalise_registration_date(df)  # parse dates FIRST
        .sort_values("registration_date", ascending=False)
        .reset_index(drop=True)
    )


def _build_row(row: pd.Series) -> str:
    """Return a ``<tr>`` for a single initiative with a Commission response.

    Args:
        row: A DataFrame row. Must contain ``title``, ``url``, ``registration_date``,
             ``objective``, and ``commission_answer_text``.

    Returns:
        A ``<tr>...</tr>`` HTML string.
    """
    response = truncate(row["commission_answer_text"], max_len=200)
    return build_initiative_row(row, f"\n          <td>{response}</td>")


def _build_rows(filtered_df: pd.DataFrame) -> str:
    """Iterate over all matching initiatives and concatenate their row HTML.

    Args:
        filtered_df: Filtered and sorted DataFrame.

    Returns:
        Concatenated ``<tr>`` HTML string for all rows.
    """
    return "".join(_build_row(row) for _, row in filtered_df.iterrows())


def generate_got_response(df: pd.DataFrame) -> str:
    """Return an HTML card containing a table of ECIs that received a Commission response.

    Filters for rows with ``current_status`` in ``_RESPONSE_STATUSES``, sorted by
    registration date descending. Each row shows the initiative title (linked to
    its page), the registration date, a truncated objective, and the truncated
    commission response text.

    Args:
        df: The full ECI initiatives DataFrame. Must contain ``current_status``,
            ``title``, ``url``, ``objective``, ``registration_date``, and
            ``commission_answer_text`` columns.

    Returns:
        An HTML string wrapping the table in a ``card`` div, or a card with a
        fallback message if no initiatives received a response.
    """
    df_sorted = _filter(df)
    df_filtered = _sort(df_sorted)

    title = (
        '<h3 class="card__title">'
        "📬 Got EU Response: "
        f'<span class="card__count" style="color:{colors.got_response}">{len(df_filtered)}</span>'
        "</h3>"
    )

    if df_filtered.empty:
        body = '<p class="list-empty">No initiatives have received an EU Commission response.</p>'
        return wrap_card(title + body)

    return wrap_table_card(
        title, _build_rows(df_filtered), df_filtered, _HEADERS, colors.got_response
    )

```

`./page_creator/partials/lists/__init__.py`:
```
from .currently_open import generate_currently_open
from .got_response import generate_got_response
from .led_to_legislation import generate_led_to_legislation
from .reached_signatures import generate_reached_signatures
from .total_initiatives import generate_total_initiatives

__all__ = [
    "generate_currently_open",
    "generate_led_to_legislation",
    "generate_reached_signatures",
    "generate_total_initiatives",
]

```

`./page_creator/partials/lists/led_to_legislation.py`:
```
"""Renders a scrollable table of ECI initiatives that directly led to EU legislation."""

import pandas as pd

from page_creator.utils import wrap_card
from page_creator.partials.lists.utils import (
    build_initiative_row,
    normalise_registration_date,
    truncate,
    wrap_table_card,
)
from page_creator.partials.styles.colors import kpi_colors as colors

_STATUS = "Law Passed"
_HEADERS = ["Initiative", "Registration", "Objective", "Legislation Example"]


def _filter(df: pd.DataFrame) -> pd.DataFrame:
    """Filter for initiatives with ``Law Passed`` status.

    Args:
        df: The full ECI initiatives DataFrame.

    Returns:
        Filtered DataFrame containing only ``_STATUS`` rows.
    """
    return df[df["current_status"] == _STATUS]


def _sort(df: pd.DataFrame) -> pd.DataFrame:
    """Normalise dates and sort by registration date descending.

    Args:
        df: Filtered DataFrame of ``Law Passed`` initiatives.

    Returns:
        Sorted and date-normalised DataFrame.
    """
    return normalise_registration_date(
        df.sort_values("registration_date", ascending=False).reset_index(drop=True)
    )


def _build_row(row: pd.Series) -> str:
    """Return a ``<tr>`` for a single initiative that led to legislation.

    Args:
        row: A DataFrame row. Must contain ``title``, ``url``, ``registration_date``,
             ``objective``, and ``legislation``.

    Returns:
        A ``<tr>...</tr>`` HTML string.
    """
    legislation = truncate(row["legislation"])
    return build_initiative_row(row, f"\n          <td>{legislation}</td>")


def _build_rows(filtered_df: pd.DataFrame) -> str:
    """Iterate over all matching initiatives and concatenate their row HTML.

    Args:
        filtered_df: Filtered and sorted DataFrame.

    Returns:
        Concatenated ``<tr>`` HTML string for all rows.
    """
    return "".join(_build_row(row) for _, row in filtered_df.iterrows())


def generate_led_to_legislation(df: pd.DataFrame) -> str:
    """Return an HTML card containing a table of ECIs that led to passed legislation.

    Filters for rows with ``current_status == 'Law Passed'``, sorted by
    registration date descending.

    Args:
        df: The full ECI initiatives DataFrame. Must contain ``current_status``,
            ``title``, ``url``, ``objective``, ``registration_date``, and
            ``legislation`` columns.

    Returns:
        An HTML string wrapping the table in a ``card`` div, or a card with a
        fallback message if no initiatives led to legislation.
    """
    df_filtered = _filter(df)
    df_sorted = _sort(df_filtered)

    title = (
        '<h3 class="card__title">⚖️ Led to Legislation: '
        "<span "
        f'class="card__count" style="color:{colors.led_to_legislation}">{len(df_sorted)}'
        "</span>"
        "</h3>"
    )

    if df_sorted.empty:
        body = '<p class="list-empty">No initiatives have led to legislation yet.</p>'
        return wrap_card(title + body)

    return wrap_table_card(
        title,
        _build_rows(df_sorted),
        df_sorted,
        _HEADERS,
        colors.led_to_legislation,
    )

```

`./page_creator/partials/lists/reached_signatures.py`:
```
"""Renders a scrollable table of ECI initiatives that reached the 1M signature threshold."""

import pandas as pd

from page_creator.utils import wrap_card
from page_creator.partials.lists.utils import (
    normalise_registration_date,
    wrap_sig_threshold_card,
    SIG_TARGET,
)
from page_creator.partials.styles.colors import kpi_colors as colors


def _filter(df: pd.DataFrame) -> pd.DataFrame:
    """Filter for initiatives that reached 1M signatures.

    Args:
        df: The full ECI initiatives DataFrame.

    Returns:
        Filtered DataFrame where ``signatures_collected >= 1_000_000``.
    """
    return df[df["signatures_collected"] >= SIG_TARGET]


def _sort(df: pd.DataFrame) -> pd.DataFrame:
    """Normalise dates and sort by registration date descending.

    Args:
        df: Filtered DataFrame of initiatives that reached 1M signatures.

    Returns:
        Sorted and date-normalised DataFrame.
    """
    return normalise_registration_date(
        df.sort_values("registration_date", ascending=False).reset_index(drop=True)
    )


def generate_reached_signatures(df: pd.DataFrame) -> str:
    """Return an HTML card containing a table of ECIs that reached 1M signatures.

    Filters for rows where ``signatures_collected >= 1_000_000``, sorted by
    registration date descending. Each row shows the initiative title (linked to
    its page), the registration date, a truncated objective, a signature progress
    bar, and a country-threshold progress bar.

    Args:
        df: The full ECI initiatives DataFrame. Must contain ``signatures_collected``,
            ``title``, ``url``, ``objective``, ``registration_date``, and
            ``signatures_threshold_met`` columns.

    Returns:
        An HTML string wrapping the table in a ``card`` div, or a card with a
        fallback message if no initiatives reached the threshold.
    """
    df_filtered = _filter(df)
    df_sorted = _sort(df_filtered)

    title = (
        '<h3 class="card__title">'
        "✅ Reached 1M Signatures: "
        "<span "
        f'class="card__count" style="color:{colors.reached_signatures}">{len(df_sorted)}'
        "</span>"
        "</h3>"
    )

    if df_sorted.empty:
        body = '<p class="list-empty">No initiatives have reached 1M signatures.</p>'
        return wrap_card(title + body)

    return wrap_sig_threshold_card(title, df_sorted, colors.reached_signatures)

```

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

`./page_creator/partials/lists/total_initiatives.py`:
```
"""Renders a scrollable table of all registered ECI initiatives."""

import pandas as pd

from page_creator.partials.lists.utils import (
    normalise_registration_date,
    wrap_sig_threshold_card,
)
from page_creator.partials.styles.colors import kpi_colors as colors


def _sort(df: pd.DataFrame) -> pd.DataFrame:
    """Normalise dates and sort all initiatives by registration date descending.

    Args:
        df: The full ECI initiatives DataFrame.

    Returns:
        Full DataFrame sorted by ``registration_date`` descending.
    """
    return (
        normalise_registration_date(df)
        .sort_values("registration_date", ascending=False)
        .reset_index(drop=True)
    )


def generate_total_initiatives(df: pd.DataFrame) -> str:
    """Return an HTML card containing a table of all registered ECI initiatives.

    Sorted by registration date descending. Each row shows the initiative title
    (linked to its page), the registration date, a truncated objective, a signature
    progress bar towards the 1M target, and a country-threshold progress bar out of
    ``COUNTRIES_THRESHOLD``.

    Args:
        df: The full ECI initiatives DataFrame. Must contain ``title``, ``url``,
            ``objective``, ``registration_date``, ``signatures_collected``, and
            ``signatures_threshold_met`` columns.

    Returns:
        An HTML string wrapping the table in a ``card`` div.
    """
    sorted_df = _sort(df)

    title = (
        '<h3 class="card__title">📋 Total Initiatives: '
        "<span "
        f'class="card__count" style="color:{colors.total_initiatives}">{len(sorted_df)}'
        "</span>"
        "</h3>"
    )

    return wrap_sig_threshold_card(title, sorted_df, colors.total_initiatives)

```

`./page_creator/partials/lists/utils/constants.py`:
```
"""Shared numeric constants for ECI list partials."""

DEFAULT_TRUNCATE = 100
SCROLL_THRESHOLD = 5
SIG_TARGET = 1_000_000
COUNTRIES_THRESHOLD = 7

```

`./page_creator/partials/lists/utils/dates.py`:
```
"""Date normalisation helpers for list partials."""

import pandas as pd


def normalise_registration_date(df: pd.DataFrame) -> pd.DataFrame:
    """Parse and normalise the ``registration_date`` column to ``datetime.date``.

    Args:
        df: DataFrame with a ``registration_date`` column in ``DD/MM/YYYY`` format.

    Returns:
        The same DataFrame with ``registration_date`` converted to ``datetime.date``.
    """
    df = df.copy()
    df["registration_date"] = pd.to_datetime(
        df["registration_date"], format="%d/%m/%Y"
    ).dt.date
    return df

```

`./page_creator/partials/lists/utils/__init__.py`:
```
"""Shared HTML-generation helpers for list and table partials."""

from page_creator.partials.lists.utils.constants import (
    COUNTRIES_THRESHOLD,
    DEFAULT_TRUNCATE,
    SCROLL_THRESHOLD,
    SIG_TARGET,
)
from page_creator.partials.lists.utils.dates import normalise_registration_date
from page_creator.partials.lists.utils.progress import progress_bar
from page_creator.partials.lists.utils.rows import (
    HEADERS_WITH_SIGNATURES,
    build_initiative_row,
    build_sig_threshold_row,
    build_sig_threshold_rows,
    wrap_sig_threshold_card,
)
from page_creator.partials.lists.utils.signatures import sig_cell, threshold_cell
from page_creator.partials.lists.utils.table import build_table, wrap_table_card
from page_creator.partials.lists.utils.text import truncate

__all__ = [
    # constants
    "COUNTRIES_THRESHOLD",
    "DEFAULT_TRUNCATE",
    "SCROLL_THRESHOLD",
    "SIG_TARGET",
    # dates
    "normalise_registration_date",
    # progress
    "progress_bar",
    # rows
    "HEADERS_WITH_SIGNATURES",
    "build_initiative_row",
    "build_sig_threshold_row",
    "build_sig_threshold_rows",
    "wrap_sig_threshold_card",
    # signatures
    "sig_cell",
    "threshold_cell",
    # table
    "build_table",
    "wrap_table_card",
    # text
    "truncate",
]

```

`./page_creator/partials/lists/utils/progress.py`:
```
"""HTML progress bar builder for list partials."""


def progress_bar(pct: float, modifier: str = "") -> str:
    """Return an HTML progress bar div filled to ``pct``%,
    capped at 100% visually with an over-threshold colour class if exceeded.
    """
    clamped = min(max(pct, 0.0), 100.0)
    over = pct > 100.0
    mod_class = f" progress-bar__fill--{modifier}" if modifier else ""
    over_class = " progress-bar__fill--over" if over else ""
    return (
        f'<div class="progress-bar">'
        f'<div class="progress-bar__fill{mod_class}{over_class}" style="width:{clamped:.1f}%">'
        f"</div></div>"
    )

```

`./page_creator/partials/lists/utils/rows.py`:
```
"""Shared HTML row and cell builders for ECI initiative tables."""

import pandas as pd

from page_creator.partials.lists.utils.signatures import sig_cell, threshold_cell
from page_creator.partials.lists.utils.table import wrap_table_card
from page_creator.partials.lists.utils.text import truncate


# Shared column headers for tables that include signature and threshold columns
HEADERS_WITH_SIGNATURES = [
    "Initiative",
    "Registration",
    "Objective",
    "Signatures",
    "Countries Threshold",
]


def build_initiative_row(row: pd.Series, extra_cells: str = "") -> str:
    """Return a ``<tr>`` with the common Initiative / Registration / Objective cells.

    Args:
        row:         A DataFrame row. Must contain ``title``, ``url``,
                     ``registration_date``, and ``objective``.
        extra_cells: Additional ``<td>`` HTML appended after the three base cells.

    Returns:
        A ``<tr>...</tr>`` HTML string.
    """
    url = row.get("url") or "#"
    registration = row["registration_date"]
    objective = truncate(row.get("objective", ""))
    return f"""
        <tr>
          <td><a href="{url}" target="_blank" rel="noopener noreferrer">{row["title"]}</a></td>
          <td>{registration}</td>
          <td>{objective}</td>{extra_cells}
        </tr>"""


def build_sig_threshold_row(row: pd.Series) -> str:
    """Return a ``<tr>`` with Initiative / Registration / Objective / Signatures / Threshold cells.

    Shared by ``reached_signatures`` and ``total_initiatives`` which have identical
    row structure. Eliminates the duplicated ``_build_row`` in both modules.

    Args:
        row: A DataFrame row. Must contain ``title``, ``url``, ``registration_date``,
             ``objective``, ``signatures_collected``, and ``signatures_threshold_met``.

    Returns:
        A ``<tr>...</tr>`` HTML string.
    """
    extra = (
        f"\n          <td>{sig_cell(row['signatures_collected'])}</td>"
        f"\n          <td>{threshold_cell(row['signatures_threshold_met'])}</td>"
    )
    return build_initiative_row(row, extra)


def build_sig_threshold_rows(df: pd.DataFrame) -> str:
    """Iterate over a DataFrame and concatenate ``<tr>`` HTML for each row.

    Shared by ``reached_signatures`` and ``total_initiatives``.

    Args:
        df: DataFrame of initiatives. Each row is passed to ``build_sig_threshold_row``.

    Returns:
        Concatenated ``<tr>`` HTML string for all rows.
    """
    return "".join(build_sig_threshold_row(row) for _, row in df.iterrows())


def wrap_sig_threshold_card(
    title: str,
    df: pd.DataFrame,
    scrollbar_color: str,
) -> str:
    """Render a complete signatures+threshold card from a filtered DataFrame.

    Combines ``build_sig_threshold_rows`` and ``wrap_table_card`` into a single
    call. Eliminates the duplicated ``wrap_table_card(title, _build_rows(...), ...)``
    pattern in ``reached_signatures`` and ``total_initiatives``.

    Args:
        title:           HTML title string (e.g. ``<h3>…</h3>``).
        df:              Filtered and sorted DataFrame of initiatives.
        scrollbar_color: CSS colour value applied to the scroll wrapper.

    Returns:
        An HTML string wrapping everything in a ``card`` div.
    """
    return wrap_table_card(
        title,
        build_sig_threshold_rows(df),
        df,
        HEADERS_WITH_SIGNATURES,
        scrollbar_color,
    )

```

`./page_creator/partials/lists/utils/signatures.py`:
```
"""Signature and countries-threshold cell builders for ECI initiative tables."""

import pandas as pd

from page_creator.partials.lists.utils.constants import (
    SIG_TARGET,
    COUNTRIES_THRESHOLD,
)
from page_creator.partials.lists.utils.progress import progress_bar


def sig_cell(value) -> str:
    """Return formatted signatures cell content with progress bar, or ``Collection not started``.

    Args:
        value: Raw ``signatures_collected`` value from a DataFrame row.

    Returns:
        An HTML string for the signatures table cell content (without ``<td>`` tags).
    """
    if pd.notna(value):
        sig_val = int(value)
        return f"{sig_val:,}{progress_bar(sig_val / SIG_TARGET * 100, 'signatures')}"
    return "Collection not started"


def threshold_cell(value) -> str:
    """Return formatted countries-threshold cell content with progress bar, or ``Collection not started``.

    Args:
        value: Raw ``signatures_threshold_met`` value from a DataFrame row.

    Returns:
        An HTML string for the threshold table cell content (without ``<td>`` tags).
    """
    if pd.notna(value):
        thr_val = int(value)
        return (
            f"{thr_val} / {COUNTRIES_THRESHOLD}"
            f"{progress_bar(thr_val / COUNTRIES_THRESHOLD * 100, 'threshold')}"
        )
    return "Collection not started"

```

`./page_creator/partials/lists/utils/table.py`:
```
"""HTML table builder and card wrapper for list partials."""

from page_creator.utils import wrap_card
from page_creator.partials.lists.utils.constants import SCROLL_THRESHOLD


def build_table(
    headers: list[str],
    rows_html: str,
    scrollable: bool = False,
    scrollbar_color: str | None = None,
) -> str:
    """Return an HTML ``data-table`` string with a sticky header row,
    optionally wrapped in a scrollable container div.

    Args:
        headers:         Column header labels.
        rows_html:       Pre-rendered ``<tr>`` HTML string.
        scrollable:      Whether to wrap the table in a scroll container.
        scrollbar_color: Optional hex colour applied as ``--scrollbar-color``
                         CSS variable on the scroll wrapper.
    """
    header_cells = "\n      ".join(f"<th>{h}</th>" for h in headers)

    if scrollable:
        color_style = (
            f' style="--scrollbar-color:{scrollbar_color}"' if scrollbar_color else ""
        )
        wrapper_open = f'<div class="data-table__scroll-wrapper"{color_style}>'
        wrapper_close = "</div>"
    else:
        wrapper_open = ""
        wrapper_close = ""

    return f"""{wrapper_open}
<table class="data-table">
  <thead>
    <tr>
      {header_cells}
    </tr>
  </thead>
  <tbody>
    {rows_html}
  </tbody>
</table>
{wrapper_close}"""


def wrap_table_card(
    title: str,
    rows: str,
    df,
    headers: list[str],
    scrollbar_color: str,
) -> str:
    """Wrap a title and pre-rendered table rows in a scrollable card.

    Args:
        title:           HTML title string (e.g. ``<h3>…</h3>``).
        rows:            Concatenated ``<tr>`` HTML strings.
        df:              The filtered DataFrame, used to determine scroll threshold.
        headers:         Column header labels passed to ``build_table``.
        scrollbar_color: CSS colour value applied to the scroll wrapper.

    Returns:
        An HTML string wrapping everything in a ``card`` div.
    """
    return wrap_card(
        title
        + build_table(
            headers,
            rows,
            scrollable=len(df) > SCROLL_THRESHOLD,
            scrollbar_color=scrollbar_color,
        )
    )

```

`./page_creator/partials/lists/utils/text.py`:
```
"""Text formatting helpers for list partials."""

import pandas as pd

from page_creator.partials.lists.utils.constants import DEFAULT_TRUNCATE


def truncate(text: str, max_len: int = DEFAULT_TRUNCATE) -> str:
    """Truncate ``text`` to ``max_len`` characters, appending '…' if cut; returns '' for NaN."""
    if pd.isna(text):
        return ""
    s = str(text)
    return s if len(s) <= max_len else s[: max_len - 1] + "…"

```

