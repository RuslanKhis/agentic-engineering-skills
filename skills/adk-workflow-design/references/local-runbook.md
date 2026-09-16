# Local execution, streaming and cleanup runbook

Read for an actual CLI/HTTP/browser path, startup failure, apparent buffering,
latency review or retained local sessions. These recipes derive from ADK 2.8.0
reader tests and the historical local-UI campaign. Adapt paths and contracts to
the target; they do not deploy a cloud application or authorise model traffic.

## Establish a reproducible local baseline

1. Locate the app discovery directory, exported root, documented launch command,
   model/backend configuration and session/artefact service. Check declared and
   installed versions separately. Use the existing interpreter for a repair;
   for a fresh-reader claim, also use a clean source copy and fresh environment
   installed from the declared requirements/lock. Never quietly borrow undeclared
   packages or copy the developer's `.env`, `.adk`, virtual environment or caches.
2. In an offline child process, pass an allowlisted environment and disable
   dotenv loading (`PYTHON_DOTENV_DISABLED=1` in the checked path). Isolate ADC and
   CLI configuration and exclude ambient keys, proxies and cloud tracing. A fake
   key alone is not network isolation. Runner-only tests can block sockets/DNS;
   real HTTP tests need loopback access and a no-provider fixture or provider
   egress denial. Inspect commands before running them: importing a root may have
   side effects even when the test itself looks harmless.
3. Keep frontend install/build as a separate applicable gate. Bundled ADK Web
   needs no application `npm` build; a custom frontend does. Import/compile checks
   establish loading only. Submit synthetic input through the actual route and
   assert the designated output, state and error behaviour.

For the checked SDK, the CLI can be launched with the selected interpreter using
`python -m google.adk.cli web AGENTS_DIR --host 127.0.0.1 --port PORT`.
Replace `AGENTS_DIR` and `PORT` with discovered paths and an available loopback
port; check that release's `--help` before adapting flags. A subprocess harness
uses `sys.executable` and an argument list to keep interpreter selection exact.
For managed inference, finish [external preflight](external-validation.md) and
obtain the bounded-call approval before submitting a model-backed app.

## Own the process, not every listener on the port

- Record the exact child process handle/PID, start time, working directory, port
  and private log path. Register cleanup before starting it. Preserve an existing
  listener and select another port; never kill by port/name to make a test pass.
- Poll a cheap readiness route with an overall deadline and short request
  timeouts, while checking whether the child exited. `/list-apps` was the tested
  ADK Web route. Readiness is not proof of credentials or meaningful output.
  Ephemeral-port selection can race with another binder; report a collision and
  restart only the owned attempt within a declared bound.
- On startup failure or interruption, terminate the owned child, wait, then kill
  that child only if the wait expires. Close log handles and the owned temporary
  copy. Repeat cleanup and check process exit and port closure. Avoid PID reuse
  mistakes when restoring cleanup from a saved record.
- Register a guarded model/client in a fresh process before agent import when
  changing SDK construction. Cached agents may still hold the earlier client.
  [Model-call controls](model-call-controls.md) covers lifespan/client ownership.

## Verify the real HTTP and persistence contract

ADK 2.8.0's tested routes were `/apps/{app}/users/{user}/sessions`,
`/apps/{app}/users/{user}/sessions/{session}`, `/run` and `/run_sse`.
Inspect the installed server/OpenAPI contract before using another version.
Create a synthetic session, preserve its returned ID and submit that same tuple.
The checked request uses `appName`, `userId`, `sessionId`, and a `newMessage`
with `role: "user"` and `parts: [{"text": "..."}]`. Streaming configuration must
match the selected route/SDK; an SSE response type alone proves no partial text.

Assert named state/node values as described in [runtime.md](runtime.md), rather
than only status 200. Exercise unknown sessions and invalid requests; record the
actual status/schema (404 and 422 in the historical local suite). Failure must
remain visible and the UI should become usable again without automatically
resubmitting a potentially billable or side-effecting operation.

To claim persistence, populate the session, snapshot relevant events/state,
stop the actual server process, start a new one against the same store, reread,
then submit a continuation. Keep the database path fixed across that restart.
That proves completed-history persistence, not interrupted-workflow recovery.
Two user IDs in this unauthenticated UI only demonstrate storage partitioning.

## Prove streaming causally before measuring speed

A completed SSE response containing several chunks can still have been buffered.
Use a boundary double that emits one meaningful partial, then waits on a gate
before producing its final response. Release that gate only after the actual
application response emits the partial. Assert the partial arrived before EOF,
then verify the final correct result, complete persisted event and model-attempt
count. Bound the test deadline so a buffering regression fails rather than hangs.

This tests the SDK → Runner → ASGI path when those components are retained.
It does not prove browser rendering, intermediary proxy behaviour or provider
latency. Exercise the actual browser separately when claiming a usable UI.

## Measure the user's wait, then isolate a bottleneck

Before paid samples, agree simple versus multi-step workflows, correctness
predicates, model/output length, cold definition, streaming setting, sample count,
thresholds and request budget. A process restart makes a process-cold sample;
it does not establish that the provider's model/caches are cold. ADK Web's
streaming preference persists in the browser profile, so record it for every run.

For each submit record: submission time; last observation with no meaningful
content; first observation with meaningful content; complete correct result;
and input/Send readiness. Keep failures and timeouts in the sample. A spinner,
placeholder or incorrect answer cannot satisfy the content predicate. Validate
rendered formatting too: collapsed chat line breaks need comparison with the
underlying artefact, not a claim that the model lost its lines.

If useful content is absent at 4.9 seconds and present at 5.2 seconds, first
content lies in `(4.9, 5.2]`; a five-second target is **INCONCLUSIVE**. Report raw
intervals and sample count, median/range where defensible, and whether final
timings include a polling/detection delay. Preserve the raw observations if the
original text predicate was wrong; reanalyse them instead of spending another
request just to get a cleaner number. Owner acceptance can change a future
target; it does not rewrite the measured result against the original threshold.

For a miss, correlate sanitised invocation IDs across browser submission,
request arrival/authentication, process initialisation, model headers/first chunk/
completion, each tool/database call and rendering. Backend spans explain causes;
they do not replace the end-to-end browser sample. Correct the measured stage:
unbuffer a stream, reuse the appropriate client, remove a duplicate call or
parallelise independent work. Preserve result correctness, authority and data
boundaries; model/region changes need their own approval. Rerun equivalent
correctness and the approved comparison sample, with limitations retained.

## Prove local cleanup without overclaiming

Under the approved deletion scope, record owned `(app, user, session)` tuples,
paths, processes and artefacts. For each disposable session, call its supported
DELETE twice, then require GET 404 and absence from the relevant list. If the
backend is the checked local SQLite store, independently open the actual database
read-only, inspect its schema, and parameterise queries for those exact session
and event keys. Preserve a populated control session and prove it is unchanged;
an empty control cannot demonstrate preservation of useful data.

Stopping the default ADK Web server retains history in each app's `.adk`
directory. Session deletion does not prove uploaded artefact deletion. For a
fully isolated practice copy, stop its owned process and dispose of the approved
copy, including local stores, then repeat the cleanup check. Preserve pre-existing
sessions and the owner's credentials. Report application data, artefacts and
process cleanup separately from provider logs, backups and delayed billing.

Chapter 0 needs no standing cloud compute, index or database for these examples.
Creating such infrastructure solely to make a local workflow work expands the
task. If the target already has managed infrastructure, follow its owned lifecycle
and the [external cleanup evidence rules](external-validation.md).
