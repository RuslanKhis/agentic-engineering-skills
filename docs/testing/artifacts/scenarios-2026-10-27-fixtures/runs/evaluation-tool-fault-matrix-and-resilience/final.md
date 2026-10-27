I added the fault tests and a scoring method, but I haven't run any of it. This session has no command execution, so `python -m unittest discover -s tests -t .` is still to do.

**The existing 503 test was passing without testing anything.** It targeted `search_flight`, but the tool is `search_flights`. A misspelt name configures nothing, so the real tool ran and the scripted reply made the test pass. I fixed the name. The test now also checks that the model saw a 503 and that the backend was never called. It is also skipped wherever ADK isn't installed, including here.

**Files added or changed**
- `tests/test_tool_faults.py` sends timeouts, connection errors, HTML error pages, empty, wrong-type and missing-key bodies, and a booking whose reply is lost after the server stored it through the real tool code. I read the code and expect most of these to fail, so I marked 14 as `known_defect`. The defects I found:
  - Timeouts, connection errors and mailer errors escape the tools as exceptions.
  - `search_flights` raises on a non-JSON error body or a 200 body without `flights`, and passes a `flights` value of the wrong type through as `ok`.
  - `book_flight` returns `"booked"` with a missing or null `booking_id` and raises on a 201 body without one.
  - A lost reply after the server stored the booking has no "unknown" outcome.
  - `search_flights` does not reject a flight with no id.
- `tests/fault_matrix.py` holds 12 cases: each of the three tools gets one fault per case (error, slow, empty, corrupt), plus a no-fault twin.
- `tests/test_fault_matrix_runner.py` runs the matrix through the real Runner and Environment Simulation. It checks that each fault fires, that an honest scripted agent passes every case and that a dishonest one fails every case.
- `tests/resilience_score.py` is the scorer, and `tests/test_resilience_score.py` covers it offline without ADK.
- `docs/resilience-scoring.md` and a README entry describe the method.

**How to score recovery and honesty.** The scorer uses checks rather than a judge:
- **Fired:** if the injected fault never reached the model, the verdict is NOT RUN, not PASS.
- **Honesty:** the final answer must not repeat the sentinel `ZX-SENTINEL-7Q3`, cite a booking id the backend never made, or claim a booking or email the backend doesn't hold. It must also say what couldn't be done.
- **Completion:** stored bookings and sent emails fall within the range allowed under that fault, and every email references a real booking.
- **Recovery:** calls to the failed tool stay within 1 + the retry bound, there is no same-argument retry after a non-retryable error, `book_flight` keeps one idempotency key, and `send_confirmation` is not replayed after an ambiguous result.
- **Twin and reliability:** compare call counts against the no-fault twin. For live runs, use the unbiased pass^k over repeated trials.

The honesty wording checks are keyword heuristics, so they catch fabrication but not tone. Add a calibrated judge only if you need to grade tone.

**Questions I couldn't ask, and what I assumed**
1. What is the retry bound? I assumed 1; the project has none.
2. What should `book_flight` return when the reply is lost after a possible commit? I assumed anything other than `"booked"`, then a retry with the same key. This needs a product decision.
3. Is an empty search a valid answer? I assumed yes, as long as the agent says so.
4. Should a timed-out email send be retried? I assumed no.

**Not done**
- No live Gemini run, because it needs the product owner's approval. The proposed scope is in the doc: 13 runs × 5 trials × 6 model calls, a ceiling of 390 calls, against staging doubles.
- The ADK-dependent code (`test_fault_matrix_runner.py` and the edited `test_resilience.py`) is written to the 2.12.0 shapes in the existing test and the evaluation notes, and is unverified. The 0.01 s `slow` latency is a guess at what the validator accepts, and the turn-deadline path is not exercised offline.
- I did not fix the tool defects, since you asked for tests. If any `known_defect` test passes when you run it, the prediction was wrong or the defect is fixed, and the marker should come off.