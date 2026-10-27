# Support assistant

Harbour Outfitters' support agent on Google ADK 2.12.0. Staff hand it ticket IDs; it reads the
ticket (`read_ticket`), refunds the order (`issue_refund`, which asks for confirmation) and
replies to the customer (`send_email`).

## Tests and CI

- `python -m unittest discover -s tests -t .` runs the unit tests and the scripted-model Runner
  tests (`tests/runner_harness.py`, `tests/test_runner_tickets.py`). google-adk is not installed
  in this environment, so the Runner tests skip here; CI installs the pins.
- `.github/workflows/ci.yml` runs on every pull request. CI has no OpenAI or NVIDIA NIM keys.
- `.github/workflows/redteam.yml` is the approved garak run against the agent itself (hand-started,
  same `live-eval` environment). `redteam/garak_target.py` wraps the Runner and records executed effects
  in a sidecar; `redteam/check_garak.py` fails the job on any finding, missing report row or attempt
  count mismatch. garak's own exit code is ignored. The gate's logic is unit-tested in
  `tests/test_redteam_gate.py` and runs in `ci.yml` with no model.
- `.github/workflows/live-eval.yml` is the approved live run: Gemini on Vertex AI through
  Workload Identity Federation, started by hand.
