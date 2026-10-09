---
goal: G03
title: "DPO and legal have signed off what data we process, where, and for how long"
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: protect-adk-sensitive-data
supporting_skills: []
blocked_by: []
phase: 1
profile: production
estimate:                # human hours, agent-assisted, x1.5 included
  hands_on: 16-24
  review_and_verify: 2-4
  total: 18-28
  calendar_waits: DPO DPIA sign-off and legal AI Act opinion
  wait_days: 15-25
owner: Security eng
status: ready
---

# G03 DPO and legal have signed off what data we process, where, and for how long

## Outcome

A signed DPIA, the AI Act classification and transparency text, retention periods and the processor list (Vertex AI, Model Armor, Guidewire) that G14 and G23 depend on. Implements D10, A9, A11, O4, O5; route and rationale in the
[plan entry](../../plans/home-claim-intake.md#g03--dpo-and-legal-have-signed-off-what-data-we-process-where-and-for-how-long).

## Scope

- In: Data-flow map from the design; DPIA draft; transparency notice text; retention table; DORA ICT register entry request.
- Out: Implementing retention (G14).
- Depth: Build: required before real customer data (pilot).

## Acceptance

- [ ] DPIA signed by the DPO with retention periods and legal basis recorded.
- [ ] Legal opinion records AI Act classification and the customer-facing AI notice text.
- [ ] Every data sink in the design's data table has an approved region and retention.

Verification: Document review; no code. Execution scope: People work only.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G03-dpia-and-compliance-decisions.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
