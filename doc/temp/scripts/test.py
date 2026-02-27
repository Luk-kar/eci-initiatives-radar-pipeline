from pathlib import Path
import pandas as pd
import plotly.express as px

# ----------------------------
# 1. Setup Data & Paths
# ----------------------------
# Change parents[1] to parents[0] if this script is in the root directory
REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"
DOCS_DIR = REPO_ROOT / "docs"
DOCS_DIR.mkdir(parents=True, exist_ok=True)

# Read the dummy data
df = pd.read_csv(DATA_DIR / "eci_initiatives.csv")

# Fill empty outcomes with "Pending" for the donut chart
if "commission_outcome" in df.columns:
    df["commission_outcome"] = df["commission_outcome"].fillna("Pending")

# ----------------------------
# 2. Build Plotly Charts
# ----------------------------
# Apply standard Plotly white template
px.defaults.template = "plotly_white"

# Chart 1: Bar Chart of Signatures by Policy Area (Top)
df_grouped = df.groupby("primary_policy_area", as_index=False)[
    "signatures_numeric"
].sum()
fig1 = px.bar(
    df_grouped,
    x="primary_policy_area",
    y="signatures_numeric",
    title="Total Signatures by Policy Area",
    color="primary_policy_area",
    text_auto=".2s",  # Automatically adds readable numbers to bars (e.g., 1.5M)
)
fig1.update_layout(
    height=400,
    margin=dict(l=20, r=20, t=50, b=20),
    xaxis_title="Policy Area",
    yaxis_title="Total Signatures",
)

# Chart 2: Donut Chart of Commission Outcomes (Bottom Left)
outcome_counts = df["commission_outcome"].value_counts().reset_index()
outcome_counts.columns = ["Outcome", "Count"]
fig2 = px.pie(
    outcome_counts,
    names="Outcome",
    values="Count",
    title="Initiatives by Commission Outcome",
    hole=0.45,  # This creates the Donut effect
    color_discrete_sequence=px.colors.qualitative.Pastel,
)
fig2.update_traces(textposition="inside", textinfo="percent+label")
fig2.update_layout(height=400, margin=dict(l=20, r=20, t=50, b=20), showlegend=False)

# Chart 3: Scatter Plot of Signatures per Initiative (Bottom Right)
fig3 = px.scatter(
    df,
    x="registration_year",
    y="signatures_numeric",
    title="Signatures per Initiative by Year",
    color="primary_policy_area",
    hover_name="title",
    size="signatures_numeric",
    size_max=40,
)
fig3.update_layout(
    height=400,
    margin=dict(l=20, r=20, t=50, b=20),
    xaxis_title="Registration Year",
    yaxis_title="Total Signatures",
    xaxis=dict(
        dtick=1
    ),  # Forces the X-axis to only show whole years (e.g. 2024, not 2024.5)
)

# Export charts to HTML fragments (Plotly.js is loaded in the HTML header instead)
html_chart1 = fig1.to_html(full_html=False, include_plotlyjs=False)
html_chart2 = fig2.to_html(full_html=False, include_plotlyjs=False)
html_chart3 = fig3.to_html(full_html=False, include_plotlyjs=False)

# ----------------------------
# 3. Build Dashboard HTML
# ----------------------------
html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ECI Dashboard POC</title>
    <!-- Load Plotly.js once from CDN to power all 3 charts -->
    <script src="https://cdn.plot.ly/plotly-2.32.0.min.js"></script>
    <style>
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background-color: #f5f7f9; 
        }}
        h1 {{ 
            text-align: center; 
            color: #333; 
            margin-bottom: 30px;
        }}
        .dashboard-container {{ 
            max-width: 1200px; 
            margin: 0 auto; 
        }}
        .card {{ 
            background: white; 
            border-radius: 8px; 
            box-shadow: 0 4px 6px rgba(0,0,0,0.05); 
            padding: 15px; 
            margin-bottom: 20px; 
        }}
        .top-row {{ 
            display: flex; 
            flex-direction: column; 
        }}
        .bottom-row {{ 
            display: flex; 
            gap: 20px; 
        }}
        .bottom-col {{ 
            flex: 1; 
            min-width: 0; 
        }}
        /* Stack vertically on mobile devices */
        @media (max-width: 768px) {{
            .bottom-row {{
                flex-direction: column;
            }}
        }}
    </style>
</head>
<body>
    <div class="dashboard-container">
        <h1>EU Citizens' Initiatives Tracker</h1>
        
        <!-- Top Chart (Full Width) -->
        <div class="top-row">
            <div class="card">
                {html_chart1}
            </div>
        </div>
        
        <!-- Bottom Charts (Side by Side) -->
        <div class="bottom-row">
            <div class="card bottom-col">
                {html_chart2}
            </div>
            <div class="card bottom-col">
                {html_chart3}
            </div>
        </div>
    </div>
</body>
</html>
"""

# Write out the file
out_path = DOCS_DIR / "index.html"
out_path.write_text(html_template, encoding="utf-8")
print(f"✅ Dashboard successfully updated at: {out_path.absolute()}")
