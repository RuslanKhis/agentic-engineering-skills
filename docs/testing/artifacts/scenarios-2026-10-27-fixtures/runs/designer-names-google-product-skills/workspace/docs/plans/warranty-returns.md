# Implementation plan: warranty answers and return requests

Status: **draft, unreviewed, schedule not machine-checked** (see Summary)
Architecture: [docs/architecture/warranty-returns.md](../architecture/warranty-returns.md)
Continuation source of truth: this plan (goals-only; no tickets written, none were requested)

## Summary for the reader

- **Profile and phase 1:** production service launched in phases. Phase 1 (G01 to G19) takes a warranty-answer-plus-confirmed-return service to production go-live for an **allowlisted cohort** of real customers, at MVP/pilot depth with the write path built to full depth. Phase 2 hardens it for all customers. All inputs are assumptions (design, Assumed answers).
- **Effort and finish:** phase 1 is **122 to 200 human hours** (summed by hand from the schedule block) against 216 team hours, of which 162 are usable after a 25% reserve. **It fits at the low end only.** Each developer carries 61 to 100 hours against 81 usable. My hand sequencing gives a finish of about **22 working days at the low end and about 39 at the high end, against 30 available**. These figures were not produced by `check_schedule.py` because this session had no shell; treat them as unchecked and run the command below before anyone relies on them.
- **Largest risks:** (1) the return path (G07, 14 to 22 h) and the unknowns behind it (O2 to O4), settled by the discovery goal G03 early in the build; (2) calendar waits outside the team, W1 and W2 at 5 to 10 working days each, gating almost everything that touches cloud or real systems; (3) launching before the penetration test (SB24), an accepted risk nobody has accepted yet (O1).
- **Decisions needed from you:** O1 (cohort launch at pilot depth, or full production depth with a later date); O4 (how customers sign in); O7 (spend ceiling and volume); a start date. Full list in the design's Open decisions.
- **Next prompt:** the three goals that can start on day 1 are G01, G04 (Dev A) and G14 (Dev B); the first is below under Resume here.

If the high end happens, the order in which scope slides to phase 2 without touching the floor is: wiring the evaluation gate into CI (keep a manual run, about 3 h), G13 reduced to logs plus one alert (about 3 h), the ASVS review inside G15 (about 2 h). These recover about 8 of the up to 38 hours of overrun, so **they do not close the gap alone**; closing it means a later date (about 8 weeks), more hours per person, or a third person on G08 and G16. I did not run those as what-ifs (no helper), so none of them is a verified remedy.

## Destination and constraints

End result: a signed-in customer asks warranty questions about their own purchases, gets a status computed from the product database, and files a return request only after confirming the exact details. Non-goals, stack and decisions: see the design. **Authorization: none yet.** The user asked for design and plan only. No repository, project, cloud resource, install or network call exists or was made; every cloud step in a goal is an execution-scope prerequisite until a target and approval are named. Model ID, ADK pin and every price are unverified (design D8, O12).

**Skill availability (checked in this workspace):** installed: `adk-engineer`, `adk-system-designer`, `deploy-adk-on-google-cloud`, `adk-agent-observability`, `adk-tool-auth-and-secrets`. **Not installed here and named by goals below (a setup prerequisite, not applied guidance):** `adk-workflow-design`, `adk-tool-interface-design`, `adk-agent-instructions`, `adk-model-and-output-contracts`, `adk-fastapi-backend`, `adk-frontend-integration`, `adk-memory-architecture`, `safe-api-tool-calls`, `adk-operational-guardrails`, `adk-agent-security`, `protect-adk-sensitive-data`, `adk-agent-evaluation`, `adk-release-engineering`, `adk-presenter`, `adk-governance-pack`; companions `shadcn` and Playwright. **Google product skills:** only the `finding-google-skills` router is installed and it was not invoked (no network). The `google/skills:<name>` entries come from the designer's catalogue table read 21 October 2026; confirm each name through the router before a goal uses it.

## Delivery profile and capacity

| Phase | Delivers | Goals | Human hours (hand sum) | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship to cohort | Warranty answers and confirmed returns live for an allowlisted cohort | G01 to G19 | 122 to 200 | 2 people × 30 days × 3.6 h = 216 h; 25% reserve leaves 162 h |
| 2, harden and open | Production depth, baseline and value, hand-over, then open to all customers | G20 to G27 | 55 to 95 (assumed, coarse) | After phase 1 evidence |

Estimates are agent-assisted human hours (hands-on plus review), assumptions for the stated team. The ×1.5 new-to-ADK multiplier is already applied to the ADK implementation goals; presentation, labelling and governance goals are not ADK work and keep their own estimates. First GCP project setup is a wait (W1), not hours. Handoff hours (1 h each, in the hands-on figure) are recorded on goals that receive work from the other developer.

| Person | Goals | Hours | Usable capacity |
| --- | --- | --- | --- |
| Dev A (agent, data, write path) | G01, G03, G04, G06, G07, G09, G10, G11 | 61 to 100 | 81 |
| Dev B (platform, identity, UI, governance, launch) | G02, G05, G08, G12 to G19 | 61 to 100 | 81 |

Order if time runs out early: Dev A G01, G04, G10, G03, G06, G07, G11, G09. Dev B G14, G05, G02, G12, G13, G08, G15, G17, G16, G18, G19. Each completed goal leaves a working, safe slice.

```yaml
- goal: G01
  phase: 1
  hands_on: 2-3
  review: 1-2
  total: 3-5
  owner: Dev A
  blocked_by: []
  calendar_waits: none
  wait_days: 0
  handoff: 0
  contracts: []
  security: []
  mentions_only: [W3]
  type: presentation
  status: planned
- goal: G02
  phase: 1
  hands_on: 4-6
  review: 1-3
  total: 5-9
  owner: Dev B
  blocked_by: [W1]
  calendar_waits: landing-zone project, billing link, policy exceptions (W1)
  wait_days: 0
  handoff: 0
  contracts: []
  security: []
  mentions_only: []
  type: implementation
  status: planned
- goal: G03
  phase: 1
  hands_on: 4-6
  review: 1-3
  total: 5-9
  owner: Dev A
  blocked_by: [W2]
  calendar_waits: access grants (W2)
  wait_days: 0
  handoff: 0
  contracts: []
  security: []
  mentions_only: [G14]
  type: discovery
  status: planned
- goal: G04
  phase: 1
  hands_on: 6-10
  review: 4-6
  total: 10-16
  owner: Dev A
  blocked_by: []
  calendar_waits: none
  wait_days: 0
  handoff: 0
  contracts: [C3, C11]
  security: []
  mentions_only: [G03]
  type: implementation
  status: planned
- goal: G05
  phase: 1
  hands_on: 5-8
  review: 3-6
  total: 8-14
  owner: Dev B
  blocked_by: [G04]
  calendar_waits: none
  wait_days: 0
  handoff: 1
  contracts: [C1, C2]
  security: [SB01, SB02, SB03, SB04, SB09, SB13, SB20]
  mentions_only: [G12]
  type: implementation
  status: planned
- goal: G06
  phase: 1
  hands_on: 4-6
  review: 2-4
  total: 6-10
  owner: Dev A
  blocked_by: [G03, G05, W3]
  calendar_waits: go-ahead decision (W3)
  wait_days: 0
  handoff: 1
  contracts: [C2, C3, C10]
  security: []
  mentions_only: [G04]
  type: implementation
  status: planned
- goal: G07
  phase: 1
  hands_on: 8-12
  review: 6-10
  total: 14-22
  owner: Dev A
  blocked_by: [G03, G06, W3]
  calendar_waits: none
  wait_days: 0
  handoff: 0
  contracts: [C4, C5, C6, C7, C10]
  security: [SB18]
  mentions_only: [G05]
  type: implementation
  status: planned
- goal: G08
  phase: 1
  hands_on: 6-8
  review: 4-6
  total: 10-14
  owner: Dev B
  blocked_by: [G07, G12]
  calendar_waits: none
  wait_days: 0
  handoff: 1
  contracts: [C1, C4]
  security: [SB10]
  mentions_only: [G05]
  type: implementation
  status: planned
- goal: G09
  phase: 1
  hands_on: 7-10
  review: 4-7
  total: 11-17
  owner: Dev A
  blocked_by: [G07, W4]
  calendar_waits: SME labelling session (W4)
  wait_days: 0
  handoff: 0
  contracts: [C3, C10, C11]
  security: []
  mentions_only: [G06]
  type: implementation
  status: planned
- goal: G10
  phase: 1
  hands_on: 3-5
  review: 2-4
  total: 5-9
  owner: Dev A
  blocked_by: [G04]
  calendar_waits: none
  wait_days: 0
  handoff: 0
  contracts: [C9, C10]
  security: [SB19]
  mentions_only: []
  type: implementation
  status: planned
- goal: G11
  phase: 1
  hands_on: 4-7
  review: 3-5
  total: 7-12
  owner: Dev A
  blocked_by: [G07]
  calendar_waits: none
  wait_days: 0
  handoff: 0
  contracts: [C7, C8]
  security: [SB14, SB17]
  mentions_only: [G14]
  type: implementation
  status: planned
- goal: G12
  phase: 1
  hands_on: 6-9
  review: 3-5
  total: 9-14
  owner: Dev B
  blocked_by: [G02, G05, W3]
  calendar_waits: go-ahead decision (W3)
  wait_days: 0
  handoff: 0
  contracts: [C1]
  security: [SB05, SB06, SB07, SB16, SB25]
  mentions_only: [G08]
  type: implementation
  status: planned
- goal: G13
  phase: 1
  hands_on: 3-5
  review: 2-3
  total: 5-8
  owner: Dev B
  blocked_by: [G12]
  calendar_waits: none
  wait_days: 0
  handoff: 0
  contracts: [C9]
  security: []
  mentions_only: []
  type: implementation
  status: planned
- goal: G14
  phase: 1
  hands_on: 3-5
  review: 2-4
  total: 5-9
  owner: Dev B
  blocked_by: []
  calendar_waits: none
  wait_days: 0
  handoff: 0
  contracts: [C8]
  security: []
  mentions_only: [G03, W5]
  type: governance
  status: planned
- goal: G15
  phase: 1
  hands_on: 2-4
  review: 2-3
  total: 4-7
  owner: Dev B
  blocked_by: [G11, G12]
  calendar_waits: none
  wait_days: 0
  handoff: 1
  contracts: []
  security: [SB15, SB21, SB22]
  mentions_only: []
  type: implementation
  status: planned
- goal: G16
  phase: 1
  hands_on: 2-3
  review: 2-3
  total: 4-6
  owner: Dev B
  blocked_by: [G08, G09, G10, G11, G13]
  calendar_waits: none
  wait_days: 0
  handoff: 1
  contracts: [C1, C2, C4, C5]
  security: []
  mentions_only: []
  type: journey
  status: planned
- goal: G17
  phase: 1
  hands_on: 3-5
  review: 2-3
  total: 5-8
  owner: Dev B
  blocked_by: [G07, G12, G13]
  calendar_waits: none
  wait_days: 0
  handoff: 1
  contracts: [C5, C11]
  security: []
  mentions_only: []
  type: implementation
  status: planned
- goal: G18
  phase: 1
  hands_on: 2-4
  review: 1-2
  total: 3-6
  owner: Dev B
  blocked_by: [G14, G15, G16, G17]
  calendar_waits: none
  wait_days: 0
  handoff: 0
  contracts: []
  security: []
  mentions_only: [W6]
  type: presentation
  status: planned
- goal: G19
  phase: 1
  hands_on: 2-3
  review: 1-2
  total: 3-5
  owner: Dev B
  blocked_by: [G18, W5, W6]
  calendar_waits: privacy sign-off (W5), launch decision (W6)
  wait_days: 0
  handoff: 0
  contracts: []
  security: []
  mentions_only: []
  type: implementation
  status: planned
- goal: W1
  phase: 1
  total: 0
  blocked_by: []
  calendar_waits: administrator creates project, billing link, policy exceptions; requested day 1
  wait_days: 5-10
- goal: W2
  phase: 1
  total: 0
  blocked_by: []
  calendar_waits: product-database read role (masked copy), returns-system staging credentials, customer-identity details; requested day 1
  wait_days: 5-10
- goal: W3
  phase: 1
  total: 0
  blocked_by: [G01]
  calendar_waits: go-ahead decision date after G01
  wait_days: 2-5
- goal: W4
  phase: 1
  total: 0
  blocked_by: []
  calendar_waits: warranty and support experts' labelling session; requested day 1
  wait_days: 3-5
- goal: W5
  phase: 1
  total: 0
  blocked_by: [G14]
  calendar_waits: privacy impact and legal sign-off after drafts
  wait_days: 8-10
- goal: W6
  phase: 1
  total: 0
  blocked_by: [G18]
  calendar_waits: launch decision date after G18
  wait_days: 2-5
```

**Schedule check not run** (no shell in this session). Run from the project root once the repository exists, with Python 3.11 or later, and quote its figures instead of mine:

```bash
python3 "$SKILL_DIR/scripts/check_schedule.py" --plan docs/plans/warranty-returns.md \
  --design docs/architecture/warranty-returns.md --days 30 \
  --reserve 0.25 --person "Dev A=3.6" --person "Dev B=3.6"
```

Hand sequencing behind the finish range (dependencies, one goal at a time per person, waits at their ends, no reserve): Dev A is the longer chain. Low: G04 and G10 done by about day 5, G03 after W2 (day 5), G06 about day 8, G07 about day 12, G11 about day 14, G09 about day 17; Dev B finishes G16 about day 18 and launch about day 22. High: W2 delays G03 to day 10; G07 ends about day 21, G09 about day 29, G16 about day 31, G18 plus W6 about day 38, G19 about day 39. The privacy sign-off (W5) starts after drafts on day 2 or 3 and is not on the critical path. The helper may find different numbers; trust it over this paragraph.

## Implementation map

Proposed module layout (greenfield, nothing inspected): `backend/app/{main,settings,principal,agent_routes,errors}.py`, `backend/app/returns/{proposals,executor,reconcile}.py`, `backend/agent/{agent,tools,warranty_rules}.py`, `backend/migrations/` (application schema only), `frontend/src/`, `docs/design/DESIGN.md`, `AGENTS.md`.

| Contract / decision | Component and integration point | GCP responsibility | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |
| C1, D2 | Principal dependency on `/api`; `user_id` overwritten server-side | Identity Platform | `adk-fastapi-backend` (principle: `adk-tool-auth-and-secrets`) | Captured-token audience (G12/A6) |
| C2, D6 | Tools read `customer_id` from session state; owner filter on records | Read-only DB role | `adk-tool-interface-design`, `adk-tool-auth-and-secrets` | Live read on masked copy |
| C3, D3 | `warranty_rules.py` pure function; tool returns cited fields | Product database | `adk-workflow-design` | Policy owner sign-off (O6) |
| C4–C6, D4, D10 | `propose_return` tool; confirm route; executor and reconcile job over operation table | Cloud SQL; returns-system credential in Secret Manager | `safe-api-tool-calls` | Idempotency or lookup support (O3) |
| C7, D5 | Tool tiers, `before_tool_callback` capability checks, scripted-model suite | None | `adk-agent-security` | Suite on real tool set |
| C8 | Logging allowlist, telemetry content capture off, erase route | Logging, Trace | `protect-adk-sensitive-data`, `adk-agent-observability` | Retention (O13) |
| C9, D9 | `max_llm_calls`, admission and kill switch in the app; max instances; Cloud Armor | Cloud Run, ALB, Cloud Armor, Billing export | `adk-operational-guardrails`, `deploy-adk-on-google-cloud` | Idle costs and prices (G12) |
| C10 | Bounded timeouts, one retry owner, error results | None | `adk-operational-guardrails` | Provider timeouts |
| C11, D8 | Release manifest, eval gate, Cloud Run revision rollback | Artifact Registry, Cloud Run | `adk-release-engineering`, `adk-model-and-output-contracts` | Model lifecycle date, ADK pin |

## Web stack and companion skills

Defaults from the designer's web application defaults apply (Vite/React/TypeScript SPA, generated client, shadcn components themed from `docs/design/DESIGN.md`, one FastAPI process, same origin). G08 writes the companion table with resolved pins into `AGENTS.md`; no deviation is recorded.

## Goals and dependencies

Goals-only plan: each phase 1 goal below is its own home. Run prompt for any goal: `/adk-engineer Carry out <ID> from docs/plans/warranty-returns.md. Read docs/architecture/warranty-returns.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence under the goal.` Status and evidence for every goal start as planned and empty.

| ID and goal | Type | Hours (total) | Depends on | Primary skill |
| --- | --- | --- | --- | --- |
| G01 Go-ahead presentation | presentation | 3-5 | none | `adk-presenter` |
| G02 Foundation and environments | implementation | 5-9 | W1 | `deploy-adk-on-google-cloud` |
| G03 Data and integration discovery | discovery | 5-9 | W2 | `adk-engineer` |
| G04 Warranty agent skeleton | implementation | 10-16 | none | `adk-workflow-design` |
| G05 Identity and per-customer scope | implementation | 8-14 | G04 | `adk-fastapi-backend` |
| G06 Product database tools | implementation | 6-10 | G03, G05, W3 | `adk-tool-interface-design` |
| G07 Propose, confirm, file | implementation | 14-22 | G03, G06, W3 | `safe-api-tool-calls` |
| G08 Customer chat UI | implementation | 10-14 | G07, G12 | `adk-frontend-integration` |
| G09 Evaluation set and gate | implementation | 11-17 | G07, W4 | `adk-agent-evaluation` |
| G10 Spend and abuse stops | implementation | 5-9 | G04 | `adk-operational-guardrails` |
| G11 Injection, sensitive data, erasure | implementation | 7-12 | G07 | `adk-agent-security` |
| G12 Staging deployment | implementation | 9-14 | G02, G05, W3 | `deploy-adk-on-google-cloud` |
| G13 Minimal observability | implementation | 5-8 | G12 | `adk-agent-observability` |
| G14 Governance drafts | governance | 5-9 | none | `adk-governance-pack` |
| G15 Security review | implementation | 4-7 | G11, G12 | `adk-agent-security` |
| G16 End-to-end journey | journey | 4-6 | G08, G09, G10, G11, G13 | `adk-agent-evaluation` |
| G17 Production readiness | implementation | 5-8 | G07, G12, G13 | `adk-release-engineering` |
| G18 Launch-decision presentation | presentation | 3-6 | G14, G15, G16, G17 | `adk-presenter` |
| G19 Cohort go-live | implementation | 3-5 | G18, W5, W6 | `deploy-adk-on-google-cloud` |

Waits requested on day 1, before any goal starts: W1, W2, W4. W3 starts when G01 is presented; W5 when G14 drafts are sent; W6 after G18.

Presentations: G01 (business audience, approval to build) and G18 (business plus the platform and security reviewers, decision to go live); the results review is phase 2 (G26). The statement of work, portability and teardown goals do not apply (internal build; no lock-in concern; production resources carry forward and are owned by the cost contract and the decommission item in Later).

### G01 Go-ahead presentation

- **Outcome:** a deck outline and decision memo for the sponsor from this design and plan: scope, the assumed answers, the cohort-versus-production choice (O1), the cost placeholder (O7), the accepted risk (SB24). Evidence slides cite design IDs; there is no run evidence yet, and the deck must say so.
- **Skills:** `adk-presenter`. **Acceptance:** A1 the outline passes the presenter's deck check and every claim cites a design or plan ID (deliverable). A2 the decision memo lists O1, O4 and O7 with a named decider each (deliverable). **Wait:** W3.

### G02 Foundation and environments (Dev B)

- **Outcome and depth:** the team can deploy to dev, staging and production projects in the landing zone with effective org policies read and recorded. Terraform or scripted, no console clicks that cannot be reproduced.
- **Route and prerequisites:** read `gcloud org-policies describe ... --effective` for `gcp.resourceLocations`, `iam.disableServiceAccountKeyCreation`, `iam.allowedPolicyMemberDomains`, `gcp.restrictServiceUsage`, `sql.restrictPublicIp`, `compute.vmExternalIpAccess`; check `billingEnabled`; enable APIs per goal (`run`, `aiplatform`, `secretmanager`, `artifactregistry`, `logging`, `monitoring`, `cloudtrace`; `sqladmin`, `compute` and `identitytoolkit` are enabled by G12). A VPC Service Controls perimeter would make every cross-boundary call a W-style wait; record yes or no.
- **Skills:** `deploy-adk-on-google-cloud`; `google/skills:google-cloud-recipe-onboarding`, `google-cloud-recipe-auth`, `gcloud` (read-only inspection and enablement, scoped flags, no global config changes). **Resources created:** Artifact Registry repository (storage beyond the free tier; idle cost not looked up, record with pricing date before creating); Secret Manager entries. Cleanup and absence checks: `gcloud artifacts repositories delete` and `list`; `gcloud secrets delete` and `list`.
- **Acceptance:** A1 the effective-policy readout is recorded with the region decision (O5). A2 service accounts exist per design identity (serving, executor, product-DB reader, deployer) with no keys. A3 a recorded readback shows enabled APIs match the list above.
- **Execution scope:** needs W1, a target project and approval for each enablement.

### G03 Data and integration discovery (Dev A)

- **Question and stopping condition:** settle O2, O3, O4, O6 in at most 6 hours. Stop when each has a documented answer or a named owner and a date. Deliver `docs/discovery/data-and-integrations.md`.
- **Expected decisions:** product-database engine, access path and masked copy; returns-system API, idempotency or status lookup, what a return triggers; how customers sign in and map to purchases; who owns the warranty rule and whether policy text is unstructured. Updates C1 to C6 in place with one-line notes if any answer changes them, and resets G05 to G07 estimates.
- **Unblocks:** G06, G07; narrows the estimate ranges. If O4 shows customers do not sign in, return to the design before G05.
- **Acceptance:** A1 each of O2, O3, O4, O6 is closed or owned with a date (deliverable). A2 any contract change is listed with the goals it moves (deliverable).

### G04 Warranty agent skeleton (Dev A)

- **Outcome:** locally, a scripted-model and a real-model run answer warranty questions from a fake product database through the rule function. No cloud, no real data.
- **Contracts:** C3, C11. **Route:** `LlmAgent` with `get_warranty_status` and `lookup_purchases`, `warranty_rules.py`, offline tests, a test principal via dependency override only in tests. Pins ADK and the model ID from the lifecycle table.
- **Skills:** `adk-workflow-design`; supporting `adk-tool-interface-design`, `adk-agent-instructions`, `adk-model-and-output-contracts`.
- **Acceptance:** A1 table-driven rule tests: covered, expired, boundary day, missing purchase date yields "cannot determine" (C3). A2 scripted model: the tool returns "no record" and the answer states it cannot determine and invents no date (C3). A3 the dumped tool declarations show the intended tools only, each with primitive parameters and a bounded result, and a rendered-request test shows a stable instruction prefix (C3). A4 the ADK version and model ID are pinned, each interface used is confirmed against the pin, and the model's retirement date is recorded (C11).

### G05 Identity and per-customer scope (Dev B)

- **Outcome:** only a verified customer can reach `/api`; every tool and record route is scoped to them.
- **Contracts and rules:** C1, C2; SB01, SB02, SB03, SB04, SB09, SB13, SB20. **Route:** principal dependency failing closed, server overwrite of `user_id`, `DatabaseSessionService` on a local database, owner filter on records, one error handler. Live-token checks wait for G12.
- **Skills:** `adk-fastapi-backend`; supporting `adk-tool-auth-and-secrets`, `adk-memory-architecture`.
- **Acceptance:** A1 with no verifier configured every `/api` route returns 401 (C1, SB01). A2 expired, wrong-audience, forged-header and forged-signature tokens are rejected (C1, SB02). A3 a forged `user_id` runs in the caller's own scope, and another customer's session id returns the same 404 body as an unknown one with no model call (C1, SB03). A4 two-customer test: a tool call naming another customer's order finds nothing (C2, SB04). A5 a verifier outage denies, and a forced exception returns a generic 500 with a request id and no internals (SB13). A6 a revoked token is refused on a sensitive action (SB20). A7 oversize and malformed bodies get 413 or 422, and no string-built SQL exists (SB09).

### G06 Product database tools (Dev A)

- **Outcome:** the agent answers from the real (masked) product database on staging.
- **Contracts:** C2, C3, C10. **Route:** read-only role through workload identity, parameterised queries scoped by trusted `customer_id`, bounded rows, error results with a status field.
- **Skills:** `adk-tool-interface-design`; supporting `adk-tool-auth-and-secrets`; `google/skills:gcloud`, `iam-helper-for-policy-management` (read-only role binding, proposals needing approval). **Execution scope:** W2 grants and W3.
- **Acceptance:** A1 on the masked copy, three test customers get the expected cited warranty fields (C3). A2 a database timeout or outage returns a bounded actionable error and the answer says it cannot check, with no fabricated status (C10). A3 an empty authorised result does not widen the query (C2). A4 an oversized result is bounded, and connection exhaustion triggers one bounded retry owner and then an honest failure. A5 permission denied or schema drift returns an actionable error and an alert signal (C10). A6 a revoked reader role surfaces as "cannot check" and is detected (C10).

### G07 Propose, confirm, file (Dev A)

- **Outcome:** a customer proposes a return, sees the exact details, confirms, and exactly one request is filed or its true state is shown.
- **Contracts and rules:** C4, C5, C6, C7, C10; SB18. **Route:** `propose_return` (draft with canonical hash), confirm route (owner, hash, recheck), executor (atomic claim, operation record before dispatch, idempotency key per O3), reconcile job. Returns system is a fake until W2 gives a staging target; live acceptance runs there, never against production.
- **Skills:** `safe-api-tool-calls`; supporting `adk-operational-guardrails`, `adk-agent-security`, `adk-tool-auth-and-secrets`.
- **Acceptance:** A1 `propose_return` writes only a draft and makes no returns-system call (C4). A2 confirm by the same customer with the matching hash files exactly once; reject runs the filing zero times (C4, SB18). A3 a changed detail, changed warranty status or an existing open return makes confirm refuse with the reason (C6). A4 a double click and two concurrent confirms produce one filing (C5). A5 killing the process after the returns system accepts and before the receipt is recorded, then restarting, reconciles by lookup and files nothing twice (C5). A6 a returns-system rejection is shown, not retried in a loop, and the draft stays (C10). A7 a timeout and a 429 leave the operation pending with visible status and no duplicate (C5, C10). A8 confirming another customer's draft returns 404 with no effect (C1, C2). A9 the declared tools for the model contain no filing tool (C4, C7). A10 "return everything I bought" yields one separately confirmed proposal per line, none filed together. A11 a malformed returns-system response is treated as outcome unknown (C5). A12 an expired or revoked returns-system credential holds the operation, alerts, and creates no duplicate (C5). A13 if the operation record cannot be written, the returns system is not called and the customer is told (C10).
- **Estimate risk:** the 14 to 22 hours depend on O3. With no idempotency key and no lookup, this goal grows and a design checkpoint is needed.

### G08 Customer chat UI (Dev B)

- **Outcome:** sign in, ask, read a streamed answer with status block, review a proposal card, confirm or reject.
- **Contracts and rules:** C1, C4; SB10. **Companions:** `shadcn`, Playwright; design system `docs/design/DESIGN.md` from the house system. Writes the companion table into `AGENTS.md`.
- **Skills:** `adk-frontend-integration`; supporting `adk-fastapi-backend`.
- **Acceptance:** A1 the browser journey runs against the real API with a scripted model: sign-in, answer, proposal card, confirm, receipt (C1, C4). A2 a reply containing an `<img onerror>` payload, a `javascript:` link and an image from an unlisted host renders inert and loads nothing (SB10). A3 a stale confirm card after a status change shows the refusal and no filing (C4). A4 a dropped stream shows an incomplete turn and never a filed state, and the status is re-read from the operation record. A5 the hand-off route for unanswerable questions is shown (O8).

### G09 Evaluation set and gate (Dev A)

- **Outcome:** a measured answer-quality and return-flow baseline, and a gate that fails by exit code.
- **Contracts:** C3, C10, C11. **Route:** at least 30 labelled cases (covered, expired, boundary, no purchase, foreign order, ambiguous product, injected text, return flows), criteria file and agreement report from the experts, runner, gate script; the CI wiring is the first item that slides (summary).
- **Skills:** `adk-agent-evaluation` with its expert-review reference; supporting `adk-release-engineering`. Experts' hours and the session date are W4; the quality decision-maker is the sponsor's nominee (O6).
- **Acceptance:** A1 a versioned criteria file, a gold set with provenance and an agreement report exist (C3). A2 introducing a regression in a rule or prompt makes the gate exit non-zero and the release manifest records the eval-set hash (C3, C11). A3 a scripted model returning prose, fenced JSON and schema-valid wrong data each gets the designed response: bounded repair then an explicit failure, wrong-but-valid counted separately (C10).

### G10 Spend and abuse stops (Dev A)

- **Outcome:** a looping, concurrent or abusive customer cannot run up spend; an operator can stop new sessions at once.
- **Contracts and rules:** C9, C10; SB19. **Route:** `max_llm_calls` from a measured run, per-customer allowance, one active run per customer and conversation, global cap, kill switch outside agent authority, state in the database, fail closed.
- **Skills:** `adk-operational-guardrails`. Needs O7 for numbers; otherwise labelled provisional values.
- **Acceptance:** A1 a scripted looping agent is stopped by the cap (C9, SB19). A2 model unavailable and model 429 give bounded retries owned in one place and an honest message (C10). A3 a second concurrent run for the same customer is refused, and the per-customer allowance refuses the next conversation (C9, SB19). A4 the kill switch refuses new sessions regardless of budget resets (C9). A5 control store unavailable or the connection pool exhausted refuses new runs (fail closed) (C9).

### G11 Injection, sensitive data, erasure (Dev A)

- **Outcome:** hostile text and personal data cannot cause harm or leak.
- **Contracts and rules:** C7, C8; SB14, SB17. **Route:** adversarial scripted-model suite on the real tool set, logging allowlist, telemetry content capture off, erase route plus delete job with a tombstone for late writers; screening seams at ingress, storage, tool and log only where a threat is shown (no Model Armor by default).
- **Skills:** `adk-agent-security`; supporting `protect-adk-sensitive-data`. Retention periods depend on O13.
- **Acceptance:** A1 an instruction planted in a product-database free-text field and in a customer message does not cause a filing, a foreign read or a disclosure; the forbidden call never runs (C7, SB17). A2 a denied-access log line exists and no message content or personal data appears in logs or traces (C8, SB14). A3 each exposure seam (ingress, session storage, tool results, telemetry) has a recorded policy and a test (C8). A4 erase removes sessions and drafts, and a queued late write is refused (C8).

### G12 Staging deployment (Dev B)

- **Outcome:** the application runs on staging behind the load balancer with real sign-in, masked data and the returns system's test target.
- **Contracts and rules:** C1; SB05, SB06, SB07, SB16, SB25. **Route:** Cloud Run service, ALB with Cloud Armor rate rule, ingress internal-LB only, Cloud SQL (private connectivity), Secret Manager, labels in deployment code, `identitytoolkit` configuration, live token audience check, ADK paths unreachable.
- **Skills:** `deploy-adk-on-google-cloud`; `google/skills:cloud-run-basics`, `google-cloud-solution-n-tier-serverless-web-app`, `google-cloud-global-frontend-configuration`, `cloud-sql-basics`, `iam-helper-for-policy-management`. **Execution scope:** W1, W3, an approved target; no command runs before the cost record below exists.
- **Resources created (record idle cost and pricing date before creating; none was looked up):** Cloud SQL instance (staging and production); external ALB forwarding rule, static IP and Cloud Armor policy; Cloud Run with minimum instances (staging 0, production per the cost record); Artifact Registry images; Secret Manager versions. Cleanup: `gcloud run services delete`; forwarding rule, then proxy, URL map, backend, address; `gcloud sql instances delete` then check backups; `gcloud artifacts repositories delete`; `gcloud secrets delete`. Absence: the matching `list` commands empty and backups page checked. **Lifetime owner:** the cost contract C9 and the decommission item in Later (production resources are not torn down by a phase goal).
- **Acceptance:** A1 at the deployed URL, `/apps/…`, `/run`, `/run_sse`, `/list-apps` and the dev UI return no ADK data and cause no model call (SB05). A2 the `run.app` URL cannot reach the service; only the load balancer can. A3 a preflight from an unlisted origin gets no allow header; `/docs`, `/redoc` and `/openapi.json` return neither UI nor schema; the CSP, `nosniff`, referrer and HSTS headers are present (SB06, SB07). A4 a rate-limit test triggers the Cloud Armor rule (SB25). A5 secrets come from Secret Manager, the secret scan is clean, and a missing or unreachable secret makes the service refuse to become ready (SB16). A6 a captured live token confirms the audience, and a token for another audience is refused (C1, SB02). A7 an identity-provider outage on staging denies access.

### G13 Minimal observability (Dev B)

- **Contracts:** C9 (evidence). **Route:** one telemetry owner per process, one span per agent, tool and logical model call with the conversation id, token usage counted once, content capture off, structured logs, two alerts (error ratio, stuck operations), a trace-to-session lookup.
- **Skills:** `adk-agent-observability`; `google/skills:cloud-run-alert-configuration`, `cloud-monitoring-notification-channels-configuration`.
- **Acceptance:** A1 an in-memory exporter test shows the spans with the conversation id. A2 usage is counted once per logical model call. A3 a synthetic failure fires the alert to a named channel and the alert leads to a stored session (C9).

### G14 Governance drafts (Dev B)

- **Outcome:** drafts for counsel, the privacy officer and security reviewers: jurisdiction screen (region from O5), regulatory memo, privacy impact inputs, impact assessment, system card, processing records, questionnaire answers. Real personal data is in scope from go-live, so this is not optional.
- **Skills:** `adk-governance-pack`. **Contracts:** C8. **Acceptance:** A1 the pack's checker passes on the drafts, each statement citing contract, decision and evidence IDs or flagged for counsel (deliverable). A2 the sign-off request is sent when drafts go out, starting W5 (deliverable). Drafts are revised after G03 closes O2 to O4.

### G15 Security review (Dev B)

- **Rules:** SB15, SB21, SB22. **Acceptance:** A1 a ZAP baseline scan against staging is recorded with each finding fixed or accepted (SB21). A2 an ASVS Level 1 review is recorded with gaps as goals (SB22). A3 `make check` runs Python and JavaScript audits failing on high findings, lockfiles are committed and pre-1.0 tools pinned (SB15). **Skills:** `adk-agent-security`, `adk-release-engineering`.

### G16 End-to-end journey (Dev B)

- **Outcome:** the whole path on staging, with every earlier acceptance item rerun (`pass_to_pass`: G05/A1 to A7, G07/A1 to A13, G08/A1 to A4, G10/A1 to A5, G11/A1 to A4).
- **Contracts:** C1, C2, C4, C5. **Skills:** `adk-agent-evaluation`; companion Playwright. **Acceptance:** A1 sign-in, warranty question, proposal, confirm, receipt on staging with masked data passes, and a second customer cannot see the first's draft (C1, C2, C4, C5). A2 all `pass_to_pass` items pass in one run.

### G17 Production readiness (Dev B)

- **Contracts:** C5, C11. **Route:** release manifest, rollback rehearsal on staging, Cloud SQL point-in-time restore into a non-production environment, restart test with an in-flight operation, runbook, on-call and incident roles (O10), reconcile alert owner.
- **Skills:** `adk-release-engineering`; supporting `adk-agent-observability`; `google/skills:cloud-sql-basics`, `google-cloud-waf-reliability`, `google-cloud-waf-cost-optimization`.
- **Acceptance:** A1 a restored copy meets the stated RPO and RTO and the time taken is recorded. A2 rollback to the previous revision serves, and the manifest's image, prompt, model, tool-schema, eval-set and secret versions move together (C11). A3 a named person is on call, a runbook and incident roles exist, and the Cloud Billing export and budget alert exist with a named reader. A4 a process restart with an operation in flight leaves its record intact, and the reconcile job completes it without a second filing (C5).

### G18 Launch-decision presentation (Dev B)

- **Outcome:** deck outline, narrative, expected questions and one-page decision memo for the sponsor, platform and security reviewers, built only from recorded evidence: the contract table with evidence tiers, G09's measured results, G15's findings, G14 status, the accepted risk (SB24) restated for a decision, the cohort definition. **Skills:** `adk-presenter`. **Acceptance:** A1 the outline passes the deck check and every claim cites recorded evidence (deliverable). Decision date is W6.

### G19 Cohort go-live (Dev B)

- **Outcome:** production deployed with the cohort allowlist enforced, and a first-day watch. Starts only after W5 and W6. **Skills:** `deploy-adk-on-google-cloud`, `adk-release-engineering`. **Resources created:** the production set under G12's cost record, with the idle cost already recorded. **Acceptance:** A1 a non-allowlisted customer is refused and an allowlisted one completes the journey (C1). A2 the production release manifest equals the staged one. A3 the kill switch and rollback were each exercised once on production before the cohort was told. **Execution scope:** a named production project, approval from W6, and the real-data access W2 grants for production.

## Phase 2 (coarse, will change after phase 1 evidence)

| ID | Goal | Primary skill | Hours | One acceptance check |
| --- | --- | --- | --- | --- |
| G20 | First live week: read the bill against C9, record measurement records (M1 cost per conversation, M2 answered-without-support share against a baseline measured first) | `adk-agent-observability` | 3-6 | M records exist with baseline, window, sample and method |
| G21 | Production hardening: penetration test by an outside party (SB24) and ASVS Level 2 with adversarial suite (SB23); findings fixed or owned | `adk-agent-security` | 12-24 plus test wait | Findings closed or accepted by a named owner |
| G22 | Canary and joint rollback automation, evaluation gate in CI, judge schedule | `adk-release-engineering` | 8-14 | A bad build is stopped by exit code and a canary rolls back |
| G23 | Full SLOs, dashboards, burn-rate alerts, feedback capture, production-to-evaluation loop | `adk-agent-observability` | 8-14 | An alert leads to a stored session that becomes an evaluation case |
| G24 | Operations hand-over to IT and the rollout pack for support staff | `adk-agent-observability`, `adk-presenter` | 8-14 | Receiving team runs a drill from the runbook |
| G25 | Open to all customers: load experiment, quota and Cloud Armor tuning, capacity | `optimise-adk-on-google-cloud` | 6-10 | Burst test holds stated latency and spend |
| G26 | Results review presentation after the first period | `adk-presenter` | 3-6 | Every figure cites an M or I record |
| G27 | Value report and a stop, continue or scale call | `adk-presenter` | 3-5 | Report cites measured baseline and counter-metric |

The decision to open to all customers waits on G21 and G26.

## Later

| Item | Trigger | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| Retrieval over unstructured policy text | O6 shows policy outside structured fields | Answers limited to structured fields | `adk-memory-architecture` |
| Photo or file upload for returns (SB11 then applies) | Business asks for evidence | Customers describe issues in text | `adk-fastapi-backend` |
| Refund or payment effects | O3 shows returns trigger money | Not built; raises C5 to money depth | `safe-api-tool-calls` |
| Human-ticket creation on hand-off | O8 asks for it | Contact link only | `adk-tool-interface-design` |
| Other languages | O9 | English only | `adk-agent-evaluation` |
| Model and capacity cost review (smallest passing model, committed use) | First bill, or a volume step, then quarterly | Possible overspend within the C9 ceiling | `optimise-adk-on-google-cloud` |
| Regional failover, game day | Availability target above single-region | Regional outage stops service | `deploy-adk-on-google-cloud` |
| Model retirement re-baseline | A retirement date inside 90 days | None if the calendar is kept | `adk-release-engineering` |
| Decommission of staging and production | Application retirement | Idle cost continues until done | `deploy-adk-on-google-cloud` |

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| The design | Contracts, decisions, accepted and open decisions |
| This plan | Capacity, cut line, goals and acceptance |
| Evaluation summary (created by G09) | Latest result per case |

## Open decisions for further planning

See the design's Open decisions O1 to O13. Blocking: O4 (G05), O3 (G07), O2 (G06), O1 (G18/G19 scope), O7 (G10 values). Independent work remains possible meanwhile: G01, G04, G14.

## Independent review

**Not done.** This session had no subagent or shell. Before the plan is handed to two developers, run the independent plan review prompt in `.claude/skills/adk-system-designer/assets/plan-review-prompt.md` in a fresh session, settle each finding in a change table here, and rerun the schedule command above.

## Resume here

- **Next goals (parallel on day 1):** G01 (Dev A), G04 (Dev A), G14 (Dev B); request W1, W2 and W4 the same day.
- **Read first:** the design, then this plan's Summary.
- **Continuation prompt:**

```text
/adk-engineer Carry out G04 Warranty agent skeleton from docs/plans/warranty-returns.md.
Read docs/architecture/warranty-returns.md and preserve its decisions.
Use adk-workflow-design with adk-tool-interface-design, adk-agent-instructions and adk-model-and-output-contracts
(install any that are missing first). Work locally with a fake product database and no cloud;
verify A1 to A4 and record the evidence and any remaining blockers under G04.
```
