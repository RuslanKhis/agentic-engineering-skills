# Implementation plan: claims triage assistant

Status: phase 2 complete; go-live planned 2026-11-10
Architecture: [docs/architecture/claims.md](../architecture/claims.md)

## Goals and dependencies

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | State |
| --- | --- | --- | --- | --- | --- | --- |
| G01-G06 Pilot build, journey and approval | 1 | mixed | 21-33 | none | various | done |
| G07 Usage and cost reporting | 2 | implementation | 2-3 | G06 | adk-agent-observability | done |
| G08 Production hardening (SB05, HA database, alerting) | 2 | implementation | 6-9 | G06 | deploy-adk-on-google-cloud | done |
| G09 Urgency table enforced in code | 2 | implementation | 2-3 | G06 | adk-operational-guardrails | done |
| G10 Report a problem from the draft view | 2 | implementation | 2-3 | G07 | adk-agent-observability | done |
| G11 Dublin office: Irish wordings and teams | 2 | implementation | 3-5 | G08 | adk-memory-architecture | done |
| G12 Rollout pack | 2 | presentation | 3-5 | G11 | adk-presenter | ready |
| G13 Operations handover to Fenwick IT | 2 | implementation | 3-4 | G08 | adk-agent-observability | in_progress |

## Measurement records

- M1: metric median triage time on pilot claims; value 13 minutes; baseline 21 minutes (brief §4); window 2026-09-01 to 2026-09-30; sample 1,184 pilot claims; method claims MI report; owner claims MI analyst; build v1.0.3
- M2: metric drafts accepted without change; value 71%; window 2026-10-01 to 2026-10-24; sample 980 drafts in Leeds; method decisions table; owner Larkspur Digital; build v1.2.0
- M3: metric re-routing rate after triage on pilot claims; value 8.2%; baseline 9% (brief §4); window 2026-10-01 to 2026-10-24; sample 980 pilot claims; method claims MI report; owner claims MI analyst; build v1.2.0

## Hypercare

Four weeks from go-live. Exit thresholds not yet agreed with Helen Okafor.

## Resume here

Next: G12 rollout pack; G13 in progress.
