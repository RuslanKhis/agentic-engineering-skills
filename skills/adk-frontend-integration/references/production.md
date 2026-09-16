# Production extensions

Read only the sections relevant to the requested product. These are explicit production principles, not claims that the teaching application implements them. Turn each required guarantee into a target-specific implementation and an observable acceptance test. An audit may conclude that a capability is out of scope without building it.

## Persistence and readiness

When conversation continuity is required, choose a session service supported by the pinned SDK and the target deployment. In-memory history belongs to one process; persistence and protection against concurrent writers are separate decisions. Keep conversation history, long-term memory and retrieval knowledge separate, with explicit ownership, retention and deletion policies for each store.

Implement and verify the storage boundary in this order:

1. Inspect the existing schema/version and migration mechanism. Prepare the required schema before admitting traffic; coordinate migration ownership instead of letting every serving worker race to migrate. Follow the task's approval boundary before changing an external database.
2. Construct session and network resources in worker lifespan, after any fork. Close partially initialised resources on startup failure and close owned clients on shutdown using the installed SDK's lifecycle.
3. Make readiness reflect the dependencies required to accept a conversation. A fixed health response proves process liveness only. Use bounded, non-mutating dependency checks; routine health probes should not invoke the model or a business tool.
4. Create and continue a synthetic conversation, stop the original serving process, then resume the same owned conversation from a fresh process without browser history replay. Confirm that another user cannot retrieve it and that unavailable or incompatible storage prevents readiness or admission under the declared policy.

Acceptance: the restart test retrieves stored history, rejected ownership checks invoke no model/tool, and the storage-failure path settles within its budget. The historical companion demonstrated remote-session recall after a local gateway restart; it did not establish local database migration, readiness or production retention guarantees. Add shared writer admission from the section below when more than one process can write.

## Identity and conversation access

Reuse the application's identity provider and verified session. Validate signatures, issuer, audience, expiry and subject before mapping claims to an application user. With several issuers, include the issuer in the identity mapping. Keep trusted user/tenant context separate from browser state and model-selected arguments.

Check the pinned provider's identity length, encoding and character constraints before forwarding the mapped ID. Use a stable internal ID with a persisted unique mapping from the verified issuer/subject and required tenant scope. Preserve distinctions between identities: truncating or normalising subjects merely to fit a provider field can merge callers. A deterministic digest requires an unambiguous input encoding and an explicit collision policy; it is not a substitute for verifying the claims.

Keep application thread IDs separate from provider resource IDs where their creation rules differ. A string safe to interpolate into a path is not necessarily a valid caller-selected provider session ID. Either validate the provider's actual creation constraints or persist an owned mapping between the application thread, exact remote resource and provider-generated session ID. Introducing that mapping also requires the matching browser/BFF create/resume contract. Test long identities, equal subjects from different issuers, and application-valid IDs rejected by provider creation rules. The companion's exercised browser UUIDs do not certify every string accepted by its application regex.

Apply ownership to create/resume, history, state, reconnect, rename, archive, delete and stop operations. Use the same safe not-found response where distinguishing absent and other-user conversations would leak information. A BFF needs access control for its own storage as well as Python's session access control.

Keep the gateway's workload identity separate from its verified end-user assertion. Strip incoming headers that only the trusted proxy may assert; verify signed assertions for the intended recipient. Cookie-authenticated requests need the project's CSRF protection. CORS only controls browser access, and same-origin routing is not authentication.

Enforce tool authorisation inside deterministic code. Scope database queries or external API operations to trusted tenant/account context. The model may choose a tool and propose arguments, but it does not decide permissions. Reject browser tool definitions that shadow trusted backend tools by name.

Acceptance: two synthetic users cannot access or execute each other's conversations or tools through any supported endpoint, and rejection invokes neither model nor side-effect adapter. Live identity-provider verification remains a separate test.

## Input and public output

Validate byte limits at the server edge as well as parsed message counts, text lengths, tool/state schemas and supported request forms. For a one-way new-turn bridge, require the intended fresh user turn; reject unsupported tool-result continuation, browser-defined tools, resume payloads or writable auth state rather than silently selecting an earlier user message.

Define a public author policy and tool success/error envelopes. Exclude hidden thought content. Consume through terminal outcome; an earlier answer is not ordinary success after a later run failure. If partial success is a product feature, give it a separate typed outcome. Validate public state values and JSON Patch operations in addition to key names.

Return fixed safe error copy, a controlled code and an opaque reference when needed. Logs and traces require an independent allowlist. Do not record prompts, credentials, raw exception strings, customer identifiers or tool payloads by default. Disabling message-content capture does not automatically redact application logs. A UUID alone does not configure distributed tracing; propagation, exporter configuration and shutdown flushing require their own integration.

Acceptance: malformed/oversized input is rejected before invocation; wrong-author/thought/private state is absent from browser output; late errors preserve failure; a synthetic private string is absent from public responses and default diagnostics.

## Deadlines and unknown outcomes

Place admission/lock waiting inside the overall request budget. Bound transport calls, retries, worker queues and stream output. Cancellation propagates, but a cancelled await or browser connection does not prove an external operation stopped.

For mutating tools, bind a stable operation key to trusted user, operation and canonical payload fingerprint. Claim it durably and atomically; repeated identical requests return the recorded result, in-progress or unresolved state. Reusing the key for different input fails. Keep the same key during recovery instead of generating a fresh one after timeout.

Commit a database mutation and its outcome record in one transaction where possible. For external effects use provider idempotency, or an outbox plus duplicate-safe delivery and reconciliation. Writing a response cache only after a separate effect leaves a crash window. A browser `Set` is not durable protection.

Retry only a transient failure of an operation whose repetition is safe, under bounded attempts and time. Status lookup or attachment to existing output must not call the agent again. UI controls should expose unresolved/in-progress state instead of making a potentially duplicated business action look like an ordinary retry.

Acceptance: a synthetic external effect occurs once across a timed-out client, duplicate request and process restart; conflicting input under the same key is rejected. Mocked effects establish application policy, not the live provider's idempotency implementation.

## Multiple writers and resource lifetime

Use shared per-conversation admission when several replicas can write. A process-local lock is insufficient. A lease needs an owner, expiry/renewal, ownership-checked release and storage-enforced fencing so a stale worker cannot commit after losing ownership.

Admission must atomically record a durable unsettled run. Keep that gate closed until bounded reconciliation confirms settlement, including when reconciliation fails or is cancelled. Lease expiry or merely withholding lease release cannot safely admit a new writer while old remote work remains unresolved. Fencing protects only writes at boundaries that enforce it; external effects still need idempotency.

Own the lease while consuming **and closing** the event stream. Returning an HTTP streaming response does not mean execution has finished. Create loop-bound SDK clients in application lifespan, retain their owning client and close partial initialisation failures. Follow the installed SDK's supported shutdown methods.

Prefer async network APIs. For unavoidable synchronous calls, use bounded workers and transport deadlines; retain a capacity slot until the underlying call actually finishes even if its awaiting request is cancelled. CPU-heavy tasks may require a separate process. An unbounded executor moves rather than removes the capacity problem.

Acceptance: different replicas cannot overlap writes; a worker resuming after lease loss cannot commit; unresolved work blocks fresh admission after lease expiry; disconnects release local resources only after bounded closure/reconciliation.

## Replay, browser tools and human approval

SSE framing supplies no durable replay. Add a retained run record, stable event IDs, monotonic sequence, authenticated attach endpoint, retention bound and expired-cursor policy before promising reconnect. Preserve identities across delivery attempts and make the browser reducer tolerate repeated events. Give tool calls and result messages distinct IDs; require exact correlation for parallel tools.

Reconnection attaches to the recorded run instead of submitting its user message again. A browser tool result or approval signal requires an authenticated authorised decision, a matching waiting run/call, a persisted continuation state and a duplicate-safe resume operation. A UI confirmation is not itself permission to perform a backend action.

Acceptance: replaying a retained tool result does not execute the tool or add a duplicate card; another user cannot attach or approve; expired/reused decisions fail safely. These services are not bundled with the skill.

## Evidence and scope

The skill supplies an implementation workflow and offline diagnostic helpers, not a certified production framework. Report each required control as implemented/tested, existing/verified, or remaining. Preserve the user's scope: a simple JSON integration does not automatically require a replay service or a new identity platform.
