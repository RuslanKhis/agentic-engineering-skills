# Implementation plan: HR assistant pilot

Status: in progress
Architecture: [docs/architecture/hr-assistant.md](../architecture/hr-assistant.md)

## Goals and dependencies

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | State |
| --- | --- | --- | --- | --- | --- | --- |
| G01 Policy answers in French and English | 1 | implementation | 5-7 | none | adk-memory-architecture | verified_local |
| G02 Own leave requests | 1 | implementation | 3-5 | none | adk-tool-auth-and-secrets | verified_local |
| G03 Routine approval rule and manager routing | 1 | implementation | 4-6 | G02 | adk-operational-guardrails | verified_local |
| G04 Pilot journey | 1 | journey | 3-4 | G01, G03 | adk-agent-evaluation | verified_local |
| G05 Governance papers | 1 | governance | 5-7 | G04 | adk-governance-pack | ready (drafted, not sent) |
| G06 Pilot approval (decision 2026-11-24) | 1 | governance | to estimate | G05, W2, W3, W4, W5, W6 | none yet | blocked |

## Calendar waits

- W1: UKG integration user, granted 2026-09-29.
- W2: review of the governance pack by Érable's counsel (Me Geneviève Roy), requested the day the drafts are sent; needed before 2026-11-24.
- W3: Quebec privacy impact assessment (EFVP, s 3.3) by Érable, with the person in charge (Marie-Claude Gagnon); needed before the pilot starts.
- W4: Quebec s 17 assessments and written agreements for each flow leaving Quebec (Toronto hosting, US model processing, Sydney log access); needed before pilot data flows.
- W5: Montréal union (Teamsters local) notice or consultation, only if counsel finds the collective agreement or law requires it; needed before the pilot starts.
- W6: update of Érable's Ontario electronic monitoring policy for prompt logging tied to employee IDs, only if counsel finds it required; needed before the pilot starts.

## Measurement records

- M1: metric policy answers citing the right section; value 92%; window 2026-10-05 to 2026-10-16; sample 300 questions (150 French, 150 English); method offline evaluation; owner Southgate Labs; build v0.5.0
- M2: metric share of pilot-shape leave requests the rule approves without review; value 64%; window 2026-10-05 to 2026-10-16; sample 500 requests replayed from July 2026; method replay; owner Southgate Labs; build v0.5.0
- M3: metric dates and leave type extracted correctly; value 98.4%; window 2026-10-05 to 2026-10-16; sample 500; method replay; owner Southgate Labs; build v0.5.0

## G05 evidence

Drafted, not sent: `docs/governance/hr-assistant/` (regulatory memo, privacy impact input pack, transfer assessment annex, impact assessment, system card, security questionnaire). Regimes in scope: Australia (consultancy's own handling), Canada (Quebec, Ontario). Checker result and open gaps: see the closing summary of the drafting session; the drafts go to Me Geneviève Roy when the owner sends them.

## Resume here

Next: G05 Governance papers.
