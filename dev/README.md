# 1. Create the venv explicitly at a chosen path
cv dev
uv venv dev/.venv.dev --python 3.12

# 2. Activate it
source .venv.dev/bin/activate

# 3. Install deps into that venv
uv pip install -e ".[dev]"

# 4. Install test dependencies
uv pip install -e ".[test]"

# 5. Regenerate the lock file
uv lock

# 6. Sync the environment from the lock file (installs/removes to match exactly)
uv sync --extra dev --extra test