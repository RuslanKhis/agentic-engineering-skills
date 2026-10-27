# Implementation plan: ADK support assistant (pilot)

Status: draft, goals identified. Phase 1 goals G01 to G07 are ready in design; none has started.
Architecture: [../architecture/support-assistant.md](../architecture/support-assistant.md) (contracts C1 to C9, decisions D1 to D10, open decisions O1 to O8, assumed answers Q1 to Q15)
Continuation source of truth: this plan (no tickets written; goals-only)

## Summary for the reader

- **Profile and phase 1:** MVP or pilot. Phase 1 (G01 to G07) is local only: a React chat and settings panel on a FastAPI service with a scripted model and local PostgreSQL. A signed-in test user can save and delete a reply language, replies stream, and every failure shows honestly. No cloud, no real model, no real data. Phase 1 ends with a pilot go-ahead review (G07).
- **Effort and finish:** phase 1 is 24.5 to 43.5 human hours against about 54 usable hours (assumed one part-time developer new to ADK, 20 working days; Q2), so it fits at the high end; finish about 9 to 16 working days. Hand-computed, not yet run through the schedule helper (see below). The deadline is unknown.
- **Largest risks:** (1) ADK's behaviour when a stream fails midway (what is persisted, what is emitted) is unverified (O6, D6), settled by G01. (2) Streaming through Cloud Run may buffer or cut off (C5), settled by G09/A3 and first met locally in G01. (3) The model may not follow the saved language (C4), measured by G08.
- **Decisions needed from you:** O1 OIDC details, O3 allowance values and model spend cap, O5 language list, O7 audience and date for G07. Each has an assumption in the design, so local work does not wait.
- **Next prompt:** the block under "Resume here".

## What to build first, and why

Build **G01**: a streamed chat run from a FastAPI route through the real ADK Runner, with a scripted model that can fail midway, an in-memory stand-in for the preference store, and a test principal that fails closed. It is first because the stream and failure contract (C5, C6) is the part where unknowns can change everything after it: the event schema, what ADK stores after a failed run, how the React client decides a reply is finished. It needs no cloud credentials, no database and no model key. Preference storage (G02) is ordinary CRUD with known behaviour, so it follows. Identity hardening (G04) and the React screen (G03) both consume G01's contract.

If time runs out early, each finished goal is still useful in this order: G01 (honest streaming backend), G02 (save and delete), G04 (real token verification), G03 (UI), G05 (persistence and spend stops), G06 (journey), G07 (review).

## Destination and constraints

Useful end result: pilot users on Cloud Run can save, use and delete a reply language, with streamed replies and honest failure states. Non-goals: group-account preferences (outside this release), tools or actions by the agent, RAG, uploads, cross-session memory, multi-instance scaling. Accepted stack: React, OIDC, PostgreSQL, Cloud Run, Python ADK with FastAPI (D2). Current authorisation: **documentation only**. Phase 1 implementation and local testing is the intended next phase but needs your go-ahead in the implementing session; deployment, IAM, paid model calls and any cloud resource are not authorised.

Inspected facts: none. No source tree, ADK version or credentials were given, so every module path below is **proposed**. Working assumption for versions: the specialists were checked against `google-adk` 2.8.0 / `google-genai` 2.19.0, with a gateway read against 2.12.0 (`adk-frontend-integration/references/compatibility.md`); G01/A8 confirms the real pin. Model ID, judge ID and prompt version are unset until G08.

Proposed layout (keep the project's own structure if one turns up):

```text
backend/app/{main,settings,principal,agent_routes,errors}.py  backend/app/routes/reply_language.py
backend/agent/            backend/migrations/ (application schema only)   backend/tests/
frontend/src/{client,routes,components}/     docs/design/DESIGN.md (only if the existing app has none)
AGENTS.md  CLAUDE.md (one line: @AGENTS.md)  Makefile (dev, check, e2e)
```

## Delivery profile and capacity

| Phase | Delivers | Goals | Human hours, agent-assisted | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship locally | The journey end to end on scripted model and synthetic data, plus the go-ahead review | G01 to G07 | from the schedule check | assumed 1 developer × 3.6 focused h/day × 20 days, 25% reserve |
| 2, pilot on Cloud Run | Live model, staging and pilot deployment, real IdP, governance, results review | G08 to G13 | from the schedule check | after W2 |

Estimates are person-hours (hands-on plus review) with a coding agent, assumptions for one developer new to ADK. The **×1.5 new-to-ADK multiplier is already applied to G01 to G06 and G08 to G11**; G07, G12 and G13 are document and stakeholder work and are not multiplied. A first GCP project, billing and IAM add about a day to G09 and are an administrator wait if the account is organisation-managed. Calendar waits: W1 OIDC provider details and client registration, W2 pilot go-ahead decision after G07, W3 model access and spend cap, W4 governance sign-off. The wait lengths are assumptions until the people involved confirm them; W1 and W3 should be requested on day 1 so they run in parallel.

```yaml
- goal: W1
  phase: 2
  total: 0
  wait_days: 5
  blocked_by: []
  calendar_waits: OIDC issuer, audience, client registration (assumed length)
  type: discovery
- goal: W3
  phase: 2
  total: 0
  wait_days: 3
  blocked_by: []
  calendar_waits: model access and owner-set spend cap (assumed length)
  type: discovery
- goal: G01
  phase: 1
  hands_on: 3-5
  review: 1.5-2.5
  total: 4.5-7.5
  owner: Dev A
  blocked_by: []
  calendar_waits: none
  wait_days: 0
  handoff: 0
  contracts: [C1, C5, C6, C8]
  security: [SB01, SB05, SB13, SB16, SB17]
  type: implementation
  status: planned
- goal: G02
  phase: 1
  hands_on: 2-4
  review: 1-2
  total: 3-6
  owner: Dev A
  blocked_by: [G01]
  calendar_waits: none
  wait_days: 0
  handoff: 0
  contracts: [C2, C3, C4]
  security: [SB04, SB09]
  type: implementation
  status: planned
- goal: G04
  phase: 1
  hands_on: 1.5-3.5
  review: 1.5-2.5
  total: 3-6
  owner: Dev A
  blocked_by: [G01]
  calendar_waits: none
  wait_days: 0
  handoff: 0
  contracts: [C1]
  security: [SB03, SB08, SB13, SB14]
  type: implementation
  status: planned
- goal: G03
  phase: 1
  hands_on: 4-6
  review: 2-3
  total: 6-9
  owner: Dev A
  blocked_by: [G01, G02]
  calendar_waits: none
  wait_days: 0
  handoff: 0
  contracts: [C5, C6, C7]
  security: [SB08, SB10]
  type: implementation
  status: planned
- goal: G05
  phase: 1
  hands_on: 2-4
  review: 1-2
  total: 3-6
  owner: Dev A
  blocked_by: [G01, G02]
  calendar_waits: none
  wait_days: 0
  handoff: 0
  contracts: [C8, C9]
  security: [SB09, SB19]
  type: implementation
  status: planned
- goal: G06
  phase: 1
  hands_on: 1-2
  review: 1-2
  total: 2-4
  owner: Dev A
  blocked_by: [G03, G04, G05]
  calendar_waits: none
  wait_days: 0
  handoff: 0
  contracts: [C1, C3, C5, C6, C7]
  security: [SB15]
  type: journey
  status: planned
- goal: G07
  phase: 1
  hands_on: 2-3
  review: 1-2
  total: 3-5
  owner: Dev A
  blocked_by: [G06]
  calendar_waits: none
  wait_days: 0
  handoff: 0
  contracts: []
  security: []
  type: presentation
  status: planned
- goal: W2
  phase: 1
  total: 0
  wait_days: 5
  blocked_by: [G07]
  calendar_waits: pilot go-ahead decision (assumed length)
  type: discovery
- goal: G08
  phase: 2
  hands_on: 3-5
  review: 1-2
  total: 4-7
  owner: Dev A
  blocked_by: [G05, W3]
  calendar_waits: W3
  wait_days: 0
  handoff: 0
  contracts: [C4, C8]
  security: []
  type: implementation
  status: planned
- goal: G09
  phase: 2
  hands_on: 3-6
  review: 2-3
  total: 5-9
  owner: Dev A
  blocked_by: [G06, W2]
  calendar_waits: W2
  wait_days: 0
  handoff: 0
  contracts: [C5, C2]
  security: [SB06, SB07, SB21]
  type: implementation
  status: planned
- goal: G10
  phase: 2
  hands_on: 2-4
  review: 2-3
  total: 4-7
  owner: Dev A
  blocked_by: [G04, G09, W1]
  calendar_waits: W1
  wait_days: 0
  handoff: 0
  contracts: [C1]
  security: [SB02, SB20, SB22]
  type: implementation
  status: planned
- goal: G11
  phase: 2
  hands_on: 3-6
  review: 2-3
  total: 5-9
  owner: Dev A
  blocked_by: [G09]
  calendar_waits: none
  wait_days: 0
  handoff: 0
  contracts: [C6]
  security: [SB14]
  type: implementation
  status: planned
- goal: G12
  phase: 2
  hands_on: 2-4
  review: 1-2
  total: 3-6
  owner: Dev A
  blocked_by: [G09]
  calendar_waits: none
  wait_days: 0
  handoff: 0
  contracts: []
  security: []
  type: governance
  status: planned
- goal: W4
  phase: 2
  total: 0
  wait_days: 10
  blocked_by: [G12]
  calendar_waits: counsel and DPO sign-off (assumed length)
  type: discovery
- goal: G13
  phase: 2
  hands_on: 2-3
  review: 1-2
  total: 3-5
  owner: Dev A
  blocked_by: [G08, G10, G11, W4]
  calendar_waits: W4
  wait_days: 0
  handoff: 0
  contracts: []
  security: []
  type: presentation
  status: planned
```

Longest dependent chain and finish range: **not run through `check_schedule.py`** (no shell was available in this session), so these are hand sums to be re-run with `python3 "$SKILL_DIR/scripts/check_schedule.py" --plan docs/plans/support-assistant.md --design docs/architecture/support-assistant.md --days 20 --reserve 0.25 --person "Dev A=3.6"` (needs Python 3.11 or later). Hand figures: phase 1 is 24.5 to 43.5 hours (G01 4.5–7.5, G02 3–6, G04 3–6, G03 6–9, G05 3–6, G06 2–4, G07 3–5). Capacity is 20 days × 3.6 h = 72 h, or 54 h after a 25% reserve, so the high end fits. One person works the goals in sequence, so the finish is about 7 to 12 working days, or 9 to 16 with the reserve on the calendar. The longest dependent chain (G01, G02, G03, G06, G07) is 18.5 to 31.5 h and is shorter than the single person's load. W2 then adds an assumed 5 working days before phase 2. Phase 2 is 24 to 43 h plus waits W1, W3 (parallel, from day 1) and W4 (10 days, after G12). The helper may also list goal mentions or outside-approval mentions for settlement; none have been settled here. Not yet checked by the helper: that every grid cell cites an existing acceptance item (hand-checked against G01 to G05 and the phase 2 items) and rule and contract coverage.

## Implementation map

| Contract / decision | Component and integration point (all proposed) | GCP responsibility | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |
| C1, D7 | `principal.py` dependency; Runner called with the principal's ID | OIDC provider (existing) | `adk-frontend-integration` (routes, SB03); `adk-tool-auth-and-secrets` for ownership rules | Real IdP claims (O1) |
| C2, C3, D3, D8 | `routes/reply_language.py`; app-schema table; Alembic job | PostgreSQL (existing instance assumed) | `adk-memory-architecture` | Existing instance and schema ownership (O2) |
| C4, D4, D10 | Run route loads the value and renders a per-run instruction; agent factory has zero tools | Model endpoint | `adk-agent-instructions` | ADK mechanism for a per-run instruction against the pin |
| C5, C6, D5, D6 | `agent_routes.py` stream route and event schema; browser stream reader | Cloud Run request timeout and streaming | `adk-frontend-integration` | What ADK persists after a mid-stream failure (O6); Cloud Run buffering |
| C8, D9 | Admission check, `RunConfig.max_llm_calls`, per-user counters; process-local lock | Model project quota; `max-instances` 1 | `adk-operational-guardrails` | Allowance values (O3) |
| C9, D8 | `DatabaseSessionService` on the ADK schema | PostgreSQL | `adk-memory-architecture` | Pin supports the needed service |

## Web stack and companion skills

Defaults come from the designer's web-application defaults, pins last checked 23 October 2026 and to be re-confirmed by G01. Deviation: the React app already exists (Q5), so its router, data layer and design system win over the defaults (D1). The first goal writes the table below into `AGENTS.md` with the pins it resolves, then this section becomes a link.

| Companion | Install | Load when | Scope notes |
| --- | --- | --- | --- |
| `fastapi` | `uv sync && uvx library-skills --claude` | G01, G02, G04, G05 | Idioms only; identity and ownership follow the design |
| `playwright-cli` | `npm i -g @playwright/cli@0.1.22`, then `playwright-cli install --skills` | G03, G06 | Role locators; never wait for network idle on a streaming page |
| `shadcn`, `vercel-react-best-practices`, `react-router` | `npx skills add` forms in web-application defaults | G03, only if the existing app uses them | Skip `server-` rules; TanStack Query not SWR |

Setup prerequisite: these specialist skills are named by the plan but are **not installed in this workspace**: `adk-fastapi-backend`, `adk-agent-instructions`, `adk-model-and-output-contracts`, `adk-operational-guardrails`, `adk-agent-observability`, `adk-release-engineering`, `adk-agent-security`, `adk-governance-pack`, `adk-presenter`, `deploy-adk-on-google-cloud`. Installed here: `adk-engineer`, `adk-frontend-integration`, `adk-memory-architecture`, `adk-agent-evaluation`, `adk-tool-auth-and-secrets`, `adk-system-designer`. Until a missing one is installed, the goal uses the installed primary skill and the companion, and notes in Evidence that the specialist's guidance was not applied.

## Goals and dependencies

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | State |
| --- | --- | --- | --- | --- | --- | --- |
| G01 Streamed run skeleton with honest failure | 1 | implementation | 4.5–7.5 | none | `adk-frontend-integration` | ready in design |
| G02 Save and delete reply language | 1 | implementation | 3–6 | G01 | `adk-memory-architecture` | ready after G01 |
| G04 Verified OIDC principal and denial tests | 1 | implementation | 3–6 | G01 | `adk-frontend-integration` | ready after G01 |
| G03 React chat and settings with honest states | 1 | implementation | 6–9 | G01, G02 | `adk-frontend-integration` | after G01, G02 |
| G05 Persistent sessions and spend stops | 1 | implementation | 3–6 | G01, G02 | `adk-memory-architecture` | after G01, G02 |
| G06 Local end-to-end journey | 1 | journey | 2–4 | G03, G04, G05 | `adk-agent-evaluation` | proposed |
| G07 Pilot go-ahead review | 1 | presentation | 3–5 | G06 | `adk-presenter` | proposed |
| G08 Live model, pinned ID, adherence | 2 | implementation | 4–7 | G05, W3 | `adk-model-and-output-contracts` | blocked on W3 |
| G09 Staging and pilot on Cloud Run | 2 | implementation | 5–9 | G06, W2 | `deploy-adk-on-google-cloud` | blocked on W2 |
| G10 Real OIDC provider, revocation | 2 | implementation | 4–7 | G04, G09, W1 | `adk-tool-auth-and-secrets` | blocked on W1 |
| G11 Observability and release gate | 2 | implementation | 5–9 | G09 | `adk-agent-observability` | proposed |
| G12 Governance pack | 2 | governance | 3–6 | G09 | `adk-governance-pack` | proposed |
| G13 Pilot results review and first bill | 2 | presentation | 3–5 | G08, G10, G11, W4 | `adk-presenter` | proposed |

### G01 — Streamed run skeleton with honest failure

- **Phase and estimate:** 1; hands-on 3–5, review 1.5–2.5, total 4.5–7.5; no waits; owner Dev A.
- **Outcome, contracts and decisions:** a test user's message produces a streamed reply from a scripted model through the real Runner; failures end in one `error` event. Proves C1 (fail closed), C5, C6, C8 (slot release); implements D2, D5, D6, D10.
- **Scope:** FastAPI app, settings, test-principal override, stream route, event schema `delta|notice|done|error`, scripted-model fixtures, a `PreferenceStore` interface with an in-memory implementation, `Makefile`, `.env.example`, `AGENTS.md`. Excludes React, PostgreSQL and real tokens. Depth: floor plus Build for C5 and C6.
- **Implementation route:** `LlmAgent` with no tools in `backend/agent/`, run through the application's own Runner with a streaming `RunConfig` (mode name to verify against the pin); route in `agent_routes.py`. First step: confirm the ADK pin and the instruction-per-run mechanism (D4), then answer O6 by running a scripted mid-stream failure and recording what the session holds.
- **Resources created:** none.
- **Prerequisites:** none.
- **Primary skill:** `adk-frontend-integration`. **Supporting:** `adk-agent-evaluation` (scripted-model tests), `adk-agent-instructions` (not installed), `adk-fastapi-backend` (not installed). **Companion skills:** `fastapi`. **Design system:** none.
- **Security rules:** SB01, SB05, SB13, SB16, SB17.
- **Acceptance:**
  - A1 With no verifier configured, every `/api` route including the stream returns 401; the test-principal override refuses to load unless a dev setting is on (C1, SB01).
  - A2 A scripted model that emits three deltas with delays: over a real socket the client reads the first delta before the last is produced, then exactly one `done` and nothing after (C5).
  - A3 A scripted model that raises after two deltas: the client gets the two deltas, then exactly one `error` with a code, `partial: true`, a request ID and no provider text (C6, SB13).
  - A4 Client disconnect mid-stream cancels the run, releases the user's slot within a bounded time and makes no further scripted model calls (C5, C8).
  - A5 An empty reply, a blocked or refused finish reason and malformed model output each end in a coded `error`, never a blank `done` (C6).
  - A6 A route inventory test finds only `/api/*` and the health check; ADK's own server routes are absent (SB05).
  - A7 After A3, the incomplete assistant turn is not stored as a completed turn, or the gap and its handling are recorded as the O6 finding (C6).
  - A8 The ADK, `google-genai` and companion pins are confirmed and recorded, and the streaming and per-run instruction API names are checked against the pin (deliverable).
  - A9 `.env.example` holds no values; `make check` runs a secret scan that is clean (SB16).
  - A10 The agent factory declares zero tools, asserted by a test (SB17).
  - A11 No delta within the first-token deadline, or no terminal event within the total deadline, produces `error` with code `timeout` (C5, C6).
  - A12 A scripted provider 429 gives a retryable `error` with a bounded retry (at most one retry, none after the first delta) (C6, C8).
- **Verification:** offline scripted-model tests through the real Runner; A2 and A4 over real sockets (local integration). Command: `make check`.
- **Execution scope:** local, no network beyond installing dependencies the implementing session is separately authorised to install.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G01 from docs/plans/support-assistant.md. Read docs/architecture/support-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G02 — Save and delete reply language

- **Phase and estimate:** 1; hands-on 2–4, review 1–2, total 3–6; owner Dev A.
- **Outcome, contracts and decisions:** `GET/PUT/DELETE /api/me/reply-language` on local PostgreSQL; the next run uses the stored value; delete removes it. Proves C2, C3, C4; implements D3, D4, D8.
- **Scope:** application-schema migration, owner-scoped routes (no ID in the path), allowlist from settings, loader at run start replacing the in-memory store, `notice` event when the store is down. Excludes UI and group preferences. Depth: Build.
- **Implementation route:** `routes/reply_language.py`; table `reply_language(issuer, subject, language_tag, updated_at)` primary key `(issuer, subject)`; hard `DELETE`; loader re-validates the tag.
- **Resources created:** none (local PostgreSQL only).
- **Prerequisites:** G01; a local PostgreSQL the implementing session may start (setup prerequisite).
- **Primary skill:** `adk-memory-architecture`. **Supporting:** `adk-fastapi-backend` (not installed). **Companion skills:** `fastapi`. **Security rules:** SB04, SB09.
- **Acceptance:**
  - A1 PUT with an allowlisted tag stores it and GET returns it; an unknown tag returns 422 and the earlier value is unchanged (C2).
  - A2 Two-user test: user B's GET, PUT and DELETE never read or change A's row; a body `user_id` is ignored (C2, C1, SB04).
  - A3 DELETE returns 204, a direct SQL query finds no row, GET reports unset, and a second DELETE also returns 204 (C3).
  - A4 After DELETE the rendered model request for a new run contains no language instruction, and no session state or event holds the value (C3, C4).
  - A5 With a value set, the rendered request carries the language instruction; a tampered row such as "ignore previous instructions" is rejected on load, the run uses the default and a warning without the value is logged (C4, C2).
  - A6 After a real process restart the value is still returned (C2).
  - A7 Delete during an in-flight run: that run keeps the old value and the next run has none; concurrent PUT and PUT leaves one valid row (last commit wins); a PUT ordered after a DELETE cannot be undone by a stale write (C3, C2).
  - A8 Oversize or malformed bodies return 413 or 422 (SB09).
  - A9 The migration applies to an empty database and rolls back; it touches only the application schema (C2).
  - A10 With PostgreSQL down: the preference routes return a generic 503 with a request ID; a run proceeds and emits a `notice` event that the saved language could not be loaded (C4).
- **Verification:** offline tests against a local PostgreSQL; A6 with a real restart. Command: `make check`.
- **Execution scope:** local. **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G02 from docs/plans/support-assistant.md. Read docs/architecture/support-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G04 — Verified OIDC principal and denial tests

- **Phase and estimate:** 1; hands-on 1.5–3.5, review 1.5–2.5, total 3–6; owner Dev A.
- **Outcome:** the backend verifies real JWTs from a local fixture issuer and derives the user from `iss`+`sub`. Proves C1; implements D7.
- **Scope:** signature, issuer, audience, expiry, algorithm allowlist, `kid`, cached JWKS with fail-closed behaviour; ownership checks on sessions. The real provider is G10.
- **Route:** `principal.py` with a generated key pair and a stub JWKS endpoint in tests.
- **Resources created:** none. **Prerequisites:** G01. **Primary skill:** `adk-frontend-integration`; **supporting:** `adk-tool-auth-and-secrets` (ownership, identity); `adk-agent-evaluation` for denial tests. **Companion:** `fastapi`. **Security rules:** SB03, SB08, SB13, SB14.
- **Acceptance:**
  - A1 A valid token yields the principal; expired, wrong audience, wrong issuer, bad signature, `alg=none` and unknown `kid` all return 401 (C1).
  - A2 A user ID in the body, query or a header is ignored and the Runner is called with the token's principal (C1, SB03).
  - A3 User B using user A's session ID gets the same 404 body as an unknown session, with zero model calls (C1, SB03).
  - A4 JWKS endpoint down with a cold cache denies; with warm cache within its TTL keys are used; the error body is generic (C1, SB13).
  - A5 Tokens travel only in the `Authorization` header; a log-capture test finds no token and no message content, and a denied-access line with principal, route and request ID exists (SB08, SB14).
- **Verification:** offline with fixture issuer. **Execution scope:** local. **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G04 from docs/plans/support-assistant.md. Read docs/architecture/support-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G03 — React chat and settings with honest states

- **Phase and estimate:** 1; hands-on 4–6, review 2–3, total 6–9; owner Dev A.
- **Outcome:** a chat view and a reply-language control that follow D1, D5 and show every state C5 to C7 name. Proves C5, C6, C7.
- **Scope:** first step: inspect the existing React app if its source is supplied (O2); otherwise build a minimal shell under `frontend/` and record that porting is a follow-up. Stream reader over `fetch` with run-time event validation; status messages announced to assistive technology. Excludes real sign-in UI.
- **Route:** `frontend/src/routes`, generated client for JSON routes, a typed stream reader.
- **Resources created:** none. **Prerequisites:** G01, G02. **Primary skill:** `adk-frontend-integration`; **companions:** `playwright-cli`, plus `shadcn` and `vercel-react-best-practices` only if the existing app uses them. **Design system:** the existing app's; else `docs/design/DESIGN.md` from the house system. **Security rules:** SB08, SB10.
- **Acceptance:**
  - A1 Deltas render progressively in a browser test against a scripted stream, without waiting for network idle (C5).
  - A2 A mid-stream `error` leaves the partial text labelled incomplete with the error message, request ID and a retry action, and never uses completed-answer styling (C6).
  - A3 Save shows "saved" only after a 2xx and a re-read; a 422 or 5xx shows "not saved" and the previous value (C7).
  - A4 A write whose response never arrives shows "couldn't confirm", re-reads, then shows the real server state (C7).
  - A5 Delete returns the control to unset; the next message's request to the scripted backend carries no language instruction; the UI notes that earlier conversation text is not erased (C3, C7).
  - A6 A scripted reply containing an `<img onerror>` payload, a `javascript:` link and an image from an unlisted host renders inert (SB10).
  - A7 Requests carry the token by `fetch` header; no `EventSource`, no token in a URL (SB08).
  - A8 An unknown event type or malformed event JSON puts the message in the error state; it is not ignored (C6).
  - A9 Status messages (saving, saved, failed, incomplete) are exposed to a screen reader and reachable by keyboard.
  - A10 A `notice` event renders visibly above the reply (C4).
  - A11 A stream that ends without a terminal event shows "connection lost", keeps the text as incomplete and offers retry (C5, C6).
  - A12 A 401 mid-session prompts sign-in again and keeps the user's unsent draft (C1, C6).
- **Verification:** local browser tests with a scripted backend; screenshots from the current build. **Execution scope:** local. **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G03 from docs/plans/support-assistant.md. Read docs/architecture/support-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G05 — Persistent sessions and spend stops

- **Phase and estimate:** 1; hands-on 2–4, review 1–2, total 3–6; owner Dev A.
- **Outcome:** conversations survive restart; one active run per user, a daily allowance and call cap refuse before any model call. Proves C8, C9; implements D8, D9.
- **Scope:** `DatabaseSessionService` on the ADK schema, owner-filtered session routes, `max_llm_calls`, allowance counters with provisional values from O3 (the owner replaces them), message size cap. Excludes shared limiter (trigger: more than one instance).
- **Resources created:** none. **Prerequisites:** G01, G02. **Primary skill:** `adk-memory-architecture`; **supporting:** `adk-operational-guardrails` (not installed). **Security rules:** SB09, SB19.
- **Acceptance:**
  - A1 After a real restart a user sees their own earlier completed turns and no one else's; an incomplete turn is not shown as complete; ADK's tables are untouched by application migrations (C9).
  - A2 A looping scripted model stops at `max_llm_calls` with a `limit_reached` event (C8, SB19).
  - A3 A second concurrent run by the same user (second tab) is refused with 409 and a clear message; the slot frees after success, error and disconnect (C8, SB19).
  - A4 After the daily allowance, a run is refused before any model call, with the reset time (C8).
  - A5 An oversize message returns 413 before any model call (SB09).
  - A6 An exhausted connection pool gives a bounded wait then a generic 503, not a hang (C8).
- **Verification:** local integration with a real restart. **Execution scope:** local. **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G05 from docs/plans/support-assistant.md. Read docs/architecture/support-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G06 — Local end-to-end journey

- **Phase and estimate:** 1; hands-on 1–2, review 1–2, total 2–4.
- **Outcome:** one browser journey against the real API with the model scripted: sign in with a fixture token, save a language, ask, watch a streamed reply, force a failure, retry, delete, ask again. Proves C1, C3, C5, C6, C7 together.
- **Primary skill:** `adk-agent-evaluation`; **companion:** `playwright-cli`. **Prerequisites:** G03, G04, G05. **Security rules:** SB15.
- **Acceptance:**
  - A1 The journey passes end to end (C1, C3, C5, C6, C7).
  - A2 Every earlier acceptance item of G01 to G05 still passes (pass_to_pass).
  - A3 `make check`, `make dev` and `make e2e` run from a fresh clone using the documented setup.
  - A4 Lockfiles are committed and one dependency audit is recorded with findings fixed or accepted (SB15).
- **Execution scope:** local. **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G06 from docs/plans/support-assistant.md. Read docs/architecture/support-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G07 — Pilot go-ahead review

- **Phase and estimate:** 1; hands-on 2–3, review 1–2, total 3–5. Audience assumed business (Q7); a technical version only if the host team must read the design.
- **Outcome:** a deck outline, narrative, expected questions and a one-page decision memo for the pilot go-ahead; every claim cites evidence in this plan. Decision date is W2. **Primary skill:** `adk-presenter` (not installed; the outline can be written by hand to the same rule until it is). **Depends on:** G06.
- **Acceptance:** A1 Every claim cites an acceptance result recorded here; unmeasured benefits are labelled hypotheses. A2 The memo states what is not yet proven: live model adherence (C4), Cloud Run streaming (C5 hosted), real IdP (C1) and backup erasure (C3).
- **Run this goal:** `/adk-engineer Carry out G07 from docs/plans/support-assistant.md. Read docs/architecture/support-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

## Phase 2: pilot on Cloud Run (written coarsely; phase 1 results will change it)

Phase 2 starts only after W2 and needs authorisation for cloud and paid model use. Each goal carries the same fields as phase 1 once it is promoted.

### G08 — Live model, pinned ID, adherence (4–7 h; `adk-model-and-output-contracts`, `adk-agent-evaluation`; W3)

Pick the model ID from the dated lifecycle table, pin it, set the model-project quota and the owner's spend cap, then measure how often replies follow each allowlisted language on a small labelled prompt set. Resources created: none beyond model calls.
- A1 An absent or revoked model credential produces a generic service error with request ID, not a hang or a provider message (C6).
- A2 Adherence per language is measured and recorded as M1 with baseline, sample and method; the pilot threshold is set by the product owner (C4).
- A3 Hitting the quota stops calls and the UI shows a retry-later error (C8).

### G09 — Staging and pilot on Cloud Run (5–9 h; `deploy-adk-on-google-cloud`; supporting `google/skills:cloud-run-basics`, `google/skills:gcloud`; W2)

Deploy one service (`max-instances` 1) with a service account, Secret Manager and a database connection; same-origin SPA and API. **Resources created:** the Cloud Run service and its container image repository. Idle cost per day is read from current pricing at goal time (not checked here); cleanup commands and the "absent" verification are recorded when the goal runs; ownership passes to the cost contract and the decommission item below. If a new Cloud SQL instance is needed (O2), add its row from the resource cost ledger first.
- A1 Readback of the deployed revision matches the release unit; rollback to the previous revision works.
- A2 A wrong database credential makes readiness fail and requests return a generic 503; the right one serves (C2).
- A3 A hosted stream delivers the first delta before the last (not buffered) and a stream cut by the request timeout shows as incomplete in the UI (C5).
- A4 Same-origin or an explicit allowlist, no schema or docs routes, `nosniff` and `frame-ancestors` headers (SB06, SB07).
- A5 A ZAP baseline scan against staging is recorded with findings fixed or accepted (SB21).

### G10 — Real OIDC provider and revocation (4–7 h; `adk-tool-auth-and-secrets`, `adk-frontend-integration`; W1)

- A1 Sign-in with the real provider yields the same principal shape as the fixture (SB02, C1).
- A2 A revoked token is refused on save and delete (SB20).
- A3 An ASVS 5.0 Level 1 review is recorded with gaps turned into goals (SB22).

### G11 — Observability and release gate (5–9 h; `adk-agent-observability`, `adk-release-engineering`)

- A1 Structured logs show denial and error lines with request ID and no content (SB14).
- A2 A stream-failure-rate SLI and token cost per run exist, each with a baseline from G08 and an alert owner.
- A3 A release manifest records image, prompt version, model ID, secret versions and eval-set hash; the deterministic evaluation gate fails by exit code in CI.

### G12 — Governance pack (3–6 h; `adk-governance-pack`)

Drafts the papers for the client's reviewers (jurisdiction screen, privacy impact input, processing records, system card), including the backup-erasure statement for C3 and conversation retention (O8). Sign-off is W4.
- A1 The skill's checker passes on the drafts; every statement cites a contract, decision or evidence ID or is flagged for counsel.

### G13 — Pilot results review and first bill (3–5 h; `adk-presenter`; W4)

- A1 First live bill is read against the cost contract and recorded; each figure cites an M or I record.

## Later

| Item | Trigger | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| Group-account preferences | A product decision after the pilot | None; individual only | `adk-memory-architecture` |
| Shared run limiter, more than one instance | A second instance or a scaling need | Overlap window at deploys, one-instance ceiling | `adk-operational-guardrails` |
| Production tier SB23 to SB25 | Production profile or external users | Pilot scope only | `adk-agent-security` |
| Cost review | First bill, then each volume step | Spend stops, not alerts, bound cost | `adk-presenter` |
| Decommission | Pilot ends or the application retires | Idle Cloud Run and storage cost until then | `deploy-adk-on-google-cloud` |
| Prompt and model migration | The pinned model's retirement date | Re-baseline needed | `adk-release-engineering` |

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| [Design](../architecture/support-assistant.md) | Contracts, decisions, grids, open decisions |
| This plan | Goals, estimates, limits, evidence per goal |

## Open decisions for further planning

The design's O1 to O8 hold these. Each has a default, so no local goal waits except where marked there. If you later pick Matt Pocock's skills (not installed here; nothing was invoked or published), the plan is portable input: `wayfinder` can take O1 to O8 as decision questions, `to-spec` can turn the design and plan into a spec, `to-tickets` can split phase 1, and `implement` can work the tickets, with this plan becoming a pointer once one of them owns the statuses.

## Resume here

- **Next goal:** G01, because it is ready and settles the riskiest unknowns (O6, Cloud Run streaming shape) before anything depends on them. Also request W1 and W3 today so they run in parallel.
- **Read first:** the design, this plan, any `AGENTS.md`.
- **Next action:** confirm the ADK pin (A8), then write the failing scripted-model streaming test (A2, A3) before the route.
- **Continuation prompt:**

```text
/adk-engineer Carry out G01 from docs/plans/support-assistant.md.
Read docs/architecture/support-assistant.md and preserve its accepted decisions.
Use adk-frontend-integration with adk-agent-evaluation.
Work locally only: no cloud, no deployment, no real model calls. Verify A1 to A12
and record actual evidence and remaining blockers in the plan.
```

After that goal: `/adk-engineer Continue the next ready goal in docs/plans/support-assistant.md.`
