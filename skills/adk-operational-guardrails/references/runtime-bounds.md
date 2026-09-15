# Runtime bounds and repeated actions

Read for loops, deadlines, tool admission or ADK integration. Outcome: tests prove forbidden work does not execute, including when a model stalls before its first event.

## Select the boundary

Define independent positive bounds for workflow rounds, model calls, tool calls and the whole invocation deadline. Count each tool in a parallel batch. Decide whether an excessive batch is rejected atomically or admits only the remaining allowance; preserve an existing contract and test the actual executions. An event counter is neither a model-call counter nor a tool-call counter.

For ADK 2.8.0, `RunConfig(max_llm_calls=N)` passed to the actual runner gives a model-call bound; choose a positive finite integer, because zero or a negative value disables that bound. It does not bound transport retries within a generation. Validate call exhaustion against the project's pinned version and catch its stop exception in the outer application. [Pinned official API](https://raw.githubusercontent.com/google/adk-python/v2.8.0/src/google/adk/agents/run_config.py).

Put the whole asynchronous iteration inside one cooperative deadline, starting before model work, with a monotonic clock. Use shorter provider deadlines where needed. Close the runner iterator on exhaustion, errors and early stops in the same task that iterates it; moving closure into a different task can break context-variable cleanup. A time check only after an event cannot stop a model that never yields.

Cold startup may perform synchronous imports or schema preparation that a cooperative timeout cannot pre-empt. Separate and measure process startup and invocation latency honestly. Use a supported startup preparation path with zero provider/tool dispatch, or return the deadline stop; do not extend the invocation deadline silently or preload private SDK modules and unrelated providers to make a tight timing test pass. Verify the first invocation as well as warm ones when this distinction matters.

Use a tool wrapper or a tested pre-execution callback/plugin for permission and repeat checks. Observe function calls/responses through ADK's actual APIs and correlate by call ID, including parallel calls and partial events. A stored function-call event is not proof of tool execution; the historical companion event guard was effective under its tested ADK ordering. Preserve that regression before changing an existing event guard or upgrading ADK.

## Classify repeats

| Outcome | Next action |
| --- | --- |
| Successful read | An identical read may be legitimate; retain finite call/time bounds |
| Terminal validation/policy failure | Block the unchanged action before another execution; request corrected information or return a static stop |
| Documented transient failure with no ambiguous effect | Apply the project's bounded retry policy and consume attempt/time allowances |
| Write accepted, timed out or outcome unknown | Reconcile by a durable operation/provider key; never blindly replay with a fresh key |
| Pending approval | Return the existing operation state; do not create a second review or execute the action |

Canonical arguments help detect identical requests but are not business identity. Changed incidental text can evade an argument hash; bind writes to the stable operation described in [human review](human-review.md). Do not log raw arguments or reversible low-entropy fingerprints. An ambiguous result and a terminal rejection need different recovery paths.

## Use the local starter narrowly

[invocation_guard.py](../assets/invocation_guard.py) is a complete dependency-free module to copy and adapt when no equivalent guard exists. Inspect its API and [tests](../tests/test_invocation_guard.py). Create one guard at trusted invocation entry and share it across every guarded tool in that invocation; creating one per call resets all limits. It belongs to one event loop, not a process-global service.

The starter guards asynchronous tool admission and outcomes only. Put the **runner itself** inside an overall deadline so a model that never calls a tool also stops. Add the project's model-call cap, usage accounting and static outer stop handling separately. Catch `GuardStopped` at the application boundary and end the invocation; returning it as a retryable tool result can continue the loop. Translate domain results explicitly into success, terminal failure or ambiguity; do not classify a timeout as safe to retry because its exception sounds temporary.

Use `await guard.run(action, arguments, operation, effect="read", classify=classifier)` where `operation` is a zero-argument async callable around the real tool and `classifier` maps its existing result schema to `"success"`, `"terminal_failure"` or `"ambiguous"`. Without a classifier, every ordinary return counts as success; structured errors therefore require one. Select `effect="write"` in trusted registration code for side effects, never from model input. The paired `admit()`/`finish()` interface is for custom adapters that can guarantee completion accounting on every exit.

Successful write replay, persistent deduplication and approval require a durable operation service. The starter cannot substitute for them. Its local timeout cannot interrupt blocking synchronous code, kill an already-running thread, or undo remote effects. Provider calls need bounded asynchronous behaviour or worker isolation; record uncertainty when cancellation leaves the outcome unknown.

Required regressions: the second terminal failure executes zero extra side effects; successful repeated reads remain possible; parallel admission stays within the chosen cap; a stalled model terminates; the last permitted tool can still produce its result/final answer if other bounds allow it; stops use no additional model call. For iterative refinement also test exhausted-loop status: returning the latest draft does not establish reviewer acceptance.
