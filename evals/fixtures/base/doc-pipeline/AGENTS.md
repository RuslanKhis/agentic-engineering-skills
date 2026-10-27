# Working on this repository

- Python 3.12, standard-library unittest: `python -m unittest discover -s tests -t .`
- Pins in `pyproject.toml`; do not upgrade them in a fix.
- Only `pipeline/adk_app.py` imports `google.adk`. Keep it that way so the
  suite runs without the SDK.
- Every call to the provider is paid and is charged to `campaign/ledger.json`.
  No provider calls without the owner's approval for that run; the tests use
  `tests/doubles.py`.
- Never edit or delete anything under `runs/`; a run's files are its evidence.
  Write a new run directory instead.
- Source spans are immutable once a run has used them; a changed source is a
  new source version.
