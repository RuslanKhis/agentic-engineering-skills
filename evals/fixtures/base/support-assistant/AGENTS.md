# Working on this repository

- Python 3.12; dependencies are pinned in `pyproject.toml`; install with
  `pip install -e .` in a virtual environment. Do not upgrade pins in a
  feature change.
- Tests: `python -m unittest discover -s tests -t .` (standard library
  unittest; no pytest).
- Keep `google.adk` imports out of `app/__init__.py`, `app/tools/` and
  `app/clients/` so the unit tests run without the SDK.
- The user ID always comes from the verified principal (`app/auth.py`),
  never from the request body or the model.
- Money is integer cents.
- Never call the real payments or mail providers from tests; use
  `tests/fakes.py`.
