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

## Tests

```bash
python -m unittest discover -s tests -t .
```

The tests use fakes for the providers and need neither ADK nor network.
