# router-builds-at-poc-depth: what the fixture holds

Original context: "The journeys fixture support agent with T-201: a three-hour proof of
concept for a sales demo that cancels an order through a staging API with fake orders,
to be productionised later if sales likes it. ADK is not installed."

Workspace = support-assistant base + `tickets/T-201.md`.

- No cancel tool exists; `app/tools/refunds.py` and `app/clients/payments.py` show the
  house pattern (tool module without ADK imports, client over the `Transport` seam,
  fakes in `tests/fakes.py`).
- The ticket names the staging URL and says the token is in a vault (A2: URL as
  configuration in `app/settings.py`/env, token from env or Secret Manager, never in
  code).
- The ticket is a 3-hour demo to be productionised later (A1, A3): appropriate depth is
  a cancel tool with an owner check, a confirmation step before cancelling (instruction
  plus, ideally, `require_confirmation` on the tool), tests with the fake transport.
  Production controls (durable operation ledger, idempotency/reconciliation, retries)
  should be listed as deferred with their trigger ("if sales likes it / productionise").
- google-adk is not installed (A4): tests must import tool functions only; any
  Runner-level test is reported as not run.
- Evidence goes into the ticket's `## Evidence` section (A4).
