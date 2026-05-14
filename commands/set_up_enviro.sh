#!/usr/bin/env bash
# set_up_enviro.sh
# Sets up virtual environments and installs dependencies for:
#   - data_pipeline  (Python 3.10+, uv-managed)
#   - page_creator   (Python 3.11+, uv-managed)
# Run from the project root.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

log()  { echo "[set_up_enviro] $*"; }
warn() { echo "[set_up_enviro] WARNING: $*" >&2; }
fail() { echo "[set_up_enviro] ERROR: $*" >&2; exit 1; }

# ---------------------------------------------------------------------------
# 1. Ensure uv is available
# ---------------------------------------------------------------------------
if ! command -v uv &>/dev/null; then

  log "uv not found — installing via official installer..."
  curl -LsSf https://astral.sh/uv/install.sh | sh || fail "Failed to install uv."

  # Reload PATH so the freshly installed uv is found in the same shell session
  export PATH="${HOME}/.cargo/bin:${HOME}/.local/bin:${PATH}"
fi

log "uv version: $(uv --version)"

# ---------------------------------------------------------------------------
# 2. data_pipeline environment
# ---------------------------------------------------------------------------

VENV_PIPELINE="${ROOT_DIR}/data_pipeline/.venv.data_pipeline"

log "--- data_pipeline ---"

if [ ! -d "${VENV_PIPELINE}" ]; then

  log "Creating venv at ${VENV_PIPELINE}..."
  uv venv "${VENV_PIPELINE}" || warn "venv creation failed — skipping data_pipeline setup."

else

  warn "Venv already exists at ${VENV_PIPELINE} — unexpected on a fresh runner, skipping creation."
fi

if [ -d "${VENV_PIPELINE}" ]; then

  log "Installing data_pipeline (editable)..."
  uv pip install --python "${VENV_PIPELINE}/bin/python" -e "${ROOT_DIR}/data_pipeline" \
    || fail "data_pipeline installation failed — aborting."
  log "data_pipeline environment ready."
fi

# ---------------------------------------------------------------------------
# 3. page_creator environment
# ---------------------------------------------------------------------------
VENV_PAGE="${ROOT_DIR}/page_creator/.venv.page_creator"

log "--- page_creator ---"

if [ ! -d "${VENV_PAGE}" ]; then
  log "Creating venv at ${VENV_PAGE}..."
  uv venv "${VENV_PAGE}" || warn "venv creation failed — skipping page_creator setup."
else
  warn "Venv already exists at ${VENV_PAGE} — unexpected on a fresh runner, skipping creation."
fi

if [ -d "${VENV_PAGE}" ]; then
  log "Installing page_creator (editable)..."
  uv pip install --python "${VENV_PAGE}/bin/python" -e "${ROOT_DIR}/page_creator" \
    || warn "page_creator installation encountered errors — continuing."
  log "page_creator environment ready."
fi

log "Environment setup complete."