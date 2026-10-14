---
goal: G08
title: Confirming the summary files exactly one claim and shows its number
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-operational-guardrails]
blocked_by: [G04, G34]
phase: 1
profile: production
estimate:
  hands_on: 26-38
  review_and_verify: 9-13
  total: 35-51
  calendar_waits: none
owner: Eng B
status: proposed
---

# G08 Confirming the summary files exactly one claim and shows its number

## Outcome

The customer's confirmation of draft version *n* becomes a durable submission
operation that a worker drives to a ClaimCenter claim number, safely under
retries, restarts, duplicates and lost responses. Implements D7, D8 and
invariants I2–I4. Uses the Guidewire adapter from G34 (handoff: 2 h from
Eng D).

## Scope

- In: `POST /v1/drafts/{id}/confirm` (`version`, `summary_hash`),
  `GET /v1/drafts/{id}/status`, `app/submission/` (operation table unique on
  draft and version, canonical payload hash, state machine, fencing version),
  Cloud Tasks named tasks per step, a sweeper for stale operations. Draft
  locked on confirm.
- Route: the API commits the operation, then enqueues, then answers 202.
  The worker re-checks the policy, then creates, then submits. SDK retries
  off; the operation owns retry and the 24 h deadline before `needs_ops`.
- Out: the HTTP adapter itself (G34), photos (G09), UI (G11), alerts (G17),
  live verification (G25).
- Depth: production; tested against the G01 fake.

## Acceptance

- [ ] A1 Confirming version *n* commits the operation row and the draft lock in one transaction before the 202; the worker files the claim; status shows the claim number.
- [ ] A2 If the draft changed after the summary was rendered, confirm of *n* returns 409 and the new summary; no operation is created.
- [ ] A3 Two confirms of the same version (double click, two tabs) produce one operation and one claim.
- [ ] A4 The fake commits the create and drops the response; the retry uses the same dedup key or finds the claim by our reference; exactly one claim exists.
- [ ] A5 Draft claim created but submit fails with 5xx or times out: operation stays `draft_created`, retries with backoff, after the deadline becomes `needs_ops`; the customer sees "received, number follows".
- [ ] A6 A 4xx validation rejection makes the operation `failed_correctable` with the field named; no retry loop.
- [ ] A7 Policy ownership and in-force status are re-checked immediately before create; a policy cancelled after confirm yields no claim and the designed message.
- [ ] A8 Two workers or a restarted worker on the same operation: the fencing version lets only one create; one claim.
- [ ] A9 429 from Guidewire is retried after Retry-After within the operation deadline; total attempts counted once across layers.
- [ ] A10 A 401 refreshes the client token once; a refresh failure keeps the operation pending and alerts.
- [ ] A11 A success response without a claim number is treated as unknown and reconciled by lookup, never as failed.
- [ ] A12 Enqueue fails, is denied (403) or its acknowledgement is lost after the commit: the sweeper re-enqueues operations pending over 2 minutes; the named task prevents a duplicate dispatch.

- [ ] A13 The worker route accepts only Cloud Tasks requests whose OIDC token is from the queue's service account; any other caller gets 403 and nothing runs.
- [ ] A14 `update_claim_draft` on a confirmed (locked) draft returns an error and changes nothing.

Verification: offline and local integration — `pytest tests/submission`
with the G01 fake fault switches, a Postgres container and a Cloud Tasks
stand-in; worker restart test.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G08-claim-filing.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
