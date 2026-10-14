---
goal: G14
title: Injected text or a hostile customer cannot make the system do anything it should not
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-security
supporting_skills: [adk-agent-evaluation]
blocked_by: [G06, G08, G09]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, ×1.5 for a team new to ADK
  hands_on: 24-36
  review_and_verify: 8-12
  total: 32-48
  calendar_waits: none
owner: Eng E
status: blocked
---

# G14 Injected text or a hostile customer cannot make the system do anything it should not

## Outcome

The design's security posture made executable: `before_tool_callback`
capability checks keyed on trusted state, and an adversarial suite asserting
that forbidden actions never run, mapped to OWASP LLM IDs.

## Scope

- In: capability check on both tools (owner, draft state, field allow-list);
  cases: photo text instructing changes or submission, customer asking for
  another customer's policy, coverage or payout fishing, tampered
  `draft_version_hash`, oversized fields, emergency phrasing in the second
  language; suite in CI; findings table; 2 h handoff from Eng A and ML.
- Out: external testing (pen test after staging).
- Depth: production threat model at the design's depth.

## Acceptance

- [ ] Every case asserts the absence of the forbidden call or effect, not only the reply text.
- [ ] A scripted model emitting an out-of-scope tool argument is refused by the callback without mutation.
- [ ] The suite runs offline in CI and fails the build on any forbidden effect.
- [ ] Findings mapped to OWASP LLM IDs with owners.

Verification: offline scripted-model suite; a bounded live run of the
suite's model-dependent cases.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G14-adversarial-suite.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
