# Verify the ADK execution path

Read this when adding ADK HTTP/confirmation integration tests, proving live-call
limits, or diagnosing response latency. The recipe comes from the Chapter 1
ADK 2.8.0 tests and audit failures. Inspect installed signatures before adapting
it; source paths named in [compatibility](compatibility.md) are provenance, not
required imports. Use the target's existing test runner.

## Exercise HTTP, confirmation and stored history offline

Keep the public tool, retry wrapper and ADK application real. Substitute only
the external provider and model boundary:

1. Disable automatic dotenv loading before constructing the test application
   (`PYTHON_DOTENV_DISABLED=1` in the tested loader). Block unexpected socket
   connections so a missed substitute fails instead of spending quota. An
   in-process `httpx.ASGITransport` needs no listener. A separate browser harness
   may allow only its explicitly owned loopback transport; that is a different
   test boundary.
2. Create the actual ADK ASGI application with disposable session storage. Enter
   its lifespan, create a session through its real route and close both client
   and application in test cleanup. An HTTPX ASGI transport alone does not
   start the application's lifespan.
3. At the pinned model generation method, supply a finite queue of model steps:
   emit a function call, then derive the scripted answer from the **actual**
   tool response in the next model request. Fail on an extra model call and
   assert that the queue is empty at the end. A fixed success sentence would
   hide a broken tool-to-model connection.
4. Submit through `/run_sse`, verify its event-stream content type, parse the
   events and reject error events. Assert the structured tool result reaches
   both the subsequent model input and stored session history. SSE plumbing
   can pass even when no incremental answer text was rendered in a browser.
5. For a mutation, assert missing consent emits `adk_request_confirmation` and
   causes zero provider calls. Read its returned call ID and original action;
   send the decision through the function-response route rather than calling
   the Python function directly. In the tested 2.8.0 path the response part was:

   ```python
   {
       "functionResponse": {
           "name": "adk_request_confirmation",
           "id": confirmation_call["id"],
           "response": {"confirmed": False},
       }
   }
   ```

   Preserve the selected client/session contract and, when supported resume
   semantics require it, the original invocation identity. Assert rejection
   makes zero provider calls. In a separate approved case, force commit then
   lost response at the provider double and count both attempts and effects.
6. Inspect effective model settings at **both** tool selection and answer
   synthesis. A configuration attached only to one stage once appeared correct
   in source but failed at the second boundary. Preserve real retry sleeps in
   deadline tests even if separate wiring tests remove random waits.

This proves offline wiring and application effects. It cannot establish live
reasoning, rejection wording, model availability or real provider replay.
Check the chosen production session service independently; the local Web
SQLite-backed path does not establish support for every database-backed ADK
service. See the [confirmation limitations](https://adk.dev/tools-custom/confirmation/#known-limitations).

## Prove live limits before consuming samples

The ordinary tool retry decorator does not bound model requests. Before an
approved live campaign, exercise its actual Runner or CLI plugin-loading path
offline and inspect the final outbound SDK configuration.

| Boundary | Assertion that matters |
| --- | --- |
| Admission | Atomically reserve a provider request before dispatch. A rejected model/input/configuration makes no request. Failed dispatched requests still consume allowance. |
| Scope | New sessions, runners or plugin instances do not each acquire a fresh allowance. Define worker/process scope; a process-local counter is not a distributed or restart-safe limit. |
| Transport | Verify effective SDK timeout units, retry count and output limit. The tested Google Gen AI timeout field used milliseconds; the mock tool used seconds. Count hidden SDK retries or explicitly disable them for the campaign. |
| Streaming | Partial chunks belong to one admitted request. Final aggregation records available usage once; repeated completion callbacks do not double-count. Retain usage from a chunk even if the trailing chunk has none. |
| Time | Admission closure prevents future requests but does not necessarily cancel an in-flight call. Use a request deadline and an independent supervisor/stop mechanism when an absolute execution window is required. |
| Restart | Preserve consumed campaign state or stop for a new campaign decision; restarting a process to reset its counter does not replenish approved allowance. |

Choose limits for the approved workflow rather than copying the historical
24-request/30-minute settings. One user turn can require multiple provider
requests, especially after a tool result or confirmation decision. Input
characters, output-token settings and request counts are useful controls but
not a hard currency spending cap. A `RunConfig.max_llm_calls` value in a
different Runner script is not inherited by `adk web`; prove the route actually
uses the control. [ADK runtime configuration](https://adk.dev/runtime/runconfig/).

## Diagnose responsiveness without discarding correctness

When latency is part of the request, first test the read-only UI observer on
an offline interaction. A broken DOM operation or stale observer closure can
consume a paid sample without a usable measurement. Record the source version,
model/backend/location, effective thinking setting and UI streaming state;
confirm streaming at the backend too. In the audit, reducing thinking to
MINIMAL produced incorrect answers, so faster output alone was not accepted.

Define first meaningful answer text, terminal correctness and final input-ready
state before measurement. Exclude thoughts, loading icons and tool badges.
Time confirmation request visibility separately from the decision-to-result
interval, excluding human deliberation. Distinguish process-cold from a new
workflow on a warm process. Submit each sample once; uncertain UI dispatch
calls for observing the existing turn, not sending it again.

Bracket submit and observation calls with a host monotonic clock. The first
positive observation gives an interval, not the exact rendering instant. Keep
paired wall-clock stamps only for correlation with server logs; do not subtract
monotonic times across a process/observer reset. Preserve failures and missing
timings instead of replacing them with better samples.

Correlate model spans, tool attempts, actual waits and final synthesis. Scheduled
retry-delay totals are not actual sleep duration when a deadline interrupts
backoff. Streaming may improve visible feedback without changing those waits.
Report retrieval successes alongside timing for answers **and errors**. The
one-second historical lookup budget yielded two retrievals and four accurate
errors in six turns; that is a measured recovery/responsiveness tradeoff, not
a real-service availability estimate or a universally useful timeout.
