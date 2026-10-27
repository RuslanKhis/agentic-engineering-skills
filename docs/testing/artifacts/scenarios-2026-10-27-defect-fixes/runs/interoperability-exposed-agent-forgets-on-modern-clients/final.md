I fixed the forgetting, but none of the new code or tests has been run, because google-adk and mcp aren't installed here. The cause comes from the skill's reference notes, which describe an offline trial on your exact versions (ADK 2.12.0, mcp 2.3.0). I haven't reproduced it myself.

**Cause.** `to_mcp_server` keeps one ADK session per MCP connection. The new client, mcp 2.3's default, negotiates protocol 2026-07-28, which has no connection. Every request therefore gets a new session. The old host talks the older handshake protocol, so its calls share a connection and it works. That session map lives in each instance's memory. With two Cloud Run instances, a redeploy or a call landing on the other instance also loses it, which explains the occasional forgetting on the old host.

**Fix** (`triage/mcp_server.py`):
- The server is now hand-built. Each reply returns a `conversation_id`, which is the ADK session id, and follow-ups pass it back as an argument.
- The tool description tells the host model to do that.
- Sessions are looked up under the caller's principal. An unknown, expired or foreign id returns the same "unknown or expired" tool error.
- Sessions live in `DatabaseSessionService` when `SESSION_DB_URL` is set, so both instances share them. Without it they fall back to in-memory, which is fine for tests and local runs only.
- The server now runs with `stateless_http=True`, so any instance can serve any request.
- `deploy/service.yaml` reads `SESSION_DB_URL` from a secret named `triage-session-db-url`.

**CI check.**
- `tests/test_mcp_follow_up.py` uses a scripted model that reports how many user turns it saw. It makes the same two-call exchange with `mcp.Client(server)` (modern) and `mode="legacy"`, and asserts the second call sees two turns. It also checks that a call without an id starts a new conversation and that a bad id is refused.
- `ci.yml` sets `REQUIRE_ADK=1`, so the test fails rather than skips if the dependencies are missing.
- The test would have failed on the old code in modern mode.

**Assumptions** (nobody was there to answer, so I proceeded on these):
- Is a shared database acceptable for session state? I assumed yes. If not, the alternatives are a single instance or session affinity, which is unreliable for MCP clients.
- I assumed the secret name `triage-session-db-url` and that the URL is an async SQLAlchemy URL.
- I assumed no per-caller authentication is configured, so every caller shares one principal and the id's unguessability is the only separation.

**Not done:**
- **Test run.** The code was written from the skill's reference and my memory of the APIs. Likely failure points are the `DatabaseSessionService` constructor, the `get_access_token` import path, and `streamable_http_app` accepting `stateless_http`. The `call_tool` result fields in the tests could also be wrong.
- **Provisioning.** I did not create the database or the secret.
- **Host changes.** The old host's model must now pass `conversation_id` itself. Its implicit per-connection memory is gone.
- **Expiry.** Session retention is not enforced.
- **Conformance.** I did not run the pinned MCP conformance suite.