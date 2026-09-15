# Authentication continuation ownership

Read this reference when the task adds consent UI, resumes a pending tool, uses native ADK authentication or integrates managed authentication. First identify who owns code exchange and which session/invocation is continued. Retain the target's pinned stack; use [compatibility-and-evidence.md](compatibility-and-evidence.md) before changing packages or resource formats.

## Select one contract

**Application broker.** The broker exchanges the code and stores credentials. An `authorization_required` tool result is an application status, not an ADK pause. After connection, the application may offer a fresh invocation of a saved read request. Recheck session ownership, expiry and cancellation before retrying. Finish connection according to its explicit policy without reviving an obsolete action. Side-effecting requests require their own approval/idempotency policy.

**Native ADK authentication.** Inspect the selected tool's authentication scheme and the pinned [ADK authentication contract](https://adk.dev/tools-custom/authentication/). Retain the pending `adk_request_credential` request, original function-call identifier, verified principal and owned session on the server. Validate the browser transaction before supplying the correlated response expected by ADK's credential flow. Preserve the original invocation identifier when the chosen Resume contract requires it. Let the selected owner exchange the code exactly once; a broker-exchanged code cannot be exchanged again by ADK.

**Managed authentication.** Inspect the configured provider's finalisation API and adapter response contract. Bind the pending request, consent nonce, browser, principal and function-call correlation. Finalise credentials through the selected API, verify the outcome, then submit the required correlated response. Reaching a continuation URL is not successful finalisation. Handle denial, expiry and failure explicitly, preserving an unauthenticated outcome when finalisation fails.

For Agent Identity work, consult the [migration guide](https://docs.cloud.google.com/iam/docs/migrate-to-agent-identity-api) and [three-legged OAuth flow](https://docs.cloud.google.com/iam/docs/auth-with-3lo-v2). A documentation review on 15 September 2026 found migration guidance for `/authProviders/`, updated APIs/IAM and finalisation, while an ADK example retained legacy `/connectors/`. Treat that as historical documentation evidence, not tested compatibility. Verify the target combination and migrate the whole contract together; changing a resource string alone is insufficient.

## Validate public and internal boundaries

Apply [oauth-lifecycle.md](oauth-lifecycle.md) for browser/account binding. Expose only allowlisted application status and validated navigation data. Keep credentials, callback URLs, auth configuration and complete ADK events server-side. State prefixes such as `temp:` or `secret:` are not universal confidentiality guarantees.

Complete the integration when tests prove correct correlation and actual tool execution after consent, rejection of wrong-session/replayed callbacks, no retry after cancellation, and safe denial/finalisation failure. Consume invocation events through completion and scan every enabled output/export path for canary credentials using [validation.md](validation.md). Report whether execution resumed an original invocation or started a new one, and distinguish mock tests from live-provider evidence.
