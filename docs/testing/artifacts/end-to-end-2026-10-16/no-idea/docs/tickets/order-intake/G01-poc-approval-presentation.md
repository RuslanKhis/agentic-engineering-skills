---
goal: G01
title: The CEO decides on the proof of concept from a deck built from the record
design: ../../architecture/order-intake.md
plan: ../../plans/order-intake.md
primary_skill: adk-presenter
supporting_skills: []
blocked_by: []
contracts: []
phase: 1
profile: proof of concept
estimate:
  hands_on: 2-3
  review_and_verify: 1
  total: 3-4
  calendar_waits: decision on 5 Nov 2026
owner: operations director (presents), contractor (drafts)
status: ready
---

# G01 Proof-of-concept approval presentation (business)

## Outcome
A 15-minute business deck, memo and pre-wiring for the owner-CEO on 5 Nov 2026, built from the brief, design and plan (D1 to D6).

## Acceptance
- [ ] A1 `check_deck.py` exits 0
- [ ] A2 every number cites the brief or the plan
- [ ] A3 cost slide states the assumed USD 300 ceiling and what is unmeasured

Verification: offline, the deck check from the project root.

## Run this ticket
```text
/adk-presenter Prepare the proof-of-concept approval presentation for a business audience from docs/discovery/order-intake.md, docs/architecture/order-intake.md and docs/plans/order-intake.md (goal G01).
```
