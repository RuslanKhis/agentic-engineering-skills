# Refund assistant

Harbour Outfitters' refund assistant on Google ADK 2.12.0. Customers reach it through the web
chat; requests pass through Agent Gateway (`deploy/agent-gateway.yaml`) to the FastAPI service on
Cloud Run. `issue_refund` posts to the payments provider's refund API with the operation ID as
its idempotency key; each attempt is recorded in `refund_operations` (`app/operations.py`).

Launch review is in two weeks.

## Tests

```bash
python -m unittest discover -s tests -t .
```

The tests use fakes for the payments provider. google-adk is not installed in this
environment, and there is no network or cloud access.
