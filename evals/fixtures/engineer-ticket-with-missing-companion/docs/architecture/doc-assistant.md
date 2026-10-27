# Design: doc assistant

Status: accepted 2026-10-16
Plan: [docs/plans/doc-assistant.md](../plans/doc-assistant.md)

Internal assistant for Nordlicht Insurance staff that answers from the policy library,
web chat on the designer's web defaults (FastAPI with the Runner in process, Vite React
SPA with shadcn and react-router, IAP). Profile: proof of concept.

## Contracts

| ID | From | Invariant | Scope | Authority | Enforcement (and recheck at the effect) | Failure outcome | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | R1 | every answer cites a policy ID and section, or says nothing was found | turn | agent | instruction plus citation check | "no policy found" | evidenced: local, G01/A1 |
| C2 | R2 | a stream ends with completed or failed | turn | runner | SSE adapter | failed event | evidenced: local, G02/A1 |
| C3 | R2 | partial text is never shown as final | turn | browser | UI state | failed badge | planned: ui test, local |
| C4 | R3 | only signed-in staff reach /api | request | IAP | verified-principal dependency | 401 | evidenced: local, G01/A2 |

## Security baseline

| Rule | Component | Depth now | Proved by (G/A), n/a: reason, or deferred: trigger |
| --- | --- | --- | --- |
| SB01 | /api routes | Build | G01/A2 |
| SB10 | Browser app | Build | G03/A3 |
