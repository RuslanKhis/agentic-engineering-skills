# Design

| ID | From | Invariant | Scope | Authority | Enforcement (and recheck at the effect) | Failure outcome | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | R1 | a user reads only their own preference | user | profile store | API dependency | 404 | planned: owner test, local |
| C2 | R1 | forget removes the preference before the next session | user | profile store | delete route | error shown | planned: forget test, local |
| C3 | R2 | a stream ends with completed, failed or interrupted | session | runner | SSE adapter | interrupted state | planned: stream test, local |
| C4 | R3 | spend stops at the daily cap | project | quota | quota | refusal | deferred: pilot |
| C5 | R2 | partial text is never shown as final | session | runner | UI state | failed badge | planned: ui test, local |

| Rule | Component | Depth now | Proved by (G/A), n/a: reason, or deferred: trigger |
| --- | --- | --- | --- |
| SB01 | /api routes | Build | G01/A2 |
| SB05 | ADK runtime | Defer | deferred: pilot |
