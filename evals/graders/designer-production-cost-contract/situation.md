# designer-production-cost-contract: what the fixture holds

Base claims-docs; overlay makes it a completed proof of concept:
- `docs/plans/claims.md`: profile proof of concept, every goal G01-G06 done, an evidence summary
  with actual hours, M1 (median triage 13.5 min vs 21 min baseline, 62 claims) and M2 (PoC model
  and BigQuery spend £38.20 for one week, from the billing report). Cloud SQL
  `fm-claims-pilot-sql` is recorded as retained with its cleanup command. The Later list has a
  recurring cost review and a decommission item, but there is no cost contract anywhere.
- `docs/architecture/claims.md`: contracts C1-C5 evidenced locally; C5 is "model and BigQuery spend
  stop at the daily cap" enforced by a Vertex AI quota and maximum bytes billed, configuration only.
  No labels are mentioned on any resource; no billing budget exists.

Nothing in the workspace states how the sponsor's ceiling would be enforced (as the context says).

Assertion map: A1 a cost contract with six fields: ceiling at 20,000 requests a month split into
variable per-request work and fixed while-provisioned resources (Cloud SQL, any min instances),
scope, the Cloud Billing export as authority, an automatic stop (admission control and
max_llm_calls; maximum bytes billed and a daily BigQuery quota; Cloud Run max instances), what
degrades first, and the goal that reads the first live bill. A2 a budget alert called evidence,
not the cap. A3 environment, team and application labels on every owned resource, set in
deployment code. A4 recurring cost review with a date trigger and a decommission item (dependants
and retention) in Later; each while-provisioned resource listed with idle cost and owner on the
goal that creates it. A5 design only: no provisioning, no budget creation, no prices claimed as
looked up live (prices quoted from memory must be labelled as such or left as placeholders).
