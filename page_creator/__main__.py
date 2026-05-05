import sys
from pathlib import Path

# Ensure the project root is on sys.path regardless of the working directory
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd

from page_creator.data_loader import find_latest_csv
from page_creator.generate_charts import (
    discover_slot_map,
    generate_partials_map,
    build_generated_js,
)
from page_creator.paths import OUT_DIR, GENERATED_JS
from page_creator.partials.date_stamp.last_data_update import generate_last_data_update


def main() -> None:
    """Load the CSV, render all partials, and write HTML files and the JS slot map."""
    csv_path, data_date = find_latest_csv()
    df = pd.read_csv(csv_path)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    GENERATED_JS.parent.mkdir(parents=True, exist_ok=True)

    slot_map = discover_slot_map()
    partials: dict[str, str] = generate_partials_map(df)
    partials["last_data_update.html"] = generate_last_data_update(data_date)

    for filename, html in partials.items():
        path = OUT_DIR / filename
        path.write_text(html, encoding="utf-8")
        print(f"  wrote {path}  ({path.stat().st_size:,} bytes)")

    GENERATED_JS.write_text(build_generated_js(slot_map), encoding="utf-8")
    print(f"  wrote {GENERATED_JS}  ({GENERATED_JS.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
