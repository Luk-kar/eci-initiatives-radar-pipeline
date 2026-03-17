"""Shared HTML-formatting helpers for Plotly hover tooltips across chart partials."""

import json
import textwrap


_WRAP_WIDTH = 60
_MAX_LINES = 6
_MAX_HOVER_ITEMS = 10

STATUS_SECTION_MAP: dict[str, str] = {
    "LawPassed": "law-passed-list-slot",
    "CommissionEngaged": "commission-engaged-list-slot",
    "RejectedLegislation": "rejected-legislation-list-slot",
    "AwaitingResponse": "awaiting-response-list-slot",
    "CollectionOngoing": "collection-ongoing-list-slot",
    "CollectionUnsuccessful": "collection-unsuccessful-list-slot",
    "Withdrawn": "withdrawn-list-slot",
}


def hover_item_list(titles: list[str], max_items: int = _MAX_HOVER_ITEMS) -> str:
    """Return a ``<br>``-joined bullet list of titles, truncated to ``max_items`` with a count suffix."""

    if not titles:
        return "None"

    items = [f"• {t}" for t in titles[:max_items]]
    result = "<br>".join(items)

    if len(titles) > max_items:
        result += f"<br><i>… (and {len(titles) - max_items} more)</i>"

    return result


def hover_wrap(text: str, width: int = _WRAP_WIDTH, max_lines: int = _MAX_LINES) -> str:
    """Break long text into ``<br>``-separated lines, truncating to ``max_lines`` with a trailing '…'."""

    lines = textwrap.wrap(str(text), width=width)

    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip() + "…"

    return "<br>".join(lines)


click_script_open_new_page = """
<script>
(function () {{
    var el = document.getElementById("{}");
    if (!el) return;

    function getDragLayer() {{
        return el.querySelector(".nsewdrag");
    }}

    el.on("plotly_hover", function () {{
        var drag = getDragLayer();
        if (drag) drag.style.cursor = "pointer";
    }});

    el.on("plotly_unhover", function () {{
        var drag = getDragLayer();
        if (drag) drag.style.cursor = "";
    }});

    el.on("plotly_click", function (data) {{
        var pt = data.points[0];
        if (pt && pt.customdata) {{
            window.open(pt.customdata[0], "_blank", "noopener,noreferrer");
        }}
    }});
}})();
</script>"""


def build_click_scroll_script(
    section_map: dict[str, str],
    point_key: str = "label",
    strip_br: bool = False,
    strip_spaces: bool = False,
) -> str:
    mapping_json = json.dumps(section_map)

    normalizers = []

    if strip_br:
        normalizers.append("rawVal.replace(/<br>/gi, '')")

    if strip_spaces:
        normalizers.append("rawVal.replace(/ /g, '')")

    clean_expr = "rawVal"

    for norm in normalizers:
        clean_expr = norm.replace("rawVal", clean_expr)

    return f"""
var _map = {mapping_json};
var _plotDiv = document.getElementById('{{plot_id}}');

_plotDiv.on('plotly_click', function(data) {{
    if (!data.points || !data.points.length) return;
    var rawVal = data.points[0].{point_key};
    var cleanVal = {clean_expr};
    var sectionId = _map[cleanVal];
    if (sectionId && typeof scrollToSection === 'function') {{
        scrollToSection(sectionId);
    }}
}});

var _style = document.createElement('style');
_style.textContent = '[id="{{plot_id}}"] .nsewdrag, [id="{{plot_id}}"] .surface {{ cursor: pointer !important; }}';
document.head.appendChild(_style);
"""
