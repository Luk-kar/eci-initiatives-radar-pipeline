#!/usr/bin/env bash
# run_pipeline.sh
# Runs the full ECI data pipeline followed by the page_creator.
#
# Pipeline stages (data_pipeline):
#   1. scraper.initiatives
#   2. extractor.initiatives
#   3. scraper.responses
#   4. extractor.responses
#   5. scraper.responses_followup
#   6. extractor.responses_followup
#   7. merger_csv.responses_followup_legislation
#   8. merger_csv.dashboard_csv
#
# Page generation (page_creator):
#   9. page_creator  (generates HTML partials + generated.js into page_to_export/)
#
# Any step failure is critical — the script aborts immediately.
# Run from the project root.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

VENV_PIPELINE="${ROOT_DIR}/data_pipeline/.venv.data_pipeline"
VENV_PAGE="${ROOT_DIR}/page_creator/.venv.page_creator"

PYTHON_PIPELINE="${VENV_PIPELINE}/bin/python3"
PYTHON_PAGE="${VENV_PAGE}/bin/python3"

log()  { echo "[run_pipeline] $*"; }
fail() { echo "[run_pipeline] ERROR: $*" >&2; exit 1; }

[ -x "${PYTHON_PIPELINE}" ] || fail "Python not found at '${PYTHON_PIPELINE}'. Has set_up_enviro.sh been run?"
[ -x "${PYTHON_PAGE}" ]     || fail "Python not found at '${PYTHON_PAGE}'. Has set_up_enviro.sh been run?"

# ---------------------------------------------------------------------------
# data_pipeline stages
# ---------------------------------------------------------------------------
log "1/9 scraper.initiatives"
"${PYTHON_PIPELINE}" -m data_pipeline.scraper.initiatives

log "2/9 extractor.initiatives"
"${PYTHON_PIPELINE}" -m data_pipeline.extractor.initiatives

log "3/9 scraper.responses"
"${PYTHON_PIPELINE}" -m data_pipeline.scraper.responses

log "4/9 extractor.responses"
"${PYTHON_PIPELINE}" -m data_pipeline.extractor.responses

log "5/9 scraper.responses_followup"
"${PYTHON_PIPELINE}" -m data_pipeline.scraper.responses_followup

log "6/9 extractor.responses_followup"
"${PYTHON_PIPELINE}" -m data_pipeline.extractor.responses_followup

log "7/9 merger_csv.responses_followup_legislation"
"${PYTHON_PIPELINE}" -m data_pipeline.merger_csv.responses_followup_legislation

log "8/9 merger_csv.dashboard_csv"
"${PYTHON_PIPELINE}" -m data_pipeline.merger_csv.dashboard_csv

# ---------------------------------------------------------------------------
# page_creator
# ---------------------------------------------------------------------------
log "9/9 page_creator"
"${PYTHON_PAGE}" -m page_creator

log "All steps completed successfully."