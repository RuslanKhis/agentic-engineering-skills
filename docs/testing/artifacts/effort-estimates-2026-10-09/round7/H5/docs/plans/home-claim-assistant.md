# Implementation plan: home-insurance claim assistant

Status: draft — ready goals identified, nothing implemented
Architecture: [../architecture/home-claim-assistant.md](../architecture/home-claim-assistant.md)
Continuation source of truth: this plan; each phase 1 goal's scope and
acceptance live in its ticket under
[../tickets/home-claim-assistant/](../tickets/home-claim-assistant/).

## Summary for the reader

- **Profile and phase 1:** production service. Phase 1 takes the assistant
  from nothing to general availability for German home-insurance customers:
  chat in the portal, photos, confirmed and idempotent FNOL creation in
  ClaimCenter, security and data controls, an employee pilot and a two-week
  controlled beta (G01–G27).
- **Effort and finish:** 775–1,222 human hours, agent-assisted, against
  2,793 hours of team capacity after a 25 % reserve — hours fit easily. The
  calendar does not: with the security reviewer at 2 hours a day (A5) the
  finish is **67–100 working days against 98**, so it fits at the low end
  only. It is limited by the chain of dependent goals and calendar waits,
  not by hours. Two tested remedies close the gap (see the what-if table):
  the security reviewer at **4 hours a day** (finish 73–94 days), or GA on
  **Tue 2027-03-17** instead of Mon 2027-03-15. Cutting the photo-analysis
  goal does not move the finish.
- **Largest risks:**
  1. Guidewire contract and sandbox access (O2, W1) — the duplicate-claim
     guarantee depends on a searchable external reference; mitigated by
     building against a fake from the documented contract (G09) and
     confirming on the sandbox later (G10). Owner Eng B.
  2. Security review capacity and pen-test timing (W3, G23) — on the longest
     chain. Book the pen test this week; owner Sec Reviewer.
  3. DPIA sign-off before real customers (W2) — start it now from the design;
     owner DPO via the product owner.
- **Decisions needed from you:** O7 (which remedy: reviewer hours or a
  two-day GA slip), O3 (spend ceiling), confirm A1–A15 in the design,
  especially A1 (one market), A3 (Guidewire Cloud API), A9 (no staff review
  before claim creation).
- **Next prompt:** `/adk-engineer Carry out docs/tickets/home-claim-assistant/G01-guidewire-fnol-contract.md.`
  (G01 and G02 are both ready and independent; start both on day 1.)

## Destination and constraints

Destination: the GA described in the design's journey and guarantees I1–I10.
Non-goals and accepted stack: design sections "Purpose and constraints" and
D1–D15. Authorisation in this session: design only — no code, dependencies,
cloud resources or IAM changes. Inspected repository: empty apart from
`.claude/skills/`; every module below is proposed. Pinned versions the goals
inherit (design "Versions"): `google-adk` 2.8.0 as a working assumption to be
confirmed in G02; model and judge `gemini-3.8-flash` (provisional, O1);
prompt version starts at `intake-v1` / `reader-v1`. A goal that changes any
of them is a release (G20), not a side effect.

## Delivery profile and capacity

| Phase | Delivers | Goals | Human hours, agent-assisted | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship | GA for one market | G01–G27 (+ waits W1–W6) | 775–1,222 | 6 people × 6 h × 98 days, plus reviewer 2 h × 98 days, 25 % held back = 2,793 h |
| 2, harden and extend | Call-centre handoff, second market, status queries, migration and tuning | G28–G33 | 188–308 | After GA, when the team has time |

Estimates are person-hours of human effort with a coding agent (hands-on plus
review and verify) for a team new to ADK: the ×1.5 multiplier is already in
every figure. Review is sized to the change: heavier on G04, G09, G11, G15,
G17 (authorisation, writes, data, security), lighter on G01, G02, G12, G13.
Calendar waits are their own entries (W1–W6, no owner, requested on day 1)
and are not hours. Pilot and beta observation windows sit on G25 and G27.

| Person or role | Goals | Hours | Capacity after reserve |
| --- | --- | --- | --- |
| Eng A (API) | G04, G07, G11, G22 | 108–170 | 441 |
| Eng B (Guidewire) | G01, G09, G10, G19, G27 | 134–208 | 441 |
| Eng C (agent) | G02, G06, G17, G18, G24 | 121–198 | 441 |
| Eng D (portal) | G05, G12, G20, G25 | 148–230 | 441 |
| Eng E (platform) | G03, G15, G21, G26 | 136–212 | 441 |
| ML Eng | G08, G13, G14 | 104–164 | 441 |
| Sec Reviewer | G16, G23 | 24–40 | 147 |

Spare hours are large on purpose: they absorb integration debugging, review
findings and help across goals. They do not shorten the chain; only the
remedies below do.

Schedule block (the single source of each estimate; tickets copy it):

```yaml
- goal: W1
  phase: 1
  total: 0
  blocked_by: []
  calendar_waits: Guidewire sandbox tenant and API client
  wait_days: 15-25
- goal: W2
  phase: 1
  total: 0
  blocked_by: []
  calendar_waits: DPIA sign-off by DPO
  wait_days: 30-45
- goal: W3
  phase: 1
  total: 0
  blocked_by: []
  calendar_waits: external pen-test slot booked
  wait_days: 25-40
- goal: W4
  phase: 1
  total: 0
  blocked_by: []
  calendar_waits: EU GCP projects and org policy from platform team
  wait_days: 5-10
- goal: W5
  phase: 1
  total: 0
  blocked_by: []
  calendar_waits: portal CIAM client and release-train slot
  wait_days: 10-15
- goal: W6
  phase: 1
  total: 0
  blocked_by: []
  calendar_waits: Vertex AI EU quota increase
  wait_days: 5-15
- goal: G01
  phase: 1
  hands_on: 10-16
  review: 2-4
  total: 12-20
  owner: Eng B
  blocked_by: []
  calendar_waits: none
  wait_days: 0
- goal: G02
  phase: 1
  hands_on: 10-16
  review: 3-6
  total: 13-22
  owner: Eng C
  blocked_by: []
  calendar_waits: none
  wait_days: 0
- goal: G03
  phase: 1
  hands_on: 32-50
  review: 8-14
  total: 40-64
  owner: Eng E
  blocked_by: [W4, G02]
  calendar_waits: see W4
  wait_days: 0
- goal: G04
  phase: 1
  hands_on: 20-32
  review: 10-16
  total: 30-48
  owner: Eng A
  blocked_by: [G02]
  calendar_waits: none
  wait_days: 0
- goal: G05
  phase: 1
  hands_on: 18-28
  review: 6-10
  total: 24-38
  owner: Eng D
  blocked_by: [G01, G02]
  calendar_waits: none
  wait_days: 0
- goal: G06
  phase: 1
  hands_on: 26-40
  review: 8-14
  total: 34-54
  owner: Eng C
  blocked_by: [G02, G05]
  calendar_waits: none
  wait_days: 0
- goal: G07
  phase: 1
  hands_on: 12-18
  review: 4-8
  total: 16-26
  owner: Eng A
  blocked_by: [G04, G05]
  calendar_waits: none
  wait_days: 0
- goal: G08
  phase: 1
  hands_on: 18-28
  review: 6-10
  total: 24-38
  owner: ML Eng
  blocked_by: [G02, G05]
  calendar_waits: none
  wait_days: 0
- goal: G09
  phase: 1
  hands_on: 30-46
  review: 12-18
  total: 42-64
  owner: Eng B
  blocked_by: [G01, G05]
  calendar_waits: none
  wait_days: 0
- goal: G10
  phase: 1
  hands_on: 14-22
  review: 4-6
  total: 18-28
  owner: Eng B
  blocked_by: [G09, W1]
  calendar_waits: see W1
  wait_days: 0
- goal: G11
  phase: 1
  hands_on: 28-42
  review: 12-18
  total: 40-60
  owner: Eng A
  blocked_by: [G06, G07, G08, G09]
  calendar_waits: none
  wait_days: 0
- goal: G12
  phase: 1
  hands_on: 52-80
  review: 10-16
  total: 62-96
  owner: Eng D
  blocked_by: [G04, W5]
  calendar_waits: see W5
  wait_days: 0
- goal: G13
  phase: 1
  hands_on: 50-76
  review: 8-12
  total: 58-88
  owner: ML Eng
  blocked_by: [G05]
  calendar_waits: none
  wait_days: 0
- goal: G14
  phase: 1
  hands_on: 18-30
  review: 4-8
  total: 22-38
  owner: ML Eng
  blocked_by: [G06, G07, G08, G13]
  calendar_waits: none
  wait_days: 0
- goal: G15
  phase: 1
  hands_on: 28-42
  review: 10-16
  total: 38-58
  owner: Eng E
  blocked_by: [G03, G06, G07, G08]
  calendar_waits: none
  wait_days: 0
- goal: G16
  phase: 1
  hands_on: 8-12
  review: 2-4
  total: 10-16
  owner: Sec Reviewer
  blocked_by: []
  calendar_waits: none
  wait_days: 0
- goal: G17
  phase: 1
  hands_on: 24-36
  review: 8-14
  total: 32-50
  owner: Eng C
  blocked_by: [G06, G07, G08, G16]
  calendar_waits: none
  wait_days: 0
- goal: G18
  phase: 1
  hands_on: 18-28
  review: 6-10
  total: 24-38
  owner: Eng C
  blocked_by: [G06, G07, G08]
  calendar_waits: none
  wait_days: 0
- goal: G19
  phase: 1
  hands_on: 26-40
  review: 6-10
  total: 32-50
  owner: Eng B
  blocked_by: [G03, G11]
  calendar_waits: none
  wait_days: 0
- goal: G20
  phase: 1
  hands_on: 26-40
  review: 6-10
  total: 32-50
  owner: Eng D
  blocked_by: [G03, G13]
  calendar_waits: none
  wait_days: 0
- goal: G21
  phase: 1
  hands_on: 30-46
  review: 8-12
  total: 38-58
  owner: Eng E
  blocked_by: [G03, G15]
  calendar_waits: none
  wait_days: 0
- goal: G22
  phase: 1
  hands_on: 18-28
  review: 4-8
  total: 22-36
  owner: Eng A
  blocked_by: [G18, G21, W6]
  calendar_waits: see W6
  wait_days: 0
- goal: G23
  phase: 1
  hands_on: 12-20
  review: 2-4
  total: 14-24
  owner: Sec Reviewer
  blocked_by: [G10, G11, G15, G17, W3]
  calendar_waits: pen-test window
  wait_days: 10-15
- goal: G24
  phase: 1
  hands_on: 14-26
  review: 4-8
  total: 18-34
  owner: Eng C
  blocked_by: [G23]
  calendar_waits: none
  wait_days: 0
- goal: G25
  phase: 1
  hands_on: 24-36
  review: 6-10
  total: 30-46
  owner: Eng D
  blocked_by: [G10, G12, G14, G19, G21]
  calendar_waits: two-week employee pilot
  wait_days: 10
- goal: G26
  phase: 1
  hands_on: 16-24
  review: 4-8
  total: 20-32
  owner: Eng E
  blocked_by: [G19, G21]
  calendar_waits: none
  wait_days: 0
- goal: G27
  phase: 1
  hands_on: 24-36
  review: 6-10
  total: 30-46
  owner: Eng B
  blocked_by: [G20, G22, G24, G25, G26, W2]
  calendar_waits: two-week controlled beta
  wait_days: 10
- goal: G28
  phase: 2
  hands_on: 30-48
  review: 10-16
  total: 40-64
  blocked_by: [G27]
  calendar_waits: none
  wait_days: 0
- goal: G29
  phase: 2
  hands_on: 38-64
  review: 10-16
  total: 48-80
  blocked_by: [G27]
  calendar_waits: none
  wait_days: 0
- goal: G30
  phase: 2
  hands_on: 16-24
  review: 4-8
  total: 20-32
  blocked_by: [G27]
  calendar_waits: none
  wait_days: 0
- goal: G31
  phase: 2
  hands_on: 12-20
  review: 4-8
  total: 16-28
  blocked_by: [G20]
  calendar_waits: none
  wait_days: 0
- goal: G32
  phase: 2
  hands_on: 30-48
  review: 10-16
  total: 40-64
  blocked_by: [G27]
  calendar_waits: none
  wait_days: 0
- goal: G33
  phase: 2
  hands_on: 18-30
  review: 6-10
  total: 24-40
  blocked_by: [G25]
  calendar_waits: none
  wait_days: 0
```

**Schedule check** (run 2026-10-14 with Python 3.12, standard library only):

```bash
python3 .claude/skills/adk-system-designer/scripts/check_schedule.py \
  --plan docs/plans/home-claim-assistant.md --tickets docs/tickets/home-claim-assistant/ \
  --days 98 --reserve 0.25 --person "Eng A=6" --person "Eng B=6" --person "Eng C=6" \
  --person "Eng D=6" --person "Eng E=6" --person "ML Eng=6" --person "Sec Reviewer=2"
```

Result: phase 1, 33 entries, 775–1,222 h; capacity 2,793 h, fits; longest
chain (low) G02 → G05 → G09 → G11 → G19 → G25 → G27, 66.89 days; longest
chain (high) G02 → G05 → G09 → G11 → G23 → G24 → G27, 99.67 days; finish
66.89–99.67 working days; calendar 98 days, **fits: low end only** (exit 1).
With `--tickets`, the helper found no ticket that disagrees with the plan.

What-if runs (same command, one change each):

| Change | Finish (working days) | Fits 98 days? |
| --- | --- | --- |
| None (baseline above) | 66.89–99.67 | Low end only |
| Security reviewer 4 h/day | 72.89–93.56 | **Yes** |
| GA moved to Tue 2027-03-17 (`--days 100`) | 66.89–99.67 | **Yes** |
| Cut G08 photo analysis (photos still attached) | 66.89–99.67 | Low end only — no help |

Changes made after earlier failing runs, each true of the work:

| Change | Why it is true |
| --- | --- |
| Guidewire work split into adapter against a documented-contract fake (G09) and sandbox verification (G10, after W1) | The adapter's logic does not need the sandbox; only its confirmation does |
| Intake agent (G06) no longer waits for the authenticated API (G04) | The agent reads `customer_id` from session state; tests set it directly |
| Photo upload (G07, Eng A) split from photo analysis (G08, ML Eng) | Different skills and owners; the reader needs only a stored image |
| Submission adversarial cases moved into G11's acceptance; G17 covers the readers | The forbidden-submit tests belong where the submit route is built |
| Production infrastructure (G21) starts after data controls (G15), not after the submit flow | Backups, HA and the restore drill do not need the submit feature; G26 reruns the drill on the release candidate |
| Draft store (G05) given to Eng D, who waits on W5 at the start | Ownership only; no dependency removed |
| Pilot and beta windows fixed at 10 working days with exit criteria (G25, G27) | A design choice with a minimum-claims exit rule; if the minimum is not met the window extends and GA moves |

If time runs out early, goals are ordered so that each finished prefix is
still useful: G01–G11 give a working, confirmed claim filing on the sandbox;
G12–G21 make it usable and safe in production; G22–G27 prove it under load,
attack and real use.

## Implementation map

| Decision | ADK or application component and integration point (proposed) | GCP responsibility | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |
| D1 | `app/agents/intake.py` (`LlmAgent`, three function tools); `app/agents/photo_reader.py` (single-turn call with `output_schema`, no tools); submit only in `app/api/submit.py` | Vertex AI EU | `adk-workflow-design` | `output_schema` behaviour on the chosen pin (G02) |
| D3 | `app/api/auth.py` middleware verifies OIDC, sets `state["app:customer_id"]`-style trusted key; owner checks in repositories | CIAM client (W5) | `adk-tool-auth-and-secrets` | Exact state-key prefix semantics on the pin |
| D4, D5 | `app/store/` (drafts, operations, allowances, tombstones); `app/worker/submit.py`; `app/guidewire/client.py` with search-before-send | Cloud SQL, Cloud Tasks, Secret Manager | `safe-api-tool-calls` | Guidewire replay contract (O2) |
| D6 | `app/photos/` upload URL, validation, re-encode | GCS buckets | `protect-adk-sensitive-data` | Scanning decision (O5) |
| D7 | Model config in `app/config/release.yaml` | Vertex AI EU | `adk-model-and-output-contracts` | EU availability (O1) |
| D8, D12, D15 | Portal widget calling the JSON API | Existing portal hosting | `adk-frontend-integration` | Portal release slot (W5) |
| D9 | Data map, screening callback, retention and erasure jobs | Model Armor or SDP, Cloud Scheduler | `protect-adk-sensitive-data` | Regional availability of screening |
| D10 | `before_model`/admission checks, `RunConfig.max_llm_calls`, operator flag | Cloud SQL | `adk-operational-guardrails` | Limits from O3 |
| D13 | OTel setup per process | Cloud Trace, Monitoring, Logging | `adk-agent-observability` | Exporter behaviour on the pin |
| D14 | `release.yaml` manifest, CI gate, traffic split | CI runner, Cloud Run revisions | `adk-release-engineering` | — |
| D2 | Two Cloud Run services from one image | Cloud Run, IAM | `deploy-adk-on-google-cloud` | Org policy (W4) |

## Goals and dependencies

Each phase 1 goal's outcome, scope, depth, acceptance and run prompt live in
its ticket; this table only orders them. Estimates are in the schedule block.

| ID and goal | Type | Depends on | Primary skill | State |
| --- | --- | --- | --- | --- |
| [G01 Guidewire FNOL contract](../tickets/home-claim-assistant/G01-guidewire-fnol-contract.md) | Discovery | — | `safe-api-tool-calls` | Ready |
| [G02 Project skeleton and pins](../tickets/home-claim-assistant/G02-project-skeleton.md) | Implementation | — | `adk-workflow-design` | Ready |
| [G03 EU environments and staging pipeline](../tickets/home-claim-assistant/G03-eu-environments.md) | Implementation | W4, G02 | `deploy-adk-on-google-cloud` | Blocked: W4 |
| [G04 Authenticated API and session ownership](../tickets/home-claim-assistant/G04-authenticated-api.md) | Implementation | G02 | `adk-tool-auth-and-secrets` | Proposed |
| [G05 Claim draft store and checklist](../tickets/home-claim-assistant/G05-claim-draft-store.md) | Implementation | G01, G02 | `adk-memory-architecture` | Proposed |
| [G06 Intake conversation agent](../tickets/home-claim-assistant/G06-intake-agent.md) | Implementation | G02, G05 | `adk-agent-instructions` | Proposed |
| [G07 Photo upload and validation](../tickets/home-claim-assistant/G07-photo-upload.md) | Implementation | G04, G05 | `protect-adk-sensitive-data` | Proposed |
| [G08 Quarantined photo reader](../tickets/home-claim-assistant/G08-photo-reader.md) | Implementation | G02, G05 | `adk-model-and-output-contracts` | Proposed |
| [G09 Guidewire adapter, idempotent create](../tickets/home-claim-assistant/G09-guidewire-adapter.md) | Implementation | G01, G05 | `safe-api-tool-calls` | Proposed |
| [G10 Guidewire sandbox verification](../tickets/home-claim-assistant/G10-guidewire-sandbox.md) | Implementation (live) | G09, W1 | `safe-api-tool-calls` | Blocked: W1 |
| [G11 Confirm-and-submit flow](../tickets/home-claim-assistant/G11-confirm-and-submit.md) | Implementation | G06, G07, G08, G09 | `safe-api-tool-calls` | Proposed |
| [G12 Portal chat, photos, confirm, status](../tickets/home-claim-assistant/G12-portal-ui.md) | Implementation | G04, W5 | `adk-frontend-integration` | Blocked: W5 |
| [G13 Evaluation set and runner](../tickets/home-claim-assistant/G13-evaluation-set.md) | Implementation | G05 | `adk-agent-evaluation` | Proposed |
| [G14 Model choice and output contracts](../tickets/home-claim-assistant/G14-model-choice.md) | Discovery + implementation | G06, G07, G08, G13 | `adk-model-and-output-contracts` | Proposed |
| [G15 Sensitive-data boundaries, retention, erasure](../tickets/home-claim-assistant/G15-sensitive-data.md) | Implementation | G03, G06, G07, G08 | `protect-adk-sensitive-data` | Proposed |
| [G16 Security design review](../tickets/home-claim-assistant/G16-security-design-review.md) | Review | — | `adk-agent-security` | Ready |
| [G17 Threat model and adversarial suite](../tickets/home-claim-assistant/G17-adversarial-suite.md) | Implementation | G06, G07, G08, G16 | `adk-agent-security` | Proposed |
| [G18 Budgets, abuse limits, operator stop](../tickets/home-claim-assistant/G18-budgets-and-limits.md) | Implementation | G06, G07, G08 | `adk-operational-guardrails` | Proposed |
| [G19 Observability and SLOs](../tickets/home-claim-assistant/G19-observability.md) | Implementation | G03, G11 | `adk-agent-observability` | Proposed |
| [G20 Release manifest, eval gate, canary](../tickets/home-claim-assistant/G20-release-engineering.md) | Implementation | G03, G13 | `adk-release-engineering` | Proposed |
| [G21 Production environment and recovery drill](../tickets/home-claim-assistant/G21-production-environment.md) | Implementation (hosted) | G03, G15 | `deploy-adk-on-google-cloud` | Proposed |
| [G22 Storm-surge load test](../tickets/home-claim-assistant/G22-load-test.md) | Implementation (hosted) | G18, G21, W6 | `optimise-adk-on-google-cloud` | Proposed |
| [G23 Pen test and security sign-off](../tickets/home-claim-assistant/G23-pen-test-sign-off.md) | Review | G10, G11, G15, G17, W3 | `adk-agent-security` | Blocked: W3 |
| [G24 Security remediation](../tickets/home-claim-assistant/G24-security-remediation.md) | Implementation | G23 | `adk-agent-security` | Proposed |
| [G25 Employee pilot](../tickets/home-claim-assistant/G25-employee-pilot.md) | Hosted trial | G10, G12, G14, G19, G21 | `adk-agent-evaluation` | Proposed |
| [G26 Runbooks and on-call handover](../tickets/home-claim-assistant/G26-runbooks.md) | Implementation | G19, G21 | `adk-agent-observability` | Proposed |
| [G27 Controlled beta and GA go/no-go](../tickets/home-claim-assistant/G27-controlled-beta.md) | Hosted trial | G20, G22, G24, G25, G26, W2 | `adk-release-engineering` | Blocked: W2 |

Waits to request on day 1 (no owner hours; the delivery lead sends the
requests): **W1** Guidewire sandbox tenant, API client and a searchable
external-reference field; **W2** DPIA (send this design); **W3** pen-test
booking for the window after G17; **W4** EU GCP projects and resource-location
policy; **W5** CIAM client and portal release slot; **W6** Vertex AI EU quota.

### Phase 2 (after GA; three or four lines each, revised once phase 1 has run)

- **G28 Call-centre agents can open a customer's draft by reference.** Staff
  identity, read-only, audited. Primary `adk-tool-auth-and-secrets`;
  supporting `adk-frontend-integration`. Acceptance: an agent without the
  claims role gets 403; every read is audited.
- **G29 Second market and language.** New instruction locale, eval cases and
  Guidewire mapping. Primary `adk-agent-evaluation`; supporting
  `adk-agent-instructions`. Acceptance: the new-language eval set meets the
  German thresholds.
- **G30 Production samples become evaluation cases.** Redacted sampled
  sessions reviewed and added to the gated set. Primary
  `adk-release-engineering`; supporting `adk-agent-observability`. Acceptance:
  eval-set hash changes with a reviewed batch and the gate reruns.
- **G31 Model migration rehearsal.** Side-by-side of the next stable model on
  the frozen set, released as its own bundle. Primary `adk-release-engineering`;
  supporting `adk-model-and-output-contracts`. Acceptance: re-baseline report
  and a rollback tested.
- **G32 "Where is my claim?" read-only status.** Primary
  `adk-tool-interface-design`; supporting `adk-tool-auth-and-secrets`.
  Acceptance: status for own claims only; other customer's claim → not found.
- **G33 Latency and cost tuning from pilot measurements.** Primary
  `optimise-adk-on-google-cloud`. Acceptance: p95 turn latency and tokens per
  completed claim improve on the same workload without quality loss.

## Later

| Item | Trigger that brings it forward | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| Multi-region failover | Availability target above 99.5 % or a regional incident | Hours of outage in a region failure; phone line is the fallback | `deploy-adk-on-google-cloud` |
| Video uploads | Adjusters ask for video evidence | Customers e-mail videos as today | `protect-adk-sensitive-data` |
| Contents inventory capture | Contents claims share above an agreed level | Inventory collected by adjusters | `adk-workflow-design` |
| Fraud-signal hand-off | Fraud team requests structured signals | Fraud review uses Guidewire data only | `safe-api-tool-calls` |
| Model failover across regions or models | Measured model outage minutes above SLO budget | Outage shows phone line | `adk-model-and-output-contracts` |
| Guidewire-side agent via A2A | Guidewire offers an agent endpoint the team wants | None | `adk-agent-interoperability` |

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| [Design](../architecture/home-claim-assistant.md) | Method, decisions D1–D15, guarantees I1–I10 |
| Evaluation summary (created in G13) | Latest result per case and metric, linked to run records |
| This plan | Schedule, remaining limits and deferred controls |

## Open decisions for further planning

The open decisions O1–O7 are listed once, in the design. O2 and O7 move
dates; O1 and O3 block G14 and G18 thresholds; O4–O6 block final values in
G15, G07 and G12 but not their start.

## Resume here

- **Next goal:** G01 Guidewire FNOL contract and G02 project skeleton — both
  ready, independent, owned by different people. G16 (security design
  review) is also ready.
- **Read first:** the design, then the ticket.
- **Next action:** send the six wait requests (W1–W6); start G01 and G02.
- **Continuation prompt:**

```text
/adk-engineer Carry out docs/tickets/home-claim-assistant/G01-guidewire-fnol-contract.md.
Read docs/architecture/home-claim-assistant.md and preserve its decisions.
Use safe-api-tool-calls with adk-tool-interface-design.
Verify the ticket's acceptance cases, fill in its Evidence section and set
its status. Leave changes uncommitted.
```

After that goal, the same request without a goal ID continues with the next
ready one: `/adk-engineer Continue the next ready goal in docs/plans/home-claim-assistant.md.`
