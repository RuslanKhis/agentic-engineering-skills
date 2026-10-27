<!--
Where end-user identity comes from in an ADK application. Reconciled
2026-10-27: ADK 2.12.0's "take the ADK user id only from an authenticated
principal" (d0c4060) changes the A2A request converter only (read in the
2.12.0 wheel, a2a/converters/request_converter.py); several skills had
described it as protecting the HTTP endpoints. Edit here, then run
scripts/sync_shared.py.
carriers: adk-tool-auth-and-secrets, adk-fastapi-backend, adk-agent-security, adk-frontend-integration, adk-memory-architecture, deploy-adk-on-google-cloud, protect-adk-sensitive-data, adk-agent-interoperability, safe-api-tool-calls
-->

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
