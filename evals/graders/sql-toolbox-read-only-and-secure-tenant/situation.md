# sql-toolbox-read-only-and-secure-tenant: what the fixture holds

Base: sql-agent. Overlay:

- `tools.yaml`: BigQuery source `fernhill-bq` with no `readOnly`/`writeMode`/`allowedDatasets`
  (A1: set `readOnly: true` — writeMode blocked — and allowedDatasets; the lock is Toolbox's
  dry-run statement-type check, not the prompt or a SELECT string check); a free-form
  `bigquery-execute-sql` tool `execute-sql` in the portal toolset (A2: remove or justify, citing
  its page's developer-assistant note); `customer-revenue` (`bigquery-sql`) with the table name
  as a `templateParameter` (A2: basic parameter or allowedValues-bound) and `tenant_id` an
  ordinary model-visible parameter (A3: bind it as a secure/bound parameter in code from the
  verified assertion, strip it from the model-facing declaration, test that a model-supplied
  tenant_id returns a tool error).
- `analytics/portal_agent.py`: instruction tells the model to read the account ID from the
  customer's message and to fall back to execute-sql.
- `portal/identity.py`: base64-decodes the IAP assertion payload without verifying the signature
  or audience (A4: hand assertion verification to adk-tool-auth-and-secrets). `portal/server.py`
  puts `customer_id` in session state but nothing binds it to the tool.
- `docs/tickets/G03.md`: the ticket; `docs/architecture/portal.md` leaves C1/C2 enforcement "to be
  decided in G03"; `docs/plans/portal.md`. `pyproject.toml` pins toolbox-adk 0.5.2.
- No Toolbox double exists yet; A4 expects CTE-DELETE, writing-UDF and COMMIT-chaining fixtures
  as fail-closed negative cases against a double, live Toolbox steps reported as not run.
- toolbox-adk and google-adk not installed; `tests/` (base) passes offline.

Original context (unchanged).
