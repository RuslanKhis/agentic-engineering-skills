---
goal: G13
title: Payment and ID numbers never get stored, and claim data is deleted on time
design: ../../architecture/home-claim-agent.md
plan: ../../plans/home-claim-agent.md
primary_skill: protect-adk-sensitive-data
supporting_skills: [adk-agent-observability]
blocked_by: [G03, G05]
phase: 1
profile: production
estimate:                # human hours, agent-assisted (×1.5 new-to-ADK multiplier included)
  hands_on: 24-40
  review_and_verify: 10-16
  total: 34-56
  calendar_waits: none
  wait_days: 0
owner: Eng A
status: proposed
---

# G13 Payment and ID numbers never get stored, and claim data is deleted on time

## Outcome

Implements D10, I8 and I10.

## Scope

- In: SDP inspection with redaction in gateway middleware before persistence and the model (fail closed); `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS=false`; metadata-only logs; retention job; erasure endpoint for the DPO process.
- Out: Face blurring (Later); Model Armor (G32).
- Depth: Production depth. Floor: fail closed when SDP is down.

## Acceptance

- [ ] Seeded card, IBAN and national-ID strings are absent from the session DB, spans and logs
- [ ] With SDP unavailable, the message is rejected and nothing is stored
- [ ] A 31-day-old draft and its photos are deleted by the retention job
- [ ] Erasure removes sessions, draft and photos and waits for an in-flight operation

Verification: Offline with an SDP fake plus local DB; one bounded live SDP call on dev.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-agent/G13-sensitive-data.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
