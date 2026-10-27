# Implementation plan: staff HR assistant pilot

Status: in progress
Architecture: [docs/architecture/hr-assistant.md](../architecture/hr-assistant.md)

## Goals and dependencies

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | State |
| --- | --- | --- | --- | --- | --- | --- |
| G01 Own leave, roster and policy answers | 1 | implementation | 5-7 | none | adk-memory-architecture | verified_local |
| G02 Scoped Workday reads for staff and managers | 1 | implementation | 5-8 | none | adk-tool-auth-and-secrets | verified_local |
| G03 Manager attendance summary | 1 | implementation | 3-5 | G02 | adk-model-and-output-contracts | verified_local |
| G04 Log masking | 1 | implementation | 2-4 | G01 | protect-adk-sensitive-data | in_progress |
| G05 Pilot journey | 1 | journey | 3-4 | G03, G04, W2, W3, W4, W5, W6 | adk-agent-evaluation | planned |
| G06 Governance papers | 1 | governance | 4-6 | G04 | adk-governance-pack | ready |

## Calendar waits

- W1: Workday integration user with read-only scope, requested from the HRIS team
  2026-09-25; granted 2026-10-08.
- W2: security review by Daniel Okoro before the pilot.
- W3: NSW workplace surveillance notice to pilot staff, at least 14 days before prompt logging
  starts for them, if counsel confirms prompt logging is computer surveillance; owner Wattle & Co.
- W4: consultation with SDA delegates under the enterprise agreement, if counsel confirms the
  assistant is major workplace change; owner Wattle & Co.
- W5: privacy policy and staff notice update (APP 5, and APP 1.8 before 10 December 2026) by the
  Privacy Officer, Grace Nguyen.
- W6: Wattle & Co counsel review of the governance papers; requested the day the drafts go out.

## Measurement records

- M1: metric correct leave balances on test questions; value 97%; window 2026-10-12 to 2026-10-16; sample 240 questions; method comparison with Workday; owner Southgate Labs; build v0.4.1
- M2: metric sensitive phrases masked in logged prompts; value 82%; window 2026-10-12 to 2026-10-16; sample 150 synthetic prompts with union and medical phrases; method masking test set; owner Southgate Labs; build v0.4.1 (missed: "my delegate", "SDA meeting", "physio", "IVF appointment" and similar)
- M3: metric attendance summaries matching Workday records; value 95%; window 2026-10-12 to 2026-10-16; sample 60 summaries; method manual comparison; owner Southgate Labs; build v0.4.1

## Resume here

Next: G06 Governance papers (drafted, not sent; drafts in docs/governance/hr-assistant/, checker not run
because no shell was available), then G04.
