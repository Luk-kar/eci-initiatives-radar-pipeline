#!/usr/bin/env bash
# give_path_latest_data.sh
# Resolves and prints the absolute path to the latest pipeline run directory
# produced by the data_pipeline. Intended to be called from GitHub Actions to
# locate the artefacts that should be copied/uploaded as workflow artefacts.
#
# Usage (standalone):
#   bash commands/give_path_latest_data.sh
#
# Usage (capture in a workflow step):
#   LATEST_DIR=$(bash commands/give_path_latest_data.sh)
#   echo "latest_dir=${LATEST_DIR}" >> "$GITHUB_OUTPUT"
#
# Search strategy:
#   The data_pipeline stores run outputs under:
#     data_pipeline/data/<run_timestamp>/eci_dashboard_<timestamp>.csv
#   The script finds the most recently modified eci_dashboard_*.csv and
#   returns its parent directory (the run folder).
#
# Exit codes:
#   0  Directory path printed to stdout.
#   1  No CSV found, or CSV has too few rows (header + at least 2 data rows required).
#
# Run from the project root.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

DATA_DIR="${ROOT_DIR}/data_pipeline/data"

fail() { echo "[give_path_latest_data] ERROR: $*" >&2; exit 1; }

[ -d "${DATA_DIR}" ] || fail "Data directory not found: ${DATA_DIR}"

LATEST_CSV=$(
  find "${DATA_DIR}" -name "eci_dashboard_*.csv" \
    -printf "%T@ %p\n" 2>/dev/null \
  | sort -n \
  | tail -1 \
  | awk '{print $2}'
)

[ -n "${LATEST_CSV}" ] || fail "No eci_dashboard_*.csv found under ${DATA_DIR}. Run the pipeline first."

ROW_COUNT=$(wc -l < "${LATEST_CSV}")
[ "${ROW_COUNT}" -gt 2 ] || fail "CSV appears empty or near-empty: '${LATEST_CSV}' has only ${ROW_COUNT} line(s) (header + at least 2 data rows required)."

echo "$(dirname "${LATEST_CSV}")"