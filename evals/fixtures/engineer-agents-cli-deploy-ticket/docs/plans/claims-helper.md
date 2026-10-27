# Implementation plan: claims helper

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | State / blocker |
| --- | --- | --- | --- | --- | --- | --- |
| G01 Scaffold with Agents CLI | 1 | implementation | 1-2 | none | adk-engineer | done |
| G02 Read-only claim tools | 1 | implementation | 2-3 | G01 | adk-tool-interface-design | done |
| G03 Cited answers | 1 | implementation | 1-2 | G02 | adk-agent-instructions | done |
| G04 Telemetry without content | 1 | implementation | 1 | G01 | adk-agent-observability | done |
| G05 Phase-1 review | 1 | presentation | 2 | G02-G04 | adk-presenter | done |
| [G06 Agent Runtime for the pilot](../tickets/G06.md) | 2 | implementation | 3-5 | G05 | deploy-adk-on-google-cloud | ready |

Execution scope for phase 2: no cloud mutation without Tomás's approval of the exact command.
