---
goal: G13
title: No personal content in telemetry, timely deletion, and a reply release check
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: protect-adk-sensitive-data
supporting_skills: [adk-agent-security]
blocked_by: [G06, G03]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 22-38
  review_and_verify: 18-32
  total: 40-70
  calendar_waits: DPIA conditions from G03
owner: E3; security reviewer reviews
status: blocked
---

# G13 No personal content in telemetry, timely deletion, and a reply release check

## Outcome

Logs and traces hold no conversation or photo content, our copies are deleted on schedule or on request, and replies promising cover are replaced before display. Implements D11, I5, I7, I9.

## Scope

- In: ADK telemetry content capture off; log filter; reply release check (deterministic phrase rules + Model Armor if G02 confirms EU availability; defined outcome when unavailable); retention job; erasure endpoint waiting for terminal operations; residency config check in CI.
- Out: Face redaction unless O4 requires it.
- Depth: Build.
- Route: Release check in the chat endpoint after the Runner finishes; retention as a Cloud Run job.
- Supporting skills: `adk-agent-security` (release-check bypass cases)
- Execution scope: Local.

## Acceptance

- [ ] Exporter and log capture tests show no message text, photo bytes or names
- [ ] A reply 'you are covered for €5,000' is replaced by the neutral template and counted
- [ ] Retention job with an injected clock deletes session, draft, photos at day 31 and not day 29
- [ ] Erasure during a pending operation waits, then deletes our copy

Verification: Offline tests; local integration for the retention job.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G13-sensitive-data-and-release-check.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
