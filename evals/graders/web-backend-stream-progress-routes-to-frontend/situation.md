# web-backend-stream-progress-routes-to-frontend: what the fixture holds

Bases: support-assistant and support-web. Overlay switches identity to an Identity Platform ID
token sent as `Authorization: Bearer` (`app/auth.py`, `app/server.py` `_verify`,
`web/src/auth.ts`, `web/src/api.ts`, firebase in `web/package.json`, `tests/test_auth.py`).

- `app/server.py`: `POST /api/chat` runs the Runner and returns one JSON body
  (`{"session_id", "reply"}`) after the run; it keeps only final-response text, so tool calls are
  invisible and partial text is lost if the run raises (A2's starting point).
- `web/src/api.ts`: `fetch("/api/chat")` with the bearer token, no user ID sent;
  `web/src/chat/ChatPanel.tsx` replaces a failed request with a canned "Sorry, something went
  wrong" message, dropping any text (A2: keep the text when a run error follows it and mark the
  turn failed).
- `web/src/chat/Message.tsx`: states streaming/completed/failed with a Failed badge.
- `docs/design/DESIGN.md`: tokens and the rule that every state is said in words.
- Identity: bearer ID token (`app/auth.py`). Native EventSource cannot send an Authorization
  header, so A3 expects the stream read with fetch plus the bearer token, and no user ID from the
  browser.
- A1: the request is about the stream contract and UI states, so adk-frontend-integration should
  lead (agent-ui-states reference), not adk-fastapi-backend.

Original context (unchanged): "An ADK web app with a FastAPI backend and a Vite React SPA themed
from docs/design/DESIGN.md; the agent route returns JSON today."
