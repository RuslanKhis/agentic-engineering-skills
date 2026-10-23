# Topology: where the Runner runs and who owns identity

Read when choosing or reviewing how the browser reaches the agent.

ADK's own API server is open by design. `get_fast_api_app` has no end-user
authentication hook (its `trigger_auth_verifier` guards only `/trigger/*`);
session and artifact routes take `user_id` in the path, and `/run` and
`/run_sse` take it in the body. Its docstring says any client that can reach
it can read and write sessions, memory and artifacts and run agents for any
user. It warns about this only when `bind_host` is passed and non-loopback;
a custom `get_fast_api_app()` call with the default `bind_host=None` stays
silent. ADK 2.12.0's changelog line "take the ADK user id only from an
authenticated principal" changes only the A2A request converter; it
authenticates nothing on the browser routes. This skill's runtime contracts
show an anonymous client creating and listing another user's sessions.

| Topology | Use when | Identity and routes |
| --- | --- | --- |
| **In-process Runner** (default) | One team owns the agent and the web app; a POC, internal tool or MVP | The app creates `Runner` and the session service in its lifespan; `/api` routes call `runner.run_async(user_id=principal.subject, ...)`. ADK's server is not mounted. |
| **Gateway to a private ADK service** | The agent is deployed separately (another team, another language runtime, `adk api_server` already in production) | The ADK service has internal ingress and accepts only the gateway's service identity (ID token). The gateway verifies the user, overwrites `user_id` on every upstream call and maps upstream errors to its own. |
| **Backend-for-frontend in front of Agent Runtime** | The agent runs on managed Agent Runtime | The app verifies the user, keeps its own record of which sessions each principal owns, and calls the runtime with its service identity. `adk-frontend-integration`'s managed-runtime reference has the client calls. |

In every topology:

- ADK's `/apps/…`, `/run`, `/run_sse`, `/run_live`, `/list-apps` and the
  development UI are unreachable from a browser or the internet (SB05). A
  check asserts "no ADK data, no docs UI, no schema, no model call" rather
  than "404", because `app.frontend()` answers browser navigation to unknown
  paths with the HTML shell.
- `adk web` runs only on loopback, for a builder-only demo.
- Google's samples that run ADK's server with `allow_origins="*"`, a
  hard-coded user or credentials read at import time are study material, not
  a template.
