Write a Python script for a data pipeline step that fulfills the following requirements. Create ONLY a skeleton of the application; DO NOT write the extensive spaCy rule implementation.

1. Locate the latest data directory.
2. Find the most recent `eci_responses_*.csv` and `eci_responses_followup_*.csv` files within it.
3. Load these CSV files into memory using csv standard library.
4. Extract structured data into memory using `spaCy` (with the `en_core_web_sm` model and `Matcher`)
5. Utilize the `data_pipeline/pipeline_shared` where applicable.

Format the output into a new CSV named following the pattern `eci_legislation_YYYY-MM-DD_HH-MM-SS.csv`. The target CSV must contain exactly these columns:
- `registration_number`: The unique identifier from the source files.
- `Law_Passed`: A list of strings containing the exact text spans matched by the spaCy `LAW_MENTIONED` rules (evaluating lemmas like "apply", "adopt", or "force" in proximity to legislative terms). This must be computed by combining the text from the `commission_answer_text` and `followup_events` columns.
- `Is_Law_Passed`: A boolean (True/False) that is True if the `Law_Passed` list is not empty.
- `Rejected_Legislation`: A boolean (True/False) that is True if the combined text of `commission_answer_text` and `followup_events` triggers any of the spaCy `REJECTED_LEGISLATION` patterns (e.g., direct rejection, refusal to repeal, withdrawal, or outside competence).

Finally, provide the necessary snippet to update the dependencies in `data_pipeline/pyproject.toml` to include the latest explicit version of `spaCy`.