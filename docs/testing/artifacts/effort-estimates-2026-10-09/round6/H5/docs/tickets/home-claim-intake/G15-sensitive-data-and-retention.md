---
goal: G15
title: Keep personal data minimal, out of telemetry and deleted on time
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: protect-adk-sensitive-data
supporting_skills: [adk-agent-observability]
blocked_by: [G02, G07, G09]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 14-23
  review_and_verify: 5-8
  total: 19-31
  calendar_waits: none
  wait_days: 0
owner: Dev E
status: blocked
---

# G15 Keep personal data minimal, out of telemetry and deleted on time

## Outcome

The model sees only what intake needs, screening runs at ingress, logs hold no content, retention jobs delete on schedule. Implements D8, D14, I6; route and rationale in the [plan](../../plans/home-claim-intake.md), entry for this goal ID.

## Scope

- In: Context projection, screening adapter (Model Armor or SDP per G02), log filters, retention jobs.
- Out: Telemetry pipeline (G19).
- Depth: Production.

## Acceptance

- [ ] A captured model request holds no customer name, email or bank details.
- [ ] Logs hold IDs, no message text; screening unavailable leads to fail-closed rejection.
- [ ] Retention jobs delete seeded expired drafts, sessions and photos, and nothing else.

Verification: Offline; live screening check in staging during G18.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G15-sensitive-data-and-retention.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
