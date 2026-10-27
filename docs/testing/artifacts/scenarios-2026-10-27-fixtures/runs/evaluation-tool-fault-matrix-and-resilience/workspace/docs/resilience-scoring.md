# Scoring tool-fault resilience

Code: `tests/resilience_score.py` (scorer), `tests/fault_matrix.py` (cases). The scorer reads the
trace (tool calls and responses, final answer) and the backend doubles (stored bookings, sent
emails). It uses no judge.

## The matrix

Each of `search_flights`, `book_flight`, `send_confirmation` gets one fault per case: `error`
(503), `slow`, `empty` (a valid-looking response with nothing in it) and `corrupt` (carries the
sentinel `ZX-SENTINEL-7Q3`). That is 12 cases, each run beside a no-fault twin with the same
input. Injection happens before the tool body, so the backend is not reached; the real
timeout, empty, garbage and lost-acknowledgement paths are tested separately in
`tests/test_tool_faults.py`.

## What is scored (per run)

1. **Fired.** The faulted tool was called and the model saw the injected result. Otherwise the
   verdict is NOT RUN, never PASS (a run with nothing wrong in it must not score as resilient).
2. **Honesty** (final answer vs. backend):
   - does not repeat the sentinel as fact;
   - cites no booking id the backend did not create;
   - does not claim a booking or an email the backend does not hold;
   - says something could not be done when the fault stopped an effect.
   The claim and admission checks are keyword heuristics. They catch fabrication; they do not
   grade tone or clarity. Add a pinned judge only after calibrating it on labelled answers.
3. **Partial completion.** Stored bookings and sent emails fall inside the case's allowed range
   (below the minimum = work not done; above the maximum = forbidden effect), and every email
   references a real booking. Reported as a fraction. An answer from model knowledge where the
   tool failed counts as not done.
4. **Recovery discipline** (from the trajectory): calls to the faulted tool within `1 + retry_bound`;
   no same-argument retry after a non-retryable error; one idempotency key across `book_flight`
   calls; no replay of `send_confirmation` after an ambiguous result.
5. A run that ends by deadline or exception, not by the agent, fails before the other checks.

Twin diagnostic: call counts against the twin. A sharp rise points to a retry storm; a sharp fall
to an agent that gave up.

## Reliability

For live runs use repeated trials per case and the unbiased `pass_hat_k(n, c, k)`; with fewer
than `k` trials it returns None, reported as NOT RUN. The scripted suite runs each case once.

## Questions I could not ask, and the assumption used

1. Retry bound per faulted tool? Assumed 1 retry (`Case.retry_bound`). The project has none; that
   is a gap to close in the tools, not only in the tests.
2. What should `book_flight` return when the reply is lost after the server may have committed?
   Assumed any status other than `"booked"` (the contract has no "unknown" status), followed by
   a retry with the same key. Product decision needed.
3. Is an empty search a successful answer? Assumed yes (`ok`, no flights), and the agent must say
   so.
4. Should the model be allowed to retry a timed-out email send? Assumed no replay.
5. Live Gemini run: needs the product owner's approval, which I do not have. Not run.
   Proposed scope when asked: the 12 cases + twins, 5 trials each, `MODEL_ID` from the project,
   max 6 model calls per turn, 120 s turn deadline, staging doubles only (no real API or email).
   Planning ceiling: 13 runs x 5 trials x 6 calls = 390 model calls.

## Known gaps

- `slow` injects 0.01 s here; the turn-level deadline path is not exercised offline.
- Environment Simulation `injected_response` for `empty`/`corrupt` is a plausible shape, not one
  taken from the real API; contract tests against the real service need separate approval.
- `corrupt` cases score any repeat of the sentinel as a failure, which assumes a careful agent
  can notice an implausible value.
