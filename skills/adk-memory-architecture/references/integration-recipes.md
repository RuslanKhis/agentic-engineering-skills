# Wire the application boundary to ADK

Read when implementing or reviewing actual HTTP admission, App/Runner assembly,
tool callbacks, public output or replay. These mechanics were inspected against
ADK 2.8.0; preserve the target's pins and validate its interfaces first. Small
extracts below illustrate integration seams, not a complete deployable server.
Their arguments come from trusted application configuration and started services.

## Assemble once, then start the controls

The baseline's managed-service assembly has this shape:

```python
from google.adk.apps import App
from google.adk.memory import VertexAiMemoryBankService
from google.adk.runners import Runner
from google.adk.sessions import VertexAiSessionService


def assemble_runner(settings, agent, plugins):
    sessions = VertexAiSessionService(
        project=settings.project,
        location=settings.agent_runtime_location,
        agent_engine_id=settings.sessions_agent_engine_id,
    )
    memory = VertexAiMemoryBankService(
        project=settings.project,
        location=settings.agent_runtime_location,
        agent_engine_id=settings.memory_bank_agent_engine_id,
    )
    app = App(name=settings.app_name, root_agent=agent, plugins=plugins)
    return Runner(app=app, session_service=sessions, memory_service=memory)
```

Adapt an existing factory instead of constructing a second runtime. This does
not provision resources, configure memory lifetime/topics, authenticate callers
or initialise protection clients. The source attaches its protected tool plugin
during API startup; calling a discoverable `root_agent` directly skips that
lifecycle. Preserve the target's injection seam rather than importing another
application's global service singleton.

Use the same session service and App name for ownership checks and Runner.
Where the selected adapter supports it, request metadata without the transcript
for ownership/policy checks (`GetSessionConfig(num_recent_events=0)` in this
baseline). Let the service allocate new session locators and verify stored TTL.
Keep async/loop-bound clients in the intended worker lifecycle and SQL clients
out of a pre-fork parent process.

Start protection and secret providers before accepting requests; make startup
and plugin registration repeatable without duplicates. On partial failure,
close already-initialised dependencies. On shutdown, stop reconciliation before
closing its gateway/ledger, then close each owned client once, attempting the
remaining closures even when one fails. Give exporter flush time room inside
Runner close and Runner close room inside whole-API shutdown. Inspect supported
close APIs instead of inventing one on every SDK service. Test the real serving
entrypoint's failed startup and bounded shutdown.

## Authenticate and protect before invocation

Use a strict bounded request schema for message and optional session locator.
Reject extra subject, tenant, customer, arbitrary state or resource selectors.
Verify one unambiguous application credential, expected issuer/audience,
signature, expiry and selected revocation policy. Resolve verified membership
to a stable internal subject; mutable email and truncated identifiers are poor
identity keys. Development aliases must remain disabled in managed production.

Keep application login, workload ADC, service-to-service tokens and delegated
tool OAuth separate. For a hosted two-token boundary, see
[managed-deployment.md](managed-deployment.md). Bound verifier/directory work;
calling a synchronous verifier in `async def` does not make it nonblocking.
Define membership refresh and revocation lag rather than assuming a fixture
directory is a live enterprise identity source.

Apply input protection before new-session creation and execution. A useful
production error contract is:

| Condition | Public meaning | Required negative assertion |
| --- | --- | --- |
| Invalid credential | Authentication failure | No session/model/tool effect |
| Valid but unmapped caller | Forbidden | No fallback subject or broader scope |
| Absent or foreign session | Same not-found result | No caller-chosen session creation |
| Malformed/rejected content | Validation/policy rejection | Unprotected input not persisted |
| Verifier, directory or policy unavailable | Safe service-unavailable result | No bypass; operational failure recorded without sensitive bodies |
| Failure after a tool may have run | Failed/indeterminate execution | Reconcile effects before retry |

The source currently maps all input-policy exceptions to 422 and all session
lookup `ValueError`s to not found. Narrower operational classification is a
production improvement, not a guarantee inherited from that code. Test duplicate
credentials, conflicting tenant claims, forged body identity, verifier outages
and unrelated SDK validation errors through the actual endpoint.

## Carry trusted context without adding model arguments

The invocation shape is:

```python
from google.adk.agents.run_config import RunConfig
from google.genai import types


async def collect_public_draft(runner, *, subject, session_id, protected_text,
                               consent, project_event):
    draft = []
    async for event in runner.run_async(
        user_id=subject,
        session_id=session_id,
        new_message=types.Content(
            role="user", parts=[types.Part(text=protected_text)]
        ),
        run_config=RunConfig(custom_metadata={"memory_write_consent": consent}),
    ):
        text = project_event(event)
        if text:
            draft.append(text)
    return "".join(draft)
```

This consumes the invocation to exhaustion. It deliberately stops before final
output screening, durable response commit and HTTP release; the caller must
complete those steps and reject an empty public draft safely. Do not return at
the first non-partial/final event and skip subsequent callbacks.

For tools, import `ToolContext` from `google.adk.tools` and let ADK inject it.
This baseline uses `.session.user_id`, `.invocation_id`, `.function_call_id`,
`.custom_metadata` and `.state`. For callbacks, use `CallbackContext` from
`google.adk.agents.callback_context`; it exposes session, invocation, metadata
and state. Check required IDs and `memory_write_consent is True` at the write
boundary. A model-visible `user_id` or `consent` argument is not a replacement.
Exercise real contexts/Runner with doubles at the model/provider edge; a
`SimpleNamespace` alone can make a nonexistent convenience property look valid.

## Project only approved public events

For typed ADK events, use a projection with an explicit partial-event guard:

```python
def final_model_text(event):
    content = event.content
    if not isinstance(content, types.Content):
        return None
    if (event.partial or content.role != "model" or event.author == "user"
            or not event.is_final_response()):
        return None
    parts = content.parts or []
    if any(part.function_call or part.function_response for part in parts):
        return None
    text = "".join(part.text for part in parts if part.text and not part.thought)
    return text or None
```

Import `types` as in the previous extract. The explicit `event.partial` check
strengthens the source projection: in ADK 2.8.0, `is_final_response()` can return
true for a partial event when `skip_summarization` or `long_running_tool_ids` is
set. Real-event tests reproduced both cases in this review; do not infer
non-partial output from that method alone.

Do not serialise whole events, state,
function payloads, thought parts or error objects into the public contract.
Test actual event types: thought plus answer, partial text with either override,
tool-bearing final
content, no public answer and a final event followed by a callback. Custom
session storage must retain complete versioned event fields and function-call
relationships internally; concatenated display text is not resumable history.

## Implement the tool-plugin contract, not just its name

Inspect the selected `BasePlugin`/`PluginManager`. In this baseline,
`before_tool_callback` receives keyword-only `tool`, `tool_args`, `tool_context`;
`after_tool_callback` adds `result`. The source transforms approved arguments or
results in place and returns `None` on success. A non-`None` value is an override;
verify short-circuit semantics instead of treating it as an ordinary result.

Maintain a per-tool schema identifying natural-language fields to transform;
an unknown tool needs a defined boundary before use. Protect a complete copy
of a structured result, cancel and await sibling tasks on failure, then publish
only a complete successful transformation. Apply protection before any state,
queue or backend write inside the tool too. Register this plugin before export
observers and test the actual manager with a downstream canary. Configuration
order alone is weaker than observing the payload received by the exporter.

## Keep replay safe across HMAC rotation

Define canonical request identity explicitly: authenticated owner, caller retry
key, protected request, supplied session locator and policy-relevant inputs such
as consent. Deterministically serialise and unambiguously separate components.
The source uses sorted compact UTF-8 JSON and length-prefixed inputs under
HMAC-SHA256. Avoid raw prompt storage or an unkeyed digest of low-entropy text
merely for deduplication. Define changed-content behaviour: including the body
in a fingerprint does not enforce one logical request per header value alone.

| Stored state | Retry behaviour |
| --- | --- |
| Completed | Return the committed protected public response |
| Reserved/running | Report in-progress; do not start another invocation |
| Indeterminate | Reconcile or expose uncertainty; no blind resubmission |
| Erased | Return the content-free gone/tombstone outcome; no regeneration |

Reserve and search retained-key aliases atomically in shared state. Record key
versions; on rotation, evaluate current and retained-version fingerprints and
alias the existing record rather than starting a new run. Keep old verification
keys until records, tombstones and overlapping deployments have passed their
retry horizons. Align record/alias/tombstone expiry to the original horizon;
neither retry nor erasure should extend it. Keep run and privacy keyrings separate.

Validate rotation against both a completed response and an erased tombstone
through the HTTP path; assert unchanged model/tool call counts. The source has
offline application coverage for those cases using a Secret Manager double.
It does not establish every distributed-store retention or key-rollout scenario.

For memory handoff details use [memory-bank.md](memory-bank.md); for telemetry
capture/schema/loss use [bigquery.md](bigquery.md). Evidence and unimplemented
extensions remain qualified in [provenance.md](provenance.md).
