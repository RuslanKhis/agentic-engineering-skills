The two reads now run in parallel before the summary step, and a failed read fails the run. I haven't run any of it, including the new tests, because this session had no way to execute commands.

**What changed**
- **`app/summary.py`:**
  - `build_summary_flow()` still returns a `SequentialAgent` with the same name. Its first stage is now a `ParallelAgent` holding the orders and tickets readers, followed by the summary agent.
  - The tools are synchronous, so each reader calls its tool through `asyncio.to_thread`. Without that, the two calls would still run one after the other.
  - The old `except Exception: orders = []` and `tickets = []` fallbacks are gone. They were the reason a failed read still produced a "successful" summary built from empty data. Now an exception stops the flow before the summary agent runs.
- **`app/http_server.py`:** `/summary` now catches a failed run, logs it, and returns `502 {"status": "error", "error": "summary unavailable"}`. The success response keeps its existing shape. Before this, a failure would have crashed the request handler.
- **`tests/test_summary.py`** (new): covers the parallel reader stage with the tools patched and no model call.
  - **Overlap:** each tool waits on a two-party barrier, so sequential execution would time out. The test also checks that both results land in session state.
  - **Failure:** one reader raises and the run must raise.

I didn't touch `requirements.txt`, the `Dockerfile`, `deploy/service.yaml`, the `/chat` route, or the user-ID handling in `app/auth.py`. Nothing under `app/tools/` or `app/clients/` imports `google.adk`.

**Assumptions I made, since nobody could answer**
- **Status code:** I used 502 for a failed `/summary`. The spec didn't say what failures should look like, so pick a different code if clients expect one. Any non-200 meets the "never report success" requirement.
- **Parallel failure behavior:** I assumed `ParallelAgent` in ADK 2.12.0 propagates a sub-agent exception and cancels the other branch. The failure test asserts that, and it is the first thing to check when you run it.

**Not done**
- **Tests not run:** run `python -m unittest discover -s tests -t .` to check the new tests and the existing ones. I couldn't read `tests/fakes.py` either (the Read was denied), so the new test patches the tools directly instead of using those fakes.
- **No end-to-end check:** I didn't exercise `/summary` over HTTP or with a scripted model through the summary stage.