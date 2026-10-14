---
goal: G13
title: Customer data stays in the EU, out of logs, and is deleted on time or on request
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: protect-adk-sensitive-data
supporting_skills: [adk-memory-architecture]
blocked_by: [G03, G04, G05]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, ×1.5 for a team new to ADK
  hands_on: 24-36
  review_and_verify: 8-12
  total: 32-48
  calendar_waits: none
owner: Eng E
mentions_only: [wait]
status: blocked
---

# G13 Customer data stays in the EU, out of logs, and is deleted on time or on request

## Outcome

Implements D12 and I6: field minimisation, content kept out of logs and
telemetry, retention by lifecycle rules and a nightly purge, an erasure job by
`customer_id`, and a residency trace across every component.

## Scope

- In: data map table from the design checked against the built code;
  structured logging with IDs only; purge of sessions and drafts after 90
  days and photos 30 days after attachment, skipping rows with unresolved
  submissions; erasure job; residency trace (model endpoint, SQL, buckets,
  logs, traces, backups); evidence for the DPIA pack.
- Out: Model Armor (later list).
- Depth: production.

## Acceptance

- [ ] A test turn with a name, address and phone number leaves none of them in log or trace exports.
- [ ] Erasure for customer A removes A's sessions, drafts and photos and leaves B's; an unresolved submission delays it and is reported.
- [ ] Purge on a fixture set deletes exactly the expired rows.
- [ ] The residency trace lists every sink with its region; none is global or outside the EU.

Verification: offline tests; dev-project readback for buckets and sinks.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G13-sensitive-data-retention.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
