# Production cost contract and BigQuery cost facts — 21 October 2026

*Cost at MVP and above is a contract with a stop, not a budget alert; and the BigQuery facts an agent application trips over.*

## Change

Follows the [resource cost floor](resource-cost-floor-2026-10-21.md) of the
same day.

- **Cost contract.** At MVP profile and above the designer writes cost as a
  contract with the six contract fields: a ceiling at a stated volume split
  into the variable per-request work and the fixed while-provisioned rows of
  the ledger; scope; the Cloud Billing export as authority; an enforcement
  stop that acts without a person (admission control and `max_llm_calls`,
  maximum bytes billed and a daily quota, maximum instances, a model-project
  quota only for a host you do not configure) beside the independent operator
  stop; what degrades first; and a goal in the first live week that reads the
  bill. A billing budget alert is evidence, never the enforcement. Every
  owned resource carries labels set in deployment code. The plan's Later
  table always holds the recurring cost review and the decommission item.
  Text in design decisions, the designer's contracts section, the depth
  table, the design and plan templates and GCP decisions; one scenario case.
- **BigQuery facts for agents**, each verified against the official page and
  written into the SQL and memory specialists: the per-user result cache and
  why reviewed templates with bound parameters hit it while generated SQL
  never does; job labels for attribution; custom project and per-user daily
  quotas; clustering order from real predicates and the recommender; the
  `MERGE` pattern for a partitioned history table; on-demand bytes versus
  edition slot-hours and which control applies under each; a bytes-versus-slots
  diagnostic row. The author's article "The $10,000 LIMIT clause" (4 August
  2026) is cited once per package as the source of the selection, with the
  facts re-verified on Google's pages and no prose reproduced.

## Automated checks

`scripts/check_repo.py` on Python 3.12: **22 packages** validate (0 errors,
0 warnings), evaluation cases are structurally valid, **695 tests** pass with
**59 optional SDK checks skipped**; `git diff --check` is clean.

## Fresh-agent trial

A subagent with a fresh context, the 22 packages readable as installed
skills, no network and nothing runnable, was asked for a one-pass production
design: a claims assistant on Cloud Run with Cloud SQL sessions, BigQuery
claim history and Sensitive Data Protection on every reply, 20,000 requests
a month, a sponsor ceiling of 1,500 dollars a month, two developers, eight
weeks, real customer data, billing export to BigQuery.

Observed: contract C8 carried all six fields. Its invariant split the ceiling
into a fixed part summed from the ledger rows the design kept (Cloud SQL with
HA, backups and IP, a Cloud Run minimum instance, Secret Manager, Artifact
Registry) and a symbolic per-request variable part. Enforcement named
`max_llm_calls`, a durable monthly admission counter refusing new sessions,
a per-customer daily allowance, maximum bytes billed with a daily quota,
Cloud Run maximum instances and an operator kill switch; the budget with its
alerts was written as "evidence that notifies after the spend, not
enforcement". Labels appeared in the contract's scope and in the deployment
goal's flags; the first-bill goal recorded a measurement; the Later table
held the monthly cost review and a decommission item that deletes the
instances, then their backups, and checks a label-filtered export the day
after. Every while-provisioned resource carried a ledger row with a price
placeholder and the creating goal's first acceptance item. Ease: **4 of 5**.

Frictions, fixed the same day: the ledger records idle cost per day while
the contract needs a month (the paragraph now says per-day times the days in
the month); whether a model-project quota is still expected on your own host
(now: the stop only for a host you do not configure, a backstop otherwise);
and "acts without a person" beside "an operator stop" (now stated as the
automatic stop plus the independent operator stop). Noted, not changed: the
schedule helper cannot run in a session without execution, which the
delivery profiles excuse only for a missing interpreter; the ledger does not
say how HA or point-in-time recovery change a Cloud SQL figure.

### Engineer: a SQL agent whose bill tripled

Fixture: a synthetic analytics agent whose tool runs model-written SQL with
no job configuration and whose instruction asks for a timestamp comment in
every query; ticket T-204 asks for a pre-execution ceiling, attribution
without personal identifiers, no double payment for repeated questions, and
a job-history diagnosis with the pricing-model statement. A fresh subagent,
no network, was asked to carry it out.

Observed: it added a dry run and an admission check that refuses an estimate
over the configured ceiling before submission, with the ceiling also set on
the job, and a test asserting the refused query produced one dry-run call
and no execution; labelled every job with agent, environment, team and an
opaque request ID, and refused an email, a user ID and a hashed email in
labels; canonicalised the SQL and removed the timestamp instruction because
the specialist says such a comment defeats the result cache, stating the
cache's conditions in the evidence; wrote the two job-history queries and
the on-demand versus reservation statement. It found every control in the
execution-safety and implementation references. Ease: **4 of 5**.

Frictions, fixed the same day: the labels paragraph forbade a caller
identifier without saying how to attribute the user (now: an opaque request
ID label joined to the audit log), and the per-user quota paragraph did not
say that one shared service account is one bucket (now it does, with the
allowance moved to admission control). Noted, not changed: no reference
states how a function tool reads the user ID from the tool context on ADK
2.8.0.

## Limits

Two trials, one design and one ticket, against synthetic projects; no live
query ran and no bill was read. The article's URL is still to be added to the
two citations.
