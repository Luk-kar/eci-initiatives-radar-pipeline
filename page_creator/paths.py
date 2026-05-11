from pathlib import Path

PARTIALS_DIR = Path(__file__).parent / "partials"
OUT_DIR = Path(__file__).parent.parent / "page_to_export" / "generated" / "partials"

GENERATED_JS = (
    Path(__file__).parent.parent
    / "page_to_export"
    / "generated"
    / "script"
    / "elements"
    / "generated.js"
)
