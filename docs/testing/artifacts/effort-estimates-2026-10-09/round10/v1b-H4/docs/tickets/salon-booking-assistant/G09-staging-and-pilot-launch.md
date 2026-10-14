---
goal: G09
title: Staging run and pilot launch
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-agent-evaluation, adk-release-engineering]
blocked_by: [G04, G05, G06, G07, G08, W1]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 4-5
  review_and_verify: 1-2
  total: 5-7
  calendar_waits: none
owner: Dev C
status: blocked
---

# G09 Staging run and pilot launch

## Outcome

Customers of the pilot salon can book through the website, and the team can
see, stop and roll back the assistant. Implements D10 and closes phase 1.

## Scope

- In: wire the real `OperationService` into the chat API; deploy to staging
  against booking API staging; run `evals/run.py` with the pinned model
  (25 cases × 3 repeats, cost cap USD 5) and record results; staging
  checklist: happy booking, slot-taken, uncertain (fault-injected), kill
  switch within 1 minute, rollback to previous revision; create production
  (same infra scripts, production booking API key); embed the widget on the
  pilot salon page only; first-day watch of logs and alerts; start recording
  the baseline (bookings via assistant, front-desk corrections). Requires W1
  (owner approval and privacy wording) before production traffic. Includes 2 h
  handoff on the pieces from Dev A and Dev B.
- Out: move/cancel (G11), other salons (G12).
- Depth: MVP. Floor: approval before outside-visible use; kill switch tested.
- Execution scope: production deployment needs the team's explicit go-ahead at
  the time; this ticket does not grant it.

## Acceptance

- [ ] Eval run: all adversarial cases pass; booking-case pass rate recorded as
      the baseline (no threshold invented before the first measurement).
- [ ] Staging checklist passes, including rollback and kill switch.
- [ ] One real booking made by a team member at the pilot salon appears in
      the booking system and is then cancelled by staff.
- [ ] W1 approval and privacy wording recorded (who, date).

Verification: authorised live on staging, then production for the pilot salon;
evidence recorded here.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G09-staging-and-pilot-launch.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
