# Implementation plan: IT helpdesk assistant

Status: draft, ready goals identified (G01, G02 can start in parallel on day 1)
Architecture: [docs/architecture/helpdesk-assistant.md](../architecture/helpdesk-assistant.md)
Continuation source of truth: this plan; phase 1 tickets in
[docs/tickets/helpdesk-assistant/](../tickets/helpdesk-assistant/) copy their goal's figures.

## Destination and constraints

Phase 1 destination: the 25 helpdesk staff sign in through IAP. They ask
runbook questions and get answers that cite Confluence pages, and they create
an `ITSD` Jira ticket after confirming its exact contents.

Non-goals are listed in the design. Accepted stack (proposed, greenfield):
Python 3.11, `google-adk` 2.8.0 (to confirm in G01), FastAPI (as bundled with
ADK), Vertex AI `gemini-3.8-flash`, Cloud Run, IAP, Secret Manager.

Authorisation: this plan is design-only. Every goal that touches GCP or
Atlassian needs the engineers' own authorised accounts. No goal deploys,
grants IAM or creates real tickets until its owner runs it with those
accounts. During development, writes go to a sandbox Jira project
(`ITSDTEST`).

Inspected repository: empty apart from `.claude/skills`. The module layout below is **proposed**:

```text
helpdesk_assistant/
  agent.py        # root_agent factory, instruction, tools wired; App
  config.py       # pinned model ID, space allow-list, project/issue-type allow-list, limits
  tools/confluence.py  tools/jira.py
  server.py       # FastAPI: IAP-JWT middleware, /chat, /confirm, static page
  static/index.html
tests/            # offline: fake LLM, fake HTTP transports, JWT fixtures
eval/gold.json    # 12 gold questions (G02)
eval/run_gold.py
```

Pinned artefacts inherited by every goal: model `gemini-3.8-flash` (from the
lifecycle table `checked_on` 2026-10-08), the instruction in `agent.py`
(versioned with git), and `google-adk==2.8.0`. Changing any of these is a
release: re-run the G02 gold set.

## Delivery profile and capacity

Profile: **internal tool** (see the design's delivery constraints).

| Phase | Delivers | Goals | Human hours, agent-assisted (range) | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship | Hosted for the helpdesk group: cited runbook answers, confirmed ticket creation, measured on 12 gold questions | G01–G05 | 21–36 | 2 people × 40 h × 0.6 focus = 48 focused h; 25% reserve (12 h) → 36 h available |
| 2, harden or graduate | The graduation conditions in the design | G06–G12 | 28.5–57 | When the team has time; not scheduled |

How the numbers were made: these are person-hours of human effort with a
coding agent (hands-on plus review and verify). They are assumptions. Each
goal's figure is the delivery-profiles starting point × **1.5** because the
team is new to ADK, applied to hands-on and review alike. **G01 also carries
the one-off GCP day** (4–6 h) because the team has never used GCP. Calendar
waits are on the goals and are not added to hours.

| Person | Goals, in order | Hours | Their capacity (focused, before reserve) |
| --- | --- | --- | --- |
| Engineer A (agent and tools) | G02 → G04 → G03 | 10.5–19.5 | 24 |
| Engineer B (cloud and hosting) | G01 → G05; reviews G03's write boundary (counted in G03) | 10.5–16.5 | 24 |

**Fit.** The phase 1 high end (36 h) equals capacity minus reserve, so it fits
with nothing to spare. B has about 7 h of slack at the high end and A about
4.5 h, so B picks up G03 review and the release record.

**Longest chain.** G01 (9) runs in parallel with G02's offline part. Then
G02's live check (~2), then G04 (4.5), then G05 (7.5). That is ≈ 23 h at the
high end against 24 focused hours per person, which is tight. The real
schedule risk is the **calendar waits** on G01 and G05, so file those
requests on day 1.

**Cut line.** "Fits: G01–G05, 21–36 h of 36. Next phase: G06–G12." If the work
runs high, **G03 moves to phase 2**. What remains is still useful: hosted,
cited runbook search for all 25 staff. Order of usefulness if time runs out:
G01 → G02 (engineers can use it locally) → G04 + G05 (colleagues can use it,
read-only) → G03.

## Implementation map

| Decision / requirement | Component and integration point (proposed) | GCP responsibility | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |
| D1 one agent, three tools | `agent.py` `LlmAgent` + `App`; `Runner` built in `server.py` | Vertex AI endpoint | `adk-workflow-design` | Confirm `App`/`Runner` constructors against the 2.8.0 pin (G01) |
| D2 live Confluence search | `tools/confluence.py` with an `httpx` client; CQL with the space filter added in code | Secret Manager `confluence-token` | `adk-tool-interface-design` | CQL syntax and endpoint against Atlassian Cloud docs (G02) |
| D3 confirmed Jira create | `tools/jira.py` `create_ticket` wrapped in `FunctionTool(..., require_confirmation=True)`; label `asst-op-<id>` | Secret Manager `jira-token` | `safe-api-tool-calls` | Jira create endpoint, label search and any idempotency support (G03) |
| D4 identity | `server.py` middleware verifies `x-goog-iap-jwt-assertion` and sets `user_id` | IAP on Cloud Run; helpdesk Google group | `adk-tool-auth-and-secrets` (G04), `deploy-adk-on-google-cloud` (G05) | IAP for Cloud Run setup and JWT audience format (G05) |
| D5 sessions | `InMemorySessionService`; min = max = 1 instance | Cloud Run scaling settings | `deploy-adk-on-google-cloud` | Restart behaviour (G05) |
| D6 pinned model | `config.py` `MODEL_ID = "gemini-3.8-flash"`, Vertex backend env | Vertex AI API enabled, region | `adk-model-and-output-contracts` | Region availability and price (G01) |
| D7 spend stop | `RunConfig(max_llm_calls=8)` in `server.py`; result caps in tools | Billing budget alert | `adk-operational-guardrails` | Loop test (G02) |
| D8 page | `static/index.html`, `/chat`, `/confirm` JSON contract | — | `adk-frontend-integration` | Browser check (G05) |
| D9 logs | JSON logger, no content | Cloud Logging | `adk-agent-observability` | Log sample (G05) |

## Goals and dependencies

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | State / blocker |
| --- | --- | --- | --- | --- | --- | --- |
| G01 GCP foundation and a pinned model answering locally | 1 | implementation + setup | 5.5–9 | — | `deploy-adk-on-google-cloud` | ready; wait: project and billing, Atlassian bot tokens |
| G02 Cited runbook answers locally, measured on 12 gold questions | 1 | implementation | 4.5–9 | offline: none; live: G01 | `adk-tool-interface-design` | ready (offline part) |
| G03 Create a Jira ticket after explicit confirmation | 1 | implementation | 3–6 | G02 | `safe-api-tool-calls` | ready after G02; wait: Jira bot create permission on `ITSDTEST`/`ITSD` |
| G04 Chat page and API bound to the verified IAP identity (local) | 1 | implementation | 3–4.5 | G02 (agent factory) | `adk-frontend-integration` | ready after G02 |
| G05 Hosted on Cloud Run behind IAP for the helpdesk group | 1 | implementation | 5–7.5 | G01, G04 (G03 for the final redeploy) | `deploy-adk-on-google-cloud` | blocked by A9 (sign-in system) for the IAP step |
| G06 Conversations survive restarts and scale-out | 2 | implementation | 4.5–9 | G05 | `adk-memory-architecture` | proposed |
| G07 Decide live CQL search versus a semantic index | 2 | discovery | 3–6 | G02 baseline | `adk-memory-architecture` | proposed |
| G08 Tickets attributed to the requesting staff member | 2 | implementation | 4.5–9 | G03 | `adk-tool-auth-and-secrets` | proposed |
| G09 30-case evaluation set gated in CI, plus outcome survey | 2 | implementation | 6–12 | G02 | `adk-agent-evaluation` | proposed; needs a CI runner |
| G10 Traces and token cost per conversation | 2 | implementation | 3–6 | G05 | `adk-agent-observability` | proposed |
| G11 Runbook secret scan and expanded adversarial suite | 2 | implementation | 4.5–9 | G03 | `adk-agent-security` | proposed |
| G12 Uncertain-create reconciliation hardened | 2 | implementation | 3–6 | G03 | `safe-api-tool-calls` | proposed; trigger: duplicate seen |

Phase 1 sum: low 5.5 + 4.5 + 3 + 3 + 5 = 21, high 9 + 9 + 6 + 4.5 + 7.5 = 36.
Phase 2 sum: low 4.5 + 3 + 4.5 + 6 + 3 + 4.5 + 3 = 28.5, high 9 + 6 + 9 + 12 + 6 + 9 + 6 = 57.

### G01 — GCP foundation and a pinned model answering locally

- **Phase and estimate:** 1; hands-on 5–8 (includes the 4–6 h first-GCP-project day), review and verify 0.5–1, total 5.5–9; calendar waits: GCP project creation and billing link by the cloud admin (assume 1–5 working days); Atlassian bot accounts with API tokens (Confluence read on the runbook spaces; Jira create on `ITSDTEST` and `ITSD`), from the Atlassian admin (assume 1–5 working days). **File both requests on day 1.** Owner: Engineer B.
- **Outcome and linked decisions:** An engineer runs a minimal agent locally that answers "hello" through the pinned Vertex model under its own credentials. Secrets exist in Secret Manager. D6, D7, design versions.
- **Scope:** In: project, region choice, Vertex AI API, billing budget alert at 50/90/100%, Secret Manager secrets `confluence-token` and `jira-token` (values entered by a person, never committed), a runtime service account (created, not yet deployed), repository skeleton with `pyproject.toml` pinning `google-adk==2.8.0` and a lock file, `config.py` with `MODEL_ID`, a hello `LlmAgent`, `.gitignore` for env files. Out: tools (G02), hosting (G05).
- **Depth:** Secrets built properly; budget alert only (no app allowance); no CI.
- **Implementation route:** `gcloud` with the engineer's own account; ADK `LlmAgent(model=MODEL_ID)` via `adk run` or a 10-line Runner script with `GOOGLE_GENAI_USE_VERTEXAI=TRUE`, `GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION` from local env (not committed). Check in the 2.8.0 pin: `LlmAgent`, `App`, `Runner`, `RunConfig.max_llm_calls`, `FunctionTool(require_confirmation=...)`.
- **Prerequisites:** cloud admin and Atlassian admin requests filed.
- **Primary skill:** `deploy-adk-on-google-cloud` (project, identity, secrets).
- **Supporting skills:** `adk-model-and-output-contracts` (model ID from the lifecycle table, region availability).
- **Acceptance:** a local call returns a model response, and the recorded model ID matches `config.py`; `gcloud secrets list` shows both secrets, and nothing secret appears in git (`git grep` for token prefixes finds nothing); a budget alert exists; the API names above are confirmed against the installed pin, with any differences recorded; region availability and price of the model are recorded with source URL and date.
- **Verification:** local integration with the engineer's credentials; `pytest -q` on the skeleton (an import test).
- **Execution scope:** creating the project and billing needs the cloud admin. Everything else is within the engineer's project-owner role.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G01 from docs/plans/helpdesk-assistant.md. Read docs/architecture/helpdesk-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G02 — Cited runbook answers locally, measured on 12 gold questions

- **Phase and estimate:** 1; hands-on 3–6 (includes about 1 h with the helpdesk lead writing gold questions and expected pages), review and verify 1.5–3, total 4.5–9; calendar waits: helpdesk lead's hour, and the Confluence token from G01 for the live part. Owner: Engineer A.
- **Outcome and linked decisions:** The running example works locally. "VPN error 809" returns the runbook steps with page links, and "no runbook found" is said honestly. D1, D2, D7, I6–I8.
- **Scope:** In: `search_runbooks` and `read_runbook` tools (CQL with code-added space filter, ≤5 results, excerpt ≤300 chars, page text ≤8,000 chars with a `truncated` flag, error results with a `status`); the agent instruction; `RunConfig(max_llm_calls=8)`; `eval/gold.json` (12 questions with expected page IDs); `eval/run_gold.py`, which reports hit@5 and citation presence. Out: Jira (G03), web page (G04).
- **Depth:** small regression set, not CI. Results bounded at the tool. No semantic index.
- **Implementation route:** function tools that take an injected `httpx` client so tests use `httpx.MockTransport`. The token is read from Secret Manager or the environment at startup, never passed as a model argument. The instruction treats page text as reference material.
- **Prerequisites:** offline part none. Live part: G01 and the Confluence token.
- **Primary skill:** `adk-tool-interface-design`.
- **Supporting skills:** `adk-agent-instructions` (instruction and "no runbook found" behaviour), `adk-agent-evaluation` (gold set and runner), `adk-operational-guardrails` (call limit).
- **Acceptance:** offline: a fake Confluence returning 2 pages leads to an answer containing both URLs. An empty result gives "no runbook found" and no second, broader query without the space filter. A forged `space = X` in the query is still constrained to the allow-list. A scripted model that loops stops at 8 calls. The rendered request shows 2 tool declarations and no token. Live: gold run recorded, with hit@5 and citations (targets 9/12 and 10/12 are provisional and do not block completion; below target is the trigger for G07). Fewer than 100 model calls are used.
- **Verification:** `pytest -q tests/` offline; `python eval/run_gold.py` as a bounded live run.
- **Execution scope:** read-only Confluence access with the bot token; Vertex calls within the budget.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G02 from docs/plans/helpdesk-assistant.md. Read docs/architecture/helpdesk-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G03 — Create a Jira ticket after explicit confirmation

- **Phase and estimate:** 1; hands-on 1.5–3, review and verify 1.5–3 (a write boundary, so a careful read plus adversarial checks, by Engineer B), total 3–6; calendar waits: bot create permission on `ITSDTEST` (sandbox) and `ITSD`. Owner: Engineer A.
- **Outcome and linked decisions:** "Open an incident for the network team" → the user sees the exact draft → Approve → ticket key and link; Reject → nothing. D3, I3–I5, security posture.
- **Scope:** In: the `create_ticket` tool (issue type and priority enums, summary ≤200, description ≤4,000, ≤3 runbook URLs). Code adds the project from config, a description footer "Requested by <verified email> via helpdesk assistant", and labels `helpdesk-assistant` and `asst-op-<id>`. The operation ID is generated in code from `function_call_id`. Wrapped in `FunctionTool(require_confirmation=True)`. There is no retry of the POST. On a timeout or 5xx after send, one label search, then "created as KEY", or "uncertain: check JQL `labels = asst-op-<id>`". Out: assignee and components; per-user reporter (G08); full reconciliation (G12).
- **Depth:** confirmation for writes (internal-tool depth); reconciliation by label, not deduplication.
- **Implementation route:** `tools/jira.py`; the user identity reaches the tool via session state set by trusted code (G04 sets it; tests set it directly), never as a model argument. Investigate whether Jira Cloud create supports an idempotency key, from documentation only, 30 minutes max, and record the answer.
- **Prerequisites:** G02 (agent and tool pattern); Jira token.
- **Primary skill:** `safe-api-tool-calls`.
- **Supporting skills:** `adk-tool-interface-design` (declaration and confirmation hint text), `adk-agent-security` (exposure check and the three adversarial cases).
- **Acceptance:** offline with a fake Jira: approve leads to exactly 1 POST with the project from config; reject and missing confirmation lead to 0 POSTs; a disallowed project or oversized field is refused before confirmation is requested, with 0 POSTs. Adversarial cases (a) to (c) from the design lead to 0 POSTs. A timeout-after-commit fake leads to an "uncertain" or "found KEY" message and no second POST. Live: one confirmed ticket in `ITSDTEST`, carrying both labels and the footer, then closed.
- **Verification:** `pytest -q tests/test_jira*.py`; one bounded live create in the sandbox project only.
- **Execution scope:** live writes **only** to `ITSDTEST` until G05's release record names `ITSD`.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G03 from docs/plans/helpdesk-assistant.md. Read docs/architecture/helpdesk-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G04 — Chat page and API bound to the verified IAP identity (local)

- **Phase and estimate:** 1; hands-on 1.5–2.5, review and verify 1.5–2 (authorisation boundary), total 3–4.5; calendar waits: none. Owner: Engineer A.
- **Outcome and linked decisions:** Staff get a simple page instead of a dev UI. The server knows who they are from IAP, not from the browser. D4, D8, I1, I2.
- **Scope:** In: `server.py` (FastAPI) with middleware that verifies `x-goog-iap-jwt-assertion` (signature against Google's IAP keys, `aud` from config, issuer) and puts the email in `user_id`; `POST /chat {session_id?, message}` → `{session_id, text, confirmation?}`; `POST /confirm {session_id, function_call_id, approved}`; session lookup only under the verified `user_id`; `static/index.html` rendering text, links and an Approve / Reject box showing the full draft; trusted code sets `user_email` in session state; a local dev mode that accepts a fixed test identity and is **off unless an env flag is set, refused when running on Cloud Run** (`K_SERVICE` set). Out: streaming, history list, styling.
- **Depth:** identity built (internal-tool depth); no streaming.
- **Implementation route:** Runner built once with `InMemorySessionService` and `RunConfig(max_llm_calls=8)`; the confirmation response is sent back as the ADK confirmation function response for that `function_call_id`, in the format to verify against the 2.8.0 pin. JWT verification uses `google-auth` `id_token.verify_token` with the IAP certs URL (to verify).
- **Prerequisites:** G02 agent factory (a stub agent is enough to start).
- **Primary skill:** `adk-frontend-integration`.
- **Supporting skills:** `adk-tool-auth-and-secrets` (JWT verification and trusted identity into tool context).
- **Acceptance:** offline: no header → 401; a JWT signed by a local test key that is not in the trusted set → 401; wrong `aud` → 401; a valid test JWT → 200. User B posting user A's `session_id` → 404. Dev-mode flag with `K_SERVICE` set → the server refuses to start. The confirm endpoint with someone else's `function_call_id` → 404 and no tool run. Manual local browser run against the fake tools shows the answer and the confirm box.
- **Verification:** `pytest -q tests/test_server*.py` offline; manual local browser check.
- **Execution scope:** local only.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G04 from docs/plans/helpdesk-assistant.md. Read docs/architecture/helpdesk-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G05 — Hosted on Cloud Run behind IAP for the helpdesk group

- **Phase and estimate:** 1; hands-on 3.5–5.5, review and verify 1.5–2, total 5–7.5; calendar waits: helpdesk Google group and IAP enablement or OAuth consent by the Workspace or cloud admin (assume 1–3 working days); possibly an internal security review of a new internal app (unknown, ask on day 1). Owner: Engineer B.
- **Outcome and linked decisions:** All 25 helpdesk staff use the assistant from a URL with their own sign-in. D4, D5, D9, I1, I2.
- **Scope:** In: container build from the repository; Cloud Run service with the runtime SA (Vertex user, Secret Manager accessor on the two secrets only); min = max = 1 instance; IAP enabled and limited to the helpdesk group; the `aud` value configured; JSON logs without content; the release record (image digest, model ID, ADK pin, lock hash, secret versions) written into this goal's evidence; a rollback note (previous revision). Out: persistent sessions (G06), traces (G10), CI (G09).
- **Depth:** Cloud Run behind IAP; minimal observability; no canary.
- **Implementation route:** `gcloud run deploy` from source or an image, using the engineer's authorised account. Set up IAP for Cloud Run following current Google docs (record URL and date). Ingress set so the service is reachable only through IAP.
- **Prerequisites:** G01, G04; A9 confirmed (Google sign-in). If A9 is false, stop and turn this into a discovery goal on the identity front door.
- **Primary skill:** `deploy-adk-on-google-cloud`.
- **Supporting skills:** `adk-agent-observability` (content-free structured logs and token counts), `adk-release-engineering` (release record and pinned versions).
- **Acceptance:** a group member opens the URL, asks the gold VPN question and gets a cited answer. A non-member account gets IAP's 403. A direct request to the `run.app` URL without IAP is refused. A restart (new revision) followed by approving an old pending confirmation leads to no ticket and a clear message. A log sample shows IDs, tool names and token counts and no message text. The release record is complete. Rollback to the previous revision is rehearsed once.
- **Verification:** hosted checks by hand with two accounts; `gcloud logging read` sample; this is authorised live work.
- **Execution scope:** deployment and IAM in the team's own project only, by the engineers. Switching `create_ticket` from `ITSDTEST` to `ITSD` is a config change recorded here, after the helpdesk lead agrees.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G05 from docs/plans/helpdesk-assistant.md. Read docs/architecture/helpdesk-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### Phase 2 goals (coarser; phase 1 results may change them)

- **G06 Conversations survive restarts and scale-out** — 4.5–9 h; primary `adk-memory-architecture`, supporting `deploy-adk-on-google-cloud`. Replace in-memory sessions with `DatabaseSessionService` on Cloud SQL for PostgreSQL (or a supported alternative), owner-scoped, with a retention period. Acceptance: a session survives a new revision, and a second user still gets 404 on it.
- **G07 Decide live CQL search versus a semantic index** (discovery) — 3–6 h; primary `adk-memory-architecture`. Run the G02 gold set against a trial index of the runbook spaces (Vertex AI Search or RAG Engine) and compare hit@5, freshness and cost. Stop after one comparison. Decision recorded; a build goal follows only if the index wins by ≥ 2 gold questions.
- **G08 Tickets attributed to the requesting staff member** — 4.5–9 h; primary `adk-tool-auth-and-secrets`. Either set `reporter` from a verified email → Jira accountId mapping (needs the "modify reporter" permission) or use per-user Atlassian OAuth (larger; re-estimate). Acceptance: the ticket's reporter is the confirming user, and another user's identity cannot be chosen.
- **G09 30-case evaluation set gated in CI, plus outcome survey** — 6–12 h; primary `adk-agent-evaluation`, supporting `adk-release-engineering`. Acceptance: CI fails on a regression below the agreed threshold, and a 5-question staff survey before and after is recorded.
- **G10 Traces and token cost per conversation** — 3–6 h; primary `adk-agent-observability`. Acceptance: one trace per invocation with tool spans and token counts, without content.
- **G11 Runbook secret scan and expanded adversarial suite** — 4.5–9 h; primary `adk-agent-security`, supporting `protect-adk-sensitive-data`. Acceptance: a scan report of runbook spaces handed to space owners, and ≥ 10 adversarial cases with 0 forbidden POSTs.
- **G12 Uncertain-create reconciliation hardened** — 3–6 h; primary `safe-api-tool-calls`. Trigger: a duplicate or uncertain ticket is seen in phase 1. Acceptance: a durable operation record survives restart, and a retry of the same operation finds rather than re-creates.

## Later

| Item | Trigger that brings it forward | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| Per-user daily request allowance | Spend above 50% of the allowance by mid-month | Budget alert is observation only | `adk-operational-guardrails` |
| Streaming answers | Staff complain about waiting; p90 > 15 s | Answer appears all at once | `adk-frontend-integration` |
| Google Chat entry point | Staff ask to use it inside Chat | Separate browser tab | `adk-frontend-integration` |
| Restricted runbook spaces with per-user permissions | Any restricted space is needed | Only open spaces are allow-listed | `adk-tool-auth-and-secrets` |
| Read, transition or comment on existing tickets | Requested by the helpdesk lead | Not possible from the assistant | `safe-api-tool-calls` |
| SLOs and alerts | Use by teams beyond the helpdesk | Problems found by users | `adk-agent-observability` |
| Canary and joint rollback | A second deployer, or a weekly release cadence | Manual rollback to the previous revision | `adk-release-engineering` |
| Model migration | Vertex retirement announced for `gemini-3.8-flash` (check the lifecycle table monthly) | — | `adk-release-engineering` |

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| [Design](../architecture/helpdesk-assistant.md) | Method, assumptions and decisions |
| `eval/` gold run summary (created by G02) | Latest retrieval and citation result |
| This plan | Remaining limits, deferred controls and evidence per goal |

## Open decisions for further planning

| Decision / question | Known facts and alternatives | Evidence or user decision needed | Blocks which goals? |
| --- | --- | --- | --- |
| Sign-in system (A9) | IAP direct needs Google identities | Identity admin | G05 |
| Jira project, types and notifications (A7) | Placeholder `ITSD` / `ITSDTEST` | Jira admin, helpdesk lead | G03 live, G05 switch-over |
| Runbook spaces and editors (A6) | 1–3 spaces assumed | Space owners | G02 live |
| Region | Must host the pinned model | Cloud admin | G01 |
| Gold-set targets | 9/12 hit@5, 10/12 cited (provisional) | Helpdesk lead | G07 trigger |

## Resume here

- **Next goal:** G01, GCP foundation and a pinned model answering locally. It
  starts the calendar waits. G02's offline part can start in parallel.
- **Read first:** the design, then this plan.
- **Next action:** file the cloud admin and Atlassian admin requests, then
  create the repository skeleton with the pinned ADK.
- **Continuation prompt:**

```text
/adk-engineer Carry out G01 from docs/plans/helpdesk-assistant.md.
Read docs/architecture/helpdesk-assistant.md and preserve its accepted decisions.
Use deploy-adk-on-google-cloud with adk-model-and-output-contracts.
Work within the team's own GCP project and local machine, verify G01's acceptance
cases, and update the plan with actual evidence and remaining blockers.
```

After that goal, the same request without a goal ID continues with the next
ready one: `/adk-engineer Continue the next ready goal in docs/plans/helpdesk-assistant.md.`
