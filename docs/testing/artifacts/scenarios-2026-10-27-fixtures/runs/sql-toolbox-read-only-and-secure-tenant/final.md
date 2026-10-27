I've made the G03 changes, but none of them has been run. I had no shell in this session, so the test command (`python -m unittest discover -s tests -t .`) is untested and the acceptance boxes in the ticket are still unticked.

**What changed**
- **Caller identity (`portal/identity.py`):** the server used to decode the IAP assertion without checking it, so anyone could forge an email and see another customer's figures. It now verifies the signature, expiry, audience and issuer, and refuses the request if anything is missing or wrong. It needs `IAP_AUDIENCE` set. `portal/server.py` returns 401 when verification fails.
- **Customer ID (`analytics/portal_agent.py`, new `portal/tenant.py`):**
  - The agent is now built per request, and the verified customer's ID is passed to the Toolbox client as a bound parameter, so the model never sees or sets it.
  - The instruction no longer tells the model to read the ID from the message.
  - A callback refuses any tool other than `customer-revenue`, and any call that carries `tenant_id`.
- **Read-only warehouse (`tools.yaml`):**
  - The source is `readOnly: true` with `allowedDatasets: [sales]`.
  - The free-form `execute-sql` tool is removed.
  - The `table` template parameter only accepts `invoices_summary` or `credit_summary`.
- **Tests and ticket:** `tests/test_portal_tenant_and_readonly.py` uses a Toolbox double and covers A1, A2, A3, forged assertions and the `tools.yaml` settings. The ticket's Evidence section is filled in.

**Assumptions**
- `toolbox-adk` is pinned at 0.5.2 and pins can't change in a feature change. So I used a client-side bound parameter instead of Toolbox's `secure: true`, which the skill notes need `toolbox-adk` 1.4.0 or later. The server therefore doesn't enforce the tenant rule itself. Moving to `secure: true` would be a separate ticket.
- I took the parameter and flag names (`bound_params`, `allowedValues` on a template parameter, the `allowedDatasets` format `sales`) from the skill notes. The packages aren't installed, so these are unconfirmed.
- The `tools.yaml` SQL text is unchanged, but AGENTS.md requires finance review for templates. Someone should confirm whether this file counts.
- I didn't change `analytics/agent.py` or `analytics/author.py`.

**Not done**
- Running the tests. The yaml tests skip if PyYAML is missing.
- Any check against a real Toolbox, BigQuery or IAP. In particular, whether a `SELECT` that calls a writing function (for example `SELECT purge_inactive_records();`) is refused. The double can't show that.
- Checking that the `portal-toolbox` service account holds only Job User and Data Viewer on `sales`, and setting `IAP_AUDIENCE`.
- The design table rows for C1 and C2 in `docs/architecture/portal.md` still say "to be decided".

**Question for you:** would you accept the `toolbox-adk` pin change so the server enforces the tenant? I carried on with the pin unchanged.