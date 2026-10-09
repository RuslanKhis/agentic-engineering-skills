---
goal: G05
title: DPIA input, data map and AI-disclosure text are with the DPO and legal
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: protect-adk-sensitive-data
supporting_skills: [adk-agent-security]
blocked_by: []
phase: 1
profile: production
estimate:                # human hours, agent-assisted (x1.5 ADK multiplier included)
  hands_on: 12–18
  review_and_verify: 4–6
  total: 16–24
  calendar_waits: DPIA sign-off by the DPO 4–8 weeks; legal review of AI-disclosure and AI Act classification 2–3 weeks; outcome baseline data from claims ops 1–2 weeks
owner: SEC
status: ready
---

# G05 DPIA input, data map and AI-disclosure text are with the DPO and legal

## Outcome

The DPO and legal have what they need to sign off before the pilot: data-flow map, processors (Google Cloud, Guidewire), retention table, residency, the A14 classification question and draft disclosure copy; claims ops provide the outcome baseline. D10, D14.

## Scope

- In: `docs/compliance/data-map.md`, `docs/compliance/dpia-input.md`, disclosure copy for G09; baseline data request for current FNOL information-request rate and time to photos; DORA ICT third-party register note for the risk office.
- Out: Legal conclusions (legal owns); control implementation (G11).
- Depth: Production. Floor: no real customer data in the documents.
- Route: Derived from the design's Data and authority table.
- Supporting skills: `adk-agent-security` (threat summary for the DPIA risk section)
- Execution scope: Documents only.

## Acceptance

- [ ] Data map covers every store and sink in the design, with region and retention
- [ ] DPIA input and disclosure text submitted; submission date recorded
- [ ] Baseline metrics received or the gap recorded as an open decision

Verification: Document review by the security reviewer and DPO.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G05-dpia-and-disclosure-pack.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
