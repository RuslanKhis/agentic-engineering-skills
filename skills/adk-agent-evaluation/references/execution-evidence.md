# Runtime checks and trustworthy observations

Read this when implementing a Runner/HTTP test harness, injected failures, an evaluation observer, worker deadlines or browser measurements. The recipes derive from actual companion regressions and the synthetic-data audit observer. They describe adaptation steps, not an installable tracing framework. Inspect the target's pinned interfaces first.

## Build through the entrypoints people use

Choose layers affected by the change; a backend-only fix does not require deploying an application.

| Layer | Concrete implementation and acceptance |
| --- | --- |
| Assets | Parse every selected eval set/config/spec with the installed schema model; assert the selected file list is nonempty. Valid JSON alone is insufficient. |
| Tools/backend | Assert authorised effects, no-effect rejections, idempotency and real domain state independently of model text. |
| Runner | Inject the scripted model at the agent factory, preserving actual tools, callbacks and session service. Record requests, exhaust events and close the Runner. |
| CLI | Execute the real entrypoint in a subprocess with deliberate cwd/environment. Check exit, output and effects; a direct helper call misses import/argument wiring. |
| HTTP | Use the actual application factory/router and test client. Create a session, submit a turn, parse response events, then read saved state. Assert actual effects and final claims in addition to status codes. |
| Browser | Check rendered output, completion/error recovery and user controls. HTTP tests do not establish browser rendering or submit-to-render timing. |
| Live/staging | After approval, exercise the real provider and required remote adapters. Offline framework tests cannot establish credentials or remote contracts. |

For ADK 2.8.0, the companion HTTP path uses `get_fast_api_app(..., web=True, use_local_storage=False)`, session creation under `/apps/{app_name}/users/{user_id}/sessions`, `/run`, and session readback. Its response list is parsed with `Event.model_validate`. These are version-bound interfaces to inspect, not a replacement for an existing custom server or evidence about its streaming route.

### Construct a decisive scripted-model test

1. Subclass the installed `BaseLlm`. For the verified interface, implement async `generate_content_async(self, llm_request, stream=False)` yielding `LlmResponse`. Store a queue of prepared responses in Pydantic `PrivateAttr` fields, and retain `llm_request.model_copy(deep=True)` before returning each queued response. Raise when exhausted; a permissive default would hide an unexpected generation.
2. Build a tool-call response using `types.Content(role="model", parts=[types.Part(function_call=types.FunctionCall(name=tool_name, args=arguments))])` inside `LlmResponse`. Use multiple function-call parts to reproduce a batch; use a text part for a model-written final answer. Supply arguments from the actual schema.
3. Create a session with explicit synthetic trusted state, construct the real Runner and consume `run_async` with the user message. Keep the same session for a stale-state reproduction; create fresh business fixtures separately when independence is required.
4. Assert attempted calls from `event.get_function_calls()`, results from `event.get_function_responses()`, stored effects and the completed response. Preserve call IDs for correlation. A forced invalid call is expected evidence of a tested guard, not a requirement that the model double make the correct decision.
5. Assert generation count when the change concerns callbacks or cost. A receipt callback can legitimately finish without another model response. Leaving the old extra scripted response unnoticed could hide the intended saving; fail on unexpected extra generations and check unused scripted responses when the scenario requires exact consumption.

Inspect callback composition and short-circuit behaviour before adding a guard, observer or receipt renderer. Existing callbacks may return a response that prevents later callbacks from running. Exercise the resulting order, and keep authorisation at the real tool/backend boundary. ADK `State` is not an ordinary dict; the verified implementation clears temporary values by assignment, not `pop()`.

For generated receipts displayed in Markdown/HTML, keep caller-supplied identifiers literal: test escaping, control characters and length bounds as well as dynamic amounts/statuses. Rendering must neither invent authority nor reinterpret an untrusted identifier as active markup. These checks supplement current-invocation provenance and same-batch success preservation.

### Keep two failure tests separate

For deterministic Environment Simulation in ADK 2.8.0, configure `EnvironmentSimulationConfig.tool_simulation_configs` with the actual tool name, an `InjectionConfig` with probability `1.0` and a fixed seed, and an `InjectedError` such as a synthetic 503. Install `EnvironmentSimulationFactory.create_callback(config)` through the existing before-tool callback seam. Assert the injected result and that the real tool/backend was **not reached**. A scripted follow-up answer establishes orchestration, not the live model's recovery choice.

Separately arrange the real backend adapter's test double to return or raise its failure through the real tool body. Assert the tool's status mapping, receipt/state handling and absence of an unauthorised write. An interception test bypasses this code and cannot cover it. Contract tests against the real service need separate approval/isolation and remain distinct from plausible generated mock data.

## Prove a deadline interrupted the intended work

The parent should launch an owned worker with a positive elapsed-time limit, propagate failures, stop the owned process/group on timeout and reap it. Test the exact supervisor implementation; a coroutine timeout cannot interrupt synchronous grading on the same event loop.

In the offline regression, substitute the provider and grading boundaries, prevent external connections before imports, and write a PID/monotonic-timestamp sentinel **inside** the blocking grader immediately before it waits beyond the deadline. Assert the sentinel exists, a meaningful interval was spent in that block, the parent returns within its bound and the child PID no longer exists. Cold metric-registry imports consumed earlier short test deadlines: a timeout without that sentinel proved only slow startup. Give the test enough startup budget without silently changing the production deadline. Validate process-group handling separately on each claimed OS.

## Make the observer earn trust

Design a minimal event schema before wrapping execution: campaign/run, process, invocation, model-call and transport-attempt IDs; boundary start/end/error; tool name/result category; policy decision; timing and numeric usage. Link a backend effect to its originating invocation. Under concurrency, a change in the process-wide store count cannot identify which user's request caused it.

Test wrappers with controlled boundaries before a paid run. They must call the original once, preserve return objects and exceptions, retain stream closure/cancellation, and pass configuration to child workers. Verify an intended call limit with a scripted overrun. Use append-only records flushed per event, with separate process files or safe serialisation; a missing end event marks incomplete work, not zero effects. Fail visibly if required observation cannot initialise, and scope instrumentation to the chosen test command.

Count logical model calls separately from transport attempts. For a campaign, a planning upper bound is maximum agent turns × enforced model calls per turn, plus simulator generations. SDK retries can multiply transport attempts; managed scoring may contain opaque additional work. Validate any installed `RunConfig.max_llm_calls` control independently; the audit's per-turn setting was not a shipped global model/tool budget.

Sum usage once per logical call. Streaming responses may repeat cumulative usage; use the last authoritative usage for that call rather than summing partials, and avoid counting duplicate Runner-event usage again. Report unavailable scorer usage or unmatched starts as unknown. None of these local counters establishes billed cost or cancels already accepted requests.

The historical observer captured selected synthetic message/tool content. For a reusable production observer, start with allowlisted metadata and opaque identifiers; use the data controls in [evaluation-design.md](evaluation-design.md) before retaining content. Do not copy synthetic-audit logging wholesale into production.

## Calibrate browser measurements before spending on them

1. Use an offline deliberately delayed response to validate the observer. Verify that it records submission, first meaningful answer text and completion, including an initially empty response area.
2. Create a sample record **before** the single submission. Measure elapsed time with a monotonic observer clock. Record poll timestamps, gaps/errors and observation bounds; a browser-automation round trip adds observation overhead.
3. Poll until a duration deadline. A locator's short default wait or a fixed poll-count ceiling can end observation before the intended deadline. Do not retry the submission if observation fails after a possible write; preserve the missing measurement and recover the existing invocation's evidence.
4. Define meaningful text and completion for the real UI. A spinner, tool row or generic status message is not an answer. Nonstreaming output can make first text and final text coincide; it does not measure first generated token.
5. Use fresh sessions and a declared cold/warm server policy. Record backend initial state separately: a new session can still reuse an idempotent business object. Retain every approved sample, failures and gaps; correlate UI timings with model/backend phases before optimising.

Completion: report the measurement boundary, individual observations and missing values. A few warm samples support their observed range/median, not a production p95 or SLA. The historical measurements were local browser rendering with cloud inference, not a deployed-service benchmark.
