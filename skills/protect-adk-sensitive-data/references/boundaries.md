# Integrate protection across the application

Read when a project has tools, stored conversations, custom entry points or
streaming. Follow the existing architecture; use this as a boundary checklist,
not a reason to replace an application with an example.
For callback signatures, runtime assembly, final-event selection, client
ownership or telemetry configuration, read
[implementation-recipes.md](implementation-recipes.md).

## Request and session boundary

Record every route into the runner. A development UI that bypasses a protected
gateway also bypasses its pre-persistence control. Either provide equivalent
protection there or keep that entry point out of the protected deployment.

<!-- shared:verified-principal -->
**Identity comes from a verified principal.** Verify the caller's credential
at the server (signature, issuer, audience, expiry and required claims, with
the pinned provider library) and derive one internal principal from it. An
email address, a client-sent `user_id`, a session or thread locator, an
invocation ID, a model-chosen argument, user text and editable headers or
session state never prove identity. That principal is the only source of the
ADK `user_id` on every Runner and session call, of the owner key on every
record, and of the subject every tool and credential lookup acts for. Tools
read it from trusted context (`tool_context.user_id`, `ToolContext.session.user_id`
or the pinned SDK's accessor), never from their own arguments. Create and load
sessions under it; an unknown or foreign session fails without revealing that
it exists. A verifier outage and an invalid credential both deny access; only
the invalid credential should prompt a new sign-in.

ADK's own API server (`adk api_server`, `adk web`, `get_fast_api_app()`)
authenticates no end user: the session routes take `user_id` from the path and
`/run` and `/run_sse` from the body. ADK 2.12.0's change "take the ADK user id
only from an authenticated principal" (d0c4060) applies to the A2A request
converter only; it authenticates nothing on those HTTP routes. Keep them
behind IAP or the application's verified-principal dependency, or on internal
ingress. A test that sends a different caller-supplied `user_id` checks lookup
partitioning, not cross-user security; a cross-user claim needs distinct
authenticated principals at the real boundary.
<!-- /shared:verified-principal -->

Authenticate using existing trusted middleware. Bound request bytes while reading, not only after
JSON parsing; independently bound decoded characters and forbid unknown fields.
Account for JSON escaping and framing when choosing a byte limit. Apply an
overall deadline that includes authentication, body reading, queueing, screening
and runner work. The historical gateway's deadline began after authentication;
an outer auth deadline is additional production work.

Protect and screen input **before** creating or appending user history. Scope
sessions by trusted tenant and user, check ownership on every turn, and record
the protection-policy version. Reject or explicitly migrate older incompatible
histories instead of silently replaying their raw text. Serialise concurrent
turns sharing a session. Process-local locks and in-memory state do not provide
distributed isolation, durability or historical data migration.

## Generated tool arguments

For each tool, declare a strict argument model, permitted free-text fields and
non-text structural constraints. Forbid extra fields and unknown tools. Do not
allow arguments such as `tenant_id`, `skip_safety` or template names to override
trusted policy. Validate the whole shape before any paid screening, transform
only declared text, then validate again. A replacement can violate length or
format constraints.

At the recorded ADK callback order:

1. In `after_model_callback`, inspect each function-call part and protect its
   arguments before the event is persisted. Mutate the **original** argument
   dictionary so the runner retains the safe values.
2. Return `None` on successful in-place mutation. Returning a replacement
   `LlmResponse` can short-circuit later plugins. Ensure the following model
   screening plugin still runs.
3. On a block/unavailable result, replace the whole model response with a fixed
   safe response and explicit blocked/unavailable metadata; leave no rejected
   function call in it. The public event projector must honour those markers.
4. In `before_tool_callback`, repeat contract/protection checks before execution.
   This second boundary does not replace the earlier persistence boundary.

Verify this with the target's actual pinned runner and stored events. A test
calling a callback directly does not prove ADK uses the mutated data. E4 in
[compatibility.md](compatibility.md) records the original real-runner tests.

## Authorisation and side effects

Inside each tool, authorise the principal against every referenced resource and
relationship. Owning an order does not imply owning an arbitrary contact. Resolve
private destinations inside a trusted adapter; return opaque references rather
than addresses. Do not make the model invent its own authorisation evidence.

Screen free text **before** a ticket write, email send, durable record or other
side effect. Output callbacks are too late to undo a write, so a screen that must prevent an effect runs on the model response before its function calls are dispatched (an `after_model_callback` that replaces a blocked response with a static message carrying no function call, with `before_tool_callback` as the second boundary), never beside the model call; a screen that only shapes the visible answer may run at release. Use a stable
domain-specific idempotency key and durable deduplication before retrying a
non-idempotent action (**production guidance**). The historical receipt tool
returned a deterministic synthetic reference and sent no real email; its hash
construction is not a production privacy token or delivery protocol.

## Public tool results

Keep the private adapter record separate from the public result. Use this order:

1. Authorise retrieval, select only explicitly permitted public fields and omit
   internal IDs, contact data and backend diagnostics. Projection is deliberate
   data minimisation, not permission to accept arbitrary values.
2. Validate the entire projected result **before** screening: strict types,
   enums for status, parseable bounded dates, domain-specific opaque-reference
   formats, maximum text/list/nesting sizes. Reject unknown public fields. For
   requested resources, verify the returned reference matches the request.
3. Protect declared free-text fields with the selected SDP/Armor policies.
   An "alignment check" added beside them is a data boundary of its own:
   LlamaFirewall's AlignmentCheck sends the user's first message and the
   whole trace, tool calls and results included, to an OpenAI-compatible
   endpoint, by default Together AI with a static `TOGETHER_API_KEY` and a
   hard-coded temperature of 0.0 (meta-llama/PurpleLlama commit d934ea2,
   `LlamaFirewall/` (MIT scanner code), read 2026-10-24).
   `AlignmentCheckScanner` itself takes no model or endpoint option, but its
   base class `CustomCheckScanner` takes `model_name`, `api_base_url`,
   `api_key_env_var` and `temperature`, so a subclass can point it at an
   endpoint inside the project; that changes where the trace goes, not what
   is in it, and it still reads a key from an environment variable. Its
   prompt leans towards allow ("When in doubt, assume the action is not
   misaligned"), a misalignment yields `HUMAN_IN_THE_LOOP_REQUIRED`, not a
   block, and a judge error yields the same `HUMAN_IN_THE_LOOP_REQUIRED`
   with a successful status, so an outage cannot be told apart from a
   finding; a trace with no user message returns `ALLOW` with an `ERROR`
   status. Treat it as a third-party sink needing the same approval as any
   model call carrying session data; it is not a gate. A judge you build
   instead can be sent only the user's goal and the proposed call, never
   tool results.
   Structural string fields must have constraints that prevent them becoming
   unscreened free-text channels. Derive those constraints from the real domain;
   do not transplant example order/contact regexes.
4. Validate the protected result again, then return only that public contract.

The historical successful-result schemas used unconstrained strings, screened
notes before full validation and did not compare requested/returned references.
An offline probe accepted sensitive data in unscreened structural fields. This
skill requires the stronger production contract; those original schemas must
not be copied unchanged. E3 documents the finding separately from live evidence.

## Complete-answer release

Project runner events through one narrow function. First recognise blocked,
unavailable and error events, including authorisation exceptions converted to
ADK error events. Map them to static public errors without provider diagnostics.
Only consider final model-role text that is not marked as thought; ignore
function-call/response payloads and intermediate deltas.

Accumulate under an output bound, stop on error/block, close the async iterator
in every path, then screen the complete projected answer. A final event alone
is not approval. JSON and SSE must invoke this same gate. SSE can emit a
content-free progress status followed by one approved final event or generic
error. Character-by-character or token streaming requires a separate tested
policy, because a secret split across chunks can defeat chunk checks.

## Logging and lifecycle

Log only an explicit metadata allowlist, such as a generated request ID, outcome
code and duration. Avoid raw bodies, prompts, tool payloads, finding quotes and
provider exception details. Inspect middleware, SDK diagnostics, traces and
error exporters independently. Suppressing displayed exception chaining alone
does not remove retained exception context or exporter capture.

Use the version-specific settings and canary procedure in
[observability configuration](implementation-recipes.md#configure-and-verify-observability).
Verify effective capture and exporter behaviour, including per-run overrides;
configuration alone does not establish that every external sink is safe.

Create clients at application lifecycle boundaries, not per callback or during
module import. The recorded runtime used an explicit `Gemini(model=...)` object
to preserve client reuse through shallow clones, and closed runner/plugins,
Gemini async/sync clients, Armor and SDP. Test repeated calls and cleanup even
when one close fails; do not initialise an unused lazy client just to close it.

RAG ingestion/retrieval, durable memory, caches, attachments, audio and images
need equivalent boundaries when present. For attachments the ADK seam is a
plugin's `on_user_message_callback`, which runs before the runner saves the
user message to the session (2.12.0 `runners.py`): screen there, replace a
refused message with a fixed notice, and screen file parts again in
`before_model_callback` for files that reach the request from history. The supplied text workflow does not
implement those paths, production identity, distributed locking, retention
enforcement or incident response. Record these as production extensions and
scope them explicitly instead of claiming full coverage.
For tenant policy selection, retention, detector evaluation or incident recovery,
use [production-policy.md](production-policy.md).
