# Implementation plan: claims triage assistant, production version

Status: **draft, unreviewed**; schedule **not machine-checked** (no shell in this session; figures below are hand-computed)
Architecture: [docs/architecture/claims-production.md](../architecture/claims-production.md)
Continuation source of truth: this plan. The PoC plan [claims.md](claims.md) is the record of phase 1 of the proof of concept; goal IDs below are this plan's own.

## Summary for the reader

- **Profile and phase 1:** production, two developers, eight weeks. Phase 1 builds the production service and puts it live for the four PoC handlers under a $300 staged ceiling, then reads the first live bill against the $1,500 contract. Full rollout to 14 handlers, handover to Fenwick IT and the results review are phase 2.
- **How the ceiling is enforced (the sponsor's open point):** the Cloud Billing export and budget alerts are delayed and only notify, so they cannot stop spend. The stop is an admission ledger in the application that reserves worst-case cost before any model call and refuses work at the cap (C9, G03), with Vertex AI and BigQuery quotas and Cloud Run max instances as backstops, an operator stop, and the billing budget and export used to tighten and to prove (G14, G15).
- **Effort and finish (hand-computed):** 122–174 human hours of goals plus 8–16 hours of handoffs, against 216 hours usable (2 × 108 after a 25 % reserve of 288). Dev A 65–98 h, Dev B 65–93 h. Limited go-live about working day 25–36 of 40. The cost reading (G15) lands about day 35–45: **fits at the low end and the middle; at the high end it runs about five days into week 9.** The build and go-live still fit; only the bill reading slips, and with it the 14-handler rollout.
- **Largest risks:** (1) per-request cost feasibility is unproven: the PoC's observed spend is about 16 times the $0.05 average the ceiling allows if a claim was one request (G01, owner Dev A, then the sponsor); (2) DPIA sign-off and DPO agreement on the infoType list (W6, W3) must be requested on day 1; (3) Dev A's serial chain G03 → G04 → G06 → G10 → G12 is the long pole.
- **Decisions needed from you:** sponsor: meaning of "request" and whether staging spend is inside the $1,500 (OD2, OD3); Helen Okafor: follow-ups refused first at 85 % (OD10); Fenwick security: accept the deferral of SB23–SB25 (OD7).
- **Next prompt:** `/adk-engineer Carry out G00 from docs/plans/claims-production.md.`

## Destination and constraints

Handlers get a screened, cited triage draft on new home claims in production, and spend cannot exceed $1,500 a month without a person overriding a stop. Non-goals: motor claims, any write to claims or policy systems, external users. Stack, pins and decisions are in the design (D2, D5–D13); ADK 2.12.0 and the pinned model IDs are inherited, and changing either is a release (G08). Inspected repository: none in this workspace; every module path is proposed. No cloud access has been used or is granted by this plan: each goal's execution scope says what it needs.

**Skills.** Installed here: adk-engineer, adk-system-designer, deploy-adk-on-google-cloud, adk-operational-guardrails, adk-agent-observability, adk-sql-agent-engineering. Named below but not installed in this workspace: protect-adk-sensitive-data, adk-fastapi-backend, adk-tool-auth-and-secrets, adk-agent-evaluation, adk-agent-security, adk-release-engineering, adk-governance-pack, adk-presenter, adk-model-and-output-contracts; `adk-engineer` explains how to get them. Google product skills (`google/skills:cloud-sql-basics`, `bigquery-basics`, `cloud-run-basics`, `google-cloud-waf-cost-optimization`) are named as supporting skills where a goal provisions the product.

## Delivery profile and capacity

Profile: production (design, "Profile, constraints and depth").

| Phase | Delivers | Goals | Human hours, agent-assisted | Capacity |
| --- | --- | --- | --- | --- |
| 1, ship | production service live for four handlers; cost contract read on a live bill | G00–G15 | 122–174, plus 8–16 handoff | 2 × 3.6 h × 40 days = 288 h; reserve 25 % → 216 h |
| 2, graduate | rollout to 14 handlers, handover, results review | G16–G19 | 14–27, not scheduled | after G15 |

Estimates are assumptions for a team that built the PoC (no learning multiplier). Dev A is Tom Reid and Dev B is Sara Lin, as in the PoC.

| Person | Goals | Hours incl. handoff | Capacity |
| --- | --- | --- | --- |
| Dev A | G00, G01, G03, G04, G06, G10, G11, G12, G13, G15 | 65–98 | 108 h |
| Dev B | G02, G05, G07, G08, G09, G14 | 65–93 | 108 h |

```yaml
- goal: G00
  phase: 1
  hands_on: 0.5-1
  review: 0
  total: 0.5-1
  owner: Dev A
  blocked_by: []
  calendar_waits: none
  wait_days: 0
  handoff: 0
  contracts: []
  security: []
  mentions_only: [W1, W2, W3, W4, W5, W9]
  type: implementation
  status: planned
- goal: W1
  phase: 1
  total: 0
  blocked_by: [G00]
  calendar_waits: production project, billing link and org-policy exceptions from the Fenwick administrator
  wait_days: 5-10
- goal: W2
  phase: 1
  total: 0
  blocked_by: [G00]
  calendar_waits: read access to the billing export dataset
  wait_days: 3-5
- goal: W3
  phase: 1
  total: 0
  blocked_by: [G00]
  calendar_waits: Fenwick DPO agrees the infoType list, transform and acceptable miss rate
  wait_days: 3-8
- goal: W4
  phase: 1
  total: 0
  blocked_by: [G00]
  calendar_waits: Raj Mehta confirms the claim-history source, loader and freshness
  wait_days: 5-10
- goal: W5
  phase: 1
  total: 0
  blocked_by: [G00]
  calendar_waits: two team leads label the gold set (session booked)
  wait_days: 5-8
- goal: W6
  phase: 1
  total: 0
  blocked_by: [G07]
  calendar_waits: DPIA sign-off, requested when the G07 drafts go out
  wait_days: 10-15
- goal: W7
  phase: 1
  total: 0
  blocked_by: [G12]
  calendar_waits: Helen Okafor's go-live decision (slot booked in advance)
  wait_days: 3
- goal: W8
  phase: 1
  total: 0
  blocked_by: [G13]
  calendar_waits: five live working days plus billing export lag
  wait_days: 8
- goal: W9
  phase: 1
  total: 0
  blocked_by: [G05]
  calendar_waits: Fenwick IT and security review of design and staging evidence, including OD7
  wait_days: 8-10
- goal: G01
  phase: 1
  hands_on: 3-4
  review: 1-2
  total: 4-6
  owner: Dev A
  blocked_by: [G00]
  calendar_waits: none
  wait_days: 0
  handoff: 0
  contracts: [C9]
  security: []
  mentions_only: []
  type: discovery
  status: planned
- goal: G02
  phase: 1
  hands_on: 8-11
  review: 3-4
  total: 11-15
  owner: Dev B
  blocked_by: [G00]
  calendar_waits: none
  wait_days: 0
  handoff: 0
  contracts: [C9]
  security: [SB16]
  mentions_only: []
  type: implementation
  status: planned
- goal: G03
  phase: 1
  hands_on: 9-12
  review: 4-6
  total: 13-18
  owner: Dev A
  blocked_by: [G01]
  calendar_waits: none
  wait_days: 0
  handoff: 0
  contracts: [C8, C9]
  security: [SB19]
  mentions_only: []
  type: implementation
  status: planned
- goal: G04
  phase: 1
  hands_on: 8-10
  review: 3-5
  total: 11-15
  owner: Dev A
  blocked_by: [G03, W3]
  calendar_waits: W3 DPO agreement on the infoType list
  wait_days: 3-8
  handoff: 0
  contracts: [C4, C6]
  security: [SB14]
  mentions_only: []
  type: implementation
  status: planned
- goal: G05
  phase: 1
  hands_on: 9-13
  review: 4-6
  total: 13-19
  owner: Dev B
  blocked_by: [G02]
  calendar_waits: none
  wait_days: 0
  handoff: 0
  contracts: [C1, C7, C11]
  security: [SB01, SB02, SB03, SB04, SB05, SB06, SB07, SB08, SB09, SB10, SB13, SB19, SB20]
  mentions_only: []
  type: implementation
  status: planned
- goal: G06
  phase: 1
  hands_on: 5-7
  review: 2-3
  total: 7-10
  owner: Dev A
  blocked_by: [G02, G04, W4]
  calendar_waits: W4 claim-history source and loader
  wait_days: 5-10
  handoff: 1-2
  contracts: [C1, C3, C8]
  security: [SB04]
  mentions_only: []
  type: implementation
  status: planned
- goal: G07
  phase: 1
  hands_on: 6-8
  review: 2-3
  total: 8-11
  owner: Dev B
  blocked_by: [G00]
  calendar_waits: none
  wait_days: 0
  handoff: 0
  contracts: []
  security: []
  mentions_only: [W3, W6]
  type: governance
  status: planned
- goal: G08
  phase: 1
  hands_on: 9-12
  review: 4-6
  total: 13-18
  owner: Dev B
  blocked_by: [G05, G03, G04, W1]
  calendar_waits: W1 production project
  wait_days: 5-10
  handoff: 1-2
  contracts: [C9, C10]
  security: [SB15, SB16, SB21]
  mentions_only: [G10]
  type: implementation
  status: planned
- goal: G09
  phase: 1
  hands_on: 6-9
  review: 2-3
  total: 8-12
  owner: Dev B
  blocked_by: [G08, G03]
  calendar_waits: none
  wait_days: 0
  handoff: 1-2
  contracts: []
  security: [SB14]
  mentions_only: []
  type: implementation
  status: planned
- goal: G10
  phase: 1
  hands_on: 7-10
  review: 3-5
  total: 10-15
  owner: Dev A
  blocked_by: [G04, G05, G06, W5]
  calendar_waits: W5 team-lead labelling session
  wait_days: 5-8
  handoff: 1-2
  contracts: [C2, C3]
  security: [SB17, SB22]
  mentions_only: []
  type: implementation
  status: planned
- goal: G11
  phase: 1
  hands_on: 2-3
  review: 1
  total: 3-4
  owner: Dev A
  blocked_by: [G03, G04, G05, G06, G10]
  calendar_waits: none
  wait_days: 0
  handoff: 0.5-1
  contracts: [C1, C7]
  security: []
  mentions_only: []
  type: journey
  status: planned
- goal: G12
  phase: 1
  hands_on: 2-4
  review: 1-2
  total: 3-6
  owner: Dev A
  blocked_by: [G11, G07]
  calendar_waits: none
  wait_days: 0
  handoff: 1-2
  contracts: []
  security: []
  mentions_only: [G14, G15]
  type: presentation
  status: planned
- goal: G13
  phase: 1
  hands_on: 3-4
  review: 1-2
  total: 4-6
  owner: Dev A
  blocked_by: [G08, G09, G12, W6, W7, W9]
  calendar_waits: W6 DPIA sign-off; W7 decision; W9 security review
  wait_days: 3-15
  handoff: 1-2
  contracts: [C9]
  security: []
  mentions_only: []
  type: implementation
  status: planned
- goal: G14
  phase: 1
  hands_on: 6-8
  review: 3-4
  total: 9-12
  owner: Dev B
  blocked_by: [G02, G03, G09, W2]
  calendar_waits: W2 billing export access
  wait_days: 3-5
  handoff: 1-2
  contracts: [C9]
  security: []
  mentions_only: []
  type: implementation
  status: planned
- goal: G15
  phase: 1
  hands_on: 3-4
  review: 1-2
  total: 4-6
  owner: Dev A
  blocked_by: [G13, G14, W8]
  calendar_waits: W8 five live days plus export lag
  wait_days: 8
  handoff: 1-2
  contracts: [C9]
  security: []
  mentions_only: []
  type: implementation
  status: planned
```

**Finish range (hand-computed from the block above at 2.7 focused hours a day per person, which is 3.6 less the 25 % reserve): about working day 35 (low) to 45 (high) for G15, limited go-live (G13) about day 25 to 36, against 40 days available.** The high end is driven by Dev A's serial chain and W7 and W8, not by total load (A 98 h of 108). Waits W1–W5 and W9 are requested by G00 on day 1; W6 is requested the day the G07 drafts go out (G07 is Dev B's first goal so it lands about day 4). Not run: `python3 .claude/skills/adk-system-designer/scripts/check_schedule.py --plan docs/plans/claims-production.md --design docs/architecture/claims-production.md --days 40 --reserve 0.25 --person "Dev A=3.6" --person "Dev B=3.6"`. Run it before trusting these figures; expect it to list mentions and handoffs for review, and the wait entries may need its exact field names. Remedies for the high-end slip were **not** tested with the helper and are not offered.

If time runs out early, the order of usefulness is: G01, G03 (spend stop), G04 (screening), G05 (identity and scope), then the rest.

## Implementation map

| Contract / decision | Component and integration point (all proposed) | GCP responsibility | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |
| C8, C9, D7 | `app/admission.py` (reserve, settle, tiers, caps), `control` and `usage_ledger` tables, price table, `RunConfig` | Cloud SQL, Vertex AI quota | adk-operational-guardrails | 20,000-request simulation on real Postgres, local |
| C9 second line, D7 | `ratchet/` private Cloud Run service; scheduled reconciliation query | Billing budget, Pub/Sub, BigQuery billing export, Scheduler | adk-operational-guardrails | synthetic envelope live in staging |
| C4, C6, D8 | `app/deidentify.py`, `after_model_callback`, `after_tool_callback`, release gate | Sensitive Data Protection | protect-adk-sensitive-data | callbacks on ADK 2.12.0 (U1) |
| C1, C7, C11, SB01–SB10, SB13, SB20 | FastAPI dependency, routes, decisions table | IAP, Cloud Run | adk-fastapi-backend | forged-header and audience tests |
| C1, C3, C8, D10 | `claim_history` template tool | BigQuery | adk-sql-agent-engineering | bytes-billed ceiling on the largest claimant |
| C2, C3, SB17, SB22 | validator, evaluation set, CI gate, adversarial suite | none | adk-agent-evaluation | gold set with provenance |
| C9, C10, SB15, SB16, SB21, D13 | IaC, release bundle, canary, restore test | Cloud Run, Cloud SQL, Artifact Registry | deploy-adk-on-google-cloud | rollback and restore timing in staging |
| SB14, D12 | OTel traces, content-free logs, SLIs, alerts | Cloud Trace, Logging, Monitoring | adk-agent-observability | exporter test |

## Goals and dependencies

Estimates, owners, dependencies and waits are in the schedule block only. Run prompt for every goal: `/adk-engineer Carry out <ID> from docs/plans/claims-production.md. Read docs/architecture/claims-production.md, use the goal's skills, verify its acceptance cases locally and record evidence under the goal.`

| ID and goal | Type | Depends on | Primary skill | State |
| --- | --- | --- | --- | --- |
| G00 Day-one requests for every wait | implementation | none | adk-engineer | ready |
| G01 Cost feasibility and per-request budget | discovery | G00 | adk-operational-guardrails | ready |
| G02 Staging foundation as code | implementation | G00 | deploy-adk-on-google-cloud | ready |
| G03 Cost admission control | implementation | G01 | adk-operational-guardrails | blocked on G01 |
| G04 Sensitive Data Protection on every reply | implementation | G03, W3 | protect-adk-sensitive-data | blocked |
| G05 Production service, identity and security baseline | implementation | G02 | adk-fastapi-backend | blocked on G02 |
| G06 Production claim history | implementation | G02, G04, W4 | adk-sql-agent-engineering | blocked |
| G07 Governance papers and DPIA inputs | governance | G00 | adk-governance-pack | ready after G00 |
| G08 Production environment, release and recovery | implementation | G05, G03, G04, W1 | deploy-adk-on-google-cloud | blocked |
| G09 Observability, SLOs and alerts | implementation | G08, G03 | adk-agent-observability | blocked |
| G10 Evaluation, CI gate, threat model, adversarial suite | implementation | G04, G05, G06, W5 | adk-agent-evaluation | blocked |
| G11 Journey check in staging | journey | G03–G06, G10 | adk-agent-evaluation | blocked |
| G12 Go-live approval presentation (business) | presentation | G11, G07 | adk-presenter | blocked |
| G13 Limited go-live for the four PoC handlers | implementation | G08, G09, G12, W6, W7, W9 | deploy-adk-on-google-cloud | blocked |
| G14 Budget ratchet and export reconciliation | implementation | G02, G03, G09, W2 | adk-operational-guardrails | blocked |
| G15 First-live-week bill reading and cost gate | implementation | G13, G14, W8 | adk-agent-observability | blocked |

Every goal below keeps the floor: no secrets in code, prompts or logs; pinned model IDs; a spend stop; nothing irreversible without a person; real personal data only as scoped here and out of logs. "Execution scope: local" means no cloud call; "staging" means the retained PoC project `fm-claims-pilot` only.

### G00 — Day-one requests for every wait
- **Outcome:** W1–W5 and W9 are requested with named owners, a date asked for and what is needed (W1 production project, billing link, org-policy exceptions per the design; W2 read on the billing export dataset; W3 DPO infoType list; W4 Raj Mehta on claim-history loader; W5 labelling session booked with the two team leads; W9 review of design and staging evidence); W7 decision slot booked with Helen Okafor; Q6 answered.
- **Acceptance:** A1 each request is recorded with owner, date asked and the date it blocks (names the goals that depend on it). A2 Q6 (change request) is answered or recorded as blocking G02.
- **Execution scope:** emails and calendar only.

### G01 — Cost feasibility and per-request budget (discovery, C9)
- **Question and bounded investigation:** can a request cost $0.05 on average and $0.15 at p95? Read the PoC's billing report by SKU, measure tokens and calls over about 20 recorded PoC requests with a model double, stop after six hours.
- **Skills:** adk-operational-guardrails; supporting adk-agent-observability (price table, token accounting), `google/skills:google-cloud-waf-cost-optimization`.
- **Acceptance:** A1 M2 (£38.20, 62 claims) is split by SKU and the unit is stated with measured requests per claim (C9). A2 expected and p95 cost per request, with tokens, calls and the pricing date, sit beside $0.05 and $0.15, and the fixed split F ≤ $300 is checked against pricing pages (C9). A3 the decision is recorded: proceed, apply named levers, or take a lower volume or higher ceiling to the sponsor; N, T, S, B for C8 and the daily and per-handler caps are fixed. A4 the retirement dates of both pinned model IDs are recorded from the dated lifecycle table, or marked unchecked.
- **Decision it unblocks:** G03 parameters. G03 can start on the structure if the sponsor's answer is pending.
- **Execution scope:** read-only console billing report for `fm-claims-pilot`; offline measurement. No paid model calls.

### G02 — Staging foundation as code (C9, SB16)
- **Outcome:** infrastructure as code for network, service accounts, roles, labels, quotas, Artifact Registry, Pub/Sub and Cloud SQL roles and schemas, applied to staging; production is the same code with sized parameters.
- **Skills:** deploy-adk-on-google-cloud; `google/skills:cloud-sql-basics`.
- **Resources created:** none new in staging (reuses `fm-claims-pilot-sql`; design resource table). Production resources come in G08.
- **Acceptance:** A1 the plan output shows every resource with `env`, `team`, `app` labels (C9). A2 the runtime service account holds only the roles the design lists and a call to a billing or IAM-changing API is denied (SB16). A3 effective values of `iam.disableServiceAccountKeyCreation`, `sql.restrictPublicIp`, `gcp.resourceLocations`, `gcp.restrictServiceUsage` are read and recorded. A4 the first-use pricing pages are read and every placeholder idle cost in the design is filled with a date. A5 the Vertex AI quota override, BigQuery daily custom quota and Cloud Run `max-instances` are in configuration.
- **Execution scope:** staging project, `plan` and approved `apply`; no production.

### G03 — Cost admission control (C8, C9, SB19)
- **Outcome:** every request is admitted, reserved and settled against the ledger as the design's cost-contract table describes (layers 1–3).
- **Skills:** adk-operational-guardrails; supporting adk-agent-observability.
- **Acceptance:** A1 20,000 simulated requests across 5 concurrent workers never push the ledger past the cap, and requests after it are refused (C9). A2 with one reservation left, two concurrent requests admit exactly one (C9). A3 a process killed between reserve and settle keeps the reservation until expiry, then settles at the reserved value (C9). A4 with the operator stop set, the model double receives zero calls; clearing it restores only that latch (C9). A5 an unreadable control store denies, never allows (C8, C9). A6 a request over `max_llm_calls`, tokens or time, or a model error, refusal or 429, ends with the fixed message and the ledger settles actual usage (C8). A7 the 201st request from one handler in a day is refused while others are unaffected; the daily dollar and monthly request caps refuse likewise (C9, SB19). A8 month rollover resets the automatic tier and keeps the operator stop and unsettled reservations (C9). A9 ADK 2.12.0 `usage_metadata` and `max_llm_calls` behave as assumed (U1).
- **Verification:** offline, real local Postgres, model double with fixed usage. Live proof is G08/A7.
- **Execution scope:** local only.

### G04 — Sensitive Data Protection on every reply (C4, C6, SB14)
- **Outcome:** notes, tool results and every model reply are screened; the session stores only screened text; nothing is released without the marker.
- **Skills:** protect-adk-sensitive-data; supporting adk-model-and-output-contracts.
- **Acceptance:** A1 the reply stored in the session and returned to the browser is the screened text (C6). A2 SDP unavailable, slow, erroring or returning an unexpected payload leaves no raw text in any reply, event or log line; the handler sees the fixed message and the ledger settles (C6, C4). A3 canary names, phones, emails, national insurance numbers and postcodes in notes, a policy API fixture, a BigQuery fixture and a model double that echoes them appear in no model request, session row, log line or response (C4, C6, SB14). A4 clause citations such as "3.2" and claim references survive the transform (C2 regression). A5 the miss rate on a labelled set of free-text notes is measured and reported to the DPO against the threshold from W3 (C4). A6 an event without the marker is withheld by the release gate (C6). A7 no partial text reaches the browser: the Runner runs non-streaming (C6). A8 an SDP 429 is treated as unavailable and fails closed (C6). A9 the callbacks run, and replace the persisted response, as assumed on ADK 2.12.0; if not, the session-service wrapper is built instead (U1).
- **Execution scope:** local with recorded SDP responses; a bounded live SDP call on staging with synthetic text for A8 and latency, no real claims.

### G05 — Production service, identity and security baseline (C1, C7, C11)
- **Outcome:** the FastAPI service behind IAP with the decisions table, per-handler sessions and the web security rules in the design.
- **Skills:** adk-fastapi-backend; supporting adk-tool-auth-and-secrets, deploy-adk-on-google-cloud. Companion skills are written into AGENTS.md by this goal from the designer's web defaults.
- **Acceptance:** A1 with the verifier unset every `/api` route returns 401 (SB01). A2 expired, wrong-audience and forged-header requests are rejected (SB02). A3 another handler's session ID gets the same 404 as an unknown one, with no model call (C7, SB03). A4 another team's claim returns 404, including at the tool hop (C1, SB04). A5 ADK's own routes return no ADK data at the staging URL (SB05). A6 no docs or schema served, headers and Origin check on state-changing requests, no wildcard CORS, bounded bodies, generic error body with a request ID, model output rendered inert (SB06–SB10, SB13). A7 a double submit records one decision, a retry after a lost response returns the first, and a decision against a superseded draft is refused (C11). A8 the retention job deletes sessions older than the retention period (OD5). A9 a revoked token is refused on a decision write, and a verifier outage denies (SB20, SB13). A10 a second concurrent run for one handler and conversation is refused with no model call (C7, SB19).
- **Execution scope:** local, then staging deploy with a captured token.

### G06 — Production claim history (C1, C3, C8, SB04)
- **Outcome:** `claim_history` as a reviewed parameterised template over the partitioned and clustered table, read-only, with a bytes ceiling.
- **Skills:** adk-sql-agent-engineering; `google/skills:bigquery-basics`.
- **Acceptance:** A1 the query is a fixed template and a model argument naming another claimant returns nothing; identifiers come from trusted state (C1, SB04). A2 the largest claimant bills at most B bytes and a query over the ceiling errors instead of returning part (C8). A3 BigQuery unavailable or slow gives a draft labelled "history unavailable", never an empty history. A4 the service account can read one dataset and create jobs, and a write is denied (C3). A5 an instruction planted in a history field is treated as data and screened. A6 quota exceeded behaves as A3.
- **Execution scope:** staging dataset with synthetic rows; production loader is Raj Mehta's (W4).

### G07 — Governance papers and DPIA inputs
- **Outcome:** the drafts Fenwick's DPO and security reviewers sign, from this design (personal data, decisions that affect access to a service): processing record, impact-assessment inputs, system card, jurisdiction screen (UK first), questionnaire answers; retention (OD5) and infoType decisions (OD4) recorded.
- **Skills:** adk-governance-pack. Acceptance: A1 the skill's checker passes on the drafts. A2 the drafts go to the DPO and W6 starts the same day, recorded.
- **Execution scope:** documents only. G07 starts early so the sign-off wait runs while the build proceeds; its figures (miss rate, retention) are refreshed in G12.

### G08 — Production environment, release and recovery (C9, C10, SB15, SB16, SB21)
- **Outcome:** production applied from the same code, pinned release bundle, canary and rollback, restore and failover rehearsed, staging overrun test, ZAP baseline.
- **Skills:** deploy-adk-on-google-cloud; supporting adk-release-engineering, `google/skills:cloud-sql-basics`, `google/skills:cloud-run-basics`.
- **Resources created:** every row of the design's resource table for `fm-claims-prod`, with idle costs filled.
- **Acceptance:** A1 production differs from staging only in sized parameters (plan diff). A2 the release bundle (image digest, prompt version, model and judge IDs, tool schema hash, price table version, infoType template version, secret versions) has no alias. A3 a canary revision takes traffic only when tagged. A4 rollback restores the previous image, prompt and price table together, timed. A5 a zonal Cloud SQL failover keeps sessions and the app reconnects (C10). A6 a point-in-time restore into non-production recovers a decision written five minutes earlier; RTO is measured against 60 min (C10). A7 in staging, with the cap set to $2, requests are refused after the cap and the Vertex AI request count stays flat afterwards; the PoC's missing live overrun test (C9). A8 a ZAP baseline on staging is recorded with each finding fixed or accepted (SB21). A9 `make check` runs dependency audits and the secret scan (SB15, SB16). A10 each resource's idle cost and cleanup command are recorded.
- **Execution scope:** staging live tests with a $2 cap; production `apply` only after W1 and explicit approval. Bounded spend: the staging allowance.

### G09 — Observability, SLOs and alerts (SB14, D12)
- **Skills:** adk-agent-observability.
- **Acceptance:** A1 an in-memory exporter test shows one span per agent, tool and logical model call with the session ID. A2 a canary in a prompt or reply never appears in logs. A3 alerts for tier changes T1–T3, ledger-versus-export drift, SDP withhold rate and SLO burn reach the named channel in staging with synthetic input. A4 a dashboard shows cost per request p50 and p95 from the ledger. A5 denied-access and sign-in failure lines are logged with principal, route and request ID. A6 each SLI has a target from the staging baseline, not 100 %.
- **Execution scope:** staging live; production after G08.

### G10 — Evaluation, CI gate, threat model, adversarial suite (C2, C3, SB17, SB22)
- **Outcome:** a gold set of at least 40 labelled new home claims, with provenance, a versioned criteria file and an agreement report; a gate that fails by exit code.
- **Skills:** adk-agent-evaluation (expert-review reference); supporting adk-agent-security.
- **Acceptance:** A1 the gold set has provenance and an agreement report between the two team leads (C2). A2 a deliberately regressed prompt fails the gate with a non-zero exit code and blocks promotion. A3 an instruction injected into a claim note causes no forbidden call, and no write tool is bound (C3, SB17). A4 an ASVS Level 1 review is recorded, gaps becoming goals (SB22). A5 a threat model names each component and its exposure. A6 an uncited or schema-invalid reply is rejected by the validator (C2). A7 a policy API that is down, slow, 401 or 429 withholds the draft as "cover not checked" (C2).
- **Execution scope:** local; the judge model runs under the staging allowance (D11).

### G11 — Journey check in staging (C1, C7)
- **Acceptance:** A1 a browser run (Playwright) opens a new escape-of-water claim, shows the draft with cited cover, accepts it, and a handler from another team cannot open it. A2 the request settles in the ledger. A3 every `pass_to_pass` test from G03–G06 and G10 passes.

### G12 — Go-live approval presentation, business audience
- **Outcome:** outline for Helen Okafor on what the four handlers get, how spend is stopped, what is unproven, the staged ceiling and the deferred controls. A1 the outline passes the presenter's deck check and every claim cites evidence recorded in this plan. A2 the cost slide shows the C9 formula with measured inputs from G01, not an assumed bill. The decision date is W7.

### G13 — Limited go-live for the four PoC handlers (C9)
- **Acceptance:** A1 the four handlers are served from production and others get 404 on the queue (C1). A2 the staged $300 cap on A is set in production and refuses at the cap. A3 an operator stop drill: drafts refused, queue reads and decision recording still work, within one minute, and clearing restores service. A4 a synthetic claim passes smoke checks. A5 the previous release is one command away.
- **Execution scope:** production deploy after W6, W7, W9 and approval.
- **Accepted risk while G14 is open:** the first live week runs with layers 1–4 and a budget alert (email only); the ratchet and reconciliation follow within that week.

### G14 — Budget ratchet and export reconciliation (C9)
- **Skills:** adk-operational-guardrails; supporting adk-agent-observability, `google/skills:bigquery-basics`.
- **Acceptance:** A1 a synthetic budget message at 85 % raises the tier to T2 with a version, and the next admission is degraded. A2 malformed, unauthenticated, stale, wrong-budget, wrong-currency, older-period and duplicate messages cannot loosen a tier; a lower reported spend does not lower the tier in the same month. A3 a fixture export with a 20 % gap makes reconciliation raise one tier and alert. A4 a missing, late or access-denied export raises a "no data" alert and never reads as zero spend. A5 a real synthetic message through the live Pub/Sub path on a small staging budget changes the control row and blocks a later request.
- **Execution scope:** staging live (small budget, Pub/Sub); production after G13. Not relied on: Cloud Billing spend-cap budgets (OD8).

### G15 — First-live-week bill reading and cost gate (C9)
- **Outcome:** the contract read against a real bill.
- **Skills:** adk-agent-observability. Records `M1` cost per request (value, baseline $0.05, window, sample, method, owner Tom Reid, build) and `M2` fixed cost.
- **Acceptance:** A1 the week's export spend, sliced by project and labels, is within 15 % of the ledger, or the gap is explained (C9). A2 actual cost per request and fixed cost are compared with G01's estimate and F ≤ $300. A3 the sponsor's decision to hold or raise the staged ceiling is recorded. A4 the label slice equals the project total.
- **Execution scope:** read-only billing export.

## Phase 2: graduate (after G15; written coarse because phase 1 will change it)

| ID | Goal | Primary skill | Estimate | Acceptance check |
| --- | --- | --- | --- | --- |
| G16 | Rollout pack and training for 14 handlers | adk-presenter | 4–8 h, plus sessions held | every handler trained before access, attendance recorded |
| G17 | Operations handover to Fenwick IT: runbooks (operator stop, tier changes, restore), alert routes, postmortem template, access transfer | adk-agent-observability | 4–8 h, plus access-transfer wait | Fenwick IT executes the operator-stop and restore runbooks unaided |
| G18 | Full rollout; raise the ceiling in config under change control | deploy-adk-on-google-cloud | 3–5 h | 14 handlers served, cap raised only after G15/A3 |
| G19 | Results review after four live weeks (business) | adk-presenter | 3–6 h, plus decision date | median triage ≤ 15 min and re-routing ≤ 9 % shown from measurement records |

## Later

| Item | Trigger | Risk accepted while it waits | Likely skill |
| --- | --- | --- | --- |
| Recurring cost review of the bill against C9 | first monthly bill, then monthly | spend drifts unnoticed | adk-agent-observability |
| Model mix and committed-use review | first monthly bill, then quarterly | higher cost than needed | adk-model-and-output-contracts |
| Model retirement migration | retirement date recorded in G01/A4 | forced swap | adk-release-engineering |
| SB23 ASVS L2 and programme, SB24 pen test, SB25 Cloud Armor | external users, a public endpoint, or W9 requires | internal users behind SSO, no write tools | adk-agent-security |
| Regional failover and game day | availability target above 99.5 % or a region incident | rebuild from code plus restore | adk-release-engineering |
| Cold-start tuning (min instances 1) | p95 cold start above 10 s | slower first draft | optimise-adk-on-google-cloud |
| Motor claims | home pilot meets its threshold | none | adk-system-designer |
| Decommission: delete production and staging resources in the design's resource table, dependants and backups included | service retires | idle Cloud SQL charges continue if forgotten | deploy-adk-on-google-cloud |

## Changes against the PoC plan

| Item | Change | Reason |
| --- | --- | --- |
| PoC Later: recurring cost review, decommission, production hardening | moved into G08, G14, G15 and the Later table | nothing dropped |
| PoC C5 | replaced by C8, C9 | see design |
| Nothing removed or weakened | | |

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| docs/architecture/claims-production.md | contracts, cost enforcement and accepted decisions |
| this plan | schedule, cut line, deferred controls and evidence |

## Open decisions

See the design's table (OD1–OD10, U1, U2). Blocking now: OD1 (G01 answers it), OD2 and OD3 (sponsor, before G03 parameters), OD4 (W3, before G04), OD9 (W4, before G06), OD7 (W9, before G13).

## Independent review

Not done: no subagent was available. Before handing this to the team, run the independent plan review in a fresh session with the prompt in `.claude/skills/adk-system-designer/assets/plan-review-prompt.md`, settle each finding here, then run the schedule check above.

## Resume here

- **Next goal:** G00, then G01 and G02 and G07 in parallel (no prerequisites after G00).
- **Read first:** the design, then this plan's goal entry.

```text
/adk-engineer Carry out G00 from docs/plans/claims-production.md.
Read docs/architecture/claims-production.md and preserve its accepted decisions.
Send the wait requests W1–W5 and W9 and book W7; record owners and dates.
```
