# Implementation plan: home-insurance claim filing agent

Status: draft. Ready goals identified; nothing implemented.
Architecture: [docs/architecture/home-claim-agent.md](../architecture/home-claim-agent.md)
Continuation source of truth: this plan. The phase 1 goals are also tickets
in [docs/tickets/home-claim-agent/](../tickets/home-claim-agent/). Each ticket
copies its goal's figures from the schedule block below.

## Destination and constraints

**Destination.** EU GA, about 2027-03-12, of a customer-facing ADK agent in
the existing portal. It takes a home-insurance first notice of loss with
photos, and the customer's confirmation creates the claim in Guidewire
ClaimCenter (design D1 to D15). **Non-goals:** coverage decisions, cost
estimates, payouts, other lines, updates to existing claims.

**Proposed stack (the user has not accepted it):** Python; google-adk
(working assumption 2.8.0, production floor ≥ 2.10.0 recommended; G03 pins
it); FastAPI gateway; Cloud Run (two services); Cloud SQL for PostgreSQL; GCS;
Cloud Tasks; SDP; Vertex AI regional EU endpoint; Secret Manager;
OpenTelemetry to Cloud Trace and Monitoring.

**Pinned artefacts the goals inherit:** agent and photo-reader model
`gemini-3.8-flash` (provisional, D7), fallback pin `gemini-3.5-flash`. The
judge model is chosen and pinned in G08. Prompt versions are created in G06
and G07. Changing any of these is a release (D14), not a side effect.

**Authorization in this session:** design only. No goal is authorised to
provision cloud resources, call Guidewire or spend money until the team
assigns it and names the target project. Credentials and resource IDs stay
out of this repository.

**Inspected repository:** empty apart from `.claude/skills/`. Every module
path below is a **proposed** layout:

```text
app/
  gateway/        FastAPI app, auth dependency, routes, SSE, upload
  agent/          ADK App + LlmAgent factory, instructions/, tools/
  photos/         validation, re-encode, photo reader
  drafts/         claim_draft model, versions, canonical payload + hash
  submission/     confirm, operation record, Cloud Tasks dispatch, worker
  guidewire/      Cloud API client, fake for tests
  guards/         SDP client, allowances, admission, kill switch
  telemetry/      OTel setup
evals/            cases/, photos/, runner, judge config
infra/            Terraform or reviewed gcloud runbooks
tests/
```

## Delivery profile and capacity

Profile: **production service** (design, *Delivery constraints*).

| Phase | Delivers | Goals | Human hours, agent-assisted | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship to staff pilot | The full journey on EU staging against the Guidewire sandbox, with every floor control, evaluated, security-reviewed in three passes, used by staff on synthetic data. Production Guidewire access is in place (dark) and the DPIA is submitted | G01 to G24 | 620-1052 | 60 working days (2026-10-12 to 2027-01-15, holidays excluded). 6 people × 5 focused h/day + reviewer × 2 h/day, 25 % reserve → 1,440 h |
| 2, graduate to GA | Production, canary, SLO alerts, storm load test, pen test, accessibility, launch language, invited-customer pilot, GA decision | G25 to G34 | 256-430 | 40 working days (2027-01-18 to 2027-03-12) → 960 h |

**Estimates.** Person-hours of human effort with a coding agent (hands-on
plus review and verify). Every figure already includes the **×1.5 multiplier
for a team new to ADK** (assumption A5), applied to all goals alike. Review
is sized to the change: heavier for identity, the Guidewire write and
security, lighter for setup, requests and templates. Calendar waits are on
the goals, not in the hours.

**Phase 1 load** (from the schedule check):

| Person or role | Goals | Hours | Their capacity (60 days, after reserve) |
| --- | --- | --- | --- |
| Eng A | G04, G13, G17 | 80-134 | 225 |
| Eng B | G01, G09, G10, G24 | 112-190 | 225 |
| Eng C | G05, G11, G15 | 84-144 | 225 |
| Eng D | G03, G07, G12, G22 | 91-152 | 225 |
| Eng E | G02, G14, G16, G23 | 121-204 | 225 |
| ML engineer | G06, G08 | 96-164 | 225 |
| Security reviewer | G18, G19, G20, G21 | 36-64 | 90 |

Eng A has the most slack. If the security reviewer cannot reach 4 h/day
(open decision), Eng A is the natural second reader for G19. A security
review needs a reader independent of the code's author, so G19 and G20 cannot
go to the engineers who wrote G10, G13 or G14.

Schedule block (the only source of each estimate; tickets copy it):

```yaml
# ---------- Phase 1 ----------
- goal: G01
  phase: 1
  hands_on: 14-24
  review: 4-6
  total: 18-30
  owner: Eng B
  blocked_by: []
  calendar_waits: Guidewire sandbox credentials and API docs from the Guidewire platform team
  wait_days: 5-10
- goal: G02
  phase: 1
  hands_on: 20-32
  review: 6-10
  total: 26-42
  owner: Eng E
  blocked_by: []
  calendar_waits: EU projects and Vertex quota from the cloud platform team
  wait_days: 3-5
- goal: G03
  phase: 1
  hands_on: 16-28
  review: 6-10
  total: 22-38
  owner: Eng D
  blocked_by: []
  calendar_waits: none
  wait_days: 0
- goal: G04
  phase: 1
  hands_on: 18-30
  review: 10-16
  total: 28-46
  owner: Eng A
  blocked_by: [G03]
  calendar_waits: none on this goal's path: CIAM staging client requested on day 1, needed before G24
  wait_days: 0
- goal: G05
  phase: 1
  hands_on: 18-30
  review: 8-14
  total: 26-44
  owner: Eng C
  blocked_by: [G03]
  calendar_waits: none
  wait_days: 0
- goal: G06
  phase: 1
  hands_on: 30-52
  review: 8-14
  total: 38-66
  owner: ML
  blocked_by: [G05]
  calendar_waits: none
  wait_days: 0
- goal: G07
  phase: 1
  hands_on: 30-50
  review: 10-16
  total: 40-66
  owner: Eng D
  blocked_by: [G03]
  calendar_waits: none
  wait_days: 0
- goal: G08
  phase: 1
  hands_on: 50-84
  review: 8-14
  total: 58-98
  owner: ML
  blocked_by: []
  calendar_waits: none
  wait_days: 0
- goal: G09
  phase: 1
  hands_on: 16-26
  review: 8-14
  total: 24-40
  owner: Eng B
  blocked_by: [G03]
  calendar_waits: none
  wait_days: 0
- goal: G10
  phase: 1
  hands_on: 32-56
  review: 12-20
  total: 44-76
  owner: Eng B
  blocked_by: [G01, G09]
  calendar_waits: none
  wait_days: 0
- goal: G11
  phase: 1
  hands_on: 28-48
  review: 8-14
  total: 36-62
  owner: Eng C
  blocked_by: [G04, G05]
  calendar_waits: UX and brand review of the chat and confirmation card
  wait_days: 3-5
- goal: G12
  phase: 1
  hands_on: 20-34
  review: 6-10
  total: 26-44
  owner: Eng D
  blocked_by: [G04, G09]
  calendar_waits: none
  wait_days: 0
- goal: G13
  phase: 1
  hands_on: 24-40
  review: 10-16
  total: 34-56
  owner: Eng A
  blocked_by: [G03, G05]
  calendar_waits: none
  wait_days: 0
- goal: G14
  phase: 1
  hands_on: 22-38
  review: 10-16
  total: 32-54
  owner: Eng E
  blocked_by: [G07, G09]
  calendar_waits: none
  wait_days: 0
- goal: G15
  phase: 1
  hands_on: 16-28
  review: 6-10
  total: 22-38
  owner: Eng C
  blocked_by: [G03]
  calendar_waits: none
  wait_days: 0
- goal: G16
  phase: 1
  hands_on: 32-56
  review: 10-16
  total: 42-72
  owner: Eng E
  blocked_by: [G02, G03]
  calendar_waits: none
  wait_days: 0
- goal: G17
  phase: 1
  hands_on: 14-24
  review: 4-8
  total: 18-32
  owner: Eng A
  blocked_by: [G16]
  calendar_waits: none
  wait_days: 0
- goal: G18
  phase: 1
  hands_on: 6-10
  review: 2-4
  total: 8-14
  owner: Security reviewer
  blocked_by: [G04, G09]
  calendar_waits: none
  wait_days: 0
- goal: G19
  phase: 1
  hands_on: 4-8
  review: 2-2
  total: 6-10
  owner: Security reviewer
  blocked_by: [G10, G13]
  calendar_waits: none
  wait_days: 0
- goal: G20
  phase: 1
  hands_on: 5-9
  review: 1-3
  total: 6-12
  owner: Security reviewer
  blocked_by: [G14, G18, G19]
  calendar_waits: none
  wait_days: 0
- goal: G21
  phase: 1
  hands_on: 12-20
  review: 4-8
  total: 16-28
  owner: Security reviewer
  blocked_by: []
  calendar_waits: DPO review and sign-off of the DPIA
  wait_days: 20-30
- goal: G22
  phase: 1
  hands_on: 2-3
  review: 1-1
  total: 3-4
  owner: Eng D
  blocked_by: []
  calendar_waits: Guidewire production change approval and IP allow-list
  wait_days: 10-15
- goal: G23
  phase: 1
  hands_on: 16-27
  review: 5-9
  total: 21-36
  owner: Eng E
  blocked_by: [G10, G22]
  calendar_waits: none
  wait_days: 0
- goal: G24
  phase: 1
  hands_on: 20-34
  review: 6-10
  total: 26-44
  owner: Eng B
  blocked_by: [G04, G06, G08, G10, G11, G12, G13, G14, G15, G17]
  calendar_waits: none
  wait_days: 0
# ---------- Phase 2 ----------
- goal: G25
  phase: 2
  hands_on: 26-44
  review: 10-16
  total: 36-60
  owner: Eng A
  blocked_by: [G16, G23, G24]
  calendar_waits: none
  wait_days: 0
- goal: G26
  phase: 2
  hands_on: 28-46
  review: 10-16
  total: 38-62
  owner: Eng E
  blocked_by: [G17, G24]
  calendar_waits: none
  wait_days: 0
- goal: G27
  phase: 2
  hands_on: 22-38
  review: 8-12
  total: 30-50
  owner: Eng E
  blocked_by: [G25]
  calendar_waits: none
  wait_days: 0
- goal: G28
  phase: 2
  hands_on: 8-14
  review: 4-6
  total: 12-20
  owner: Eng C
  blocked_by: [G14, G16, G20]
  calendar_waits: external penetration test on staging (booked in G18)
  wait_days: 10-15
- goal: G29
  phase: 2
  hands_on: 22-38
  review: 8-12
  total: 30-50
  owner: Eng C
  blocked_by: [G24]
  calendar_waits: external accessibility audit
  wait_days: 5-10
- goal: G30
  phase: 2
  hands_on: 34-60
  review: 6-10
  total: 40-70
  owner: ML
  blocked_by: [G24]
  calendar_waits: none
  wait_days: 0
- goal: G31
  phase: 2
  hands_on: 18-30
  review: 6-10
  total: 24-40
  owner: Eng D
  blocked_by: [G21, G25, G28]
  calendar_waits: two weeks of invited-customer traffic
  wait_days: 10
- goal: G32
  phase: 2
  hands_on: 12-22
  review: 4-6
  total: 16-28
  owner: Eng D
  blocked_by: [G24]
  calendar_waits: none
  wait_days: 0
- goal: G33
  phase: 2
  hands_on: 14-24
  review: 4-6
  total: 18-30
  owner: ML
  blocked_by: [G24]
  calendar_waits: none
  wait_days: 0
- goal: G34
  phase: 2
  hands_on: 8-14
  review: 4-6
  total: 12-20
  owner: Eng B
  blocked_by: [G26, G27, G29, G30, G31]
  calendar_waits: go/no-go meeting with claims, legal, DPO and security
  wait_days: 1-2
```

### Schedule check

Run on 2026-10-09 with Python 3.12 (the default `python3` here is 3.9; the
skill asks for 3.11 or later):

```bash
P=.claude/skills/adk-system-designer/scripts/check_schedule.py
PEOPLE=(--person "Eng A=5" --person "Eng B=5" --person "Eng C=5" --person "Eng D=5" \
        --person "Eng E=5" --person "ML=5" --person "Security reviewer=2")
python3.12 -I $P --plan docs/plans/home-claim-agent.md --tickets docs/tickets/home-claim-agent/ \
  --phase 1 --capacity 1440 --days 60 --reserve 0.25 "${PEOPLE[@]}"
python3.12 -I $P --plan docs/plans/home-claim-agent.md --phase 2 --capacity 960 --days 40 --reserve 0.25 "${PEOPLE[@]}"
python3.12 -I $P --plan docs/plans/home-claim-agent.md --phase "" --capacity 2400 --days 100 --reserve 0.25 "${PEOPLE[@]}"
```

```text
# phase 1, plan + tickets (exit 1: calendar fits low end only; no plan/ticket mismatches)
Phase 1: 24 goals, 620-1052 human hours
Capacity after reserve: 1440 h; fits: yes
  Eng A: 80-134 h of 225 h available
  Eng B: 112-190 h of 225 h available
  Eng C: 84-144 h of 225 h available
  Eng D: 91-152 h of 225 h available
  Eng E: 121-204 h of 225 h available
  ML: 96-164 h of 225 h available
  Security reviewer: 36-64 h of 90 h available
Longest dependent chain (low): G02 -> G16 -> G17 -> G24, 32.87 working days
Longest dependent chain (high): G03 -> G09 -> G10 -> G19 -> G20, 55.73 working days
Finish with these people and dependencies, 25% of each day held in reserve: 36.6-61.53 working days
Calendar: 60 working days; fits: low end only

# phase 2 alone (exit 1: low end only)
Phase 2: 10 goals, 256-430 human hours
Capacity after reserve: 960 h; fits: yes
  Eng A: 36-60 h of 150 h available
  Eng B: 12-20 h of 150 h available
  Eng C: 42-70 h of 150 h available
  Eng D: 40-68 h of 150 h available
  Eng E: 68-112 h of 150 h available
  ML: 58-100 h of 150 h available
Longest dependent chain (low): G28 -> G31 -> G34, 33.8 working days
Longest dependent chain (high): G28 -> G31 -> G34, 48.33 working days
Finish with these people and dependencies, 25% of each day held in reserve: 33.8-48.33 working days
Calendar: 40 working days; fits: low end only

# whole programme to GA (exit 1: low end only)
Phase all: 34 goals, 876-1482 human hours
Capacity after reserve: 2400 h; fits: yes
  Eng A: 116-194 h of 375 h available
  Eng B: 124-210 h of 375 h available
  Eng C: 126-214 h of 375 h available
  Eng D: 131-220 h of 375 h available
  Eng E: 189-316 h of 375 h available
  ML: 154-264 h of 375 h available
  Security reviewer: 36-64 h of 150 h available
Longest dependent chain (low): G03 -> G09 -> G10 -> G19 -> G20 -> G28 -> G31 -> G34, 65.8 working days
Longest dependent chain (high): G03 -> G09 -> G10 -> G19 -> G20 -> G28 -> G31 -> G34, 104.07 working days
Finish with these people and dependencies, 25% of each day held in reserve: 67.47-106.13 working days
Calendar: 100 working days; fits: low end only
```

**Reading the result.** The hours fit with a wide margin, but the calendar
does not at the high end. Phase 1 fits 60 days at the low end only (36.6 to
61.5 days). The whole programme to GA fits 100 days at the low end only (67.5
to 106.1 days), so at the high end GA slips about 6 working days. The phase 2
check on its own overstates the slip, because it does not let the pen test
and the pilot preparation overlap the end of phase 1. The whole-programme
figure is the one to plan against. The critical chain is
G03 → G09 → G10 → G19 → G20 → G28 → G31 → G34: the submission path, the
part-time reviewer's last two passes, the external pen test, the two-week
pilot and the GA decision.

**What moves if work runs high.** In phase 1, G23 (production Guidewire
configuration, dark) moves to the first week of phase 2; nothing on the
floor moves. For GA, the user decides between the options in *Open
decisions*. The recommendation is to raise the reviewer to about 4 h/day in
weeks 8 to 12. That is "add people", which the plan cannot assume on its own.

**Changes made after failing runs**, each true of the work:

1. The first plan put the whole Guidewire submission path into one goal for
   one person (62 to 106 h). It is now two goals with two owners: G09 (the
   confirm binding and operation record) and G10 (the worker and Guidewire
   client). The split adds 6 to 10 h of integration.
2. The security review was one end-of-phase goal for a 2 h/day reviewer. It
   is now three passes that follow the components as they land (G18, G19,
   G20). The split adds 2 to 4 h.
3. G04 no longer carries the CIAM registration wait. G04's work uses a test
   issuer, the registration is requested on day 1, and real CIAM is needed
   only before the staff pilot (G24). The wait was not shortened; it moved
   to where it actually blocks.
4. G07 and G09 depend on G03's trusted-state interface instead of G04. G04's
   denial suite covers every route whenever it lands.
5. G05 is built against a GCS fake, and its live bucket check moved to G16,
   which already depends on G02. G16 depends on G03 instead of G04, because
   staging stays behind staff-only access until G04 lands, and G24 still
   needs G04.
6. The UI was one 58 to 100 h goal. It is now G11 (chat, draft card, upload;
   Eng C) and G12 (confirmation, status, fallback; Eng D); the split adds
   4 to 6 h. G11 now depends on G05, because its upload step uses G05's API.
7. Production Guidewire access was one goal modelled as work then wait. It is
   now G22, a small request filed on day 1, and G23, the configuration after
   the approval. The 10 to 15 day wait is unchanged and simply starts
   earlier.
8. The staging dashboard and alert moved from G17 into G26, phase 2's SLO
   goal. That is scope moved, not dropped. The staff pilot needs spans and
   metrics, not paging.
9. Owners were rebalanced. An exhaustive owner search found no assignment
   whose high-end phase 1 finish is below 61.5 days, so the remaining gap is
   structural and goes to the user as a decision.

## Implementation map

| Decision / requirement | ADK or application component and integration point | GCP service/responsibility | Primary skill (goal) | Verification still needed |
| --- | --- | --- | --- | --- |
| D2, D4: one agent with three tools; the draft is a record | `App` + `LlmAgent` factory in `app/agent/`; the gateway owns the `Runner` and `RunConfig`; tools write through `app/drafts/` | Vertex AI EU endpoint | `adk-workflow-design` (G03), `adk-agent-instructions` (G07) | Pin and interfaces against the chosen ADK version (G03) |
| D5, I1: identity | FastAPI dependency verifies the OIDC JWT (JWKS cached); code writes `customer_id` into session state at creation; owner check on each route | CIAM | `adk-tool-auth-and-secrets` (G04) | CIAM claim names and the customer→policy mapping |
| D3, I2, I3: submission | `POST /drafts/{id}/confirm` → `submission_operation` insert → Cloud Tasks → `claim-submitter` → `app/guidewire/` | Cloud Tasks, Cloud Run, Secret Manager, Cloud NAT static IP | `safe-api-tool-calls` (G09, G10) | Guidewire replay contract (G01) |
| D9: photos | `POST /drafts/{id}/photos` → validate and re-encode → GCS → tool-less reader with `output_schema` → draft | GCS EU bucket, Vertex | `protect-adk-sensitive-data` (G05), `adk-model-and-output-contracts` (G06) | Schema enforcement on Vertex for the pinned model; image token cost |
| D10, I8: sensitive data | Gateway middleware calls SDP before `Runner.run_async` and before persistence; content capture off | SDP (EU location), Cloud Logging EU buckets | `protect-adk-sensitive-data` (G13) | SDP EU location and latency |
| D11, I9: budgets | `RunConfig.max_llm_calls`; allowance table with an atomic update; admission limit; kill-switch config | Cloud SQL | `adk-operational-guardrails` (G15) | Thresholds against A6 |
| D12: browser | SSE text plus JSON cards from Cloud SQL; fallback link | Existing portal hosting | `adk-frontend-integration` (G11, G12) | Portal stack and CSP |
| Security posture | `before_tool_callback` capability checks; adversarial suite with a scripted model | — | `adk-agent-security` (G14, G18 to G20) | — |
| D14: release | `release-manifest.json`, CI gate, Cloud Run revisions | Artifact Registry, CI | `deploy-adk-on-google-cloud` (G16), `adk-release-engineering` (G25) | The CI platform in use |
| D15: telemetry | OTel provider set once per process; span attributes `draft_id`, `operation_id` | Cloud Trace and Monitoring (EU) | `adk-agent-observability` (G17, G26) | Exporter region settings |

## Goals and dependencies

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | State / blocker |
| --- | --- | --- | --- | --- | --- | --- |
| G01 Guidewire FNOL contract | 1 | discovery | 18-30 | — | `safe-api-tool-calls` | ready; wait: sandbox access |
| G02 EU GCP foundations, model residency, prices | 1 | discovery + setup | 26-42 | — | `deploy-adk-on-google-cloud` | ready; wait: projects |
| G03 Walking skeleton | 1 | implementation | 22-38 | — | `adk-workflow-design` | ready |
| G04 Customer identity and ownership | 1 | implementation | 28-46 | G03 | `adk-tool-auth-and-secrets` | proposed |
| G05 Photo upload API | 1 | implementation | 26-44 | G03 | `protect-adk-sensitive-data` | proposed |
| G06 Tool-less photo reader | 1 | implementation | 38-66 | G05 | `adk-model-and-output-contracts` | proposed |
| G07 Claim conversation agent | 1 | implementation | 40-66 | G03 | `adk-agent-instructions` | proposed |
| G08 Evaluation set and runner | 1 | implementation | 58-98 | — | `adk-agent-evaluation` | ready |
| G09 Confirm binding and submission operation | 1 | implementation | 24-40 | G03 | `safe-api-tool-calls` | proposed |
| G10 Submitter worker and Guidewire client | 1 | implementation | 44-76 | G01, G09 | `safe-api-tool-calls` | proposed |
| G11 Portal chat, draft card and photo upload UI | 1 | implementation | 36-62 | G04, G05 | `adk-frontend-integration` | proposed; wait: UX review |
| G12 Confirmation, status and fallback UI | 1 | implementation | 26-44 | G04, G09 | `adk-frontend-integration` | proposed |
| G13 Sensitive-data boundaries and retention | 1 | implementation | 34-56 | G03, G05 | `protect-adk-sensitive-data` | proposed |
| G14 Capability checks and adversarial suite | 1 | implementation | 32-54 | G07, G09 | `adk-agent-security` | proposed |
| G15 Budgets, admission and kill switch | 1 | implementation | 22-38 | G03 | `adk-operational-guardrails` | proposed |
| G16 Staging deployment and release pipeline | 1 | implementation | 42-72 | G02, G03 | `deploy-adk-on-google-cloud` | proposed |
| G17 Telemetry spans and metrics | 1 | implementation | 18-32 | G16 | `adk-agent-observability` | proposed |
| G18 Security review pass 1 | 1 | review | 8-14 | G04, G09 | `adk-agent-security` | proposed |
| G19 Security review pass 2 | 1 | review | 6-10 | G10, G13 | `adk-agent-security` | proposed |
| G20 Security review pass 3 | 1 | review | 6-12 | G14, G18, G19 | `adk-agent-security` | proposed |
| G21 DPIA input package | 1 | discovery | 16-28 | — | `protect-adk-sensitive-data` | ready; wait: DPO |
| G22 Request production Guidewire access | 1 | request | 3-4 | — | `safe-api-tool-calls` | ready; wait: approval |
| G23 Production Guidewire connection (dark) | 1 | implementation | 21-36 | G10, G22 | `safe-api-tool-calls` | proposed |
| G24 Staff pilot on staging | 1 | validation | 26-44 | G04, G06, G08, G10 to G15, G17 | `adk-agent-evaluation` | proposed |
| G25 Production deploy, canary, joint rollback | 2 | implementation | 36-60 | G16, G23, G24 | `adk-release-engineering` | proposed |
| G26 SLOs, alerts, dashboards, on-call and reconciliation runbook | 2 | implementation | 38-62 | G17, G24 | `adk-agent-observability` | proposed |
| G27 Storm load test and admission tuning | 2 | implementation | 30-50 | G25 | `optimise-adk-on-google-cloud` | proposed |
| G28 External pen test and fix triage | 2 | review | 12-20 | G14, G16, G20 | `adk-agent-security` | proposed |
| G29 Accessibility audit and fixes | 2 | implementation | 30-50 | G24 | `adk-frontend-integration` | proposed |
| G30 Launch-language evaluation and localisation | 2 | implementation | 40-70 | G24 | `adk-agent-evaluation` | blocked: A1 |
| G31 Invited-customer pilot | 2 | validation | 24-40 | G21, G25, G28 | `adk-agent-evaluation` | proposed |
| G32 Model Armor layer evaluation | 2 | discovery | 16-28 | G24 | `protect-adk-sensitive-data` | proposed |
| G33 Model lifecycle re-baseline readiness | 2 | implementation | 18-30 | G24 | `adk-release-engineering` | proposed |
| G34 GA go/no-go | 2 | review | 12-20 | G26, G27, G29, G30, G31 | `adk-release-engineering` | proposed |

**Order if time runs short** (each step is still useful): G03 → G07 → G09 →
G10 → G12 gives a working filing journey on a laptop. G04, G08, G13, G14 and
G15 are the floor for any real user and are never cut. G23 moves to phase 2
before any floor goal moves.

**Day-1 requests** (they start calendar waits; owners in brackets):

- Guidewire sandbox (B, G01)
- EU projects and quota (E, G02)
- CIAM staging client (A, G04)
- Production Guidewire access (D, G22)
- DPO slot (security reviewer, G21)
- Pen-test booking (security reviewer, confirmed in G18)
- UX review slot (C, G11)

### Phase 1 goals

Each goal below is also a ticket in `docs/tickets/home-claim-agent/`. The
ticket holds the acceptance checklist; this plan holds the route, the depth
and the skills.

#### G01 — Guidewire FNOL contract (discovery)

- **Phase and estimate:** 1; hands-on 14-24, review 4-6, total 18-30. Wait:
  Guidewire sandbox credentials and docs, 5-10 days, requested on day 1.
  Owner Eng B.
- **Outcome and linked decisions:** D3, I2. Settles the provider facts:
  - the Cloud API calls for creating a draft claim, Homeowners FNOL fields,
    document attachment and submit;
  - the replay or idempotency mechanism and its scope and retention;
  - lookup by an external reference we control;
  - rate limits, error codes and the OAuth client flow.
- **Scope:** recorded sandbox calls; `docs/integration/guidewire-fnol-contract.md`;
  a fake Guidewire spec for G10. No production access.
- **Depth:** production; the floor is no secrets in the note.
- **Implementation route:** a throwaway script outside `app/`; recorded
  responses become G10's fixtures.
- **Prerequisites:** a sandbox client from the Guidewire platform team.
- **Primary skill:** `safe-api-tool-calls`. **Supporting skills:**
  `adk-tool-auth-and-secrets` (client-credential handling).
- **Acceptance:** every question has an answer with evidence or a named gap;
  a duplicate-create experiment shows the replay behaviour; the decision
  between key replay and lookup by external reference is recorded for G10.
- **Verification:** bounded live calls on the sandbox only, ≤ 50 requests.
- **Execution scope:** sandbox only; needs the team's go-ahead and the client.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G01 from docs/plans/home-claim-agent.md. Read docs/architecture/home-claim-agent.md, use the goal's primary and supporting skills, verify its acceptance cases and record evidence here.`

#### G02 — EU GCP foundations, model residency and prices

- **Phase and estimate:** 1; hands-on 20-32, review 6-10, total 26-42. Wait:
  projects and quota, 3-5 days. Owner Eng E.
- **Outcome:** D6, D7, D8, I7.
  - Dev and staging projects in the EU with the `gcp.resourceLocations`
    policy.
  - The region confirmed: is `gemini-3.8-flash` (otherwise `gemini-3.5-flash`)
    served on the Vertex regional endpoint there, and do the data-logging and
    caching settings meet A10?
  - Prices for the model, SDP, Cloud SQL and Tasks, recorded with their date.
  - `gateway-sa` and `submitter-sa` with least privilege; Cloud SQL, the
    bucket, the Tasks queue, empty Secret Manager entries, budget alerts and
    the static egress IP.
  - Whether CMEK is required.
- **Scope:** dev and staging; production in G23 and G25.
- **Depth:** production least privilege; the floor is no keys in files and EU
  only.
- **Implementation route:** Terraform or reviewed `gcloud` runbooks in
  `infra/`, following the landing zone.
- **Primary skill:** `deploy-adk-on-google-cloud`. **Supporting skills:**
  `adk-model-and-output-contracts` (pin choice from the dated lifecycle
  table).
- **Acceptance:** a readback shows every resource in the chosen EU region;
  one regional model call succeeds and a config test rejects the global
  endpoint; the roles of each service account match the design; the
  design's D7 and cost sections are updated with sources and dates.
- **Verification:** authorised live, on the dev project.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G02 from docs/plans/home-claim-agent.md. Read docs/architecture/home-claim-agent.md, use the goal's primary and supporting skills, verify its acceptance cases and record evidence here.`

#### G03 — Walking skeleton

- **Phase and estimate:** 1; hands-on 16-28, review 6-10, total 22-38; no
  wait. Owner Eng D.
- **Outcome:** D2, D4, D8.
  - A local FastAPI gateway owns an ADK `App` and `Runner` with
    `DatabaseSessionService` on Postgres, the pinned model ID from config and
    `RunConfig.max_llm_calls`.
  - The `claim_draft` table has versions and a canonical-payload hash.
  - A trusted-state interface (`customer_id`, `draft_id` written by code)
    with a local-only stub identity.
  - Placeholder tools.
- **Scope:** skeleton and test harness. Real auth is G04; the prompt and
  tools are G07.
- **Depth:** kept code, with the extension points later goals need.
- **Primary skill:** `adk-workflow-design`. **Supporting skills:**
  `adk-model-and-output-contracts` (pinned ID), `adk-memory-architecture`
  (sessions versus the draft record).
- **Acceptance:**
  - **Confirm the ADK pin, and every ADK interface the design names, against
    that pin; record the version.**
  - A scripted conversation writes draft v1 → v2.
  - A process restart returns the same session and draft.
  - No model alias is used.
  - Exceeding `max_llm_calls` ends the turn with the designed error.
- **Verification:** offline plus local integration (Postgres container).
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G03 from docs/plans/home-claim-agent.md. Read docs/architecture/home-claim-agent.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

#### G04 — Customer identity and ownership

- **Phase and estimate:** 1; hands-on 18-30, review 10-16, total 28-46. The
  CIAM staging client is requested on day 1 and needed before G24. Owner
  Eng A.
- **Outcome:** D5, I1.
  - OIDC JWT verification replaces the G03 stub.
  - Owner checks on the session, draft, photo, confirm and status routes.
  - `list_my_policies` reads the authoritative lookup through an adapter
    (a fake and a staging adapter).
- **Primary skill:** `adk-tool-auth-and-secrets`. **Supporting skills:**
  `adk-tool-interface-design` (the `list_my_policies` declaration).
- **Acceptance:**
  - Customer B gets 404 on every resource and route of customer A.
  - A customer ID placed in a message has no effect, because the tools take
    none.
  - An expired or wrong-audience token is rejected.
- **Verification:** offline plus local integration with a test JWKS.
- **Run this goal:** `/adk-engineer Carry out G04 from docs/plans/home-claim-agent.md. Read docs/architecture/home-claim-agent.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

#### G05 — Photo upload API

- **Phase and estimate:** 1; hands-on 18-30, review 8-14, total 26-44. Owner
  Eng C.
- **Outcome:** D9 ingest.
  - Magic-byte check (JPEG, PNG, HEIC); ≤ 15 MB each; ≤ 10 per draft.
  - Re-encode to JPEG without EXIF.
  - Store under `drafts/{draft_id}/` and record on the draft.
  - A 30-day lifecycle rule.
- **Primary skill:** `protect-adk-sensitive-data`. **Supporting skills:** none.
- **Acceptance:**
  - GPS EXIF is absent after upload.
  - A polyglot file, an oversized file and an 11th photo are rejected with an
    actionable message.
  - The object is not public and the owner check applies.
- **Verification:** offline against a GCS fake. The live bucket check runs in
  G16.
- **Run this goal:** `/adk-engineer Carry out G05 from docs/plans/home-claim-agent.md. Read docs/architecture/home-claim-agent.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

#### G06 — Tool-less photo reader

- **Phase and estimate:** 1; hands-on 30-52, review 8-14, total 38-66. Owner
  ML engineer.
- **Outcome:** D9.
  - One model call with no tools and `output_schema=PhotoObservation`,
    including the refusal shape.
  - One repair attempt, then an "unprocessed" outcome.
  - Code writes the observations to the draft.
  - Accuracy measured on 60 to 100 labelled photos, staff-staged and
    licensed.
- **Primary skill:** `adk-model-and-output-contracts`. **Supporting skills:**
  `adk-agent-instructions` (reader instruction), `adk-agent-security` (an
  untrusted image must not steer the output), `adk-agent-evaluation` (photo
  set).
- **Acceptance:**
  - Scripted prose, fenced JSON and wrong-but-valid outputs each produce the
    designed outcome.
  - A photo containing instruction text yields observations only.
  - Agreement with the labels is reported.
  - The captured request shows 0 tools and the schema.
- **Verification:** offline, plus a bounded live run on Vertex EU (≤ 300
  calls).
- **Run this goal:** `/adk-engineer Carry out G06 from docs/plans/home-claim-agent.md. Read docs/architecture/home-claim-agent.md, use the goal's primary and supporting skills, verify its acceptance cases and record evidence here.`

#### G07 — Claim conversation agent

- **Phase and estimate:** 1; hands-on 30-50, review 10-16, total 40-66. Owner
  Eng D.
- **Outcome:** D2, I5, I6.
  - The versioned instruction: Homeowners FNOL facts, safety first, no
    coverage, payout or cost statements, answers in the customer's language.
  - Three tools with bounded results and actionable errors.
  - The emergency flag and the forbidden-commitment check on responses.
- **Primary skill:** `adk-agent-instructions`. **Supporting skills:**
  `adk-tool-interface-design` (three declarations), `adk-agent-evaluation`
  (development cases).
- **Acceptance:**
  - The rendered request shows the versioned instruction, 3 tools, and no
    identity among the model-visible arguments.
  - Field completeness and no-commitment results are reported on the G08
    development set.
  - An emergency message shows the fixed guidance in the same turn.
  - "File it now" produces the confirmation card, not a submission.
- **Run this goal:** `/adk-engineer Carry out G07 from docs/plans/home-claim-agent.md. Read docs/architecture/home-claim-agent.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

#### G08 — Evaluation set and runner

- **Phase and estimate:** 1; hands-on 50-84, review 8-14, total 58-98. Owner
  ML engineer.
- **Outcome:**
  - 80 to 120 labelled conversation cases in the launch language and
    English, with gold FNOL fields. Topics: water, storm, fire, burglary,
    subsidence, out-of-scope motor, coverage questions, emergencies and
    injection photos.
  - A runner with deterministic field checks and a **pinned judge**, chosen
    from the dated lifecycle table.
  - A frozen development/holdout split and a cost ceiling per run.
- **Primary skill:** `adk-agent-evaluation`. **Supporting skills:**
  `adk-model-and-output-contracts` (judge pin), `adk-release-engineering`
  (eval-set hash).
- **Acceptance:**
  - The runner exits non-zero below the threshold; missing results count as
    failures.
  - Judge agreement with two human labellers on 30 cases is reported.
  - The eval-set hash is stable.
- **Run this goal:** `/adk-engineer Carry out G08 from docs/plans/home-claim-agent.md. Read docs/architecture/home-claim-agent.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

#### G09 — Confirm binding and submission operation

- **Phase and estimate:** 1; hands-on 16-26, review 8-14, total 24-40. Owner
  Eng B.
- **Outcome:** D3, I2, I3.
  - `POST /drafts/{id}/confirm` with the displayed `version_hash` and a fresh
    policy check.
  - A unique `submission_operation` created in the same transaction that
    freezes the draft.
  - Cloud Tasks dispatch (a fake in tests) and a status endpoint.
- **Primary skill:** `safe-api-tool-calls`. **Supporting skills:**
  `adk-operational-guardrails` (approval binding).
- **Acceptance:**
  - A double confirm produces one operation.
  - A stale hash returns 409 and dispatches nothing.
  - A scripted model has no route to confirm.
- **Run this goal:** `/adk-engineer Carry out G09 from docs/plans/home-claim-agent.md. Read docs/architecture/home-claim-agent.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

#### G10 — Submitter worker and Guidewire client

- **Phase and estimate:** 1; hands-on 32-56, review 12-20, total 44-76.
  Owner Eng B.
- **Outcome:** I2, I4. A `claim-submitter` worker with a leased state
  machine (`pending → dispatched → created → documents → filed | uncertain |
  rejected`), replay or lookup following G01, per-photo sub-operations, and
  escaped payloads.
- **Primary skill:** `safe-api-tool-calls`. **Supporting skills:**
  `adk-tool-auth-and-secrets` (the Guidewire secret only in
  `submitter-sa`).
- **Acceptance:** against the fake Guidewire:
  - A crash after commit leaves one claim and ends `filed`.
  - A lost response triggers a lookup and no second create.
  - A partial document failure keeps the claim and retries the photos.
  - A stale lease cannot record a result.
  - HTML in the description is escaped.

  Plus one end-to-end sandbox filing.
- **Run this goal:** `/adk-engineer Carry out G10 from docs/plans/home-claim-agent.md. Read docs/architecture/home-claim-agent.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

#### G11 — Portal chat, draft card and photo upload UI

- **Phase and estimate:** 1; hands-on 28-48, review 8-14, total 36-62. Wait:
  UX and brand review, 3-5 days. Owner Eng C.
- **Outcome:** D12. SSE text, the draft card, photo upload with progress, the
  AI disclosure and the emergency banner.
- **Primary skill:** `adk-frontend-integration`. **Supporting skills:** none.
- **Acceptance:**
  - After a disconnect and reload, the saved history and draft are shown.
  - The upload's rejection messages are visible.
  - The emergency banner shows the fixed text.
- **Run this goal:** `/adk-engineer Carry out G11 from docs/plans/home-claim-agent.md. Read docs/architecture/home-claim-agent.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

#### G12 — Confirmation, status and fallback UI

- **Phase and estimate:** 1; hands-on 20-34, review 6-10, total 26-44. Owner
  Eng D.
- **Outcome:** D12, I4, I9. The confirmation card shows the exact summary
  and carries its hash. The status view reads the operation record. The
  form fallback appears on the kill switch or an outage.
- **Primary skill:** `adk-frontend-integration`. **Supporting skills:** none.
- **Acceptance:**
  - "Filed" appears only from the status endpoint.
  - A late error after HTTP 200 shows an error.
  - The kill switch shows the form link.
  - A 409 shows the new summary.
- **Run this goal:** `/adk-engineer Carry out G12 from docs/plans/home-claim-agent.md. Read docs/architecture/home-claim-agent.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

#### G13 — Sensitive-data boundaries and retention

- **Phase and estimate:** 1; hands-on 24-40, review 10-16, total 34-56. Owner
  Eng A.
- **Outcome:** D10, I8, I10. SDP redaction before persistence and before the
  model, failing closed; content capture off; the retention job; an erasure
  endpoint for the DPO process.
- **Primary skill:** `protect-adk-sensitive-data`. **Supporting skills:**
  `adk-agent-observability` (content-capture gates).
- **Acceptance:**
  - Seeded card, IBAN and ID strings are absent from the session DB, spans
    and logs.
  - An SDP outage rejects the message.
  - A 31-day-old draft and its photos are deleted.
  - Erasure waits for an in-flight operation.
- **Run this goal:** `/adk-engineer Carry out G13 from docs/plans/home-claim-agent.md. Read docs/architecture/home-claim-agent.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

#### G14 — Capability checks and adversarial suite

- **Phase and estimate:** 1; hands-on 22-38, review 10-16, total 32-54. Owner
  Eng E.
- **Outcome:** the design's security posture.
  - A `before_tool_callback` that checks the owner and the frozen-draft
    state.
  - The trifecta table confirmed against the code.
  - The adversarial cases as scripted-model tests that assert the forbidden
    effect is absent.
  - Findings mapped to OWASP IDs.
- **Primary skill:** `adk-agent-security`. **Supporting skills:**
  `adk-agent-evaluation` (live adversarial cases added to G08).
- **Acceptance:** every forbidden action is refused at the trusted boundary
  without mutation, and a frozen draft cannot be edited.
- **Run this goal:** `/adk-engineer Carry out G14 from docs/plans/home-claim-agent.md. Read docs/architecture/home-claim-agent.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

#### G15 — Budgets, admission and kill switch

- **Phase and estimate:** 1; hands-on 16-28, review 6-10, total 22-38. Owner
  Eng C.
- **Outcome:** D11, I9.
  - A per-invocation call cap, a 60-call session cap and 3 drafts per
    customer per day, enforced atomically.
  - An admission limit and a kill switch.
  - Confirm and status keep working after model admission stops.
- **Primary skill:** `adk-operational-guardrails`. **Supporting skills:** none.
- **Acceptance:**
  - The 61st call and the 4th draft are refused with the form link.
  - Two concurrent requests cannot both take the last allowance.
  - The kill switch stops new sessions within one config refresh.
- **Run this goal:** `/adk-engineer Carry out G15 from docs/plans/home-claim-agent.md. Read docs/architecture/home-claim-agent.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

#### G16 — Staging deployment and release pipeline

- **Phase and estimate:** 1; hands-on 32-56, review 10-16, total 42-72. Owner
  Eng E.
- **Outcome:** D6, D14.
  - Both services on Cloud Run staging in the EU, behind staff-only access,
    with their service accounts, the Cloud SQL connector, Secret Manager and
    the NAT IP.
  - CI builds the image, runs the offline tests, writes
    `release-manifest.json` and runs the G08 gate once the set exists.
  - A deploy readback, and the live bucket check from G05.
- **Primary skill:** `deploy-adk-on-google-cloud`. **Supporting skills:**
  `adk-release-engineering` (manifest, gate), `adk-agent-observability`
  (the first shared environment).
- **Acceptance:**
  - The readback shows the image digest, model ID, prompt version and secret
    versions on the serving revision.
  - A failing gate blocks the deploy.
  - The previous revision can be restored with one command.
- **Run this goal:** `/adk-engineer Carry out G16 from docs/plans/home-claim-agent.md. Read docs/architecture/home-claim-agent.md, use the goal's primary and supporting skills, verify its acceptance cases and record evidence here.`

#### G17 — Telemetry spans and metrics

- **Phase and estimate:** 1; hands-on 14-24, review 4-8, total 18-32. Owner
  Eng A.
- **Outcome:** D15.
  - One span per agent, tool and model call, carrying `draft_id` and
    `operation_id`.
  - Metrics for T2, duplicates, uncertain age, and tokens and cost per filed
    claim.
  - The dashboard and alert are in G26.
- **Primary skill:** `adk-agent-observability`. **Supporting skills:**
  `protect-adk-sensitive-data` (no content in spans).
- **Acceptance:** an in-memory exporter test shows the expected spans with
  their IDs and no content, and the metrics appear on staging.
- **Run this goal:** `/adk-engineer Carry out G17 from docs/plans/home-claim-agent.md. Read docs/architecture/home-claim-agent.md, use the goal's primary and supporting skills, verify its acceptance cases and record evidence here.`

#### G18 — Security review pass 1: design, identity, confirm binding

- **Phase and estimate:** 1; hands-on 6-10, review 2-4, total 8-14. Owner
  security reviewer.
- **Outcome:** findings on the design, G04 and G09; the pen-test dates
  confirmed for G28.
- **Primary skill:** `adk-agent-security`. **Supporting skills:**
  `adk-tool-auth-and-secrets`.
- **Acceptance:** a findings list with severities, and pen-test booking
  evidence.
- **Run this goal:** `/adk-engineer Carry out G18 from docs/plans/home-claim-agent.md. Read docs/architecture/home-claim-agent.md, use the goal's primary and supporting skills, verify its acceptance cases and record evidence here.`

#### G19 — Security review pass 2: submitter and sensitive data

- **Phase and estimate:** 1; hands-on 4-8, review 2-2, total 6-10. Owner
  security reviewer.
- **Outcome:** findings on G10 and G13.
- **Primary skill:** `adk-agent-security`. **Supporting skills:**
  `protect-adk-sensitive-data`.
- **Acceptance:** a findings list; no secret is readable by `gateway-sa`.
- **Run this goal:** `/adk-engineer Carry out G19 from docs/plans/home-claim-agent.md. Read docs/architecture/home-claim-agent.md, use the goal's primary and supporting skills, verify its acceptance cases and record evidence here.`

#### G20 — Security review pass 3: adversarial suite and pen-test scope

- **Phase and estimate:** 1; hands-on 5-9, review 1-3, total 6-12. Owner
  security reviewer.
- **Outcome:** a review of G14; earlier findings closed or accepted; the
  pen-test scope sent.
- **Primary skill:** `adk-agent-security`. **Supporting skills:** none.
- **Acceptance:** no open high finding before staff use; the scope document
  has been sent.
- **Run this goal:** `/adk-engineer Carry out G20 from docs/plans/home-claim-agent.md. Read docs/architecture/home-claim-agent.md, use the goal's primary and supporting skills, verify its acceptance cases and record evidence here.`

#### G21 — DPIA input package

- **Phase and estimate:** 1; hands-on 12-20, review 4-8, total 16-28. Wait:
  DPO sign-off, 20-30 days. Owner security reviewer. **Submit in weeks 1 to
  2.**
- **Outcome:** A10 to A13. Data flow, processors (Google, Guidewire),
  residency, retention, minimisation and the photo-blurring question, taken
  from the design. The AI Act questions go to legal.
- **Primary skill:** `protect-adk-sensitive-data`. **Supporting skills:** none.
- **Acceptance:** the submission date is recorded, and the DPO's conditions
  become goals or Later items.
- **Run this goal:** `/adk-engineer Carry out G21 from docs/plans/home-claim-agent.md. Read docs/architecture/home-claim-agent.md, use the goal's primary and supporting skills, verify its acceptance cases and record evidence here.`

#### G22 — Request production Guidewire access

- **Phase and estimate:** 1; hands-on 2-3, review 1-1, total 3-4. Wait:
  production change approval and IP allow-list, 10-15 days. Owner Eng D.
  **File on day 1.**
- **Outcome:** a request for a production OAuth client and an IP allow-list.
  The static IP is supplied when G02 reserves it.
- **Primary skill:** `safe-api-tool-calls`. **Supporting skills:** none.
- **Acceptance:** the request reference and date are recorded, and the IP
  amendment has been sent.
- **Run this goal:** `/adk-engineer Carry out G22 from docs/plans/home-claim-agent.md. Read docs/architecture/home-claim-agent.md, use the goal's primary and supporting skills, verify its acceptance cases and record evidence here.`

#### G23 — Production Guidewire connection (dark)

- **Phase and estimate:** 1; hands-on 16-27, review 5-9, total 21-36. Owner
  Eng E.
- **Outcome:** the production client in Secret Manager with rotation
  documented, and a read-only connectivity check. No claims are created and
  no customer traffic reaches it.
- **Primary skill:** `safe-api-tool-calls`. **Supporting skills:**
  `adk-tool-auth-and-secrets` (rotation).
- **Acceptance:** the connectivity check passes from the production project,
  no claim is created, and only `submitter-sa` can read the secret.
- **Run this goal:** `/adk-engineer Carry out G23 from docs/plans/home-claim-agent.md. Read docs/architecture/home-claim-agent.md, use the goal's primary and supporting skills, verify its acceptance cases and record evidence here.`

#### G24 — Staff pilot on staging

- **Phase and estimate:** 1; hands-on 20-34, review 6-10, total 26-44. Owner
  Eng B.
- **Outcome:**
  - About 20 staff file synthetic claims against the Guidewire sandbox.
  - Two adjusters review the created claims.
  - The release candidate passes the G08 gate.
  - Baseline figures from today's form are collected.
- **Primary skill:** `adk-agent-evaluation`. **Supporting skills:**
  `adk-agent-observability` (from traces to cases).
- **Acceptance:** a report covering completion rate, adjuster-judged
  completeness, latency against T1, cost per filed claim and zero
  duplicates, with issues triaged into phase 2. Failing sessions become eval
  cases.
- **Run this goal:** `/adk-engineer Carry out G24 from docs/plans/home-claim-agent.md. Read docs/architecture/home-claim-agent.md, use the goal's primary and supporting skills, verify its acceptance cases and record evidence here.`

### Phase 2 goals (coarser; refine after G24)

- **G25 Production deploy, canary, joint rollback** (`adk-release-engineering`;
  supporting `deploy-adk-on-google-cloud`). Acceptance: the canary
  thresholds are set in advance, and a rehearsed rollback restores the
  image, prompt and model together.
- **G26 SLOs, alerts, dashboards, on-call and reconciliation runbook**
  (`adk-agent-observability`). Includes the staging dashboard and alert
  moved from G17. Acceptance: in a game day the alert reaches on-call and
  leads to the stored session and operation, and the reconciliation runbook
  is rehearsed on an `uncertain` operation.
- **G27 Storm load test and admission tuning** (`optimise-adk-on-google-cloud`).
  Acceptance: under a 10× burst within a cost cap, admission holds, the form
  fallback appears, and Guidewire returns no storm of 429s.
- **G28 External pen test and fix triage** (`adk-agent-security`). Starts
  when staging is feature-complete, which can be before G24 ends.
  Acceptance: no open high or critical finding.
- **G29 Accessibility audit and fixes** (`adk-frontend-integration`).
  Acceptance: a WCAG 2.1 AA audit passes (an assumed requirement).
- **G30 Launch-language evaluation and localisation** (`adk-agent-evaluation`).
  Blocked on A1. Acceptance: the thresholds hold in the launch language.
- **G31 Invited-customer pilot** (`adk-agent-evaluation`). Needs G21 (DPIA)
  and G28. Acceptance: a pilot report against the form baseline, with the
  adjuster correction rate no higher.
- **G32 Model Armor layer evaluation** (`protect-adk-sensitive-data`;
  supporting `adk-agent-security`). Acceptance: the measured extra catch
  rate and latency lead to an adopt or reject decision.
- **G33 Model lifecycle re-baseline readiness** (`adk-release-engineering`;
  supporting `adk-model-and-output-contracts`). Acceptance: the lifecycle
  snapshot is refreshed, a side-by-side on the frozen development set is
  done, and the next retirement date is in the calendar.
- **G34 GA go/no-go** (`adk-release-engineering`). Acceptance: every
  graduation condition has evidence, signed off by claims, legal, the DPO and
  security.

Run any phase 2 goal after refining it here, for example:
`/adk-engineer Carry out G25 from docs/plans/home-claim-agent.md.`

## Later

| Item | Trigger that brings it forward | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| Add photos to, or check the status of, an existing claim in chat | Pilot feedback; call-centre volume | Customers use the portal and phone for follow-ups | `adk-workflow-design` |
| Face and document blurring | A DPIA condition | Adjusters see unblurred photos, as today | `protect-adk-sensitive-data` |
| Damage cost estimation | Adjuster demand and measured accuracy; AI Act review | None; the feature does not exist | `adk-model-and-output-contracts` |
| Second market or more languages | Business decision | — | `adk-agent-evaluation` |
| Multi-region failover | An SLO above 99.5 % | A regional outage sends customers to the form | `deploy-adk-on-google-cloud` |
| Cost and latency tuning | Cost per filed claim or p95 over target | Higher spend | `optimise-adk-on-google-cloud` |
| Historical claim photos in evaluation | The DPIA permits it | A less realistic eval set | `adk-agent-evaluation` |
| Voice channel | Product decision | — | `adk-frontend-integration` |

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| [Design](../architecture/home-claim-agent.md) | Method, guarantees and decisions |
| `evals/SUMMARY.md` (from G08) | Latest result per case, linked to run records |
| This plan | Remaining limits, deferred controls and status |

## Open decisions for further planning

| Decision / question | Known facts and alternatives | Evidence or user decision needed | Blocks which goals? |
| --- | --- | --- | --- |
| GA high-end slip of about 6 working days | (a) Reviewer at about 4 h/day in weeks 8 to 12, **recommended**; (b) a 1-week pilot; (c) GA up to about 2027-03-20 | Product owner and security lead | G18 to G20, G28, G31, G34 |
| Guidewire replay contract | Key replay versus lookup by external reference | G01 sandbox evidence | G10 detail, G23 |
| Model availability in the EU region | 3.8-flash preferred; 3.5-flash as fallback, with a migration before 2027-05-19 | G02 | G06, G07 live runs |
| Launch country and languages | One market assumed | Product owner | G30 |
| Spend cap | €2k/month in phase 1 assumed | Business owner | G15 thresholds |
| AI Act classification | Assumed not high-risk | Legal | G34 |
| CMEK | Assumed not required | Security policy | G02 |
| Profile and cut line | Production; phase 1 ends at the staff pilot | Product owner | — |

## Resume here

- **Next goal:** G03, the walking skeleton. It has no prerequisites and needs
  no cloud access. G01, G02, G08, G21 and G22 are also ready and run in
  parallel by owner. Their day-1 requests start the calendar waits.
- **Read first:** the design, this plan, and `docs/tickets/home-claim-agent/G03-walking-skeleton.md`.
- **Next action:** file the day-1 requests, then Eng D starts G03 locally.
- **Continuation prompt:**

```text
/adk-engineer Carry out G03 from docs/plans/home-claim-agent.md.
Read docs/architecture/home-claim-agent.md and preserve its accepted decisions.
Use adk-workflow-design with adk-model-and-output-contracts and adk-memory-architecture.
Work locally only, verify the G03 acceptance cases, and update
the plan with actual evidence and remaining blockers.
```

After that goal, the same request without a goal ID continues with the next
ready one: `/adk-engineer Continue the next ready goal in docs/plans/home-claim-agent.md.`
