#!/usr/bin/env bash
# run_page_creator.sh
# Runs only the page_creator stage (9/9).
#
# Why as separate script:
# # Separated from the data_pipeline stages so it is excluded from retry logic —
# its output is deterministic given valid pipeline data and retrying it would be wasteful.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
VENV_PAGE="${ROOT_DIR}/page_creator/.venv.page_creator"
PYTHON_PAGE="${VENV_PAGE}/bin/python3"

log()  { echo "[run_page_creator] $*"; }
fail() { echo "[run_page_creator] ERROR: $*" >&2; exit 1; }

[ -x "${PYTHON_PAGE}" ] || fail "Python not found at '${PYTHON_PAGE}'."

log "9/9 page_creator"
"${PYTHON_PAGE}" -m page_creator

log "Page creator completed successfully."