# Implementation plan: IT helpdesk runbook and ticket assistant

Status: draft; ready goals identified (G01 ready; G02–G04 follow in order)
Architecture: [docs/architecture/helpdesk-assistant.md](../architecture/helpdesk-assistant.md)
Continuation source of truth: this plan; tickets in `docs/tickets/helpdesk-assistant/` copy phase 1 goals.

## Destination and constraints

Phase 1 destination: the 25 helpdesk staff open one URL, sign in with Google,
ask runbook questions and get cited answers, and get a pre-filled Jira ticket
draft they submit themselves. Non-goals and assumptions: see the design's
assumed-answers table (all provisional). Authorization: design only; no goal
has been carried out. Cloud work in G01 and G03 needs the user's GCP project
and permission.

Greenfield repository: nothing inspected beyond `.claude/skills/`. Proposed
layout (unverified, adjust in G01):

```
helpdesk_assistant/agent.py      # root_agent, instruction, call-cap callback
helpdesk_assistant/confluence.py # search_runbooks adapter
helpdesk_assistant/jira_draft.py # draft_ticket link builder
tests/                           # offline tests, recorded Confluence fixtures
eval/regression.yaml             # 15-20 labelled questions
pyproject.toml                   # google-adk==2.8.0 (working pin)
```

Inherited pins: `google-adk==2.8.0` (to confirm in G01), model
`gemini-3.5-flash` on Vertex AI (lifecycle table checked 2026-10-08), prompt
versioned in `agent.py`. Changing one of them is a release, not a side effect.

## Delivery profile and capacity

Profile: internal tool (see design).

| Phase | Delivers | Goals | Estimate (focused h) | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship | Helpdesk staff use hosted, cited runbook search and ticket drafts | G01–G04 | 21–31 | 2 × 0.5 × 10 d × 6 h × 0.6 ≈ 36; 25% reserve → 27 usable |
| 2, graduate | Direct ticket creation, per-user sessions, eval gate, diagnosable failures | G05–G08 | 26–40 | When the team has time |

Phase 1 fits at the low/middle of its range only. If work runs high, G04 moves
to phase 2. Order keeps each completed goal useful: G01 (agent runs) → G02
(search useful locally) → G03 (colleagues use it) → G04 (drafts). One engineer
alone: same order; G03 is the line below which the team has nothing to hand to
colleagues.

Suggested split: Engineer A takes G01 then G03; engineer B takes G02 then G04
once G01's skeleton exists.

## Implementation map

| Decision | Component and integration point | GCP | Primary skill | Still to verify |
| --- | --- | --- | --- | --- |
| D1 | `LlmAgent` `root_agent` in `agent.py` | Vertex AI | adk-workflow-design | ADK 2.8.0 constructor |
| D2 | `search_runbooks` function tool → Confluence Cloud REST search (CQL) | Secret Manager | adk-tool-interface-design | CQL endpoint, fields, rate limits |
| D3 | Token read at startup by runtime service account | Secret Manager, IAM | adk-tool-auth-and-secrets | — |
| D4 | `draft_ticket` function tool returning a create URL | none | adk-tool-interface-design | Jira Cloud create-URL pre-fill |
| D5 | `adk web`-served app on Cloud Run behind IAP | Cloud Run, IAP, Artifact Registry | deploy-adk-on-google-cloud | IAP on Cloud Run direct vs load balancer |
| D6 / I5 | `before_model_callback` call counter per invocation | Billing budget alert | adk-operational-guardrails | Callback signature in pinned ADK |

## Goals and dependencies

| ID and goal | Phase | Type | Estimate | Depends on | Primary skill | State |
| --- | --- | --- | --- | --- | --- | --- |
| G01 Agent answers locally on Vertex with a call cap | 1 | impl + setup | 4–6 h | — | adk-workflow-design | ready (needs GCP project) |
| G02 Cited runbook search from real Confluence | 1 | impl | 8–11 h | G01 | adk-tool-interface-design | blocked: G01 |
| G03 Colleagues use it behind IAP on Cloud Run | 1 | impl | 6–8 h | G01, G02 | deploy-adk-on-google-cloud | blocked: G02, GCP permission |
| G04 Pre-filled Jira ticket draft the user submits | 1 | spike + impl | 3–6 h | G01 | adk-tool-interface-design | blocked: G01 |
| G05 Direct Jira creation with confirmation | 2 | impl | 10–14 h | G04 | safe-api-tool-calls | proposed |
| G06 Per-user sessions and a small front end | 2 | impl | 8–12 h | G03 | adk-frontend-integration | proposed |
| G07 Regression set in CI with pinned release note | 2 | impl | 4–7 h | G02 | adk-release-engineering | proposed |
| G08 Traces, token cost and time-to-answer measure | 2 | impl | 4–7 h | G03 | adk-agent-observability | proposed |

### G01 — Agent answers locally on Vertex with a call cap

- **Phase and estimate:** 1; 4–6 h (includes first GCP project, IAM and ADC setup for a team new to GCP)
- **Outcome and linked decisions:** an engineer runs `adk web` locally and chats with a pinned Gemini model on Vertex; a runaway turn stops at 6 model calls. D1, D6, I5.
- **Scope:** project skeleton, `pyproject.toml` pin, `root_agent` with a placeholder instruction and no tools, call-cap callback, billing budget alert. Out: tools (G02, G04), hosting (G03).
- **Depth:** floor only: pinned model and ADK, call cap, budget alert, no secrets in repo.
- **Implementation route:** `LlmAgent(model="gemini-3.5-flash")`; `before_model_callback` counting per `invocation_id` in callback state; Vertex via ADC (`gcloud auth application-default login`); `.env` with project/location, git-ignored.
- **Prerequisites:** a GCP project with billing (user-owned), Vertex AI API enabled; Python 3.11.
- **Primary skill:** adk-workflow-design
- **Supporting skills:** adk-operational-guardrails (call cap and budget alert); adk-model-and-output-contracts (model pin against the lifecycle table)
- **Acceptance:** local chat answers; scripted-model test hitting 7 calls ends the turn with the stop message and no 7th call; `grep` finds no key in the repo; installed ADK version and model availability recorded.
- **Verification:** offline `pytest tests/test_call_cap.py`; local integration `adk web` one turn on Vertex (authorized live, ≤ 5 calls).
- **Execution scope:** local code authorized by the plan; creating the GCP project and budget needs the user's permission.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G01 from docs/plans/helpdesk-assistant.md. Read docs/architecture/helpdesk-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G02 — Cited runbook search from real Confluence

- **Phase and estimate:** 1; 8–11 h
- **Outcome and linked decisions:** asking "VPN certificate expired" returns the steps with links to the source pages, or "no runbook found". D2, D3, I2, I3.
- **Scope:** `search_runbooks` adapter (CQL built in code from an allowlist of spaces, excludes label `restricted`, top 5, excerpt ≤ 1,500 chars, URL and last-modified), token from Secret Manager (env var locally), instruction to cite or decline, 15–20 labelled questions with expected pages. Out: semantic index, per-user permissions.
- **Depth:** internal-tool build for retrieval and a small regression set; read-only credential; errors returned as `status: error`.
- **Implementation route:** function tool in `confluence.py` using `httpx` to Confluence Cloud REST search; recorded JSON fixtures for tests; instruction in `agent.py`.
- **Prerequisites:** G01; read-only Atlassian bot account and API token (user to supply); list of spaces (A4).
- **Primary skill:** adk-tool-interface-design
- **Supporting skills:** adk-tool-auth-and-secrets (bot token in Secret Manager); adk-agent-instructions (cite-or-decline instruction); adk-agent-evaluation (regression set)
- **Acceptance:** hit@5 ≥ 0.8 on the regression set (provisional target); model text like `space = HR OR` is quoted, never injected into CQL; missing token fails closed with a clear error; every cited URL appears in that turn's tool results.
- **Verification:** offline `pytest tests/test_confluence.py` with fixtures; local integration regression run against real Confluence (read-only).
- **Execution scope:** read-only calls to the company Confluence with the bot token.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G02 from docs/plans/helpdesk-assistant.md. Read docs/architecture/helpdesk-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G03 — Colleagues use it behind IAP on Cloud Run

- **Phase and estimate:** 1; 6–8 h
- **Outcome and linked decisions:** helpdesk staff open one URL with their Google login; others get 403. D5, I1, I6.
- **Scope:** container/deploy of the ADK web app to Cloud Run (`max-instances=1`), runtime service account with Vertex user and Secret Manager accessor only, IAP restricted to `helpdesk@`, `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS=false`, structured logs with IDs and token counts only. Out: per-user sessions (G06), traces (G08).
- **Depth:** internal tool hosting; accepted dev-UI risk recorded in the design.
- **Implementation route:** `adk deploy cloud_run` or `gcloud run deploy` (verify flags with installed `--help`); IAP directly on Cloud Run if available in region, else external load balancer.
- **Prerequisites:** G01, G02; GCP permission to deploy and set IAM; the `helpdesk@` group.
- **Primary skill:** deploy-adk-on-google-cloud
- **Supporting skills:** adk-tool-auth-and-secrets (runtime identity, least privilege); adk-agent-observability (content capture off, minimal logs); adk-release-engineering (deploy note with image, model ID, ADK pin)
- **Acceptance:** member completes the VPN journey; non-member account gets 403; log search for the question text returns nothing; deploy note records revision, model ID and ADK version.
- **Verification:** hosted checks on the authorized project; offline tests pass before deploy.
- **Execution scope:** needs explicit permission for the GCP project, IAM changes and deployment.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G03 from docs/plans/helpdesk-assistant.md. Read docs/architecture/helpdesk-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G04 — Pre-filled Jira ticket draft the user submits

- **Phase and estimate:** 1; 3–6 h (1 h spike included)
- **Outcome and linked decisions:** "raise a ticket for network ops" yields a summary, description and a link that opens Jira's create screen pre-filled; the user submits under their own login. D4, I4.
- **Scope:** spike (≤ 1 h): confirm Jira Cloud create-URL pre-fill for project, issue type, summary, description; stop and fall back to copyable text plus a plain create link if unsupported. `draft_ticket` tool with site, project and issue type from config; URL-encoding and length bound. Out: API creation (G05).
- **Depth:** no Jira credential, no network call, no write.
- **Implementation route:** pure function tool in `jira_draft.py`; instruction line: call only when the user asks.
- **Prerequisites:** G01; Jira site, project key and issue type (A7).
- **Primary skill:** adk-tool-interface-design
- **Supporting skills:** adk-agent-instructions (when to draft, never claim a ticket was created)
- **Acceptance:** the link opens Jira create with fields filled (manual check); the agent never says "ticket created"; the tool cannot change host or project from model arguments; no Jira secret exists in the project.
- **Verification:** offline `pytest tests/test_jira_draft.py`; manual local check of one link.
- **Execution scope:** local only; opening the link is done by a person.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G04 from docs/plans/helpdesk-assistant.md. Read docs/architecture/helpdesk-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### Phase 2 (coarser; phase 1 results may change them)

- **G05 Direct Jira creation with confirmation** — 10–14 h. Primary: safe-api-tool-calls. Supporting: adk-tool-auth-and-secrets (bot or per-user credential, reporter mapping), adk-agent-security (trifecta: runbook text + write), adk-operational-guardrails (confirmation), adk-tool-interface-design. Acceptance: no create without a confirmation bound to the exact fields; a retried create with the same operation key yields one ticket (verify Jira duplicate-lookup contract); a scripted injected runbook cannot trigger a create.
- **G06 Per-user sessions and a small front end** — 8–12 h. Primary: adk-frontend-integration. Supporting: adk-memory-architecture (session backend if persistence wanted). Acceptance: user ID derived from the IAP identity; user B cannot open user A's session.
- **G07 Regression set in CI with release note** — 4–7 h. Primary: adk-release-engineering. Supporting: adk-agent-evaluation. Acceptance: CI fails by exit code when hit@5 drops below baseline; release note lists image, prompt version, model ID.
- **G08 Traces, token cost and time-to-answer** — 4–7 h. Primary: adk-agent-observability. Acceptance: one span per agent/tool/model call with session ID, no content; a before/after time-to-answer sample from five volunteers.

## Later

| Item | Trigger | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| Indexed semantic search (e.g. Vertex AI Search) | hit@5 < 0.8 after instruction/query tuning | Keyword misses | adk-memory-architecture |
| Per-user Confluence permissions (OAuth 3LO) | Restricted pages or non-helpdesk spaces | Shared read credential | adk-tool-auth-and-secrets |
| PII/secret screening | Personal data or secrets found in runbooks or chats | Content only kept out of logs | protect-adk-sensitive-data |
| Model migration off `gemini-3.5-flash` | Vertex retirement notice (currently "2027-05-19 or later") | — | adk-release-engineering |
| Multi-instance scaling | Concurrency complaints | Single instance | optimise-adk-on-google-cloud |
| Slack/Chat front end | Users ask to stay in chat tool | Separate browser tab | adk-frontend-integration |

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| docs/architecture/helpdesk-assistant.md | Method, assumptions, decisions |
| eval/regression results (created in G02) | Retrieval and citation quality |
| This plan | Remaining limits and deferred controls |

## Open decisions for further planning

See the design's Open decisions; A8 (draft vs direct create) and A10 (dev UI)
can move the cut line.

## Resume here

- **Next goal:** G01, ready: no unresolved design dependency; needs a GCP project.
- **Read first:** the design, this plan.
- **Next action:** confirm Python 3.11 and the ADK 2.8.0 pin, create the skeleton.
- **Continuation prompt:**

```text
/adk-engineer Carry out G01 from docs/plans/helpdesk-assistant.md.
```

After that: `/adk-engineer Continue the next ready goal in docs/plans/helpdesk-assistant.md.`
