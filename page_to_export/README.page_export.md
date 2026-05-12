# 🌐 Page Export

The final presentation layer of the European Citizens’ Initiative (ECI) Dashboard. This module acts as the public-facing static web directory, combining the base HTML structure, static assets, and the dynamically generated partials (charts, tables, and counters) produced by the `page_creator`.

## Overview

The `page_to_export` directory contains the complete dashboard UI ready to be served. It integrates Plotly visualizations, responsive CSS, and dynamic partial loading via JavaScript.

It includes:

- **Base Layout (`index.html`)**: The main container defining the layout grid and placeholder slots for dynamic content.
- **Generated Content**: The output location for the `page_creator` artifacts, including rendered HTML partials and auto-generated JavaScript element maps.
- **Static Assets**: Contains standard structural parts like headers, footers, styling (`styles.css`), images, and core vanilla JavaScript logic.
- **Client-side Logic**: Custom scripts for injecting partials into the DOM, handling scroll-to-top functionality, anchoring, and computing dynamic countdowns for ongoing initiatives.

## Project structure

```text
page_to_export/
│
├── README.page_export.md <-- This doc
├── index.html              # Main HTML skeleton with target slots
│
├── generated/              # Output directory populated by page_creator
│   ├── partials/           # Rendered Plotly charts and data lists (.html)
│   └── script/
│       └── elements/
│           └── generated.js # Auto-generated array of generated partial maps
│
└── static/                 # Version-controlled frontend assets
    ├── images/             # Banners and icons
    ├── partials/           # Static HTML fragments (header, footer)
    ├── script/             # Core JS utilities
    │   ├── back_to_top.js  # Floating back-to-top button logic
    │   ├── left_days.js    # Client-side days-left calculation
    │   ├── move_to_section.js # Smooth scrolling anchors
    │   ├── partials.js     # Async loader for generated and static partials
    │   └── elements/
    │       └── static.js   # Array map of static partials
    └── styles/
        └── base.css        # Dashboard responsive styling
```

## Running locally

Because this dashboard uses JavaScript to dynamically fetch and assemble its components, it will not load correctly if you simply double-click the `index.html` file. 

It must be served through a local development server. You can use any standard server tool of your choice:

**Using VS Code (Recommended):**
If you use Visual Studio Code, you can simply use the **Live Server** extension. Right-click `index.html` and select **"Open with Live Server"**.

**Using Python (Terminal):**
Alternatively, you can use Python's built-in server. Run the following commands in your terminal:
```bash
# Navigate to the export directory
cd page_to_export

# Start a local web server on port 8000
python3 -m http.server 8000
```

Then open your browser and navigate to:
[http://localhost:8000](http://localhost:8000)