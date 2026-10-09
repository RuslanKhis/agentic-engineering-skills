# Implementation plan: IT helpdesk runbook and ticket assistant

Status: draft. The goals are ready in design, but the cut line (O1) and the
assumed answers A1–A14 are not yet confirmed by the user.
Architecture: [docs/architecture/helpdesk-assistant.md](../architecture/helpdesk-assistant.md)
Continuation source of truth: this plan. Phase 1 tickets are in
[docs/tickets/helpdesk-assistant/](../tickets/helpdesk-assistant/).

## Destination and constraints

**End result:** 25 helpdesk analysts ask runbook questions and get cited answers
from Confluence. On request, they create an `ITHD` Jira ticket after confirming
its exact contents. **Non-goals:** Confluence edits, Jira updates or
transitions, and use by end users.

**Accepted stack (proposed):**

- Python 3.11 and `google-adk==2.8.0`.
- One `LlmAgent` on Vertex AI using `gemini-3.8-flash` (from the lifecycle
  table checked_on 2026-10-08).
- Function tools over the Confluence and Jira Cloud REST APIs.
- Secret Manager for the Atlassian tokens.
- Phase 2: Cloud Run behind IAP.

**Authorization:** design only. No code, cloud resources or Atlassian accounts
exist yet. Each goal states its own external prerequisites.

**Inspected:** an empty repository. Every module below is proposed:

```
helpdesk_assistant/__init__.py, agent.py (root_agent), config.py, prompt.md,
confluence.py, jira.py, tools.py
tests/fakes.py, test_runbook_tools.py, test_ticket_flow.py, test_runner_limits.py
eval/gold_questions.yaml, eval/run_gold.py, eval/results/
pyproject.toml (pins), .env.example (no values)
```

The pinned model, ADK version and `prompt.md` are inherited by every goal.
Changing any of them is a release (re-run G03), not a side effect.

## Delivery profile and capacity

Profile: **internal tool**, delivered in phases. Phase 1 is a local pilot;
phase 2 graduates it to all 25 staff. See the
[design's delivery constraints](../architecture/helpdesk-assistant.md#delivery-constraints-depth-and-deferred-controls).

| Phase | Delivers | Goals | Human hours, agent-assisted | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship | Working assistant on real runbooks and Jira, run locally by the engineers and demoed to the lead, with a measured gold-question score | G01–G04 | 15–26 | 2 × 0.5 × 10 d × 6 h × 0.6 = 36 h; 25% reserve (9 h) → 27 h available |
| 2, graduate | Verified identity, hosted behind IAP for 25 staff, CI, adversarial cases, attribution, outcome measured | G05–G11 | 23–42 | Next available block (about 3 weeks at the same rate) |

The estimates are assumptions for this team: base hours from the delivery
profile table × 1.5 for a team new to ADK, plus GCP first-project setup on G01.
Calendar waits are listed on their goals and are not counted as hours.

| Person | Goals | Hours | Capacity after reserve |
| --- | --- | --- | --- |
| Engineer A | G02, G03 | 7–12 | 13.5 |
| Engineer B | G01, G04 | 8–14 | 13.5 (high end 0.5 h over) |

If G01 runs high, Engineer A writes G04's offline tests after G02.

**Longest dependent chain:** G01 → G04, 8–14 h, plus the Atlassian and GCP
admin waits. Start both waits on day 1.

**If time runs out**, stop after G02 → G03: a measured runbook assistant
without ticket creation is still useful, and G04 moves to phase 2.

**Cut line (to confirm, O1):** phase 1 is G01–G04, 15–26 h of the 27 available.
Phase 2 is G05–G11.

## Implementation map

| Decision | Component and integration point (proposed) | GCP responsibility | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |
| D1, D4 | `agent.py` builds `LlmAgent(model=config.MODEL_ID, instruction=prompt.md, tools=[...])` | — | adk-tool-interface-design | Declaration dump at 2.8.0 |
| D2, I1 | `confluence.py` adds the CQL space filter from `config.CONFLUENCE_SPACES`; `read_runbook` checks the page's space | — | adk-tool-interface-design | Real CQL syntax against Confluence Cloud (G03) |
| D3, I2, I3 | `tools.py` draft/create pair; the create tool is wrapped with ADK confirmation (`FunctionTool(..., require_confirmation=...)`, check at 2.8.0); `jira.py` makes one POST with no retry | — | safe-api-tool-calls | Confirmation with `adk web` and the in-memory session (O6) |
| D5 | `config.MODEL_ID = "gemini-3.8-flash"`, Vertex backend through environment variables | Vertex AI in the chosen region | adk-model-and-output-contracts | Availability and price on Vertex (G01) |
| I5 | `RunConfig(max_llm_calls=8)` where the Runner is owned (tests, the G06 app); a budget alert for `adk web` | Billing budget | adk-operational-guardrails | Behaviour of `adk web` without the app's RunConfig (G02 note) |
| Secrets | `config.py` reads tokens from Secret Manager via ADC; `.env` holds only resource names | Secret Manager, IAM | adk-tool-auth-and-secrets | G01 |
| D7 (phase 2) | FastAPI owning the `Runner`; IAP JWT verified in middleware; `user_id` = email | Cloud Run, IAP | adk-tool-auth-and-secrets / deploy-adk-on-google-cloud | O2 |

## Goals and dependencies

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | State |
| --- | --- | --- | --- | --- | --- | --- |
| G01 GCP project, model and Atlassian access ready | 1 | implementation (setup) | 4–7 | — | adk-tool-auth-and-secrets | ready; external waits |
| G02 Runbook answers with citations, offline | 1 | implementation | 3–5 | — | adk-tool-interface-design | ready |
| G03 Runbook answers measured on real Confluence | 1 | implementation | 4–7 | G01, G02 | adk-agent-evaluation | ready after deps |
| G04 Ticket created only after confirmation | 1 | implementation | 4–7 | G02 (offline), G01 (live) | safe-api-tool-calls | ready; O4, O6 |
| G05 Decide the identity provider path for IAP | 2 | discovery | 1–2 | — | adk-tool-auth-and-secrets | proposed |
| G06 Signed-in web page with per-user sessions | 2 | implementation | 5–9 | G04, G05 | adk-tool-auth-and-secrets | proposed |
| G07 Hosted on Cloud Run behind IAP | 2 | implementation | 6–10 | G06 | deploy-adk-on-google-cloud | proposed |
| G08 Tests in CI and a release manifest | 2 | implementation | 4–8 | G04 | adk-release-engineering | proposed |
| G09 Adversarial cases for the write tool | 2 | implementation | 3–5 | G04 | adk-agent-security | proposed |
| G10 Tickets attributed to the requesting analyst | 2 | implementation | 2–4 | G06 | safe-api-tool-calls | proposed |
| G11 Measure time-to-runbook against the baseline | 2 | discovery | 2–4 | G07 | adk-agent-evaluation | proposed |

The phase totals are sums of their goals. Phase 1: 4+3+4+4 = 15 to
7+5+7+7 = 26. Phase 2: 1+5+6+4+3+2+2 = 23 to 2+9+10+8+5+4+4 = 42.

### G01 — GCP project, model and Atlassian access ready

- **Phase and estimate:** phase 1. Human hours, agent-assisted: hands-on 3–5,
  review and verify 1–2, total 4–7. This includes the team's first GCP project
  and IAM. Calendar waits: a GCP project and billing link from the
  organisation or finance admin (1–5 working days); Atlassian bot accounts
  with space read and `ITHD` create-only permissions from the Atlassian admin
  (1–5 working days). Owner: Engineer B.
- **Outcome and linked decisions:** the developers can call the pinned model on
  Vertex and read both Atlassian tokens through ADC, with nothing secret in the
  repository. Linked: D5, D6, floor.
- **Scope:** in: the project, Vertex AI API, region choice, budget alert at
  US$100 a month, two Secret Manager secrets, developer IAM roles, `.env.example`
  and the `pyproject.toml` pins. Out: Cloud Run, IAP, service accounts for
  hosting (G07).
- **Depth:** internal tool. Keyless developer ADC and least-privilege roles.
  The floor kept: secrets only in Secret Manager, and a spend alert.
- **Implementation route:** `config.py` loads secrets by resource name. A
  pinned `google-adk==2.8.0`. Re-read the Vertex model page and pricing page;
  record their URLs and dates in the design (O5).
- **Prerequisites:** admin contacts for GCP and Atlassian (request on day 1).
- **Primary skill:** adk-tool-auth-and-secrets.
- **Supporting skills:** adk-model-and-output-contracts, to confirm the
  `gemini-3.8-flash` pin or the `gemini-3.5-flash` fallback and record its
  lifecycle date.
- **Acceptance:**
  - A one-call smoke test with the pinned model ID returns text.
  - Both secrets are read via ADC.
  - The budget alert exists.
  - `git grep` finds no token.
  - A developer without the Secret Accessor role is denied.
- **Verification:** authorised live; at most 5 model calls.
- **Execution scope:** requires the user's go-ahead for project creation and
  billing. That is not authorised by this design.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G01 from docs/plans/helpdesk-assistant.md. Read docs/architecture/helpdesk-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases and record evidence here.`

### G02 — Runbook answers with citations, offline

- **Phase and estimate:** phase 1. Hands-on 1–2, review and verify 2–3, total
  3–5. No waits. Owner: Engineer A.
- **Outcome:** an analyst's question produces an answer that cites runbook
  URLs, run against a fake Confluence. Linked: D1, D2, D4, D6, I1, I4, I5.
- **Scope:** in: `agent.py`, `prompt.md`, `config.py`, `confluence.py` (an
  HTTP client behind an interface), the tools `search_runbooks` and
  `read_runbook`, fakes, and tests through the real `Runner` with a scripted
  model. Out: live calls (G03) and Jira (G04).
- **Depth:** results bounded (5 hits, 8,000 characters); space allow-list in
  code; `max_llm_calls=8`; pinned model and ADK. No write tool, so the
  security split is not needed yet.
- **Implementation route:** as in the implementation map. Confirm the 2.8.0
  APIs for `LlmAgent`, `FunctionTool` and `RunConfig` from the installed
  package, and record the pin.
- **Prerequisites:** none. It runs offline with fakes.
- **Primary skill:** adk-tool-interface-design.
- **Supporting skills:** adk-agent-instructions (prompt.md and a
  rendered-request test); adk-model-and-output-contracts (model config and
  thinking level).
- **Acceptance:**
  - A scripted question → `search_runbooks` → `read_runbook` → an answer
    containing the page URL.
  - An empty search gives "no runbook found", with no wider CQL.
  - A page in space `HR` gives `not_allowed`.
  - A looping model stops at 8 calls.
  - The declaration dump shows 4 or fewer tools, with their byte size recorded.
- **Verification:** `pytest tests/` offline (requires google-adk installed).
- **Execution scope:** local file changes only.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G02 from docs/plans/helpdesk-assistant.md. Read docs/architecture/helpdesk-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G03 — Runbook answers measured on real Confluence

- **Phase and estimate:** phase 1. Hands-on 2–4 (gold set with the lead,
  judging answers), review and verify 2–3, total 4–7. Waits: about 2 hours of
  the helpdesk lead's time for labelling. Owner: Engineer A.
- **Outcome:** the lead sees a scored table showing how often the assistant
  cites the right runbook. Linked: D2, D5, I4.
- **Scope:** in: `eval/gold_questions.yaml` (about 20 real questions with
  expected page IDs, including 3 with no runbook), `eval/run_gold.py`, a
  results table, prompt adjustments, and a secret-pattern scan of the runbook
  space. Out: semantic retrieval (Later) and CI (G08).
- **Depth:** small regression set, no judge model (exact page-ID match plus a
  human read of the answers). Budget: at most 200 model calls a run.
- **Prerequisites:** G01 and G02.
- **Primary skill:** adk-agent-evaluation.
- **Supporting skills:** adk-agent-instructions (prompt iteration on misses);
  protect-adk-sensitive-data (the runbook secret scan and keeping content out
  of logs).
- **Acceptance:**
  - The results table shows hit rate @1 and @5 against the target (provisional
    70% @5).
  - The 3 no-runbook questions are answered "none found".
  - The scan report lists 0 secret-like strings, or the hits are reported to
    the knowledge owner and the space is not used until they are fixed.
- **Verification:** authorised live (Confluence read and Vertex), with limits
  stated in the run record.
- **Execution scope:** reads from the configured spaces only.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G03 from docs/plans/helpdesk-assistant.md. Read docs/architecture/helpdesk-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases and record evidence here.`

### G04 — Ticket created only after confirmation

- **Phase and estimate:** phase 1. Hands-on 1–3, review and verify 3–4, total
  4–7. Waits: the Jira admin's decision on the real `ITHD` project versus a
  sandbox (O4). Owner: Engineer B.
- **Outcome:** "raise a ticket for network" shows the exact draft. Only the
  analyst's confirmation creates it, and the reply shows the key. Linked: D3,
  I2, I3.
- **Scope:** in: `jira.py`, the tools `draft_jira_ticket` and
  `create_jira_ticket`, the draft state machine, the `hda-<op_id>` label, the
  "Requested by" line, and tests. Out: reporter attribution (G10),
  adversarial suite (G09), retries and reconciliation.
- **Depth:** confirmation enforced in code; one project; allow-listed fields;
  no automatic retry; an uncertain outcome shown to the analyst.
- **Implementation route:** check ADK 2.8.0 tool confirmation with `adk web` and
  the in-memory session (O6). If it is unsupported, keep create unavailable in
  `adk web` and move the confirm action to the G06 page.
- **Prerequisites:** G02 for the agent skeleton; G01 for the live check.
- **Primary skill:** safe-api-tool-calls.
- **Supporting skills:** adk-operational-guardrails (the confirmation
  mechanics); adk-tool-interface-design (the two new tool declarations);
  adk-agent-security (this agent now reads untrusted runbook text and holds a
  write, so the confirmation must be structural).
- **Acceptance:**
  - Draft, then confirm, gives one fake Jira POST and the key in the reply.
  - Without confirmation there are 0 POSTs.
  - Confirming an altered draft gives 0 POSTs.
  - A timeout gives 1 POST, the status `uncertain`, and a second confirm is
    refused.
  - A 400 response gives `failed` with the field error.
  - One live confirmed ticket in the agreed project.
- **Verification:** offline `pytest tests/test_ticket_flow.py`, plus one
  authorised live create.
- **Execution scope:** the live create needs the O4 decision.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G04 from docs/plans/helpdesk-assistant.md. Read docs/architecture/helpdesk-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### Phase 2 goals (coarser; phase 1 results may change them)

- **G05 Decide the identity provider path (1–2 h, discovery, adk-tool-auth-and-secrets).**
  Is it a Google group with IAP, or workforce identity federation? Stop when
  the IdP and group are named. This unblocks G06 and G07.
- **G06 Signed-in web page with per-user sessions (5–9 h, adk-tool-auth-and-secrets; supporting adk-frontend-integration).**
  A FastAPI app owns the Runner, verifies the IAP JWT, sets `user_id` to the
  email, provides a simple chat and confirm page, and sets `max_llm_calls`.
  Acceptance: user B cannot load user A's session; a request without a valid
  JWT gets 401.
- **G07 Hosted on Cloud Run behind IAP (6–10 h, deploy-adk-on-google-cloud; supporting adk-agent-observability, adk-release-engineering).**
  A service account with secret access only, ingress through IAP, one
  instance, structured logs without content, and token counts. Acceptance: a
  non-group account is denied; the logs contain no message text.
- **G08 Tests in CI and a release manifest (4–8 h, adk-release-engineering).**
  `release.json` records the ADK pin, model ID, prompt and tool schema hashes;
  CI runs the offline tests. Acceptance: CI fails on a changed model alias.
- **G09 Adversarial cases for the write tool (3–5 h, adk-agent-security).**
  An injected runbook page and pasted end-user text. Acceptance:
  `create_jira_ticket` is never executed without confirmation.
- **G10 Tickets attributed to the requesting analyst (2–4 h, safe-api-tool-calls).**
  The reporter accountId is looked up from the verified email. Acceptance:
  the reporter equals the signed-in user; with no match, the bot is reporter
  plus the line.
- **G11 Measure time-to-runbook against the baseline (2–4 h, adk-agent-evaluation).**
  A before/after sample of 20 calls. Acceptance: the median time is reported
  together with the correction rate.

## Later

| Item | Trigger that brings it forward | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| Semantic retrieval (Vertex AI Search Confluence connector) | G03 hit rate @5 below 70% | Some questions get "none found" | adk-memory-architecture |
| Durable sessions (DatabaseSessionService) | Lost-chat complaints, or more than one instance | Restarts drop chats | adk-memory-architecture |
| Per-user Confluence permissions (OAuth 3LO) | Page restrictions, or non-helpdesk users | All staff see the whole space | adk-tool-auth-and-secrets |
| Per-user daily model cap | Hosted spend above 50% of the allowance | Budget alert only | adk-operational-guardrails |
| SLOs and alerts | Daily use by all 25, or an incident | Failures noticed by users | adk-agent-observability |
| Model migration | `gemini-3.8-flash` retirement announced | — | adk-release-engineering |
| Google Chat or Slack surface | User demand after G07 | — | adk-frontend-integration |

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| docs/architecture/helpdesk-assistant.md | Method, assumptions and decisions |
| eval/results/ summary (from G03) | Latest gold-question score |
| This plan | Remaining limits and deferred controls |

## Open decisions for further planning

See the design's [Open decisions](../architecture/helpdesk-assistant.md#open-decisions)
O1–O6. O2 blocks G06 and G07; O4 blocks only G04's live check; O5 blocks G03.

## Resume here

- **Next goal:** G01 and G02 in parallel. G02 needs nothing external; G01
  starts the admin waits.
- **Read first:** the design, then this plan.
- **Next action:** Engineer B sends the GCP and Atlassian admin requests;
  Engineer A runs G02.
- **Continuation prompt:**

```text
/adk-engineer Carry out G02 — Runbook answers with citations, offline from docs/plans/helpdesk-assistant.md.
Read docs/architecture/helpdesk-assistant.md and preserve its accepted decisions.
Use adk-tool-interface-design with adk-agent-instructions and adk-model-and-output-contracts.
Work within local file changes only, verify the G02 acceptance cases offline, and update
the plan with actual evidence and remaining blockers.
```

After that goal: `/adk-engineer Continue the next ready goal in docs/plans/helpdesk-assistant.md.`
