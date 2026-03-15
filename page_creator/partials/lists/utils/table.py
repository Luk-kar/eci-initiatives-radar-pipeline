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
