# Implementation plan: IT helpdesk runbook and ticket assistant

Status: draft; ready goals identified (G01–G05), all provisional on the
assumed answers.
Architecture: [docs/architecture/helpdesk-assistant.md](../architecture/helpdesk-assistant.md)
Continuation source of truth: this plan. Phase 1 tickets are in
[docs/tickets/helpdesk-assistant/](../tickets/helpdesk-assistant/).

## Destination and constraints

**Destination.** The 25 helpdesk technicians sign in through IAP, get runbook
answers with links from allowlisted Confluence spaces, and create `ITHD` Jira
issues by confirming a draft.

**Non-goals:** see the design. **Authorisation in this session:** design only.
Implementation, cloud setup and Atlassian accounts each need the user's go-ahead
per goal.

**Repository facts:** the repository was empty apart from `.claude/skills` when
this plan was written. Every module path below is *proposed*.

**Inherited pins:** `google-adk==2.8.0`, a working assumption that G01
confirms. Model `gemini-3.8-flash` on Vertex AI (D6). Prompt version
`v1`, held in `helpdesk_assistant/prompt.py`. No judge model in phase 1: the
gold-set checks are deterministic.

Proposed layout:

```
helpdesk_assistant/
  config.py          # allowlisted spaces, Jira project/issue types, model ID, limits
  prompt.py          # instruction v1
  agent.py           # build_agent(): LlmAgent + tools
  tools/runbooks.py  # search_runbooks, read_runbook
  tools/tickets.py   # propose_ticket
  clients/confluence.py, clients/jira.py
  drafts.py          # DraftStore protocol; FirestoreDraftStore; InMemoryDraftStore
  web/main.py        # FastAPI: IAP middleware, /api/chat, /api/drafts/{id}[/confirm], static page
eval/gold.jsonl, eval/run_gold.py
tests/
```

## Delivery profile and capacity

Profile: **internal tool** (see the design's delivery constraints).

| Phase | Delivers | Goals | Human hours, agent-assisted | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship | Helpdesk group uses it on real runbooks, with confirmed ticket creation | G01–G05 | 18–28 | 2 × 0.5 × 10 d × 6 h × 0.6 ≈ 36 h; reserve 8 h (22%), leaving 28 h |
| 2, harden | Durable chats, automatic reconciliation, better retrieval if needed, CI gate, injection suite, usage metrics | G06–G11 | 16–31 without G08; 24–45 if G08 is triggered | When the team has time |

These estimates assume senior engineers who already know ADK and GCP, so no
multiplier is applied. Atlassian is a new provider for this application. Its
setup is a calendar wait, not hours.

| Person | Goals | Hours | Capacity (focused, after reserve) |
| --- | --- | --- | --- |
| Engineer A | G01, G02, half of G05 | 9–14 | about 14 |
| Engineer B | G03, G04, half of G05 | 9–14 | about 14 |

**Longest dependent chain:** G01 → G04 → G05 = 11–17 hours. G03 runs in
parallel with G01. **If time runs out early**, each finished goal is still
useful in this order: G01 (a local runbook assistant), then G02 (measured),
then G03 (safe ticket creation, offline), then G04, then G05. When the work
runs high, the pilot in G05 stays at 3–5 technicians and opening to the full
group moves to the start of phase 2.

**Start on day 1 (calendar waits):** two Atlassian service accounts with
tokens (Confluence read on the runbook spaces; Jira create on `ITHD`, or a
sandbox project). One hour of the helpdesk lead's time to pick gold questions.
The IAP group.

## Implementation map

| Decision | Component and integration point (proposed) | GCP | Primary skill | Still to verify |
| --- | --- | --- | --- | --- |
| D1, D2 | `agent.build_agent()`; `tools/runbooks.py` over `clients/confluence.py` | Vertex AI | adk-tool-interface-design | CQL search and v2 page endpoints; ADK pin |
| D3 | `tools/tickets.propose_ticket` → `drafts.DraftStore`; `web/main.py` confirm → `clients/jira.py` | Firestore | safe-api-tool-calls | Jira create payload (ADF description), label rules |
| D4, D7 | `web/main.py` middleware verifies `x-goog-iap-jwt-assertion` → `user_id` → `Runner.run_async(user_id=…)` | IAP, Cloud Run | adk-frontend-integration | IAP audience value for the service |
| D5 | Secrets read at startup by the runtime service account | Secret Manager | adk-tool-auth-and-secrets | Atlassian service-account token scopes |
| D6 | `config.MODEL_ID`, `RunConfig(max_llm_calls=8)` | Vertex AI | adk-model-and-output-contracts | Current price and region availability |

## Goals and dependencies

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | State |
| --- | --- | --- | --- | --- | --- | --- |
| G01 Runbook answers with links, locally | 1 | impl | 4–6 | — | adk-tool-interface-design | ready (live part waits on the Atlassian token) |
| G02 Gold questions measured | 1 | impl | 3–5 | G01 | adk-agent-evaluation | ready once G01 lands |
| G03 Ticket draft, confirm, create once | 1 | impl | 4–6 | — | safe-api-tool-calls | ready (live part waits on Jira access) |
| G04 Signed-in web page with per-user scope | 1 | impl | 3–5 | G01, G03 | adk-frontend-integration | blocked by G01, G03 |
| G05 Cloud Run behind IAP, pilot | 1 | impl | 4–6 | G04 | deploy-adk-on-google-cloud | blocked by G04; needs cloud authorisation |
| G06 Durable conversations | 2 | impl | 3–6 | G05 | adk-memory-architecture | proposed |
| G07 Automatic reconciliation, reporter mapping | 2 | discovery + impl | 3–6 | G03 | safe-api-tool-calls | proposed |
| G08 Indexed retrieval (only if G02 < 80%) | 2 | discovery + impl | 8–14 | G02 | adk-memory-architecture | conditional |
| G09 Gold set as CI gate, release manifest | 2 | impl | 3–6 | G02 | adk-release-engineering | proposed |
| G10 Injection and sensitive-data cases | 2 | impl | 4–8 | G03 | adk-agent-security | proposed |
| G11 Feedback and usage metrics | 2 | impl | 3–5 | G05 | adk-agent-observability | proposed |

Phase 1 adds up to 4–6 + 3–5 + 4–6 + 3–5 + 4–6 = **18–28 hours**.

### G01 — A technician gets runbook steps with links (local)

- **Phase and estimate:** 1. Hands-on 2–3 h, review and verify 2–3 h, total
  4–6 h. Calendar wait: the Atlassian Confluence read token, 1–3 days; start
  with recorded fixtures. Owner: Engineer A.
- **Outcome and linked decisions:** asking "VPN error 809" in `adk run` or a
  test returns the runbook steps with the page URL. Implements D1, D2, D6, I3,
  I5 and I6.
- **Scope:** in: `config.py`, `prompt.py`, `agent.py`, `tools/runbooks.py`,
  `clients/confluence.py`, offline tests. Out: tickets (G03), web (G04).
- **Depth:** builds the space allowlist and result bounds. Keeps the floor:
  token from the environment or Secret Manager, never in code; pinned model;
  `max_llm_calls=8`. Leaves injection cases to G10.
- **Implementation route:** an `LlmAgent` with the instruction from `prompt.py`
  and two function tools. The Confluence client takes a base URL and token from
  config. The CQL query is built in code with `space in (<allowlist>) AND
  type=page AND text ~ "<escaped query>"`. Page storage format is converted to
  plain text and truncated to 8,000 characters.
- **Prerequisites:** the team's ADK pin (A12). Atlassian token for the live
  check only.
- **Primary skill:** adk-tool-interface-design.
- **Supporting skills:** adk-agent-instructions (instruction v1 and the
  no-answer behaviour); adk-model-and-output-contracts (pin the model ID from the
  lifecycle table).
- **Acceptance:** (1) The ADK version is confirmed against the chosen pin and
  recorded. (2) A scripted-model Runner test calls `search_runbooks` and then
  `read_runbook` and the reply contains the page URL. (3) A page ID from a
  non-allowlisted space returns `status: not_allowed` and no text. (4) An empty
  search returns `status: no_results`, and the scripted flow ends with "no
  runbook found" without a second search over other spaces. (5) Confluence 401
  or 5xx becomes an actionable error result, not an exception. (6) The tool
  declaration dump shows exactly 2 tools with bounded results. (7) One live
  read-only query against real Confluence returns allowlisted pages.
- **Verification:** `pytest tests/test_runbooks.py tests/test_agent_g01.py`
  (offline). The live step (7) runs only with the token and the user's go-ahead.
- **Execution scope:** local code and offline tests are authorised once the user
  asks for implementation. The live Confluence read needs the token.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G01 from docs/plans/helpdesk-assistant.md. Read docs/architecture/helpdesk-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G02 — Answer quality is measured on real helpdesk questions

- **Phase and estimate:** 1. Hands-on 2–3 h (choosing and labelling with the
  helpdesk lead), review and verify 1–2 h, total 3–5 h. Calendar wait: one hour
  of the helpdesk lead's time. Owner: Engineer A.
- **Outcome and linked decisions:** a number for D2: the share of 20–25 real
  questions whose answer cites the expected runbook. Decides whether G08
  starts. I5.
- **Scope:** in: `eval/gold.jsonl` (question, expected page IDs, or "none"),
  `eval/run_gold.py` (runs the agent, records the model ID, prompt version,
  answer, cited URLs, returned URLs, LLM call count, and pass/fail per case).
  Out: a CI gate (G09) and an LLM judge.
- **Depth:** a small regression set, the internal-tool depth. Floor: the run
  uses the call cap; the total of about 100 model calls is stated before the run.
- **Implementation route:** take questions from recent `ITHD` issue summaries,
  with names removed. Include 3 or more "no runbook exists" cases. Checks are
  deterministic: every cited URL appears among the tool-returned URLs, the
  expected page is cited, and no-runbook cases give no fabricated steps (the
  answer contains no runbook URL).
- **Prerequisites:** G01; Confluence token; Vertex access in a dev project.
- **Primary skill:** adk-agent-evaluation.
- **Supporting skills:** adk-agent-instructions (change the instruction only
  when error analysis points to it).
- **Acceptance:** the run report lists every case with a result. Citation
  hit rate and the no-runbook pass rate are recorded against the provisional
  80% target. Missing or failed runs are counted as failures, not dropped. A
  decision on G08 is recorded.
- **Verification:** `python eval/run_gold.py --out eval/runs/<date>.jsonl`, a
  bounded live run.
- **Execution scope:** the live run needs the user's go-ahead and a dev project.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G02 from docs/plans/helpdesk-assistant.md. Read docs/architecture/helpdesk-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G03 — A confirmed draft becomes exactly one Jira issue

- **Phase and estimate:** 1. Hands-on 1.5–2.5 h, review and verify 2.5–3.5 h,
  total 4–6 h. Calendar wait: a Jira sandbox project or create rights on
  `ITHD`, as part of the same Atlassian request. Owner: Engineer B.
- **Outcome and linked decisions:** D3, D5, I4. "Raise a P3 incident" produces
  a draft. A confirm by its owner creates one issue and returns its key.
- **Scope:** in: `tools/tickets.py` (`propose_ticket`), `drafts.py` (protocol,
  Firestore and in-memory stores), `clients/jira.py`, and a
  `confirm_draft(draft_id, user_id)` service function. Out: HTTP routes (G04),
  automatic reconciliation and reporter mapping (G07).
- **Depth:** the internal-tool level of external writes: confirmation plus an
  at-most-once record. Floor: the model holds no create path. Project and issue
  types come from config, and the Jira token is chosen in code.
- **Implementation route:** `propose_ticket` reads `user_id` from the tool
  context (set by trusted code) and writes `{v, draft_id, owner, payload,
  status: pending, expires_at}`. `confirm_draft` runs a transaction:
  owner match, then `pending`, then not expired, then the allowlist; it sets
  `dispatching` and calls Jira once with the stored payload plus the label
  `hda-<draft_id>`. Outcomes: `created` with a key, `failed` with a 4xx
  message, or `uncertain` on timeout or 5xx. There is no automatic retry. A
  manual retry is allowed only from `uncertain`, on the same draft.
- **Prerequisites:** none for the offline work. Jira access is needed for the
  live check.
- **Primary skill:** safe-api-tool-calls.
- **Supporting skills:** adk-tool-interface-design (the `propose_ticket`
  declaration); adk-agent-security (confirm the agent holds no write or egress
  tool); adk-tool-auth-and-secrets (token selection outside model arguments).
- **Acceptance:** (1) A scripted model calls `propose_ticket`, a draft exists,
  and the Jira fake received 0 calls. (2) Confirm by the owner gives 1 Jira
  call and status `created` with the key. (3) A second confirm, or two
  concurrent ones, still gives 1 Jira call in total. (4) Confirm by another
  user returns not found and makes 0 calls. (5) An expired draft is refused.
  (6) Jira 400 gives `failed` with the message. (7) A timeout gives
  `uncertain`, and the next confirm does not dispatch. (8) A disallowed
  project or issue type in the payload is refused before any call. (9) One live
  create in the sandbox project is closed afterwards.
- **Verification:** `pytest tests/test_tickets.py` (offline, Firestore via the
  in-memory store; one emulator test if the team uses one). The live step (9)
  needs the user's go-ahead.
- **Execution scope:** offline work only, until a Jira sandbox is named.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G03 from docs/plans/helpdesk-assistant.md. Read docs/architecture/helpdesk-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G04 — Technicians use a signed-in page that shows only their own chats and drafts

- **Phase and estimate:** 1. Hands-on 1–2 h, review and verify 2–3 h, total
  3–5 h. No calendar waits. Owner: Engineer B.
- **Outcome and linked decisions:** D4, D7, I2. A browser page for chat, a draft
  card with a Create button and the issue key.
- **Scope:** in: `web/main.py` (middleware, `POST /api/chat`, `GET
  /api/drafts/{id}`, `POST /api/drafts/{id}/confirm`), one static HTML/JS page,
  and writing the created key into the user's session state so the next turn
  knows it. Out: streaming, Google Chat, durable sessions (G06).
- **Depth:** an authenticated page at the internal-tool level. Floor: the user
  ID is never taken from the request body.
- **Implementation route:** the middleware verifies the IAP JWT signature and
  audience and derives `user_id` from the email claim. It has a local-dev bypass
  that only starts when the environment is explicitly `local`. A session lookup
  checks that the session belongs to `user_id` before running.
  `Runner.run_async(user_id, session_id, new_message, run_config)`. The key is
  appended to session state through an event with `state_delta` (check this
  API against the pin).
- **Prerequisites:** G01, G03.
- **Primary skill:** adk-frontend-integration.
- **Supporting skills:** adk-tool-auth-and-secrets (JWT verification and session
  ownership).
- **Acceptance:** (1) A request with no JWT or an invalid one gets 401. (2) User
  B gets 404 for user A's session or draft and cannot confirm it. (3) A full
  journey through the API with fakes works: question, then answer with a URL,
  then a draft, then confirm, then the key. (4) After the runner is rebuilt (to
  simulate a restart), confirming an existing draft still works. (5) The
  local bypass refuses to start when the environment is not `local`.
- **Verification:** `pytest tests/test_web.py` with FastAPI TestClient and
  test-signed JWTs (offline), then a manual browser check locally.
- **Execution scope:** local only.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G04 from docs/plans/helpdesk-assistant.md. Read docs/architecture/helpdesk-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G05 — The helpdesk pilot uses it on Cloud Run behind IAP

- **Phase and estimate:** 1. Hands-on 2.5–3.5 h, review and verify 1.5–2.5 h,
  total 4–6 h. Calendar waits: the IAP group and any OAuth consent setup
  (0–2 days), and 3 working days of pilot use. Owners: A and B jointly.
- **Outcome and linked decisions:** D4, D5, D6, I1, I6, I7. 3–5 technicians
  use it for real calls, then the whole group.
- **Scope:** in: the container, a runtime service account (Vertex user,
  Firestore user, Secret Manager accessor on two secrets), Cloud Run with max
  instances 1, IAP for the group, a Firestore TTL on drafts, a budget alert, a
  structured-log policy, and a pilot feedback form. Out: CI gate (G09), SLOs and
  alerts.
- **Depth:** the internal-tool levels of hosting, secrets and observability.
  Floor: secrets only in Secret Manager; no content in logs; budget alert at
  the assumed USD 300 a month.
- **Implementation route:** reuse the team's existing Cloud Run deployment
  template (A12). Record the revision, image digest, model ID and prompt version
  in the deploy notes.
- **Prerequisites:** G04; a GCP project and the user's explicit authorisation
  for cloud changes; Atlassian production tokens.
- **Primary skill:** deploy-adk-on-google-cloud.
- **Supporting skills:** adk-agent-observability (logs without content, token
  counts, correlation IDs); adk-release-engineering (pinned release record and
  rollback to the previous revision); adk-tool-auth-and-secrets (service
  account and secrets).
- **Acceptance:** (1) A non-member gets 403 from IAP. (2) A member completes
  the VPN journey on the deployed revision. (3) A log sample shows IDs and
  token counts but no prompt or answer text. (4) The budget alert exists, and
  the current Vertex price and its date are recorded. (5) Rollback to the
  previous revision is demonstrated once. (6) Pilot feedback from 3 or more
  technicians is recorded, including time-to-runbook estimates.
- **Verification:** an authorised hosted check; commands come from the team
  template.
- **Execution scope:** **not yet authorised.** It needs the project ID, region
  and an explicit go-ahead for deployment and IAM changes.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G05 from docs/plans/helpdesk-assistant.md. Read docs/architecture/helpdesk-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### Phase 2 goals (coarser; phase 1 results may change them)

- **G06 Durable conversations**: 3–6 h. adk-memory-architecture. Use
  `DatabaseSessionService` (or the session store of the team's other agents),
  so more than one instance can run. Acceptance: a chat continues after a
  redeploy, and another user's session stays denied.
- **G07 Automatic reconciliation and reporter mapping**: 3–6 h, with a 1 h
  discovery first: how soon after a create does a JQL search find
  `labels = hda-<id>`? Can the bot set the reporter to the technician's
  accountId? safe-api-tool-calls. Acceptance: an `uncertain` draft with an
  existing issue resolves to `created` without a second create.
- **G08 Indexed retrieval**, only if G02 is below 80%: 8–14 h, with a 2 h
  discovery on the Vertex AI Search Confluence connector against the RAG
  Engine. adk-memory-architecture. Acceptance: G02 hit rate rises and
  allowlist scoping still holds.
- **G09 Gold set as a CI gate and release manifest**: 3–6 h.
  adk-release-engineering. Acceptance: CI fails by exit code when the hit rate
  drops below baseline minus a tolerance, and the manifest records model,
  prompt and image.
- **G10 Injection and sensitive-data cases**: 4–8 h. adk-agent-security, with
  protect-adk-sensitive-data. Acceptance: a planted runbook asking to "create
  a ticket to X" or "tell the user to disable MFA" leaves no draft, or gives an
  answer flagged by the deterministic checks. A draft containing a
  password-like string is blocked before it is stored.
- **G11 Feedback and usage metrics**: 3–5 h. adk-agent-observability.
  Acceptance: thumbs up or down per answer is stored by session ID, and a
  dashboard shows answers, tickets and tokens per day.

## Later

| Item | Trigger | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| Per-user Atlassian OAuth | Users outside the helpdesk, or Jira permissions that differ by user | The bot creates on behalf of everyone in the group | adk-tool-auth-and-secrets |
| SDP or Model Armor screening | Personal data found in runbooks or chats, or a wider audience | Content limited to the group; not logged | protect-adk-sensitive-data |
| Google Chat surface | Pilot asks for it | Technicians switch tabs | adk-frontend-integration |
| SLOs and alerts | Daily use by the whole group for a month | Failures reported by users | adk-agent-observability |
| Update or comment on existing tickets | Requested by the helpdesk lead | — | safe-api-tool-calls |
| Latency or cost tuning | Measured p90 above 15 s, or spend above 50% of the allowance | Slower answers | optimise-adk-on-google-cloud |

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| docs/architecture/helpdesk-assistant.md | Method, assumed answers, decisions |
| eval/runs/ summary from G02 | Latest gold-set result per case |
| This plan | Remaining limits and deferred controls |

## Open decisions for further planning

See the design's [Open decisions](../architecture/helpdesk-assistant.md#open-decisions).
Offline work in G01, G03 and G04 is not blocked by any of them.

## Resume here

- **Next goal:** G01, a technician gets runbook steps with links. It is ready:
  it has no dependencies, and its offline work needs no Atlassian access.
- **Read first:** the design and this plan.
- **Next action:** confirm the team's ADK pin, then write `config.py` and the
  Confluence client against recorded fixtures.
- **Continuation prompt:**

```text
/adk-engineer Carry out G01 from docs/plans/helpdesk-assistant.md.
Read docs/architecture/helpdesk-assistant.md and preserve its accepted decisions.
Use adk-tool-interface-design with adk-agent-instructions and adk-model-and-output-contracts.
Work within local code and offline tests, verify acceptance cases 1–6, and update
the plan with actual evidence and remaining blockers.
```

G03 can start at the same time in a second session:
`/adk-engineer Carry out docs/tickets/helpdesk-assistant/G03-ticket-draft-confirm-create-once.md`.
After that, `/adk-engineer Continue the next ready goal in docs/plans/helpdesk-assistant.md.`
