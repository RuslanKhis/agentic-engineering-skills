---
goal: G12
title: Customer data is screened, kept out of telemetry, held in the EU and deleted on time
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: protect-adk-sensitive-data
supporting_skills: [adk-agent-observability]
blocked_by: [G05, G16, G18]
phase: 1
profile: production
estimate:
  hands_on: 14-20
  review_and_verify: 4-7
  total: 18-27
  calendar_waits: none
owner: Eng E
status: proposed
---

# G12 Customer data is screened, kept out of telemetry, held in the EU and deleted on time

## Outcome

Implements D9 and invariant I6: screening of customer text and model
replies, content-free telemetry, retention, erasure and residency checks.
Needs G18's `degraded` answer for the fail-closed path. Retention and erasure of photos already sent to ClaimCenter are G33,
because they need G09's transfer states. Handoff: 2 h from Eng C on buckets
and infrastructure.

## Scope

- In: Model Armor calls before the model and before release of a reply
  (fail closed); logging filter and telemetry content-capture settings;
  Cloud Scheduler jobs and GCS lifecycle rules for retention; erasure
  endpoint for the DPO process; residency readback script.
- Out: threat model and adversarial cases (G14).
- Depth: production.

## Acceptance

- [ ] A1 A test run seeded with PII markers in messages and photos finds none in log output or in an in-memory trace exporter.
- [ ] A2 Model Armor in an EU region screens customer text and model replies (availability confirmed from official docs, URL and date recorded); a block verdict, a 4xx rejection (for example an oversized request) or a 403 returns the designed reply; screening unavailable, slow or out of quota fails closed for that turn and offers the prefilled form.
- [ ] A3 Sessions, drafts and photos of abandoned drafts are deleted 30 days after abandonment, sessions 30 days after filing; lifecycle and job configs are read back from staging.
- [ ] A4 An erasure request for a customer with no confirmed draft deletes their sessions, drafts and photos; an absence query confirms it and touches no other customer.
- [ ] A5 A readback shows every store, the model endpoint and screening in EU locations; no global endpoint is configured.
- [ ] A6 Customer text carrying prompt-injection patterns is flagged by screening before the model call, and the flag is recorded on the turn (photos are covered structurally by D1 and by G14).

Verification: offline for A1 and A4; authorised staging readback for A2,
A3 and A5.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G12-sensitive-data.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
