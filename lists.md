`./page_creator/partials/lists/currently_open.py`:
```
"""
Renders a scrollable table of ECI initiatives
currently open for signature collection.
"""

# Third party
import pandas as pd

from page_creator.utils import wrap_card
from page_creator.partials.lists.utils import build_table, progress_bar, truncate

_STATUS = "Collection Ongoing"
_SCROLL_THRESHOLD = 5
_COUNTRIES_THRESHOLD = 7
_SIG_TARGET = 1_000_000

_HEADERS = ["Initiative", "Objective", "Signatures", "Countries Threshold"]


def generate_currently_open(df: pd.DataFrame) -> str:
    """
    Return an HTML card containing a table of all currently open ECI initiatives.

    Filters for rows with ``current_status == 'Collection Ongoing'``, sorted by
    signature count descending. Each row shows the initiative title (linked to its
    page), a truncated objective, a signature progress bar towards the 1M target,
    and a country-threshold progress bar out of ``_COUNTRIES_THRESHOLD``. The table
    gains a scroll wrapper when the row count exceeds ``_SCROLL_THRESHOLD``.

    Args:
        df: The full ECI initiatives DataFrame. Must contain ``current_status``,
            ``title``, ``url``, ``objective``, ``signatures_collected``, and
            ``signatures_threshold_met`` columns.

    Returns:
        An HTML string wrapping the table in a ``card`` div, or a card with a
        fallback message if no initiatives are currently open.
    """

    open_df = (
        df[df["current_status"] == _STATUS]
        .sort_values("signatures_collected", ascending=False)
        .reset_index(drop=True)
    )

    title = f'<h3 class="card__title">🗳️ Currently Open: <span class="card__count">{len(open_df)}</span></h3>'

    if open_df.empty:
        body = '<p class="list-empty">No initiatives currently open for signature collection.</p>'
        return wrap_card(title + body)

    rows = ""
    for _, row in open_df.iterrows():
        url = row.get("url") or "#"
        objective = truncate(row.get("objective", ""))

        if pd.notna(row["signatures_collected"]):
            sig_val = int(row["signatures_collected"])
            sigs = (
                f"{sig_val:,}{progress_bar(sig_val / _SIG_TARGET * 100, 'signatures')}"
            )
        else:
            sigs = "N/A"

        if pd.notna(row["signatures_threshold_met"]):
            thr_val = int(row["signatures_threshold_met"])
            threshold = f"{thr_val} / {_COUNTRIES_THRESHOLD}{progress_bar(thr_val / _COUNTRIES_THRESHOLD * 100, 'threshold')}"
        else:
            threshold = "N/A"

        rows += f"""
        <tr>
          <td><a href="{url}" target="_blank" rel="noopener noreferrer">{row["title"]}</a></td>
          <td>{objective}</td>
          <td>{sigs}</td>
          <td>{threshold}</td>
        </tr>"""

    return wrap_card(
        title + build_table(_HEADERS, rows, scrollable=len(open_df) > _SCROLL_THRESHOLD)
    )

```

`./page_creator/partials/lists/got_response.py`:
```
"""Renders a scrollable table of ECI initiatives that received an EU Commission response."""

import pandas as pd

from page_creator.utils import wrap_card
from page_creator.partials.lists.utils import build_table, truncate


_RESPONSE_STATUSES = frozenset(
    ["Commission Engaged", "Law Passed", "Rejected Legislation"]
)
_SCROLL_THRESHOLD = 5

_HEADERS = ["Initiative", "Objective", "Response"]


def generate_got_response(df: pd.DataFrame) -> str:
    """Return an HTML card containing a table of ECIs that received a Commission response.

    Filters for rows with ``current_status`` in ``_RESPONSE_STATUSES``, sorted by
    signature count descending. Each row shows the initiative title (linked to
    its page), a truncated objective, and the truncated commission response text.

    Args:
        df: The full ECI initiatives DataFrame. Must contain ``current_status``,
            ``title``, ``url``, ``objective``, and ``commission_answer_text`` columns.

    Returns:
        An HTML string wrapping the table in a ``card`` div, or a card with a
        fallback message if no initiatives received a response.
    """

    filtered_df = (
        df[df["current_status"].isin(_RESPONSE_STATUSES)]
        .sort_values("signatures_collected", ascending=False)
        .reset_index(drop=True)
    )

    title = f'<h3 class="card__title">📬 Got EU Response: <span class="card__count">{len(filtered_df)}</span></h3>'

    if filtered_df.empty:
        body = '<p class="list-empty">No initiatives have received an EU Commission response.</p>'
        return wrap_card(title + body)

    rows = ""
    for _, row in filtered_df.iterrows():
        url = row.get("url") or "#"
        objective = truncate(row.get("objective", ""))
        response = truncate(row.get("commission_answer_text", ""), max_len=200)

        rows += f"""
        <tr>
          <td><a href="{url}" target="_blank" rel="noopener noreferrer">{row["title"]}</a></td>
          <td>{objective}</td>
          <td>{response}</td>
        </tr>"""

    return wrap_card(
        title
        + build_table(_HEADERS, rows, scrollable=len(filtered_df) > _SCROLL_THRESHOLD)
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


_STATUS = "Law Passed"
_SCROLL_THRESHOLD = 5
_LEGISLATION_FALLBACK = "Legislation details not yet available."

_HEADERS = ["Initiative", "Objective", "Legislation"]


def generate_led_to_legislation(df: pd.DataFrame) -> str:
    """Return an HTML card containing a table of ECIs that led to passed legislation.

    Filters for rows with ``current_status == 'Law Passed'``, sorted by signature
    count descending. The Legislation column uses a fallback placeholder until
    real legislative reference data is added to the dataset.

    Args:
        df: The full ECI initiatives DataFrame. Must contain ``current_status``,
            ``title``, ``url``, and ``objective`` columns.

    Returns:
        An HTML string wrapping the table in a ``card`` div, or a card with a
        fallback message if no initiatives led to legislation.
    """
    filtered_df = (
        df[df["current_status"] == _STATUS]
        .sort_values("signatures_collected", ascending=False)
        .reset_index(drop=True)
    )

    title = f'<h3 class="card__title">⚖️ Led to Legislation: <span class="card__count">{len(filtered_df)}</span></h3>'

    if filtered_df.empty:
        body = '<p class="list-empty">No initiatives have led to legislation yet.</p>'
        return wrap_card(title + body)

    rows = ""
    for _, row in filtered_df.iterrows():
        url = row.get("url") or "#"
        objective = truncate(row.get("objective", ""))
        # TODO: replace fallback once legislation column is added to the dataset
        legislation = truncate(row.get("legislation", _LEGISLATION_FALLBACK))

        rows += f"""
        <tr>
          <td><a href="{url}" target="_blank" rel="noopener noreferrer">{row["title"]}</a></td>
          <td>{objective}</td>
          <td>{legislation}</td>
        </tr>"""

    return wrap_card(
        title
        + build_table(_HEADERS, rows, scrollable=len(filtered_df) > _SCROLL_THRESHOLD)
    )

```

`./page_creator/partials/lists/reached_signatures.py`:
```
"""Renders a scrollable table of ECI initiatives that reached the 1M signature threshold."""

import pandas as pd

from page_creator.utils import wrap_card
from page_creator.partials.lists.utils import build_table, progress_bar, truncate


_SIG_TARGET = 1_000_000
_SCROLL_THRESHOLD = 5
_COUNTRIES_THRESHOLD = 7

_HEADERS = ["Initiative", "Objective", "Signatures", "Countries Threshold"]


def generate_reached_signatures(df: pd.DataFrame) -> str:
    """Return an HTML card containing a table of ECIs that reached 1M signatures.

    Filters for rows where ``signatures_collected >= 1_000_000``, sorted by
    signature count descending. Each row shows the initiative title (linked to
    its page), a truncated objective, a signature progress bar, and a
    country-threshold progress bar.

    Args:
        df: The full ECI initiatives DataFrame. Must contain ``signatures_collected``,
            ``title``, ``url``, ``objective``, and ``signatures_threshold_met`` columns.

    Returns:
        An HTML string wrapping the table in a ``card`` div, or a card with a
        fallback message if no initiatives reached the threshold.
    """

    filtered_df = (
        df[df["signatures_collected"] >= _SIG_TARGET]
        .sort_values("signatures_collected", ascending=False)
        .reset_index(drop=True)
    )

    title = f'<h3 class="card__title">✅ Reached 1M Signatures: <span class="card__count">{len(filtered_df)}</span></h3>'

    if filtered_df.empty:
        body = '<p class="list-empty">No initiatives have reached 1M signatures.</p>'
        return wrap_card(title + body)

    rows = ""
    for _, row in filtered_df.iterrows():
        url = row.get("url") or "#"
        objective = truncate(row.get("objective", ""))

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
          <td>{objective}</td>
          <td>{sigs}</td>
          <td>{threshold}</td>
        </tr>"""

    return wrap_card(
        title
        + build_table(_HEADERS, rows, scrollable=len(filtered_df) > _SCROLL_THRESHOLD)
    )

```

`./page_creator/partials/lists/total_initiatives.py`:
```
"""Renders a scrollable table of all registered ECI initiatives."""

import pandas as pd

from page_creator.utils import wrap_card
from page_creator.partials.lists.utils import build_table, progress_bar, truncate


_SCROLL_THRESHOLD = 5
_COUNTRIES_THRESHOLD = 7
_SIG_TARGET = 1_000_000

_HEADERS = ["Initiative", "Objective", "Signatures", "Countries Threshold"]


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

    sorted_df = df.sort_values("signatures_collected", ascending=False).reset_index(
        drop=True
    )

    title = f'<h3 class="card__title">📋 Total Initiatives: <span class="card__count">{len(sorted_df)}</span></h3>'

    rows = ""
    for _, row in sorted_df.iterrows():

        url = row.get("url") or "#"
        objective = truncate(row.get("objective", ""))

        if pd.notna(row["signatures_collected"]):
            sig_val = int(row["signatures_collected"])
            sigs = (
                f"{sig_val:,}{progress_bar(sig_val / _SIG_TARGET * 100, 'signatures')}"
            )
        else:
            sigs = "N/A"

        if pd.notna(row["signatures_threshold_met"]):
            thr_val = int(row["signatures_threshold_met"])
            threshold = f"{thr_val} / {_COUNTRIES_THRESHOLD}{progress_bar(thr_val / _COUNTRIES_THRESHOLD * 100, 'threshold')}"
        else:
            threshold = "N/A"

        rows += f"""
        <tr>
          <td><a href="{url}" target="_blank" rel="noopener noreferrer">{row["title"]}</a></td>
          <td>{objective}</td>
          <td>{sigs}</td>
          <td>{threshold}</td>
        </tr>"""

    return wrap_card(
        title
        + build_table(_HEADERS, rows, scrollable=len(sorted_df) > _SCROLL_THRESHOLD)
    )

```

`./page_creator/partials/lists/utils.py`:
```
"""Shared HTML-generation helpers for list and table partials."""

# Third-party
import pandas as pd

_DEFAULT_TRUNCATE = 100
_DEFAULT_SCROLL_THRESHOLD = 5


def truncate(text: str, max_len: int = _DEFAULT_TRUNCATE) -> str:
    """
    Truncate ``text`` to ``max_len`` characters, appending '…' if cut; returns '' for NaN.
    """

    if pd.isna(text):
        return ""

    s = str(text)

    return s if len(s) <= max_len else s[: max_len - 1] + "…"


def progress_bar(pct: float, modifier: str = "") -> str:
    """
    Return an HTML progress bar div filled to ``pct``%,
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


def build_table(headers: list[str], rows_html: str, scrollable: bool = False) -> str:
    """
    Return an HTML ``data-table`` string with a sticky header row,
    optionally wrapped in a scrollable container div.
    """

    header_cells = "\n      ".join(f"<th>{h}</th>" for h in headers)
    wrapper_open = '<div class="data-table__scroll-wrapper">' if scrollable else ""
    wrapper_close = "</div>" if scrollable else ""
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

```

