# Troubleshooting and boundary tests

Use this reference for a failed integration, missing or duplicated output, cancellation, or a latency question. Diagnose the target's selected JSON or AG-UI contract before changing transport, dependencies or infrastructure. These procedures and acceptance targets are guidance; historical verified behaviour and its limits are recorded in [provenance.md](provenance.md). A successful new test establishes only the boundary it actually exercises.

## Locate the first divergent boundary

Reproduce with synthetic input under a fixed attempt/time budget. Record the expected public result, observed failure and relevant versions. Follow one invocation through the boundaries below; correct the first divergence and rerun that regression. A plausible answer alone is insufficient evidence of a tool result or rendered card.

| Boundary | Evidence to compare |
| --- | --- |
| ADK or managed provider | Confirmed function call, correlated function response, public text versus thought/partial content, and terminal error/outcome. |
| Application collector or AG-UI translator | Selected public text, validated results/state, encoded event order, and matching run/message/call/result identities. |
| Gateway or CopilotKit BFF | Verified caller context, forwarded contract, response framing, buffering, cancellation and deadline behaviour. |
| Browser store and renderer | Registered agent/tool names, runtime parsing, retained messages, duplicate handling, visible result and restored controls. |

Inspect full payloads only in controlled synthetic tests. Default diagnostics retain allowlisted event types, bounded sizes, timings, safe failure categories and opaque correlations. Keep prompts, credentials, raw user/resource identifiers and unfiltered exceptions out of diagnostic records. Keep unique correlation IDs out of metric labels. A request reference is not a configured distributed trace.

## Symptom to regression

| Symptom | Boundary evidence | Correction | Regression that closes the issue |
| --- | --- | --- | --- |
| Answer appears but a tool card is missing or broken | Compare the actual source call/result with the translator allowlist, encoded result, BFF forwarding, registered tool name and renderer's runtime schema. | Align the mismatched name, correlation or validated result variant. Keep malformed/unknown results in a safe failure state; preserve the target's domain schema. | Run the configured tool with a synthetic model response; verify its arguments, result and rendered card together. Include malformed and null results. |
| Several cards appear for one tool | Compare partial argument events, confirmed calls, stable call IDs and repeated delivery in the browser reducer. | Announce one confirmed call, keep argument fragments under that ID, and correlate exactly one result. If replay is implemented, preserve IDs and make repeated delivery harmless. | Partial arguments followed by one confirmed call produce one card. Two simultaneous calls to the same tool retain distinct results; ambiguous IDs fail under the chosen policy. |
| Answer text repeats or is missing after partials | Compare source partial chunks and completed aggregate with emitted deltas and browser text. | Apply the selected delta/aggregate policy once per logical message; keep thought content and unapproved authors out. | Partial `Bill` + `ing.` followed by aggregate `Billing.` produces `Billing.` once. Test aggregate-only and partial-only termination separately. |
| Remote SDK reports a closed transport | Check who owns the SDK client, whether only its returned remote object survives, and when lifespan/garbage collection closes it. | Retain client and remote object together through consumption/closure; use supported lifespan shutdown. | Through the installed SDK and fake transport, drop unrelated references and force collection; the retained pair still works, then closes at shutdown. |
| A supplied ID fails creation, disappears, or seems to belong to another user | Compare application syntax, pinned provider creation rules, exact requested/returned resource, verified owner and typed metadata status. | Validate provider creation rules or map application IDs to provider IDs. Follow the selected create/resume contract; only confirmed absence permits authorised creation. Generic query 400/403 or failed inventory remains an error. | Resume-only unknown IDs and wrong-owner IDs fail safely with zero model calls; test authorised first creation, wrong resource names, unsafe/provider-invalid IDs and an ambiguous creation outcome without a second create. |
| 401/403, wrong project/model, or configuration edits have no effect | Identify the failing hop. Inspect configuration sources and precedence without values; distinguish browser identity, service credential, CLI login, ADC/quota project, Runtime region and model location. | Correct the exact verifier/configuration boundary and restart affected local processes as required. Prepare any required external permission change through the task's approval process. | Invalid caller credentials invoke no agent. Read-only prerequisite checks report denied access as unknown; offline tests remain runnable without credentials. |
| HTTP success or normal run completion follows an error | Inspect all events, including after final-looking text; inspect public errors and captured diagnostics independently. | Retain failure through exhaustion. Return the declared safe failure or typed partial outcome; preserve cancellation as control flow. | Answer, reported error, then another final-looking answer remains failed. A synthetic private exception marker appears in neither public output nor default diagnostics. |
| Deadline expires too late, controls remain busy, or cancellation hangs | Measure admission wait, preparation, execution, body consumption and closure independently; inspect owned tasks/iterators after cancellation. | Put waiting inside the overall budget, add appropriate dependency deadlines and bounded cleanup, and restore controls according to known versus unresolved outcome. | Use the cancellation matrix and body-deadline pattern below; count invocations and verify no automatic retry. |
| SSE connects, but answer text arrives only at completion or stalls | Check whether the provider emits public partials, then compare translator emission, wire/BFF forwarding and browser receipt/render timings. | Request the pinned ADK streaming mode where needed; otherwise fix the demonstrated parser, buffering or rendering boundary. A tool may legitimately precede answer text. | A controlled delayed source reaches the browser incrementally through the real local path. Record provider timing separately before attributing a live stall. |
| CLI exits zero or prints an ID, but the operation failed | Inspect the structured terminal result, saved operation/resource binding and bounded provider readback. | Treat exit status as one signal. Reconcile the accepted operation before resubmission; keep unknown outcomes explicit. | A fake command that exits zero with a failure result is rejected; readback uncertainty does not trigger a second mutation. |
| Stream parsing fails after the provider may have completed | Distinguish SDK JSON-lines/SSE parsing from provider execution; retain an authorised operation reference and inspect bounded status/history when supported. | Use the pinned SDK parser/encoder. Repair and replay a synthetic captured shape locally before any new invocation; reconcile effects rather than rerunning to obtain a parseable answer. | The actual installed parser consumes a synthetic equivalent successfully. A parse error causes no automatic model/tool retry and never claims the provider operation was rolled back. |

The retained SDK owner, explicit ADK SSE mode, partial/aggregate handling, confirmed calls and direct metadata absence checks came from concrete companion failures and regressions. The full production behaviours above, including generic parallel-tool correlation, durable recovery and real multi-user identity, require their own tests; they do not inherit that historical evidence.

## Offline vertical test recipe

For a local ADK backend, replace the external model boundary while retaining the real Runner, session service, tools, HTTP route and event encoder:

1. Inspect when the application captures its agent/model. In an isolated test application or process, define a scripted subclass of the installed ADK `BaseLlm` using its supported `generate_content_async`/`LlmResponse` surface. Set any test-only configuration first, import the agent module and install that model on the test agent **before the first application import** that constructs a Runner or adapter. Prefer an existing factory when it supplies the same isolation. Restore the original model after lifespan shutdown; avoid global replacement in a concurrently serving process.
2. Script a real function call with valid synthetic arguments, let ADK execute the existing safe tool, then generate the answer from its returned function response. Replace an external side-effect adapter if the tool would otherwise write outside the fixture; record that additional substitution. Counter-check actual model/tool invocations rather than stubbing the collector under test.
3. Enter application lifespan and call the existing HTTP route through the project's ASGI test client. Use the real verifier with test credentials when available; otherwise explicitly label a test-only auth override and separately confirm the default unconfigured route fails closed. A synthetic identity does not test a live identity provider.
4. Assert the complete response or encoded wire events, exact tool/result correlation and stored session history. Resume with only a new user message. Send missing/invalid auth, unknown/wrong-owner IDs and unsupported input forms; each rejected request must make zero model or side-effect calls.
5. Add scripts for partials plus aggregate, reported error after answer text, malformed tool data, a synthetic private error and a stalled model. Capture public output and logs separately. Test the browser against this local backend when one exists: success, failure/timeout, then a distinct successful request with usable controls.
6. Record exactly which boundaries were real or substituted. For a remote gateway, substituting provider transport exercises that gateway and parser; it does not execute a remote Runner. In-process HTTP tests do not establish BFF forwarding, network SSE framing or browser rendering.

The previous greenfield evaluation caught a generated disconnect-polling bug that swallowed cancellation and turned successful calls into deadline failures. Its correction and passing offline tests support testing this boundary explicitly; they do not prescribe a universal disconnect implementation. In ASGI tests, distinguish cancellation of the handler task from delivery of an actual `http.disconnect` after the request body. Keep receive ownership explicit so body parsing and disconnect observation do not consume each other's messages.

## Cancellation phase matrix

Use events/barriers to reach the intended phase deterministically. Give each assertion a bounded wait and count invocations, task/iterator closure and synthetic effects. Re-raise cancellation; inspect active work after the client has gone.

| Inject cancellation/disconnect at | Required observation |
| --- | --- |
| Admission or conversation-lock wait | Waiting consumes the overall deadline; no model/tool starts; the waiter and its bookkeeping are removed. |
| Silent provider before its next event | Disconnect is observed without waiting for another provider event; cooperative work is cancelled and the owned iterator is closed. |
| During a tool | Cooperative local work closes. A blocking worker retains its capacity slot until it actually ends; a started external effect becomes unresolved until reconciled. |
| After visible text, before terminal outcome | Earlier text does not become ordinary success. The browser settles into the selected failed/interrupted state without an automatic resend. |
| During iterator/client closure | Cleanup has its own bounded policy, including cancellation during cleanup. Unresolved remote work keeps durable admission blocked; closure failure does not silently release permission for a new writer. |

After each local case, verify a distinct new request succeeds when the relevant resources are settled. Use an independent conversation while a mutating run remains unresolved, and verify that the unresolved conversation stays gated. Never use resubmission of the cancelled mutation as the recovery test. SDK iterator closure and absence of local tasks are evidence about local resources, not proof that a remote effect stopped. Distributed settlement gates and blocking-worker behaviour are acceptance targets only when the product implements those capabilities.

## HTTP response-body deadline pattern

Test the browser request helper with a fake fetch/response boundary. First let headers arrive promptly with a successful status, then keep `response.json()` or a controlled response-body stream pending beyond a short test deadline. Separately stall fetch before headers. In both cases assert a controlled timeout, an aborted request signal, cleared timers/listeners/in-flight controls, and exactly one fetch call. Include an external abort while the body is pending if the helper accepts a caller signal.

Complete a subsequent distinct synthetic request to verify recovery. Also test malformed JSON, wrong success-field types and structured/validation-list error bodies without showing provider detail. A mock that ignores abort can require an explicit deadline race to settle the helper; that establishes the helper's bounded wait, not cancellation of real network or provider work. Exercise native fetch/body cancellation in the real local browser when available.

## Timing worksheet

Measure a user-visible objective separately from the configured failure deadline. Agree on the objective and authorised sample budget before live calls. Use synthetic content, one native user action per sample, a monotonic clock per boundary and stable opaque correlation; compare durations within a clock domain rather than subtracting unrelated host clocks.

| Record for each sample | Definition |
| --- | --- |
| Conditions | Versions, path/transport, cold or warm process, new or resumed session, foreground tab and approved attempt number. Record unknown conditions as unknown. |
| Action start | Native Send/submit observation; exclude older answers already present in the page. |
| First event | First protocol event received, labelled by event type. A run-start or heartbeat is not answer text. |
| First visible answer text | First newly rendered, layout-visible assistant prose; exclude spinners, telemetry and tool cards. |
| Tool milestone | Separately record confirmed call and validated result/card times. Argument completion is not execution success. |
| Final answer and terminal outcome | Record answer completion and the run's success/failure separately. DOM idle/quiet-period heuristics do not prove provider settlement. |
| Validity and result | Functional result, failure/timeout, missing milestones, tab visibility and sampling gaps. Retain invalid/failed samples with their reason. |

For collected JSON, first visible text and final answer may coincide. For streaming, compare provider emission, translator output, BFF receipt/forwarding and browser rendering to locate accumulated delay. Check explicit model streaming and proxy buffering before proposing larger infrastructure. Warm instances can reduce startup delay but do not guarantee model/tool latency.

Report sample count and individual observations before summaries; small samples do not establish an SLO or justify percentile claims. The historical managed browser campaign missed its five-second first-answer target despite functional success and streamed text; two model-stage stalls had no established cause. Preserve that uncertainty. A new timing run consumes its approved request budget, including failures; it does not authorise retries or configuration changes to improve the reported sample.
