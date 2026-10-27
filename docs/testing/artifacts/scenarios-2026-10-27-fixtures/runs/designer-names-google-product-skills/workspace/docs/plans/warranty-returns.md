# Implementation plan: warranty answers and return requests

Status: draft. No goal has run. The design's scope answers are assumptions (design, "Assumed answers"), so this plan is provisional until they are confirmed.
Architecture: [docs/architecture/warranty-returns.md](../architecture/warranty-returns.md)
Continuation source of truth: this plan (no tickets written; ask for them per phase).

## Summary for the reader

- **Profile and phase 1:** Production profile, cut to what two developers can carry in six weeks. Phase 1 delivers a signed-in customer journey on Cloud Run: grounded warranty answers, a confirmed and idempotent return request, the production floor, and a go-live review, ending in a canary launch to a small share of customers. Ramp to 100 percent, the ASVS Level 2 review, the support rollout pack and the first live bill come in phase 2.
- **Effort and finish (hand arithmetic, the schedule helper was not run):** phase 1 totals 149 to 223 human hours against 216 usable (288 focused hours less a 25 percent reserve); only the low end fits. By my rough walk the calendar finishes between working day 30 and day 41 against 30 available, so the 2026-12-11 date holds only if every wait comes in at its low end. Details and untested remedies are under "Delivery profile and capacity".
- **Largest risks:** (1) calendar waits on other teams (landing zone, data and return-system access, identity, privacy sign-off, pen test) set the finish more than the work does; W1 to W3, W5 and the pen-test booking must be requested on day 1. (2) The return system may lack an idempotency key or lookup (O2), which weakens C5; G03 settles it first. (3) Real customer data with a model in the loop: the residency answer (O5) can change the model and region after work has started.
- **Decisions needed from you:** confirm or move the cut line; O4 spend ceiling and volume; O5 jurisdictions and retention; O10 hours and start date; O8 SPA or portal. The rest are in the design's open decisions.
- **Next prompt:** the three access requests and the pen-test booking are human actions for today. Then `/adk-engineer Carry out G02 from docs/plans/warranty-returns.md.` G01 needs `adk-presenter`, which is not installed.

## Destination and constraints

A signed-in customer gets warranty answers about their own products from the product database, and files a return request after confirming a stored proposal, once. Non-goals and the accepted stack are in the design. Authorization today: design and plan only. No repository, cloud project or credentials were touched. Nothing is installed.

Inherited from the design, not decided here: model ID chosen in G02 from the lifecycle table; ADK pin assumed `google-adk==2.8.0` and confirmed in G02/A3; prompt, model, judge and tool schema change together as a release (C10).

Setup prerequisites, because these skills are not installed in this environment: `adk-presenter`, `adk-agent-evaluation`, `adk-governance-pack`, `adk-fastapi-backend`, `adk-frontend-integration`, `adk-agent-security`, `adk-agent-instructions`, `adk-tool-interface-design`, `adk-model-and-output-contracts`, `adk-memory-architecture`, `safe-api-tool-calls`, `adk-operational-guardrails`, `protect-adk-sensitive-data`, `adk-release-engineering`, `adk-workflow-design`, and the Google product skills named per goal. `adk-engineer`, `deploy-adk-on-google-cloud`, `adk-agent-observability` and `adk-tool-auth-and-secrets` are installed. A goal does not claim a skill's guidance until it is installed.

## Delivery profile and capacity

Profile: production, linked to the design's delivery constraints. Capacity assumptions: two developers, 4.8 focused hours a day each, 30 working days from 2026-11-02, reserve 25 percent. Estimates are human hours with a coding agent, hands-on plus review; ADK goals include a ×1.5 multiplier for a team new to ADK (stated once, applied to every implementation goal; presentation, labelling and governance goals keep their own figures). The team knows GCP, so no first-project day is added; the project itself is W1.

| Phase | Delivers | Goals | Human hours | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship | Controlled launch to a small share of customers | G01 to G19 | 149–223 | 2 × 4.8 × 30 = 288; usable 216 |
| 2, harden and ramp | General availability and the first measured results | G20 to G25 | 33–53 (rough) | After phase 1 |

Schedule block, the single source of each estimate and wait:

```yaml
- goal: W0
  phase: 1
  total: 0
  calendar_waits: go-ahead decision on the design from the sponsor
  wait_days: 2-3
  blocked_by: [G01]
  type: discovery
- goal: W1
  phase: 1
  total: 0
  calendar_waits: access request to the landing-zone team for the project, billing link, IAM grants and policy exceptions
  wait_days: 5-10
  blocked_by: []
  type: discovery
- goal: W2
  phase: 1
  total: 0
  calendar_waits: access request to the product database and return system owners for read access and sandbox credentials
  wait_days: 5-10
  blocked_by: []
  type: discovery
- goal: W3
  phase: 1
  total: 0
  calendar_waits: access request to the identity owners for an OIDC client and test customers
  wait_days: 3-5
  blocked_by: []
  type: discovery
- goal: W5
  phase: 1
  total: 0
  calendar_waits: warranty experts labelling session booked and held
  wait_days: 5-8
  blocked_by: []
  type: discovery
- goal: W4
  phase: 1
  total: 0
  calendar_waits: privacy and legal sign-off of the DPIA input from the privacy owner
  wait_days: 10-15
  blocked_by: [G13]
  type: governance
- goal: W6
  phase: 1
  total: 0
  calendar_waits: penetration test by an outside party on staging, booked on day 1
  wait_days: 8-10
  blocked_by: [G09, G11]
  type: discovery
- goal: W7
  phase: 1
  total: 0
  calendar_waits: go-live approval from the sponsor after the review
  wait_days: 2-3
  blocked_by: [G18]
  type: discovery
- goal: G01
  phase: 1
  hands_on: 2-3
  review: 1
  total: 3-4
  owner: Dev A
  blocked_by: []
  contracts: []
  security: []
  type: presentation
  status: planned
- goal: G02
  phase: 1
  hands_on: 4-6
  review: 2-3
  total: 6-9
  owner: Dev A
  blocked_by: []
  contracts: [C7, C8, C10]
  security: [SB15, SB16]
  type: implementation
  status: planned
- goal: G03
  phase: 1
  hands_on: 4-6
  review: 1-2
  total: 5-8
  owner: Dev A
  blocked_by: [W2, W3]
  contracts: [C1, C2, C5]
  security: []
  type: discovery
  status: planned
- goal: G04
  phase: 1
  hands_on: 6-9
  review: 3-5
  total: 9-14
  owner: Dev B
  handoff: 1
  blocked_by: [G02, G03, W0]
  contracts: [C1, C9]
  security: [SB01, SB02, SB03, SB04, SB13, SB20]
  type: implementation
  status: planned
- goal: G05
  phase: 1
  hands_on: 7-10
  review: 4-6
  total: 11-16
  owner: Dev A
  blocked_by: [G02, G03, W0]
  contracts: [C1, C2, C6, C9]
  security: [SB04, SB17]
  type: implementation
  status: planned
- goal: G06
  phase: 1
  hands_on: 6-9
  review: 2-3
  total: 8-12
  owner: Dev A
  blocked_by: [G05, W5]
  contracts: [C2, C6, C10]
  security: []
  type: implementation
  status: planned
- goal: G07
  phase: 1
  hands_on: 8-12
  review: 4-6
  total: 12-18
  owner: Dev A
  handoff: 1
  blocked_by: [G04, G05]
  contracts: [C1, C3, C4, C5, C6]
  security: [SB18]
  type: implementation
  status: planned
- goal: G08
  phase: 1
  hands_on: 6-9
  review: 4-6
  total: 10-15
  owner: Dev A
  blocked_by: [G07]
  contracts: [C5, C7, C8, C9]
  security: [SB16]
  type: implementation
  status: planned
- goal: G09
  phase: 1
  hands_on: 9-13
  review: 4-6
  total: 13-19
  owner: Dev B
  handoff: 1
  blocked_by: [G04, G05]
  contracts: [C3, C8, C9]
  security: [SB05, SB06, SB07, SB09, SB10, SB13, SB19]
  type: implementation
  status: planned
- goal: G10
  phase: 1
  hands_on: 5-8
  review: 3-4
  total: 8-12
  owner: Dev B
  handoff: 1
  blocked_by: [G04, G05]
  contracts: [C7, C8]
  security: [SB14, SB19]
  type: implementation
  status: planned
- goal: G11
  phase: 1
  hands_on: 8-12
  review: 4-6
  total: 12-18
  owner: Dev B
  blocked_by: [G02, W1]
  contracts: [C7, C8, C10]
  security: [SB05, SB25]
  type: implementation
  status: planned
- goal: G12
  phase: 1
  hands_on: 7-10
  review: 3-4
  total: 10-14
  owner: Dev B
  handoff: 1
  blocked_by: [G11, G06]
  contracts: [C2, C5, C7, C9, C10]
  security: []
  type: implementation
  status: planned
- goal: G13
  phase: 1
  hands_on: 5-8
  review: 2-3
  total: 7-11
  owner: Dev A
  blocked_by: [G03]
  contracts: [C7]
  security: []
  type: governance
  status: planned
- goal: G14
  phase: 1
  hands_on: 6-9
  review: 3-4
  total: 9-13
  owner: Dev A
  handoff: 1
  blocked_by: [G07, G09]
  contracts: [C1, C3, C6]
  security: [SB17, SB23]
  type: implementation
  status: planned
- goal: G15
  phase: 1
  hands_on: 6-9
  review: 3-4
  total: 9-13
  owner: Dev B
  handoff: 1
  blocked_by: [G08, G10, G12, G14, W6]
  contracts: [C8, C9]
  security: [SB21, SB22, SB24]
  type: implementation
  status: planned
- goal: G16
  phase: 1
  hands_on: 4-6
  review: 2-3
  total: 6-9
  owner: Dev B
  blocked_by: [G15]
  contracts: [C1, C2, C3, C4, C5, C9]
  security: []
  type: journey
  status: planned
- goal: G17
  phase: 1
  hands_on: 3-5
  review: 1-2
  total: 4-7
  owner: Dev B
  blocked_by: [G15]
  contracts: [C5, C10]
  security: []
  type: implementation
  status: planned
- goal: G18
  phase: 1
  hands_on: 3-4
  review: 1-2
  total: 4-6
  owner: Dev B
  blocked_by: [G16, G17, W4]
  contracts: []
  security: []
  type: presentation
  status: planned
- goal: G19
  phase: 1
  hands_on: 2-3
  review: 1-2
  total: 3-5
  owner: Dev B
  blocked_by: [W7, G17]
  contracts: [C8, C10]
  security: []
  type: implementation
  status: planned
```

**Schedule check: NOT RUN.** This session had no way to execute `scripts/check_schedule.py`, so the figures below are my hand arithmetic, not the helper's, and the design's grid, contract and security-rule coverage was checked by reading, not by the script. Run this before relying on any of it:

```bash
python3 .claude/skills/adk-system-designer/scripts/check_schedule.py --plan docs/plans/warranty-returns.md \
  --design docs/architecture/warranty-returns.md --days 30 --reserve 0.25 \
  --person "Dev A=4.8" --person "Dev B=4.8"
```

Hand figures, phase 1: total 149 to 223 hours (sum of the entries above). Dev A 71 to 106 hours, Dev B 78 to 117, each against 144 focused hours less the 25 percent reserve, 108. The high end does not fit for Dev B and the total (223 against 216) is marginal. The calendar is the larger problem: waits W1 and W2 (up to 10 days each), then the chain G03, G05, G07, G09, the pen test W6 (up to 10 days), G15, G16 or G17, G18, W7 and G19. My rough walk puts the finish near working day 30 if every wait comes in at its low end and near day 41 if they come in at the high end, against 30 available. So phase 1 meets 2026-12-11 only in the best case. Remedies I have not tested with the helper: a later external canary (G19 after W6 and its fixes, with G15's drills and scans not waiting for the pen test), starting the pen test as soon as G09 and G11 exist, a third person for G11 and G12, or a date of about 8 weeks. Choose one and rerun the check.

## Implementation map

| Contract / decision | Component and integration point (proposed layout) | GCP responsibility | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |
| C1, D6 | `app/auth.py` verified-principal dependency; `user_id` overwritten on every Runner call; tools read `tool_context.state` | Customer identity provider; workload identity | `adk-fastapi-backend` | Token audience against a captured token (O3) |
| C2, D2, D3 | `agent/tools.py` projections; `agent/schema.py` output model; `app/validate.py` evidence check | Read-only access to product database | `adk-tool-interface-design` | Access path (O1) |
| C3, C4, D4 | `returns/proposals.py`, `returns/eligibility.py`, `/api/returns/{id}/confirm` | Cloud SQL | `safe-api-tool-calls` | Eligibility rules (O6) |
| C5, D5 | `returns/operations.py`, `returns/rms_client.py`, reconcile endpoint | Cloud Scheduler, Secret Manager | `safe-api-tool-calls` | Idempotency and lookup (O2) |
| C7, C8, D8 | `app/admission.py`, `app/retention.py`, logging filter | Cloud SQL, model project quota | `adk-operational-guardrails`, `protect-adk-sensitive-data` | Retention period (O5), ceiling (O4) |
| C9, C10, D10 | `release/manifest.py`, Cloud Build config, alert policies | Cloud Run revisions, Cloud Build, Monitoring | `adk-release-engineering`, `adk-agent-observability` | Baselines from first week |

The first goal writes a project `AGENTS.md` (pins, `make check`, the evidence directory, the design's invariants) with a one-line `CLAUDE.md` include.

## Web stack and companion skills

The design uses the designer's web application defaults without deviation (baseline SPA, same origin). G09 writes the companion table with pins into `AGENTS.md` from that reference and links to it afterwards. Companion skills are named by that reference; none is installed here.

## Goals and dependencies

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | State |
| --- | --- | --- | --- | --- | --- | --- |
| W0–W7 calendar waits | 1 | wait | 0 | see schedule | none | request W1, W2, W3, W5 and the W6 booking on day 1 |
| G01 Go-ahead presentation | 1 | presentation | 3–4 | none | `adk-presenter` | ready once the skill is installed |
| G02 Skeleton, pins, `make check` | 1 | implementation | 6–9 | none | `adk-workflow-design` | ready |
| G03 Interface discovery | 1 | discovery | 5–8 | W2, W3 | `adk-tool-interface-design` | blocked on W2, W3 |
| G04 Customer identity and scope | 1 | implementation | 9–14 | G02, G03, W0 | `adk-fastapi-backend` | blocked |
| G05 Grounded warranty answers | 1 | implementation | 11–16 | G02, G03, W0 | `adk-tool-interface-design` | blocked |
| G06 Evaluation set and runner | 1 | implementation | 8–12 | G05, W5 | `adk-agent-evaluation` | blocked |
| G07 Return proposal and confirmation | 1 | implementation | 12–18 | G04, G05 | `safe-api-tool-calls` | blocked |
| G08 Return-system adapter and reconcile | 1 | implementation | 10–15 | G07 | `safe-api-tool-calls` | blocked |
| G09 Chat API and baseline SPA | 1 | implementation | 13–19 | G04, G05 | `adk-frontend-integration` | blocked |
| G10 Data protection and spend stops | 1 | implementation | 8–12 | G04, G05 | `adk-operational-guardrails` | blocked |
| G11 Cloud Run, edge and data tier | 1 | implementation | 12–18 | G02, W1 | `deploy-adk-on-google-cloud` | blocked on W1 |
| G12 Observability and release gate | 1 | implementation | 10–14 | G11, G06 | `adk-agent-observability` | blocked |
| G13 Governance papers | 1 | governance | 7–11 | G03 | `adk-governance-pack` | blocked |
| G14 Threat model and adversarial suite | 1 | implementation | 9–13 | G07, G09 | `adk-agent-security` | blocked |
| G15 Staging checks and drills | 1 | implementation | 9–13 | G08, G10, G12, G14, W6 | `adk-release-engineering` | blocked |
| G16 Journey on staging | 1 | journey | 6–9 | G15 | `adk-agent-evaluation` | blocked |
| G17 Operations handover | 1 | implementation | 4–7 | G15 | `adk-agent-observability` | blocked |
| G18 Go-live review | 1 | presentation | 4–6 | G16, G17, W4 | `adk-presenter` | blocked |
| G19 Canary launch | 1 | implementation | 3–5 | W7, G17 | `deploy-adk-on-google-cloud` | blocked |

Every implementation goal runs the earlier goals' acceptance items it touches as regression checks. Product skills below are unconfirmed against the live catalogue; confirm each through the installed `finding-google-skills` router before first use, and treat their commands as proposals needing approval for the scope.

### G01 — Go-ahead presentation

- **Phase and estimate:** 1; hands-on 2–3, review 1, total 3–4; wait W0 for the decision; owner Dev A.
- **Outcome, contracts, decisions:** The sponsor sees the design, the cut line, the assumptions to confirm (O1–O11) and the cost and risk position, and decides.
- **Scope:** Business audience. Excludes any claim about results; nothing is built.
- **Depth:** Cites design IDs only; every figure is a labelled assumption.
- **Implementation route:** Deck outline, narrative, expected questions, one-page decision memo from this plan and the design.
- **Resources created:** none.
- **Prerequisites:** none beyond the design.
- **Primary skill:** `adk-presenter`. **Supporting:** none. **Companion:** none. **Design system:** none. **Security rules:** none.
- **Acceptance:**
  - A1 THE outline SHALL pass the presenter's deck check with every claim citing a design or plan ID.
  - A2 THE memo SHALL ask for the decisions O4, O5, O10 and the cut line, and record who decides and by when.
- **Verification:** the deck check; manual read-through.
- **Execution scope:** document only.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-presenter Build the go-ahead review for docs/plans/warranty-returns.md (G01), business audience.`

### G02 — Skeleton, pins and `make check`

- **Phase and estimate:** 1; hands-on 4–6, review 2–3, total 6–9; owner Dev A.
- **Outcome, contracts, decisions:** A local repository where one `LlmAgent` with a stub tool runs through the Runner under scripted-model tests, and `make check` runs. Proves C7 (logging filter exists), C8 (`max_llm_calls`), C10 (pins), SB15, SB16. Implements D2 skeleton.
- **Scope:** Layout, lockfile, `AGENTS.md`, CI skeleton, secret scan, dependency audit, scripted model, model ID selection. Excludes real tools, cloud.
- **Depth:** Floor items: no secrets, spend stop, pinned model.
- **Implementation route:** proposed layout in the implementation map; model ID from `adk-model-and-output-contracts/assets/model-lifecycle-*.json` once installed, otherwise the first acceptance is to obtain it; region from O5 (ask, or record the assumption).
- **Resources created:** none.
- **Prerequisites:** Python 3.11 or later; package installs are done by the developer, and an install is its own approval.
- **Primary skill:** `adk-workflow-design`. **Supporting:** `adk-model-and-output-contracts` (model ID and lifecycle date). **Companion:** none.
- **Security rules:** SB15, SB16.
- **Acceptance:**
  - A1 THE `make check` SHALL run lint, unit tests, the Python dependency audit and a secret scan, and fail on a seeded finding in each (SB15, SB16).
  - A2 THE scripted-model run SHALL pass through the Runner with `max_llm_calls` set and the model ID pinned with its retirement date recorded (C8, C10).
  - A3 THE chosen ADK pin SHALL be confirmed against installed signatures for `RunConfig`, `DatabaseSessionService` and tool context, and any move from `google-adk==2.8.0` recorded (C10).
  - A4 THE logging filter SHALL drop message content fields in a unit test (C7).
- **Verification:** offline; `make check` exit codes.
- **Execution scope:** local only.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G02 from docs/plans/warranty-returns.md. Read docs/architecture/warranty-returns.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G03 — Interface discovery (bounded)

- **Phase and estimate:** 1; hands-on 4–6, review 1–2, total 5–8; waits W2, W3; owner Dev A.
- **Outcome, contracts:** A memo at `docs/discovery/interfaces.md` that settles O1, O2, O3 and O7 or says which stay open. Contracts touched: C1, C2, C5.
- **Question and stopping condition:** What are the product database, return system and token facts the design assumed? Stop at 8 hours or when A1 to A5 are answered, whichever is first; unresolved items become open decisions with an owner.
- **Scope:** Read-only inspection of sandbox or sample data. No writes.
- **Depth:** Records facts and assumptions separately; no secrets in the memo.
- **Prerequisites:** W2 and W3 satisfied (access request granted); no production writes.
- **Primary skill:** `adk-tool-interface-design`. **Supporting:** `adk-tool-auth-and-secrets` (token and credential facts). **Companion:** none.
- **Acceptance:**
  - A1 THE memo SHALL list the product database tables and columns the journey needs, the access path, freshness, and which columns are free text (C2, C6).
  - A2 THE memo SHALL record the return system's create call, whether it accepts an idempotency key and for how long, its status lookup, sandbox availability and error codes (C5).
  - A3 THE memo SHALL record the token issuer, audience, customer claim and its mapping to the product database's customer key (C1).
  - A4 THE memo SHALL record the outcome measure and baseline, or name the owner who will supply it (O7).
  - A5 IF the return system lacks an idempotency key or lookup, THEN the memo SHALL propose the revised C5 and D5 and mark G07 and G08 blocked on a checkpoint.
- **Verification:** read of the memo against each item.
- **Execution scope:** read-only against sandbox; production data only if the owner grants it in W2.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G03 from docs/plans/warranty-returns.md. Read docs/architecture/warranty-returns.md and record the memo.`

### G04 — Customer identity and scope

- **Phase and estimate:** 1; hands-on 6–9, review 3–5, total 9–14; handoff 1 from G03; owner Dev B.
- **Outcome, contracts, decisions:** Every `/api` route verifies the customer token; the principal overwrites `user_id` on every ADK call; sessions are owner-filtered; revocation is checked before sensitive actions. Proves C1, C9; implements D6.
- **Scope:** Verifier, dependency, session ownership, a two-customer test fixture. Excludes the SPA sign-in UI (G09).
- **Depth:** Build, at the floor and tiers 1 to 6.
- **Implementation route:** `app/auth.py`, middleware, owner-filtered session lookup; library from the identity provider (O3).
- **Prerequisites:** G02, G03, W0. Token audience confirmed against a captured token.
- **Primary skill:** `adk-fastapi-backend`. **Supporting:** `adk-tool-auth-and-secrets`, `adk-frontend-integration` (session routes). **Security rules:** SB01, SB02, SB03, SB04, SB13, SB20.
- **Acceptance:**
  - A1 WITH the verifier unset, EVERY `/api` route SHALL return 401 (C1, SB01).
  - A2 AN expired token, a wrong-audience token and a forged-header request SHALL be rejected (C1, SB02).
  - A3 A forged `user_id` in the body SHALL run in the caller's own scope, and another customer's session SHALL return the same 404 body as an unknown one with no model call (C1, SB03).
  - A4 IN a two-customer test, a tool call whose arguments name another customer's product SHALL find nothing (C1, SB04).
  - A5 A revoked token SHALL be refused on a sensitive-action route (SB20).
  - A6 A verifier or key-fetch outage SHALL deny and return a generic error with a request ID (C9, SB13).
- **Verification:** offline plus local two-customer fixtures; one captured real token for A2.
- **Execution scope:** local; test customers from W3.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G04 from docs/plans/warranty-returns.md. Read docs/architecture/warranty-returns.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G05 — Grounded warranty answers

- **Phase and estimate:** 1; hands-on 7–10, review 4–6, total 11–16; owner Dev A.
- **Outcome, contracts, decisions:** A customer's warranty question is answered from the record with evidence, or honestly declined. Proves C1, C2, C6, C9; implements D2, D3.
- **Scope:** `list_my_products`, `get_warranty`, output schema with `cannot_answer`, instructions, validator, handoff wording. Excludes returns (G07) and evaluation labelling (G06).
- **Depth:** Build. Typed projections; free-text columns excluded or bounded.
- **Implementation route:** `agent/tools.py`, `agent/schema.py`, `app/validate.py`; customer key from trusted state (a stub principal until G04 lands, then real).
- **Prerequisites:** G02, G03, W0; product-database access path (O1).
- **Primary skill:** `adk-tool-interface-design`. **Supporting:** `adk-model-and-output-contracts` (schema, repair budget), `adk-agent-instructions`, `adk-agent-security` (injection check). **Security rules:** SB04, SB17.
- **Acceptance:**
  - A1 FOR an owned product with a record, THE answer SHALL carry code-computed status, evidence IDs and as-of date (C2).
  - A2 WITH no record, THE answer SHALL say it cannot find the product and offer a handoff, and invent no terms (C2, C9).
  - A3 A scripted answer claiming coverage absent from the turn's tool results SHALL be rejected by the validator, with a bounded repair budget and an explicit failure shape (C2).
  - A4 A product-database text field and a customer message containing an injected instruction SHALL not cause any tool call outside the allowed set, and `propose_return` SHALL not be called without a return intent (C6, SB17).
  - A5 A tool argument naming another customer's product SHALL return not found (C1, SB04).
  - A6 WHEN the model is unavailable, slow or rate limited, THE run SHALL end inside the deadline with an honest message and one retry owner (C9).
  - A7 WHEN the product database is unavailable, slow or its pool is exhausted, THE tool SHALL time out and the answer SHALL be an honest failure (C9).
  - A8 WHEN the model returns blocked, empty, prose, fenced JSON or schema-valid wrong data, THE application SHALL respond as designed and count the wrong-but-valid case separately (C2).
  - A9 THE declaration dump SHALL show at most four tools with bounded results, and the rendered-request test SHALL match the versioned instruction (C2).
  - A10 WHEN the product database rejects a query (permission or schema drift), THE answer SHALL be an honest failure with no partial claim (C9).
  - A11 WHEN the product database credential is expired or revoked, THE tool SHALL fail closed and no fallback credential SHALL be used (C9).
- **Verification:** offline scripted model plus a bounded live check on the pinned model with declared request and cost limits.
- **Execution scope:** local; live model calls need an authorised project (W1).
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G05 from docs/plans/warranty-returns.md. Read docs/architecture/warranty-returns.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G06 — Evaluation set and runner

- **Phase and estimate:** 1; hands-on 6–9, review 2–3, total 8–12; wait W5 for the experts' session; owner Dev A.
- **Outcome, contracts:** A versioned criteria file, a labelled set of at least 40 cases with provenance and expert agreement, and a runner that fails by exit code. Proves C2, C6, C10.
- **Scope:** Warranty questions, out-of-scope and adversarial cases. Excludes the CI wiring (G12).
- **Depth:** Build with a gate.
- **Prerequisites:** G05; the experts named by the warranty policy owner.
- **Primary skill:** `adk-agent-evaluation` (expert-review reference). **Supporting:** none.
- **Acceptance:**
  - A1 A criteria file, a gold set of at least 40 cases with provenance, and an expert agreement report SHALL exist and be versioned (C2).
  - A2 THE runner SHALL exit non-zero when the grounded-answer pass rate is below the threshold agreed with the experts (C2).
  - A3 AT least 10 cases SHALL be out-of-scope or adversarial and expect a refusal or handoff (C2, C6).
  - A4 THE baseline on the pinned model SHALL be recorded with the eval-set hash (C10).
- **Verification:** local runner; live model calls within declared limits.
- **Execution scope:** model calls on an authorised project.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G06 from docs/plans/warranty-returns.md. Read docs/architecture/warranty-returns.md.`

### G07 — Return proposal and confirmation

- **Phase and estimate:** 1; hands-on 8–12, review 4–6, total 12–18; handoff 1 from G04; owner Dev A.
- **Outcome, contracts, decisions:** A customer's return intent becomes a stored, hashed proposal; only an authenticated confirm call files it; stale, over-broad and repeated actions are refused. Proves C1, C3, C4, C5, C6; implements D4, D5 (record and state machine).
- **Scope:** `propose_return` draft tool, eligibility function, confirm endpoint, executor against a fake return system, operation record with unique key, durable dispatch. Excludes the real return system (G08).
- **Depth:** Build. Eligibility rules pending O6.
- **Prerequisites:** G04, G05; O6.
- **Primary skill:** `safe-api-tool-calls`. **Supporting:** `adk-operational-guardrails` (approval binding, expiry), `adk-fastapi-backend` (confirm route), `adk-agent-security` (no model-callable write). **Security rules:** SB18.
- **Acceptance:**
  - A1 NO model-callable tool SHALL make a return-system call; `propose_return` SHALL only write a draft (C3, C6).
  - A2 CONFIRM with a matching hash SHALL call the fake return system once; reject or no confirmation SHALL call it zero times (C3, SB18).
  - A3 IF the warranty ends or the product is returned between proposal and confirm, THEN confirm SHALL be refused and a fresh proposal offered (C3, C4).
  - A4 A proposal or confirm for another customer's product SHALL be refused (C1, C4).
  - A5 TWO concurrent or repeated confirms SHALL yield one operation and one return-system call (C5).
  - A6 AN expired proposal SHALL be refused (C3).
  - A7 "Return everything I own" SHALL produce one proposal per product line with its own confirm, and no bulk filing (C3).
  - A8 "Yes" typed into the chat SHALL not file anything; only the confirm endpoint does (C3, C6).
  - A9 AN ineligible product SHALL be refused in code with a reason code the model cannot override (C4).
  - A10 IF the commit acknowledgement is lost, THEN a retry SHALL return the same operation (C5).
  - A11 AFTER a restart with an operation pending, THE dispatch SHALL resume from the durable record (C5).
- **Verification:** offline with a fake return system and killed-process tests; local database.
- **Execution scope:** local.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G07 from docs/plans/warranty-returns.md. Read docs/architecture/warranty-returns.md.`

### G08 — Return-system adapter and reconcile

- **Phase and estimate:** 1; hands-on 6–9, review 4–6, total 10–15; owner Dev A.
- **Outcome, contracts:** The executor files a request in the sandbox exactly once, even after crashes and lost responses. Proves C5, C7, C8, C9.
- **Scope:** Real adapter, idempotency key, status lookup, reconcile worker, `unknown` handling and support-queue entry, credential handling. Excludes production credentials.
- **Prerequisites:** G07; sandbox credentials from W2; the revised D5 if G03/A5 fired.
- **Primary skill:** `safe-api-tool-calls`. **Supporting:** `adk-tool-auth-and-secrets`. **Security rules:** SB16.
- **Acceptance:**
  - A1 A confirmed proposal SHALL create one record in the sandbox and the customer SHALL see its reference (C5).
  - A2 AFTER a kill between the provider accepting and the receipt being stored, A restart SHALL find the existing record by key, create no second one, and preserve the verified effect (C5, C9).
  - A3 ON timeout or 5xx, THE operation SHALL be `unknown`, the customer SHALL be told it is being checked, a support-queue entry SHALL exist and no resend SHALL occur before lookup (C5, C9).
  - A4 ON a 4xx rejection, THE state SHALL be `rejected`, nothing SHALL be retried and a fresh proposal SHALL be possible (C9).
  - A5 ON a 429, THE adapter SHALL back off with jitter and bounded attempts under one retry owner (C8).
  - A6 WITH the credential expired or revoked, THE adapter SHALL fail closed, raise an alert and use no fallback credential (C9, SB16).
  - A7 A different payload under the same operation ID SHALL be rejected (C5).
  - A8 THE credential SHALL come from Secret Manager or workload identity and appear in no log or event (C7, SB16).
  - A9 AN unexpected or malformed return-system payload SHALL be treated as failure or unknown, never as success (C5, C9).
- **Verification:** local against the sandbox, with a fault-injecting proxy; no production calls.
- **Execution scope:** sandbox only.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G08 from docs/plans/warranty-returns.md. Read docs/architecture/warranty-returns.md.`

### G09 — Chat API and baseline SPA

- **Phase and estimate:** 1; hands-on 9–13, review 4–6, total 13–19; handoff 1 from G05; owner Dev B.
- **Outcome, contracts:** A signed-in customer chats in a browser, with streamed answers and a confirm card rendered from a stored draft. Proves C3, C8, C9; the web rules named below.
- **Scope:** Run and stream route, owner-filtered session routes, run lock, request limits, SPA with sign-in, error handler, headers, generated client. The confirm card is built against the proposals API contract with a fake until G07 is merged; G16 runs it for real. Portal embedding is phase 2 (O8).
- **Prerequisites:** G04, G05; companions pinned from web defaults.
- **Primary skill:** `adk-frontend-integration`. **Supporting:** `adk-fastapi-backend`. **Companion skills:** per web application defaults. **Design system:** `DESIGN.md` from the organisation's house system, or the defaults' baseline if none (O8). **Security rules:** SB05, SB06, SB07, SB09, SB10, SB13, SB19.
- **Acceptance:**
  - A1 A SECOND concurrent run for the same customer SHALL be refused (C8, SB19).
  - A2 AN oversize body SHALL get 413 and a malformed body 422 (SB09).
  - A3 A scripted reply with an `<img onerror>` payload, a `javascript:` link and an image from an unlisted host SHALL render inert and load nothing (C3, SB10).
  - A4 A forced exception SHALL return a generic 500 with a request ID and no stack or provider message (C9, SB13).
  - A5 AT the served build, `/docs`, `/redoc`, `/openapi.json` and ADK's own routes SHALL return no schema, no ADK data and cause no model call, and the header test SHALL pass (SB05, SB07).
  - A6 A preflight from an unlisted origin SHALL receive no allow header (SB06).
  - A7 THE confirm card SHALL show product and remedy from the stored draft, not from model text (C3, SB10).
  - A8 IF the browser disconnects mid-answer, THE run SHALL close and no partial answer SHALL be stored as a finished turn (C9).
  - A9 AFTER a process restart, THE session SHALL continue for its owner only (C1).
- **Verification:** local with Playwright; screenshot and accessibility check at production depth.
- **Execution scope:** local.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G09 from docs/plans/warranty-returns.md. Read docs/architecture/warranty-returns.md.`

### G10 — Data protection and spend stops

- **Phase and estimate:** 1; hands-on 5–8, review 3–4, total 8–12; handoff 1 from G05; owner Dev B.
- **Outcome, contracts:** Customer content stays out of logs; sessions expire and can be erased; a looping or abusive customer and a runaway bill are stopped by the application. Proves C7, C8.
- **Scope:** Logging gate, retention and erasure job, card-number input detector, admission control, kill switch, model-project quota record. Ceiling and volume figures come from O4.
- **Prerequisites:** G04, G05; retention period (O5) or the assumed 30 days recorded as assumption.
- **Primary skill:** `adk-operational-guardrails`. **Supporting:** `protect-adk-sensitive-data`. **Security rules:** SB14, SB19.
- **Acceptance:**
  - A1 LOGS and traces SHALL contain no prompt, reply or personal content, and the denied-access line SHALL be present (C7, SB14).
  - A2 THE retention job SHALL delete sessions and drafts older than the period, and an erasure by customer SHALL remove them (C7).
  - A3 A message containing a payment card number SHALL be refused before storage and model (C7).
  - A4 A looping scripted model SHALL stop at `max_llm_calls` (C8, SB19).
  - A5 A customer at the daily allowance SHALL be refused with no model call (C8).
  - A6 THE kill switch SHALL stop new runs within the stated seconds while status and reconcile still work, and the agent SHALL have no write path to it (C8).
  - A7 WHEN the admission store is unavailable, NEW runs SHALL be refused (C8).
  - A8 THE model-project quota SHALL be set and recorded as a backstop (C8).
  - A9 THE per-request model-call inventory SHALL show the bound including SDK retries (C8).
- **Verification:** offline and local; quota readback is a hosted step in G11.
- **Execution scope:** local; quota setting needs W1 and approval.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G10 from docs/plans/warranty-returns.md. Read docs/architecture/warranty-returns.md.`

### G11 — Cloud Run, edge and data tier

- **Phase and estimate:** 1; hands-on 8–12, review 4–6, total 12–18; wait W1; owner Dev B.
- **Outcome, contracts, decisions:** The skeleton, then each merged goal, deploys to staging and production from one pipeline behind the load balancer with only the load balancer able to reach it. Proves C7, C8, C10; implements D1, D7.
- **Scope:** Infrastructure as code in the landing zone's convention, service accounts, Cloud SQL, Secret Manager, Artifact Registry, ALB with Cloud Armor, labels, billing export, backups. Staging with synthetic data only.
- **Depth:** Production. Staging scales to zero and is single-zone.
- **Resources created:** Each row's idle cost is a placeholder until G11/A1 reads the pricing page. Cloud Run with minimum instance 1 in production (idle rate; cleanup `gcloud run services delete`; verify `gcloud run services list`), Cloud SQL regional instance with backups and point-in-time recovery (per second running; `gcloud sql instances delete` then `gcloud sql backups delete`; verify both lists), external ALB forwarding rule, address, proxy and URL map (hourly; delete in dependency order; verify `forwarding-rules list` and `addresses list`), Artifact Registry repository (per GiB; `gcloud artifacts repositories delete`), Secret Manager versions (per active version). Lifetime owner: the cost contract C8 and the decommission item in Later; there is no teardown goal because production continues.
- **Prerequisites:** G02, W1; effective org policies read (`gcp.resourceLocations`, `sql.restrictPublicIp`, key-creation and member-domain constraints); the APIs each step enables named in its approval (`run`, `sqladmin`, `secretmanager`, `artifactregistry`, `compute`, `cloudbuild`, `monitoring`).
- **Primary skill:** `deploy-adk-on-google-cloud`. **Supporting:** `google/skills:cloud-run-basics` (service and ingress), `google/skills:cloud-sql-basics` (instance, backups), `google/skills:google-cloud-global-frontend-configuration` (ALB, Cloud Armor), `google/skills:iam-helper-for-policy-management` (bindings), `google/skills:gcloud` (commands), `google/skills:google-cloud-waf-reliability`, `-security` and `-cost-optimization` (pillar checks). All unconfirmed against the live catalogue. **Security rules:** SB05, SB25.
- **Acceptance:**
  - A1 BEFORE any resource is created, THE pricing pages SHALL be read and the idle cost, cleanup and verification rows above filled with dates (C8).
  - A2 STAGING and production SHALL deploy the same image digest from the pipeline; the default `run.app` URL SHALL be refused and ADK paths return nothing (SB05).
  - A3 THE serving identity SHALL have narrow grants, no key files, and the effective IAM readback SHALL match the design (C1).
  - A4 A Cloud Armor rate rule SHALL trigger in a test (SB25).
  - A5 EVERY resource SHALL carry `env`, `team` and `app` labels set in code, and the billing export SHALL be live (C8).
  - A6 THE effective org policies and the region and residency choice SHALL be recorded and reconciled with O5.
  - A7 A revision readback SHALL show the image digest and configuration equal to the release manifest, and a revision that cannot read its secrets SHALL fail readiness while the previous one keeps serving (C10).
  - A8 Cloud SQL SHALL use private connectivity, backups and point-in-time recovery, with RPO and RTO recorded per store (C9).
  - A9 STAGING SHALL contain no production data (C7).
- **Verification:** hosted readbacks; infrastructure plan reviewed before apply.
- **Execution scope:** NOT authorised. Needs a named project from W1, a named region and approval for each apply. Application Design Center plan assessment, if the organisation uses it, is cited as evidence.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G11 from docs/plans/warranty-returns.md. Read docs/architecture/warranty-returns.md. Propose each cloud command and wait for approval for the named project.`

### G12 — Observability and release gate

- **Phase and estimate:** 1; hands-on 7–10, review 3–4, total 10–14; handoff 1 from G06; owner Dev B.
- **Outcome, contracts, decisions:** Traces, SLIs and alerts on the contracts; a Cloud Build gate that fails on a bad evaluation; a manifest; a rehearsed rollback and canary procedure. Proves C2, C5, C7, C9, C10; implements D10.
- **Prerequisites:** G11, G06.
- **Primary skill:** `adk-agent-observability`. **Supporting:** `adk-release-engineering`; `google/skills:cloud-run-alert-configuration`, `google/skills:google-cloud-slo-alert-configuration`, `google/skills:cloud-build-basics` (unconfirmed). **Resources created:** alert policies and the evaluation job's model spend; Cloud Build charges per build minute only; owner: C8.
- **Acceptance:**
  - A1 AN in-memory exporter test SHALL show one span per agent, tool and logical model call with the conversation ID set (C9).
  - A2 CONTENT capture SHALL be off in the deployed environment, verified on a deployed trace (C7).
  - A3 SLIs SHALL be defined as good over total with owners, and alerts SHALL route to the named owner (C2, C5, C9).
  - A4 THE CI gate SHALL fail by exit code when the evaluation is below threshold, and the manifest SHALL contain no alias (C10).
  - A5 A rollback to the previous revision SHALL be rehearsed in staging with prompt, model, tool schema and secrets moving together (C10).
  - A6 AN alert SHALL fire for an `unknown` operation older than 15 minutes (C5).
  - A7 THE canary traffic-split procedure SHALL be run in staging (C10).
- **Execution scope:** NOT authorised for cloud; offline parts local.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G12 from docs/plans/warranty-returns.md. Read docs/architecture/warranty-returns.md.`

### G13 — Governance papers

- **Phase and estimate:** 1; hands-on 5–8, review 2–3, total 7–11; wait W4 for the sign-off; owner Dev A.
- **Outcome, contracts:** Draft privacy and legal papers for the privacy owner and counsel: jurisdiction screen, privacy impact (DPIA) input, records of processing, impact assessment and system card, each statement citing contract, decision and evidence IDs. Proves C7 (retention and erasure policy).
- **Prerequisites:** G03 (the data map). The signed-off retention period feeds G10 when it lands.
- **Primary skill:** `adk-governance-pack`.
- **Acceptance:**
  - A1 THE drafts SHALL exist under `docs/governance/warranty-returns/` and the skill's checker SHALL pass (C7).
  - A2 THE privacy input SHALL list every flow of personal data including the model region, logs and backups (C7).
  - A3 THE sign-off request SHALL be sent with the drafts, starting W4.
- **Execution scope:** documents only; sign-off is the privacy owner's.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G13 from docs/plans/warranty-returns.md.`

### G14 — Threat model and adversarial suite

- **Phase and estimate:** 1; hands-on 6–9, review 3–4, total 9–13; handoff 1 from G09; owner Dev A.
- **Outcome, contracts:** A recorded threat model and a scripted-model suite asserting forbidden actions never run. Proves C1, C3, C6; SB17, SB23 at Minimal.
- **Prerequisites:** G07, G09.
- **Primary skill:** `adk-agent-security`. **Security rules:** SB17, SB23.
- **Acceptance:**
  - A1 THE threat model SHALL record the per-agent check (private data, untrusted content, write) and its resolution, and list the OWASP LLM and agentic rows used (SB17, SB23).
  - A2 THE suite SHALL show that injected text in the product record, the customer message and a tool result never causes a filing, a cross-customer read or an off-list tool call (C1, C3, C6, SB23).
  - A3 THE system prompt and rendered request SHALL contain no secret or internal identifier (SB16).
- **Execution scope:** local.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G14 from docs/plans/warranty-returns.md.`

### G15 — Staging checks and drills

- **Phase and estimate:** 1; hands-on 6–9, review 3–4, total 9–13; handoff 1 from G14; owner Dev B.
- **Outcome, contracts:** The staging scans, the pen-test triage, a backup restore and the failure drills are done before any customer sees the service. Proves C8, C9; SB21, SB22, SB24.
- **Prerequisites:** G08, G10, G12, G14; W6 pen test report received.
- **Primary skill:** `adk-release-engineering`. **Supporting:** `adk-agent-observability`; `google/skills:google-cloud-waf-reliability` (unconfirmed). **Security rules:** SB21, SB22, SB24.
- **Acceptance:**
  - A1 THE ZAP baseline scan SHALL run on staging and each finding be fixed or accepted by an owner (SB21).
  - A2 THE ASVS Level 1 review SHALL be recorded with each gap as a goal or fix (SB22).
  - A3 THE pen-test findings SHALL be fixed or accepted by an owner (SB24).
  - A4 A Cloud SQL backup SHALL be restored into a non-production environment and RPO and RTO measured against the design (C9).
  - A5 DRILLS SHALL show an honest failure with no invented answer when the model is unavailable or its permission is revoked, and when the return system is down (C9).
  - A6 WHEN the app database is unavailable or its credential is revoked, NEW runs SHALL be refused and confirmed operations SHALL stay consistent (C9).
  - A7 A bounded burst test with a stated measurement boundary SHALL show admission refusing cleanly with no pool or quota exhaustion (C8).
- **Execution scope:** staging only, within declared request and cost limits.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G15 from docs/plans/warranty-returns.md.`

### G16 — Journey on staging

- **Phase and estimate:** 1; hands-on 4–6, review 2–3, total 6–9; owner Dev B.
- **Outcome, contracts:** The whole path on staging with synthetic customers: ask, answer, propose, confirm, reference, plus every earlier regression test. Proves C1 to C5, C9.
- **Primary skill:** `adk-agent-evaluation`; Playwright as companion.
- **Acceptance:**
  - A1 A synthetic customer SHALL ask about an owned product, receive a grounded answer, propose a return, confirm and see one reference in the sandbox (C1, C2, C3, C5).
  - A2 EVERY earlier goal's acceptance item that its ticket lists as a regression check SHALL pass.
  - A3 A second customer SHALL be unable to read, propose or confirm anything for the first (C1, C4).
  - A4 WITH the return system faulted, THE same journey SHALL end in `unknown` and a support entry, and the customer SHALL see no false confirmation (C5, C9).
- **Execution scope:** staging.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G16 from docs/plans/warranty-returns.md.`

### G17 — Operations handover

- **Phase and estimate:** 1; hands-on 3–5, review 1–2, total 4–7; owner Dev B.
- **Outcome, contracts:** A runbook the on-call owner can use. Proves C5 (the unknown-state procedure), C10 (rollback and retirement date).
- **Primary skill:** `adk-agent-observability` (operations handover reference). Blocked on O9 for names.
- **Acceptance:**
  - A1 THE runbook SHALL cover unknown returns and who closes them, the kill switch, rollback, model retirement date and the incident roles, each with a command or link (C5, C10).
  - A2 AN on-call owner and an escalation path SHALL be named before launch (C10).
  - A3 THE owner SHALL walk one drill from the runbook (C5).
- **Execution scope:** documents and a drill in staging.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G17 from docs/plans/warranty-returns.md.`

### G18 — Go-live review

- **Phase and estimate:** 1; hands-on 3–4, review 1–2, total 4–6; wait W4 first, W7 after; owner Dev B.
- **Outcome:** The sponsor decides on the canary launch with evidence, residual risks, the cost ceiling and the phase 2 ramp plan.
- **Primary skill:** `adk-presenter`. Business audience; the technical read for security and privacy reviewers is the design plus G13, G14, G15 evidence unless O11 says otherwise.
- **Acceptance:**
  - A1 THE outline SHALL pass the deck check and every claim SHALL cite an evidence record in this plan.
  - A2 THE memo SHALL state residual risks with owners, the cost ceiling and the ramp gates.
- **Run this goal:** `/adk-presenter Build the go-live review for docs/plans/warranty-returns.md (G18).`

### G19 — Canary launch

- **Phase and estimate:** 1; hands-on 2–3, review 1–2, total 3–5; owner Dev B.
- **Outcome, contracts:** Production serves a small share of customers with rollback ready. Proves C8, C10.
- **Primary skill:** `deploy-adk-on-google-cloud`. **Supporting:** `adk-release-engineering`.
- **Acceptance:**
  - A1 THE traffic split SHALL be set to the agreed small share with the previous revision ready (C10).
  - A2 THE SLIs SHALL be read after 24 hours and compared with the provisional targets (C8).
  - A3 THE rollback command SHALL be confirmed to work on the live service without sending traffic to it.
- **Execution scope:** NOT authorised: production changes need the W7 approval and a named target.
- **Run this goal:** `/adk-engineer Carry out G19 from docs/plans/warranty-returns.md.`

### Phase 2 goals

| ID | Goal | Primary skill | Estimate | One acceptance check |
| --- | --- | --- | --- | --- |
| G20 | ASVS Level 2 review and gaps (SB23) | `adk-agent-security` | 8–12 | Review recorded; each gap fixed or accepted by an owner |
| G21 | First live bill against C8, and the first cost review | `adk-operational-guardrails` | 3–5 | M1 records the bill against the estimate with the window and sample |
| G22 | Ramp to 100 percent by SLI gates | `adk-release-engineering` | 4–6 | Each step has a gate read from the SLIs; rollback tested at the top step |
| G23 | Support-team rollout pack | `adk-presenter` | 4–8 | Guide and training delivered; unknown-return handling rehearsed |
| G24 | Results review | `adk-presenter` | 4–6 | Every figure cites an M or I record |
| G25 | Portal embedding (O8), if chosen | `adk-frontend-integration` | 10–16 | Embedded journey passes G16's checks |

## Later

| Item | Trigger | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| Recurring cost and model-mix review | A date each month, the first bill, a volume step | Spend above the smallest model that would pass | `adk-model-and-output-contracts` |
| Committed-use review | Three stable months | Paying list price | `optimise-adk-on-google-cloud` |
| Latency and capacity tuning | Measured p95 above target | Slower answers | `optimise-adk-on-google-cloud` |
| BigQuery agent analytics, production-to-evaluation sampling | First incident or a quality drift | Slower quality learning | `adk-agent-observability` |
| Refunds or other remedies | A policy decision | None; out of scope | `safe-api-tool-calls` |
| Cross-session memory | A requirement | None | `adk-memory-architecture` |
| Decommission | Application retires | Idle spend if forgotten | `deploy-adk-on-google-cloud` (ledger cleanups, dependants and retention) |
| Model retirement re-baseline | Retirement date in the manifest | Forced migration | `adk-release-engineering` |

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| docs/architecture/warranty-returns.md | Method, contracts and accepted decisions |
| docs/discovery/interfaces.md (after G03) | What the databases and return system actually do |
| This plan | Remaining limits, deferred controls, evidence by contract |

## Open decisions for further planning

See the design's open decisions O1 to O11. Those that block build goals: O1, O2, O3 (G03 settles them), O6 (G07), O4 and O5 (G10, G11). O10 changes every figure in this plan.

## Resume here

- **Next goal:** G02, which is ready and independent. First, today: send the access requests W1, W2, W3, the SME session request W5 and the pen-test booking W6.
- **Read first:** the design and this plan.
- **Continuation prompt:**

```text
/adk-engineer Carry out G02 from docs/plans/warranty-returns.md.
Read docs/architecture/warranty-returns.md and preserve its accepted decisions.
Use adk-workflow-design with adk-model-and-output-contracts.
Work locally only, verify A1 to A4, and update the plan with actual evidence.
```
