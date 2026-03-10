"""
Reusable top level logic
"""


def wrap_card(inner_html: str, extra_class: str = "") -> str:
    """Wrap an HTML fragment in a styled card ``<div>``.

    Combines the base ``card`` CSS class with any additional classes,
    then returns the inner HTML enclosed in the resulting container.

    Args:
        inner_html: The HTML content to nest inside the card div.
        extra_class: Optional additional CSS class(es) to append to
            the base ``card`` class. Multiple classes can be passed
            as a space-separated string, e.g. ``"card--wide featured"``.

    Returns:
        A string containing the card ``<div>`` with ``inner_html``
        as its content.

    Example:
        >>> wrap_card("<p>Hello</p>")
        '<div class="card">\\n<p>Hello</p>\\n</div>'

        >>> wrap_card("<p>Hello</p>", extra_class="card--highlight")
        '<div class="card card--highlight">\\n<p>Hello</p>\\n</div>'
    """

    cls = f"card {extra_class}".strip()
    return f"""<div class="{cls}">\n{inner_html}\n</div>"""
