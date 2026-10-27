# Support assistant

Harbour Outfitters' support agent on Google ADK 2.12.0. Staff hand it ticket IDs; it reads the
ticket (`read_ticket`), refunds the order (`issue_refund`, which asks for confirmation) and
replies to the customer (`send_email`).

## Tests and CI

- `python -m unittest discover -s tests -t .` runs the unit tests and the scripted-model Runner
  tests (`tests/runner_harness.py`, `tests/test_runner_tickets.py`). google-adk is not installed
  in this environment, so the Runner tests skip here; CI installs the pins.
- `.github/workflows/ci.yml` runs on every pull request. CI has no OpenAI or NVIDIA NIM keys.
- `.github/workflows/live-eval.yml` is the approved live run: Gemini on Vertex AI through
  Workload Identity Federation, started by hand.
