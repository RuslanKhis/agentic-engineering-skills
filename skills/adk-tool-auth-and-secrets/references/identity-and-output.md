# Identity and public-output boundaries

Read for gateway/tool changes, a cross-user access report, public event translation or credential leakage. Preserve the application's identity provider and response contract unless changing them is the requested task.

## Establish ownership

Map the browser credential to a validated issuer/project, tenant where applicable and subject; derive one internal principal. Email, a supplied `user_id`, a session locator and an invocation ID do not prove identity. Verify signature, issuer, audience, expiry and required claims with the pinned provider library. Distinguish recognised invalid/revoked credentials from verifier outages; both deny access, but only the former should suggest signing in again. Configure expected Firebase project and tenant behaviour explicitly if that provider is selected.

Create and load sessions under the verified principal. An unknown or foreign session should have a non-enumerating failure. Carry the same trusted identity into the tool and credential repository. The target may use `ToolContext.session.user_id` or the pinned SDK's invocation accessor; do not introduce a version migration to change a valid accessor. If adding a server-created identity-state consistency guard, initialise it in session creation too. It is not a browser credential.

Inspect model-visible tool declarations, not just Python parameters: frameworks inject some arguments. A tool must not let model text select another user's credential or an arbitrary authenticated URL. Constrain operations/resources deterministically. Check user/tenant ownership alongside an object locator, and recheck on history, cancellation and continuation routes that exist. Retain any required write confirmation/idempotency boundary.

## Project output; do not dump events

Consume the invocation according to its completion/cancellation contract. A final response can still contain thought-marked parts; allowlist public text and exclude those parts. Do not serialise the entire event, auth configuration, state delta, function arguments/results, callback URL or request headers to create a public response. A streamed UI should use a small trusted application event schema, with correlation retained server-side.

The optional `assets/public_text.py` adapter accepts trusted ADK-like event objects and returns final text or `None` for a non-final event. It rejects malformed shapes and enforces an explicit character cap. Its async collector consumes later events too. Preserve the application's existing streaming/cancellation semantics when adapting; do not replace a streaming UI with final JSON merely because the companion used JSON.

Projection is **not secret detection**: if a credential has already entered allowlisted public text, the adapter cannot identify it. Keep credentials upstream of the model and apply the target's content policy. Tests deliberately demonstrate this limitation. The adapter is not a whole-application confidentiality guarantee.

## Protect separate logging/export boundaries

Sanitise model/provider exceptions at the point before framework logging can capture raw payloads. A generic gateway 503 may occur too late. Test both framework logs and public output with synthetic exception canaries. Preserve diagnostic codes/opaque operation correlation without copying exception bodies.

Use allowlisted audit fields under the project's privacy policy. Stable opaque user IDs are still linkable; do not claim anonymity. Configure trace export/linkage deliberately and keep high-cardinality correlation out of metric labels. For ADK 2.8.0's legacy span-content path, explicitly configure `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS=false` when content capture is prohibited; inspect other overrides/exporters too. That flag does not sanitise custom instrumentation or analytics. Treat `temp:` as a lifetime scope, not confidentiality or universal redaction.

Completion requires tests showing an owner mismatch denies before provider access, a forged tool/request identity cannot change ownership, non-public canaries do not enter public output, and relevant error/export boundaries preserve the policy. See [validation](validation.md). The historical companion does not establish full Firebase or every-exporter compliance; see [evidence](compatibility-and-evidence.md).
