`./page_creator/partials/lists/awaiting_response.py`:
```
"""Renders a scrollable table of ECI initiatives no longer in active collection."""

import pandas as pd

from page_creator.utils import wrap_card
from page_creator.partials.lists.utils import (
    normalise_registration_date,
    wrap_sig_threshold_card,
)
from page_creator.partials.styles.colors import kpi_colors as colors
from page_creator.partials.lists.utils.sort import sort_by_registration_date

_STATUS = "Awaiting Response"


def _filter(df: pd.DataFrame) -> pd.DataFrame:
    """Filter for initiatives that are no longer in active collection.

    Args:
        df: The full ECI initiatives DataFrame.

    Returns:
        Filtered DataFrame containing only ``_STATUS`` rows.
    """
    return df[df["current_status"] == "Waiting for Response"]


def _sort(df: pd.DataFrame) -> pd.DataFrame:
    """Normalise dates and sort by registration date descending.

    Args:
        df: Filtered DataFrame of closed-collection initiatives.

    Returns:
        Sorted and date-normalised DataFrame.
    """
    return sort_by_registration_date(df)


def generate_awaiting_response(df: pd.DataFrame) -> str:
    """Return an HTML card containing a table of ECIs no longer in active collection.

    Filters for rows with ``current_status`` in ``_STATUSES``, sorted by
    registration date descending. Each row shows the initiative title (linked to
    its page), the registration date, a truncated objective, a signature progress
    bar, and a country-threshold progress bar.

    Args:
        df: The full ECI initiatives DataFrame. Must contain ``current_status``,
            ``title``, ``url``, ``objective``, ``registration_date``,
            ``signatures_collected``, and ``signatures_threshold_met`` columns.

    Returns:
        An HTML string wrapping the table in a ``card`` div, or a card with a
        fallback message if no initiatives match.
    """
    df_filtered = _filter(df)
    df_sorted = _sort(df_filtered)
    df_final = normalise_registration_date(df_sorted)

    title = (
        '<h3 class="card__title">'
        f"⌛ {_STATUS}: "
        f'<span class="card__count" style="color:{colors.awaiting_response}">{len(df_final)}</span>'
        "</h3>"
    )

    if df_final.empty:
        body = '<p class="list-empty">No closed-collection initiatives found.</p>'
        return wrap_card(title + body)

    return wrap_sig_threshold_card(title, df_final, colors.awaiting_response)

```

`./page_creator/partials/lists/collection_ongoing.py`:
```
"""Renders a scrollable table of ECI initiatives Collection Ongoing for signature collection."""

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
from page_creator.partials.styles.colors import kpi_colors as colors

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


def generate_collection_ongoing(df: pd.DataFrame) -> str:
    """Return an HTML card containing a table of all Collection Ongoing ECI initiatives.

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
        fallback message if no initiatives are collection ongoing.
    """
    df_filter = _filter(df)
    df_open = _sort(df_filter)

    if df_open.empty:
        return wrap_card(
            "\n\nNo initiatives collection ongoing for signature collection.\n\n"
        )

    title = (
        '<h3 class="card__title">🗳️ Collection Ongoing:'
        "<span "
        f'class="card__count" style="color:{colors.collection_ongoing}">{len(df_open)}'
        "</span>"
        "</h3>"
    )

    body = build_table(
        _HEADERS, _build_rows(df_open), scrollable=len(df_open) > SCROLL_THRESHOLD
    )

    return wrap_card(title + body)

```

`./page_creator/partials/lists/collection_unsuccessful.py`:
```
"""Renders a scrollable table of ECI initiatives no longer in active collection."""

import pandas as pd

from page_creator.utils import wrap_card
from page_creator.partials.lists.utils import (
    normalise_registration_date,
    wrap_sig_threshold_card,
)
from page_creator.partials.styles.colors import kpi_colors as colors
from page_creator.partials.lists.utils.sort import sort_by_registration_date

_STATUS = "Collection Unsuccessful"


def _filter(df: pd.DataFrame) -> pd.DataFrame:
    """Filter for initiatives that are no longer in active collection.

    Args:
        df: The full ECI initiatives DataFrame.

    Returns:
        Filtered DataFrame containing only ``_STATUS`` rows.
    """
    return df[
        df["current_status"] == "Collection Unsuccessful"
    ]  # Renamed: "Collection Unsuccessful"


def _sort(df: pd.DataFrame) -> pd.DataFrame:
    """Normalise dates and sort by registration date descending.

    Args:
        df: Filtered DataFrame of closed-collection initiatives.

    Returns:
        Sorted and date-normalised DataFrame.
    """
    return sort_by_registration_date(df)


def generate_collection_unsuccessful(df: pd.DataFrame) -> str:
    """Return an HTML card containing a table of ECIs no longer in active collection.

    Filters for rows with ``current_status`` in ``_STATUSES``, sorted by
    registration date descending. Each row shows the initiative title (linked to
    its page), the registration date, a truncated objective, a signature progress
    bar, and a country-threshold progress bar.

    Args:
        df: The full ECI initiatives DataFrame. Must contain ``current_status``,
            ``title``, ``url``, ``objective``, ``registration_date``,
            ``signatures_collected``, and ``signatures_threshold_met`` columns.

    Returns:
        An HTML string wrapping the table in a ``card`` div, or a card with a
        fallback message if no initiatives match.
    """
    df_filtered = _filter(df)
    df_sorted = _sort(df_filtered)
    df_final = normalise_registration_date(df_sorted)

    title = (
        '<h3 class="card__title">'
        f"🏳️ {_STATUS}: "
        "<span "
        f'class="card__count" style="color:{colors.collection_unsuccessful}">{len(df_final)}'
        "</span>"
        "</h3>"
    )

    if df_final.empty:
        body = '<p class="list-empty">No closed-collection initiatives found.</p>'
        return wrap_card(title + body)

    return wrap_sig_threshold_card(title, df_final, colors.collection_unsuccessful)

```

`./page_creator/partials/lists/commission_engaged.py`:
```
"""Renders a scrollable table of ECI initiatives that directly led to EU legislation."""

import pandas as pd

from page_creator.partials.styles.colors import kpi_colors as colors
from page_creator.partials.lists.utils.sort import sort_by_registration_date
from page_creator.partials.lists.utils import (
    generate_response_card,
)

_STATUS = "Commission Engaged"
_HEADERS = ["Initiative", "Registration", "Objective", "Commission Response"]


def _filter(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["current_status"] == _STATUS]


def _sort(df: pd.DataFrame) -> pd.DataFrame:
    return sort_by_registration_date(df)


def generate_commission_engaged(df: pd.DataFrame) -> str:
    """
    generate commission engaged table
    """

    color = colors.commission_engaged
    df_sorted = _sort(_filter(df))
    title = (
        f'<h3 class="card__title">🏛️ {_STATUS}: '
        f'<span class="card__count" style="color:{color}">{len(df_sorted)}</span>'
        "</h3>"
    )
    return generate_response_card(
        df_sorted,
        title,
        _HEADERS,
        color,
        empty_message="No initiatives have engaged the Commission yet.",
    )

```

`./page_creator/partials/lists/got_response.py`:
```
"""Renders a scrollable table of ECI initiatives that received an EU Commission response."""

import pandas as pd

from page_creator.partials.styles.colors import kpi_colors as colors
from page_creator.partials.lists.utils.sort import sort_by_registration_date
from page_creator.partials.lists.utils import generate_response_card

_RESPONSE_STATUSES = frozenset(
    ["Commission Engaged", "Law Passed", "Rejected Legislation"]
)
_HEADERS = ["Initiative", "Registration", "Objective", "Response"]


def _filter(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["current_status"].isin(_RESPONSE_STATUSES)]


def _sort(df: pd.DataFrame) -> pd.DataFrame:
    return sort_by_registration_date(df)


def generate_got_response(df: pd.DataFrame) -> str:
    """
    Generating got response table
    """

    color = colors.got_response
    df_sorted = _sort(_filter(df))
    title = (
        '<h3 class="card__title">'
        "📬 Got EU Response: "
        f'<span class="card__count" style="color:{color}">{len(df_sorted)}</span>'
        "</h3>"
    )
    return generate_response_card(
        df_sorted,
        title,
        _HEADERS,
        color,
        empty_message="No initiatives have received an EU Commission response.",
    )

```

`./page_creator/partials/lists/__init__.py`:
```
from .collection_ongoing import generate_collection_ongoing
from .got_response import generate_got_response
from .law_passed import generate_law_passed
from .reached_signatures import generate_reached_signatures
from .total_initiatives import generate_total_initiatives
from .awaiting_response import generate_awaiting_response
from .collection_unsuccessful import generate_collection_unsuccessful
from .commission_engaged import generate_commission_engaged
from .rejected_legislation import generate_rejected_legislation
from .withdrawn import generate_withdrawn

__all__ = [
    "generate_collection_ongoing",
    "generate_law_passed",
    "generate_reached_signatures",
    "generate_total_initiatives",
    "generate_awaiting_response",
    "generate_collection_unsuccessful",
    "generate_commission_engaged",
    "generate_rejected_legislation",
    "generate_withdrawn",
]

```

`./page_creator/partials/lists/law_passed.py`:
```
"""Renders a scrollable table of ECI initiatives that directly led to EU legislation."""

import pandas as pd

from page_creator.utils import wrap_card
from page_creator.partials.lists.utils import (
    normalise_registration_date,
    build_initiative_row,
    truncate,
    wrap_table_card,
)
from page_creator.partials.styles.colors import kpi_colors as colors
from page_creator.partials.lists.utils.sort import sort_by_registration_date

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

    return sort_by_registration_date(df)


def _build_row(row: pd.Series) -> str:
    """Return a ``<tr>`` for a single initiative that law passed.

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


def generate_law_passed(df: pd.DataFrame) -> str:
    """Return an HTML card containing a table of ECIs that led to passed legislation.

    Filters for rows with ``current_status == 'Law Passed'``, sorted by
    registration date descending.

    Args:
        df: The full ECI initiatives DataFrame. Must contain ``current_status``,
            ``title``, ``url``, ``objective``, ``registration_date``, and
            ``legislation`` columns.

    Returns:
        An HTML string wrapping the table in a ``card`` div, or a card with a
        fallback message if no initiatives law passed.
    """
    df_filtered = _filter(df)
    df_sorted = _sort(df_filtered)
    df_final = normalise_registration_date(df_sorted)

    title = (
        '<h3 class="card__title">⚖️ Law Passed: '
        "<span "
        f'class="card__count" style="color:{colors.law_passed}">{len(df_final)}'
        "</span>"
        "</h3>"
    )

    if df_final.empty:
        body = '<p class="list-empty">No initiatives have law_passed yet.</p>'
        return wrap_card(title + body)

    return wrap_table_card(
        title,
        _build_rows(df_final),
        df_final,
        _HEADERS,
        colors.law_passed,
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
from page_creator.partials.lists.utils.sort import sort_by_registration_date


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

    return sort_by_registration_date(df)


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
    df_final = normalise_registration_date(df_sorted)

    title = (
        '<h3 class="card__title">'
        "✅ Reached 1M Signatures: "
        "<span "
        f'class="card__count" style="color:{colors.reached_signatures}">{len(df_final)}'
        "</span>"
        "</h3>"
    )

    if df_final.empty:
        body = '<p class="list-empty">No initiatives have reached 1M signatures.</p>'
        return wrap_card(title + body)

    return wrap_sig_threshold_card(title, df_final, colors.reached_signatures)

```

`./page_creator/partials/lists/rejected_legislation.py`:
```
"""Renders a scrollable table of ECI initiatives that directly led to EU legislation."""

import pandas as pd

from page_creator.partials.styles.colors import kpi_colors as colors
from page_creator.partials.lists.utils.sort import sort_by_registration_date
from page_creator.partials.lists.utils import generate_response_card

_STATUS = "Rejected Legislation"
_HEADERS = ["Initiative", "Registration", "Objective", "Response"]


def _filter(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["current_status"] == _STATUS]


def _sort(df: pd.DataFrame) -> pd.DataFrame:
    return sort_by_registration_date(df)


def generate_rejected_legislation(df: pd.DataFrame) -> str:
    """
    Generate rejected legislation table
    """

    color = colors.rejected_legislation
    df_sorted = _sort(_filter(df))
    title = (
        f'<h3 class="card__title">❌ {_STATUS}: '
        f'<span class="card__count" style="color:{color}">{len(df_sorted)}</span>'
        "</h3>"
    )
    return generate_response_card(
        df_sorted,
        title,
        _HEADERS,
        color,
        empty_message="No initiatives have been rejected yet.",
    )

```

`./page_creator/partials/lists/tests/law_passed.py`:
```
"""Tests for _filter and _sort logic in law passed.py."""

import datetime

import pandas as pd
import pytest

from page_creator.partials.lists.law_passed import _filter, _sort


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

`./page_creator/partials/lists/tests/test_collection_ongoing.py`:
```
"""Tests for _filter and _sort logic in collection_ongoing.py."""

import pandas as pd
import pytest

from page_creator.partials.lists.collection_ongoing import _filter, _sort


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
from page_creator.partials.lists.utils.sort import sort_by_registration_date


def _sort(df: pd.DataFrame) -> pd.DataFrame:
    """Normalise dates and sort all initiatives by registration date descending.

    Args:
        df: The full ECI initiatives DataFrame.

    Returns:
        Full DataFrame sorted by ``registration_date`` descending.
    """

    return sort_by_registration_date(df)


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
    df_sorted = _sort(df)
    df_final = normalise_registration_date(df_sorted)

    title = (
        '<h3 class="card__title">📋 Total Initiatives: '
        "<span "
        f'class="card__count" style="color:{colors.total_initiatives}">{len(df_final)}'
        "</span>"
        "</h3>"
    )

    return wrap_sig_threshold_card(title, df_final, colors.total_initiatives)

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
    """Parse and normalise the ``registration_date`` column to a human-readable string.

    Args:
        df: DataFrame with a ``registration_date`` column in ``DD/MM/YYYY`` format.

    Returns:
        The same DataFrame with ``registration_date`` converted to ``'1 Jan 2024'`` format.
    """
    df = df.copy()
    df["registration_date"] = pd.to_datetime(
        df["registration_date"], format="%d/%m/%Y"
    ).dt.strftime("%-d %b %Y")
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
    build_response_row,
    build_response_rows,
    generate_response_card,
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
    "build_response_row",
    "build_response_rows",
    "generate_response_card",
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
from page_creator.partials.lists.utils.dates import normalise_registration_date
from page_creator.utils import wrap_card

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


def build_response_row(row: pd.Series) -> str:
    """Return a ``<tr>`` for an initiative with a truncated Commission response cell.

    Shared by ``commission_engaged``, ``rejected_legislation``, and ``got_response``.

    Args:
        row: Must contain ``title``, ``url``, ``registration_date``,
             ``objective``, and ``commission_answer_text``.

    Returns:
        A ``<tr>...</tr>`` HTML string.
    """
    response = truncate(row["commission_answer_text"], max_len=200)
    return build_initiative_row(row, f"\n          <td>{response}</td>")


def build_response_rows(df: pd.DataFrame) -> str:
    """Iterate over a DataFrame and concatenate response ``<tr>`` HTML for each row."""
    return "".join(build_response_row(row) for _, row in df.iterrows())


def generate_response_card(
    df: pd.DataFrame,
    title: str,
    headers: list[str],
    color: str,
    empty_message: str,
) -> str:
    """Run the standard filter→sort→normalise→render pipeline for response-type lists.

    Shared by ``commission_engaged``, ``rejected_legislation``, and ``got_response``.

    Args:
        df:            Already-filtered and sorted DataFrame (normalise not yet applied).
        title:         Pre-rendered ``<h3>`` HTML title string.
        headers:       Column header labels.
        color:         CSS colour for the scrollbar.
        empty_message: Fallback ``<p>`` message text when ``df`` is empty.

    Returns:
        An HTML string wrapping the table in a ``card`` div.
    """

    df_final = normalise_registration_date(df)

    if df_final.empty:
        return wrap_card(title + f'<p class="list-empty">{empty_message}</p>')

    return wrap_table_card(
        title, build_response_rows(df_final), df_final, headers, color
    )


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
    """
    Return formatted countries-threshold cell content with progress bar,
    or ``Collection not started``.

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

`./page_creator/partials/lists/utils/sort.py`:
```
"""Shared sorting utilities for list partials."""

import pandas as pd


def sort_by_registration_date(df: pd.DataFrame) -> pd.DataFrame:
    """Parse and sort a DataFrame by registration_date descending.

    Converts ``registration_date`` from a day-first string to ``datetime.date``,
    sorts descending (most recent first), and resets the index.

    Args:
        df: Must contain a ``registration_date`` column in ``DD/MM/YYYY`` format.

    Returns:
        A sorted copy with ``registration_date`` as ``datetime.date``.
    """
    df = df.copy()
    df["registration_date"] = pd.to_datetime(
        df["registration_date"], dayfirst=True
    ).dt.date
    return df.sort_values("registration_date", ascending=False).reset_index(drop=True)

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

`./page_creator/partials/lists/utils/tests/__init__.py`:
```

```

`./page_creator/partials/lists/utils/tests/test_dates.py`:
```
"""Tests for normalise_registration_date in utils/dates.py."""

import pytest
import pandas as pd

from page_creator.partials.lists.utils.dates import normalise_registration_date


@pytest.fixture
def base_df():
    return pd.DataFrame(
        {
            "registration_date": [
                "01/01/2015",
                "15/11/2021",
                "28/02/2019",
                "31/12/2023",
            ],
            "title": ["A", "B", "C", "D"],
        }
    )


class TestNormaliseRegistrationDate:
    def test_returns_formatted_strings(self, base_df):

        result = normalise_registration_date(base_df)
        for v in result["registration_date"]:
            assert isinstance(v, str)

    def test_correct_format(self, base_df):

        result = normalise_registration_date(base_df)
        # "1 Jan 2015", "15 Nov 2021", etc.
        assert result.iloc[0]["registration_date"] == "1 Jan 2015"
        assert result.iloc[1]["registration_date"] == "15 Nov 2021"
        assert result.iloc[2]["registration_date"] == "28 Feb 2019"
        assert result.iloc[3]["registration_date"] == "31 Dec 2023"

    def test_does_not_mutate_original(self, base_df):

        original = base_df["registration_date"].tolist()
        normalise_registration_date(base_df)
        assert base_df["registration_date"].tolist() == original

    def test_single_digit_day_has_no_leading_zero(self):

        df = pd.DataFrame({"registration_date": ["05/03/2020"]})
        result = normalise_registration_date(df)
        assert result.iloc[0]["registration_date"] == "5 Mar 2020"

    def test_invalid_date_raises(self):

        df = pd.DataFrame({"registration_date": ["not-a-date"]})
        with pytest.raises(Exception):
            normalise_registration_date(df)

    def test_empty_df_returns_empty(self):

        df = pd.DataFrame({"registration_date": pd.Series([], dtype=str)})
        result = normalise_registration_date(df)
        assert result.empty

    def test_other_columns_preserved(self, base_df):

        result = normalise_registration_date(base_df)
        assert "title" in result.columns
        assert result["title"].tolist() == base_df["title"].tolist()

```

`./page_creator/partials/lists/utils/tests/test_progress.py`:
```
"""Tests for progress_bar in utils/progress.py."""

from page_creator.partials.lists.utils.progress import progress_bar


class TestProgressBar:
    def test_returns_html_string(self):

        assert isinstance(progress_bar(50.0), str)

    def test_contains_progress_bar_class(self):

        assert 'class="progress-bar"' in progress_bar(50.0)

    def test_fill_width_reflects_percentage(self):

        result = progress_bar(75.0)
        assert 'style="width:75.0%"' in result

    def test_zero_percent(self):

        assert 'style="width:0.0%"' in progress_bar(0.0)

    def test_100_percent(self):

        assert 'style="width:100.0%"' in progress_bar(100.0)

    def test_over_100_clamped_to_100_visually(self):

        result = progress_bar(150.0)
        assert 'style="width:100.0%"' in result

    def test_over_100_adds_over_class(self):

        assert "progress-bar__fill--over" in progress_bar(150.0)

    def test_exactly_100_does_not_add_over_class(self):

        assert "progress-bar__fill--over" not in progress_bar(100.0)

    def test_negative_clamped_to_zero(self):

        assert 'style="width:0.0%"' in progress_bar(-10.0)

    def test_modifier_class_added(self):

        result = progress_bar(50.0, "signatures")
        assert "progress-bar__fill--signatures" in result

    def test_no_modifier_no_extra_class(self):

        result = progress_bar(50.0)
        assert "progress-bar__fill--" not in result

    def test_modifier_and_over_both_applied(self):

        result = progress_bar(200.0, "days-left")
        assert "progress-bar__fill--days-left" in result
        assert "progress-bar__fill--over" in result

```

`./page_creator/partials/lists/utils/tests/test_rows.py`:
```
"""Tests for build_initiative_row, build_sig_threshold_row, and related helpers."""

import pandas as pd
import pytest
from page_creator.partials.lists.utils.rows import (
    build_initiative_row,
    build_sig_threshold_row,
    build_sig_threshold_rows,
    HEADERS_WITH_SIGNATURES,
)


@pytest.fixture
def base_row():
    return pd.Series(
        {
            "title": "Stop Plastic Pollution",
            "url": "https://eci.ec.europa.eu/001",
            "registration_date": "1 Jan 2020",
            "objective": "Reduce single-use plastic across the EU.",
            "signatures_collected": 1_200_000,
            "signatures_threshold_met": 9,
        }
    )


class TestBuildInitiativeRow:
    def test_contains_title(self, base_row):

        result = build_initiative_row(base_row)
        assert "Stop Plastic Pollution" in result

    def test_contains_url_as_href(self, base_row):

        result = build_initiative_row(base_row)
        assert 'href="https://eci.ec.europa.eu/001"' in result

    def test_contains_registration_date(self, base_row):

        result = build_initiative_row(base_row)
        assert "1 Jan 2020" in result

    def test_contains_truncated_objective(self, base_row):

        result = build_initiative_row(base_row)
        assert "Reduce single-use plastic" in result

    def test_opens_in_new_tab(self, base_row):

        result = build_initiative_row(base_row)
        assert 'target="_blank"' in result

    def test_extra_cells_appended(self, base_row):

        result = build_initiative_row(base_row, extra_cells="<td>EXTRA</td>")
        assert "<td>EXTRA</td>" in result

    def test_missing_url_falls_back_to_hash(self, base_row):

        row = base_row.copy()
        row["url"] = None
        result = build_initiative_row(row)
        assert 'href="#"' in result

    def test_wrapped_in_tr(self, base_row):

        result = build_initiative_row(base_row)
        assert result.strip().startswith("<tr>") or "<tr>" in result
        assert "</tr>" in result


class TestBuildSigThresholdRow:
    def test_contains_signature_count(self, base_row):

        result = build_sig_threshold_row(base_row)
        assert "1,200,000" in result

    def test_contains_threshold_fraction(self, base_row):

        result = build_sig_threshold_row(base_row)
        assert "9 /" in result

    def test_contains_progress_bar(self, base_row):

        result = build_sig_threshold_row(base_row)
        assert "progress-bar" in result

    def test_null_signatures_shows_collection_not_started(self, base_row):

        row = base_row.copy()
        row["signatures_collected"] = None
        row["signatures_threshold_met"] = None
        result = build_sig_threshold_row(row)
        assert "Collection not started" in result


class TestBuildSigThresholdRows:
    def test_concatenates_all_rows(self, base_row):

        df = pd.DataFrame([base_row, base_row])
        result = build_sig_threshold_rows(df)
        assert result.count("Stop Plastic Pollution") == 2

    def test_empty_df_returns_empty_string(self):

        df = pd.DataFrame(
            columns=[
                "title",
                "url",
                "registration_date",
                "objective",
                "signatures_collected",
                "signatures_threshold_met",
            ]
        )
        assert build_sig_threshold_rows(df) == ""


class TestHeadersWithSignatures:
    def test_has_five_columns(self):

        assert len(HEADERS_WITH_SIGNATURES) == 5

    def test_contains_expected_headers(self):

        assert "Initiative" in HEADERS_WITH_SIGNATURES
        assert "Registration" in HEADERS_WITH_SIGNATURES
        assert "Signatures" in HEADERS_WITH_SIGNATURES
        assert "Countries Threshold" in HEADERS_WITH_SIGNATURES

```

`./page_creator/partials/lists/utils/tests/test_signatures.py`:
```
"""Tests for sig_cell and threshold_cell in utils/signatures.py."""

from page_creator.partials.lists.utils.signatures import sig_cell, threshold_cell
from page_creator.partials.lists.utils.constants import SIG_TARGET, COUNTRIES_THRESHOLD


class TestSigCell:
    def test_none_returns_collection_not_started(self):

        assert sig_cell(None) == "Collection not started"

    def test_nan_returns_collection_not_started(self):

        assert sig_cell(float("nan")) == "Collection not started"

    def test_zero_returns_formatted_zero(self):

        result = sig_cell(0)
        assert result.startswith("0")
        assert "Collection not started" not in result

    def test_value_formatted_with_commas(self):

        result = sig_cell(1_234_567)
        assert "1,234,567" in result

    def test_contains_progress_bar(self):

        assert "progress-bar" in sig_cell(500_000)

    def test_exact_target_shows_100_percent_bar(self):

        result = sig_cell(SIG_TARGET)
        assert "width:100.0%" in result

    def test_above_target_shows_over_class(self):

        result = sig_cell(SIG_TARGET + 1)
        assert "progress-bar__fill--over" in result

    def test_half_target_shows_50_percent(self):

        result = sig_cell(SIG_TARGET // 2)
        assert "width:50.0%" in result

    def test_uses_signatures_modifier(self):

        assert "progress-bar__fill--signatures" in sig_cell(500_000)


class TestThresholdCell:
    def test_none_returns_collection_not_started(self):

        assert threshold_cell(None) == "Collection not started"

    def test_nan_returns_collection_not_started(self):

        assert threshold_cell(float("nan")) == "Collection not started"

    def test_zero_shows_zero_of_threshold(self):

        result = threshold_cell(0)
        assert f"0 / {COUNTRIES_THRESHOLD}" in result
        assert "Collection not started" not in result

    def test_value_shows_n_of_threshold(self):

        result = threshold_cell(5)
        assert f"5 / {COUNTRIES_THRESHOLD}" in result

    def test_contains_progress_bar(self):

        assert "progress-bar" in threshold_cell(3)

    def test_exact_threshold_shows_100_percent(self):

        result = threshold_cell(COUNTRIES_THRESHOLD)
        assert "width:100.0%" in result

    def test_above_threshold_shows_over_class(self):

        result = threshold_cell(COUNTRIES_THRESHOLD + 1)
        assert "progress-bar__fill--over" in result

    def test_uses_threshold_modifier(self):

        assert "progress-bar__fill--threshold" in threshold_cell(3)

```

`./page_creator/partials/lists/utils/tests/test_table.py`:
```
"""Tests for build_table and wrap_table_card in utils/table.py."""

import pandas as pd

from page_creator.partials.lists.utils.table import build_table, wrap_table_card
from page_creator.partials.lists.utils.constants import SCROLL_THRESHOLD


HEADERS = ["Col A", "Col B", "Col C"]
ROWS_HTML = "<tr><td>1</td><td>2</td><td>3</td></tr>"


class TestBuildTable:
    def test_contains_table_class(self):

        assert 'class="data-table"' in build_table(HEADERS, ROWS_HTML)

    def test_headers_rendered_as_th(self):

        result = build_table(HEADERS, ROWS_HTML)
        for h in HEADERS:
            assert f"<th>{h}</th>" in result

    def test_rows_included_in_tbody(self):

        result = build_table(HEADERS, ROWS_HTML)
        assert ROWS_HTML in result

    def test_not_scrollable_by_default(self):

        result = build_table(HEADERS, ROWS_HTML)
        assert "data-table__scroll-wrapper" not in result

    def test_scrollable_adds_wrapper(self):

        result = build_table(HEADERS, ROWS_HTML, scrollable=True)
        assert "data-table__scroll-wrapper" in result

    def test_scrollbar_color_applied_when_scrollable(self):

        result = build_table(
            HEADERS, ROWS_HTML, scrollable=True, scrollbar_color="#abc123"
        )
        assert "--scrollbar-color:#abc123" in result

    def test_no_color_style_when_not_scrollable(self):

        result = build_table(
            HEADERS, ROWS_HTML, scrollable=False, scrollbar_color="#abc123"
        )
        assert "--scrollbar-color" not in result

    def test_no_color_style_when_no_color_provided(self):

        result = build_table(HEADERS, ROWS_HTML, scrollable=True)
        assert "--scrollbar-color" not in result

    def test_empty_rows_still_renders_table(self):

        result = build_table(HEADERS, "")
        assert "<table" in result
        assert "<thead>" in result


class TestWrapTableCard:
    def _make_df(self, n: int) -> pd.DataFrame:

        return pd.DataFrame({"title": [f"ECI {i}" for i in range(n)]})

    def test_contains_title(self):

        result = wrap_table_card(
            "<h3>Title</h3>", ROWS_HTML, self._make_df(3), HEADERS, "#fff"
        )
        assert "<h3>Title</h3>" in result

    def test_wrapped_in_card(self):

        result = wrap_table_card(
            "<h3>T</h3>", ROWS_HTML, self._make_df(3), HEADERS, "#fff"
        )
        assert "card" in result

    def test_not_scrollable_below_threshold(self):

        df = self._make_df(SCROLL_THRESHOLD)
        result = wrap_table_card("<h3>T</h3>", ROWS_HTML, df, HEADERS, "#fff")
        assert "data-table__scroll-wrapper" not in result

    def test_scrollable_above_threshold(self):

        df = self._make_df(SCROLL_THRESHOLD + 1)
        result = wrap_table_card("<h3>T</h3>", ROWS_HTML, df, HEADERS, "#fff")
        assert "data-table__scroll-wrapper" in result

    def test_scrollbar_color_passed_through(self):

        df = self._make_df(SCROLL_THRESHOLD + 1)
        result = wrap_table_card("<h3>T</h3>", ROWS_HTML, df, HEADERS, "#3CA371")
        assert "--scrollbar-color:#3CA371" in result

```

`./page_creator/partials/lists/utils/tests/test_text.py`:
```
"""Tests for truncate in utils/text.py."""

from page_creator.partials.lists.utils.text import truncate
from page_creator.partials.lists.utils.constants import DEFAULT_TRUNCATE


class TestTruncate:
    def test_short_text_unchanged(self):

        assert truncate("Hello") == "Hello"

    def test_exact_max_len_unchanged(self):

        text = "A" * DEFAULT_TRUNCATE
        assert truncate(text) == text

    def test_over_max_len_truncated(self):

        text = "A" * (DEFAULT_TRUNCATE + 10)
        result = truncate(text)
        assert len(result) == DEFAULT_TRUNCATE
        assert result.endswith("…")

    def test_custom_max_len(self):

        result = truncate("Hello World", max_len=5)
        assert result == "Hell…"

    def test_none_returns_empty_string(self):

        assert truncate(None) == ""

    def test_nan_returns_empty_string(self):

        assert truncate(float("nan")) == ""

    def test_pd_na_returns_empty_string(self):

        import pandas as pd

        assert truncate(pd.NA) == ""

    def test_numeric_input_coerced_to_string(self):

        result = truncate(12345)
        assert result == "12345"

    def test_empty_string_returns_empty_string(self):

        assert truncate("") == ""

    def test_exactly_one_over_appends_ellipsis(self):

        text = "A" * (DEFAULT_TRUNCATE + 1)
        result = truncate(text)
        assert result.endswith("…")
        assert len(result) == DEFAULT_TRUNCATE

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

`./page_creator/partials/lists/withdrawn.py`:
```
"""Renders a scrollable table of ECI initiatives no longer in active collection."""

import pandas as pd

from page_creator.utils import wrap_card
from page_creator.partials.lists.utils import (
    normalise_registration_date,
    wrap_sig_threshold_card,
)
from page_creator.partials.styles.colors import kpi_colors as colors
from page_creator.partials.lists.utils.sort import sort_by_registration_date

_STATUS = "Withdrawn"


def _filter(df: pd.DataFrame) -> pd.DataFrame:
    """Filter for initiatives that are no longer in active collection.

    Args:
        df: The full ECI initiatives DataFrame.

    Returns:
        Filtered DataFrame containing only ``_STATUS`` rows.
    """
    return df[df["current_status"] == _STATUS]


def _sort(df: pd.DataFrame) -> pd.DataFrame:
    """Normalise dates and sort by registration date descending.

    Args:
        df: Filtered DataFrame of closed-collection initiatives.

    Returns:
        Sorted and date-normalised DataFrame.
    """
    return sort_by_registration_date(df)


def generate_withdrawn(df: pd.DataFrame) -> str:
    """Return an HTML card containing a table of ECIs no longer in active collection.

    Filters for rows with ``current_status`` in ``_STATUSES``, sorted by
    registration date descending. Each row shows the initiative title (linked to
    its page), the registration date, a truncated objective, a signature progress
    bar, and a country-threshold progress bar.

    Args:
        df: The full ECI initiatives DataFrame. Must contain ``current_status``,
            ``title``, ``url``, ``objective``, ``registration_date``,
            ``signatures_collected``, and ``signatures_threshold_met`` columns.

    Returns:
        An HTML string wrapping the table in a ``card`` div, or a card with a
        fallback message if no initiatives match.
    """
    df_filtered = _filter(df)
    df_sorted = _sort(df_filtered)
    df_final = normalise_registration_date(df_sorted)

    title = (
        '<h3 class="card__title">'
        f"🔙 {_STATUS}: "
        f'<span class="card__count" style="color:{colors.withdrawn}">{len(df_final)}</span>'
        "</h3>"
    )

    if df_final.empty:
        body = '<p class="list-empty">No closed-collection initiatives found.</p>'
        return wrap_card(title + body)

    return wrap_sig_threshold_card(title, df_final, colors.withdrawn)

```

