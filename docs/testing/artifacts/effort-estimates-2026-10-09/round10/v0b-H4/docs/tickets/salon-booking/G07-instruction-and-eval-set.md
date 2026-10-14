---
goal: G07
title: We know how often the assistant picks the right action, and it never claims a change it didn't make
design: ../../architecture/salon-booking.md
plan: ../../plans/salon-booking.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-agent-instructions]
blocked_by: [G02]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 6-9
  review_and_verify: 2-3
  total: 8-12
  calendar_waits: none
owner: Dev A
status: blocked
---

# G07 We know how often the assistant picks the right action, and it never claims a change it didn't make

## Outcome

A versioned instruction and a 30-case labelled set with a local runner, so the
pilot launches on a measured result. Covers the instruction contract in the
design and I4. Most of the hours are writing and labelling cases and reading
model output.

## Scope

- In: `prompts/booking_agent/instruction.md` (scope, missing-detail questions,
  never claim completion, 24-hour handoff, brief refusals); 30 cases in
  `evals/cases/`: book, move, cancel, ambiguous dates ("next Friday" on a
  Friday, around midnight and a DST change), unknown service, another salon,
  off-topic, "just book it without asking", other person's appointment.
  Propose-tool cases are written against the declarations in the design and
  run once G05 lands; `evals/README.md` records the latest result per case.
  One error-analysis iteration.
- Out: CI gate (G11), judge-based metrics.
- Depth: MVP Build with an evaluation set. Floor: pinned model and prompt version recorded with each run.

## Acceptance

- [ ] Rendered-request test shows the instruction, date and time zone, and no customer contact details
- [ ] Runner reports tool-selection and argument correctness per case, with failed and missing runs listed, and exits non-zero on any I4 violation
- [ ] Baseline run recorded with model ID, prompt version and eval-set hash; target proposed from it (not assumed)

Verification: deterministic checks offline; one bounded live run on Vertex AI (≤ 30 cases × 3 repeats) once G08 gives credentials — report as not run until then.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking/G07-instruction-and-eval-set.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
