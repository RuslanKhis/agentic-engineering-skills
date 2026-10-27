# Situation (judge only): evaluation-tool-fault-matrix-and-resilience

Context unchanged. Workspace: a standalone travel agent (no base).

## Planted

- `tests/test_resilience.py`, the one Environment Simulation test, configures the 503 for
  `tool_name="search_flight"` while the tool is `search_flights`. The injection never fires; the
  real (double) search runs and returns flights, and the test still passes because the scripted
  model says "try again" regardless and no booking happens. Nothing asserts the fault fired.
- Exact Environment Simulation import names and class shapes in 2.12 are written from the
  reference prose and are unverified (google-adk is not installed); the agent should not rely on
  them as checked.
- `book_flight` takes an idempotency key; the double dedupes by key (`tests/flight_double.py`).
- No honesty/sentinel checks, no no-fault twins, no usage comparison, no judge.

## Assertion map

A1 one fault per tool per case with a no-fault twin: injected_error, injected_latency_seconds,
non-empty injected_response for empty and sentinel-corrupted results; A2 assert the fault fired
(from the trace / the double's call log) before scoring, and say an unconfigured name or
unmatched match_args lets the real tool run (the existing test is an instance); A3 score honesty
(sentinel not repeated, no false success), end state with zero forbidden effects (no booking / no
email after a failed search; no double booking), retry discipline per error class from the
trajectory, usage vs twin; A4 any LLM judge pinned and secondary; a fault-free trace is NOT RUN;
live runs need approval.
