# Static Analysis Development Environment

A standalone virtual environment dedicated entirely to static code analysis and formatting tools. 

**Design Intent:**
These tools are explicitly separated from the main Python application code libraries and runtime/testing environments. By isolating static analysis tools (like `pylint`), we avoid dependency resolution issues and library conflicts that can occur when linters require specific package versions that clash with the data pipeline's actual requirements.

## Setup Instructions

# 1. Create the venv explicitly at a chosen path
uv venv dev/.venv.dev --python 3.12

# 2. Activate it
source dev/.venv.dev/bin/activate

# 3. Change into the dev/ directory to install the static analysis deps
cd dev
uv pip install -e ".[dev]"

# 4. Regenerate the lock file
uv lock

# 5. Sync the environment from the lock file
uv sync --extra dev

# 6. Return to the project root
cd ..