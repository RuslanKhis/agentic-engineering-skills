# Booking agent

An ADK 2.12 agent that books, moves and cancels appointments at Harbour Physio clinics.

- `booking_agent/agent.py` builds the agent; `booking_agent/tools.py` are its tools over
  `booking_agent/backend.py` (an in-memory backend; production swaps in the clinic API client).
- `eval_cases/booking.evalset.json`: 40 cases with reference tool trajectories;
  `eval_cases/test_config.json` sets the criteria.
- `tests/test_tools.py` tests the tools offline; `tests/test_evalset.py` runs the evalset with
  `AgentEvaluator` (needs google-adk and model access; skips otherwise).
- Nightly CI: `.github/workflows/nightly-eval.yml`; reports under `reports/`.

google-adk is not installed in this environment and there is no model access.
