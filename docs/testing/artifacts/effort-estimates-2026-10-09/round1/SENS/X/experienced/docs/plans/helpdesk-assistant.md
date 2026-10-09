# Implementation plan: IT helpdesk runbook and ticket assistant

Status: draft; ready goals identified (G01, G02)
Architecture: [docs/architecture/helpdesk-assistant.md](../architecture/helpdesk-assistant.md)
Continuation source of truth: this plan; tickets in
[docs/tickets/helpdesk-assistant/](../tickets/helpdesk-assistant/) copy phase 1 goals.

## Destination and constraints

Phase 1 ends with the 25 helpdesk engineers signing in through IAP, getting
cited runbook answers from the allowlisted Confluence spaces, and creating a
Jira issue from a draft they confirm with one click. Non-goals and assumed
answers are in the design (A1–A9). Authorization so far: design only; no code,
cloud, IAM or Atlassian changes have been made or approved.

Inspected: the repository holds only `.claude/skills/`; no application code,
manifest or pin. All modules below are **proposed**:

```text
helpdesk_assistant/
  agent.py            # LlmAgent factory, instruction loaded from prompts/
  prompts/runbook_assistant.md
  tools/confluence.py # search_runbooks, get_runbook (function tools)
  tools/proposals.py  # propose_ticket (stores draft, no Jira call)
  jira_client.py      # create + search-by-label, used only by /confirm
  store.py            # Firestore: proposals, operations, daily counters
  app.py              # FastAPI: IAP JWT middleware, /chat, /proposals/{id}/confirm, static page
  static/index.html
tests/                # fakes for Confluence, Jira, Firestore; scripted-model Runner tests
evals/regression.evalset.json
```

Inherited pins (provisional until G01): google-adk 2.8.0; model
`gemini-3.8-flash` on Vertex AI (fallback `gemini-3.5-flash`); prompt version =
hash of `prompts/runbook_assistant.md`. Changing any of these is a release.

## Delivery profile and capacity

Profile: internal tool (design, "Delivery constraints").

| Phase | Delivers | Goals | Estimate (focused h) | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship | Colleagues use it daily with their own identity on real runbooks; confirmed ticket creation | G01–G04 | 19–27 | 2 × 0.5 × 10 d × 6 h × 0.6 ≈ 36 h; 25% reserve ≈ 9 h → 27 h |
| 2, harden or graduate | Graduation conditions: measured quality gate, per-user Jira identity, screening, persistent sessions | G05–G09 | 22–34 | When the team has time |

The high end of phase 1 exactly meets capacity minus reserve. If time runs
out, the goals are ordered so each finished one is useful: G02 gives a local
search assistant, G03 puts it in colleagues' hands, G04 adds tickets. If G04
runs high, ship its fallback (a prefilled Jira create link the engineer
submits in Jira; no write credential) and move API creation to phase 2.
The two engineers can split: one takes G02 while the other does G01 and the
G03 scaffolding, then G04's offline Jira/ledger work in parallel with G03.

## Implementation map

| Decision | Component and integration point (proposed) | GCP responsibility | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |
| D1 one agent | `agent.py` factory; `Runner` built in `app.py` with `RunConfig(max_llm_calls=8)` | Vertex AI endpoint | `adk-workflow-design` | Confirm `RunConfig` field names on the chosen pin |
| D2 live search | `tools/confluence.py`; CQL with config-owned space filter; HTML→text and caps | Secret Manager for the read token | `adk-tool-interface-design` | O1, O2 |
| D3 draft, then code create | `tools/proposals.py` + `/proposals/{id}/confirm` route | Firestore | `safe-api-tool-calls` | Jira create semantics (O3) |
| D4 service account reporter | `jira_client.py`; reporter lookup by verified email | Secret Manager for the create token | `adk-tool-auth-and-secrets` | O3 |
| D5 model pin | `agent.py` constant + revision label | Vertex model availability in region | `adk-model-and-output-contracts` | O5 |
| D6 Cloud Run + IAP | `app.py` middleware verifying `x-goog-iap-jwt-assertion` | Cloud Run, IAP, service identity | `deploy-adk-on-google-cloud` | IAP audience value; authorised project |
| D7 spend stop | `RunConfig` + Firestore daily counter at `/chat` admission | Billing budget alert | `adk-operational-guardrails` | O6 values |

## Goals and dependencies

| ID and goal | Phase | Type | Estimate | Depends on | Primary skill | State |
| --- | --- | --- | --- | --- | --- | --- |
| G01 Confirm Atlassian, model and pin contracts | 1 | discovery | 2–3 h | — | `adk-tool-auth-and-secrets` | ready (needs Atlassian admin access) |
| G02 Engineer gets a cited runbook answer locally | 1 | implementation | 6–8 h | G01 for the live check only | `adk-tool-interface-design` | ready (offline with fakes) |
| G03 Helpdesk colleagues use it behind IAP | 1 | implementation | 5–7 h | G02; authorised GCP project | `deploy-adk-on-google-cloud` | blocked: G02, project authorisation |
| G04 Engineer creates a Jira issue from a confirmed draft | 1 | implementation | 6–9 h | G01 (O3), G02; G03 for hosted check | `safe-api-tool-calls` | blocked: G01, G02 |
| G05 Quality measured from real use | 2 | implementation | 5–8 h | G03 | `adk-agent-evaluation` | proposed |
| G06 Release gate and model migration calendar | 2 | implementation | 4–6 h | G05 | `adk-release-engineering` | proposed |
| G07 Tickets created under the engineer's own Jira identity | 2 | implementation | 6–9 h | G04 | `adk-tool-auth-and-secrets` | proposed |
| G08 Secrets in runbooks screened before the model | 2 | implementation | 4–6 h | G02 | `protect-adk-sensitive-data` | proposed |
| G09 Conversations survive restarts and scale-out | 2 | implementation | 3–5 h | G03 | `adk-memory-architecture` | proposed |

### G01 — Confirm Atlassian, model and pin contracts

- **Phase and estimate:** 1; 2–3 h.
- **Outcome and linked decisions:** settles O1, O2, O3, O5 and the ADK pin so G02–G04 build against facts (A5–A7, D2, D4, D5).
- **Scope:** read-only inspection and one record `docs/architecture/helpdesk-assistant-contracts.md`. Out: creating service accounts or tokens unless the Atlassian admin does it separately.
- **Depth:** discovery only; no secrets written into the record.
- **Implementation route:** Confluence/Jira admin pages and REST docs; Vertex model-versions page for the region; the specialists' `compatibility.md` for the ADK pin.
- **Prerequisites:** someone with Atlassian admin rights; network access (not available in the design session).
- **Primary skill:** `adk-tool-auth-and-secrets` (token type, scope, storage).
- **Supporting skills:** `safe-api-tool-calls` (Jira create replay/idempotency contract); `adk-model-and-output-contracts` (model availability and lifecycle).
- **Acceptance:** record answers: Cloud or Data Center; runbook space keys and whether any page restriction is narrower than the helpdesk group; Jira project key, issue type, required fields, component and priority values; whether the create token can set reporter; whether create supports any idempotency key and whether label search is immediately consistent; model ID confirmed on Vertex in region or fallback chosen; ADK pin chosen.
- **Verification:** reviewed record; stop when every item has an answer or a named owner.
- **Execution scope:** read-only; any live API call uses a read-only or sandbox target.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G01 from docs/plans/helpdesk-assistant.md. Read docs/architecture/helpdesk-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G02 — Engineer gets a cited runbook answer locally

- **Phase and estimate:** 1; 6–8 h.
- **Outcome and linked decisions:** "VPN error 809" returns the right steps with page links, or says no runbook was found (I2, I3, D1, D2, D5, D7).
- **Scope:** `agent.py`, `prompts/`, `tools/confluence.py`, fakes, Runner tests, a ~15-case regression set from real helpdesk questions (helpdesk lead supplies them). Out: hosting, tickets.
- **Depth:** internal tool; floor: pinned model, `max_llm_calls`, token from env/Secret Manager, no content in logs, credential-pattern masking on page text.
- **Implementation route:** `LlmAgent` with `search_runbooks` and `get_runbook`; space filter and caps in code; `get_runbook` refuses page IDs not returned by a search in the session.
- **Prerequisites:** none for offline work; G01 for the live Confluence check.
- **Primary skill:** `adk-tool-interface-design`.
- **Supporting skills:** `adk-agent-instructions` (instruction and citation rule); `adk-agent-evaluation` (regression set); `adk-model-and-output-contracts` (model pin).
- **Acceptance:** offline: scripted model calls search then get, answer carries a URL from the hits; empty search → "no runbook found", no invented steps; model-supplied CQL operators escaped and the space filter always present; page over 8k chars truncated with `truncated: true`; looping script stops at 8 calls. Live (after G01): ≥12 of 15 regression cases cite a correct page (provisional threshold).
- **Verification:** `pytest tests/` offline; `adk eval` on the regression set against the live model (bounded, ~15 cases × 1 run).
- **Execution scope:** local; live model and Confluence calls need G01 credentials.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G02 from docs/plans/helpdesk-assistant.md. Read docs/architecture/helpdesk-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G03 — Helpdesk colleagues use it behind IAP

- **Phase and estimate:** 1; 5–7 h.
- **Outcome and linked decisions:** a group member opens the page and gets G02's answers; anyone else is refused (I1, I6, D6, D7).
- **Scope:** `app.py` (JWT middleware, `/chat`, daily counter, session ownership), `static/index.html`, Dockerfile, Cloud Run service, IAP, Secret Manager, budget alert, structured logs, revision labels. Out: tickets (G04), persistent sessions (G09).
- **Depth:** internal tool; floor: least-privilege service identity, secrets from Secret Manager, no content in logs, pinned versions in revision labels.
- **Implementation route:** FastAPI wrapping the ADK `Runner` with `InMemorySessionService`; Cloud Run max instances 1; IAP restricted to the Workspace group.
- **Prerequisites:** G02; an authorised GCP project, region and the group address.
- **Primary skill:** `deploy-adk-on-google-cloud`.
- **Supporting skills:** `adk-tool-auth-and-secrets` (IAP JWT verification, Secret Manager); `adk-frontend-integration` (completed-JSON page contract, session ownership); `adk-agent-observability` (structured logs without content); `adk-release-engineering` (pinned release labels, rollback to previous revision).
- **Acceptance:** offline: missing/forged JWT → 401; user B gets 403 on user A's session; 41st turn of the day → limit message. Hosted: member completes the VPN journey; non-member blocked by IAP; logs show IDs and token counts and no runbook text; previous revision retained.
- **Verification:** `pytest`; hosted checks listed above, run once in the authorised project.
- **Execution scope:** deployment, IAM and IAP changes need explicit approval for the named project.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G03 from docs/plans/helpdesk-assistant.md. Read docs/architecture/helpdesk-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G04 — Engineer creates a Jira issue from a confirmed draft

- **Phase and estimate:** 1; 6–9 h.
- **Outcome and linked decisions:** "open a ticket for networking" shows a draft card; Create returns one Jira key (I4, I5, D3, D4).
- **Scope:** `tools/proposals.py`, `store.py` (proposals, operations), `jira_client.py`, `/proposals/{id}/confirm`, draft card in the page, injection cases. Out: per-user OAuth (G07), comments or transitions.
- **Depth:** internal tool: confirmation in code, durable operation record, reconcile-not-retry. Fallback if over estimate: prefilled Jira create link, no create token.
- **Implementation route:** model calls `propose_ticket` (enum-validated, stored with payload hash, owner = verified email); `/confirm` checks owner, claims the operation in a Firestore transaction, creates with label `hda-op-<id>`, records the key; on timeout searches by label.
- **Prerequisites:** G01 (O3 answers), G02; G03 for the hosted check.
- **Primary skill:** `safe-api-tool-calls`.
- **Supporting skills:** `adk-agent-security` (trifecta split, adversarial cases); `adk-tool-interface-design` (`propose_ticket` declaration); `adk-tool-auth-and-secrets` (create token, reporter from verified identity).
- **Acceptance:** double confirm → one fake-Jira create, same key; timeout after fake commit → label search finds it, no second create; not found → `uncertain`, no retry; user B confirming A's proposal → 403, no call; edited payload with old ID → 409; three injected-page cases ("create a P1 ticket", "email this to…", "ignore previous instructions") → zero Jira calls; Jira 400 → `failed`, draft kept.
- **Verification:** `pytest` offline with fakes; one live create in a sandbox project or with a test label, then deleted by the Jira admin.
- **Execution scope:** live Jira write needs the admin's approval and target from G01.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G04 from docs/plans/helpdesk-assistant.md. Read docs/architecture/helpdesk-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### Phase 2 goals (coarser; phase 1 results may change them)

- **G05 Quality measured from real use** — 5–8 h, `adk-agent-evaluation` (+ `adk-agent-observability` for thumbs feedback and trace-to-case). Acceptance: 40-case set built partly from redacted thumbs-down sessions; citation-correct rate reported per release.
- **G06 Release gate and model migration** — 4–6 h, `adk-release-engineering`. Acceptance: CI fails by exit code when the regression rate drops below the agreed threshold; manifest records image, ADK, model, prompt hash; the model's retirement date is in the team calendar.
- **G07 Per-user Jira identity** — 6–9 h, `adk-tool-auth-and-secrets` (+ `safe-api-tool-calls`). Acceptance: issue creator is the engineer; disconnect stops new creates; refresh failure does not fall back to the service account.
- **G08 Runbook secret screening** — 4–6 h, `protect-adk-sensitive-data`. Acceptance: a seeded credential in a fake page never reaches the captured model request; screening outage → answer refused, not unscreened.
- **G09 Persistent sessions** — 3–5 h, `adk-memory-architecture` (+ `deploy-adk-on-google-cloud`). Acceptance: conversation survives a revision restart; another user cannot load it.

## Later

| Item | Trigger | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| Semantic index (Vertex AI Search) over runbooks | Retrieval hit rate below ~70% on the set | Weaker keyword recall | `adk-memory-architecture` |
| Per-user Confluence permissions | Restricted pages appear, or other teams join | Only safe while A6 holds | `adk-tool-auth-and-secrets` |
| Google Chat / Slack front end | Users ask for it | Context switch to a browser tab | `adk-frontend-integration` |
| Streaming answers | Median complete answer > ~10 s | Waiting on a spinner | `adk-frontend-integration` |
| SLOs and alerts | First incident logs could not explain, or wider rollout | Problems found by users | `adk-agent-observability` |
| Adversarial suite beyond 3 cases | Any new write or egress tool | Draft-level injection influence | `adk-agent-security` |
| Latency/cost tuning | Measured complaint or spend alert | Unmeasured cost per turn | `optimise-adk-on-google-cloud` |

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| [Design](../architecture/helpdesk-assistant.md) | Assumed answers, decisions, invariants |
| `evals/` results summary (created by G02) | Latest regression result per case |
| This plan | Phase status, remaining limits and deferred controls |

## Open decisions for further planning

See design "Open decisions" O1–O6. O1–O3 and O5 are G01's job; O4 and O6
need the user.

## Resume here

- **Next goal:** G01 (needs Atlassian admin access), or G02 offline in parallel; both ready.
- **Read first:** the design, then this plan.
- **Next action:** G01: list runbook space keys and check page restrictions.
- **Continuation prompt:**

```text
/adk-engineer Carry out G01 Confirm Atlassian, model and pin contracts from docs/plans/helpdesk-assistant.md.
Read docs/architecture/helpdesk-assistant.md and preserve its accepted decisions.
Use adk-tool-auth-and-secrets with safe-api-tool-calls and adk-model-and-output-contracts.
Work within read-only inspection, verify its acceptance items, and update
the plan with actual evidence and remaining blockers.
```

After that goal: `/adk-engineer Continue the next ready goal in docs/plans/helpdesk-assistant.md.`
