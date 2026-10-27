# Working on this repository

- Python 3.12; dependencies are pinned in `pyproject.toml`; install with
  `pip install -e .` in a virtual environment. Do not upgrade pins in a
  feature change.
- Tests: `python -m unittest discover -s tests -t .` (standard library
  unittest; no pytest). `tests/runner/` holds scripted-model Runner tests; they
  need google-adk and are skipped where it is not installed.
- Keep `google.adk` imports out of `app/__init__.py`, `app/tools/` and
  `app/clients/` so the unit tests run without the SDK.
- The user ID always comes from the verified principal (`app/auth.py`),
  never from the request body or the model.
- Money is integer cents.
- Never call the real payments or mail providers from tests; use
  `tests/fakes.py`.

## Personal data and credentials

- Production screens customer input with Model Armor and de-identifies
  replies and logs with Sensitive Data Protection (`app/screening.py`). CI has
  no Google Cloud credentials, so those calls are replaced by fakes in tests.
- Test data is synthetic only; the canaries in `tests/runner/canaries.py` are
  the values the Runner tests look for in every sink.
- Credential formats we issue or hold: payments provider keys `hpk_live_` or
  `hpk_test_` followed by 32 hex characters; mail relay tokens `hmr-` followed by
  a UUID; IAP-signed JWTs. None may appear in logs, prompts or session state.
