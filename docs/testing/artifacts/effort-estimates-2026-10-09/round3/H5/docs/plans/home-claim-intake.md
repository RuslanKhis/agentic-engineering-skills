# Implementation plan: home-insurance claim intake agent

Status: draft — ready goals identified (phase 1), assumptions unconfirmed
Architecture: [docs/architecture/home-claim-intake.md](../architecture/home-claim-intake.md)
Continuation source of truth: this plan; phase 1 tickets in
[docs/tickets/home-claim-intake/](../tickets/home-claim-intake/) copy its goals.

## Destination and constraints

GA on 2027-03-09 (assumption A1): signed-in German policyholders file a home
FNOL with photos through a chat in the existing portal and receive a
ClaimCenter claim number; the agent never decides cover. Non-goals and
accepted stack: see the design's Purpose and D1–D12. Authorization for this
session: design and plan only; no code, no cloud, no Guidewire calls.

Inherited pins (design D9, D12): agent and photo model `gemini-3.8-flash`
(Vertex AI, EU regional endpoint — unverified, G02); judge `gemini-3.8-flash`
for tone only; google-adk 2.8.0 as working assumption, confirmed in G03.
Prompt version starts at `intake-v1`. A goal that changes one of these is a
release (G17), not a side effect. Inspected repository: only `.claude/skills/`;
every module path below is **proposed**.

Proposed layout: `app/api/` (FastAPI routes, auth middleware),
`app/agent/` (intake agent, tools, instruction), `app/photos/` (upload, analysis
call), `app/drafts/` (draft repository, validator), `app/submission/` (ledger,
worker, Guidewire adapter), `infra/` (Terraform requests to platform team),
`evals/` (cases, runner), `tests/`.

## Delivery profile and capacity

Profile: **production service** (design, Delivery constraints). Phase 1 is an
internal staging slice of it.

Capacity assumptions (A2): engineers and ML engineer 8 h × 0.6 focus = 4.8
focused h/day; security reviewer 8 h × 0.4 × 0.6 ≈ 1.9 h/day. Team new to ADK:
**every estimate below already includes the ×1.5 multiplier**, hands-on and
review alike. First-GCP-project setup is not added (team knows GCP; A2).

| Phase | Delivers | Goals | Human hours, agent-assisted (range) | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship (2026-10-12 → 2026-11-20, 30 working days) | A team member, signed in as a synthetic customer on staging, files a claim with photos and gets a Guidewire **sandbox** claim number; eval baseline; threat model reviewed; DPIA submitted | G01–G13 | 267–418 (schedule check) | 30 days × (6 × 4.8 + 1.9) ≈ 921 h; 25% reserve → **690 h** |
| 2, graduate to pilot and GA (2026-11-23 → 2027-03-05, 67 working days after holidays) | Graduation conditions, closed pilot with real customers, GA readiness | G14–G25 | 332–540 (schedule check) | 67 × 30.7 ≈ 2,057 h; 25% reserve → **1,540 h** |

Phase 1 uses well under half of the reserved capacity. That is deliberate:
the critical path, not hours, sets the date (Guidewire contract → adapter →
sandbox end to end), and new-to-ADK teams meet setup surprises. Spare hours go
first to G25 (UX, accessibility) and G18 (SLOs), which have no phase-1
dependencies beyond G12 — pull them forward rather than adding scope.

Load (from the schedule check, phase 1):

| Person or role | Goals | Hours | Their capacity (30 days) |
| --- | --- | --- | --- |
| Eng A | G01, G06, G12 | 66–101 | 144 |
| Eng B | G03, G10 | 44–70 | 144 |
| Eng C | G04 | 24–38 | 144 |
| Eng D | G05, G11 | 45–70 | 144 |
| Eng E | G08, G09 | 35–57 | 144 |
| ML | G02, G07 | 41–62 | 144 |
| Sec | G13 | 12–20 | 57 |

Schedule block, the single machine-readable source of each estimate:

```yaml
- goal: G01
  phase: 1
  hands_on: 12-18
  review: 2-3
  total: 14-21
  owner: Eng A
  blocked_by: []
  calendar_waits: Guidewire claims-IT workshop and sandbox client
  wait_days: 3-5
- goal: G02
  phase: 1
  hands_on: 5-8
  review: 1-2
  total: 6-10
  owner: ML
  blocked_by: []
  calendar_waits: Vertex AI EU quota request
  wait_days: 0-3
- goal: G03
  phase: 1
  hands_on: 15-24
  review: 6-10
  total: 21-34
  owner: Eng B
  blocked_by: []
  calendar_waits: none
  wait_days: 0
- goal: G04
  phase: 1
  hands_on: 18-28
  review: 6-10
  total: 24-38
  owner: Eng C
  blocked_by: []
  calendar_waits: none
  wait_days: 0
- goal: G05
  phase: 1
  hands_on: 16-24
  review: 6-10
  total: 22-34
  owner: Eng D
  blocked_by: [G02]
  calendar_waits: none
  wait_days: 0
- goal: G06
  phase: 1
  hands_on: 28-42
  review: 12-18
  total: 40-60
  owner: Eng A
  blocked_by: [G01]
  calendar_waits: none
  wait_days: 0
- goal: G07
  phase: 1
  hands_on: 30-44
  review: 5-8
  total: 35-52
  owner: ML
  blocked_by: [G02]
  calendar_waits: none
  wait_days: 0
- goal: G08
  phase: 1
  hands_on: 14-22
  review: 6-10
  total: 20-32
  owner: Eng E
  blocked_by: [G04]
  calendar_waits: none
  wait_days: 0
- goal: G09
  phase: 1
  hands_on: 12-20
  review: 3-5
  total: 15-25
  owner: Eng E
  blocked_by: []
  calendar_waits: DPO workshop scheduling
  wait_days: 2-4
- goal: G10
  phase: 1
  hands_on: 18-28
  review: 5-8
  total: 23-36
  owner: Eng B
  blocked_by: [G03]
  calendar_waits: GCP staging projects and IAM from platform team
  wait_days: 3-5
- goal: G11
  phase: 1
  hands_on: 18-28
  review: 5-8
  total: 23-36
  owner: Eng D
  blocked_by: [G03]
  calendar_waits: none
  wait_days: 0
- goal: G12
  phase: 1
  hands_on: 8-14
  review: 4-6
  total: 12-20
  owner: Eng A
  blocked_by: [G04, G05, G06, G07, G10, G11]
  calendar_waits: none
  wait_days: 0
- goal: G13
  phase: 1
  hands_on: 10-16
  review: 2-4
  total: 12-20
  owner: Sec
  blocked_by: [G08]
  calendar_waits: none
  wait_days: 0
- goal: G14
  phase: 2
  hands_on: 22-36
  review: 8-14
  total: 30-50
  owner: Eng A
  blocked_by: [G12]
  calendar_waits: Guidewire production client and change approval
  wait_days: 5-10
- goal: G15
  phase: 2
  hands_on: 14-24
  review: 6-10
  total: 20-34
  owner: Eng B
  blocked_by: [G12]
  calendar_waits: Customer IAM client registration
  wait_days: 3-5
- goal: G16
  phase: 2
  hands_on: 22-34
  review: 8-14
  total: 30-48
  owner: Eng E
  blocked_by: [G13]
  calendar_waits: none
  wait_days: 0
- goal: G17
  phase: 2
  hands_on: 18-30
  review: 6-10
  total: 24-40
  owner: Eng B
  blocked_by: [G15]
  calendar_waits: none
  wait_days: 0
- goal: G18
  phase: 2
  hands_on: 15-26
  review: 5-8
  total: 20-34
  owner: Eng C
  blocked_by: [G12]
  calendar_waits: none
  wait_days: 0
- goal: G19
  phase: 2
  hands_on: 18-30
  review: 6-10
  total: 24-40
  owner: Eng C
  blocked_by: [G18]
  calendar_waits: none
  wait_days: 0
- goal: G20
  phase: 2
  hands_on: 12-20
  review: 4-8
  total: 16-28
  owner: Eng D
  blocked_by: [G19]
  calendar_waits: none
  wait_days: 0
- goal: G21
  phase: 2
  hands_on: 40-60
  review: 10-16
  total: 50-76
  owner: ML
  blocked_by: [G14, G15, G16, G17, G18]
  calendar_waits: DPIA sign-off and pilot go decision by claims leadership
  wait_days: 5-10
- goal: G22
  phase: 2
  hands_on: 32-52
  review: 8-12
  total: 40-64
  owner: ML
  blocked_by: [G21]
  calendar_waits: none
  wait_days: 0
- goal: G23
  phase: 2
  hands_on: 12-20
  review: 6-10
  total: 18-30
  owner: Sec
  blocked_by: [G15, G16]
  calendar_waits: external penetration test
  wait_days: 10-15
- goal: G24
  phase: 2
  hands_on: 22-34
  review: 8-14
  total: 30-48
  owner: Eng A
  blocked_by: [G17, G20, G21, G23]
  calendar_waits: GA go decision by claims leadership
  wait_days: 2-5
- goal: G25
  phase: 2
  hands_on: 24-38
  review: 6-10
  total: 30-48
  owner: Eng D
  blocked_by: [G12]
  calendar_waits: none
  wait_days: 0
```

Longest dependent chain and finish range: see
[Schedule check results](#schedule-check-results). If phase 1 runs high, the
order that keeps each completed goal useful is G03 → G04 → G06 → G12; G09's
DPIA submission must not slip because its sign-off gates the pilot.

### Schedule check results

Run on 2026-10-09 with `python3.12 -I .claude/skills/adk-system-designer/scripts/check_schedule.py --plan docs/plans/home-claim-intake.md --tickets docs/tickets/home-claim-intake/ --phase <1|2> --capacity <690|1540> --days <30|67>` and `--person` 4.8 h/day for Eng A–E and ML, 1.9 h/day for Sec. Exit status 0 for both phases.

| Phase | Hours | Capacity after reserve | Longest chain (high end) | Finish range | Calendar |
| --- | --- | --- | --- | --- | --- |
| 1 | 267–418 | 690 h, fits | G01 → G06 → G12, 26.0 working days | 16.8–26.0 working days | 30 days, fits |
| 2 | 332–540 | 1,540 h, fits | G14 → G21 → G24, 61.3 working days | 35.9–61.3 working days | 67 days, fits (≈ 6 days margin at the high end) |

**What the check changed.** The first run reported phase 1 "low end only" (high
end 32.4 days): G13 waited for G06, and the part-time reviewer's 12–20 h take
up to 10.5 calendar days. G13 now starts after G08 and reviews G06's design and
work in progress; the re-check of G06's finished code moved into G14. Phase 2
was "low end only" at 74.6 days because GA (G24) waited for the pilot quality
iteration (G22); G22 now runs alongside the rollout and G24 waits for the pilot
(G21) only.

**Cut line (to confirm with the user):** phase 1 = G01–G13, 267–418 of 690 h, an internal
staging end to end on the Guidewire sandbox by 2026-11-20. Phase 2 = G14–G25 to
GA on 2027-03-09. Phase 2's high end leaves only about six working days of
calendar slack, almost all on the Guidewire production client wait (G14) and
the pilot go decision (G21). Start both requests during phase 1. If GA is at
risk, cut G25 to an accessibility audit only, then defer G22's second iteration.
Never cut G16, G17, G19 or G23: they are the floor and the graduation conditions.

## Implementation map

| Decision / requirement | ADK or application component and integration point (proposed) | GCP service/responsibility | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |
| D1 one agent | `app/agent/intake.py`: `LlmAgent` in an `App`, run by the application's `Runner` in `app/api/chat.py` | Vertex AI EU endpoint | `adk-workflow-design` (routing), built in G04 under `adk-tool-interface-design` | ADK 2.8.0 constructors (G03) |
| D2 identity | `app/api/auth.py` middleware verifies OIDC, writes `customer_id` to app-owned state before `Runner.run_async`; tools read it from `tool_context.state` | Customer IAM JWKS | `adk-tool-auth-and-secrets` | IAM token claims (A8) |
| D3 sessions/drafts | `DatabaseSessionService` on Cloud SQL; `app/drafts/repository.py` keyed by `customer_id` | Cloud SQL Postgres EU | `adk-memory-architecture` | Session schema on 2.8.0 |
| D4 browser contract | `app/api/chat.py` SSE events `{type: text_delta|tool_status|draft_updated|turn_complete|error}`; `GET /drafts/{id}/summary`; `GET /submissions/{id}` | Cloud Run | `adk-frontend-integration` | Portal team's widget host |
| D5 submission | `app/submission/ledger.py`, `worker.py`, `guidewire.py` (adapter with fake for tests) | Cloud Tasks, Cloud Run worker, Secret Manager | `safe-api-tool-calls` | Guidewire replay contract (G01) |
| D6 split + checks | `before_tool_callback` in `app/agent/guards.py` comparing tool args to trusted state | — | `adk-agent-security` | Adversarial suite (G08) |
| D7 photos | `app/photos/upload.py` (signed URL, limits, EXIF strip), `app/photos/analyse.py` (`output_schema`, no tools) | GCS EU (CMEK) | `adk-model-and-output-contracts` | Schema enforcement on Vertex EU |
| D8 data protection | Logging filters, OTel content capture off, SDP redaction for eval samples | SDP, Cloud Logging | `protect-adk-sensitive-data` | SDP EU region (G02) |
| D9 model pin | `app/config/release.yaml` manifest | Vertex AI | `adk-model-and-output-contracts` / `adk-release-engineering` | EU availability (G02) |
| D10 budgets | `RunConfig(max_llm_calls=15)`, limits table in Postgres | Billing budget alert | `adk-operational-guardrails` | Limit tests |
| D11 hosting | Two Cloud Run services, separate service accounts | Cloud Run, IAM | `deploy-adk-on-google-cloud` | Platform-team Terraform |

## Goals and dependencies

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | State / blocker |
| --- | --- | --- | --- | --- | --- | --- |
| G01 Guidewire FNOL contract | 1 | discovery | 14–21 | — | `safe-api-tool-calls` | ready (wait: claims IT) |
| G02 EU model and service residency | 1 | discovery | 6–10 | — | `adk-model-and-output-contracts` | ready |
| G03 Authenticated chat skeleton | 1 | implementation | 21–34 | — | `adk-frontend-integration` | ready |
| G04 Intake agent and claim draft | 1 | implementation | 24–38 | — | `adk-tool-interface-design` | ready |
| G05 Photo upload and analysis | 1 | implementation | 22–34 | G02 | `adk-model-and-output-contracts` | ready after G02 (local work can start) |
| G06 Submission ledger and Guidewire adapter | 1 | implementation | 40–60 | G01 | `safe-api-tool-calls` | ready after G01 |
| G07 Evaluation set and baseline | 1 | implementation | 35–52 | G02 | `adk-agent-evaluation` | ready after G02 (labelling can start) |
| G08 Adversarial suite and budgets | 1 | implementation | 20–32 | G04 | `adk-agent-security` | ready after G04 |
| G09 Data map and DPIA input | 1 | implementation | 15–25 | — | `protect-adk-sensitive-data` | ready |
| G10 Staging deployment and telemetry | 1 | implementation | 23–36 | G03 | `deploy-adk-on-google-cloud` | ready after G03 (wait: platform team) |
| G11 Portal chat widget | 1 | implementation | 23–36 | G03 | `adk-frontend-integration` | ready after G03 |
| G12 Staging end to end on Guidewire sandbox | 1 | implementation | 12–20 | G04 G05 G06 G07 G10 G11 | `adk-agent-evaluation` | blocked by dependencies |
| G13 Phase 1 security review | 1 | review | 12–20 | G08 | `adk-agent-security` | blocked by dependencies |
| G14–G25 | 2 | implementation | see schedule | see schedule | see below | proposed |

### G01 — Guidewire FNOL contract (discovery)

- **Phase and estimate:** 1; hands-on 12–18, review 2–3, total 14–21;
  calendar wait: Guidewire claims-IT workshop and sandbox client (3–5 days);
  owner Eng A
- **Outcome and linked decisions:** settles O1 for D5 and I2.
- **Scope:** read the insurer's ClaimCenter Cloud API docs and configuration;
  workshop with claims IT; request a sandbox OAuth client scoped to FNOL
  creation and document upload; record: endpoints for draft claim, documents,
  submit; required fields for a home FNOL (loss cause codes, policy reference,
  address, reporter); replay/idempotency mechanism (header or searchable
  external reference); document size/type limits; rate limits; error shapes;
  maintenance windows. Out: writing the adapter (G06).
- **Depth:** discovery only; no production credentials.
- **Implementation route:** output is `docs/integration/guidewire-fnol-contract.md`
  plus a recorded (secret-free) sandbox request/response set for the G06 fake.
- **Prerequisites:** none; request sandbox client on day 1.
- **Primary skill:** `safe-api-tool-calls`
- **Supporting skills:** `adk-tool-auth-and-secrets` (client-credentials storage and scope)
- **Acceptance:** contract document answers every question above with a source;
  replay behaviour verified by one duplicate sandbox call, or recorded as
  "unsupported → reconcile by external reference"; stopping condition: two
  weeks, then unresolved items go to O1 with an owner.
- **Verification:** reviewed document; bounded sandbox calls (authorised live).
- **Execution scope:** sandbox calls need the claims-IT client; nothing in production.
- **Status and evidence:** planned
- **Run this goal:** `/adk-engineer Carry out G01 from docs/plans/home-claim-intake.md. Read docs/architecture/home-claim-intake.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G02 — EU model and service residency (discovery)

- **Phase and estimate:** 1; hands-on 5–8, review 1–2, total 6–10; wait: Vertex AI EU quota request (0–3 days); owner ML
- **Outcome and linked decisions:** settles O2 for D8, D9.
- **Scope:** confirm `gemini-3.8-flash` on a regional EU Vertex endpoint
  (europe-west3 or europe-west4), multimodal input and `output_schema`
  support there; quotas; dated EU prices; Model Armor and SDP EU locations;
  refresh the lifecycle table date; propose a fallback model if unavailable.
- **Depth:** discovery; one bounded live call per capability.
- **Implementation route:** `docs/integration/model-residency.md`; release manifest draft `app/config/release.yaml`.
- **Prerequisites:** a GCP project the ML engineer may use.
- **Primary skill:** `adk-model-and-output-contracts`
- **Supporting skills:** `protect-adk-sensitive-data` (Model Armor/SDP region facts)
- **Acceptance:** cited sources with dates; one successful EU-regional image+schema call; a named fallback if unavailable.
- **Verification:** authorised live call ≤ 20 requests.
- **Execution scope:** needs a GCP project and Vertex quota; no customer data.
- **Status and evidence:** planned
- **Run this goal:** `/adk-engineer Carry out G02 from docs/plans/home-claim-intake.md. Read docs/architecture/home-claim-intake.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G03 — Authenticated chat skeleton

- **Phase and estimate:** 1; hands-on 15–24, review 6–10, total 21–34; no wait; owner Eng B
- **Outcome and linked decisions:** a signed-in synthetic customer chats with an echo-capable agent; D2, D3, D4, D12, I1, I7.
- **Scope:** repository skeleton, FastAPI app, OIDC verification against a test issuer, `customer_id` into app-owned state, `DatabaseSessionService` on local Postgres, SSE turn endpoint, session ownership on every route, `RunConfig(max_llm_calls=15)`, turn limit. Out: real agent tools (G04), UI (G11).
- **Depth:** production-grade identity scope; staging IAM only.
- **Implementation route:** `app/api/`, `app/config/`; pin `google-adk==2.8.0` and confirm interfaces used against it.
- **Prerequisites:** none.
- **Primary skill:** `adk-frontend-integration`
- **Supporting skills:** `adk-tool-auth-and-secrets` (verified identity → trusted state), `adk-memory-architecture` (session service)
- **Acceptance:** happy path streams a reply; another customer's session ID → 404 with no model call; process restart resumes the session; 16th model call in one invocation is refused; ADK pin confirmed.
- **Verification:** offline pytest with a scripted model; local integration with Postgres and real restart.
- **Execution scope:** local only.
- **Status and evidence:** planned
- **Run this goal:** `/adk-engineer Carry out G03 from docs/plans/home-claim-intake.md. Read docs/architecture/home-claim-intake.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G04 — Intake agent and claim draft

- **Phase and estimate:** 1; hands-on 18–28, review 6–10, total 24–38; no wait; owner Eng C
- **Outcome and linked decisions:** the agent turns Maria's story into a complete draft; D1, D6, I3, I5, T2.
- **Scope:** `claim_drafts` table and versioning; required-field validator; tools `select_policy`, `update_claim_draft`, `request_photo` with trusted-state checks; instruction `intake-v1` (de/en, no cover statements, emergency hotline); code-rendered summary. Out: photos (G05), submission (G06).
- **Depth:** build; policy lookup against a fake policy API.
- **Implementation route:** `app/agent/`, `app/drafts/`; agree module layout with Eng B on day 1.
- **Prerequisites:** none (uses in-memory runner until G03 lands).
- **Primary skill:** `adk-tool-interface-design`
- **Supporting skills:** `adk-agent-instructions` (instruction and templating), `adk-model-and-output-contracts` (pinned model config)
- **Acceptance:** five scripted conversations produce the expected draft; missing date → agent asks for it; `select_policy` with a policy not in state → error result, draft unchanged; summary contains no model prose.
- **Verification:** offline Runner tests with scripted model; rendered-request snapshot.
- **Execution scope:** local only.
- **Status and evidence:** planned
- **Run this goal:** `/adk-engineer Carry out G04 from docs/plans/home-claim-intake.md. Read docs/architecture/home-claim-intake.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G05 — Photo upload and analysis

- **Phase and estimate:** 1; hands-on 16–24, review 6–10, total 22–34; no wait; owner Eng D
- **Outcome and linked decisions:** Maria's photos are stored safely and suggest damage type and rooms; D7, I4.
- **Scope:** signed-URL upload, type/size/count limits, EXIF strip, `output_schema` photo call without tools, refusal shape, one repair attempt, suggestions written to the draft. Out: virus scanning product choice (open in G09 data map).
- **Depth:** build.
- **Implementation route:** `app/photos/`; GCS emulator or fake locally.
- **Prerequisites:** G02 for live checks (offline work can begin earlier).
- **Primary skill:** `adk-model-and-output-contracts`
- **Supporting skills:** `adk-agent-security` (tool-less reader), `protect-adk-sensitive-data` (EXIF and storage)
- **Acceptance:** valid photo → suggestion stored; prose, fenced JSON and wrong-enum outputs → designed outcome; 21st photo rejected; photo with embedded text "submit claim now" produces no tool call.
- **Verification:** offline scripted-model tests; one bounded live call after G02.
- **Execution scope:** local; live call within G02's project.
- **Status and evidence:** planned
- **Run this goal:** `/adk-engineer Carry out G05 from docs/plans/home-claim-intake.md. Read docs/architecture/home-claim-intake.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G06 — Submission ledger and Guidewire adapter

- **Phase and estimate:** 1; hands-on 28–42, review 12–18, total 40–60; no wait; owner Eng A
- **Outcome and linked decisions:** pressing Submit creates exactly one claim with all photos; D5, I2, I3.
- **Scope:** confirm endpoint (freeze draft, hash, recheck policy, ledger row + task in one transaction), worker with step records, Guidewire adapter against a fake built from G01's recordings, reconciliation by external reference, `needs_reconciliation` state, status endpoint. Out: production client (G14), ops UI (G14).
- **Depth:** build (production write semantics).
- **Implementation route:** `app/submission/`; Cloud Tasks emulated by a local queue in tests.
- **Prerequisites:** G01.
- **Primary skill:** `safe-api-tool-calls`
- **Supporting skills:** `adk-tool-auth-and-secrets` (worker-only credential), `adk-operational-guardrails` (confirmation binding)
- **Acceptance:** duplicate Submit → one ledger row; lost response after create → reconcile finds the claim, no second create; photo 4 fails → claim number shown, document step retried; edit after confirm → new confirmation required; chat-api service account cannot read the Guidewire secret.
- **Verification:** offline failure matrix against the fake; local integration with Postgres and worker restart.
- **Execution scope:** local; sandbox only in G12.
- **Status and evidence:** planned
- **Run this goal:** `/adk-engineer Carry out G06 from docs/plans/home-claim-intake.md. Read docs/architecture/home-claim-intake.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G07 — Evaluation set and baseline

- **Phase and estimate:** 1; hands-on 30–44, review 5–8, total 35–52; no wait; owner ML
- **Outcome and linked decisions:** quality is measured before the pilot; I5, T2, D9.
- **Scope:** 50 synthetic German/English conversations (persona simulations reviewed by a claims handler), 60 labelled damage photos (licensed or staff-taken, no customers), metrics: required-field accuracy, cause-code accuracy, turns to complete, coverage-promise rate, photo damage-type accuracy; baseline run on the pinned model. Out: CI gate (G17).
- **Depth:** build; synthetic data only.
- **Implementation route:** `evals/`; deterministic scorers; judge only for tone.
- **Prerequisites:** G02; claims handler time for review (part of hands-on).
- **Primary skill:** `adk-agent-evaluation`
- **Supporting skills:** `adk-model-and-output-contracts` (judge pin)
- **Acceptance:** eval set versioned with hash; baseline report with per-metric results and failed/missing cases; coverage-promise rate reported.
- **Verification:** offline scorer tests; bounded live run within budget.
- **Execution scope:** G02 project; no customer data.
- **Status and evidence:** planned
- **Run this goal:** `/adk-engineer Carry out G07 from docs/plans/home-claim-intake.md. Read docs/architecture/home-claim-intake.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G08 — Adversarial suite and budgets

- **Phase and estimate:** 1; hands-on 14–22, review 6–10, total 20–32; no wait; owner Eng E
- **Outcome and linked decisions:** I4 and I7 are tested; D6, D10.
- **Scope:** trifecta table, `before_tool_callback` capability checks, scripted-model adversarial cases listed in the design, per-session photo/turn and per-customer daily limits. Out: pen test (G23), surge admission (G19).
- **Depth:** build.
- **Implementation route:** `app/agent/guards.py`, `tests/adversarial/`.
- **Prerequisites:** G04.
- **Primary skill:** `adk-agent-security`
- **Supporting skills:** `adk-operational-guardrails` (limits)
- **Acceptance:** every adversarial case asserts the forbidden call never ran and no foreign data appears; 4th session for a customer in a day → refusal with web-form link.
- **Verification:** offline.
- **Execution scope:** local.
- **Status and evidence:** planned
- **Run this goal:** `/adk-engineer Carry out G08 from docs/plans/home-claim-intake.md. Read docs/architecture/home-claim-intake.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G09 — Data map and DPIA input

- **Phase and estimate:** 1; hands-on 12–20, review 3–5, total 15–25; wait: DPO workshop scheduling (2–4 days); owner Eng E
- **Outcome and linked decisions:** D8, O4, O5 submitted to the DPO.
- **Scope:** data map across ingress, model context, tools, session events, photos, ledger, logs, traces; content-capture policy; retention proposal; DPIA technical annex; AI-interaction disclosure text proposal. Out: building screening and erasure (G16).
- **Depth:** build documents; minimal code (logging filter spec).
- **Implementation route:** `docs/compliance/data-map.md`.
- **Prerequisites:** none.
- **Primary skill:** `protect-adk-sensitive-data`
- **Supporting skills:** `adk-agent-observability` (content-capture gates)
- **Acceptance:** DPIA annex submitted with every data class owned; open retention questions logged.
- **Verification:** DPO receipt.
- **Execution scope:** documents only.
- **Status and evidence:** planned
- **Run this goal:** `/adk-engineer Carry out G09 from docs/plans/home-claim-intake.md. Read docs/architecture/home-claim-intake.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G10 — Staging deployment and telemetry

- **Phase and estimate:** 1; hands-on 18–28, review 5–8, total 23–36; wait: GCP staging projects and IAM from platform team (3–5 days); owner Eng B
- **Outcome and linked decisions:** D11, I6, release manifest.
- **Scope:** two Cloud Run services in europe-west3 with separate service accounts, Cloud SQL, Cloud Tasks, GCS, Secret Manager; OTel traces with content capture off; release manifest; deterministic tests in CI. Out: eval gate and canary (G17), SLOs (G18).
- **Depth:** build for staging.
- **Implementation route:** `infra/` Terraform requests; `Dockerfile`; CI config.
- **Prerequisites:** G03.
- **Primary skill:** `deploy-adk-on-google-cloud`
- **Supporting skills:** `adk-agent-observability` (exporter, no content), `adk-release-engineering` (manifest)
- **Acceptance:** deployed revision readback matches the manifest; exporter test shows one span per agent/tool/model call and no content; chat-api SA denied on the Guidewire secret.
- **Verification:** offline exporter test; authorised staging deployment.
- **Execution scope:** staging projects only, after platform team grants.
- **Status and evidence:** planned
- **Run this goal:** `/adk-engineer Carry out G10 from docs/plans/home-claim-intake.md. Read docs/architecture/home-claim-intake.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G11 — Portal chat widget

- **Phase and estimate:** 1; hands-on 18–28, review 5–8, total 23–36; no wait; owner Eng D
- **Outcome and linked decisions:** D4; Maria uses the journey in a browser.
- **Scope:** widget with streaming text, photo upload, code-rendered summary and Submit, status view, emergency banner, AI disclosure. Out: accessibility audit and mobile polish (G25).
- **Depth:** build on staging portal.
- **Implementation route:** portal repository (to locate) or a staging host page.
- **Prerequisites:** G03.
- **Primary skill:** `adk-frontend-integration`
- **Supporting skills:** none
- **Acceptance:** browser test shows incremental text; summary matches the draft; a failed turn shows an error, not a stale answer.
- **Verification:** local browser test against G03.
- **Execution scope:** local and staging.
- **Status and evidence:** planned
- **Run this goal:** `/adk-engineer Carry out G11 from docs/plans/home-claim-intake.md. Read docs/architecture/home-claim-intake.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G12 — Staging end to end on Guidewire sandbox

- **Phase and estimate:** 1; hands-on 8–14, review 4–6, total 12–20; no wait; owner Eng A
- **Outcome and linked decisions:** phase 1 "done".
- **Scope:** run the journey on staging against the sandbox; run G07's eval set against staging; replay check of I2 on the sandbox. Out: production (G14).
- **Depth:** build.
- **Implementation route:** staging configuration; sandbox client from G01.
- **Prerequisites:** G04, G05, G06, G07, G10, G11.
- **Primary skill:** `adk-agent-evaluation`
- **Supporting skills:** `safe-api-tool-calls` (sandbox replay check)
- **Acceptance:** sandbox claim number returned with six documents; duplicate submit creates nothing new; eval results on staging within tolerance of G07 baseline.
- **Verification:** authorised live, staging and sandbox only.
- **Execution scope:** staging + sandbox.
- **Status and evidence:** planned
- **Run this goal:** `/adk-engineer Carry out G12 from docs/plans/home-claim-intake.md. Read docs/architecture/home-claim-intake.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G13 — Phase 1 security review

- **Phase and estimate:** 1; hands-on 10–16, review 2–4, total 12–20; no wait; owner Sec
- **Outcome and linked decisions:** independent review of D2, D5, D6, I1–I4.
- **Scope:** review threat model, adversarial suite, service-account grant plan, and the submission ledger design (G01 contract plus G06 work in progress); findings with OWASP IDs. Out: pen test (G23); the re-check of G06's finished code is an acceptance item of G14 (moved by the schedule check, see cut line).
- **Depth:** build.
- **Implementation route:** `docs/security/phase1-review.md`.
- **Prerequisites:** G08.
- **Primary skill:** `adk-agent-security`
- **Supporting skills:** `adk-tool-auth-and-secrets` (grant review)
- **Acceptance:** findings list with severity; no open critical before the pilot.
- **Verification:** reviewer sign-off.
- **Execution scope:** read-only review.
- **Status and evidence:** planned
- **Run this goal:** `/adk-engineer Carry out G13 from docs/plans/home-claim-intake.md. Read docs/architecture/home-claim-intake.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### Phase 2 goals (coarser; refine after G12)

| ID | Goal | Primary skill | Supporting | One observable acceptance check |
| --- | --- | --- | --- | --- |
| G14 | Production Guidewire connection, reconciliation runbook and ops queue; security reviewer re-checks G06's finished write path | `safe-api-tool-calls` | `adk-tool-auth-and-secrets` | A forced uncertain submission appears in the ops queue and is resolved without a duplicate claim; reviewer sign-off on the write path |
| G15 | Production customer IAM and session security | `adk-tool-auth-and-secrets` | `adk-frontend-integration` | Cross-customer denial tests pass against production IAM tokens |
| G16 | Screening (Model Armor/SDP), retention and erasure jobs | `protect-adk-sensitive-data` | `adk-memory-architecture` | Erasure of a test customer removes sessions, drafts and photos; screening outage has the designed outcome |
| G17 | Eval gate in CI, release manifest, canary and joint rollback | `adk-release-engineering` | `adk-agent-evaluation` | A regressed prompt fails CI by exit code; rollback restores image + prompt + model together |
| G18 | SLOs, alerts, dashboards, on-call runbook | `adk-agent-observability` | — | A synthetic failure burns error budget and pages; the alert links to the session |
| G19 | Surge admission, per-customer allowance, degrade to web form | `adk-operational-guardrails` | — | Above the admission limit, new sessions see the web-form link; existing sessions continue |
| G20 | Load and cost test at storm peak | `optimise-adk-on-google-cloud` | `adk-agent-observability` | 60 concurrent sessions meet T1 provisional targets; cost per claim recorded |
| G21 | Closed pilot with real customers | `adk-agent-evaluation` | `adk-agent-observability` | ≥ 100 pilot claims; handler call-back rate compared with O3 baseline |
| G22 | Quality iteration from pilot error analysis (runs alongside the GA rollout; not a GA blocker) | `adk-agent-evaluation` | `adk-agent-instructions` | Re-measured dev set improves on the top two error classes without regression |
| G23 | External penetration test and security sign-off | `adk-agent-security` | — | No open critical/high findings |
| G24 | GA production rollout, DR and rollback rehearsal | `deploy-adk-on-google-cloud` | `adk-release-engineering` | Rollback rehearsal completes with in-flight submissions intact |
| G25 | Accessibility (WCAG 2.1 AA) and mobile-web polish | `adk-frontend-integration` | — | Accessibility audit passes on the claim journey |

Each phase-2 goal runs with `/adk-engineer Carry out <ID> from docs/plans/home-claim-intake.md.` once phase 1 evidence has refined it.

## Later

| Item | Trigger that brings it forward | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| Further markets and languages | Business decision on a second country | German/English only | `adk-agent-instructions` |
| Claim status questions for existing claims | Customer demand in pilot transcripts | Customers use existing status page | `adk-tool-interface-design` |
| Damage estimation / repair-partner triage | Business case and labelled data | Handlers estimate | `adk-agent-evaluation` |
| Native app and voice | Portal roadmap | Web only | `adk-frontend-integration` |
| Multi-region failover | Availability target above 99.5% | Region outage → web form | `deploy-adk-on-google-cloud` |
| Model migration | `gemini-3.8-flash` retirement announced | — | `adk-release-engineering` |

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| [design](../architecture/home-claim-intake.md) | Method and decisions (draft) |
| `evals/README.md` (G07, not yet written) | Latest result per case |
| this plan | Remaining limits and deferred controls |

## Open decisions for further planning

| Decision / question | Known facts and alternatives | Evidence or user decision needed | Blocks which goals? |
| --- | --- | --- | --- |
| Guidewire replay contract (O1) | Replay header vs search by external reference vs manual | G01 | G06 final shape, G12 |
| EU model availability (O2) | `gemini-3.8-flash` preferred; fallback `gemini-3.5-flash` (retirement ≥ 2027-05-19) | G02 | G05/G07 live runs |
| Baseline metrics (O3) | None known | Claims operations | G21 success criteria |
| AI Act classification and disclosure (O4) | Assumed not high-risk | Legal | G11 copy, G21 |
| Retention periods (O5) | A12 assumed | DPO | G16 |
| Assumptions A1–A18 and the cut line | See design | User | All provisional decisions |

## Resume here

- **Next goal:** G01 Guidewire FNOL contract — it has no prerequisites, holds
  the longest calendar wait and sits on the critical path. G02, G03, G04 and
  G09 are also ready and can start the same day with other owners.
- **Read first:** the design, this plan, `docs/tickets/home-claim-intake/G01-guidewire-fnol-contract.md`.
- **Next action:** request the Guidewire sandbox OAuth client and the claims-IT workshop.
- **Continuation prompt:**

```text
/adk-engineer Carry out G01 from docs/plans/home-claim-intake.md.
Read docs/architecture/home-claim-intake.md and preserve its accepted decisions.
Use safe-api-tool-calls with adk-tool-auth-and-secrets.
Work within the Guidewire sandbox only, verify the contract questions and the
replay check, and update the plan with actual evidence and remaining blockers.
```

After that goal, the same request without a goal ID continues with the next
ready one: `/adk-engineer Continue the next ready goal in docs/plans/home-claim-intake.md.`
