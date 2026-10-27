# Design: support assistant pilot

Status: accepted 2026-10-06

## Scope gate

| Question | Answer |
| --- | --- |
| Artifact type | pilot with 40 customers for six weeks |
| People | one developer (Priya), agent-assisted |
| Stack | google-adk 2.12.0, FastAPI on Cloud Run (europe-west2) behind IAP, dev project `harbour-support-dev` |

## Contracts

| ID | From | Invariant | Scope | Authority | Enforcement | Failure outcome | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | R1 | a customer reads only their own orders and refunds | user | store | tool owner check | not found | evidenced: local, G01 |
| C2 | R2 | a conversation survives an instance restart | session | session store | DatabaseSessionService on Cloud SQL | conversation restarts | planned: G03 |
| C3 | R3 | every resource the pilot creates is deleted or retained with an owner at the end | project | teardown ticket | G06 cleanup commands, billing readback | cost keeps running | planned: G06 |

## Decisions

- D1 Sessions move from in-memory to `DatabaseSessionService` on Cloud SQL for
  PostgreSQL (a small dedicated-core instance with private IP), one
  instance in the dev project, created by script, deleted by G06.
- D2 Credentials for the database come from Secret Manager; the runtime
  service account gets `roles/cloudsql.client` on the project only.
