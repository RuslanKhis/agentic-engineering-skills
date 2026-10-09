---
goal: G03
title: Hand compliance a data map and DPIA input pack
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: protect-adk-sensitive-data
supporting_skills: [adk-agent-security]
blocked_by: []
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 12-22
  review_and_verify: 4-6
  total: 16-28
  calendar_waits: DPO/legal review and DPIA sign-off (4-8 weeks); start in week 1, needed before the pilot
owner: E3 with the DPO; security reviewer reviews
status: ready
---

# G03 Hand compliance a data map and DPIA input pack

## Outcome

Compliance can assess the DPIA, AI Act transparency and DORA questions from an accurate data map, and their conditions flow back into G08, G12 and G13. Implements D2, D11, I7, I9, O3, O4; A11, A13, A14.

## Scope

- In: `docs/compliance/home-claim-intake-data-map.md`: every data class from the design's data table, processors (Google Cloud, Guidewire), regions, retention, erasure path, model inputs, AI disclosure text proposal, list of questions O3/O4.
- Out: The legal assessment itself.
- Depth: Production floor: real personal data only after sign-off.
- Route: Documentation only.
- Supporting skills: `adk-agent-security` (threat summary for the DPIA risk section)
- Execution scope: Documentation authorized; sign-off is the DPO's.

## Acceptance

- [ ] Each data class lists purpose, location, retention, recipients and erasure
- [ ] Every model input (text, photos, injected policy data) is listed
- [ ] O3 and O4 have recorded answers or a dated pending status
- [ ] No real customer data in the document

Verification: Review by the security reviewer and DPO; checklist in the document.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G03-data-map-and-dpia-input.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
