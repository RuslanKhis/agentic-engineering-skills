# Implementation plan: IT helpdesk runbook and ticket assistant

Status: draft, ready goals identified (G01, G03 can start today)
Architecture: [docs/architecture/helpdesk-assistant.md](../architecture/helpdesk-assistant.md)
Continuation source of truth: this plan; phase 1 goal detail lives in the
tickets under [docs/tickets/helpdesk-assistant/](../tickets/helpdesk-assistant/).

## Summary for the reader

- **Profile and phase 1:** Internal tool for the 25 helpdesk staff. Phase 1
  puts a hosted, IAP-protected assistant in their hands. It answers from the
  allow-listed Confluence runbooks with cited pages and drafts a Jira ticket
  that the user copies into Jira. Its search quality is measured on 20 real
  helpdesk questions.
- **Effort and finish:** 17–24 human hours against 27 h of capacity after the
  25% reserve. Finish in 6.7–9.6 of 10 working days. **Fits** (schedule check
  run 2026-10-14, below).
- **Cut line:** the full request, where the assistant creates the ticket
  through the Jira API after a click, does **not** fit at the high end
  (finish 8.2–12.6 days). Creating tickets through the API is **G06**, the
  first phase 2 goal. If G01–G04 run at the low end (Dev A has ≥3 h left
  after G05), G06 can start in week 2.
- **Largest risks:** (1) Atlassian bot account and permissions arrive late
  (W1); this blocks hosting (G04) and measurement (G05), so request it today.
  (2) Keyword search misses runbooks (G05 measures it; G09 is the fix).
  (3) Restricted pages leak to all 25 users if the bot can see more than a
  helpdesk member can. Mitigation: D6 group membership plus the G05
  restricted-page check.
- **Decisions needed from you:** confirm or move the cut line. Alternatives
  checked: +3 working days, or 4 h/day of real half-time (see what-ifs).
  Also accept or reject O1–O3 and confirm A2, A4–A6 in the design.
- **Next prompt:** `/adk-engineer Carry out G01 from docs/plans/helpdesk-assistant.md.`

## Destination and constraints

Destination: the design's journey (search, cite, create a ticket after a
click) for the helpdesk group, on Cloud Run behind IAP. Accepted stack:
none accepted yet. The proposals are Python, `google-adk==2.8.0` (working
assumption, confirmed in G01), `gemini-3.8-flash` on Vertex AI (D8), the
prompt as a versioned file. A goal that changes the model, prompt or pin is a
release. Authorization: design only. The goals here authorize local work;
G04 needs the user to name the GCP project and approve its IAM and IAP
changes. The repository is empty, so all paths are **proposed**:
`helpdesk_assistant/agent.py`, `tools/confluence.py`, `tools/drafts.py`,
`web/app.py`, `web/static/`, `tests/`, `eval/gold.jsonl`.

## Delivery profile and capacity

Profile: internal tool (design, Delivery constraints). Capacity is 2 people
× 10 working days × 1.8 focused h/day (6 h × 0.5 time × 0.6 focus, A2), with
25% held back. That leaves 13.5 h per person and 27 h in total. Estimates are
for experienced ADK and GCP developers, so no multiplier is applied.

| Phase | Delivers | Goals | Human hours, agent-assisted | Capacity |
| --- | --- | --- | --- | --- |
| 1, ship | Hosted cited search plus ticket drafts, measured | G01–G05 (+W1, W2) | 17–24 | 27 h after reserve |
| 2, harden | Jira creation, persistence, real reporter, CI gate | G06–G11 | 29–53 (hand sum, unscheduled) | when the team has time |

| Person | Goals | Hours | Capacity |
| --- | --- | --- | --- |
| Dev A | G01, G02, G05 | 8–11 | 13.5 |
| Dev B | G03, G04 | 9–13 | 13.5 |

```yaml
- goal: W1
  phase: 1
  total: 0
  calendar_waits: Atlassian bot account, token, group and project permissions
  wait_days: 2-5
- goal: W2
  phase: 1
  total: 0
  calendar_waits: helpdesk lead writes 20 gold questions
  wait_days: 3-5
- goal: G01
  phase: 1
  hands_on: 2-3
  review: 1-1
  total: 3-4
  owner: Dev A
  blocked_by: []
- goal: G02
  phase: 1
  hands_on: 1-2
  review: 1-1
  total: 2-3
  owner: Dev A
  blocked_by: [G01]
- goal: G03
  phase: 1
  hands_on: 3-4
  review: 2-3
  total: 5-7
  owner: Dev B
  blocked_by: []
- goal: G04
  phase: 1
  hands_on: 3-4
  review: 1-2
  total: 4-6
  owner: Dev B
  blocked_by: [G01, G02, G03, W1]
- goal: G05
  phase: 1
  hands_on: 2-3
  review: 1-1
  total: 3-4
  owner: Dev A
  blocked_by: [G01, W1, W2]
- goal: G06
  phase: 2
  hands_on: 3-5
  review: 2-3
  total: 5-8
  owner: Dev A
  blocked_by: [G02, G04]
```

**Day 1 actions (not goals):** request W1 from the Atlassian admin. The bot
needs read access to the runbook spaces through a group matching the helpdesk
read set, plus create permission in `ITHD` so G06 isn't waiting later. Ask the
helpdesk lead for W2: 20 real questions, each with its expected runbook page.

Schedule check, run 2026-10-14:
`python3.12 .claude/skills/adk-system-designer/scripts/check_schedule.py --plan docs/plans/helpdesk-assistant.md --tickets docs/tickets/helpdesk-assistant/ --days 10 --reserve 0.25 --person "Dev A=1.8" --person "Dev B=1.8"`
gives 17–24 h of 27 h, fits. Dev A 8–11 h and Dev B 9–13 h, each of 13.5 h.
The longest chain is G01 → G02 → G04, 6.67–9.63 working days, which fits the
10 available.

What-ifs (same command, scope or flags varied):

| Variant | Finish (working days) | Result |
| --- | --- | --- |
| Full request in phase 1 (G02 creates through the API, 4–7 h) | 8.15–12.59 | Low end only; Dev A 10–15 h of 13.5 |
| Full request, measurement (G05) moved to phase 2 | 8.15–12.59 | Low end only; the chain doesn't change |
| Full request, deploy without the Jira path, then a 1.5–2 h hosted-enable goal | 8.52–12.59 | Low end only (G03 → G04 → enable chain) |
| **Chosen:** ticket drafts in phase 1, API creation in G06 | 6.67–9.63 | Fits |
| Full request with 13 working days | 8.15–12.59 | Fits |
| Full request with both engineers at 2.4 h/day (4 h × 0.6) | 6.11–9.44 | Fits |
| Full request with only Dev A at 2.4 h/day | 6.85–10.56 | Low end only |

Changed after the failing run: G02's scope was cut to drafts, and the Jira
write moved to G06 with its own hours. No dependency, wait or review was
shortened. If time runs out early, the goals stay useful in this order: G01
(local cited search), G03 + G04 (hosted for the team), G05 (measured), G02
(drafts).

## Implementation map

| Decision | Component and integration point (proposed) | GCP | Primary skill | Still to verify |
| --- | --- | --- | --- | --- |
| D1, D2, D3 | `LlmAgent` in `agent.py`; `search_runbooks` and `read_runbook` in `tools/confluence.py`; space list from config | Vertex AI | `adk-tool-interface-design` | ADK 2.8.0 signatures; CQL `space in (...)` syntax |
| D4 | `draft_jira_ticket` writes to the owner-keyed draft store in `tools/drafts.py`; user ID from `ToolContext` (trusted Runner value) | — | `adk-tool-interface-design` | That `ToolContext` exposes `user_id` on the pin |
| D4, D4a | Commit service plus `POST /drafts/{id}/commit` (G06) | — | `safe-api-tool-calls` | JQL label lookup latency |
| D5, D9 | `web/app.py` FastAPI: IAP JWT middleware → Runner; escaped rendering | IAP | `adk-frontend-integration` | IAP JWT audience format for direct Cloud Run IAP |
| D6, D7, D8, D10 | Cloud Run service with `max-instances=1`; runtime service account; Secret Manager; structured logs | Cloud Run, Secret Manager, Billing | `deploy-adk-on-google-cloud` | Vertex price; region availability of 3.8-flash |

## Goals and dependencies

| ID and goal | Phase | Type | Hours | Depends on | Primary skill | State |
| --- | --- | --- | --- | --- | --- | --- |
| [G01 Cited runbook search, local](../tickets/helpdesk-assistant/G01-runbook-search-agent.md) | 1 | impl | 3–4 | — | `adk-tool-interface-design` | ready |
| [G02 Ticket drafts](../tickets/helpdesk-assistant/G02-ticket-drafts.md) | 1 | impl | 2–3 | G01 | `adk-tool-interface-design` | proposed |
| [G03 Authenticated chat page](../tickets/helpdesk-assistant/G03-authenticated-chat-page.md) | 1 | impl | 5–7 | — | `adk-frontend-integration` | ready |
| [G04 Hosted for the helpdesk group](../tickets/helpdesk-assistant/G04-cloud-run-behind-iap.md) | 1 | impl | 4–6 | G01–G03, W1 | `deploy-adk-on-google-cloud` | blocked (W1, GCP project named) |
| [G05 Gold-set measurement](../tickets/helpdesk-assistant/G05-gold-set-measurement.md) | 1 | impl + evidence | 3–4 | G01, W1, W2 | `adk-agent-evaluation` | blocked (W1, W2) |
| G06–G11 | 2 | see below | 29–53 | — | — | proposed |

### Phase 2 (outline; phase 1 results will change these)

- **G06 Create the Jira issue on click.** Commit service and endpoint (D4,
  D4a), with owner check, project and type validation, label lookup, no
  automatic retry, and "uncertain" state. 5–8 h, Dev A, after G02 and G04.
  Primary `safe-api-tool-calls`; supporting `adk-agent-security`,
  `adk-frontend-integration`. Acceptance: a fake-Jira double commit makes one
  create call; a timeout shows "uncertain"; another user's draft returns 404;
  a scripted model plus an injected runbook makes zero create calls; one live
  issue lands in `ITHD` with the label.
- **G07 Persistent sessions and drafts** (`DatabaseSessionService`, Cloud SQL
  or Firestore drafts), allowing more than one instance. 4–6 h.
  `adk-memory-architecture`. Acceptance: a chat and a pending draft survive a
  revision restart and stay owner-scoped.
- **G08 Real reporter and per-user authority.** Find the Jira accountId by
  verified email and set the reporter, or use Atlassian OAuth 3LO per user.
  8–16 h plus an Atlassian admin app approval wait. `adk-tool-auth-and-secrets`.
  Acceptance: the reporter is the clicking user; a restricted page isn't
  returned to a non-member.
- **G09 Semantic retrieval** (only if G05 hit@5 is below 80%): a Vertex AI
  Search index over the allow-listed spaces. 6–12 h. `adk-memory-architecture`.
  Acceptance: G05 hit@5 improves on the same gold set and no new space appears.
- **G10 Evaluation gate in CI and a release manifest** (model, prompt hash,
  pin, eval-set hash; model-retirement calendar). 3–6 h.
  `adk-release-engineering`. Acceptance: CI fails on a gold-set regression.
- **G11 Traces and token cost per turn**, plus a weekly-active-users view.
  3–5 h. `adk-agent-observability`. Acceptance: one span per agent, tool and
  model call, carrying the session ID, with content capture off.

## Later

| Item | Trigger | Risk accepted while it waits | Likely skill |
| --- | --- | --- | --- |
| SDP or Model Armor screening of answers | A secret or PII reported in an answer | Entitled readers see secrets already in runbooks | `protect-adk-sensitive-data` |
| Per-user daily allowance | Spend above A3 or abuse | One user can spend up to 10 calls per turn without limit | `adk-operational-guardrails` |
| Adversarial suite, SLOs and alerts, canary | Audience beyond the helpdesk, or an incident | Slower detection | `adk-agent-security`, `adk-agent-observability` |
| Reader/writer split | Automatic ticket creation without a click | — (no write tool in the model today) | `adk-agent-security` |
| Update or close tickets; JSM customer portal | Helpdesk asks for it | — | `safe-api-tool-calls` |

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| The design | Decisions, invariants, assumptions |
| `eval/results.md` (G05) | hit@5, cited-answer rate, latency on the gold set |
| This plan | Cut line, remaining goals, deferred controls |

## Open decisions for further planning

See the design's open decisions O1–O5 and assumed answers A1–A10. Of these,
only W1/O4 block phase 1 goals (G04, G05). The cut line itself needs a
decision from the user.

## Resume here

- **Next goal:** G01, cited runbook search, local. It has no prerequisites.
  G03 can run in parallel for Dev B.
- **Read first:** the design, then this plan, then the G01 ticket.
- **Next action:** pin `google-adk`, confirm the `LlmAgent`, `Runner` and
  `RunConfig` signatures, then write fake Confluence fixtures.

```text
/adk-engineer Carry out G01 from docs/plans/helpdesk-assistant.md.
```

After that goal: `/adk-engineer Continue the next ready goal in docs/plans/helpdesk-assistant.md.`
