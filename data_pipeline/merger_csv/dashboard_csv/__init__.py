"""
ECI Dashboard CSV Merger
========================
Merges the three upstream CSVs

* ``eci_initiatives_*.csv``
* ``eci_responses_*.csv``                       (only ``commission_answer_text``)
* ``eci_responses_followup_legislation_*.csv``  (without ``commission_answer_text``)

…into a single dashboard-ready ``eci_dashboard_*.csv`` whose schema matches
the historical ``initiatives_<timestamp>.csv`` reference file (the csv created for the dashboard to clarify requirements for the dashboard).
"""
