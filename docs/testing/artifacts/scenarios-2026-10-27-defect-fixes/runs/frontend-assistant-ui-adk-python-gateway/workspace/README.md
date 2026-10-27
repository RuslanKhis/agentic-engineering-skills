# Support assistant

Customer-support assistant for Harbour Outfitters' online shop, built on
Google ADK. It answers order questions, searches the help-centre articles,
reads inbound support emails, issues refunds through the payments provider
and sends replies. Signed-in customers reach it through the web chat; the
FastAPI service runs on Cloud Run behind IAP.

## Layout

- `app/agent.py` builds the ADK agent (`build_agent()`, `root_agent`).
- `app/prompts.py` holds the instruction text.
- `app/tools/` holds the tool functions; they import nothing from ADK so the
  unit tests can load them without the SDK.
- `app/clients/` wraps the payments and mail providers.
- `app/store.py` is the SQLite store (orders, customer profiles, refunds).
- `app/auth.py` turns the IAP assertion into a `Principal`.
- `app/server.py` is the FastAPI app.

## assistant-ui gateway

The web app uses `@assistant-ui/react-google-adk` (pinned 0.0.40) against two routes:

- `POST /api/adk/sessions` creates a session owned by the verified principal.
- `POST /api/adk/run` takes the proxy body and streams filtered ADK events as SSE.

`app/gateway.py` holds the rules (tested without ADK): body validation (`stateDelta`,
`runConfig` and browser ids are refused or ignored), the public event filter (no thoughts,
state, usage or raw error text), approvals (only `adk_request_confirmation` with exactly
`{"confirmed": bool}` for a call still pending in the caller's session) and edit checkpoints
(`start` or `after:<invocation id>` resolved to `Runner.rewind_async`; refused once a refund
or email in the removed turns went through).

Known limits: sessions are in memory and the per-session lock is per process, so run one
instance until a persistent session service and shared lock are chosen; there is no history
endpoint, so a page reload starts a new conversation and drops an unanswered approval;
the old `/api/chat` route is untouched and cannot answer an approval.

## Tests

```bash
python -m unittest discover -s tests -t .
```

The tests use fakes for the providers and need neither ADK nor network.
