---
goal: G14
title: "Personal data stays in the EU, out of telemetry, and is deleted on schedule"
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: protect-adk-sensitive-data
supporting_skills: [adk-agent-observability]
blocked_by: [G04]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, x1.5 included
  hands_on: 14-20
  review_and_verify: 6-9
  total: 20-29
  calendar_waits: none
  wait_days: 0
owner: Security eng
status: blocked
---

# G14 Personal data stays in the EU, out of telemetry, and is deleted on schedule

## Outcome

Content capture off, log filters, Model Armor on customer text, retention and erasure jobs with configurable periods (values from G03). Implements D10, I6, O4, O6; route and rationale in the
[plan entry](../../plans/home-claim-intake.md#g14--personal-data-stays-in-the-eu-out-of-telemetry-and-is-deleted-on-schedule).

## Scope

- In: Telemetry gates; log redaction; retention job for sessions, drafts and photos; erasure endpoint for the DPO process; Model Armor fail mode.
- Out: DPIA itself (G03).
- Depth: Build.

## Acceptance

- [ ] Exporter test shows spans with IDs and no prompt, response or image content.
- [ ] Retention job deletes expired transcripts, drafts and photos and leaves the operation audit row minimised.
- [ ] Model Armor outage produces the agreed outcome.

Verification: Offline and dev integration tests. Execution scope: Dev only.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G14-sensitive-data-boundaries-and-retention.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
