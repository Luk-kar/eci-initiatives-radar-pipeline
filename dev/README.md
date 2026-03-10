# 1. Create the venv explicitly at a chosen path
uv venv dev/.venv.dev --python 3.12

# 2. Activate it
source dev/.venv.dev/bin/activate

# 3. Install deps into that venv
uv pip install -e ".[dev]"
