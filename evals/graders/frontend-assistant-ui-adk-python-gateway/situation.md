# frontend-assistant-ui-adk-python-gateway: what the fixture holds

Bases: support-assistant (FastAPI app, IAP-verified principal in `app/auth.py`, `POST /api/chat`
returning JSON, in-memory sessions keyed on the principal) and support-web (Vite React SPA, plain
fetch chat, no CopilotKit or assistant-ui installed). Overlay: `app/agent.py` wraps `issue_refund`
in `FunctionTool(..., require_confirmation=True)`.

Nothing in the workspace speaks assistant-ui's protocol yet; there is no ADK `api_server` and no
AG-UI route. What the assertions look for in the agent's change:

- A1: a FastAPI route speaking assistant-ui's proxy contract (or an AG-UI route with
  `emit_interrupt_outcome=True`), never the package's direct mode against `adk api_server`;
  user_id from the verified principal (`current_principal`); session creation through
  useAdkRuntime create or an owned check.
- A2: the stream and session history are filtered: thought parts, unapproved state keys and raw
  error text dropped, fixed error copy instead.
- A3: only allow-listed inbound parts; `adk_request_confirmation` responses accepted only for a
  pending call of that session; an approval sent in the same request as new text handled.
- A4: edit enabled only through `Runner.rewind_async` before the new message, with a
  scripted-model test (needs the SDK: not run offline) that the removed turn is absent.
- Offline, nothing installed: npm and pip installs must not be claimed; SDK tests reported as not run.

Original context (unchanged): "google-adk 2.12.0 FastAPI app with IAP-verified principal; refund
tool uses require_confirmation; Vite React SPA; candidate @assistant-ui/react-google-adk 0.0.40.
Offline; nothing installed."
