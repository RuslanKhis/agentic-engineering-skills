# Implementation plan: IT helpdesk runbook and ticket assistant

Status: draft; ready goals identified (G01, G04)
Architecture: [../architecture/helpdesk-assistant.md](../architecture/helpdesk-assistant.md)
Continuation source of truth: this plan; phase 1 goal scope and acceptance live in
the [tickets](../tickets/helpdesk-assistant/)

## Summary for the reader

- **Profile and phase 1:** internal tool. Phase 1 gives the 25 helpdesk agents a
  web assistant behind IAP that searches the Confluence runbook spaces and answers
  with cited pages, measured on a 15-case gold set and tried by three pilot
  colleagues. **Jira ticket creation is not in phase 1**: it is the first phase 2
  work (G03, G07).
- **Effort and finish:** 15.5–24.5 human hours against 27 h of capacity after a
  25 % reserve; finish in 7.04–10 working days of 10. Fits, at the high end with no
  slack on the calendar (schedule check below).
- **Largest risks:** (1) runbook pages restricted to subsets of staff would make the
  shared bot account over-share (open decision A5, blocks G05 go-live); (2) keyword
  CQL search may miss paraphrased questions (G02 measures it; Vertex AI Search is the
  phase 2 fallback); (3) access requests W1 take longer than 5 working days (requested
  on day 1 in G01; G05 waits on them).
- **Decisions needed from you:** confirm or move the cut line (ticketing in phase 2);
  confirm the real hours per day (A2: at 2.4 h/day each, G03 ticket drafting fits in
  phase 1); answer A5 and A10 in the design's assumed-answers table.
- **Next prompt:** `/adk-engineer Carry out docs/tickets/helpdesk-assistant/G01-runbook-search-agent.md.`
  (Dev B can start G04 in parallel.)

## Destination and constraints

Destination: the journey in the design, with tickets created on confirmation by the
end of phase 2. Non-goals: answering end users directly, editing Confluence,
assigning or transitioning Jira issues. Stack: Python, google-adk (working assumption
2.8.0, confirmed in G01), Vertex AI `gemini-3.8-flash` pinned (D6), Cloud Run with
direct IAP (D3). Repository: empty apart from skills; every module path below is
**proposed** (`app/agent.py`, `app/tools/confluence.py`, `app/api.py`,
`app/static/`, `tests/`, `eval/gold.jsonl`, `release.toml`). Authorization in this
session: design only; no cloud, IAM or Atlassian changes have been made or approved.

## Delivery profile and capacity

| Phase | Delivers | Goals | Human hours | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship | Colleagues search runbooks with their own identity; quality measured | G01, G02, G04, G05, G06 (+ wait W1) | 15.5–24.5 | 2 people × 1.8 focused h/day × 10 days = 36 h; 25 % reserve → 27 h |
| 2, harden and add tickets | Ticket drafting and confirmed creation; adversarial cases; CI eval gate | G03, G07, G08, G09 (+ wait W2) | 12–21 | When the team has time after phase 1 |

Estimates are human hours for an experienced ADK developer with a coding agent
(hands-on plus review and verify); no new-team multiplier (both engineers have
shipped ADK agents on GCP). Focused hours: A2 in the design.

| Person | Goals | Hours | Capacity after reserve |
| --- | --- | --- | --- |
| Dev A | G01, G02, G06 | 7.5–13.5 | 13.5 |
| Dev B | G04, G05 | 8–11 | 13.5 |

```yaml
- goal: W1
  phase: 1
  total: 0
  calendar_waits: Atlassian read-only bot account and token for runbook spaces; helpdesk Google group for IAP
  wait_days: 3-5
- goal: G01
  phase: 1
  hands_on: 2-4
  review: 1-2
  total: 3-6
  owner: Dev A
  blocked_by: []
- goal: G02
  phase: 1
  hands_on: 2-4
  review: 1-1
  total: 3-5
  owner: Dev A
  blocked_by: [G01]
- goal: G04
  phase: 1
  hands_on: 3-4
  review: 2-3
  total: 5-7
  owner: Dev B
  blocked_by: []
- goal: G05
  phase: 1
  hands_on: 2-3
  review: 1-1
  total: 3-4
  owner: Dev B
  blocked_by: [G01, G04, W1]
  handoff: 0.5
- goal: G06
  phase: 1
  hands_on: 1-2
  review: 0.5-0.5
  total: 1.5-2.5
  owner: Dev A
  blocked_by: [G05, G02]
  handoff: 0.5
- goal: W2
  phase: 2
  total: 0
  calendar_waits: Jira sandbox project, bot write permission and Modify reporter
  wait_days: 3-10
- goal: G03
  phase: 2
  hands_on: 1-2
  review: 1-1
  total: 2-3
  owner: Dev B
  blocked_by: [G05]
- goal: G07
  phase: 2
  hands_on: 3-5
  review: 2-3
  total: 5-8
  owner: Dev B
  blocked_by: [G03, W2]
- goal: G08
  phase: 2
  hands_on: 1-2
  review: 1-2
  total: 2-4
  owner: Dev A
  blocked_by: [G07]
  handoff: 0.5
- goal: G09
  phase: 2
  hands_on: 2-4
  review: 1-2
  total: 3-6
  owner: Dev A
  blocked_by: [G02]
```

Schedule check, run 2026-10-14 with
`python3 .claude/skills/adk-system-designer/scripts/check_schedule.py --plan docs/plans/helpdesk-assistant.md --tickets docs/tickets/helpdesk-assistant/ --days 10 --reserve 0.25 --person "Dev A=1.8" --person "Dev B=1.8"`
(Python 3.9.13 here, below the 3.11 the skill names; the script ran without error):
phase 1 is 15.5–24.5 h against 27 h, fits; longest chain at the high end
G04 → G05 → G06, 10 working days; finish 7.04–10 working days of 10, fits.

What-ifs run with the same command (one row each):

| Variant | Hours | Finish (working days) | Result |
| --- | --- | --- | --- |
| Ticket drafting G03 in phase 1 (Dev B), 20-case gold set | 18.5–28.5 | 8.52–12.22 | Low end only; Jira create already excluded |
| As above with G06 moved to Dev B, 15-case gold set | 17.5–27.5 | 8.52–12.22 | Low end only |
| G03 moved to phase 2, 20-case gold set | 16.5–25.5 | 7.04–10.74 | Hours fit, calendar low end only |
| **G03 moved to phase 2, 15-case gold set (chosen)** | 15.5–24.5 | 7.04–10 | Fits |
| First row with 2.4 focused h/day each (A2 at an 8-hour day) | 18.5–28.5 | 6.39–9.17 | Fits: G03 can return to phase 1 |

Changes after failing runs: G03 moved to phase 2 (scope cut), G02 reduced from 20 to
15 cases (simplified goal; G09 grows it). No dependency, wait or review was removed.
If time runs out early, stop after G05: a deployed, identity-scoped search tool is
useful without the measurement report, and G02/G06 follow.

## Implementation map

| Decision | Component and integration point (proposed) | GCP | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |
| D1, D2, D6, D8 | `app/agent.py` factory: `LlmAgent` + `search_runbooks`, `get_runbook_page` in `app/tools/confluence.py`; Runner with `RunConfig(max_llm_calls=8)` | Vertex AI model endpoint | `adk-memory-architecture` | ADK pin; Gemini 3.8 Flash on Vertex in region |
| D3, D7 | `app/api.py`: IAP JWT verification middleware → `user_id`; own-session endpoints; `app/static/` page with escaped rendering | Cloud Run, direct IAP | `adk-frontend-integration` | IAP JWT audience format for direct IAP |
| D4, D10, D11 | Service account, Secret Manager token, structured logging, `release.toml` | Cloud Run, Secret Manager, Logging | `deploy-adk-on-google-cloud` | Existing deployment template (A9) |
| D5 | `app/tools/jira.py`: `draft_ticket`, `create_ticket` with `require_confirmation=True` | Secret Manager | `safe-api-tool-calls` | Entity-property JQL lookup |
| D9 | Adversarial cases against the create path | — | `adk-agent-security` | — |

## Goals and dependencies

| ID and goal | Phase | Type | Hours | Depends on | Primary skill | State |
| --- | --- | --- | --- | --- | --- | --- |
| W1 Access requests (bot account, Google group) | 1 | wait | 0, 3–5 days | — | — | to request on day 1 (G01) |
| [G01 Runbook search agent, local](../tickets/helpdesk-assistant/G01-runbook-search-agent.md) | 1 | implementation | 3–6 | — | `adk-memory-architecture` | ready |
| [G02 Gold set and grounded-answer measurement](../tickets/helpdesk-assistant/G02-gold-set-measurement.md) | 1 | implementation | 3–5 | G01 | `adk-agent-evaluation` | blocked by G01 |
| [G04 Identity-bound chat API and page](../tickets/helpdesk-assistant/G04-identity-bound-chat.md) | 1 | implementation | 5–7 | — | `adk-frontend-integration` | ready |
| [G05 Deploy behind IAP with the real agent](../tickets/helpdesk-assistant/G05-deploy-behind-iap.md) | 1 | implementation | 3–4 | G01, G04, W1 | `deploy-adk-on-google-cloud` | blocked; needs cloud authorization |
| [G06 Pilot with three helpdesk agents](../tickets/helpdesk-assistant/G06-pilot.md) | 1 | implementation | 1.5–2.5 | G05, G02 | `adk-agent-evaluation` | blocked |
| G03 Ticket draft | 2 | implementation | 2–3 | G05 | `adk-tool-interface-design` | proposed |
| G07 Confirmed Jira create | 2 | implementation | 5–8 | G03, W2 | `safe-api-tool-calls` | proposed |
| G08 Adversarial cases on the write path | 2 | implementation | 2–4 | G07 | `adk-agent-security` | proposed |
| G09 Eval gate in CI and release manifest | 2 | implementation | 3–6 | G02 | `adk-release-engineering` | proposed |

### Phase 2 goals

- **G03 Ticket draft** (D5). `draft_ticket(summary, description, issue_type, priority)`
  validated in code against allow-lists; returns a draft the page shows. Supporting:
  `adk-model-and-output-contracts`, `adk-agent-instructions`. Acceptance: a missing
  required detail yields a question, not an invented value.
- **G07 Confirmed Jira create** (D5, I6). Starts with a 1-hour check that an entity
  property set at create time is searchable by JQL in the sandbox; if not, use a label.
  Supporting: `adk-tool-interface-design`, `adk-operational-guardrails`,
  `adk-tool-auth-and-secrets`, `adk-agent-security`. Acceptance: rejected confirmation
  creates nothing; a simulated timeout after Jira commits leads to lookup, not a second
  issue; a model-supplied project or assignee is refused.
- **G08 Adversarial cases** (D9). Runbook fixtures with planted instructions; a
  scripted model tries to create a ticket with exfiltrated text; assert no create
  without confirmation and the payload shown equals the payload sent.
- **G09 Eval gate in CI** (D11). Grow the gold set to 30 including ticket cases;
  CI fails below the G02 baseline; `release.toml` records model, prompt and tool-schema
  hash. Supporting: `adk-agent-evaluation`. Acceptance: a deliberately broken prompt
  fails CI.

## Later

| Item | Trigger | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| Vertex AI Search index of runbooks | G02 hit@5 below 80 % | Paraphrased questions missed | `adk-memory-architecture` |
| Per-user Confluence access (delegated OAuth) | Restricted runbook pages (A5) | None while all pages are shared | `adk-tool-auth-and-secrets` |
| Durable sessions (`DatabaseSessionService`) | Lost-conversation complaints, or more than one instance | Conversations lost on deploy | `adk-memory-architecture` |
| Content screening of tool results | Secrets found in runbooks (A7) | Hostnames reach the model | `protect-adk-sensitive-data` |
| Traces, SLOs, alerts | Second team or unattributable incident | Failures noticed by users first | `adk-agent-observability` |
| Model migration rehearsal | Shutdown date announced for the pinned model | — | `adk-release-engineering` |

## Open decisions for further planning

See the design's [open decisions](../architecture/helpdesk-assistant.md#open-decisions);
A5 blocks G05 go-live, A10 blocks G07, A2 moves the cut line.

## Resume here

- **Next goal:** G01, ready now (offline work with fixtures; a personal read token is
  enough for the live check). G04 is ready in parallel for Dev B.
- **Read first:** the design, then the G01 ticket.
- **Continuation prompt:**

```text
/adk-engineer Carry out docs/tickets/helpdesk-assistant/G01-runbook-search-agent.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

After that: `/adk-engineer Continue the next ready goal in docs/plans/helpdesk-assistant.md.`
