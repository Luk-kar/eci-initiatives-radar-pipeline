`./page_creator/partials/lists/currently_open.py`:
```
"""Renders a scrollable table of ECI initiatives currently open for signature collection."""

# Third party
import pandas as pd

# Local
from page_creator.utils import wrap_card
from page_creator.partials.lists.utils import build_table, progress_bar, truncate

_STATUS = "Collection Ongoing"
_SCROLL_THRESHOLD = 5
_COUNTRIES_THRESHOLD = 7
_SIG_TARGET = 1_000_000

_HEADERS = ["Initiative", "Objective", "Days Left", "Signatures", "Countries Threshold"]


def generate_currently_open(df: pd.DataFrame) -> str:
    """
    Return an HTML card containing a table of all currently open ECI initiatives.

    Filters for rows with ``current_status == 'Collection Ongoing'``, sorted by
    signature count descending. Each row shows the initiative title (linked to its
    page), a truncated objective, a days-left cell (JavaScript-rendered from
    ``timeline_collection_start`` and ``timeline_collection_closed``), a signature
    progress bar towards the 1M target, and a country-threshold progress bar out of
    ``_COUNTRIES_THRESHOLD``.

    The table gains a scroll wrapper when the row count exceeds ``_SCROLL_THRESHOLD``.

    Args:
        df: The full ECI initiatives DataFrame. Must contain ``current_status``,
            ``title``, ``url``, ``objective``, ``signatures_collected``,
            ``signatures_threshold_met``, ``timeline_collection_start``, and
            ``timeline_collection_closed`` columns.

    Returns:
        An HTML string wrapping the table in a ``card`` div, or a card with a
        fallback message if no initiatives are currently open.
    """

    open_df = df[df["current_status"] == _STATUS].copy()

    open_df["_start_dt"] = pd.to_datetime(
        open_df["timeline_collection_start"], dayfirst=True, errors="raise"
    )
    open_df["_has_closed"] = open_df["timeline_collection_closed"].notna() & (
        open_df["timeline_collection_closed"].str.strip() != ""
    )

    open_df = (
        open_df.sort_values(["_has_closed", "_start_dt"], ascending=[True, True])
        .drop(columns=["_start_dt", "_has_closed"])
        .reset_index(drop=True)
    )

    if open_df.empty:
        title = """\n\nNo initiatives currently open for signature collection.\n\n"""
        return wrap_card(title)

    rows = ""
    for _, row in open_df.iterrows():
        url = row["url"]
        objective = truncate(row["objective"])

        # --- Days Left cell ---
        date_start = row.get("timeline_collection_start", "")
        date_closed = row.get("timeline_collection_closed", "")
        date_start = "" if pd.isna(date_start) else str(date_start).strip()
        date_closed = "" if pd.isna(date_closed) else str(date_closed).strip()

        # Compute elapsed % of the 12-month window for the static progress bar
        if date_start:
            start_dt = pd.to_datetime(date_start, dayfirst=True, errors="coerce")
            deadline_dt = start_dt + pd.DateOffset(months=12)
            now_dt = pd.Timestamp.now()
            total_ms = (deadline_dt - start_dt).total_seconds()
            elapsed_ms = (now_dt - start_dt).total_seconds()
            pct = min(max(elapsed_ms / total_ms * 100, 0), 100)
            bar = progress_bar(pct, "days-left")
        else:
            bar = ""

        days_left = (
            f'<td class="days-left-cell" data-start="{date_start}" data-closed="{date_closed}">'
            f'<span class="days-left-cell__label"></span>'
            f"{bar}"
            f"</td>"
        )

        # --- Signatures cell ---
        if pd.notna(row["signatures_collected"]):
            sig_val = int(row["signatures_collected"])
            sigs = (
                f"{sig_val:,}{progress_bar(sig_val / _SIG_TARGET * 100, 'signatures')}"
            )
        else:
            sigs = "N/A"

        # --- Countries threshold cell ---
        if pd.notna(row["signatures_threshold_met"]):
            thr_val = int(row["signatures_threshold_met"])
            threshold = (
                f"{thr_val}"
                " / "
                f"{_COUNTRIES_THRESHOLD}{progress_bar(thr_val / _COUNTRIES_THRESHOLD * 100, 'threshold')}"
            )
        else:
            threshold = "N/A"

        rows += f"""
        <tr>
            <td><a href="{url}" target="_blank">{row.get('title', '')}</a></td>
            <td>{objective}</td>
            {days_left}
            <td>{sigs}</td>
            <td>{threshold}</td>
        </tr>"""

    body = build_table(_HEADERS, rows, scrollable=len(open_df) > _SCROLL_THRESHOLD)
    title = f"""\n\nCurrently Open ({len(open_df)})\n\n"""
    return wrap_card(title + body)

```

`./page_creator/partials/lists/got_response.py`:
```
"""Renders a scrollable table of ECI initiatives that received an EU Commission response."""

import pandas as pd

from page_creator.utils import wrap_card
from page_creator.partials.lists.utils import build_table, truncate
from page_creator.partials.styles.colors import kpi_colors as colors


_RESPONSE_STATUSES = frozenset(
    ["Commission Engaged", "Law Passed", "Rejected Legislation"]
)
_SCROLL_THRESHOLD = 5

_HEADERS = ["Initiative", "Registration", "Objective", "Response"]


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

    filtered_df = (
        df[df["current_status"].isin(_RESPONSE_STATUSES)]
        .sort_values("registration_date", ascending=False)
        .reset_index(drop=True)
    )

    title = (
        '<h3 class="card__title">'
        "📬 Got EU Response: "
        f'<span class="card__count" style="color:{colors.got_response}">{len(filtered_df)}</span>'
        "</h3>"
    )

    if filtered_df.empty:
        body = '<p class="list-empty">No initiatives have received an EU Commission response.</p>'
        return wrap_card(title + body)

    df["registration_date"] = pd.to_datetime(
        df["registration_date"], format="%d/%m/%Y"
    ).dt.date

    rows = ""
    for _, row in filtered_df.iterrows():

        url = row["url"]
        registration = row["registration_date"]
        objective = truncate(row["objective"])
        response = truncate(row["commission_answer_text"], max_len=200)

        rows += f"""
        <tr>
          <td><a href="{url}" target="_blank" rel="noopener noreferrer">{row["title"]}</a></td>
          <td>{registration}</td>
          <td>{objective}</td>
          <td>{response}</td>
        </tr>"""

    return wrap_card(
        title
        + build_table(
            _HEADERS,
            rows,
            scrollable=len(filtered_df) > _SCROLL_THRESHOLD,
            scrollbar_color=colors.got_response,
        )
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
from page_creator.partials.lists.utils import build_table, truncate
from page_creator.partials.styles.colors import kpi_colors as colors

_STATUS = "Law Passed"
_SCROLL_THRESHOLD = 5
_LEGISLATION_FALLBACK = "Legislation details not yet available."

_HEADERS = ["Initiative", "Registration", "Objective", "Legislation"]


def generate_led_to_legislation(df: pd.DataFrame) -> str:
    """Return an HTML card containing a table of ECIs that led to passed legislation.

    Filters for rows with ``current_status == 'Law Passed'``, sorted by
    registration date descending. The Legislation column uses a fallback
    placeholder until real legislative reference data is added to the dataset.

    Args:
        df: The full ECI initiatives DataFrame. Must contain ``current_status``,
            ``title``, ``url``, ``objective``, and ``registration_date`` columns.

    Returns:
        An HTML string wrapping the table in a ``card`` div, or a card with a
        fallback message if no initiatives led to legislation.
    """

    filtered_df = (
        df[df["current_status"] == _STATUS]
        .sort_values("registration_date", ascending=False)
        .reset_index(drop=True)
    )

    title = f'<h3 class="card__title">⚖️ Led to Legislation: <span class="card__count" style="color:{colors.led_to_legislation}">{len(filtered_df)}</span></h3>'

    if filtered_df.empty:
        body = '<p class="list-empty">No initiatives have led to legislation yet.</p>'
        return wrap_card(title + body)

    df["registration_date"] = pd.to_datetime(
        df["registration_date"], format="%d/%m/%Y"
    ).dt.date

    rows = ""
    for _, row in filtered_df.iterrows():
        url = row["url"]
        registration = row["registration_date"]
        objective = truncate(row["objective"])

        # TODO: replace fallback once legislation column is added to the dataset
        legislation = truncate(row.get("legislation", _LEGISLATION_FALLBACK))

        rows += f"""
        <tr>
          <td><a href="{url}" target="_blank" rel="noopener noreferrer">{row["title"]}</a></td>
          <td>{registration}</td>
          <td>{objective}</td>
          <td>{legislation}</td>
        </tr>"""

    return wrap_card(
        title
        + build_table(
            _HEADERS,
            rows,
            scrollable=len(filtered_df) > _SCROLL_THRESHOLD,
            scrollbar_color=colors.led_to_legislation,
        )
    )

```

`./page_creator/partials/lists/reached_signatures.py`:
```
"""Renders a scrollable table of ECI initiatives that reached the 1M signature threshold."""

import pandas as pd

from page_creator.utils import wrap_card
from page_creator.partials.lists.utils import build_table, progress_bar, truncate
from page_creator.partials.styles.colors import kpi_colors as colors


_SIG_TARGET = 1_000_000
_SCROLL_THRESHOLD = 5
_COUNTRIES_THRESHOLD = 7

_HEADERS = [
    "Initiative",
    "Registration",
    "Objective",
    "Signatures",
    "Countries Threshold",
]


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

    filtered_df = (
        df[df["signatures_collected"] >= _SIG_TARGET]
        .sort_values("registration_date", ascending=False)
        .reset_index(drop=True)
    )

    title = (
        '<h3 class="card__title">'
        "✅ Reached 1M Signatures: "
        f'<span class="card__count" style="color:{colors.reached_signatures}">{len(filtered_df)}</span>'
        "</h3>"
    )

    if filtered_df.empty:
        body = '<p class="list-empty">No initiatives have reached 1M signatures.</p>'
        return wrap_card(title + body)

    df["registration_date"] = pd.to_datetime(
        df["registration_date"], format="%d/%m/%Y"
    ).dt.date

    rows = ""
    for _, row in filtered_df.iterrows():
        url = row["url"]
        registration = row["registration_date"]
        objective = truncate(row["objective"])

        sig_val = int(row["signatures_collected"])
        sigs = f"{sig_val:,}{progress_bar(sig_val / _SIG_TARGET * 100, 'signatures')}"

        if pd.notna(row["signatures_threshold_met"]):
            thr_val = int(row["signatures_threshold_met"])
            threshold = f"{thr_val} / {_COUNTRIES_THRESHOLD}{progress_bar(thr_val / _COUNTRIES_THRESHOLD * 100, 'threshold')}"
        else:
            threshold = "N/A"

        rows += f"""
        <tr>
          <td><a href="{url}" target="_blank" rel="noopener noreferrer">{row["title"]}</a></td>
          <td>{registration}</td>
          <td>{objective}</td>
          <td>{sigs}</td>
          <td>{threshold}</td>
        </tr>"""

    return wrap_card(
        title
        + build_table(
            _HEADERS,
            rows,
            scrollable=len(filtered_df) > _SCROLL_THRESHOLD,
            scrollbar_color=colors.reached_signatures,
        )
    )

```

`./page_creator/partials/lists/total_initiatives.py`:
```
"""Renders a scrollable table of all registered ECI initiatives."""

import pandas as pd

from page_creator.utils import wrap_card
from page_creator.partials.lists.utils import build_table, progress_bar, truncate
from page_creator.partials.styles.colors import kpi_colors as colors


_SCROLL_THRESHOLD = 5
_COUNTRIES_THRESHOLD = 7
_SIG_TARGET = 1_000_000

_HEADERS = [
    "Initiative",
    "Registration",
    "Objective",
    "Signatures",
    "Countries Threshold",
]


def generate_total_initiatives(df: pd.DataFrame) -> str:
    """Return an HTML card containing a table of all registered ECI initiatives.

    Sorted by signature count descending. Each row shows the initiative title
    (linked to its page), a truncated objective, a signature progress bar towards
    the 1M target, and a country-threshold progress bar out of ``_COUNTRIES_THRESHOLD``.

    Args:
        df: The full ECI initiatives DataFrame. Must contain ``title``, ``url``,
            ``objective``, ``signatures_collected``, and ``signatures_threshold_met`` columns.

    Returns:
        An HTML string wrapping the table in a ``card`` div.
    """

    sorted_df = df.sort_values("registration_date", ascending=False).reset_index(
        drop=True
    )

    title = (
        '<h3 class="card__title">📋 Total Initiatives: '
        f'<span class="card__count" style="color:{colors.total_initiatives}">{len(sorted_df)}</span>'
        "</h3>"
    )

    rows = ""

    df["registration_date"] = pd.to_datetime(
        df["registration_date"], format="%d/%m/%Y"
    ).dt.date

    for _, row in sorted_df.iterrows():

        url = row["url"]
        registration = row["registration_date"]
        objective = truncate(row["objective"])

        if pd.notna(row["signatures_collected"]):
            sig_val = int(row["signatures_collected"])
            sigs = (
                f"{sig_val:,}{progress_bar(sig_val / _SIG_TARGET * 100, 'signatures')}"
            )
        else:
            sigs = "N/A"

        if pd.notna(row["signatures_threshold_met"]):
            thr_val = int(row["signatures_threshold_met"])
            threshold = (
                f"{thr_val}"
                " / "
                f"{_COUNTRIES_THRESHOLD}{progress_bar(thr_val / _COUNTRIES_THRESHOLD * 100, 'threshold')}"
            )
        else:
            threshold = "N/A"

        rows += f"""
        <tr>
          <td><a href="{url}" target="_blank" rel="noopener noreferrer">{row["title"]}</a></td>
          <td>{registration}</td>
          <td>{objective}</td>
          <td>{sigs}</td>
          <td>{threshold}</td>
        </tr>"""

    return wrap_card(
        title
        + build_table(
            _HEADERS,
            rows,
            scrollable=len(sorted_df) > _SCROLL_THRESHOLD,
            scrollbar_color=colors.total_initiatives,
        )
    )

```

`./page_creator/partials/lists/utils.py`:
```
"""Shared HTML-generation helpers for list and table partials."""

# Third-party
import pandas as pd


_DEFAULT_TRUNCATE = 100
_SCROLL_THRESHOLD = 5
_SIG_TARGET = 1_000_000
_COUNTRIES_THRESHOLD = 7


def truncate(text: str, max_len: int = _DEFAULT_TRUNCATE) -> str:
    """Truncate ``text`` to ``max_len`` characters, appending '…' if cut; returns '' for NaN."""
    if pd.isna(text):
        return ""
    s = str(text)
    return s if len(s) <= max_len else s[: max_len - 1] + "…"


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
                         CSS variable on the scroll wrapper, overriding the default thumb colour.
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


def wrap_table_card(
    title: str,
    rows: str,
    df: pd.DataFrame,
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
    from page_creator.utils import (
        wrap_card,
    )  # local import to avoid circular dependency

    return wrap_card(
        title
        + build_table(
            headers,
            rows,
            scrollable=len(df) > _SCROLL_THRESHOLD,
            scrollbar_color=scrollbar_color,
        )
    )

```

