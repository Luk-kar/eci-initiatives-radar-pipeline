#!/usr/bin/env bash

# -----------------------------------------------------------------------------
# Script Name: read_files_and_content.sh

# Description:
# This script collects all files under a specified input directory (excluding
# any `.git` folders and their contents) and concatenates them, in
# deterministic sorted order, into a single output file.

# Usage:
#   ./read_files_and_content.sh <input_directory> <output_file>
#
# Arguments:
# Path to the directory to search files in.
# Path to the file where concatenated content is written.

# Example:
# ./read_files_and_content.sh "./page_creator" "page_creator.md"

# Notes:
# - Overwrites if it already exists.
# - Ensures deterministic order by sorting file paths.
# - Skips `.git` directories and everything inside them.
# -----------------------------------------------------------------------------

set -euo pipefail
IFS=$'\n\t'

# Usage check
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <input_dir> <output_file>"
  exit 1
fi

INPUT_DIR=$1
OUTPUT_FILE=$2

find "$INPUT_DIR" \
  -type d \( -name .git -o -name __pycache__ -o -name dbt -o -name .venv \) -prune -o \
  -type f ! -name "*.csv" -print | sort | while read -r FILE; do
  echo "\`$FILE\`:"
  echo '```'
  cat "$FILE"
  echo
  echo '```'
  echo
done > "$OUTPUT_FILE"