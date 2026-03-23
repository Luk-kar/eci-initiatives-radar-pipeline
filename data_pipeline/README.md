# 1. Create a venv in data_pipeline/ (from root)
uv venv data_pipeline/.venv.data_pipeline

# 2. Activate it (still from root)
source data_pipeline/.venv.data_pipeline/bin/activate

# 3. Install the project in editable mode, pointing at the subdir
uv pip install -e data_pipeline

# 4
eci-scrape-initiatives
# or
python -m data_pipeline.scraper.initiatives
python -m data_pipeline.extractor.initiatives

# 5. For tests:
uv pip install -e data_pipeline[dev]
python -m pytest data_pipeline
======================