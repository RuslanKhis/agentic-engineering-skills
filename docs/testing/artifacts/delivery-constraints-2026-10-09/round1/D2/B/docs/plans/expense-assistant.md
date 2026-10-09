# Implementation plan: finance expense assistant

Status: draft; ready goals identified (D01, G01, G02 can start in parallel)
Architecture: [docs/architecture/expense-assistant.md](../architecture/expense-assistant.md)
Continuation source of truth: this plan

## Destination and constraints

A read-only ADK assistant on Cloud Run behind IAP that answers expense-policy
questions with citations and shows a signed-in finance employee their own
claims from PostgreSQL. Non-goals: writes, other employees' claims, streaming.
Decisions D1–D10 and assumptions A1–A10 are in the design; all are provisional
until the user confirms them.

Inherited pins: `google-adk==2.8.0` (working assumption, confirm in G01),
model `gemini-3.8-flash` on Vertex AI (fallback `gemini-3.5-flash`), prompt
version `v1`, policy version from the bundle. Changing any of these is a
release, not a side effect of a goal.

Repository inspected: empty except `.claude/skills/`. Every module below is a
**proposed** layout:

```text
expense_assistant/
  agent.py          # LlmAgent factory, instruction v1, RunConfig
  tools/policy.py   # lookup_policy over policy bundle
  tools/claims.py   # list_my_claims, get_my_claim (reviewed SQL)
  identity.py       # IAP JWT verification, email -> employee_id
  server.py         # FastAPI: /api/turn, /api/session, static page
  policy/           # sections/*.md + manifest.json (policy_version)
  static/index.html # text-only chat page, CSP
tests/              # unit, scripted-model Runner tests, fixtures
evals/              # regression set
release.json        # release manifest
```

No credentials or private resource identifiers belong in this plan; use
placeholders such as `<PROJECT>`, `<REGION>`, `<INSTANCE>`.

## Delivery profile and capacity

Profile: **internal tool** (see design, "Delivery constraints").

| Phase | Delivers | Goals | Estimate (focused hours) | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship | 40 finance colleagues use it with their own identity on real policy and their own claims | D01, G01–G05 | 32–43 | 2 × 0.5 × 15 d × 6 h × 0.6 ≈ 54 h; reserve 11–22 h |
| 2, harden or graduate | DB-enforced scope, persistent sessions, policy release process, feedback loop, adversarial suite | G06–G10 | 25–35 | When the team has time |

Estimates assume engineers new to ADK and comfortable with GCP. Parallel
tracks: engineer A: G01 → G04; engineer B: D01 → G02 → G03; both: G05.
If time runs out early, stop after G03: a deployed policy-only assistant is
useful on its own and holds no personal data.

**Cut line (for the user to confirm or move):** phase 1 = D01, G01–G05,
about 37 of 54 hours. Phase 2 = G06–G10.

## Implementation map

| Decision / requirement | ADK or application component and integration point | GCP service/responsibility | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |
| D1, D6 one agent, pinned model | `LlmAgent` in `agent.py`, invoked by `Runner` from `server.py`; `RunConfig(max_llm_calls=6)` | Vertex AI (service account, keyless) | `adk-agent-instructions` | ADK 2.8.0 APIs; 3.8-flash on Vertex in `<REGION>` |
| D2 policy retrieval | `lookup_policy` function tool over packaged bundle | None | `adk-memory-architecture` | Policy source format (A7) |
| D3 identity scope | `identity.py` verifies IAP JWT; handler creates the session with `user_id=email` and state `employee_id`; tools read `tool_context.state` | IAP, Google Group | `adk-tool-auth-and-secrets` | IAP JWT audience format for Cloud Run |
| D4, D5 claims lookup | `tools/claims.py` reviewed SQL on views via Cloud SQL Python Connector (IAM auth) | Cloud SQL role `expense_assistant_ro` | `adk-tool-auth-and-secrets` | Schema and IAM DB auth (D01) |
| D7 hosting | Container with `server.py` entrypoint | Cloud Run, IAP, ingress internal + LB or IAP-for-Cloud-Run | `deploy-adk-on-google-cloud` | IAP-on-Cloud-Run setup path in `<REGION>` |
| D8 browser | `/api/turn` completed JSON; text rendering; CSP | Same service | `adk-frontend-integration` | Browser check |
| D9 budget | `max_llm_calls`; per-user daily counter in handler | Billing budget alert | `adk-operational-guardrails` | — |
| I6 logs | Allow-listed structured logger; ADK content capture off | Cloud Logging | `adk-agent-observability` | Hosted read-back |

## Goals and dependencies

| ID and goal | Phase | Type | Estimate | Depends on | Primary skill | State / blocker |
| --- | --- | --- | --- | --- | --- | --- |
| D01 Confirm DB, identity mapping and policy source | 1 | discovery | 2–3 h | — | `adk-tool-auth-and-secrets` | ready (needs a DBA conversation) |
| G01 Policy Q&A agent with citations, locally | 1 | implementation | 7–9 h | — | `adk-memory-architecture` | ready |
| G02 Authenticated chat API and page, locally | 1 | implementation | 5–7 h | — (stubs agent until G01) | `adk-frontend-integration` | ready |
| G03 Deploy policy-only assistant on Cloud Run behind IAP | 1 | implementation | 7–9 h | G01, G02 | `deploy-adk-on-google-cloud` | proposed; needs `<PROJECT>` and deploy authorisation |
| G04 Own-claims lookup with enforced scope | 1 | implementation | 7–9 h | G01; D01 for real DB | `adk-tool-auth-and-secrets` | ready on a local fixture |
| G05 Regression set, release gate and rollout to 40 users | 1 | implementation | 4–6 h | G03, G04 | `adk-agent-evaluation` | proposed |
| G06 PostgreSQL row-level security | 2 | implementation | 4–6 h | G04 | `adk-tool-auth-and-secrets` | proposed |
| G07 Persistent sessions with retention | 2 | implementation | 5–7 h | G05 | `adk-memory-architecture` | proposed |
| G08 Governed policy release process | 2 | implementation | 4–6 h | G05 | `adk-memory-architecture` | proposed |
| G09 Feedback capture and production-sample evals | 2 | implementation | 6–8 h | G05 | `adk-agent-observability` | proposed |
| G10 Adversarial suite for cross-user and injection attempts | 2 | implementation | 4–6 h | G04 | `adk-agent-security` | proposed |

### D01 — Confirm database, identity mapping and policy source

- **Phase and estimate:** 1; 2–3 h.
- **Outcome and linked decisions:** settles A6, A7, A8 for D2, D3, D5.
- **Scope:** questions to the DBA and finance controller; read the claims and employees schema (no data copied); confirm IAM DB auth is enabled on the instance; confirm where the policy docs live and who approves them; confirm region.
- **Depth:** discovery only; no grants created.
- **Implementation route:** written answers appended to the design's Assumed answers table; draft SQL for views `v_my_claims` and `v_employees` and the `expense_assistant_ro` role, for the DBA to review.
- **Prerequisites:** access to a DBA and the finance controller.
- **Primary skill:** `adk-tool-auth-and-secrets`.
- **Supporting skills:** `adk-sql-agent-engineering` (reviewed read-only query shape).
- **Acceptance:** each of A6–A8 is marked confirmed or corrected; view and role DDL reviewed by the DBA; if IAM DB auth is unavailable, D5 switches to the Secret Manager fallback in the design.
- **Verification:** document review; no live queries.
- **Execution scope:** local documents only; creating the role is a DBA action outside this goal.
- **Stopping condition:** answers recorded or 3 h spent; unanswered items stay open decisions, G04 continues on the fixture.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out D01 from docs/plans/expense-assistant.md. Read docs/architecture/expense-assistant.md, use the goal's primary and supporting skills, record the confirmed answers and the reviewed view/role DDL in the design.`

### G01 — Policy Q&A agent with citations, locally

- **Phase and estimate:** 1; 7–9 h (includes ~2 h ADK setup).
- **Outcome and linked decisions:** an engineer asks a policy question in `adk web` or a script and gets a cited answer; D1, D2, D6, D9, I4, I5.
- **Scope:** `agent.py`, `tools/policy.py`, policy bundle (real docs if D01 has them, otherwise a fixture policy), instruction v1, `RunConfig(max_llm_calls=6)`, 8 checked policy cases. Excludes claims, web server, deployment.
- **Depth:** internal-tool core judgment; floor: pinned model ID, call cap, no secrets (Vertex via ADC).
- **Implementation route:** `LlmAgent(model="gemini-3.8-flash", tools=[lookup_policy])`; bundle = `policy/sections/*.md` + `manifest.json` with `policy_version`; in-process BM25 ranking; result `{status, policy_version, sections:[{id,title,text}]}` capped at 6 KB; today's date injected by code.
- **Prerequisites:** Python 3.11+, `google-adk==2.8.0` pinned in `pyproject.toml`, a dev GCP project with Vertex AI enabled.
- **Primary skill:** `adk-memory-architecture`.
- **Supporting skills:** `adk-agent-instructions` (instruction v1, citation and "not covered" behaviour); `adk-tool-interface-design` (`lookup_policy` declaration and result bound); `adk-model-and-output-contracts` (confirm model pin and Vertex availability, thinking setting).
- **Acceptance:** 8 policy cases answered with the expected section ID; a "not covered" question returns the contact-finance answer without invention; a scripted model that keeps calling tools stops at 6 calls; ADK 2.8.0 API names confirmed; `gemini-3.8-flash` confirmed on Vertex in `<REGION>` or the pin switched to `gemini-3.5-flash` and the design updated.
- **Verification:** offline pytest (tool ranking, size bound, scripted-model cap); bounded live run of the 8 cases (≤ 50 model calls).
- **Execution scope:** local code and a dev Vertex project; live calls need the engineer's own project.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G01 from docs/plans/expense-assistant.md. Read docs/architecture/expense-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G02 — Authenticated chat API and page, locally

- **Phase and estimate:** 1; 5–7 h.
- **Outcome and linked decisions:** a local page sends a message and shows the answer for a verified user; D3, D8, I1, I6, I7.
- **Scope:** `server.py` (FastAPI), `identity.py` (IAP JWT verification with a test key locally), session create/turn endpoints, session ownership check, one in-flight turn per session, per-user daily cap, allow-listed logger, `static/index.html` rendering text only with CSP. Agent stubbed until G01 lands.
- **Depth:** identity is build; logging minimal; no streaming.
- **Implementation route:** handler verifies JWT → email → (G04 adds `employee_id`) → `Runner.run_async` with `user_id=email`; JSON response `{turn_id, text, status}`.
- **Prerequisites:** none (G01 for the real agent).
- **Primary skill:** `adk-frontend-integration`.
- **Supporting skills:** `adk-tool-auth-and-secrets` (JWT verification, session ownership); `adk-agent-observability` (log allow-list, ADK content capture off).
- **Acceptance:** missing/forged/expired JWT → 401; another user's session ID → 404; overlapping turn → 409; 61st turn of the day → limit message; log records contain no message text; a crafted answer with a markdown image renders as literal text.
- **Verification:** offline pytest with httpx test client; manual browser check.
- **Execution scope:** local only.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G02 from docs/plans/expense-assistant.md. Read docs/architecture/expense-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G03 — Deploy policy-only assistant on Cloud Run behind IAP

- **Phase and estimate:** 1; 7–9 h (first IAP setup is the main risk).
- **Outcome and linked decisions:** finance-group members use policy Q&A in the browser; non-members are refused; D7, I1, I6.
- **Scope:** container, service account `sa-expense-assistant` with Vertex AI user role, Cloud Run `max-instances=1`, IAP restricted to `finance-assistant-users`, ingress restricted, billing budget alert, `release.json`, GitHub Actions unit-test workflow. Claims tools are not deployed yet.
- **Depth:** hosting and release minimal; observability minimal.
- **Implementation route:** per `deploy-adk-on-google-cloud` for Cloud Run; JWT audience configured from the deployed service; release manifest records image digest, ADK version, model ID, prompt and policy versions, tool schema hash.
- **Prerequisites:** G01, G02; `<PROJECT>` and `<REGION>` (A8); explicit authorisation to deploy and change IAM.
- **Primary skill:** `deploy-adk-on-google-cloud`.
- **Supporting skills:** `adk-release-engineering` (manifest, pinned versions, CI); `adk-agent-observability` (structured logs, token counts, hosted log read-back).
- **Acceptance:** member account gets a cited answer; non-member gets 403; logs for a test turn contain no message text; manifest matches the serving revision; Vertex price for the pinned model looked up and the cost formula in the design filled in.
- **Verification:** hosted checks (authorised), CI run green.
- **Execution scope:** **not yet authorised**; needs the user's go-ahead for the named project.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G03 from docs/plans/expense-assistant.md. Read docs/architecture/expense-assistant.md, use the goal's primary and supporting skills, deploy only to the project I name, verify its acceptance cases and record evidence here.`

### G04 — Own-claims lookup with enforced scope

- **Phase and estimate:** 1; 7–9 h.
- **Outcome and linked decisions:** a signed-in user asks "where is my taxi claim?" and sees only their own claims; D3, D4, D5, I2, I3.
- **Scope:** `tools/claims.py` with `list_my_claims` and `get_my_claim`, email → `employee_id` lookup in the handler, local Postgres fixture with two employees, view/role DDL from D01, Cloud SQL connector config. Excludes RLS (G06).
- **Depth:** identity and scope build; sensitive data minimal (field-minimised results).
- **Implementation route:** tools read `employee_id` from `tool_context.state`; SQL `SELECT … FROM v_my_claims WHERE employee_id = $1 AND …` with `limit ≤ 20`; results `{status: ok|empty|truncated|not_found|unavailable, as_of, claims:[…]}`; DB errors → `unavailable`, never `empty`.
- **Prerequisites:** G01; D01 for the real schema (fixture otherwise); G02 for the trusted state write.
- **Primary skill:** `adk-tool-auth-and-secrets`.
- **Supporting skills:** `adk-tool-interface-design` (two tool declarations, result shape); `adk-sql-agent-engineering` (reviewed parameterised read-only queries).
- **Acceptance:** user A sees A's claims; user A asking for B's claim ref gets `not_found`; tool declarations have no identity parameter; DB down → "unavailable" answer, not "no claims"; role cannot `INSERT/UPDATE/DELETE` (grant test); unmapped email → claims unavailable, policy still works.
- **Verification:** offline pytest against local Postgres (container or fixture) with a scripted model; deployed check after G03 with two test accounts (authorised).
- **Execution scope:** local; role creation on the real instance is a DBA action.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G04 from docs/plans/expense-assistant.md. Read docs/architecture/expense-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G05 — Regression set, release gate and rollout to 40 users

- **Phase and estimate:** 1; 4–6 h.
- **Outcome and linked decisions:** a ~25-case regression set (12 policy, 8 own-claims, 5 refusal/adversarial) run before each release; rollout to the group; I4, I5, outcome hypothesis A9.
- **Scope:** `evals/` cases on fixture data, a run script with a call cap and pass threshold, release checklist, baseline count of finance-mailbox questions (A9), pilot with 5 users then the group.
- **Depth:** internal-tool evaluation (small regression set, manual pre-release run, not a CI gate).
- **Primary skill:** `adk-agent-evaluation`.
- **Supporting skills:** `adk-release-engineering` (record eval-set hash and result in `release.json`).
- **Acceptance:** regression set passes at the agreed threshold (proposed ≥ 23/25, with all refusal cases passing); p95 complete-answer latency measured; 5-user pilot feedback recorded; group rollout done.
- **Verification:** local eval run with recorded results; hosted rollout authorised separately.
- **Execution scope:** eval locally; rollout needs the user's go-ahead.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G05 from docs/plans/expense-assistant.md. Read docs/architecture/expense-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### Phase 2 goals (coarse; refine after phase 1 results)

- **G06 PostgreSQL row-level security** — `SET LOCAL app.employee_id` per transaction plus an RLS policy on the claims view, so a code bug cannot leak rows. Primary `adk-tool-auth-and-secrets`; supporting `adk-sql-agent-engineering`. Acceptance: with the app's `WHERE` clause removed in a test, rows of other employees are still not returned.
- **G07 Persistent sessions** — `DatabaseSessionService` on a separate database (not the expense DB), retention (e.g. 30 days) and deletion job; allows `max-instances > 1`. Primary `adk-memory-architecture`; supporting `deploy-adk-on-google-cloud`. Acceptance: conversation survives a restart for its owner only; expired sessions removed.
- **G08 Governed policy release process** — export from the policy source, controller approval, version bump, staged eval before promotion. Primary `adk-memory-architecture`; supporting `adk-release-engineering`.
- **G09 Feedback and production-sample evals** — thumbs up/down with reason, redacted sampled sessions into `evals/`. Primary `adk-agent-observability`; supporting `adk-agent-evaluation`, `protect-adk-sensitive-data`.
- **G10 Adversarial suite** — scripted cross-user and injection attempts asserting forbidden tool calls never run. Primary `adk-agent-security`; supporting `adk-agent-evaluation`.

## Later

| Item | Trigger that brings it forward | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| Finance-reviewer access to other employees' claims | Product owner confirms A4 the other way | Reviewers keep using the expense system UI | `adk-tool-auth-and-secrets` |
| SLOs, alerts | Rollout beyond finance or two incidents/month | Problems reported by users, not alerts | `adk-agent-observability` |
| Canary and joint rollback | > 1 release/week or a second team | Rollback is manual revision switch | `adk-release-engineering` |
| Model Armor / SDP screening | Third-party content enters context | Own-data-only exposure | `protect-adk-sensitive-data` |
| Managed retrieval (Vertex AI Search/RAG Engine) | Policy corpus > ~200 pages or retrieval misses in eval | In-process ranking | `adk-memory-architecture` |
| Streaming responses | p95 complete answer > 10 s and users complain | Users wait for full answer | `adk-frontend-integration` |
| Model migration off `gemini-3.8-flash` | A shutdown/retirement date is announced | — (calendar check monthly) | `adk-release-engineering` |
| Write actions (submit/annotate claims) | Explicit product request | — | `safe-api-tool-calls` |

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| [Design](../architecture/expense-assistant.md) | Method, assumptions and decisions |
| `evals/README.md` (created in G05) | Latest regression result per case |
| This plan | Remaining limits and deferred controls |

## Open decisions for further planning

| Decision / question | Known facts and alternatives | Evidence or user decision needed | Blocks which goals? |
| --- | --- | --- | --- |
| Reviewer access (A4) | Request says "own"; finance staff often need others' | Product owner | None in phase 1; reshapes G06 |
| DB facts (A6) | Assumed Cloud SQL + IAM DB auth | DBA via D01 | Real-DB part of G04 |
| Policy source (A7) | Assumed a few docs, controller approves | Finance controller via D01 | Real content in G01 |
| Region (A8) | Same as Cloud SQL | IT/security | G03 |
| Deploy authorisation | None given | User names `<PROJECT>` and approves IAM changes | G03, G05 rollout |

## Resume here

- **Next goal:** G01 — Policy Q&A agent with citations, locally. Ready: needs no external decision; a fixture policy works until D01 answers A7. D01 and G02 can run in parallel by the second engineer.
- **Read first:** docs/architecture/expense-assistant.md, this plan.
- **Next action:** create `pyproject.toml` pinning `google-adk==2.8.0` and confirm the APIs named in the design against that version.
- **Continuation prompt:**

```text
/adk-engineer Carry out G01 — Policy Q&A agent with citations, locally — from docs/plans/expense-assistant.md.
Read docs/architecture/expense-assistant.md and preserve its accepted decisions.
Use adk-memory-architecture with adk-agent-instructions, adk-tool-interface-design and adk-model-and-output-contracts.
Work within local code and the engineer's dev Vertex project, verify the 8 policy cases, the "not covered" case and the 6-call cap, and update
the plan with actual evidence and remaining blockers.
```

After that goal: `/adk-engineer Continue the next ready goal in docs/plans/expense-assistant.md.`
