# Support assistant

Harbour Outfitters' support assistant, built on Google ADK 2.8.0. Launch is planned for
next month. The agent works the shared support inbox: it reads inbound customer emails
(`fetch_email`), searches the help-centre articles and community answers (`search_docs`),
looks up orders and customer contact details, issues refunds through the payments provider
(`issue_refund`), replies by email (`send_email`) and notes what it did on the ticket.

Screening: the Model Armor plugin in `app/plugins/screening.py` screens each user message
before the model sees it (template in europe-west4).

## Layout

- `app/agent.py` builds the agent and the `App` with its plugins.
- `app/prompts.py` holds the instruction text.
- `app/tools/` holds the eight tool functions; they import nothing from ADK.
- `app/clients/` wraps the payments and mail providers.
- `app/store.py` is the SQLite store.

## Tests

```bash
python -m unittest discover -s tests -t .
```

The tests use fakes for the providers. google-adk is not installed in this environment and
there are no model credentials, so nothing here runs the agent itself.
