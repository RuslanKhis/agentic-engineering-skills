# Implementation plan: IT helpdesk runbook and ticket assistant

Status: draft. Ready goals are identified; nothing is implemented.
Architecture: [../architecture/helpdesk-assistant.md](../architecture/helpdesk-assistant.md)
Continuation source of truth: this plan. Tickets for phase 1 are under
[../tickets/helpdesk-assistant/](../tickets/helpdesk-assistant/).

## Summary for the reader

- **Profile and phase 1:** internal tool. Phase 1 delivers a Cloud Run service
  behind IAP that the helpdesk pilot group can use. It searches the IT runbook
  spaces with cited answers and creates `ITHELP` tickets only after the staff
  member confirms them. It ends with a walkthrough by the helpdesk lead (G05).
- **Effort and finish:** phase 1 is 14 to 23 human hours, against 27 hours of
  capacity after a 25% reserve. The finish range is 5.9 to 9.6 of the 10 working
  days. **Fits**, with a thin margin on Dev A's chain G01 → G03 → G05. All figures
  come from `check_schedule.py`, run on 2026-10-14.
- **Largest risks:**
  1. Confluence keyword search quality, measured in G01; the fallback is G10.
  2. A late Atlassian bot account or sandbox (wait W1), which blocks only G05.
     G02 requests it on day 1.
  3. Dev A has 0.5 hours of slack at the high end. If G01 runs high by day 4,
     G05 moves to Dev B with 0.5 hours added for the handoff.
- **Decisions needed from you:** the assumed answers A1 to A14 in the design,
  especially A4, A6 and A8. Confirm the cut line below, or choose one of the
  alternatives that keep durable proposals in phase 1.
- **Next prompt:** `/adk-engineer Carry out docs/tickets/helpdesk-assistant/G01-runbook-search-agent.md. Read its design and plan, use its primary and supporting skills, run its verification locally, fill in the Evidence section and set status. Leave changes uncommitted.`

## Destination and constraints

The destination is the journey in the design, used daily by the 25 helpdesk
staff. Non-goals:

- Jira search, update or comment.
- Access for other IT teams or end users.
- A document index.

The stack is a proposal: Python, `google-adk==2.8.0`, Vertex AI
`gemini-3.5-flash`, Cloud Run, IAP and Secret Manager (D2, D7). No repository
code exists yet; every path below is a **proposed** layout. G01 confirms the
ADK pin and model ID before writing code.

This session authorizes design only. Implementing the goals is authorized
separately by running their prompts. Cloud changes (deploy, IAP, IAM, secrets,
quota) in G04 and G05 need the user's explicit go-ahead for the named project.

Proposed layout:

- `app/agent.py`: `App` and `LlmAgent`.
- `app/tools/confluence.py` and `app/tools/tickets.py`.
- `app/server.py`: FastAPI, IAP middleware and the confirm endpoint.
- `app/static/index.html`
- `tests/`
- `eval/gold.jsonl`

## Delivery profile and capacity

Capacity is 2 people × 10 days × 6 hours × 0.5 time × 0.6 focus = 1.8 focused
hours a day each, which is 36 hours in total. The 25% reserve leaves 27 hours.
Estimates assume senior engineers experienced with ADK and GCP working with a
coding agent, so no novice multiplier applies.

| Phase | Delivers | Goals | Human hours | Capacity |
| --- | --- | --- | --- | --- |
| 1, ship | Pilot group uses it with their own identity on real runbooks and the Jira sandbox, then `ITHELP` | G01–G05, W1 | 14–23 | 27 after reserve |
| 2, harden | All 25 users; durable proposals; attribution; evaluation gate; retrieval decision | G06–G10 | 16–29 | When time allows, about weeks 3 to 5 |

| Person | Phase 1 goals | Hours | Their capacity |
| --- | --- | --- | --- |
| Dev A | G01, G03, G05 | 8–13 | 13.5 |
| Dev B | G02, G04 | 6–10 | 13.5 |

Schedule block. This is the single source of each estimate; the tickets copy it.

```yaml
- goal: W1
  phase: 1
  total: 0
  owner: ""
  blocked_by: []
  calendar_waits: Atlassian bot accounts (Confluence read, Jira create) and Jira sandbox project, requested in G02 first step
  wait_days: 1-3
- goal: G01
  phase: 1
  hands_on: 2-3
  review: 1-2
  total: 3-5
  owner: Dev A
  blocked_by: []
  calendar_waits: helpdesk lead supplies ~20 gold questions (needed by day 3)
  wait_days: 0
- goal: G02
  phase: 1
  hands_on: 2-3
  review: 1-2
  total: 3-5
  owner: Dev B
  blocked_by: []
  calendar_waits: none
  wait_days: 0
- goal: G03
  phase: 1
  hands_on: 2-3
  review: 1-2
  total: 3-5
  owner: Dev A
  blocked_by: [G01]
  calendar_waits: none
  wait_days: 0
- goal: G04
  phase: 1
  hands_on: 2-3
  review: 1-2
  total: 3-5
  owner: Dev B
  blocked_by: []
  calendar_waits: none
  wait_days: 0
- goal: G05
  phase: 1
  hands_on: 1-2
  review: 1
  total: 2-3
  owner: Dev A
  blocked_by: [W1, G02, G03, G04]
  calendar_waits: helpdesk lead available for a 1-hour walkthrough
  wait_days: 0
- goal: G06
  phase: 2
  total: 3-5
  owner: TBD
  blocked_by: [G05]
- goal: G07
  phase: 2
  total: 4-7
  owner: TBD
  blocked_by: [G05]
- goal: G08
  phase: 2
  total: 2-4
  owner: TBD
  blocked_by: [G05]
- goal: G09
  phase: 2
  total: 4-7
  owner: TBD
  blocked_by: [G05]
- goal: G10
  phase: 2
  total: 3-6
  owner: TBD
  blocked_by: [G01]
```

Schedule check, run on 2026-10-14 with Python 3.11:

```text
python3.11 .claude/skills/adk-system-designer/scripts/check_schedule.py --plan docs/plans/helpdesk-assistant.md \
  --tickets docs/tickets/helpdesk-assistant/ --days 10 --reserve 0.25 --person "Dev A=1.8" --person "Dev B=1.8"
```

Result: 14 to 23 hours; fits capacity (27 hours). The longest chain at the high
end is G01 → G03 → G05, 9.63 days. The finish range is 5.93 to 9.63 working days,
which fits the calendar. The run exited with status 0, and the tickets match the
plan.

**Changes after failing runs:**

| Run | Result | Change made, and why it is true of the work |
| --- | --- | --- |
| 1 | Finish 8.41–11.11 days, calendar low end only | A separate 1-hour "G00 access request" goal was being scheduled after other work. In reality it is a 15-minute request on day 1, so it was folded into G02's first step. The 1–3 day wait is kept unchanged as W1. |
| 2 | Finish 6.67–10.37 days, still low end only | The durable operation record and automatic reconciliation went beyond the internal-tool depth, which asks only for confirmation of writes. They moved to G07, and G02 dropped from 4–6 to 3–5 hours. A duplicate `ITHELP` ticket can be closed, and I4 still holds within one instance. |

**What-ifs that would keep the durable record (G07's core) in phase 1**, each
run with the helper on run 2's plan:

| Remedy | Finish |
| --- | --- |
| 12 working days instead of 10 | 6.67–10.37 days; fits |
| Dev B gives 2.3 focused hours a day instead of 1.8 | 5.93–9.63 days; fits |

**If time runs out early:** each completed goal is still useful in this order.

1. G01: a local search assistant.
2. G02: a tested confirm path.
3. G04: hosting.
4. G03: the page.
5. G05: the pilot.

## Implementation map

| Decision | Component and integration point (proposed) | GCP | Primary skill | Still to verify |
| --- | --- | --- | --- | --- |
| D1, D3 | `app/tools/confluence.py`: `search_runbooks` and `get_runbook`, with the space allowlist in code | Secret Manager (bot A token) | adk-tool-interface-design | CQL `siteSearch` behaviour and v2 page body format on the tenant |
| D2, D8 | `app/agent.py` `App`; `RunConfig(max_llm_calls=8)` passed by `app/server.py` | Vertex AI; quota and budget | adk-workflow-design | The ADK 2.8.0 pin and `gemini-3.5-flash` availability in the region |
| D4, I3, I4 | `app/tools/tickets.py`: `propose_ticket` and the proposal registry; `POST /api/proposals/{id}/confirm` in `app/server.py` | Secret Manager (bot B token) | safe-api-tool-calls | Jira required fields; whether label search is immediately consistent |
| D6, I1, I2 | `app/server.py` IAP JWT middleware deriving `user_id`; `app/static/index.html` | IAP | adk-frontend-integration | IAP audience string for Cloud Run |
| D7, D9 | `Dockerfile`; Cloud Run service at `max-instances=1`; JSON logs | Cloud Run, IAM, Logging | deploy-adk-on-google-cloud | The existing project's region and policies |

## Goals and dependencies

| ID and goal | Phase | Type | Hours | Depends on | Primary skill | State |
| --- | --- | --- | --- | --- | --- | --- |
| G01 Runbook search agent with gold-set measurement | 1 | implementation | 3–5 | — | adk-tool-interface-design | ready |
| G02 Ticket proposal and confirmed creation (offline) | 1 | implementation | 3–5 | — | safe-api-tool-calls | ready (final fields after A8) |
| G03 IAP-authenticated page and session ownership | 1 | implementation | 3–5 | G01 | adk-frontend-integration | ready after G01 |
| G04 Cloud Run behind IAP with secrets, logs and spend stop | 1 | implementation | 3–5 | — | deploy-adk-on-google-cloud | ready in design; cloud changes need go-ahead |
| G05 Integrated deployment, live checks and lead walkthrough | 1 | implementation | 2–3 | W1, G02, G03, G04 | adk-agent-evaluation | blocked |
| G06–G10 | 2 | see below | 16–29 | — | — | proposed |

### G01: Runbook search agent with gold-set measurement

- **Phase and estimate:** phase 1. Hands-on 2–3, review 1–2, total 3–5 hours.
  Calendar wait: the gold questions from the lead (A13). Owner: Dev A.
- **Outcome and linked decisions:** in a local run, a question returns steps
  with a cited runbook URL. Implements D1, D2, D3 and D8, and measures I5.
- **Scope:** the agent, the two read tools and their instruction; `eval/gold.jsonl`;
  a script that reports recall@5 and the cited-page rate.
  Out of scope: tickets (G02), the UI (G03) and deployment (G04).
- **Depth:** build the measurement on a small set. The floor kept here is the
  pinned model, `max_llm_calls`, and a token read from the environment or
  Secret Manager, never from code.
- **Implementation route:** `LlmAgent` with function tools. CQL with
  `space in (allowlist)` added in code. Page body converted to text and capped
  at 8,000 characters. Fake Confluence fixtures for offline tests. Locally, use
  a read-only token: the developer's own token until W1 delivers bot A.
- **Primary skill:** adk-tool-interface-design.
- **Supporting skills:**
  - adk-agent-instructions: the instruction text.
  - adk-agent-evaluation: the gold-set runner.
  - adk-model-and-output-contracts: confirming the pin against the lifecycle file.
- **Acceptance:**
  - Offline: search returns at most 5 bounded hits.
  - Offline: an out-of-allowlist page ID is refused with an actionable error.
  - Offline: when Confluence returns 503, the agent says search is unavailable
    and gives no steps.
  - Offline: a scripted looping model stops at 8 calls.
  - Live: recall@5 and the cited-page rate on the gold set are recorded, with
    a target of 80% or more (I5, assumed).
  - The `google-adk` pin and the model ID are confirmed.
- **Verification:** `pytest tests/test_confluence.py tests/test_agent_limits.py`
  offline; `python eval/run_gold.py` as a bounded live run of about 20
  questions × about 4 calls.
- **Execution scope:** local code. Live reads use a read-only token only.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G01 from docs/plans/helpdesk-assistant.md. Read docs/architecture/helpdesk-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G02: Ticket proposal and confirmed creation (offline)

- **Phase and estimate:** phase 1. Hands-on 2–3, review 1–2, total 3–5 hours.
  First step: request W1, the bot accounts and the sandbox. Owner: Dev B.
- **Outcome and linked decisions:** asking for a ticket yields a preview, and
  only `POST /api/proposals/{id}/confirm` by the same user creates it. Implements
  D4 and D5, and guarantees I2 (for proposals), I3 and I4.
- **Scope:** `propose_ticket` with field validation; an in-process registry
  with owner, TTL and one-shot state; the confirm endpoint; a Jira client
  behind an interface, with a fake.
  Out of scope: durable records and reconciliation (G07), reporter mapping (G08)
  and the live sandbox call (G05).
- **Depth:** build confirmation for writes. Keep the floor: no write without a
  human. Replay and reconciliation are deferred to G07.
- **Implementation route:** the tool stores the proposal and returns
  `{status: "awaiting_confirmation", proposal_id, preview}`. The endpoint takes
  `user_id` from the verified identity, which is stubbed until G03. Project,
  labels and footer are fixed in code. A Jira timeout is recorded as
  `uncertain` and never retried automatically.
- **Primary skill:** safe-api-tool-calls.
- **Supporting skills:**
  - adk-tool-interface-design: the `propose_ticket` declaration.
  - adk-agent-security: the injected-runbook case asserting no create.
  - adk-tool-auth-and-secrets: selecting bot B's credential in code.
- **Acceptance:**
  - Confirm creates exactly one fake issue carrying the fixed project, labels
    and footer.
  - A second confirm returns the same key.
  - Confirming another user's proposal returns 404.
  - An expired proposal returns "expired".
  - A Jira timeout leaves state `uncertain` and shows the label hint.
  - A scripted model given an injected runbook page produces proposals only;
    the fake Jira records 0 creates.
- **Verification:** `pytest tests/test_tickets.py tests/test_confirm_endpoint.py`
  (offline).
- **Execution scope:** local code, plus the access request, which is an email
  or form only.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G02 from docs/plans/helpdesk-assistant.md. Read docs/architecture/helpdesk-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G03: IAP-authenticated page and session ownership

- **Phase and estimate:** phase 1. Hands-on 2–3, review 1–2, total 3–5 hours.
  No calendar waits. Owner: Dev A.
- **Outcome and linked decisions:** a staff member chats in a page and sees a
  proposal card with Create and Discard. Implements D6 and guarantees I1 and I2.
- **Scope:** IAP JWT verification middleware; a `/api/chat` wrapper around the
  Runner with server-derived `user_id`; a static page with safe Markdown
  rendering and the card wired to G02's endpoint.
  Out of scope: streaming polish and a history list.
- **Depth:** build identity and ownership. Keep the floor: no remote images,
  and links only to Atlassian domains.
- **Implementation route:** FastAPI middleware verifies
  `x-goog-iap-jwt-assertion` against Google's keys and the configured audience.
  Session operations always use the derived `user_id`. The page renders
  Markdown with images disabled and a link allowlist.
- **Primary skill:** adk-frontend-integration.
- **Supporting skills:** adk-tool-auth-and-secrets, for verifying the identity
  boundary.
- **Acceptance:**
  - A valid token reaches chat.
  - A missing, forged or wrong-audience token gets 401.
  - User B gets 404 on user A's session and on user A's proposal.
  - An answer containing `![x](https://evil/…)` and a foreign link renders
    neither.
  - Locally, a full journey with fakes ends at a ticket key.
- **Verification:** `pytest tests/test_iap_middleware.py tests/test_sessions.py`
  offline; a local browser run against the fakes.
- **Execution scope:** local code.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G03 from docs/plans/helpdesk-assistant.md. Read docs/architecture/helpdesk-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G04: Cloud Run behind IAP with secrets, logs and spend stop

- **Phase and estimate:** phase 1. Hands-on 2–3, review 1–2, total 3–5 hours.
  No calendar waits, assuming A11. Owner: Dev B.
- **Outcome and linked decisions:** the current app runs on Cloud Run, reachable
  only by the helpdesk group. Implements D7, D8 and D9.
- **Scope:**
  - The Dockerfile.
  - Service account `sa-helpdesk-agent`: Vertex user, plus access to the two
    secrets only.
  - `max-instances=1`.
  - IAP restricted to the helpdesk group.
  - JSON logs without content.
  - A Vertex quota and a budget alert at A3.
  - CI running the offline tests.

  Out of scope: SLOs, a canary, and more than one instance.
- **Depth:** build the hosting. Observability and release are minimal at this
  profile. The previous revision is kept for rollback.
- **Implementation route:** the team's existing Cloud Run and IAP pattern.
  Secrets are mounted as environment variables from Secret Manager. Model
  prices are checked against A3 to set the quota.
- **Primary skill:** deploy-adk-on-google-cloud.
- **Supporting skills:**
  - adk-agent-observability: log fields and token counts.
  - adk-release-engineering: the pinned release manifest.
  - adk-operational-guardrails: the quota and budget alert.
- **Acceptance:**
  - A group member loads the page.
  - A non-member is denied by IAP.
  - A log sample contains IDs and token counts but no message text.
  - The release manifest lists the image, model ID, ADK version and secret
    versions, with no aliases.
  - The budget alert and quota are visible.
- **Verification:** hosted checks in the authorized project; `pytest` in CI.
- **Execution scope:** **requires the user's explicit go-ahead** for the
  project and region before any deploy, IAM, IAP or secret change.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G04 from docs/plans/helpdesk-assistant.md. Read docs/architecture/helpdesk-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G05: Integrated deployment, live checks and lead walkthrough

- **Phase and estimate:** phase 1. Hands-on 1–2, review 1, total 2–3 hours.
  Calendar wait: the lead's availability for one hour. Owner: Dev A.
- **Outcome and linked decisions:** the pilot group can use the full journey.
  Covers I5 and I6, and includes live checks of D3 and D5.
- **Scope:**
  - Deploy G01, G02 and G03 together using G04's pipeline.
  - Switch to the bot A and bot B tokens.
  - Create one issue in the Jira sandbox.
  - Re-run the gold set on the deployed service.
  - The lead's walkthrough: 5 real questions and 1 ticket.
  - Record the baseline latency.
  - Switch to `ITHELP` after the lead's sign-off.
- **Depth:** a pilot of 3 to 5 people only (see the graduation conditions).
- **Primary skill:** adk-agent-evaluation.
- **Supporting skills:**
  - deploy-adk-on-google-cloud: the redeploy.
  - safe-api-tool-calls: the live sandbox create.
- **Acceptance:**
  - Exactly one sandbox issue exists, with label `op-<id>` and the footer.
  - A create in another project returns 403.
  - The gold set on the deployed service is within 5 points of G01's result.
  - The lead completes the journey and signs off.
  - A log sample contains no message text.
- **Verification:** bounded live and hosted checks.
- **Execution scope:** requires the go-ahead from G04, plus W1 delivered.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G05 from docs/plans/helpdesk-assistant.md. Read docs/architecture/helpdesk-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### Phase 2 (these will change after phase 1)

- **G06 Roll out to all 25 users, with feedback capture.** Primary skill:
  adk-agent-observability. 3–5 hours. Add a thumbs up/down control linked to
  the session ID, and a weekly usage and cost query from the logs.
  Acceptance: feedback events are queryable by session, and I6 is compared
  with the G05 baseline.
- **G07 Durable proposals and reconciliation.** Primary skill:
  safe-api-tool-calls. 4–7 hours. Store proposals and operation records in
  Firestore, reconcile uncertain creates by a JQL search for `op-<id>`, and
  move sessions to a persistent backend so more than one instance can run.
  Acceptance: after a timeout, a restart and a retry, exactly one issue exists.
- **G08 Reporter attribution.** Primary skill: adk-tool-auth-and-secrets.
  2–4 hours. Map the verified email to a Jira `accountId` and set it as
  reporter, falling back to the footer. Acceptance: the issue's reporter is the
  confirming staff member.
- **G09 Regression set of 40 or more cases, with a CI evaluation gate.**
  Primary skill: adk-release-engineering. 4–7 hours. Acceptance: CI fails when
  recall@5 drops more than 5 points below the baseline.
- **G10 Retrieval decision (discovery).** Primary skill:
  adk-memory-architecture. 3–6 hours. If G01's recall is below 80%, compare a
  Vertex AI Search Confluence connector on the same gold set. Stopping
  condition: the gold set has been run on both. Decision: keep CQL, or adopt
  the index with permission sync.

## Later

| Item | Trigger | Risk accepted while it waits | Likely skill |
| --- | --- | --- | --- |
| SDP screening of runbook text | A credential is found in a runbook | Secrets could appear in answers (not in logs) | protect-adk-sensitive-data |
| Per-user Jira OAuth (3LO) | Audit requires the per-user creator | The bot is the creator (A9) | adk-tool-auth-and-secrets |
| Adversarial suite beyond the I3 case | Any new write or egress tool | Injection is limited to proposals | adk-agent-security |
| SLOs and alerts | Users outside the helpdesk, or an incident | Outages are noticed by users | adk-agent-observability |
| Per-user allowance | Spend above A3 | Shared quota exhaustion | adk-operational-guardrails |
| Canary and joint rollback | Weekly prompt or model releases | Manual rollback to the previous revision | adk-release-engineering |
| Model re-baseline | Before the `gemini-3.5-flash` Vertex retirement (2027-05-19 or later); re-check the lifecycle file quarterly | — | adk-model-and-output-contracts |
| Jira update and comment tools | Requested by the helpdesk | — (requires a new trifecta review) | adk-tool-interface-design |

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| [Design](../architecture/helpdesk-assistant.md) | Decisions, guarantees and assumptions |
| This plan | Goals, schedule, cut line and deferred items |
| `eval/` summary (G01, G05) | Gold-set results, linked to run records |

## Open decisions for further planning

See the design's [Open decisions](../architecture/helpdesk-assistant.md#open-decisions).
In addition, confirm the cut line: either durable proposals in phase 2 (current),
or in phase 1 with 12 days or more hours from Dev B (see the what-ifs above).

## Resume here

- **Next goal:** G01, which has no prerequisites. G02 and G04 can start in
  parallel.
- **Read first:** the design, then this plan.
- **Next action:** confirm the `google-adk` pin and model ID, then write fake
  Confluence fixtures.
- **Continuation prompt:**

```text
/adk-engineer Carry out G01 Runbook search agent from docs/plans/helpdesk-assistant.md.
Read docs/architecture/helpdesk-assistant.md and preserve its accepted decisions.
Use adk-tool-interface-design with adk-agent-instructions, adk-agent-evaluation
and adk-model-and-output-contracts. Work locally only, verify G01's acceptance
cases, and update the plan with actual evidence and remaining blockers.
```

After that goal: `/adk-engineer Continue the next ready goal in docs/plans/helpdesk-assistant.md.`
