---
goal: G10
title: Confirmed drafts become exactly one ClaimCenter claim
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: [G01, G05, G06]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 28-50
  review_and_verify: 22-40
  total: 50-90
  calendar_waits: Guidewire sandbox from G01
owner: E1
status: blocked
---

# G10 Confirmed drafts become exactly one ClaimCenter claim

## Outcome

When the customer confirms version v of the summary, the API creates one FNOL with a receipt, and duplicates, timeouts and restarts cannot create a second one. Implements D3, D7, D8, I2, I3, I4.

## Scope

- In: Submit endpoint binding `draft_id`, version and payload hash; policy re-read; operation table (unique `draft_id`); canonical FNOL payload per the G01 mapping; Guidewire adapter with token from Secret Manager; error classification; bounded retry for safe errors; `uncertain` state; status endpoint.
- Out: Attachments and the reconciler job (G11).
- Depth: Build: full replay contract. Floor: never redispatch an uncertain create without lookup.
- Route: Ordinary service module `guidewire/` and `ops/`; no ADK tool exposes it.
- Supporting skills: `adk-tool-auth-and-secrets` (Guidewire client credentials via Secret Manager and workload identity)
- Execution scope: Local; sandbox calls with the G01 test client.

## Acceptance

- [ ] Confirmed draft creates one claim and the UI status endpoint returns its number
- [ ] Double submit and a retry after timeout-after-commit yield one claim (fake Guidewire counts creates)
- [ ] Stale draft version returns 409 and nothing is sent
- [ ] No route lets the agent or a tool call the adapter (static test)

Verification: Offline with fault-injecting fake Guidewire; bounded live: 5 sandbox creates.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G10-idempotent-claim-submission.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
