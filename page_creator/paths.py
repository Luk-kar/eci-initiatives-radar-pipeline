from pathlib import Path

PARTIALS_DIR = Path(__file__).parent / "partials"
OUT_DIR = Path(__file__).parent.parent / "page_to_export" / "partials"
GENERATED_JS = (
    Path(__file__).parent.parent
    / "page_to_export"
    / "script"
    / "elements"
    / "generated.js"
)
