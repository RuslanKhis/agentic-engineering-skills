I resumed G02 (streamed replies) and wrote the A2 and A3 code and tests, but I couldn't run any of it. Bash is disabled in this session, so nothing has been executed and the G02 re-verify command was not run.

**Why G02, not G03:** G01 is `verified_local`, and G02 is the first goal in the plan whose prerequisites are done. G03 is also ready and its touched paths don't overlap with G02's, so it can run in parallel. I left it for another session.

**What I did (in `wt-G02/`, uncommitted):**
- **`app/stream.py`, A2:** `relay` now emits only `failed` after the runner raises, with no `completed` following. Before, `completed` always followed.
- **`app/stream.py`, A3:** on cancel or close, `relay` closes the event source to stop the run and records `interrupted`. No frame is sent because the client is gone.
- **Recording:** `relay` takes an optional `record` callback. The route passes one that logs the state.
- **`tests/test_stream.py`:** added `test_failed_after_partial_text_has_no_completed` and `test_disconnect_stops_run_and_records_interrupted`.
- **`docs/tickets/support/G02.md`:** updated the Progress block and left the status `in_progress`.

**Test status:** A1 still shows as done from the earlier session. The A2 and A3 tests are **not run**, so those boxes stay unticked.

**Assumptions** (nobody was available to ask):
- Recording `interrupted` only logs for now, because there is no store table for stream states.
- The disconnect path in the real route assumes Starlette cancels the response task, which I couldn't check without FastAPI.

**Left undone:**
- Run `python -m unittest tests.test_stream` in `wt-G02/`, then the full suite from the main checkout.
- Mount `make_route` in `app/server.py`.
- Add the fetch reader in `web/src/chat/`.
- Tick A2 and A3 in the ticket and write the final Evidence, including the C3 contract line.
- I estimate about 1–1.5 human hours to run the tests, mount the route and build and check the web reader.

**Next prompt:** `/adk-engineer Resume docs/tickets/support/G02.md from its Progress block.`