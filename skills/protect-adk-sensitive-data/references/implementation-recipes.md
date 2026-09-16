# Implement the runtime boundaries

Read when changing ADK callbacks, gateway assembly, response release, client
ownership or observability. Use [boundaries.md](boundaries.md) for the policy
contracts and [compatibility.md](compatibility.md) for E1–E14 provenance. These
recipes make those contracts implementable without the companion application.
Adaptation skeletons below require the named application helpers; they are not
a complete runnable gateway or plugin. SDK observations are specific to the
installed ADK 2.8.0 / google-genai 2.19.0 source inspected for this skill.

## Assemble once; carry one deadline

Build the graph from validated trusted settings and injected dependencies:

1. Create one SDP adapter, one direct Armor adapter, an explicit model object,
   the existing session service and the runner. Register the argument/result
   plugin first and the native model-screening plugin second, once per `App`.
   Verify the registered tool names equal the policy registry names at startup.
2. Start async transports on the serving event loop. Configuration/imports must
   not open an async channel or trigger ADC. Assign ownership of every injected
   client so exactly one component closes it.
3. At request ingress, create an absolute monotonic deadline **before** awaiting
   authentication. Authenticate before body parsing or paid screening. Read the
   body incrementally under the byte bound, parse a strict request shape, and
   apply the decoded character bound. Carry that same deadline through queueing,
   screening, session locking, runner iteration and final screening.
4. Protect the message, screen the protected value, then get/create the owned
   session. Hold its turn lock through runner execution and approved-response
   collection. Bind identity through a scoped context manager that resets its
   context variable on exit; use only the protected message in `new_message`.
5. Return the approved value through the common JSON/SSE adapter. SSE starts
   with a content-free status and ends with one approved final or static error.

Set the body byte limit from the accepted encoding rather than equating bytes
and characters: a JSON-escaped non-BMP character can occupy 12 bytes, plus
bounded framing/field overhead. Reject oversized chunks before appending them.
An ASGI ingress wrapper or equivalent must cover authentication and streaming
response iteration; a deadline started inside an endpoint runs after FastAPI
authentication dependencies. The companion fixed body/read limits but still
starts its deadline after authentication; the outer deadline is additional
production hardening (E1, E10).

Put semaphore acquisition inside the absolute deadline. For each provider call,
use `timeout=min(rpc_limit, deadline - loop.time())`; if no time remains, withhold
the operation. For an initially bounded integration, set `retry=None`. Limit
active requests separately from active screening calls if runner/model work can
exhaust capacity. Test cancellation while waiting for a slot and during an RPC.

ADK 2.8.0's native Armor plugin calls its client without explicit `retry` or
`timeout` kwargs and has no semaphore. Direct-client limits do not automatically
cover those calls. Its constructor accepts `client=...`: an application-owned
async facade can apply the same slot, deadline, timeout and retry policy to
`sanitize_user_prompt` and `sanitize_model_response`. Count native and direct
calls separately and test this facade through the native plugin. This is an
adaptation requirement, not an implemented property of the historical gateway.
`retry=None` disables the GAPIC retry policy; it does not prove that a supplied
transport has no lower-level retry. For an exact attempt ceiling or no-wire-retry
claim, verify the SDK/transport construction and accounting described in
[live budget and retry accounting](troubleshooting.md#live-budget-and-retry-accounting).

## Protect arguments before ADK stores them

**ADK 2.8.0 adaptation skeleton.** Implement `protect_arguments(name, args)` to
return `None` after successful in-place mutation, or a strict static blocked
dictionary. It must validate the full shape, protect only declared text, then
validate again. Implement `public_result(name, args, result)` using the stronger
projection/validation order in [boundaries.md](boundaries.md).

```python
from typing import Any
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_response import LlmResponse
from google.adk.plugins import BasePlugin
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
from google.genai import types


def safe_stop(marker: str) -> LlmResponse:
    # marker is selected by application code, never copied from provider data.
    return LlmResponse(
        content=types.Content(role="model", parts=[types.Part(
            text="I cannot process that request safely.",
        )]),
        custom_metadata={marker: True},
    )


class ToolBoundary(BasePlugin):
    async def after_model_callback(
        self, *, callback_context: CallbackContext, llm_response: LlmResponse,
    ) -> LlmResponse | None:
        for part in (llm_response.content.parts or []) if llm_response.content else []:
            call = part.function_call
            if call is None:
                continue
            if not isinstance(call.args, dict):
                return safe_stop("tool_policy_blocked")
            blocked = await self.protect_arguments(call.name or "", call.args)
            if blocked is not None:
                unavailable = blocked["error_code"] in {
                    "SENSITIVE_DATA_UNAVAILABLE", "MODEL_ARMOR_UNAVAILABLE",
                }
                return safe_stop(
                    "screening_unavailable" if unavailable else "tool_policy_blocked"
                )
        return None

    async def before_tool_callback(
        self, *, tool: BaseTool, tool_args: dict[str, Any], tool_context: ToolContext,
    ) -> dict[str, Any] | None:
        return await self.protect_arguments(tool.name, tool_args)

    async def after_tool_callback(
        self, *, tool: BaseTool, tool_args: dict[str, Any],
        tool_context: ToolContext, result: dict[str, Any],
    ) -> dict[str, Any]:
        return await self.public_result(tool.name, tool_args, result)
```

Construct the plugin with a stable name and its injected boundaries. On success,
commit validated arguments with `args.clear(); args.update(safe_args)` to the
**original dictionary**. An empty dictionary is still an original object: avoid
`call.args or {}`, which substitutes a different dictionary when it is empty.
If the domain permits no-argument calls represented by `None`, explicitly
normalise that representation before validation and assign the safe dictionary
back to the function call; otherwise reject it.

ADK's plugin manager stops at the first non-`None` callback return. Returning a
replacement response on success skips the following Armor plugin. Returning a
replacement on failure deliberately removes every function call and tags the
safe event for the public projector. ADK copies arguments before tool execution,
so `before_tool_callback` alone cannot repair the earlier persisted event.
Handle provider failures inside the boundary and return static decisions;
unhandled callback exceptions reach ADK logging with exception details.

The actual-runner canary is a small executable scenario, not a direct method
test: subclass `BaseLlm`, record `LlmRequest` snapshots, yield a first
`LlmResponse` containing a function call with a synthetic email in a permitted
text field, then yield a safe final response. Inject this model into the real
`Runner` with in-memory sessions and fake providers. Assert the raw canary is
absent from stored events, the second model request, captured logs and public
response, and that the side-effect sink receives only transformed text. Repeat
with denied credentials, unavailable screening, an unknown tool and an extra
authority field: assert zero side effects and no rejected call in history.
Finally emit a valid call plus blocked visible model text in the same response;
assert the following screening plugin runs and prevents execution. For multiple
calls, place the invalid call after a valid one and assert the whole response
is withheld before any tool runs. E4 records the original runner evidence;
the multiple-call and empty-dictionary cases are additional target regressions.

## Project and screen the exact public answer

**Algorithm; adapt event/error types to the installed runner.** Classify every
event in this order, before extracting any answer text:

```text
screening_unavailable is true                         -> UNAVAILABLE
model_armor_blocked or tool_policy_blocked is true     -> BLOCKED
trusted ADK AuthorizationDenied error code             -> UNAUTHORIZED
any other error_code or error_message                 -> ERROR
not final, absent content, or content.role != "model" -> IGNORE
otherwise join text parts excluding thought parts     -> FINAL(text) or IGNORE
```

Markers above are exact boolean flags generated by trusted hooks. Do not render
metadata, `error_message`, function-call arguments or function-response payloads.
Map error kinds to static application exceptions/public codes; the historical
gateway uses one generic 404 for missing and unauthorised sessions. ADK 2.8.0
turns tool authorisation exceptions into error events, so catching only the
original Python exception misses this path (E1, E5).
The native Armor plugin marks both a detected match and its fail-closed provider
failure as `model_armor_blocked=True`. A distinct unavailable outcome requires a
tested adapter/plugin adaptation; the projector cannot infer it from safe text.

```text
selected_final = absent
try:
    for each event in async runner iterator:
        projected = project(event)
        on BLOCKED/UNAVAILABLE/UNAUTHORIZED/ERROR: abort
        on FINAL: enforce text bound; selected_final = projected.text
finally:
    await iterator.aclose() when available
require selected_final exists and is non-empty
approved = await screen_complete_response(selected_final, protected_prompt)
require approved is a non-empty string within the output bound
return approved
```

The historical runner contract selects the last complete final response; it
does not concatenate complete snapshots or expose deltas. If the target emits
fragments instead, define and test their assembly contract before screening.
For either contract, concatenate text parts within a selected event so a secret
split between parts is screened as one string. Apply the same gate to JSON and
SSE; never release a prefix while the runner or final check is outstanding.
Keep the overall deadline active through iterator closing and final screening.
Post-screening output bounds are additional hardening if rewriting is enabled.

Test: a block/error event that also appears final; a safe final followed by an
error; intermediate canary deltas; a canary split between text parts; thoughts
and tool payloads; no final; oversized final; screening failure; and iterator
closure on block, timeout and cancellation. Assert JSON/SSE agree and both
release zero answer bytes on failure. See E5 and `test_security_invariants.py`
for historical release evidence; new cancellation/assembly variants need fresh
target tests.

## Reuse and close owned clients

**ADK 2.8.0 / google-genai 2.19.0 code fragment.** Build an explicit
`Gemini(model=trusted_model_name)` once and pass that object as `LlmAgent.model`.
The tested workflow shallow-clones the agent; the explicit model survives and
retains its cached SDK client. Retain the owned model separately if a test
replaces `root_agent.model` with a scripted model.

```python
from google.adk.models.google_llm import Gemini


async def close_owned_model(model: Gemini) -> None:
    client = model.__dict__.get("api_client")
    if client is None:
        return
    try:
        await client.aio.aclose()
    finally:
        client.close()
```

`Gemini.api_client` is a `cached_property`; reading it during shutdown would
create a previously unused client. In the inspected GenAI version, `Client.aio`
returns the already-created async facade (`_aio`); async and sync closes are
distinct. Recheck these details on upgrades. This fragment applies to a client
created through the model; if supplying `Gemini(client=...)`, track and close
that owned client explicitly, including when it was never cached as `api_client`.

Close runner/plugins, then owned model, direct Armor and SDP, using nested
`try/finally` or an equivalent cleanup stack so every close is attempted. Roll
back already-started dependencies if a later startup fails. Native Armor's
`close()` closes its lazy internal `_client`, but not its supplied client;
the application must close an injected client/facade. Mark lifecycle state so
repeated shutdown does not double-close shared resources.

Verify repeated real-runner calls reuse one underlying SDK client and auth load,
while two users' histories stay isolated. Also test an unused runtime, a failed
async model close followed by the sync close, and all remaining boundary closes.
E7's historical tests cover five calls and these shutdown paths. Reuse shares
transports, not conversation state. Same-session turns require serialization;
different sessions should remain independent. A process-local lock is only a
single-process guarantee, and an unbounded lock registry needs a retention
strategy before production deployment (E1, E10).

## Configure and verify observability

For the inspected ADK 2.8.0 implementation, this is a deployment configuration
baseline; validate it before constructing the application or telemetry objects:

```text
ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS=false
OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=NO_CONTENT
ADK_EXPERIMENTAL_TELEMETRY=false
ADK_CAPTURE_MCP_HTTP_BODIES=false
ADK_TELEMETRY_IGNORE_RUN_CONFIG=true
```

Legacy ADK span content defaults **on**. The OTEL setting has named modes;
`NO_CONTENT` is explicit. Per-request `RunConfig.telemetry` otherwise overrides
environment choices; `ADK_TELEMETRY_IGNORE_RUN_CONFIG=true` selects environment
policy. `TelemetryConfig` snapshots environment values at construction, so
changing process variables later does not repair an existing config. Set and
validate these values in trusted startup/deployment configuration, rather than
silently using `setdefault` when a conflicting value is present. Preserve an
existing equivalent stronger policy after verifying its effective behaviour.

Offline checks can additionally set `OTEL_SDK_DISABLED=true`; that is not a
replacement for reviewing production exporters. External GenAI instrumentation
reads its own environment and does not necessarily honour ADK per-run options.
Inspect middleware, HTTP wire logging, exception exporters and trace processors
separately. Native Armor uses `logger.exception` on provider failures, and the
plugin manager logs uncaught callback exceptions with `exc_info=True`. Safe
application logging alone therefore does not establish safe SDK failure logs.
At the configured SDK log handlers, replace sensitive failure records with a
static stage/outcome; discard the original `msg`, `args`, `exc_info`, `exc_text`,
`stack_info` and unapproved extras before export. Cover every handler/exporter
receiving those records, not only the console. Alternatively normalise provider
exceptions inside an injected boundary, raising a generic failure outside the
original exception handler so it retains no provider exception context. Verify
the complete path with a provider exception containing a canary. Frame-local
and request-body capture still require their own exporter controls.

Keep application logs behind a narrow helper accepting generated request ID,
allowlisted stage/outcome, elapsed milliseconds and numeric call counts only.
Count started/completed/failed/cancelled calls per trusted boundary name; count
retries if enabled and include native-plugin calls. Never label metrics with
user/session text, resource references or provider error strings. Stage timings
identify cumulative screening cost without retaining content; do not interpret
a small warm sample as a capacity or tail-latency benchmark. Safe typed provider
diagnostics and their allowlist construction belong in
[troubleshooting.md](troubleshooting.md).

Source anchors: E1/E4/E5/E7 describe the application and historical tests;
`tests/test_request_limits.py` covers padded/slow request bodies;
`tests/test_model_client_lifecycle.py` covers client ownership; ADK
`plugins/plugin_manager.py`, `integrations/model_armor/_plugin.py`,
`telemetry/context.py` and `telemetry/tracing.py` supply the inspected SDK
contracts. Source inspection establishes these behaviours, not a fresh live
integration or a complete exporter audit. Keep full cloud executors, demo
identities, stores and campaign harnesses out of runtime adaptations.
