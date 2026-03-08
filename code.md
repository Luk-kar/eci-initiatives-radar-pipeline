`./page_to_export/index.html`:
```
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
  <title>ECI Dashboard POC</title>
  <script src="https://cdn.plot.ly/plotly-2.32.0.min.js"></script>
</head>
<link rel="stylesheet" href="./styles/styles.css">

<body>
  <div class="dashboard-container" id="top"></div>
  <div class="dashboard-container">

    <div id="header-slot"></div>
    <div id="footer-slot"></div>
    <div id="kpi-slot"></div>

    <div class="table-curently-open-slot">
      <div id="currently-open"></div>
    </div>

    <div class="row-top-10-graph">
      <div id="chart1-slot"></div>
    </div>

    <div class="move-top-page">
      <button id="back-to-top" class="back-to-top-btn" aria-label="Scroll to top" title="Back to top">
        &#8679;
      </button>
    </div>

    <div class="bottom-row">
      <div id="chart-initiatives-status-slot"></div>
      <div id="chart-signatures-count-slot"></div>
    </div>

  </div>

  <script>
    
    const backToTopBtn = document.getElementById("back-to-top");

    window.addEventListener("scroll", () => {
      backToTopBtn.classList.toggle("visible", window.scrollY > 300);
    });

    backToTopBtn.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });

    async function loadPartial(url, targetId) {
      const res  = await fetch(url);
      const html = await res.text();
      const target = document.getElementById(targetId);
      target.innerHTML = html;
      target.querySelectorAll("script").forEach(old => {
        const s = document.createElement("script");
        s.textContent = old.textContent;
        old.replaceWith(s);
      });
    }

    (async () => {
      await loadPartial("partials/header.html",                "header-slot");
      await loadPartial("partials/deep_dive_footer.html",      "footer-slot");
      await loadPartial("partials/kpi_row.html",   "kpi-slot");
      await loadPartial("partials/chart_top_10_signatures.html",     "chart1-slot");
      await loadPartial("partials/chart_outcomes.html",        "chart-initiatives-status-slot");
      await loadPartial("partials/chart_signatures_cohorts.html", "chart-signatures-count-slot");
      await loadPartial("partials/list_currently_open.html",   "currently-open");
    })();
  </script>
</body>
</html>

```
`./page_to_export/styles/styles.css`:
```
body { 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background-color: #f5f7f9; 
        }
        h1 { 
            text-align: center; 
            color: #2A3F5F; 
            margin-bottom: 15px;
        }
        .dashboard-container { 
            max-width: 1200px; 
            margin: 0 auto; 
        }
        .card { 
            background: white; 
            border-radius: 8px; 
            box-shadow: 0 4px 6px rgba(0,0,0,0.05); 
            padding: 15px; 
            margin-bottom: 20px; 
        }
        .row-top-10-graph { 
            display: flex; 
            flex-direction: column; 
        }
        .bottom-row { 
            display: flex; 
            gap: 20px; 
        }
        .bottom-col { 
            flex: 1; 
            min-width: 0; 
        }
        /* Stack vertically on mobile devices */
        @media (max-width: 768px) {
            .bottom-row {
                flex-direction: column;
            }
        }
.deep-dive-banner {
  display: inline-flex;
  justify-content: center;
  width: 100%;
  margin: 0 0 30px 0;

}

.deep-dive-link {
  padding: 8px 20px;
  background: #003399;
  border-radius: 20px;
  color: #fafafa;
  font-size: 0.9rem;
  font-weight: 600;
  text-decoration: none;
  transition: background 0.2s ease, color 0.2s ease;
  
}

.deep-dive-link:hover {
  background: #e0e7ff;
  color: #3a3fcc;
  
}
/* ── KPI counter row ─────────────────────────────────────── */
.kpi-row {
    display: flex;
    gap: 0;
    /* border: 1.5px solid #b0c4de; */
    border-radius: 8px;
    background: white;
    margin-bottom: 20px;
    overflow: hidden;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05); 
}
.kpi-card {
    flex: 1;
    display: flex;
    flex-direction: column;
    padding: 14px 20px;
    border-right: 4px solid #f5f7f9;
}
.kpi-card:last-child { border-right: none; }
.kpi-header {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 6px;
}
.kpi-label {
    font-size: 0.8rem;
    white-space: nowrap;
    text-align: center;
    color: #2A3F5F;
    margin-bottom: 8px;
}
.kpi-body {
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.kpi-value {
    font-size: 2rem;
    font-weight: 700;
    line-height: 1;
    text-align: center;

}
@media (max-width: 768px) {
    .kpi-row { flex-direction: column; }
    .kpi-card { border-right: none; border-bottom: 1px solid #e0e8f0; }
    .kpi-card:last-child { border-bottom: none; }
}
/* ==========================================================================
   Card Title & Count Badge
   ========================================================================== */

.card__title {
  font-size: 1rem;
  font-weight: 400;
  color: #2a3f5f;
  display: flex;
  align-items: center;
  gap: 8px;
}

.card__count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #1069c0;
  font-size: 1.3rem;
  font-weight: 700;
  letter-spacing: 0.02em;
}

/* ==========================================================================
   Data Table
   ========================================================================== */

.data-table__scroll-wrapper {
  max-height: 320px;        /* ~5 rows visible */
  overflow-y: auto;
  /* keep the thead sticky while scrolling */
  position: relative;
}

.data-table__scroll-wrapper::after {
  content: "";
  position: sticky;
  bottom: 0;
  left: 0;
  display: block;
  width: 100%;
  height: 48px;
  background: linear-gradient(to bottom, transparent, rgba(255, 255, 255, 0.92));
  pointer-events: none;
  border-radius: 0 0 6px 6px;
  transition: opacity 0.2s ease;
}

.data-table__scroll-wrapper.is-scrolled-end::after {
  opacity: 0;
}

/* when wrapped, the table itself handles its own border */
.data-table__scroll-wrapper .data-table {
  border: none;
}

/* Modern standard — Chrome 121+, Firefox, Brave 1.61+ */
@supports (scrollbar-width: auto) {
  .data-table__scroll-wrapper {
    scrollbar-width: thin;
    scrollbar-color: #003399 #f0f4fa;
  }
}

/* Chrome / Edge / Safari / Brave (pre-121) */
@supports selector(::-webkit-scrollbar) {
  .data-table__scroll-wrapper::-webkit-scrollbar {
    width: 6px;
  }

  .data-table__scroll-wrapper::-webkit-scrollbar-track {
    background: #f0f4fa;
    border-radius: 0 6px 6px 0;
  }

  .data-table__scroll-wrapper::-webkit-scrollbar-thumb {
    background-color: #003399;
    border-radius: 6px;
  }

  .data-table__scroll-wrapper::-webkit-scrollbar-thumb:hover {
    background-color: #003399;
  }
}



.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
  color: #2a3f5f;
}

.data-table thead tr {
  background-color: #f0f4fa;
  border-bottom: 2px solid #d0d9e8;
}

.data-table thead th {
  padding: 10px 14px;
  text-align: left;
  font-weight: 700;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #2a3f5f;
  white-space: nowrap;
}

.data-table tbody tr {
  border-bottom: 1px solid #edf0f5;
  transition: background-color 0.15s ease;
}

.data-table tbody tr:last-child {
  border-bottom: none;
}

.data-table tbody tr:hover {
  background-color: #f7f9fd;
}

.data-table td {
  padding: 10px 14px;
  vertical-align: top;
  line-height: 1.5;
}

/* Initiative link column */
.data-table td:first-child {
  font-weight: 600;
  white-space: nowrap;
}

.data-table td:first-child a {
  color: #1069c0;
  text-decoration: none;
}

.data-table td:first-child a:hover {
  text-decoration: underline;
  color: #0a4d9c;
}

/* Objective column — muted, smaller */
.data-table td:nth-child(2) {
  color: #2a3f5f;
  font-size: 0.82rem;
}

.list-empty {
  color: #8a9ab0;
  font-style: italic;
  font-size: 0.875rem;
  margin: 8px 0 0 0;
}

/* Progress bar — base */
.progress-bar {
  margin-top: 5px;
  height: 4px;
  background-color: #e8edf5;
  border-radius: 2px;
  overflow: hidden;
  width: 100%;
}

.progress-bar__fill {
  height: 100%;
  border-radius: 2px;
  transition: width 0.4s ease;
}

/* Signatures — blue, proportional to 1 000 000 target */
.progress-bar__fill--signatures {
  background-color: #4a7fb5;
}

/* Countries threshold — green when making progress, gold when close */
.progress-bar__fill--threshold {
  background-color: #0d9488;
}

/* Overflowing bar — overlays the modifier color when value exceeds max */
.progress-bar__fill--over {
  background-color: #f0a500 !important;
  box-shadow: 0 0 4px rgba(240, 165, 0, 0.5);
}
/* Smooth scroll for the whole page */
@media (prefers-reduced-motion: no-preference) {
  html {
    scroll-behavior: smooth;
  }
}

/* Back-to-top button */
.back-to-top-btn {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  width: 2.75rem;
  height: 2.75rem;
  border-radius: 50%;
  border: none;
  background-color: #0d6efd;   /* adjust to your dashboard accent colour */
  color: #fff;
  font-size: 1.5rem;
  line-height: 1;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);

  /* hidden by default */
  opacity: 0;
  pointer-events: none;
  transform: translateY(0.5rem);
  transition: opacity 0.25s ease, transform 0.25s ease;
  z-index: 999;
}

.back-to-top-btn.visible {
  opacity: 1;
  pointer-events: all;
  transform: translateY(0);
}

.back-to-top-btn:hover {
  background-color: #0b5ed7;
  transform: translateY(-2px);
}

.back-to-top-btn:focus-visible {
  outline: 3px solid #0d6efd;
  outline-offset: 3px;
}

```

`./page_creator/config.py`:
```
import plotly.express as px

COLORS   = px.colors.qualitative.Plotly
MARGIN   = dict(l=20, r=20, t=50, b=20)
HEIGHT   = 400
DIV_ARGS = dict(full_html=False, include_plotlyjs=False, config={"responsive": True})

```

`./page_creator/generate_charts.py`:
```
#!/usr/bin/env python3
import sys
from pathlib import Path

# Ensure project root (parent of page_creator/) is always on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
from page_creator.partials.charts import (
    generate_chart_top_10_signatures,
    generate_chart_outcomes,
    generate_chart_signatures_cohorts,
)
from page_creator.partials.counters import generate_kpi_row
from page_creator.partials.lists import generate_currently_open

CSV_PATH = Path(__file__).parent / "data" / "initiatives.csv"
OUT_DIR = Path(__file__).parent.parent / "page_to_export" / "partials"


def main():
    df = pd.read_csv(CSV_PATH)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print(df.columns)

    charts = {
        "kpi_row.html": generate_kpi_row(df),
        "chart_top_10_signatures.html": generate_chart_top_10_signatures(df),
        "list_currently_open.html": generate_currently_open(df),
        "chart_outcomes.html": generate_chart_outcomes(df),
        "chart_signatures_cohorts.html": generate_chart_signatures_cohorts(df),
    }

    for filename, html in charts.items():
        path = OUT_DIR / filename
        path.write_text(html, encoding="utf-8")
        print(f"  wrote {path}  ({path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()

```

`./page_creator/partials/charts/__init__.py`:
```
from .outcomes import generate_chart_outcomes
from .top_10_signatures import generate_chart_top_10_signatures
from .signatures_cohorts import generate_chart_signatures_cohorts

__all__ = [
    "generate_chart_outcomes",
    "generate_chart_top_10_signatures",
    "generate_chart_signatures_cohorts",
]

```

`./page_creator/partials/charts/outcomes.py`:
```
import pandas as pd
import plotly.graph_objects as go

from page_creator.config import MARGIN, HEIGHT, DIV_ARGS
from page_creator.utils import wrap_card

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

STATUS_COLORS = {
    "Law Passed": "#3CA371",
    "Commission Engaged": "#9CCC65",
    "Collection Ongoing": "#F5A623",
    "Waiting for Response": "#9E9E9E",
    "Withdrawn": "#4B4B4B",
    "Rejected Legislation": "#F44336",
    "Collection Unsuccessful": "#8B1111",
}

DEFAULT_COLOR = "#757575"

MAX_TITLE_LEN = 40
MAX_HOVER_ITEMS = 5


# ------------------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------------------


def _truncate_title(title: str, max_len: int = MAX_TITLE_LEN) -> str:
    return title if len(title) <= max_len else title[: max_len - 1] + "…"


def _eci_list_for_hover(titles: list[str]) -> str:
    if not titles:
        return "No ECIs"
    items = [f"• {_truncate_title(t)}" for t in titles[:MAX_HOVER_ITEMS]]
    result = "<br>".join(items)
    if len(titles) > MAX_HOVER_ITEMS:
        result += f"<br><i>… (and {len(titles) - MAX_HOVER_ITEMS} more)</i>"
    return result


# ------------------------------------------------------------------------------
# Chart
# ------------------------------------------------------------------------------


def generate_chart_outcomes(df: pd.DataFrame) -> str:
    counts = df["current_status"].value_counts().reset_index()
    counts.columns = ["current_status", "count"]

    # Reorder rows to match STATUS_COLORS key order; unknowns go to the end
    status_order = list(STATUS_COLORS.keys())
    counts["_order"] = (
        counts["current_status"]
        .map({s: i for i, s in enumerate(status_order)})
        .fillna(len(status_order))
    )
    counts = counts.sort_values("_order").drop(columns="_order").reset_index(drop=True)

    total = counts["count"].sum()
    counts["percentage"] = (counts["count"] / total * 100).round(1)
    counts["color"] = counts["current_status"].map(
        lambda s: STATUS_COLORS.get(s, DEFAULT_COLOR)
    )
    counts["eci_list"] = counts["current_status"].apply(
        lambda s: _eci_list_for_hover(df[df["current_status"] == s]["title"].tolist())
    )

    # customdata: [0] count  [1] percentage  [2] eci_list
    customdata = counts[["count", "percentage", "eci_list"]].values.tolist()

    fig = go.Figure(
        go.Pie(
            labels=counts["current_status"],
            values=counts["count"],
            hole=0.45,
            marker=dict(colors=counts["color"].tolist()),
            customdata=customdata,
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Count: %{customdata[0][0]}<br>"
                "Percentage: %{customdata[0][1]}%<br><br>"
                "<b>ECIs:</b><br>%{customdata[0][2]}"
                "<extra></extra>"
            ),
            textinfo="percent+label",
            textposition="inside",
            textfont=dict(size=11, color="white", family="Arial Black"),
            sort=False,
        )
    )

    fig.update_layout(
        title="Initiatives by Current Status",
        margin=MARGIN,
        height=HEIGHT,
        width=500,
        showlegend=True,
        legend=dict(
            font=dict(size=12),
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02,
        ),
    )

    return wrap_card(fig.to_html(**DIV_ARGS), extra_class="bottom-col")

```

`./page_creator/partials/charts/signatures_cohorts.py`:
```
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from page_creator.config import MARGIN, HEIGHT, DIV_ARGS
from page_creator.utils import wrap_card

ECI_THRESHOLD = 1_000_000
NUM_BINS = 50
MAX_HOVER_ITEMS = 15


def _get_bin_ecis(df: pd.DataFrame, bin_start: float, bin_end: float) -> str:
    titles = df[
        (df["signatures_collected"] >= bin_start)
        & (df["signatures_collected"] <= bin_end)
    ]["title"].tolist()

    if not titles:
        return "No ECIs"

    items = [f"• {t}" for t in titles[:MAX_HOVER_ITEMS]]
    result = "<br>".join(items)
    if len(titles) > MAX_HOVER_ITEMS:
        result += f"<br><i>... (and {len(titles) - MAX_HOVER_ITEMS} more)</i>"
    return result


def generate_chart_signatures_cohorts(df: pd.DataFrame) -> str:
    sigs = df[df["signatures_collected"].notna()].copy()

    bins = np.linspace(0, sigs["signatures_collected"].max(), NUM_BINS + 1)
    below_bins = bins[bins < ECI_THRESHOLD]
    above_bins = bins[bins >= ECI_THRESHOLD]

    hist_below, edges_below = np.histogram(
        sigs[sigs["signatures_collected"] < ECI_THRESHOLD]["signatures_collected"],
        bins=below_bins,
    )
    hist_above, edges_above = np.histogram(
        sigs[sigs["signatures_collected"] >= ECI_THRESHOLD]["signatures_collected"],
        bins=above_bins,
    )

    centers_below = (edges_below[:-1] + edges_below[1:]) / 2
    centers_above = (edges_above[:-1] + edges_above[1:]) / 2

    eci_lists_below = [
        _get_bin_ecis(sigs, edges_below[i], edges_below[i + 1])
        for i in range(len(edges_below) - 1)
    ]
    eci_lists_above = [
        _get_bin_ecis(sigs, edges_above[i], edges_above[i + 1])
        for i in range(len(edges_above) - 1)
    ]

    colors_below = []
    for center in centers_below:
        ratio = center / ECI_THRESHOLD
        r = int(195 + (255 - 195) * ratio)
        g = int(66 + (244 - 66) * ratio)
        b = int(66 + (79 - 66) * ratio)
        colors_below.append(f"rgb({r},{g},{b})")

    colors_above = []
    for center in centers_above:
        ratio = min((center - ECI_THRESHOLD) / ECI_THRESHOLD, 1.0)
        r = int(184 - (184 - 60) * ratio)
        g = int(216 - (216 - 163) * ratio)
        b = int(127 - (127 - 113) * ratio)
        colors_above.append(f"rgb({r},{g},{b})")

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=centers_below,
            y=hist_below,
            name="Below 1M",
            marker=dict(color=colors_below, line=dict(color="white", width=0.5)),
            width=np.diff(edges_below),
            customdata=eci_lists_below,
            hovertemplate=(
                "<b>Signatures Range:</b> %{x:,.0f}<br>"
                "<b>Count:</b> %{y}<br><br>"
                "<b>ECIs:</b><br>%{customdata}"
                "<extra></extra>"
            ),
        )
    )

    fig.add_trace(
        go.Bar(
            x=centers_above,
            y=hist_above,
            name="Above 1M",
            marker=dict(color=colors_above, line=dict(color="white", width=0.5)),
            width=np.diff(edges_above),
            customdata=eci_lists_above,
            hovertemplate=(
                "<b>Signatures Range:</b> %{x:,.0f}<br>"
                "<b>Count:</b> %{y}<br><br>"
                "<b>ECIs:</b><br>%{customdata}"
                "<extra></extra>"
            ),
        )
    )

    fig.add_vline(
        x=ECI_THRESHOLD,
        line_dash="dash",
        line_color="#3AB23F",
        line_width=3,
        annotation_text="1M Threshold",
        annotation_position="top right",
        annotation_font_size=13,
        annotation_font_color="#3AB23F",
    )

    fig.update_layout(
        title="Distribution of Signature Counts",
        xaxis_title="Signatures Collected",
        yaxis_title="Number of Initiatives",
        margin=MARGIN,
        height=HEIGHT,
        width=620,
        showlegend=True,
        bargap=0.05,
        legend=dict(font=dict(size=13)),
    )

    return wrap_card(fig.to_html(**DIV_ARGS), extra_class="bottom-col")

```

`./page_creator/partials/charts/top_10_signatures.py`:
```
import textwrap

import pandas as pd
import plotly.graph_objects as go

from page_creator.config import MARGIN, HEIGHT, DIV_ARGS
from page_creator.utils import wrap_card

ECI_THRESHOLD = 1_000_000
_WRAP_WIDTH = 60
_CHART_DIV_ID = "chart-top10-signatures"


def _bar_color(signatures: float, max_signatures: float) -> str:
    """Gradient color per bar: dark-red→light-yellow below 1M, light-green→dark-green above."""
    if signatures >= ECI_THRESHOLD:
        ratio = min(
            (signatures - ECI_THRESHOLD) / max(max_signatures - ECI_THRESHOLD, 1), 1.0
        )
        r = int(184 - (184 - 60) * ratio)
        g = int(216 - (216 - 163) * ratio)
        b = int(127 - (127 - 113) * ratio)
    else:
        ratio = signatures / ECI_THRESHOLD
        r = int(195 + (255 - 195) * ratio)
        g = int(66 + (244 - 66) * ratio)
        b = int(66 + (79 - 66) * ratio)
    return f"rgb({r},{g},{b})"


def _hover_wrap(text: str, width: int = _WRAP_WIDTH) -> str:
    """Break long text into <br>-separated lines for Plotly hover tooltips."""
    lines = textwrap.wrap(str(text), width=width)
    return "<br>".join(lines)


def generate_chart_top_10_signatures(df: pd.DataFrame) -> str:
    agg = (
        df.groupby("title", as_index=False)
        .agg(
            signatures_collected=("signatures_collected", "sum"),
            signatures_threshold_met=("signatures_threshold_met", "first"),
            objective=("objective", "first"),
            commission_answer_text=("commission_answer_text", "first"),
            url=("url", "first"),
        )
        .nlargest(10, "signatures_collected")
        .sort_values("signatures_collected", ascending=True)
    )

    agg["objective"] = agg["objective"].apply(_hover_wrap)
    agg["commission_answer_text"] = agg["commission_answer_text"].apply(_hover_wrap)

    max_sigs = agg["signatures_collected"].max()
    colors = [_bar_color(s, max_sigs) for s in agg["signatures_collected"]]

    # customdata: [0] threshold_met  [1] objective  [2] commission_answer_text  [3] url
    customdata = agg[
        [
            "signatures_threshold_met",
            "objective",
            "commission_answer_text",
            "url",
            "registration_year",
        ]
    ].values

    fig = go.Figure(
        go.Bar(
            y=agg["title"],
            x=agg["signatures_collected"],
            orientation="h",
            marker=dict(color=colors, line=dict(color="white", width=0.5)),
            customdata=customdata,
            hovertemplate=(
                "<b>%{y}</b><br><br>"
                "<b>Signatures:</b> %{x:,.0f}<br>"
                "<b>Year:</b> %{customdata[4]}<br>"  # TODO
                "<b>Countries Threshold Met:</b> %{customdata[0]}/27<br><br>"
                "<b>Objective:</b><br>%{customdata[1]}<br><br>"
                "<b>Commission Response:</b><br>%{customdata[2]}<br><br>"
                "<i>🔗 Click to open initiative page</i>"
                "<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        title=dict(
            text="Top 10 Initiatives by Signatures (All-Time)",
            x=0.015,
            xanchor="left",
        ),
        margin=MARGIN,
        height=HEIGHT,
        xaxis_title="Signatures",
        yaxis=dict(
            title="",
            ticksuffix="   ",
        ),
        yaxis_title="",
        showlegend=False,
        clickmode="event",
    )

    fig.add_vline(
        x=ECI_THRESHOLD,
        line_dash="dash",
        line_color="#3AB23F",
        line_width=2,
        annotation_text="1M threshold",
        annotation_position="top right",
        annotation_font_color="#3AB23F",
        annotation_font_size=13,
    )

    chart_html = fig.to_html(**{**DIV_ARGS, "div_id": _CHART_DIV_ID})

    click_js = f"""
<style>
  #{_CHART_DIV_ID} .bars path {{ cursor: pointer !important; }}
</style>
<script>
(function () {{
  var el = document.getElementById("{_CHART_DIV_ID}");
  var drag = el.querySelector(".nsewdrag");

  el.on("plotly_hover", function () {{
    if (drag) drag.style.cursor = "pointer";
  }});
  el.on("plotly_unhover", function () {{
    if (drag) drag.style.cursor = "default";
  }});
  el.on("plotly_click", function (data) {{
    var url = data.points[0].customdata[3];
    if (url) window.open(url, "_blank", "noopener,noreferrer");
  }});
}})();
</script>
"""

    return wrap_card(chart_html + click_js)

```

`./page_creator/partials/counters/__init__.py`:
```
from .kpi_row import generate_kpi_row

__all__ = [
    "generate_kpi_row",
]

```

`./page_creator/partials/counters/kpi_row.py`:
```
import pandas as pd


def generate_kpi_row(df: pd.DataFrame) -> str:
    metrics = [
        {
            "label": "Total Initiatives:",
            "value": len(df),
            "color": "#333",
            "icon": "📋",
        },
        {
            "label": "Currently Open:",
            "value": int((df["current_status"] == "Collection Ongoing").sum()),
            "color": "#1069c0",
            "icon": "🗳️",
        },
        {
            "label": "Reached 1M Signatures:",
            "value": int((df["signatures_collected"] >= 1_000_000).sum()),
            "color": "#557B2D",
            "icon": "✅",
        },
        {
            "label": "Got EU Response:",
            "value": int(
                df["current_status"]
                .isin(["Commission Engaged", "Law Passed", "Rejected Legislation"])
                .sum()
            ),
            "color": "#006064",
            "icon": "📬",
        },
        {
            "label": "Led to Legislation:",
            "value": int((df["current_status"] == "Law Passed").sum()),
            "color": "#6a1b9a",
            "icon": "⚖️",
        },
    ]

    cards = "\n".join(
        f"""      <div class="kpi-card">
        <span class="kpi-label">{m["icon"]} {m["label"]}</span>
        <span class="kpi-value" style="color:{m["color"]}">{m["value"]}</span>
      </div>"""
        for m in metrics
    )

    return f"""<div class="kpi-row">
{cards}
</div>"""

```

`./page_creator/partials/lists/currently_open.py`:
```
import pandas as pd

from page_creator.utils import wrap_card


_STATUS = "Collection Ongoing"
_TRUNCATE = 100
_SCROLL_THRESHOLD = 5
_COUNTRIES_THRESHOLD = 7
_SIG_TARGET = 1_000_000


def _truncate(text: str, max_len: int = _TRUNCATE) -> str:
    if pd.isna(text):
        return ""
    s = str(text)
    return s if len(s) <= max_len else s[: max_len - 1] + "…"


def _progress_bar(pct: float, modifier: str = "") -> str:
    clamped = min(max(pct, 0.0), 100.0)
    over = pct > 100.0
    mod_class = f" progress-bar__fill--{modifier}" if modifier else ""
    over_class = " progress-bar__fill--over" if over else ""
    return (
        f'<div class="progress-bar">'
        f'<div class="progress-bar__fill{mod_class}{over_class}" style="width:{clamped:.1f}%">'
        f"</div></div>"
    )


def generate_currently_open(df: pd.DataFrame) -> str:
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
        name = row["title"]
        objective = _truncate(row.get("objective", ""))

        if pd.notna(row["signatures_collected"]):
            sig_val = int(row["signatures_collected"])
            sig_pct = sig_val / _SIG_TARGET * 100
            sigs = f"{sig_val:,}{_progress_bar(sig_pct, 'signatures')}"
        else:
            sigs = "N/A"

        if pd.notna(row["signatures_threshold_met"]):
            thr_val = int(row["signatures_threshold_met"])
            thr_pct = thr_val / _COUNTRIES_THRESHOLD * 100
            threshold = f"{thr_val} / {_COUNTRIES_THRESHOLD}{_progress_bar(thr_pct, 'threshold')}"
        else:
            threshold = "N/A"

        rows += f"""
        <tr>
          <td><a href="{url}" target="_blank" rel="noopener noreferrer">{name}</a></td>
          <td>{objective}</td>
          <td>{sigs}</td>
          <td>{threshold}</td>
        </tr>"""

    scrollable = len(open_df) > _SCROLL_THRESHOLD
    table_wrapper_open = (
        '<div class="data-table__scroll-wrapper">' if scrollable else ""
    )
    table_wrapper_close = "</div>" if scrollable else ""

    table = f"""
{table_wrapper_open}
<table class="data-table">
  <thead>
    <tr>
      <th>Initiative</th>
      <th>Objective</th>
      <th>Signatures</th>
      <th>Countries Threshold</th>
    </tr>
  </thead>
  <tbody>
    {rows}
  </tbody>
</table>
{table_wrapper_close}"""

    return wrap_card(title + table)

```

`./page_creator/partials/lists/__init__.py`:
```
from .currently_open import generate_currently_open

__all__ = ["generate_currently_open"]

```

`./page_creator/pyproject.toml`:
```
[project]
name = "page-creator"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "pandas",
    "plotly",
]

[project.scripts]
generate = "generate_charts:main"

```

`./page_creator/utils.py`:
```
def wrap_card(inner_html: str, extra_class: str = "") -> str:
    cls = f"card {extra_class}".strip()
    return f'''<div class="{cls}">\n{inner_html}\n</div>'''

```

`./page_creator/uv.lock`:
```
version = 1
revision = 3
requires-python = ">=3.11"
resolution-markers = [
    "python_full_version >= '3.14' and sys_platform == 'win32'",
    "python_full_version >= '3.14' and sys_platform == 'emscripten'",
    "python_full_version >= '3.14' and sys_platform != 'emscripten' and sys_platform != 'win32'",
    "python_full_version < '3.14' and sys_platform == 'win32'",
    "python_full_version < '3.14' and sys_platform == 'emscripten'",
    "python_full_version < '3.14' and sys_platform != 'emscripten' and sys_platform != 'win32'",
]

[[package]]
name = "narwhals"
version = "2.17.0"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/75/59/81d0f4cad21484083466f278e6b392addd9f4205b48d45b5c8771670ebf8/narwhals-2.17.0.tar.gz", hash = "sha256:ebd5bc95bcfa2f8e89a8ac09e2765a63055162837208e67b42d6eeb6651d5e67", size = 620306, upload-time = "2026-02-23T09:44:34.142Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/4b/27/20770bd6bf8fbe1e16f848ba21da9df061f38d2e6483952c29d2bb5d1d8b/narwhals-2.17.0-py3-none-any.whl", hash = "sha256:2ac5307b7c2b275a7d66eeda906b8605e3d7a760951e188dcfff86e8ebe083dd", size = 444897, upload-time = "2026-02-23T09:44:32.006Z" },
]

[[package]]
name = "numpy"
version = "2.4.2"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/57/fd/0005efbd0af48e55eb3c7208af93f2862d4b1a56cd78e84309a2d959208d/numpy-2.4.2.tar.gz", hash = "sha256:659a6107e31a83c4e33f763942275fd278b21d095094044eb35569e86a21ddae", size = 20723651, upload-time = "2026-01-31T23:13:10.135Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/d3/44/71852273146957899753e69986246d6a176061ea183407e95418c2aa4d9a/numpy-2.4.2-cp311-cp311-macosx_10_9_x86_64.whl", hash = "sha256:e7e88598032542bd49af7c4747541422884219056c268823ef6e5e89851c8825", size = 16955478, upload-time = "2026-01-31T23:10:25.623Z" },
    { url = "https://files.pythonhosted.org/packages/74/41/5d17d4058bd0cd96bcbd4d9ff0fb2e21f52702aab9a72e4a594efa18692f/numpy-2.4.2-cp311-cp311-macosx_11_0_arm64.whl", hash = "sha256:7edc794af8b36ca37ef5fcb5e0d128c7e0595c7b96a2318d1badb6fcd8ee86b1", size = 14965467, upload-time = "2026-01-31T23:10:28.186Z" },
    { url = "https://files.pythonhosted.org/packages/49/48/fb1ce8136c19452ed15f033f8aee91d5defe515094e330ce368a0647846f/numpy-2.4.2-cp311-cp311-macosx_14_0_arm64.whl", hash = "sha256:6e9f61981ace1360e42737e2bae58b27bf28a1b27e781721047d84bd754d32e7", size = 5475172, upload-time = "2026-01-31T23:10:30.848Z" },
    { url = "https://files.pythonhosted.org/packages/40/a9/3feb49f17bbd1300dd2570432961f5c8a4ffeff1db6f02c7273bd020a4c9/numpy-2.4.2-cp311-cp311-macosx_14_0_x86_64.whl", hash = "sha256:cb7bbb88aa74908950d979eeaa24dbdf1a865e3c7e45ff0121d8f70387b55f73", size = 6805145, upload-time = "2026-01-31T23:10:32.352Z" },
    { url = "https://files.pythonhosted.org/packages/3f/39/fdf35cbd6d6e2fcad42fcf85ac04a85a0d0fbfbf34b30721c98d602fd70a/numpy-2.4.2-cp311-cp311-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:4f069069931240b3fc703f1e23df63443dbd6390614c8c44a87d96cd0ec81eb1", size = 15966084, upload-time = "2026-01-31T23:10:34.502Z" },
    { url = "https://files.pythonhosted.org/packages/1b/46/6fa4ea94f1ddf969b2ee941290cca6f1bfac92b53c76ae5f44afe17ceb69/numpy-2.4.2-cp311-cp311-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:c02ef4401a506fb60b411467ad501e1429a3487abca4664871d9ae0b46c8ba32", size = 16899477, upload-time = "2026-01-31T23:10:37.075Z" },
    { url = "https://files.pythonhosted.org/packages/09/a1/2a424e162b1a14a5bd860a464ab4e07513916a64ab1683fae262f735ccd2/numpy-2.4.2-cp311-cp311-musllinux_1_2_aarch64.whl", hash = "sha256:2653de5c24910e49c2b106499803124dde62a5a1fe0eedeaecf4309a5f639390", size = 17323429, upload-time = "2026-01-31T23:10:39.704Z" },
    { url = "https://files.pythonhosted.org/packages/ce/a2/73014149ff250628df72c58204822ac01d768697913881aacf839ff78680/numpy-2.4.2-cp311-cp311-musllinux_1_2_x86_64.whl", hash = "sha256:1ae241bbfc6ae276f94a170b14785e561cb5e7f626b6688cf076af4110887413", size = 18635109, upload-time = "2026-01-31T23:10:41.924Z" },
    { url = "https://files.pythonhosted.org/packages/6c/0c/73e8be2f1accd56df74abc1c5e18527822067dced5ec0861b5bb882c2ce0/numpy-2.4.2-cp311-cp311-win32.whl", hash = "sha256:df1b10187212b198dd45fa943d8985a3c8cf854aed4923796e0e019e113a1bda", size = 6237915, upload-time = "2026-01-31T23:10:45.26Z" },
    { url = "https://files.pythonhosted.org/packages/76/ae/e0265e0163cf127c24c3969d29f1c4c64551a1e375d95a13d32eab25d364/numpy-2.4.2-cp311-cp311-win_amd64.whl", hash = "sha256:b9c618d56a29c9cb1c4da979e9899be7578d2e0b3c24d52079c166324c9e8695", size = 12607972, upload-time = "2026-01-31T23:10:47.021Z" },
    { url = "https://files.pythonhosted.org/packages/29/a5/c43029af9b8014d6ea157f192652c50042e8911f4300f8f6ed3336bf437f/numpy-2.4.2-cp311-cp311-win_arm64.whl", hash = "sha256:47c5a6ed21d9452b10227e5e8a0e1c22979811cad7dcc19d8e3e2fb8fa03f1a3", size = 10485763, upload-time = "2026-01-31T23:10:50.087Z" },
    { url = "https://files.pythonhosted.org/packages/51/6e/6f394c9c77668153e14d4da83bcc247beb5952f6ead7699a1a2992613bea/numpy-2.4.2-cp312-cp312-macosx_10_13_x86_64.whl", hash = "sha256:21982668592194c609de53ba4933a7471880ccbaadcc52352694a59ecc860b3a", size = 16667963, upload-time = "2026-01-31T23:10:52.147Z" },
    { url = "https://files.pythonhosted.org/packages/1f/f8/55483431f2b2fd015ae6ed4fe62288823ce908437ed49db5a03d15151678/numpy-2.4.2-cp312-cp312-macosx_11_0_arm64.whl", hash = "sha256:40397bda92382fcec844066efb11f13e1c9a3e2a8e8f318fb72ed8b6db9f60f1", size = 14693571, upload-time = "2026-01-31T23:10:54.789Z" },
    { url = "https://files.pythonhosted.org/packages/2f/20/18026832b1845cdc82248208dd929ca14c9d8f2bac391f67440707fff27c/numpy-2.4.2-cp312-cp312-macosx_14_0_arm64.whl", hash = "sha256:b3a24467af63c67829bfaa61eecf18d5432d4f11992688537be59ecd6ad32f5e", size = 5203469, upload-time = "2026-01-31T23:10:57.343Z" },
    { url = "https://files.pythonhosted.org/packages/7d/33/2eb97c8a77daaba34eaa3fa7241a14ac5f51c46a6bd5911361b644c4a1e2/numpy-2.4.2-cp312-cp312-macosx_14_0_x86_64.whl", hash = "sha256:805cc8de9fd6e7a22da5aed858e0ab16be5a4db6c873dde1d7451c541553aa27", size = 6550820, upload-time = "2026-01-31T23:10:59.429Z" },
    { url = "https://files.pythonhosted.org/packages/b1/91/b97fdfd12dc75b02c44e26c6638241cc004d4079a0321a69c62f51470c4c/numpy-2.4.2-cp312-cp312-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:6d82351358ffbcdcd7b686b90742a9b86632d6c1c051016484fa0b326a0a1548", size = 15663067, upload-time = "2026-01-31T23:11:01.291Z" },
    { url = "https://files.pythonhosted.org/packages/f5/c6/a18e59f3f0b8071cc85cbc8d80cd02d68aa9710170b2553a117203d46936/numpy-2.4.2-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:9e35d3e0144137d9fdae62912e869136164534d64a169f86438bc9561b6ad49f", size = 16619782, upload-time = "2026-01-31T23:11:03.669Z" },
    { url = "https://files.pythonhosted.org/packages/b7/83/9751502164601a79e18847309f5ceec0b1446d7b6aa12305759b72cf98b2/numpy-2.4.2-cp312-cp312-musllinux_1_2_aarch64.whl", hash = "sha256:adb6ed2ad29b9e15321d167d152ee909ec73395901b70936f029c3bc6d7f4460", size = 17013128, upload-time = "2026-01-31T23:11:05.913Z" },
    { url = "https://files.pythonhosted.org/packages/61/c4/c4066322256ec740acc1c8923a10047818691d2f8aec254798f3dd90f5f2/numpy-2.4.2-cp312-cp312-musllinux_1_2_x86_64.whl", hash = "sha256:8906e71fd8afcb76580404e2a950caef2685df3d2a57fe82a86ac8d33cc007ba", size = 18345324, upload-time = "2026-01-31T23:11:08.248Z" },
    { url = "https://files.pythonhosted.org/packages/ab/af/6157aa6da728fa4525a755bfad486ae7e3f76d4c1864138003eb84328497/numpy-2.4.2-cp312-cp312-win32.whl", hash = "sha256:ec055f6dae239a6299cace477b479cca2fc125c5675482daf1dd886933a1076f", size = 5960282, upload-time = "2026-01-31T23:11:10.497Z" },
    { url = "https://files.pythonhosted.org/packages/92/0f/7ceaaeaacb40567071e94dbf2c9480c0ae453d5bb4f52bea3892c39dc83c/numpy-2.4.2-cp312-cp312-win_amd64.whl", hash = "sha256:209fae046e62d0ce6435fcfe3b1a10537e858249b3d9b05829e2a05218296a85", size = 12314210, upload-time = "2026-01-31T23:11:12.176Z" },
    { url = "https://files.pythonhosted.org/packages/2f/a3/56c5c604fae6dd40fa2ed3040d005fca97e91bd320d232ac9931d77ba13c/numpy-2.4.2-cp312-cp312-win_arm64.whl", hash = "sha256:fbde1b0c6e81d56f5dccd95dd4a711d9b95df1ae4009a60887e56b27e8d903fa", size = 10220171, upload-time = "2026-01-31T23:11:14.684Z" },
    { url = "https://files.pythonhosted.org/packages/a1/22/815b9fe25d1d7ae7d492152adbc7226d3eff731dffc38fe970589fcaaa38/numpy-2.4.2-cp313-cp313-macosx_10_13_x86_64.whl", hash = "sha256:25f2059807faea4b077a2b6837391b5d830864b3543627f381821c646f31a63c", size = 16663696, upload-time = "2026-01-31T23:11:17.516Z" },
    { url = "https://files.pythonhosted.org/packages/09/f0/817d03a03f93ba9c6c8993de509277d84e69f9453601915e4a69554102a1/numpy-2.4.2-cp313-cp313-macosx_11_0_arm64.whl", hash = "sha256:bd3a7a9f5847d2fb8c2c6d1c862fa109c31a9abeca1a3c2bd5a64572955b2979", size = 14688322, upload-time = "2026-01-31T23:11:19.883Z" },
    { url = "https://files.pythonhosted.org/packages/da/b4/f805ab79293c728b9a99438775ce51885fd4f31b76178767cfc718701a39/numpy-2.4.2-cp313-cp313-macosx_14_0_arm64.whl", hash = "sha256:8e4549f8a3c6d13d55041925e912bfd834285ef1dd64d6bc7d542583355e2e98", size = 5198157, upload-time = "2026-01-31T23:11:22.375Z" },
    { url = "https://files.pythonhosted.org/packages/74/09/826e4289844eccdcd64aac27d13b0fd3f32039915dd5b9ba01baae1f436c/numpy-2.4.2-cp313-cp313-macosx_14_0_x86_64.whl", hash = "sha256:aea4f66ff44dfddf8c2cffd66ba6538c5ec67d389285292fe428cb2c738c8aef", size = 6546330, upload-time = "2026-01-31T23:11:23.958Z" },
    { url = "https://files.pythonhosted.org/packages/19/fb/cbfdbfa3057a10aea5422c558ac57538e6acc87ec1669e666d32ac198da7/numpy-2.4.2-cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:c3cd545784805de05aafe1dde61752ea49a359ccba9760c1e5d1c88a93bbf2b7", size = 15660968, upload-time = "2026-01-31T23:11:25.713Z" },
    { url = "https://files.pythonhosted.org/packages/04/dc/46066ce18d01645541f0186877377b9371b8fa8017fa8262002b4ef22612/numpy-2.4.2-cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:d0d9b7c93578baafcbc5f0b83eaf17b79d345c6f36917ba0c67f45226911d499", size = 16607311, upload-time = "2026-01-31T23:11:28.117Z" },
    { url = "https://files.pythonhosted.org/packages/14/d9/4b5adfc39a43fa6bf918c6d544bc60c05236cc2f6339847fc5b35e6cb5b0/numpy-2.4.2-cp313-cp313-musllinux_1_2_aarch64.whl", hash = "sha256:f74f0f7779cc7ae07d1810aab8ac6b1464c3eafb9e283a40da7309d5e6e48fbb", size = 17012850, upload-time = "2026-01-31T23:11:30.888Z" },
    { url = "https://files.pythonhosted.org/packages/b7/20/adb6e6adde6d0130046e6fdfb7675cc62bc2f6b7b02239a09eb58435753d/numpy-2.4.2-cp313-cp313-musllinux_1_2_x86_64.whl", hash = "sha256:c7ac672d699bf36275c035e16b65539931347d68b70667d28984c9fb34e07fa7", size = 18334210, upload-time = "2026-01-31T23:11:33.214Z" },
    { url = "https://files.pythonhosted.org/packages/78/0e/0a73b3dff26803a8c02baa76398015ea2a5434d9b8265a7898a6028c1591/numpy-2.4.2-cp313-cp313-win32.whl", hash = "sha256:8e9afaeb0beff068b4d9cd20d322ba0ee1cecfb0b08db145e4ab4dd44a6b5110", size = 5958199, upload-time = "2026-01-31T23:11:35.385Z" },
    { url = "https://files.pythonhosted.org/packages/43/bc/6352f343522fcb2c04dbaf94cb30cca6fd32c1a750c06ad6231b4293708c/numpy-2.4.2-cp313-cp313-win_amd64.whl", hash = "sha256:7df2de1e4fba69a51c06c28f5a3de36731eb9639feb8e1cf7e4a7b0daf4cf622", size = 12310848, upload-time = "2026-01-31T23:11:38.001Z" },
    { url = "https://files.pythonhosted.org/packages/6e/8d/6da186483e308da5da1cc6918ce913dcfe14ffde98e710bfeff2a6158d4e/numpy-2.4.2-cp313-cp313-win_arm64.whl", hash = "sha256:0fece1d1f0a89c16b03442eae5c56dc0be0c7883b5d388e0c03f53019a4bfd71", size = 10221082, upload-time = "2026-01-31T23:11:40.392Z" },
    { url = "https://files.pythonhosted.org/packages/25/a1/9510aa43555b44781968935c7548a8926274f815de42ad3997e9e83680dd/numpy-2.4.2-cp313-cp313t-macosx_11_0_arm64.whl", hash = "sha256:5633c0da313330fd20c484c78cdd3f9b175b55e1a766c4a174230c6b70ad8262", size = 14815866, upload-time = "2026-01-31T23:11:42.495Z" },
    { url = "https://files.pythonhosted.org/packages/36/30/6bbb5e76631a5ae46e7923dd16ca9d3f1c93cfa8d4ed79a129814a9d8db3/numpy-2.4.2-cp313-cp313t-macosx_14_0_arm64.whl", hash = "sha256:d9f64d786b3b1dd742c946c42d15b07497ed14af1a1f3ce840cce27daa0ce913", size = 5325631, upload-time = "2026-01-31T23:11:44.7Z" },
    { url = "https://files.pythonhosted.org/packages/46/00/3a490938800c1923b567b3a15cd17896e68052e2145d8662aaf3e1ffc58f/numpy-2.4.2-cp313-cp313t-macosx_14_0_x86_64.whl", hash = "sha256:b21041e8cb6a1eb5312dd1d2f80a94d91efffb7a06b70597d44f1bd2dfc315ab", size = 6646254, upload-time = "2026-01-31T23:11:46.341Z" },
    { url = "https://files.pythonhosted.org/packages/d3/e9/fac0890149898a9b609caa5af7455a948b544746e4b8fe7c212c8edd71f8/numpy-2.4.2-cp313-cp313t-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:00ab83c56211a1d7c07c25e3217ea6695e50a3e2f255053686b081dc0b091a82", size = 15720138, upload-time = "2026-01-31T23:11:48.082Z" },
    { url = "https://files.pythonhosted.org/packages/ea/5c/08887c54e68e1e28df53709f1893ce92932cc6f01f7c3d4dc952f61ffd4e/numpy-2.4.2-cp313-cp313t-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:2fb882da679409066b4603579619341c6d6898fc83a8995199d5249f986e8e8f", size = 16655398, upload-time = "2026-01-31T23:11:50.293Z" },
    { url = "https://files.pythonhosted.org/packages/4d/89/253db0fa0e66e9129c745e4ef25631dc37d5f1314dad2b53e907b8538e6d/numpy-2.4.2-cp313-cp313t-musllinux_1_2_aarch64.whl", hash = "sha256:66cb9422236317f9d44b67b4d18f44efe6e9c7f8794ac0462978513359461554", size = 17079064, upload-time = "2026-01-31T23:11:52.927Z" },
    { url = "https://files.pythonhosted.org/packages/2a/d5/cbade46ce97c59c6c3da525e8d95b7abe8a42974a1dc5c1d489c10433e88/numpy-2.4.2-cp313-cp313t-musllinux_1_2_x86_64.whl", hash = "sha256:0f01dcf33e73d80bd8dc0f20a71303abbafa26a19e23f6b68d1aa9990af90257", size = 18379680, upload-time = "2026-01-31T23:11:55.22Z" },
    { url = "https://files.pythonhosted.org/packages/40/62/48f99ae172a4b63d981babe683685030e8a3df4f246c893ea5c6ef99f018/numpy-2.4.2-cp313-cp313t-win32.whl", hash = "sha256:52b913ec40ff7ae845687b0b34d8d93b60cb66dcee06996dd5c99f2fc9328657", size = 6082433, upload-time = "2026-01-31T23:11:58.096Z" },
    { url = "https://files.pythonhosted.org/packages/07/38/e054a61cfe48ad9f1ed0d188e78b7e26859d0b60ef21cd9de4897cdb5326/numpy-2.4.2-cp313-cp313t-win_amd64.whl", hash = "sha256:5eea80d908b2c1f91486eb95b3fb6fab187e569ec9752ab7d9333d2e66bf2d6b", size = 12451181, upload-time = "2026-01-31T23:11:59.782Z" },
    { url = "https://files.pythonhosted.org/packages/6e/a4/a05c3a6418575e185dd84d0b9680b6bb2e2dc3e4202f036b7b4e22d6e9dc/numpy-2.4.2-cp313-cp313t-win_arm64.whl", hash = "sha256:fd49860271d52127d61197bb50b64f58454e9f578cb4b2c001a6de8b1f50b0b1", size = 10290756, upload-time = "2026-01-31T23:12:02.438Z" },
    { url = "https://files.pythonhosted.org/packages/18/88/b7df6050bf18fdcfb7046286c6535cabbdd2064a3440fca3f069d319c16e/numpy-2.4.2-cp314-cp314-macosx_10_15_x86_64.whl", hash = "sha256:444be170853f1f9d528428eceb55f12918e4fda5d8805480f36a002f1415e09b", size = 16663092, upload-time = "2026-01-31T23:12:04.521Z" },
    { url = "https://files.pythonhosted.org/packages/25/7a/1fee4329abc705a469a4afe6e69b1ef7e915117747886327104a8493a955/numpy-2.4.2-cp314-cp314-macosx_11_0_arm64.whl", hash = "sha256:d1240d50adff70c2a88217698ca844723068533f3f5c5fa6ee2e3220e3bdb000", size = 14698770, upload-time = "2026-01-31T23:12:06.96Z" },
    { url = "https://files.pythonhosted.org/packages/fb/0b/f9e49ba6c923678ad5bc38181c08ac5e53b7a5754dbca8e581aa1a56b1ff/numpy-2.4.2-cp314-cp314-macosx_14_0_arm64.whl", hash = "sha256:7cdde6de52fb6664b00b056341265441192d1291c130e99183ec0d4b110ff8b1", size = 5208562, upload-time = "2026-01-31T23:12:09.632Z" },
    { url = "https://files.pythonhosted.org/packages/7d/12/d7de8f6f53f9bb76997e5e4c069eda2051e3fe134e9181671c4391677bb2/numpy-2.4.2-cp314-cp314-macosx_14_0_x86_64.whl", hash = "sha256:cda077c2e5b780200b6b3e09d0b42205a3d1c68f30c6dceb90401c13bff8fe74", size = 6543710, upload-time = "2026-01-31T23:12:11.969Z" },
    { url = "https://files.pythonhosted.org/packages/09/63/c66418c2e0268a31a4cf8a8b512685748200f8e8e8ec6c507ce14e773529/numpy-2.4.2-cp314-cp314-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:d30291931c915b2ab5717c2974bb95ee891a1cf22ebc16a8006bd59cd210d40a", size = 15677205, upload-time = "2026-01-31T23:12:14.33Z" },
    { url = "https://files.pythonhosted.org/packages/5d/6c/7f237821c9642fb2a04d2f1e88b4295677144ca93285fd76eff3bcba858d/numpy-2.4.2-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:bba37bc29d4d85761deed3954a1bc62be7cf462b9510b51d367b769a8c8df325", size = 16611738, upload-time = "2026-01-31T23:12:16.525Z" },
    { url = "https://files.pythonhosted.org/packages/c2/a7/39c4cdda9f019b609b5c473899d87abff092fc908cfe4d1ecb2fcff453b0/numpy-2.4.2-cp314-cp314-musllinux_1_2_aarch64.whl", hash = "sha256:b2f0073ed0868db1dcd86e052d37279eef185b9c8db5bf61f30f46adac63c909", size = 17028888, upload-time = "2026-01-31T23:12:19.306Z" },
    { url = "https://files.pythonhosted.org/packages/da/b3/e84bb64bdfea967cc10950d71090ec2d84b49bc691df0025dddb7c26e8e3/numpy-2.4.2-cp314-cp314-musllinux_1_2_x86_64.whl", hash = "sha256:7f54844851cdb630ceb623dcec4db3240d1ac13d4990532446761baede94996a", size = 18339556, upload-time = "2026-01-31T23:12:21.816Z" },
    { url = "https://files.pythonhosted.org/packages/88/f5/954a291bc1192a27081706862ac62bb5920fbecfbaa302f64682aa90beed/numpy-2.4.2-cp314-cp314-win32.whl", hash = "sha256:12e26134a0331d8dbd9351620f037ec470b7c75929cb8a1537f6bfe411152a1a", size = 6006899, upload-time = "2026-01-31T23:12:24.14Z" },
    { url = "https://files.pythonhosted.org/packages/05/cb/eff72a91b2efdd1bc98b3b8759f6a1654aa87612fc86e3d87d6fe4f948c4/numpy-2.4.2-cp314-cp314-win_amd64.whl", hash = "sha256:068cdb2d0d644cdb45670810894f6a0600797a69c05f1ac478e8d31670b8ee75", size = 12443072, upload-time = "2026-01-31T23:12:26.33Z" },
    { url = "https://files.pythonhosted.org/packages/37/75/62726948db36a56428fce4ba80a115716dc4fad6a3a4352487f8bb950966/numpy-2.4.2-cp314-cp314-win_arm64.whl", hash = "sha256:6ed0be1ee58eef41231a5c943d7d1375f093142702d5723ca2eb07db9b934b05", size = 10494886, upload-time = "2026-01-31T23:12:28.488Z" },
    { url = "https://files.pythonhosted.org/packages/36/2f/ee93744f1e0661dc267e4b21940870cabfae187c092e1433b77b09b50ac4/numpy-2.4.2-cp314-cp314t-macosx_11_0_arm64.whl", hash = "sha256:98f16a80e917003a12c0580f97b5f875853ebc33e2eaa4bccfc8201ac6869308", size = 14818567, upload-time = "2026-01-31T23:12:30.709Z" },
    { url = "https://files.pythonhosted.org/packages/a7/24/6535212add7d76ff938d8bdc654f53f88d35cddedf807a599e180dcb8e66/numpy-2.4.2-cp314-cp314t-macosx_14_0_arm64.whl", hash = "sha256:20abd069b9cda45874498b245c8015b18ace6de8546bf50dfa8cea1696ed06ef", size = 5328372, upload-time = "2026-01-31T23:12:32.962Z" },
    { url = "https://files.pythonhosted.org/packages/5e/9d/c48f0a035725f925634bf6b8994253b43f2047f6778a54147d7e213bc5a7/numpy-2.4.2-cp314-cp314t-macosx_14_0_x86_64.whl", hash = "sha256:e98c97502435b53741540a5717a6749ac2ada901056c7db951d33e11c885cc7d", size = 6649306, upload-time = "2026-01-31T23:12:34.797Z" },
    { url = "https://files.pythonhosted.org/packages/81/05/7c73a9574cd4a53a25907bad38b59ac83919c0ddc8234ec157f344d57d9a/numpy-2.4.2-cp314-cp314t-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:da6cad4e82cb893db4b69105c604d805e0c3ce11501a55b5e9f9083b47d2ffe8", size = 15722394, upload-time = "2026-01-31T23:12:36.565Z" },
    { url = "https://files.pythonhosted.org/packages/35/fa/4de10089f21fc7d18442c4a767ab156b25c2a6eaf187c0db6d9ecdaeb43f/numpy-2.4.2-cp314-cp314t-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:9e4424677ce4b47fe73c8b5556d876571f7c6945d264201180db2dc34f676ab5", size = 16653343, upload-time = "2026-01-31T23:12:39.188Z" },
    { url = "https://files.pythonhosted.org/packages/b8/f9/d33e4ffc857f3763a57aa85650f2e82486832d7492280ac21ba9efda80da/numpy-2.4.2-cp314-cp314t-musllinux_1_2_aarch64.whl", hash = "sha256:2b8f157c8a6f20eb657e240f8985cc135598b2b46985c5bccbde7616dc9c6b1e", size = 17078045, upload-time = "2026-01-31T23:12:42.041Z" },
    { url = "https://files.pythonhosted.org/packages/c8/b8/54bdb43b6225badbea6389fa038c4ef868c44f5890f95dd530a218706da3/numpy-2.4.2-cp314-cp314t-musllinux_1_2_x86_64.whl", hash = "sha256:5daf6f3914a733336dab21a05cdec343144600e964d2fcdabaac0c0269874b2a", size = 18380024, upload-time = "2026-01-31T23:12:44.331Z" },
    { url = "https://files.pythonhosted.org/packages/a5/55/6e1a61ded7af8df04016d81b5b02daa59f2ea9252ee0397cb9f631efe9e5/numpy-2.4.2-cp314-cp314t-win32.whl", hash = "sha256:8c50dd1fc8826f5b26a5ee4d77ca55d88a895f4e4819c7ecc2a9f5905047a443", size = 6153937, upload-time = "2026-01-31T23:12:47.229Z" },
    { url = "https://files.pythonhosted.org/packages/45/aa/fa6118d1ed6d776b0983f3ceac9b1a5558e80df9365b1c3aa6d42bf9eee4/numpy-2.4.2-cp314-cp314t-win_amd64.whl", hash = "sha256:fcf92bee92742edd401ba41135185866f7026c502617f422eb432cfeca4fe236", size = 12631844, upload-time = "2026-01-31T23:12:48.997Z" },
    { url = "https://files.pythonhosted.org/packages/32/0a/2ec5deea6dcd158f254a7b372fb09cfba5719419c8d66343bab35237b3fb/numpy-2.4.2-cp314-cp314t-win_arm64.whl", hash = "sha256:1f92f53998a17265194018d1cc321b2e96e900ca52d54c7c77837b71b9465181", size = 10565379, upload-time = "2026-01-31T23:12:51.345Z" },
    { url = "https://files.pythonhosted.org/packages/f4/f8/50e14d36d915ef64d8f8bc4a087fc8264d82c785eda6711f80ab7e620335/numpy-2.4.2-pp311-pypy311_pp73-macosx_10_15_x86_64.whl", hash = "sha256:89f7268c009bc492f506abd6f5265defa7cb3f7487dc21d357c3d290add45082", size = 16833179, upload-time = "2026-01-31T23:12:53.5Z" },
    { url = "https://files.pythonhosted.org/packages/17/17/809b5cad63812058a8189e91a1e2d55a5a18fd04611dbad244e8aeae465c/numpy-2.4.2-pp311-pypy311_pp73-macosx_11_0_arm64.whl", hash = "sha256:e6dee3bb76aa4009d5a912180bf5b2de012532998d094acee25d9cb8dee3e44a", size = 14889755, upload-time = "2026-01-31T23:12:55.933Z" },
    { url = "https://files.pythonhosted.org/packages/3e/ea/181b9bcf7627fc8371720316c24db888dcb9829b1c0270abf3d288b2e29b/numpy-2.4.2-pp311-pypy311_pp73-macosx_14_0_arm64.whl", hash = "sha256:cd2bd2bbed13e213d6b55dc1d035a4f91748a7d3edc9480c13898b0353708920", size = 5399500, upload-time = "2026-01-31T23:12:58.671Z" },
    { url = "https://files.pythonhosted.org/packages/33/9f/413adf3fc955541ff5536b78fcf0754680b3c6d95103230252a2c9408d23/numpy-2.4.2-pp311-pypy311_pp73-macosx_14_0_x86_64.whl", hash = "sha256:cf28c0c1d4c4bf00f509fa7eb02c58d7caf221b50b467bcb0d9bbf1584d5c821", size = 6714252, upload-time = "2026-01-31T23:13:00.518Z" },
    { url = "https://files.pythonhosted.org/packages/91/da/643aad274e29ccbdf42ecd94dafe524b81c87bcb56b83872d54827f10543/numpy-2.4.2-pp311-pypy311_pp73-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:e04ae107ac591763a47398bb45b568fc38f02dbc4aa44c063f67a131f99346cb", size = 15797142, upload-time = "2026-01-31T23:13:02.219Z" },
    { url = "https://files.pythonhosted.org/packages/66/27/965b8525e9cb5dc16481b30a1b3c21e50c7ebf6e9dbd48d0c4d0d5089c7e/numpy-2.4.2-pp311-pypy311_pp73-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:602f65afdef699cda27ec0b9224ae5dc43e328f4c24c689deaf77133dbee74d0", size = 16727979, upload-time = "2026-01-31T23:13:04.62Z" },
    { url = "https://files.pythonhosted.org/packages/de/e5/b7d20451657664b07986c2f6e3be564433f5dcaf3482d68eaecd79afaf03/numpy-2.4.2-pp311-pypy311_pp73-win_amd64.whl", hash = "sha256:be71bf1edb48ebbbf7f6337b5bfd2f895d1902f6335a5830b20141fc126ffba0", size = 12502577, upload-time = "2026-01-31T23:13:07.08Z" },
]

[[package]]
name = "packaging"
version = "26.0"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/65/ee/299d360cdc32edc7d2cf530f3accf79c4fca01e96ffc950d8a52213bd8e4/packaging-26.0.tar.gz", hash = "sha256:00243ae351a257117b6a241061796684b084ed1c516a08c48a3f7e147a9d80b4", size = 143416, upload-time = "2026-01-21T20:50:39.064Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/b7/b9/c538f279a4e237a006a2c98387d081e9eb060d203d8ed34467cc0f0b9b53/packaging-26.0-py3-none-any.whl", hash = "sha256:b36f1fef9334a5588b4166f8bcd26a14e521f2b55e6b9de3aaa80d3ff7a37529", size = 74366, upload-time = "2026-01-21T20:50:37.788Z" },
]

[[package]]
name = "page-creator"
version = "0.1.0"
source = { virtual = "." }
dependencies = [
    { name = "pandas" },
    { name = "plotly" },
]

[package.metadata]
requires-dist = [
    { name = "pandas" },
    { name = "plotly" },
]

[[package]]
name = "pandas"
version = "3.0.1"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "numpy" },
    { name = "python-dateutil" },
    { name = "tzdata", marker = "sys_platform == 'emscripten' or sys_platform == 'win32'" },
]
sdist = { url = "https://files.pythonhosted.org/packages/2e/0c/b28ed414f080ee0ad153f848586d61d1878f91689950f037f976ce15f6c8/pandas-3.0.1.tar.gz", hash = "sha256:4186a699674af418f655dbd420ed87f50d56b4cd6603784279d9eef6627823c8", size = 4641901, upload-time = "2026-02-17T22:20:16.434Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/ff/07/c7087e003ceee9b9a82539b40414ec557aa795b584a1a346e89180853d79/pandas-3.0.1-cp311-cp311-macosx_10_9_x86_64.whl", hash = "sha256:de09668c1bf3b925c07e5762291602f0d789eca1b3a781f99c1c78f6cac0e7ea", size = 10323380, upload-time = "2026-02-17T22:18:16.133Z" },
    { url = "https://files.pythonhosted.org/packages/c1/27/90683c7122febeefe84a56f2cde86a9f05f68d53885cebcc473298dfc33e/pandas-3.0.1-cp311-cp311-macosx_11_0_arm64.whl", hash = "sha256:24ba315ba3d6e5806063ac6eb717504e499ce30bd8c236d8693a5fd3f084c796", size = 9923455, upload-time = "2026-02-17T22:18:19.13Z" },
    { url = "https://files.pythonhosted.org/packages/0e/f1/ed17d927f9950643bc7631aa4c99ff0cc83a37864470bc419345b656a41f/pandas-3.0.1-cp311-cp311-manylinux_2_24_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:406ce835c55bac912f2a0dcfaf27c06d73c6b04a5dde45f1fd3169ce31337389", size = 10753464, upload-time = "2026-02-17T22:18:21.134Z" },
    { url = "https://files.pythonhosted.org/packages/2e/7c/870c7e7daec2a6c7ff2ac9e33b23317230d4e4e954b35112759ea4a924a7/pandas-3.0.1-cp311-cp311-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:830994d7e1f31dd7e790045235605ab61cff6c94defc774547e8b7fdfbff3dc7", size = 11255234, upload-time = "2026-02-17T22:18:24.175Z" },
    { url = "https://files.pythonhosted.org/packages/5c/39/3653fe59af68606282b989c23d1a543ceba6e8099cbcc5f1d506a7bae2aa/pandas-3.0.1-cp311-cp311-musllinux_1_2_aarch64.whl", hash = "sha256:a64ce8b0f2de1d2efd2ae40b0abe7f8ae6b29fbfb3812098ed5a6f8e235ad9bf", size = 11767299, upload-time = "2026-02-17T22:18:26.824Z" },
    { url = "https://files.pythonhosted.org/packages/9b/31/1daf3c0c94a849c7a8dab8a69697b36d313b229918002ba3e409265c7888/pandas-3.0.1-cp311-cp311-musllinux_1_2_x86_64.whl", hash = "sha256:9832c2c69da24b602c32e0c7b1b508a03949c18ba08d4d9f1c1033426685b447", size = 12333292, upload-time = "2026-02-17T22:18:28.996Z" },
    { url = "https://files.pythonhosted.org/packages/1f/67/af63f83cd6ca603a00fe8530c10a60f0879265b8be00b5930e8e78c5b30b/pandas-3.0.1-cp311-cp311-win_amd64.whl", hash = "sha256:84f0904a69e7365f79a0c77d3cdfccbfb05bf87847e3a51a41e1426b0edb9c79", size = 9892176, upload-time = "2026-02-17T22:18:31.79Z" },
    { url = "https://files.pythonhosted.org/packages/79/ab/9c776b14ac4b7b4140788eca18468ea39894bc7340a408f1d1e379856a6b/pandas-3.0.1-cp311-cp311-win_arm64.whl", hash = "sha256:4a68773d5a778afb31d12e34f7dd4612ab90de8c6fb1d8ffe5d4a03b955082a1", size = 9151328, upload-time = "2026-02-17T22:18:35.721Z" },
    { url = "https://files.pythonhosted.org/packages/37/51/b467209c08dae2c624873d7491ea47d2b47336e5403309d433ea79c38571/pandas-3.0.1-cp312-cp312-macosx_10_13_x86_64.whl", hash = "sha256:476f84f8c20c9f5bc47252b66b4bb25e1a9fc2fa98cead96744d8116cb85771d", size = 10344357, upload-time = "2026-02-17T22:18:38.262Z" },
    { url = "https://files.pythonhosted.org/packages/7c/f1/e2567ffc8951ab371db2e40b2fe068e36b81d8cf3260f06ae508700e5504/pandas-3.0.1-cp312-cp312-macosx_11_0_arm64.whl", hash = "sha256:0ab749dfba921edf641d4036c4c21c0b3ea70fea478165cb98a998fb2a261955", size = 9884543, upload-time = "2026-02-17T22:18:41.476Z" },
    { url = "https://files.pythonhosted.org/packages/d7/39/327802e0b6d693182403c144edacbc27eb82907b57062f23ef5a4c4a5ea7/pandas-3.0.1-cp312-cp312-manylinux_2_24_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:b8e36891080b87823aff3640c78649b91b8ff6eea3c0d70aeabd72ea43ab069b", size = 10396030, upload-time = "2026-02-17T22:18:43.822Z" },
    { url = "https://files.pythonhosted.org/packages/3d/fe/89d77e424365280b79d99b3e1e7d606f5165af2f2ecfaf0c6d24c799d607/pandas-3.0.1-cp312-cp312-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:532527a701281b9dd371e2f582ed9094f4c12dd9ffb82c0c54ee28d8ac9520c4", size = 10876435, upload-time = "2026-02-17T22:18:45.954Z" },
    { url = "https://files.pythonhosted.org/packages/b5/a6/2a75320849dd154a793f69c951db759aedb8d1dd3939eeacda9bdcfa1629/pandas-3.0.1-cp312-cp312-musllinux_1_2_aarch64.whl", hash = "sha256:356e5c055ed9b0da1580d465657bc7d00635af4fd47f30afb23025352ba764d1", size = 11405133, upload-time = "2026-02-17T22:18:48.533Z" },
    { url = "https://files.pythonhosted.org/packages/58/53/1d68fafb2e02d7881df66aa53be4cd748d25cbe311f3b3c85c93ea5d30ca/pandas-3.0.1-cp312-cp312-musllinux_1_2_x86_64.whl", hash = "sha256:9d810036895f9ad6345b8f2a338dd6998a74e8483847403582cab67745bff821", size = 11932065, upload-time = "2026-02-17T22:18:50.837Z" },
    { url = "https://files.pythonhosted.org/packages/75/08/67cc404b3a966b6df27b38370ddd96b3b023030b572283d035181854aac5/pandas-3.0.1-cp312-cp312-win_amd64.whl", hash = "sha256:536232a5fe26dd989bd633e7a0c450705fdc86a207fec7254a55e9a22950fe43", size = 9741627, upload-time = "2026-02-17T22:18:53.905Z" },
    { url = "https://files.pythonhosted.org/packages/86/4f/caf9952948fb00d23795f09b893d11f1cacb384e666854d87249530f7cbe/pandas-3.0.1-cp312-cp312-win_arm64.whl", hash = "sha256:0f463ebfd8de7f326d38037c7363c6dacb857c5881ab8961fb387804d6daf2f7", size = 9052483, upload-time = "2026-02-17T22:18:57.31Z" },
    { url = "https://files.pythonhosted.org/packages/0b/48/aad6ec4f8d007534c091e9a7172b3ec1b1ee6d99a9cbb936b5eab6c6cf58/pandas-3.0.1-cp313-cp313-macosx_10_13_x86_64.whl", hash = "sha256:5272627187b5d9c20e55d27caf5f2cd23e286aba25cadf73c8590e432e2b7262", size = 10317509, upload-time = "2026-02-17T22:18:59.498Z" },
    { url = "https://files.pythonhosted.org/packages/a8/14/5990826f779f79148ae9d3a2c39593dc04d61d5d90541e71b5749f35af95/pandas-3.0.1-cp313-cp313-macosx_11_0_arm64.whl", hash = "sha256:661e0f665932af88c7877f31da0dc743fe9c8f2524bdffe23d24fdcb67ef9d56", size = 9860561, upload-time = "2026-02-17T22:19:02.265Z" },
    { url = "https://files.pythonhosted.org/packages/fa/80/f01ff54664b6d70fed71475543d108a9b7c888e923ad210795bef04ffb7d/pandas-3.0.1-cp313-cp313-manylinux_2_24_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:75e6e292ff898679e47a2199172593d9f6107fd2dd3617c22c2946e97d5df46e", size = 10365506, upload-time = "2026-02-17T22:19:05.017Z" },
    { url = "https://files.pythonhosted.org/packages/f2/85/ab6d04733a7d6ff32bfc8382bf1b07078228f5d6ebec5266b91bfc5c4ff7/pandas-3.0.1-cp313-cp313-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:1ff8cf1d2896e34343197685f432450ec99a85ba8d90cce2030c5eee2ef98791", size = 10873196, upload-time = "2026-02-17T22:19:07.204Z" },
    { url = "https://files.pythonhosted.org/packages/48/a9/9301c83d0b47c23ac5deab91c6b39fd98d5b5db4d93b25df8d381451828f/pandas-3.0.1-cp313-cp313-musllinux_1_2_aarch64.whl", hash = "sha256:eca8b4510f6763f3d37359c2105df03a7a221a508f30e396a51d0713d462e68a", size = 11370859, upload-time = "2026-02-17T22:19:09.436Z" },
    { url = "https://files.pythonhosted.org/packages/59/fe/0c1fc5bd2d29c7db2ab372330063ad555fb83e08422829c785f5ec2176ca/pandas-3.0.1-cp313-cp313-musllinux_1_2_x86_64.whl", hash = "sha256:06aff2ad6f0b94a17822cf8b83bbb563b090ed82ff4fe7712db2ce57cd50d9b8", size = 11924584, upload-time = "2026-02-17T22:19:11.562Z" },
    { url = "https://files.pythonhosted.org/packages/d6/7d/216a1588b65a7aa5f4535570418a599d943c85afb1d95b0876fc00aa1468/pandas-3.0.1-cp313-cp313-win_amd64.whl", hash = "sha256:9fea306c783e28884c29057a1d9baa11a349bbf99538ec1da44c8476563d1b25", size = 9742769, upload-time = "2026-02-17T22:19:13.926Z" },
    { url = "https://files.pythonhosted.org/packages/c4/cb/810a22a6af9a4e97c8ab1c946b47f3489c5bca5adc483ce0ffc84c9cc768/pandas-3.0.1-cp313-cp313-win_arm64.whl", hash = "sha256:a8d37a43c52917427e897cb2e429f67a449327394396a81034a4449b99afda59", size = 9043855, upload-time = "2026-02-17T22:19:16.09Z" },
    { url = "https://files.pythonhosted.org/packages/92/fa/423c89086cca1f039cf1253c3ff5b90f157b5b3757314aa635f6bf3e30aa/pandas-3.0.1-cp313-cp313t-macosx_10_13_x86_64.whl", hash = "sha256:d54855f04f8246ed7b6fc96b05d4871591143c46c0b6f4af874764ed0d2d6f06", size = 10752673, upload-time = "2026-02-17T22:19:18.304Z" },
    { url = "https://files.pythonhosted.org/packages/22/23/b5a08ec1f40020397f0faba72f1e2c11f7596a6169c7b3e800abff0e433f/pandas-3.0.1-cp313-cp313t-macosx_11_0_arm64.whl", hash = "sha256:4e1b677accee34a09e0dc2ce5624e4a58a1870ffe56fc021e9caf7f23cd7668f", size = 10404967, upload-time = "2026-02-17T22:19:20.726Z" },
    { url = "https://files.pythonhosted.org/packages/5c/81/94841f1bb4afdc2b52a99daa895ac2c61600bb72e26525ecc9543d453ebc/pandas-3.0.1-cp313-cp313t-manylinux_2_24_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:a9cabbdcd03f1b6cd254d6dda8ae09b0252524be1592594c00b7895916cb1324", size = 10320575, upload-time = "2026-02-17T22:19:24.919Z" },
    { url = "https://files.pythonhosted.org/packages/0a/8b/2ae37d66a5342a83adadfd0cb0b4bf9c3c7925424dd5f40d15d6cfaa35ee/pandas-3.0.1-cp313-cp313t-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:5ae2ab1f166668b41e770650101e7090824fd34d17915dd9cd479f5c5e0065e9", size = 10710921, upload-time = "2026-02-17T22:19:27.181Z" },
    { url = "https://files.pythonhosted.org/packages/a2/61/772b2e2757855e232b7ccf7cb8079a5711becb3a97f291c953def15a833f/pandas-3.0.1-cp313-cp313t-musllinux_1_2_aarch64.whl", hash = "sha256:6bf0603c2e30e2cafac32807b06435f28741135cb8697eae8b28c7d492fc7d76", size = 11334191, upload-time = "2026-02-17T22:19:29.411Z" },
    { url = "https://files.pythonhosted.org/packages/1b/08/b16c6df3ef555d8495d1d265a7963b65be166785d28f06a350913a4fac78/pandas-3.0.1-cp313-cp313t-musllinux_1_2_x86_64.whl", hash = "sha256:6c426422973973cae1f4a23e51d4ae85974f44871b24844e4f7de752dd877098", size = 11782256, upload-time = "2026-02-17T22:19:32.34Z" },
    { url = "https://files.pythonhosted.org/packages/55/80/178af0594890dee17e239fca96d3d8670ba0f5ff59b7d0439850924a9c09/pandas-3.0.1-cp313-cp313t-win_amd64.whl", hash = "sha256:b03f91ae8c10a85c1613102c7bef5229b5379f343030a3ccefeca8a33414cf35", size = 10485047, upload-time = "2026-02-17T22:19:34.605Z" },
    { url = "https://files.pythonhosted.org/packages/bb/8b/4bb774a998b97e6c2fd62a9e6cfdaae133b636fd1c468f92afb4ae9a447a/pandas-3.0.1-cp314-cp314-macosx_10_15_x86_64.whl", hash = "sha256:99d0f92ed92d3083d140bf6b97774f9f13863924cf3f52a70711f4e7588f9d0a", size = 10322465, upload-time = "2026-02-17T22:19:36.803Z" },
    { url = "https://files.pythonhosted.org/packages/72/3a/5b39b51c64159f470f1ca3b1c2a87da290657ca022f7cd11442606f607d1/pandas-3.0.1-cp314-cp314-macosx_11_0_arm64.whl", hash = "sha256:3b66857e983208654294bb6477b8a63dee26b37bdd0eb34d010556e91261784f", size = 9910632, upload-time = "2026-02-17T22:19:39.001Z" },
    { url = "https://files.pythonhosted.org/packages/4e/f7/b449ffb3f68c11da12fc06fbf6d2fa3a41c41e17d0284d23a79e1c13a7e4/pandas-3.0.1-cp314-cp314-manylinux_2_24_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:56cf59638bf24dc9bdf2154c81e248b3289f9a09a6d04e63608c159022352749", size = 10440535, upload-time = "2026-02-17T22:19:41.157Z" },
    { url = "https://files.pythonhosted.org/packages/55/77/6ea82043db22cb0f2bbfe7198da3544000ddaadb12d26be36e19b03a2dc5/pandas-3.0.1-cp314-cp314-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:c1a9f55e0f46951874b863d1f3906dcb57df2d9be5c5847ba4dfb55b2c815249", size = 10893940, upload-time = "2026-02-17T22:19:43.493Z" },
    { url = "https://files.pythonhosted.org/packages/03/30/f1b502a72468c89412c1b882a08f6eed8a4ee9dc033f35f65d0663df6081/pandas-3.0.1-cp314-cp314-musllinux_1_2_aarch64.whl", hash = "sha256:1849f0bba9c8a2fb0f691d492b834cc8dadf617e29015c66e989448d58d011ee", size = 11442711, upload-time = "2026-02-17T22:19:46.074Z" },
    { url = "https://files.pythonhosted.org/packages/0d/f0/ebb6ddd8fc049e98cabac5c2924d14d1dda26a20adb70d41ea2e428d3ec4/pandas-3.0.1-cp314-cp314-musllinux_1_2_x86_64.whl", hash = "sha256:c3d288439e11b5325b02ae6e9cc83e6805a62c40c5a6220bea9beb899c073b1c", size = 11963918, upload-time = "2026-02-17T22:19:48.838Z" },
    { url = "https://files.pythonhosted.org/packages/09/f8/8ce132104074f977f907442790eaae24e27bce3b3b454e82faa3237ff098/pandas-3.0.1-cp314-cp314-win_amd64.whl", hash = "sha256:93325b0fe372d192965f4cca88d97667f49557398bbf94abdda3bf1b591dbe66", size = 9862099, upload-time = "2026-02-17T22:19:51.081Z" },
    { url = "https://files.pythonhosted.org/packages/e6/b7/6af9aac41ef2456b768ef0ae60acf8abcebb450a52043d030a65b4b7c9bd/pandas-3.0.1-cp314-cp314-win_arm64.whl", hash = "sha256:97ca08674e3287c7148f4858b01136f8bdfe7202ad25ad04fec602dd1d29d132", size = 9185333, upload-time = "2026-02-17T22:19:53.266Z" },
    { url = "https://files.pythonhosted.org/packages/66/fc/848bb6710bc6061cb0c5badd65b92ff75c81302e0e31e496d00029fe4953/pandas-3.0.1-cp314-cp314t-macosx_10_15_x86_64.whl", hash = "sha256:58eeb1b2e0fb322befcf2bbc9ba0af41e616abadb3d3414a6bc7167f6cbfce32", size = 10772664, upload-time = "2026-02-17T22:19:55.806Z" },
    { url = "https://files.pythonhosted.org/packages/69/5c/866a9bbd0f79263b4b0db6ec1a341be13a1473323f05c122388e0f15b21d/pandas-3.0.1-cp314-cp314t-macosx_11_0_arm64.whl", hash = "sha256:cd9af1276b5ca9e298bd79a26bda32fa9cc87ed095b2a9a60978d2ca058eaf87", size = 10421286, upload-time = "2026-02-17T22:19:58.091Z" },
    { url = "https://files.pythonhosted.org/packages/51/a4/2058fb84fb1cfbfb2d4a6d485e1940bb4ad5716e539d779852494479c580/pandas-3.0.1-cp314-cp314t-manylinux_2_24_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:94f87a04984d6b63788327cd9f79dda62b7f9043909d2440ceccf709249ca988", size = 10342050, upload-time = "2026-02-17T22:20:01.376Z" },
    { url = "https://files.pythonhosted.org/packages/22/1b/674e89996cc4be74db3c4eb09240c4bb549865c9c3f5d9b086ff8fcfbf00/pandas-3.0.1-cp314-cp314t-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:85fe4c4df62e1e20f9db6ebfb88c844b092c22cd5324bdcf94bfa2fc1b391221", size = 10740055, upload-time = "2026-02-17T22:20:04.328Z" },
    { url = "https://files.pythonhosted.org/packages/d0/f8/e954b750764298c22fa4614376531fe63c521ef517e7059a51f062b87dca/pandas-3.0.1-cp314-cp314t-musllinux_1_2_aarch64.whl", hash = "sha256:331ca75a2f8672c365ae25c0b29e46f5ac0c6551fdace8eec4cd65e4fac271ff", size = 11357632, upload-time = "2026-02-17T22:20:06.647Z" },
    { url = "https://files.pythonhosted.org/packages/6d/02/c6e04b694ffd68568297abd03588b6d30295265176a5c01b7459d3bc35a3/pandas-3.0.1-cp314-cp314t-musllinux_1_2_x86_64.whl", hash = "sha256:15860b1fdb1973fffade772fdb931ccf9b2f400a3f5665aef94a00445d7d8dd5", size = 11810974, upload-time = "2026-02-17T22:20:08.946Z" },
    { url = "https://files.pythonhosted.org/packages/89/41/d7dfb63d2407f12055215070c42fc6ac41b66e90a2946cdc5e759058398b/pandas-3.0.1-cp314-cp314t-win_amd64.whl", hash = "sha256:44f1364411d5670efa692b146c748f4ed013df91ee91e9bec5677fb1fd58b937", size = 10884622, upload-time = "2026-02-17T22:20:11.711Z" },
    { url = "https://files.pythonhosted.org/packages/68/b0/34937815889fa982613775e4b97fddd13250f11012d769949c5465af2150/pandas-3.0.1-cp314-cp314t-win_arm64.whl", hash = "sha256:108dd1790337a494aa80e38def654ca3f0968cf4f362c85f44c15e471667102d", size = 9452085, upload-time = "2026-02-17T22:20:14.331Z" },
]

[[package]]
name = "plotly"
version = "6.5.2"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "narwhals" },
    { name = "packaging" },
]
sdist = { url = "https://files.pythonhosted.org/packages/e3/4f/8a10a9b9f5192cb6fdef62f1d77fa7d834190b2c50c0cd256bd62879212b/plotly-6.5.2.tar.gz", hash = "sha256:7478555be0198562d1435dee4c308268187553cc15516a2f4dd034453699e393", size = 7015695, upload-time = "2026-01-14T21:26:51.222Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/8a/67/f95b5460f127840310d2187f916cf0023b5875c0717fdf893f71e1325e87/plotly-6.5.2-py3-none-any.whl", hash = "sha256:91757653bd9c550eeea2fa2404dba6b85d1e366d54804c340b2c874e5a7eb4a4", size = 9895973, upload-time = "2026-01-14T21:26:47.135Z" },
]

[[package]]
name = "python-dateutil"
version = "2.9.0.post0"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "six" },
]
sdist = { url = "https://files.pythonhosted.org/packages/66/c0/0c8b6ad9f17a802ee498c46e004a0eb49bc148f2fd230864601a86dcf6db/python-dateutil-2.9.0.post0.tar.gz", hash = "sha256:37dd54208da7e1cd875388217d5e00ebd4179249f90fb72437e91a35459a0ad3", size = 342432, upload-time = "2024-03-01T18:36:20.211Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/ec/57/56b9bcc3c9c6a792fcbaf139543cee77261f3651ca9da0c93f5c1221264b/python_dateutil-2.9.0.post0-py2.py3-none-any.whl", hash = "sha256:a8b2bc7bffae282281c8140a97d3aa9c14da0b136dfe83f850eea9a5f7470427", size = 229892, upload-time = "2024-03-01T18:36:18.57Z" },
]

[[package]]
name = "six"
version = "1.17.0"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/94/e7/b2c673351809dca68a0e064b6af791aa332cf192da575fd474ed7d6f16a2/six-1.17.0.tar.gz", hash = "sha256:ff70335d468e7eb6ec65b95b99d3a2836546063f63acc5171de367e834932a81", size = 34031, upload-time = "2024-12-04T17:35:28.174Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/b7/ce/149a00dd41f10bc29e5921b496af8b574d8413afcd5e30dfa0ed46c2cc5e/six-1.17.0-py2.py3-none-any.whl", hash = "sha256:4721f391ed90541fddacab5acf947aa0d3dc7d27b2e1e8eda2be8970586c3274", size = 11050, upload-time = "2024-12-04T17:35:26.475Z" },
]

[[package]]
name = "tzdata"
version = "2025.3"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/5e/a7/c202b344c5ca7daf398f3b8a477eeb205cf3b6f32e7ec3a6bac0629ca975/tzdata-2025.3.tar.gz", hash = "sha256:de39c2ca5dc7b0344f2eba86f49d614019d29f060fc4ebc8a417896a620b56a7", size = 196772, upload-time = "2025-12-13T17:45:35.667Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/c7/b0/003792df09decd6849a5e39c28b513c06e84436a54440380862b5aeff25d/tzdata-2025.3-py2.py3-none-any.whl", hash = "sha256:06a47e5700f3081aab02b2e513160914ff0694bce9947d6b76ebd6bf57cfc5d1", size = 348521, upload-time = "2025-12-13T17:45:33.889Z" },
]

```

`./page_to_export/index.html`:
```
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
  <title>ECI Dashboard POC</title>
  <script src="https://cdn.plot.ly/plotly-2.32.0.min.js"></script>
</head>
<link rel="stylesheet" href="./styles/styles.css">

<body>
  <div class="dashboard-container" id="top">

    <div id="header-slot"></div>
    <div id="footer-slot"></div>
    <div id="kpi-slot"></div>

    <div class="table-curently-open-slot">
      <div id="currently-open"></div>
    </div>

    <div class="row-top-10-graph">
      <div id="chart1-slot"></div>
    </div>

    <div class="move-top-page">
      <button id="back-to-top" class="back-to-top-btn" aria-label="Scroll to top" title="Back to top">
        &#8963;
      </button>
    </div>

    <div class="bottom-row">
      <div id="chart-initiatives-status-slot"></div>
      <div id="chart-signatures-count-slot"></div>
    </div>

  </div>

  <script src="./script/back_to_top.js"></script>
  <script src="./script/partials.js"></script>
</body>
</html>

```

`./page_to_export/partials/chart_outcomes.html`:
```
<div class="card bottom-col">
<div>                            <div id="a6e1c891-37b0-44bf-a4e5-ce2bc1380ef8" class="plotly-graph-div" style="height:400px; width:500px;"></div>            <script type="text/javascript">                window.PLOTLYENV=window.PLOTLYENV || {};                                if (document.getElementById("a6e1c891-37b0-44bf-a4e5-ce2bc1380ef8")) {                    Plotly.newPlot(                        "a6e1c891-37b0-44bf-a4e5-ce2bc1380ef8",                        [{"customdata":[[2,6.9,"\u2022 Fur Free Europe\u003cbr\u003e\u2022 Right to Water"],[1,3.4,"\u2022 End the Cage Age"],[12,41.4,"\u2022 AI Regulation for Workers\u003cbr\u003e\u2022 Tax the Rich\u003cbr\u003e\u2022 Clean Air for Europe\u003cbr\u003e\u2022 Ban PFAS Forever Chemicals\u003cbr\u003e\u2022 European Rail Night Revival\u003cbr\u003e\u003ci\u003e\u2026 (and 7 more)\u003c\u002fi\u003e"],[1,3.4,"\u2022 Save Bees and Farmers"],[1,3.4,"\u2022 One of Us"],[1,3.4,"\u2022 Stop Finning - Stop the Trade"],[11,37.9,"\u2022 Protect EU Borders\u003cbr\u003e\u2022 Ban Microplastics\u003cbr\u003e\u2022 Digital Rights Charter\u003cbr\u003e\u2022 Universal Basic Income EU\u003cbr\u003e\u2022 Ban Factory Farming\u003cbr\u003e\u003ci\u003e\u2026 (and 6 more)\u003c\u002fi\u003e"]],"hole":0.45,"hovertemplate":"\u003cb\u003e%{label}\u003c\u002fb\u003e\u003cbr\u003eCount: %{customdata[0][0]}\u003cbr\u003ePercentage: %{customdata[0][1]}%\u003cbr\u003e\u003cbr\u003e\u003cb\u003eECIs:\u003c\u002fb\u003e\u003cbr\u003e%{customdata[0][2]}\u003cextra\u003e\u003c\u002fextra\u003e","labels":["Law Passed","Commission Engaged","Collection Ongoing","Waiting for Response","Withdrawn","Rejected Legislation","Collection Unsuccessful"],"marker":{"colors":["#3CA371","#9CCC65","#F5A623","#9E9E9E","#4B4B4B","#F44336","#8B1111"]},"sort":false,"textfont":{"color":"white","family":"Arial Black","size":11},"textinfo":"percent+label","textposition":"inside","values":{"dtype":"i1","bdata":"AgEMAQEBCw=="},"type":"pie"}],                        {"template":{"data":{"histogram2dcontour":[{"type":"histogram2dcontour","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"choropleth":[{"type":"choropleth","colorbar":{"outlinewidth":0,"ticks":""}}],"histogram2d":[{"type":"histogram2d","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"heatmap":[{"type":"heatmap","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"contourcarpet":[{"type":"contourcarpet","colorbar":{"outlinewidth":0,"ticks":""}}],"contour":[{"type":"contour","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"surface":[{"type":"surface","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"mesh3d":[{"type":"mesh3d","colorbar":{"outlinewidth":0,"ticks":""}}],"scatter":[{"fillpattern":{"fillmode":"overlay","size":10,"solidity":0.2},"type":"scatter"}],"parcoords":[{"type":"parcoords","line":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatterpolargl":[{"type":"scatterpolargl","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"bar":[{"error_x":{"color":"#2a3f5f"},"error_y":{"color":"#2a3f5f"},"marker":{"line":{"color":"#E5ECF6","width":0.5},"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"bar"}],"scattergeo":[{"type":"scattergeo","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatterpolar":[{"type":"scatterpolar","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"histogram":[{"marker":{"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"histogram"}],"scattergl":[{"type":"scattergl","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatter3d":[{"type":"scatter3d","line":{"colorbar":{"outlinewidth":0,"ticks":""}},"marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scattermap":[{"type":"scattermap","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scattermapbox":[{"type":"scattermapbox","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatterternary":[{"type":"scatterternary","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scattercarpet":[{"type":"scattercarpet","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"carpet":[{"aaxis":{"endlinecolor":"#2a3f5f","gridcolor":"white","linecolor":"white","minorgridcolor":"white","startlinecolor":"#2a3f5f"},"baxis":{"endlinecolor":"#2a3f5f","gridcolor":"white","linecolor":"white","minorgridcolor":"white","startlinecolor":"#2a3f5f"},"type":"carpet"}],"table":[{"cells":{"fill":{"color":"#EBF0F8"},"line":{"color":"white"}},"header":{"fill":{"color":"#C8D4E3"},"line":{"color":"white"}},"type":"table"}],"barpolar":[{"marker":{"line":{"color":"#E5ECF6","width":0.5},"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"barpolar"}],"pie":[{"automargin":true,"type":"pie"}]},"layout":{"autotypenumbers":"strict","colorway":["#636efa","#EF553B","#00cc96","#ab63fa","#FFA15A","#19d3f3","#FF6692","#B6E880","#FF97FF","#FECB52"],"font":{"color":"#2a3f5f"},"hovermode":"closest","hoverlabel":{"align":"left"},"paper_bgcolor":"white","plot_bgcolor":"#E5ECF6","polar":{"bgcolor":"#E5ECF6","angularaxis":{"gridcolor":"white","linecolor":"white","ticks":""},"radialaxis":{"gridcolor":"white","linecolor":"white","ticks":""}},"ternary":{"bgcolor":"#E5ECF6","aaxis":{"gridcolor":"white","linecolor":"white","ticks":""},"baxis":{"gridcolor":"white","linecolor":"white","ticks":""},"caxis":{"gridcolor":"white","linecolor":"white","ticks":""}},"coloraxis":{"colorbar":{"outlinewidth":0,"ticks":""}},"colorscale":{"sequential":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"sequentialminus":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"diverging":[[0,"#8e0152"],[0.1,"#c51b7d"],[0.2,"#de77ae"],[0.3,"#f1b6da"],[0.4,"#fde0ef"],[0.5,"#f7f7f7"],[0.6,"#e6f5d0"],[0.7,"#b8e186"],[0.8,"#7fbc41"],[0.9,"#4d9221"],[1,"#276419"]]},"xaxis":{"gridcolor":"white","linecolor":"white","ticks":"","title":{"standoff":15},"zerolinecolor":"white","automargin":true,"zerolinewidth":2},"yaxis":{"gridcolor":"white","linecolor":"white","ticks":"","title":{"standoff":15},"zerolinecolor":"white","automargin":true,"zerolinewidth":2},"scene":{"xaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white","gridwidth":2},"yaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white","gridwidth":2},"zaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white","gridwidth":2}},"shapedefaults":{"line":{"color":"#2a3f5f"}},"annotationdefaults":{"arrowcolor":"#2a3f5f","arrowhead":0,"arrowwidth":1},"geo":{"bgcolor":"white","landcolor":"#E5ECF6","subunitcolor":"white","showland":true,"showlakes":true,"lakecolor":"white"},"title":{"x":0.05},"mapbox":{"style":"light"}}},"margin":{"l":20,"r":20,"t":50,"b":20},"legend":{"font":{"size":12},"orientation":"v","yanchor":"middle","y":0.5,"xanchor":"left","x":1.02},"title":{"text":"Initiatives by Current Status"},"height":400,"width":500,"showlegend":true},                        {"responsive": true}                    )                };            </script>        </div>
</div>
```

`./page_to_export/partials/chart_policy_area.html`:
```
<div class="card">
<div>                            <div id="2f71742d-bbee-4a68-aa61-158d0ec7f1bf" class="plotly-graph-div" style="height:400px; width:100%;"></div>            <script type="text/javascript">                window.PLOTLYENV=window.PLOTLYENV || {};                                if (document.getElementById("2f71742d-bbee-4a68-aa61-158d0ec7f1bf")) {                    Plotly.newPlot(                        "2f71742d-bbee-4a68-aa61-158d0ec7f1bf",                        [{"hovertemplate":"Policy Area=%{x}\u003cbr\u003eTotal Signatures=%{y}\u003cextra\u003e\u003c\u002fextra\u003e","legendgroup":"Animal Welfare","marker":{"color":"#636EFA","pattern":{"shape":""}},"name":"Animal Welfare","orientation":"v","showlegend":true,"textposition":"auto","texttemplate":"%{y:.2s}","x":["Animal Welfare"],"xaxis":"x","y":{"dtype":"i4","bdata":"6D0sAA=="},"yaxis":"y","type":"bar"},{"hovertemplate":"Policy Area=%{x}\u003cbr\u003eTotal Signatures=%{y}\u003cextra\u003e\u003c\u002fextra\u003e","legendgroup":"Environment","marker":{"color":"#EF553B","pattern":{"shape":""}},"name":"Environment","orientation":"v","showlegend":true,"textposition":"auto","texttemplate":"%{y:.2s}","x":["Environment"],"xaxis":"x","y":{"dtype":"i4","bdata":"bC0hAA=="},"yaxis":"y","type":"bar"},{"hovertemplate":"Policy Area=%{x}\u003cbr\u003eTotal Signatures=%{y}\u003cextra\u003e\u003c\u002fextra\u003e","legendgroup":"Human Rights","marker":{"color":"#00CC96","pattern":{"shape":""}},"name":"Human Rights","orientation":"v","showlegend":true,"textposition":"auto","texttemplate":"%{y:.2s}","x":["Human Rights"],"xaxis":"x","y":{"dtype":"i4","bdata":"l1IZAA=="},"yaxis":"y","type":"bar"},{"hovertemplate":"Policy Area=%{x}\u003cbr\u003eTotal Signatures=%{y}\u003cextra\u003e\u003c\u002fextra\u003e","legendgroup":"Taxation","marker":{"color":"#AB63FA","pattern":{"shape":""}},"name":"Taxation","orientation":"v","showlegend":true,"textposition":"auto","texttemplate":"%{y:.2s}","x":["Taxation"],"xaxis":"x","y":{"dtype":"i4","bdata":"kJQNAA=="},"yaxis":"y","type":"bar"},{"hovertemplate":"Policy Area=%{x}\u003cbr\u003eTotal Signatures=%{y}\u003cextra\u003e\u003c\u002fextra\u003e","legendgroup":"Employment","marker":{"color":"#FFA15A","pattern":{"shape":""}},"name":"Employment","orientation":"v","showlegend":true,"textposition":"auto","texttemplate":"%{y:.2s}","x":["Employment"],"xaxis":"x","y":{"dtype":"i4","bdata":"0N0GAA=="},"yaxis":"y","type":"bar"},{"hovertemplate":"Policy Area=%{x}\u003cbr\u003eTotal Signatures=%{y}\u003cextra\u003e\u003c\u002fextra\u003e","legendgroup":"Security","marker":{"color":"#19D3F3","pattern":{"shape":""}},"name":"Security","orientation":"v","showlegend":true,"textposition":"auto","texttemplate":"%{y:.2s}","x":["Security"],"xaxis":"x","y":{"dtype":"i4","bdata":"tNYBAA=="},"yaxis":"y","type":"bar"}],                        {"template":{"data":{"histogram2dcontour":[{"type":"histogram2dcontour","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"choropleth":[{"type":"choropleth","colorbar":{"outlinewidth":0,"ticks":""}}],"histogram2d":[{"type":"histogram2d","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"heatmap":[{"type":"heatmap","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"contourcarpet":[{"type":"contourcarpet","colorbar":{"outlinewidth":0,"ticks":""}}],"contour":[{"type":"contour","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"surface":[{"type":"surface","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"mesh3d":[{"type":"mesh3d","colorbar":{"outlinewidth":0,"ticks":""}}],"scatter":[{"fillpattern":{"fillmode":"overlay","size":10,"solidity":0.2},"type":"scatter"}],"parcoords":[{"type":"parcoords","line":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatterpolargl":[{"type":"scatterpolargl","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"bar":[{"error_x":{"color":"#2a3f5f"},"error_y":{"color":"#2a3f5f"},"marker":{"line":{"color":"#E5ECF6","width":0.5},"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"bar"}],"scattergeo":[{"type":"scattergeo","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatterpolar":[{"type":"scatterpolar","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"histogram":[{"marker":{"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"histogram"}],"scattergl":[{"type":"scattergl","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatter3d":[{"type":"scatter3d","line":{"colorbar":{"outlinewidth":0,"ticks":""}},"marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scattermap":[{"type":"scattermap","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scattermapbox":[{"type":"scattermapbox","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatterternary":[{"type":"scatterternary","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scattercarpet":[{"type":"scattercarpet","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"carpet":[{"aaxis":{"endlinecolor":"#2a3f5f","gridcolor":"white","linecolor":"white","minorgridcolor":"white","startlinecolor":"#2a3f5f"},"baxis":{"endlinecolor":"#2a3f5f","gridcolor":"white","linecolor":"white","minorgridcolor":"white","startlinecolor":"#2a3f5f"},"type":"carpet"}],"table":[{"cells":{"fill":{"color":"#EBF0F8"},"line":{"color":"white"}},"header":{"fill":{"color":"#C8D4E3"},"line":{"color":"white"}},"type":"table"}],"barpolar":[{"marker":{"line":{"color":"#E5ECF6","width":0.5},"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"barpolar"}],"pie":[{"automargin":true,"type":"pie"}]},"layout":{"autotypenumbers":"strict","colorway":["#636efa","#EF553B","#00cc96","#ab63fa","#FFA15A","#19d3f3","#FF6692","#B6E880","#FF97FF","#FECB52"],"font":{"color":"#2a3f5f"},"hovermode":"closest","hoverlabel":{"align":"left"},"paper_bgcolor":"white","plot_bgcolor":"#E5ECF6","polar":{"bgcolor":"#E5ECF6","angularaxis":{"gridcolor":"white","linecolor":"white","ticks":""},"radialaxis":{"gridcolor":"white","linecolor":"white","ticks":""}},"ternary":{"bgcolor":"#E5ECF6","aaxis":{"gridcolor":"white","linecolor":"white","ticks":""},"baxis":{"gridcolor":"white","linecolor":"white","ticks":""},"caxis":{"gridcolor":"white","linecolor":"white","ticks":""}},"coloraxis":{"colorbar":{"outlinewidth":0,"ticks":""}},"colorscale":{"sequential":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"sequentialminus":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"diverging":[[0,"#8e0152"],[0.1,"#c51b7d"],[0.2,"#de77ae"],[0.3,"#f1b6da"],[0.4,"#fde0ef"],[0.5,"#f7f7f7"],[0.6,"#e6f5d0"],[0.7,"#b8e186"],[0.8,"#7fbc41"],[0.9,"#4d9221"],[1,"#276419"]]},"xaxis":{"gridcolor":"white","linecolor":"white","ticks":"","title":{"standoff":15},"zerolinecolor":"white","automargin":true,"zerolinewidth":2},"yaxis":{"gridcolor":"white","linecolor":"white","ticks":"","title":{"standoff":15},"zerolinecolor":"white","automargin":true,"zerolinewidth":2},"scene":{"xaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white","gridwidth":2},"yaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white","gridwidth":2},"zaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white","gridwidth":2}},"shapedefaults":{"line":{"color":"#2a3f5f"}},"annotationdefaults":{"arrowcolor":"#2a3f5f","arrowhead":0,"arrowwidth":1},"geo":{"bgcolor":"white","landcolor":"#E5ECF6","subunitcolor":"white","showland":true,"showlakes":true,"lakecolor":"white"},"title":{"x":0.05},"mapbox":{"style":"light"}}},"xaxis":{"anchor":"y","domain":[0.0,1.0],"title":{"text":"Policy Area"},"categoryorder":"array","categoryarray":["Animal Welfare","Environment","Human Rights","Taxation","Employment","Security"]},"yaxis":{"anchor":"x","domain":[0.0,1.0],"title":{"text":"Total Signatures"}},"legend":{"title":{"text":"Policy Area"},"tracegroupgap":0},"title":{"text":"Total Signatures by Policy Area"},"barmode":"relative","margin":{"l":20,"r":20,"t":50,"b":20},"height":400,"showlegend":true},                        {"responsive": true}                    )                };            </script>        </div>
</div>
```

`./page_to_export/partials/chart_signatures_cohorts.html`:
```
<div class="card bottom-col">
<div>                            <div id="232f1f34-d02c-4ff7-b8c4-8cbbee58fa5a" class="plotly-graph-div" style="height:400px; width:620px;"></div>            <script type="text/javascript">                window.PLOTLYENV=window.PLOTLYENV || {};                                if (document.getElementById("232f1f34-d02c-4ff7-b8c4-8cbbee58fa5a")) {                    Plotly.newPlot(                        "232f1f34-d02c-4ff7-b8c4-8cbbee58fa5a",                        [{"customdata":["\u2022 Mandatory Climate Education\u003cbr\u003e\u2022 End Dark Patterns Online","\u2022 Digital Rights Charter\u003cbr\u003e\u2022 Ban Factory Farming\u003cbr\u003e\u2022 Free Public Transport\u003cbr\u003e\u2022 Protect Old Growth Forests\u003cbr\u003e\u2022 Clean Air for Europe\u003cbr\u003e\u2022 Protect Whistleblowers in EU Funds\u003cbr\u003e\u2022 European Accessible Cities","\u2022 Ban Microplastics\u003cbr\u003e\u2022 Universal Basic Income EU\u003cbr\u003e\u2022 EU Housing Guarantee\u003cbr\u003e\u2022 Ban Glyphosate Renewal\u003cbr\u003e\u2022 Europe for Mental Health","\u2022 Protect EU Borders\u003cbr\u003e\u2022 European Rail Night Revival\u003cbr\u003e\u2022 Stop Greenwashing Claims","\u2022 Ban PFAS Forever Chemicals","No ECIs","\u2022 Fair Digital Platform Work","No ECIs","\u2022 EU Right to Repair Plus","No ECIs","\u2022 Ban Facial Recognition in Public","\u2022 AI Regulation for Workers","No ECIs","No ECIs","No ECIs","No ECIs","No ECIs","No ECIs","No ECIs","No ECIs","No ECIs","No ECIs","No ECIs","No ECIs","No ECIs","No ECIs"],"hovertemplate":"\u003cb\u003eSignatures Range:\u003c\u002fb\u003e %{x:,.0f}\u003cbr\u003e\u003cb\u003eCount:\u003c\u002fb\u003e %{y}\u003cbr\u003e\u003cbr\u003e\u003cb\u003eECIs:\u003c\u002fb\u003e\u003cbr\u003e%{customdata}\u003cextra\u003e\u003c\u002fextra\u003e","marker":{"color":["rgb(196,69,66)","rgb(198,76,66)","rgb(200,82,67)","rgb(202,89,67)","rgb(205,96,68)","rgb(207,103,68)","rgb(209,109,69)","rgb(212,116,69)","rgb(214,123,70)","rgb(216,130,70)","rgb(218,136,71)","rgb(221,143,71)","rgb(223,150,72)","rgb(225,157,72)","rgb(228,163,73)","rgb(230,170,73)","rgb(232,177,74)","rgb(234,184,74)","rgb(237,190,75)","rgb(239,197,75)","rgb(241,204,76)","rgb(243,211,76)","rgb(246,217,77)","rgb(248,224,77)","rgb(250,231,78)","rgb(253,238,78)"],"line":{"color":"white","width":0.5}},"name":"Below 1M","width":{"dtype":"f8","bdata":"H4XrUfiH4kAfhetR+IfiQB6F61H4h+JAIIXrUfiH4kAghetR+IfiQByF61H4h+JAIIXrUfiH4kAghetR+IfiQCCF61H4h+JAIIXrUfiH4kAghetR+IfiQBiF61H4h+JAIIXrUfiH4kAghetR+IfiQCCF61H4h+JAIIXrUfiH4kAghetR+IfiQCCF61H4h+JAIIXrUfiH4kAghetR+IfiQCCF61H4h+JAIIXrUfiH4kAghetR+IfiQBCF61H4h+JAIIXrUfiH4kAghetR+IfiQA=="},"x":{"dtype":"f8","bdata":"H4XrUfiH0kCuR+F69MvrQGZmZmb2KfdAexSuR\u002fk2AEHD9Shc99gEQQrXo3D1eglBUrgehfMcDkHNzMzMeF8RQXE9Ctd3sBNBFa5H4XYBFkG5HoXrdVIYQVyPwvV0oxpBAAAAAHT0HEGkcD0Kc0UfQaRwPQo5yyBB9ihcj7jzIUFI4XoUOBwjQZqZmZm3RCRB7FG4HjdtJUE+CtejtpUmQZDC9Sg2vidB4noUrrXmKEE0MzMzNQ8qQYbrUbi0NytB16NwPTRgLEEpXI\u002fCs4gtQQ=="},"y":{"dtype":"i1","bdata":"AgcFAwEAAQABAAEBAAAAAAAAAAAAAAAAAAA="},"type":"bar"},{"customdata":["\u2022 Save Bees and Farmers","No ECIs","\u2022 Stop Finning - Stop the Trade","No ECIs","No ECIs","No ECIs","No ECIs","No ECIs","No ECIs","\u2022 End the Cage Age","No ECIs","No ECIs","\u2022 Fur Free Europe","No ECIs","No ECIs","No ECIs","\u2022 Right to Water","No ECIs","No ECIs","No ECIs","No ECIs","No ECIs","\u2022 One of Us"],"hovertemplate":"\u003cb\u003eSignatures Range:\u003c\u002fb\u003e %{x:,.0f}\u003cbr\u003e\u003cb\u003eCount:\u003c\u002fb\u003e %{y}\u003cbr\u003e\u003cbr\u003e\u003cb\u003eECIs:\u003c\u002fb\u003e\u003cbr\u003e%{customdata}\u003cextra\u003e\u003c\u002fextra\u003e","marker":{"color":["rgb(178,213,126)","rgb(173,211,125)","rgb(169,209,125)","rgb(164,207,124)","rgb(159,205,124)","rgb(155,203,123)","rgb(150,201,123)","rgb(145,199,122)","rgb(140,197,122)","rgb(136,195,121)","rgb(131,193,121)","rgb(126,191,120)","rgb(122,189,120)","rgb(117,187,119)","rgb(112,185,118)","rgb(107,183,118)","rgb(103,181,117)","rgb(98,179,117)","rgb(93,177,116)","rgb(89,175,116)","rgb(84,173,115)","rgb(79,171,115)","rgb(75,169,114)"],"line":{"color":"white","width":0.5}},"name":"Above 1M","width":{"dtype":"f8","bdata":"IIXrUfiH4kAghetR+IfiQCCF61H4h+JAIIXrUfiH4kAghetR+IfiQCCF61H4h+JAIIXrUfiH4kAghetR+IfiQCCF61H4h+JAIIXrUfiH4kAghetR+IfiQCCF61H4h+JAIIXrUfiH4kAghetR+IfiQCCF61H4h+JAIIXrUfiH4kAghetR+IfiQCCF61H4h+JAIIXrUfiH4kAghetR+IfiQACF61H4h+JAIIXrUfiH4kAghetR+IfiQA=="},"x":{"dtype":"f8","bdata":"zczMzLLZL0GQwvUoGYEwQbgehetYFTFB4noUrpipMUEK16Nw2D0yQTQzMzMY0jJBXI\u002fC9VdmM0GG61G4l\u002fozQa5H4XrXjjRB2KNwPRcjNUEAAAAAV7c1QSpcj8KWSzZBUrgehdbfNkF8FK5HFnQ3QaRwPQpWCDhBzszMzJWcOEH2KFyP1TA5QSCF61EVxTlBSOF6FFVZOkFyPQrXlO06QZqZmZnUgTtBwvUoXBQWPEHsUbgeVKo8QQ=="},"y":{"dtype":"i1","bdata":"AQABAAAAAAAAAQAAAQAAAAEAAAAAAAE="},"type":"bar"}],                        {"template":{"data":{"histogram2dcontour":[{"type":"histogram2dcontour","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"choropleth":[{"type":"choropleth","colorbar":{"outlinewidth":0,"ticks":""}}],"histogram2d":[{"type":"histogram2d","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"heatmap":[{"type":"heatmap","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"contourcarpet":[{"type":"contourcarpet","colorbar":{"outlinewidth":0,"ticks":""}}],"contour":[{"type":"contour","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"surface":[{"type":"surface","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"mesh3d":[{"type":"mesh3d","colorbar":{"outlinewidth":0,"ticks":""}}],"scatter":[{"fillpattern":{"fillmode":"overlay","size":10,"solidity":0.2},"type":"scatter"}],"parcoords":[{"type":"parcoords","line":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatterpolargl":[{"type":"scatterpolargl","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"bar":[{"error_x":{"color":"#2a3f5f"},"error_y":{"color":"#2a3f5f"},"marker":{"line":{"color":"#E5ECF6","width":0.5},"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"bar"}],"scattergeo":[{"type":"scattergeo","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatterpolar":[{"type":"scatterpolar","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"histogram":[{"marker":{"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"histogram"}],"scattergl":[{"type":"scattergl","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatter3d":[{"type":"scatter3d","line":{"colorbar":{"outlinewidth":0,"ticks":""}},"marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scattermap":[{"type":"scattermap","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scattermapbox":[{"type":"scattermapbox","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatterternary":[{"type":"scatterternary","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scattercarpet":[{"type":"scattercarpet","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"carpet":[{"aaxis":{"endlinecolor":"#2a3f5f","gridcolor":"white","linecolor":"white","minorgridcolor":"white","startlinecolor":"#2a3f5f"},"baxis":{"endlinecolor":"#2a3f5f","gridcolor":"white","linecolor":"white","minorgridcolor":"white","startlinecolor":"#2a3f5f"},"type":"carpet"}],"table":[{"cells":{"fill":{"color":"#EBF0F8"},"line":{"color":"white"}},"header":{"fill":{"color":"#C8D4E3"},"line":{"color":"white"}},"type":"table"}],"barpolar":[{"marker":{"line":{"color":"#E5ECF6","width":0.5},"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"barpolar"}],"pie":[{"automargin":true,"type":"pie"}]},"layout":{"autotypenumbers":"strict","colorway":["#636efa","#EF553B","#00cc96","#ab63fa","#FFA15A","#19d3f3","#FF6692","#B6E880","#FF97FF","#FECB52"],"font":{"color":"#2a3f5f"},"hovermode":"closest","hoverlabel":{"align":"left"},"paper_bgcolor":"white","plot_bgcolor":"#E5ECF6","polar":{"bgcolor":"#E5ECF6","angularaxis":{"gridcolor":"white","linecolor":"white","ticks":""},"radialaxis":{"gridcolor":"white","linecolor":"white","ticks":""}},"ternary":{"bgcolor":"#E5ECF6","aaxis":{"gridcolor":"white","linecolor":"white","ticks":""},"baxis":{"gridcolor":"white","linecolor":"white","ticks":""},"caxis":{"gridcolor":"white","linecolor":"white","ticks":""}},"coloraxis":{"colorbar":{"outlinewidth":0,"ticks":""}},"colorscale":{"sequential":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"sequentialminus":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"diverging":[[0,"#8e0152"],[0.1,"#c51b7d"],[0.2,"#de77ae"],[0.3,"#f1b6da"],[0.4,"#fde0ef"],[0.5,"#f7f7f7"],[0.6,"#e6f5d0"],[0.7,"#b8e186"],[0.8,"#7fbc41"],[0.9,"#4d9221"],[1,"#276419"]]},"xaxis":{"gridcolor":"white","linecolor":"white","ticks":"","title":{"standoff":15},"zerolinecolor":"white","automargin":true,"zerolinewidth":2},"yaxis":{"gridcolor":"white","linecolor":"white","ticks":"","title":{"standoff":15},"zerolinecolor":"white","automargin":true,"zerolinewidth":2},"scene":{"xaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white","gridwidth":2},"yaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white","gridwidth":2},"zaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white","gridwidth":2}},"shapedefaults":{"line":{"color":"#2a3f5f"}},"annotationdefaults":{"arrowcolor":"#2a3f5f","arrowhead":0,"arrowwidth":1},"geo":{"bgcolor":"white","landcolor":"#E5ECF6","subunitcolor":"white","showland":true,"showlakes":true,"lakecolor":"white"},"title":{"x":0.05},"mapbox":{"style":"light"}}},"shapes":[{"line":{"color":"#3AB23F","dash":"dash","width":3},"type":"line","x0":1000000,"x1":1000000,"xref":"x","y0":0,"y1":1,"yref":"y domain"}],"annotations":[{"font":{"color":"#3AB23F","size":13},"showarrow":false,"text":"1M Threshold","x":1000000,"xanchor":"left","xref":"x","y":1,"yanchor":"top","yref":"y domain"}],"margin":{"l":20,"r":20,"t":50,"b":20},"legend":{"font":{"size":13}},"title":{"text":"Distribution of Signature Counts"},"xaxis":{"title":{"text":"Signatures Collected"}},"yaxis":{"title":{"text":"Number of Initiatives"}},"height":400,"width":620,"showlegend":true,"bargap":0.05},                        {"responsive": true}                    )                };            </script>        </div>
</div>
```

`./page_to_export/partials/chart_signatures_year.html`:
```
<div class="card bottom-col">
<div>                            <div id="965d0634-5a3f-487c-97f9-7e432782ffc4" class="plotly-graph-div" style="height:400px; width:100%;"></div>            <script type="text/javascript">                window.PLOTLYENV=window.PLOTLYENV || {};                                if (document.getElementById("965d0634-5a3f-487c-97f9-7e432782ffc4")) {                    Plotly.newPlot(                        "965d0634-5a3f-487c-97f9-7e432782ffc4",                        [{"hovertemplate":"\u003cb\u003e%{hovertext}\u003c\u002fb\u003e\u003cbr\u003e\u003cbr\u003eRegistration Year=%{x}\u003cbr\u003eTotal Signatures=%{marker.size}\u003cextra\u003e\u003c\u002fextra\u003e","hovertext":["Fur Free Europe","End the Cage Age","Save Bees and Farmers","Stop Finning - Stop the Trade","AI Regulation for Workers","Tax the Rich","Right to Water","Protect EU Borders","One of Us","Ban Microplastics","Digital Rights Charter","Universal Basic Income EU","Ban Factory Farming","Free Public Transport","EU Housing Guarantee","Ban Glyphosate Renewal","Mandatory Climate Education","End Dark Patterns Online","Protect Old Growth Forests"],"legendgroup":"","marker":{"color":"#636EFA","size":{"dtype":"i4","bdata":"b+wWAHlRFQBwFhAA\u002fBYRANDdBgCQlA0Al1IZALTWAQB09BwAiFUBAMLTAACttQEAJA0BAASrAABOdAEA1jIBAOB5AACudAAA9u8AAA=="},"sizemode":"area","sizeref":527.1077777777778,"symbol":"circle"},"mode":"markers","name":"","orientation":"v","showlegend":false,"x":{"dtype":"i2","bdata":"6AfnB+kH5gfqB+oH6AfqB+UH5gfnB+UH5wfmB+gH5wfoB+kH5gc="},"xaxis":"x","y":{"dtype":"i4","bdata":"b+wWAHlRFQBwFhAA\u002fBYRANDdBgCQlA0Al1IZALTWAQB09BwAiFUBAMLTAACttQEAJA0BAASrAABOdAEA1jIBAOB5AACudAAA9u8AAA=="},"yaxis":"y","type":"scatter"}],                        {"template":{"data":{"histogram2dcontour":[{"type":"histogram2dcontour","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"choropleth":[{"type":"choropleth","colorbar":{"outlinewidth":0,"ticks":""}}],"histogram2d":[{"type":"histogram2d","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"heatmap":[{"type":"heatmap","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"contourcarpet":[{"type":"contourcarpet","colorbar":{"outlinewidth":0,"ticks":""}}],"contour":[{"type":"contour","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"surface":[{"type":"surface","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"mesh3d":[{"type":"mesh3d","colorbar":{"outlinewidth":0,"ticks":""}}],"scatter":[{"fillpattern":{"fillmode":"overlay","size":10,"solidity":0.2},"type":"scatter"}],"parcoords":[{"type":"parcoords","line":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatterpolargl":[{"type":"scatterpolargl","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"bar":[{"error_x":{"color":"#2a3f5f"},"error_y":{"color":"#2a3f5f"},"marker":{"line":{"color":"#E5ECF6","width":0.5},"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"bar"}],"scattergeo":[{"type":"scattergeo","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatterpolar":[{"type":"scatterpolar","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"histogram":[{"marker":{"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"histogram"}],"scattergl":[{"type":"scattergl","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatter3d":[{"type":"scatter3d","line":{"colorbar":{"outlinewidth":0,"ticks":""}},"marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scattermap":[{"type":"scattermap","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scattermapbox":[{"type":"scattermapbox","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatterternary":[{"type":"scatterternary","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scattercarpet":[{"type":"scattercarpet","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"carpet":[{"aaxis":{"endlinecolor":"#2a3f5f","gridcolor":"white","linecolor":"white","minorgridcolor":"white","startlinecolor":"#2a3f5f"},"baxis":{"endlinecolor":"#2a3f5f","gridcolor":"white","linecolor":"white","minorgridcolor":"white","startlinecolor":"#2a3f5f"},"type":"carpet"}],"table":[{"cells":{"fill":{"color":"#EBF0F8"},"line":{"color":"white"}},"header":{"fill":{"color":"#C8D4E3"},"line":{"color":"white"}},"type":"table"}],"barpolar":[{"marker":{"line":{"color":"#E5ECF6","width":0.5},"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"barpolar"}],"pie":[{"automargin":true,"type":"pie"}]},"layout":{"autotypenumbers":"strict","colorway":["#636efa","#EF553B","#00cc96","#ab63fa","#FFA15A","#19d3f3","#FF6692","#B6E880","#FF97FF","#FECB52"],"font":{"color":"#2a3f5f"},"hovermode":"closest","hoverlabel":{"align":"left"},"paper_bgcolor":"white","plot_bgcolor":"#E5ECF6","polar":{"bgcolor":"#E5ECF6","angularaxis":{"gridcolor":"white","linecolor":"white","ticks":""},"radialaxis":{"gridcolor":"white","linecolor":"white","ticks":""}},"ternary":{"bgcolor":"#E5ECF6","aaxis":{"gridcolor":"white","linecolor":"white","ticks":""},"baxis":{"gridcolor":"white","linecolor":"white","ticks":""},"caxis":{"gridcolor":"white","linecolor":"white","ticks":""}},"coloraxis":{"colorbar":{"outlinewidth":0,"ticks":""}},"colorscale":{"sequential":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"sequentialminus":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"diverging":[[0,"#8e0152"],[0.1,"#c51b7d"],[0.2,"#de77ae"],[0.3,"#f1b6da"],[0.4,"#fde0ef"],[0.5,"#f7f7f7"],[0.6,"#e6f5d0"],[0.7,"#b8e186"],[0.8,"#7fbc41"],[0.9,"#4d9221"],[1,"#276419"]]},"xaxis":{"gridcolor":"white","linecolor":"white","ticks":"","title":{"standoff":15},"zerolinecolor":"white","automargin":true,"zerolinewidth":2},"yaxis":{"gridcolor":"white","linecolor":"white","ticks":"","title":{"standoff":15},"zerolinecolor":"white","automargin":true,"zerolinewidth":2},"scene":{"xaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white","gridwidth":2},"yaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white","gridwidth":2},"zaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white","gridwidth":2}},"shapedefaults":{"line":{"color":"#2a3f5f"}},"annotationdefaults":{"arrowcolor":"#2a3f5f","arrowhead":0,"arrowwidth":1},"geo":{"bgcolor":"white","landcolor":"#E5ECF6","subunitcolor":"white","showland":true,"showlakes":true,"lakecolor":"white"},"title":{"x":0.05},"mapbox":{"style":"light"}}},"xaxis":{"anchor":"y","domain":[0.0,1.0],"title":{"text":"Registration Year"},"dtick":1},"yaxis":{"anchor":"x","domain":[0.0,1.0],"title":{"text":"Total Signatures"}},"legend":{"tracegroupgap":0,"itemsizing":"constant","title":{"text":"primary_policy_area"}},"title":{"text":"Signatures per Initiative by Year"},"margin":{"l":20,"r":20,"t":50,"b":20},"height":400},                        {"responsive": true}                    )                };            </script>        </div>
</div>
```

`./page_to_export/partials/chart_top_10_signatures.html`:
```
<div class="card">
<div>                            <div id="chart-top10-signatures" class="plotly-graph-div" style="height:400px; width:100%;"></div>            <script type="text/javascript">                window.PLOTLYENV=window.PLOTLYENV || {};                                if (document.getElementById("chart-top10-signatures")) {                    Plotly.newPlot(                        "chart-top10-signatures",                        [{"customdata":[[5,"Strengthen the right to repair by extending spare-parts\u003cbr\u003eavailability, mandating repairability scores, and limiting\u003cbr\u003esoftware locks that hinder repair.","The Commission has registered the initiative and refers to\u003cbr\u003ethe Sustainable Products Initiative and right-to-repair\u003cbr\u003emeasures. It will assess the requested extensions within the\u003cbr\u003eexisting legislative framework.","https:\u002f\u002fcitizens-initiative.europa.eu\u002finitiatives\u002feu-right-to-repair-plus_en"],[6,"Prohibit real-time facial recognition and biometric mass\u003cbr\u003esurveillance in publicly accessible spaces across the EU,\u003cbr\u003ewith narrow exceptions.","The Commission has registered the initiative and notes the\u003cbr\u003eapplicable framework under the AI Act and data protection\u003cbr\u003erules. It will assess whether additional EU measures are\u003cbr\u003eneeded within security and fundamental-rights constraints.","https:\u002f\u002fcitizens-initiative.europa.eu\u002finitiatives\u002fban-facial-recognition-public_en"],[5,"Ensure that AI systems used in employment contexts are\u003cbr\u003esubject to human oversight, algorithmic transparency, and\u003cbr\u003eworkers' right to explanation for any automated decision\u003cbr\u003eaffecting their employment conditions.","The Commission is reviewing the submitted request. Under the\u003cbr\u003eAI Act, high-risk AI systems used in employment are subject\u003cbr\u003eto transparency and human oversight requirements. Further\u003cbr\u003emeasures to strengthen workers' rights are under\u003cbr\u003econsideration.","https:\u002f\u002fcitizens-initiative.europa.eu\u002finitiatives\u002fai-regulation-workers_en"],[8,"Introduce a progressive EU-wide net wealth tax on\u003cbr\u003eindividuals holding assets above \u20ac1 million to fund the\u003cbr\u003egreen transition, reduce inequality, and finance public\u003cbr\u003eservices across member states.","The Commission is reviewing the initiative. Tax policy\u003cbr\u003eremains primarily a member state competence. The Commission\u003cbr\u003ewill explore whether EU-level coordination mechanisms on\u003cbr\u003ewealth taxation can complement existing anti-avoidance\u003cbr\u003eframeworks.","https:\u002f\u002fcitizens-initiative.europa.eu\u002finitiatives\u002ftax-the-rich_en"],[11,"Restore biodiversity and transition to nature-friendly\u003cbr\u003efarming by reducing synthetic pesticide use by 80% by 2030\u003cbr\u003eand restoring natural ecosystems on at least 10% of\u003cbr\u003eagricultural land.","The Commission confirms its commitment to reduce chemical\u003cbr\u003epesticide use and risk by 50% and more hazardous pesticides\u003cbr\u003eby 50% by 2030, as set out in the Farm to Fork and\u003cbr\u003eBiodiversity Strategies, and will present a legislative\u003cbr\u003eproposal accordingly.","https:\u002f\u002fcitizens-initiative.europa.eu\u002finitiatives\u002fsave-bees-and-farmers_en"],[12,"Prohibit the import, export, sale, and offer for sale of\u003cbr\u003eloose shark fins and all products containing shark fins\u003cbr\u003eother than fins naturally attached to the shark's body in\u003cbr\u003ethe European Union.","The Commission is conducting an impact assessment to\u003cbr\u003eevaluate extending the 'fins naturally attached' policy to\u003cbr\u003eimports and exports. A legislative proposal addressing the\u003cbr\u003eshark fin trade is expected within the current mandate.","https:\u002f\u002fcitizens-initiative.europa.eu\u002finitiatives\u002fstop-finning-stop-the-trade_en"],[14,"Propose legislation to phase out and ultimately prohibit the\u003cbr\u003euse of cages for farmed animals including laying hens,\u003cbr\u003erabbits, pullets, broiler breeders, layer breeders, quail,\u003cbr\u003educks and geese.","The Commission commits to propose legislation to phase out\u003cbr\u003eand ban the use of cages for all animals listed in the\u003cbr\u003einitiative by 2027, in line with the Farm to Fork Strategy\u003cbr\u003eobjectives and following a thorough impact assessment.","https:\u002f\u002fcitizens-initiative.europa.eu\u002finitiatives\u002fend-cage-age_en"],[16,"Ban the farming of animals for their fur across all EU\u003cbr\u003emember states and prohibit the import and export of fur and\u003cbr\u003efur products into and from the EU.","The Commission acknowledges the citizens' concerns regarding\u003cbr\u003eanimal welfare in fur farming. It will assess the\u003cbr\u003efeasibility of an EU-wide ban in the context of the upcoming\u003cbr\u003erevision of the Animal Welfare legislation and the Farm to\u003cbr\u003eFork Strategy.","https:\u002f\u002fcitizens-initiative.europa.eu\u002finitiatives\u002ffur-free-europe_en"],[18,"Recognise access to safe drinking water and sanitation as a\u003cbr\u003ehuman right, exclude water services from internal market\u003cbr\u003erules and liberalisation, and strengthen EU efforts to\u003cbr\u003eachieve universal access to water and sanitation.","Following the European Citizens' Initiative 'Right2Water',\u003cbr\u003ethe Commission carried out a public consultation and adopted\u003cbr\u003ea Communication reaffirming the commitment that water is a\u003cbr\u003epublic good and a human right. The revised Drinking Water\u003cbr\u003eDirective adopted in 2020 strengthens the universal access\u003cbr\u003eobligation.","https:\u002f\u002fcitizens-initiative.europa.eu\u002finitiatives\u002fright-to-water_en"],[19,"Prohibit the EU from financing activities which presuppose\u003cbr\u003ethe destruction of human embryos in particular in the areas\u003cbr\u003eof research development aid and public health.","The organizers formally withdrew the initiative before the\u003cbr\u003eCommission issued a substantive response. The withdrawal was\u003cbr\u003esubmitted to the Secretariat-General and the initiative was\u003cbr\u003eclosed without a Commission Communication being adopted.","https:\u002f\u002fcitizens-initiative.europa.eu\u002finitiatives\u002fone-of-us_en"]],"hovertemplate":"\u003cb\u003e%{y}\u003c\u002fb\u003e\u003cbr\u003e\u003cbr\u003e\u003cb\u003eSignatures:\u003c\u002fb\u003e %{x:,.0f}\u003cbr\u003e\u003cb\u003eCountries Threshold Met:\u003c\u002fb\u003e %{customdata[0]}\u002f27\u003cbr\u003e\u003cbr\u003e\u003cb\u003eObjective:\u003c\u002fb\u003e\u003cbr\u003e%{customdata[1]}\u003cbr\u003e\u003cbr\u003e\u003cb\u003eCommission Response:\u003c\u002fb\u003e\u003cbr\u003e%{customdata[2]}\u003cbr\u003e\u003cbr\u003e\u003ci\u003e\ud83d\udd17 Click to open initiative page\u003c\u002fi\u003e\u003cextra\u003e\u003c\u002fextra\u003e","marker":{"color":["rgb(213,121,70)","rgb(219,140,71)","rgb(222,146,71)","rgb(183,215,126)","rgb(176,212,126)","rgb(167,208,125)","rgb(129,192,120)","rgb(114,186,119)","rgb(92,177,116)","rgb(60,163,113)"],"line":{"color":"white","width":0.5}},"orientation":"h","x":{"dtype":"i4","bdata":"gLcEACRYBgDQ3QYApEIPAHAWEAD8FhEAeVEVAG\u002fsFgCXUhkAdPQcAA=="},"y":["EU Right to Repair Plus","Ban Facial Recognition in Public","AI Regulation for Workers","Tax the Rich","Save Bees and Farmers","Stop Finning - Stop the Trade","End the Cage Age","Fur Free Europe","Right to Water","One of Us"],"type":"bar"}],                        {"template":{"data":{"histogram2dcontour":[{"type":"histogram2dcontour","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"choropleth":[{"type":"choropleth","colorbar":{"outlinewidth":0,"ticks":""}}],"histogram2d":[{"type":"histogram2d","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"heatmap":[{"type":"heatmap","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"contourcarpet":[{"type":"contourcarpet","colorbar":{"outlinewidth":0,"ticks":""}}],"contour":[{"type":"contour","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"surface":[{"type":"surface","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"mesh3d":[{"type":"mesh3d","colorbar":{"outlinewidth":0,"ticks":""}}],"scatter":[{"fillpattern":{"fillmode":"overlay","size":10,"solidity":0.2},"type":"scatter"}],"parcoords":[{"type":"parcoords","line":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatterpolargl":[{"type":"scatterpolargl","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"bar":[{"error_x":{"color":"#2a3f5f"},"error_y":{"color":"#2a3f5f"},"marker":{"line":{"color":"#E5ECF6","width":0.5},"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"bar"}],"scattergeo":[{"type":"scattergeo","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatterpolar":[{"type":"scatterpolar","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"histogram":[{"marker":{"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"histogram"}],"scattergl":[{"type":"scattergl","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatter3d":[{"type":"scatter3d","line":{"colorbar":{"outlinewidth":0,"ticks":""}},"marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scattermap":[{"type":"scattermap","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scattermapbox":[{"type":"scattermapbox","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatterternary":[{"type":"scatterternary","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scattercarpet":[{"type":"scattercarpet","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"carpet":[{"aaxis":{"endlinecolor":"#2a3f5f","gridcolor":"white","linecolor":"white","minorgridcolor":"white","startlinecolor":"#2a3f5f"},"baxis":{"endlinecolor":"#2a3f5f","gridcolor":"white","linecolor":"white","minorgridcolor":"white","startlinecolor":"#2a3f5f"},"type":"carpet"}],"table":[{"cells":{"fill":{"color":"#EBF0F8"},"line":{"color":"white"}},"header":{"fill":{"color":"#C8D4E3"},"line":{"color":"white"}},"type":"table"}],"barpolar":[{"marker":{"line":{"color":"#E5ECF6","width":0.5},"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"barpolar"}],"pie":[{"automargin":true,"type":"pie"}]},"layout":{"autotypenumbers":"strict","colorway":["#636efa","#EF553B","#00cc96","#ab63fa","#FFA15A","#19d3f3","#FF6692","#B6E880","#FF97FF","#FECB52"],"font":{"color":"#2a3f5f"},"hovermode":"closest","hoverlabel":{"align":"left"},"paper_bgcolor":"white","plot_bgcolor":"#E5ECF6","polar":{"bgcolor":"#E5ECF6","angularaxis":{"gridcolor":"white","linecolor":"white","ticks":""},"radialaxis":{"gridcolor":"white","linecolor":"white","ticks":""}},"ternary":{"bgcolor":"#E5ECF6","aaxis":{"gridcolor":"white","linecolor":"white","ticks":""},"baxis":{"gridcolor":"white","linecolor":"white","ticks":""},"caxis":{"gridcolor":"white","linecolor":"white","ticks":""}},"coloraxis":{"colorbar":{"outlinewidth":0,"ticks":""}},"colorscale":{"sequential":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"sequentialminus":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"diverging":[[0,"#8e0152"],[0.1,"#c51b7d"],[0.2,"#de77ae"],[0.3,"#f1b6da"],[0.4,"#fde0ef"],[0.5,"#f7f7f7"],[0.6,"#e6f5d0"],[0.7,"#b8e186"],[0.8,"#7fbc41"],[0.9,"#4d9221"],[1,"#276419"]]},"xaxis":{"gridcolor":"white","linecolor":"white","ticks":"","title":{"standoff":15},"zerolinecolor":"white","automargin":true,"zerolinewidth":2},"yaxis":{"gridcolor":"white","linecolor":"white","ticks":"","title":{"standoff":15},"zerolinecolor":"white","automargin":true,"zerolinewidth":2},"scene":{"xaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white","gridwidth":2},"yaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white","gridwidth":2},"zaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white","gridwidth":2}},"shapedefaults":{"line":{"color":"#2a3f5f"}},"annotationdefaults":{"arrowcolor":"#2a3f5f","arrowhead":0,"arrowwidth":1},"geo":{"bgcolor":"white","landcolor":"#E5ECF6","subunitcolor":"white","showland":true,"showlakes":true,"lakecolor":"white"},"title":{"x":0.05},"mapbox":{"style":"light"}}},"title":{"text":"Top 10 Initiatives by Signatures (All-Time)","x":0.015,"xanchor":"left"},"margin":{"l":20,"r":20,"t":50,"b":20},"yaxis":{"title":{"text":""},"ticksuffix":"   "},"height":400,"xaxis":{"title":{"text":"Signatures"}},"showlegend":false,"clickmode":"event","shapes":[{"line":{"color":"#3AB23F","dash":"dash","width":2},"type":"line","x0":1000000,"x1":1000000,"xref":"x","y0":0,"y1":1,"yref":"y domain"}],"annotations":[{"font":{"color":"#3AB23F","size":13},"showarrow":false,"text":"1M threshold","x":1000000,"xanchor":"left","xref":"x","y":1,"yanchor":"top","yref":"y domain"}]},                        {"responsive": true}                    )                };            </script>        </div>
<style>
  #chart-top10-signatures .bars path { cursor: pointer !important; }
</style>
<script>
(function () {
  var el = document.getElementById("chart-top10-signatures");
  var drag = el.querySelector(".nsewdrag");

  el.on("plotly_hover", function () {
    if (drag) drag.style.cursor = "pointer";
  });
  el.on("plotly_unhover", function () {
    if (drag) drag.style.cursor = "default";
  });
  el.on("plotly_click", function (data) {
    var url = data.points[0].customdata[3];
    if (url) window.open(url, "_blank", "noopener,noreferrer");
  });
})();
</script>

</div>
```

`./page_to_export/partials/deep_dive_footer.html`:
```
<div class="deep-dive-banner">
  <a
    href="https://www.kaggle.com/code/lukkardata/eci-commission-response"
    target="_blank"
    rel="noopener noreferrer"
    class="deep-dive-link"
  >
    💡 Deep Dive Breakdown
  </a>
</div>


```

`./page_to_export/partials/header.html`:
```
<h1>🇪🇺 European Citizens' Initiatives Tracker</h1>
```

`./page_to_export/partials/kpi_row.html`:
```
<div class="kpi-row">
      <div class="kpi-card">
        <span class="kpi-label">📋 Total Initiatives:</span>
        <span class="kpi-value" style="color:#333">29</span>
      </div>
      <div class="kpi-card">
        <span class="kpi-label">🗳️ Currently Open:</span>
        <span class="kpi-value" style="color:#1069c0">12</span>
      </div>
      <div class="kpi-card">
        <span class="kpi-label">✅ Reached 1M Signatures:</span>
        <span class="kpi-value" style="color:#557B2D">7</span>
      </div>
      <div class="kpi-card">
        <span class="kpi-label">📬 Got EU Response:</span>
        <span class="kpi-value" style="color:#006064">4</span>
      </div>
      <div class="kpi-card">
        <span class="kpi-label">⚖️ Led to Legislation:</span>
        <span class="kpi-value" style="color:#6a1b9a">2</span>
      </div>
</div>
```

`./page_to_export/partials/list_currently_open.html`:
```
<div class="card">
<h3 class="card__title">🗳️ Currently Open: <span class="card__count">12</span></h3>
<div class="data-table__scroll-wrapper">
<table class="data-table">
  <thead>
    <tr>
      <th>Initiative</th>
      <th>Objective</th>
      <th>Signatures</th>
      <th>Countries Threshold</th>
    </tr>
  </thead>
  <tbody>
    
        <tr>
          <td><a href="https://citizens-initiative.europa.eu/initiatives/tax-the-rich_en" target="_blank" rel="noopener noreferrer">Tax the Rich</a></td>
          <td>Introduce a progressive EU-wide net wealth tax on individuals holding assets above €1 million to fu…</td>
          <td>1,000,100<div class="progress-bar"><div class="progress-bar__fill progress-bar__fill--signatures progress-bar__fill--over" style="width:100.0%"></div></div></td>
          <td>8 / 7<div class="progress-bar"><div class="progress-bar__fill progress-bar__fill--threshold progress-bar__fill--over" style="width:100.0%"></div></div></td>
        </tr>
        <tr>
          <td><a href="https://citizens-initiative.europa.eu/initiatives/ai-regulation-workers_en" target="_blank" rel="noopener noreferrer">AI Regulation for Workers</a></td>
          <td>Ensure that AI systems used in employment contexts are subject to human oversight, algorithmic tran…</td>
          <td>450,000<div class="progress-bar"><div class="progress-bar__fill progress-bar__fill--signatures" style="width:45.0%"></div></div></td>
          <td>5 / 7<div class="progress-bar"><div class="progress-bar__fill progress-bar__fill--threshold" style="width:71.4%"></div></div></td>
        </tr>
        <tr>
          <td><a href="https://citizens-initiative.europa.eu/initiatives/ban-facial-recognition-public_en" target="_blank" rel="noopener noreferrer">Ban Facial Recognition in Public</a></td>
          <td>Prohibit real-time facial recognition and biometric mass surveillance in publicly accessible spaces…</td>
          <td>415,780<div class="progress-bar"><div class="progress-bar__fill progress-bar__fill--signatures" style="width:41.6%"></div></div></td>
          <td>6 / 7<div class="progress-bar"><div class="progress-bar__fill progress-bar__fill--threshold" style="width:85.7%"></div></div></td>
        </tr>
        <tr>
          <td><a href="https://citizens-initiative.europa.eu/initiatives/eu-right-to-repair-plus_en" target="_blank" rel="noopener noreferrer">EU Right to Repair Plus</a></td>
          <td>Strengthen the right to repair by extending spare-parts availability, mandating repairability score…</td>
          <td>309,120<div class="progress-bar"><div class="progress-bar__fill progress-bar__fill--signatures" style="width:30.9%"></div></div></td>
          <td>5 / 7<div class="progress-bar"><div class="progress-bar__fill progress-bar__fill--threshold" style="width:71.4%"></div></div></td>
        </tr>
        <tr>
          <td><a href="https://citizens-initiative.europa.eu/initiatives/fair-digital-platform-work_en" target="_blank" rel="noopener noreferrer">Fair Digital Platform Work</a></td>
          <td>Guarantee minimum standards for platform workers, including transparent algorithmic management, fai…</td>
          <td>263,900<div class="progress-bar"><div class="progress-bar__fill progress-bar__fill--signatures" style="width:26.4%"></div></div></td>
          <td>4 / 7<div class="progress-bar"><div class="progress-bar__fill progress-bar__fill--threshold" style="width:57.1%"></div></div></td>
        </tr>
        <tr>
          <td><a href="https://citizens-initiative.europa.eu/initiatives/ban-pfas-forever-chemicals_en" target="_blank" rel="noopener noreferrer">Ban PFAS Forever Chemicals</a></td>
          <td>Phase out PFAS in consumer products and industrial uses where safer alternatives exist, with strict…</td>
          <td>188,450<div class="progress-bar"><div class="progress-bar__fill progress-bar__fill--signatures" style="width:18.8%"></div></div></td>
          <td>3 / 7<div class="progress-bar"><div class="progress-bar__fill progress-bar__fill--threshold" style="width:42.9%"></div></div></td>
        </tr>
        <tr>
          <td><a href="https://citizens-initiative.europa.eu/initiatives/stop-greenwashing-claims_en" target="_blank" rel="noopener noreferrer">Stop Greenwashing Claims</a></td>
          <td>Prohibit misleading environmental marketing claims by requiring substantiation, standard labels, an…</td>
          <td>144,500<div class="progress-bar"><div class="progress-bar__fill progress-bar__fill--signatures" style="width:14.4%"></div></div></td>
          <td>3 / 7<div class="progress-bar"><div class="progress-bar__fill progress-bar__fill--threshold" style="width:42.9%"></div></div></td>
        </tr>
        <tr>
          <td><a href="https://citizens-initiative.europa.eu/initiatives/european-rail-night-revival_en" target="_blank" rel="noopener noreferrer">European Rail Night Revival</a></td>
          <td>Create an EU framework to expand cross-border night trains, improve ticketing interoperability, and…</td>
          <td>121,330<div class="progress-bar"><div class="progress-bar__fill progress-bar__fill--signatures" style="width:12.1%"></div></div></td>
          <td>2 / 7<div class="progress-bar"><div class="progress-bar__fill progress-bar__fill--threshold" style="width:28.6%"></div></div></td>
        </tr>
        <tr>
          <td><a href="https://citizens-initiative.europa.eu/initiatives/europe-for-mental-health_en" target="_blank" rel="noopener noreferrer">Europe for Mental Health</a></td>
          <td>Adopt an EU mental health action plan with minimum service standards, prevention measures, and dedi…</td>
          <td>97,640<div class="progress-bar"><div class="progress-bar__fill progress-bar__fill--signatures" style="width:9.8%"></div></div></td>
          <td>2 / 7<div class="progress-bar"><div class="progress-bar__fill progress-bar__fill--threshold" style="width:28.6%"></div></div></td>
        </tr>
        <tr>
          <td><a href="https://citizens-initiative.europa.eu/initiatives/clean-air-for-europe_en" target="_blank" rel="noopener noreferrer">Clean Air for Europe</a></td>
          <td>Set binding EU-wide air quality targets aligned with WHO guidelines, strengthen enforcement, and ex…</td>
          <td>74,210<div class="progress-bar"><div class="progress-bar__fill progress-bar__fill--signatures" style="width:7.4%"></div></div></td>
          <td>1 / 7<div class="progress-bar"><div class="progress-bar__fill progress-bar__fill--threshold" style="width:14.3%"></div></div></td>
        </tr>
        <tr>
          <td><a href="https://citizens-initiative.europa.eu/initiatives/european-accessible-cities_en" target="_blank" rel="noopener noreferrer">European Accessible Cities</a></td>
          <td>Ensure barrier-free access in public spaces and transport by setting EU accessibility benchmarks fo…</td>
          <td>68,320<div class="progress-bar"><div class="progress-bar__fill progress-bar__fill--signatures" style="width:6.8%"></div></div></td>
          <td>1 / 7<div class="progress-bar"><div class="progress-bar__fill progress-bar__fill--threshold" style="width:14.3%"></div></div></td>
        </tr>
        <tr>
          <td><a href="https://citizens-initiative.europa.eu/initiatives/protect-whistleblowers-eu-funds_en" target="_blank" rel="noopener noreferrer">Protect Whistleblowers in EU Funds</a></td>
          <td>Improve protection for whistleblowers reporting fraud and corruption involving EU funds, with secur…</td>
          <td>55,860<div class="progress-bar"><div class="progress-bar__fill progress-bar__fill--signatures" style="width:5.6%"></div></div></td>
          <td>1 / 7<div class="progress-bar"><div class="progress-bar__fill progress-bar__fill--threshold" style="width:14.3%"></div></div></td>
        </tr>
  </tbody>
</table>
</div>
</div>
```

`./page_to_export/script/back_to_top.js`:
```
const backToTopBtn = document.getElementById("back-to-top");

window.addEventListener("scroll", () => {
    backToTopBtn.classList.toggle("visible", window.scrollY > 300);
});

backToTopBtn.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
});
```

`./page_to_export/script/partials.js`:
```
async function loadPartial(url, targetId) {
    const res = await fetch(url);
    const html = await res.text();
    const target = document.getElementById(targetId);
    target.innerHTML = html;
    target.querySelectorAll("script").forEach(old => {
        const s = document.createElement("script");
        s.textContent = old.textContent;
        old.replaceWith(s);
    });
}

(async () => {
    await loadPartial("partials/header.html", "header-slot");
    await loadPartial("partials/deep_dive_footer.html", "footer-slot");
    await loadPartial("partials/kpi_row.html", "kpi-slot");
    await loadPartial("partials/chart_top_10_signatures.html", "chart1-slot");
    await loadPartial("partials/chart_outcomes.html", "chart-initiatives-status-slot");
    await loadPartial("partials/chart_signatures_cohorts.html", "chart-signatures-count-slot");
    await loadPartial("partials/list_currently_open.html", "currently-open");
})();
```

`./page_to_export/styles/base.css`:
```
/*
  Base page styles for the ECI Dashboard.
  - Sets a light grey background with a clean sans-serif font and no default browser margins.
  - All content is wrapped in a centred, max-width container to keep the layout readable on wide screens.
  - Cards are white panels with rounded corners and a soft shadow to visually separate sections.
  - The bottom row uses flexbox to place two charts side by side, collapsing to a single column on mobile screens.
*/

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  margin: 0;
  padding: 20px;
  background-color: #f5f7f9;
}

h1 {
  text-align: center;
  color: #2A3F5F;
  margin-bottom: 15px;
}

.dashboard-container {
  max-width: 1200px;
  margin: 0 auto;
}

.card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  padding: 15px;
  margin-bottom: 20px;
}

.row-top-10-graph {
  display: flex;
  flex-direction: column;
}

.bottom-row {
  display: flex;
  gap: 20px;
}

.bottom-col {
  flex: 1;
  min-width: 0;
}

@media (max-width: 768px) {
  .bottom-row {
    flex-direction: column;
  }
}

```

`./page_to_export/styles/buttons.css`:
```
/*
  Styles for the deep-dive navigation banner and the back-to-top button.
  - Deep-dive banner: a full-width centred row acting as a section link to a detailed page.
  - Deep-dive link: a navy pill-shaped button that fades to light blue on hover.
  - Back-to-top button: a fixed circle pinned to the bottom-right corner, hidden until triggered by JS.
  - Visibility: controlled via opacity and pointer-events so it fades in/out smoothly without layout shifts.
  - Hover states: both elements share the same light-blue colour scheme on interaction.
*/

.deep-dive-banner {
  display: inline-flex;
  justify-content: center;
  width: 100%;
  margin: 0 0 30px 0;
}

.deep-dive-link {
  padding: 8px 20px;
  background: #003399;
  border-radius: 20px;
  color: #fafafa;
  font-size: 0.9rem;
  font-weight: 600;
  text-decoration: none;
  transition: background 0.2s ease, color 0.2s ease;
}

.deep-dive-link:hover {
  background: #e0e7ff;
  color: #1069c0;
}

/* Back-to-top button */
.back-to-top-btn {
  position: fixed;
  bottom: 2rem;
  right: 3rem;
  width: 2.75rem;
  height: 2.75rem;
  border-radius: 50%;
  border: none;
  background-color: #003399;
  color: #fff;
  font-size: 2rem;
  line-height: 3.6rem;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);

  /* hidden by default */
  opacity: 0;
  pointer-events: none;
  transform: translateY(0.5rem);
  transition: opacity 0.25s ease, transform 0.25s ease,
              background-color 0.2s ease, color 0.2s ease;
  z-index: 999;
}

.back-to-top-btn:hover {
  background-color: #e0e7ff;
  color: #1069c0;
}

.back-to-top-btn.visible {
  opacity: 1;
  pointer-events: all;
  transform: translateY(0);
}

.back-to-top-btn:focus-visible {
  outline: 3px solid #0d6efd;
  outline-offset: 3px;
}

```

`./page_to_export/styles/kpi.css`:
```
/*
  Styles for the KPI counter row — the strip of headline numbers at the top of the dashboard.
  - Cards are laid out side by side using flexbox, each taking equal width.
  - A thin right border acts as a visual divider between cards; the last card has none.
  - Large bold numbers draw the eye, with a small label above each value.
  - On mobile the row stacks vertically, switching dividers from right borders to bottom borders.
*/

.kpi-row {
    display: flex;
    gap: 0;
    border-radius: 8px;
    background: white;
    margin-bottom: 20px;
    overflow: hidden;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05); 
}
.kpi-card {
    flex: 1;
    display: flex;
    flex-direction: column;
    padding: 14px 20px;
    border-right: 4px solid #f5f7f9;
}
.kpi-card:last-child { border-right: none; }
.kpi-header {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 6px;
}
.kpi-label {
    font-size: 0.8rem;
    white-space: nowrap;
    text-align: center;
    color: #2A3F5F;
    margin-bottom: 8px;
}
.kpi-body {
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.kpi-value {
    font-size: 2rem;
    font-weight: 700;
    line-height: 1;
    text-align: center;

}
@media (max-width: 768px) {
    .kpi-row { flex-direction: column; }
    .kpi-card { border-right: none; border-bottom: 1px solid #e0e8f0; }
    .kpi-card:last-child { border-bottom: none; }
}
```

`./page_to_export/styles/styles.css`:
```
/*
  Entry point for all dashboard styles.
*/

@import "./base.css";
@import "./kpi.css";
@import "./table.css";
@import "./buttons.css";

```

`./page_to_export/styles/table.css`:
```
/*
  Styles for the currently-open initiatives table and its supporting elements.
  - The scroll wrapper constrains the table to ~5 visible rows with a fade-out gradient at the bottom.
  - A custom navy scrollbar is applied cross-browser via both the modern and webkit APIs.
  - Table headers are uppercase and bold; rows highlight on hover for readability.
  - Progress bars beneath each row show signature and country-threshold progress with colour-coded fills.
  - An amber override colour is applied when a bar value exceeds its maximum target.
*/

.card__title {
  font-size: 1rem;
  font-weight: 400;
  color: #2a3f5f;
  display: flex;
  align-items: center;
  gap: 8px;
}

.card__count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #1069c0;
  font-size: 1.3rem;
  font-weight: 700;
  letter-spacing: 0.02em;
}

.data-table__scroll-wrapper {
  max-height: 320px;
  overflow-y: auto;
  position: relative;
}

.data-table__scroll-wrapper::after {
  content: "";
  position: sticky;
  bottom: 0;
  left: 0;
  display: block;
  width: 100%;
  height: 48px;
  background: linear-gradient(to bottom, transparent, rgba(255, 255, 255, 0.92));
  pointer-events: none;
  border-radius: 0 0 6px 6px;
  transition: opacity 0.2s ease;
}

.data-table__scroll-wrapper.is-scrolled-end::after { opacity: 0; }
.data-table__scroll-wrapper .data-table { border: none; }

@supports (scrollbar-width: auto) {
  .data-table__scroll-wrapper {
    scrollbar-width: thin;
    scrollbar-color: #003399 #f0f4fa;
  }
}

@supports selector(::-webkit-scrollbar) {
  .data-table__scroll-wrapper::-webkit-scrollbar { width: 6px; }
  .data-table__scroll-wrapper::-webkit-scrollbar-track {
    background: #f0f4fa;
    border-radius: 0 6px 6px 0;
  }
  .data-table__scroll-wrapper::-webkit-scrollbar-thumb {
    background-color: #0d6efd;
    border-radius: 6px;
  }
  .data-table__scroll-wrapper::-webkit-scrollbar-thumb:hover {
    background-color: #0d6efd;
  }
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
  color: #2a3f5f;
}

.data-table thead tr {
  background-color: #f0f4fa;
  border-bottom: 2px solid #d0d9e8;
}

.data-table thead th {
  padding: 10px 14px;
  text-align: left;
  font-weight: 700;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #2a3f5f;
  white-space: nowrap;

  /* ✅ Sticky header */
  position: sticky;
  top: 0;
  background-color: #f0f4fa; /* must be explicit — prevents rows showing through */
  z-index: 1;      
}

.data-table tbody tr {
  border-bottom: 1px solid #edf0f5;
  transition: background-color 0.15s ease;
}

.data-table tbody tr:last-child { border-bottom: none; }
.data-table tbody tr:hover { background-color: #f7f9fd; }

.data-table td {
  padding: 10px 14px;
  vertical-align: top;
  line-height: 1.5;
}

.data-table td:first-child { font-weight: 600; white-space: nowrap; }
.data-table td:first-child a { color: #1069c0; text-decoration: none; }
.data-table td:first-child a:hover { text-decoration: underline; color: #0a4d9c; }
.data-table td:nth-child(2) { color: #2a3f5f; font-size: 0.82rem; }

.list-empty {
  color: #8a9ab0;
  font-style: italic;
  font-size: 0.875rem;
  margin: 8px 0 0 0;
}

.progress-bar {
  margin-top: 5px;
  height: 4px;
  background-color: #e8edf5;
  border-radius: 2px;
  overflow: hidden;
  width: 100%;
}

.progress-bar__fill {
  height: 100%;
  border-radius: 2px;
  transition: width 0.4s ease;
}

.progress-bar__fill--signatures { background-color: #4a7fb5; }
.progress-bar__fill--threshold  { background-color: #0d9488; }
.progress-bar__fill--over {
  background-color: #f0a500 !important;
  box-shadow: 0 0 4px rgba(240, 165, 0, 0.5);
}

```

