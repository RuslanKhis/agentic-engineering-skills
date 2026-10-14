---
goal: G22
title: Invited customers file real claims, and handlers confirm the claims are good
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-agent-observability, adk-release-engineering]
blocked_by: [W6, G18, G19, G24]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, ×1.5 for a team new to ADK
  hands_on: 30-45
  review_and_verify: 6-10
  total: 36-55
  calendar_waits: pilot runs with invited customers
owner: Eng A
status: blocked
---

# G22 Invited customers file real claims, and handlers confirm the claims are good

## Outcome

Production deployment opened to an invite list (e.g. 2,000 policyholders)
for the pilot period after the DPIA is signed; handlers review every pilot
claim; the hypothesis in the design is measured against the form baseline
(O6). Runs in parallel with the external test if O3 is accepted.

## Scope

- In: production release through the pipeline with an allow-list; handler
  review form (complete, corrected, wrong); daily review of failures and
  cost; exit report with completion rate, call-back rate, correction rate,
  coverage-promise count, tokens per claim; go or no-go recommendation; 2 h
  handoff from Eng D and ML.
- Out: GA traffic.
- Depth: production; real personal data under the signed DPIA only.

## Acceptance

- [ ] Every pilot claim reviewed by a handler; correction rate reported against the baseline.
- [ ] Zero coverage or payout promises in pilot transcripts.
- [ ] Zero duplicate claims; every `UNCERTAIN` row resolved.
- [ ] Exit report with a go or no-go and the thresholds for GA.

Verification: production evidence from the pilot, reviewed by claims
operations and the product owner.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G22-invite-only-pilot.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
