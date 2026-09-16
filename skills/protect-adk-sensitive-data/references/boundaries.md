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

Authenticate using existing trusted middleware. Derive tenant/user identifiers
from the verified principal, never user text, model arguments or editable
headers without verification. Bound request bytes while reading, not only after
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
side effect. Output callbacks are too late to undo a write. Use a stable
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
need equivalent boundaries when present. The supplied text workflow does not
implement those paths, production identity, distributed locking, retention
enforcement or incident response. Record these as production extensions and
scope them explicitly instead of claiming full coverage.
For tenant policy selection, retention, detector evaluation or incident recovery,
use [production-policy.md](production-policy.md).
