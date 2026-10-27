# Claims agent

Kestrel Mutual's claims-intake agent on Google ADK 2.12.0. Partner systems call it over A2A:
`claims/server.py` serves the agent with `to_a2a` and mounts it under `/a2a/claims` in the
FastAPI app. It runs on Cloud Run with IAM-only ingress (callers need `roles/run.invoker`
and send a Google-signed ID token).

Tools (`claims/tools/`):

- `read_document(document_id)` reads a document the claimant uploaded (PDF text).
- `file_payout(claim_id, amount_cents, payee_account)` files a payout; it asks for
  confirmation (`require_confirmation=True`).
- `send_email(to, subject, body)` emails the claimant or an adjuster.

## Tests

```bash
python -m unittest discover -s tests -t .
```

`tests/test_injection.py` runs the agent through the real Runner with a scripted model and checks
that a document carrying instructions does not lead to a payout. google-adk is not installed in
this environment, so those tests skip here; CI installs the pinned dependencies. CI has no model
credentials.
