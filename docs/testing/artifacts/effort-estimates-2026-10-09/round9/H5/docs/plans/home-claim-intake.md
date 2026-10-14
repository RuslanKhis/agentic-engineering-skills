# Implementation plan: home-insurance claim intake agent (EU)

Status: draft. Ready goals are identified (G01, G02, G03). Nothing has been implemented.
Architecture: [docs/architecture/home-claim-intake.md](../architecture/home-claim-intake.md)
Continuation source of truth: this plan (schedule) and the tickets in
[docs/tickets/home-claim-intake/](../tickets/home-claim-intake/) (goal scope and acceptance).

## Summary for the reader

- **Profile and phase 1:** this is a production service. Phase 1 is GA for German home-policy customers
  in the web portal on 2027-03-15 (assumption A1). Customers file a home claim by
  chat with photos. The claim, with its photos, is created in Guidewire ClaimCenter only after
  the customer confirms. Before GA come staging on synthetic data, then a
  limited-customer pilot.
- **Effort and finish:** phase 1 needs **668–1,122 human hours**, agent-assisted,
  against **2,340 h** of capacity after a 25 % reserve. It is projected to finish
  in **58–95 working days** of the **100** available (2026-10-15 to 2027-03-12),
  so it **fits** at the high end. The calendar is set by dependencies, not
  hours. The longest chain (high) runs from the agent skeleton through Guidewire
  submission, the photo attachment work, the second security review, the pilot launch and
  the pilot run to GA: G03 → G06 → G10 → G23 → G25 → G21 → W7 → G26, 91.7 days.
  The plan uses 29–48 % of total capacity, and individual roles are loaded at 17–58 %. Spare hours do
  not shorten that chain (see O7).
- **Largest risks:**
  1. The Guidewire replay contract is unknown, so "one claim per confirmation"
     is provisional. G02 resolves it, and W2 sandbox access is requested on day 1.
  2. The DPIA (W1, 25–40 days) and the pen test (W3) are external waits that gate
     the pilot and GA. G01 requests both on day 1.
  3. The EU availability of the chosen model `gemini-3.8-flash` and of Model Armor is
     unverified. G01 checks it, and the fallback model forces a migration about
     2 months after GA.
- **Decisions needed from you:**
  - Confirm or correct assumed answers A1–A15 in the design, above all the market and
    date, the Guidewire access and the security reviewer's hours.
  - Confirm the cut line below or pull in phase 2 items (O7).
- **Next prompt:** see [Resume here](#resume-here).

## Destination and constraints

The destination is the journey, decisions D1–D15 and invariants I1–I8 in the design. The
following are non-goals at GA: coverage statements, claim status, mobile, other markets.
Nothing is authorised beyond local design work. Every goal that touches GCP or
Guidewire needs its target and permission named when it is run.

- **Repository:** empty apart from `.claude/skills/`, so every module path
  in the tickets is *proposed*.
- **ADK pin:** working assumption `google-adk==2.8.0`. G03 confirms it (O3).
- **Model:** pinned `gemini-3.8-flash` for the agent, the photo analyser and the
  judge (D8). The prompt version is recorded in the release manifest (G17).
  Changing any of these is a release, not a side effect.
- **Credentials:** none appear in this document. The Guidewire client secret
  and the CIAM configuration live in Secret Manager (G04, G24).

## Delivery profile and capacity

Profile: production, as set out in the design's
[delivery constraints](../architecture/home-claim-intake.md#delivery-constraints-depth-and-deferred-controls).

| Phase | Delivers | Goals | Human hours, agent-assisted | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship | GA in Germany: staging, pilot, go-live | G01–G27, waits W1–W7 | 668–1,122 | 6 people × 5 h/day plus security 1.2 h/day, over 100 days, with 25 % reserve = 2,340 h |
| 2, harden or grow | Post-GA items P2-01 to P2-06 | P2-01–P2-06 | 150–290 (sum of the ranges below) | After GA, when the team has time |

Estimates are person-hours of human effort (hands-on plus review and verify) for a
developer working with a coding agent. They **include the ×1.5 new-to-ADK
multiplier** (A3), applied to every goal. Waits are schedule entries
(`total: 0`) with `wait_days`, and they are never added to hours.

| Person or role | Phase 1 goals | Hours | Their capacity (after reserve) |
| --- | --- | --- | --- |
| Lead | G01, G05, G12, G13, G21, G26 | 120–204 | 375 |
| Integration | G02, G10 | 64–102 | 375 |
| Platform | G04, G18, G22, G24 | 80–136 | 375 |
| Frontend | G11, G16, G17 | 122–204 | 375 |
| Agent | G03, G06, G07, G15, G20, G23 | 130–218 | 375 |
| ML | G08, G09, G19, G27 | 136–232 | 375 |
| Security (part-time) | G14, G25 | 16–26 | 90 |

The schedule block below is the only source of each estimate, owner, dependency and wait.
Tickets copy it.

```yaml
- goal: W1
  phase: 1
  total: 0
  blocked_by: []
  calendar_waits: DPIA sign-off by DPO
  wait_days: 25-40
- goal: W2
  phase: 1
  total: 0
  blocked_by: []
  calendar_waits: Guidewire sandbox tenant and API client from Guidewire team
  wait_days: 10-20
- goal: W3
  phase: 1
  total: 0
  blocked_by: [G18]
  calendar_waits: external penetration test of staging
  wait_days: 10-15
- goal: W4
  phase: 1
  total: 0
  blocked_by: []
  calendar_waits: Vertex AI EU quota increase
  wait_days: 5-10
- goal: W5
  phase: 1
  total: 0
  blocked_by: []
  calendar_waits: GCP projects, billing and org IAM from cloud platform team
  wait_days: 3-8
- goal: W6
  phase: 1
  total: 0
  blocked_by: [G11]
  calendar_waits: legal and compliance review of customer-facing wording
  wait_days: 5-10
- goal: G01
  phase: 1
  hands_on: 6-10
  review: 2-4
  total: 8-14
  owner: Lead
  blocked_by: []
  calendar_waits: none
  wait_days: 0
  handoff: 0
- goal: G02
  phase: 1
  hands_on: 12-20
  review: 4-6
  total: 16-26
  owner: Integration
  blocked_by: []
  calendar_waits: none
  wait_days: 0
  handoff: 0
- goal: G03
  phase: 1
  hands_on: 10-18
  review: 4-6
  total: 14-24
  owner: Agent
  blocked_by: []
  calendar_waits: none
  wait_days: 0
  handoff: 0
- goal: G04
  phase: 1
  hands_on: 20-34
  review: 6-10
  total: 26-44
  owner: Platform
  blocked_by: [W5]
  calendar_waits: W5
  wait_days: 0
  handoff: 0
- goal: G05
  phase: 1
  hands_on: 18-30
  review: 8-14
  total: 26-44
  owner: Lead
  blocked_by: [G01, G03]
  calendar_waits: none
  wait_days: 0
  handoff: 2
- goal: G06
  phase: 1
  hands_on: 28-46
  review: 8-14
  total: 36-60
  owner: Agent
  blocked_by: [G03]
  calendar_waits: none
  wait_days: 0
  handoff: 0
- goal: G07
  phase: 1
  hands_on: 20-34
  review: 6-10
  total: 26-44
  owner: Agent
  blocked_by: [G04, G05]
  calendar_waits: none
  wait_days: 0
  handoff: 3
- goal: G08
  phase: 1
  hands_on: 24-40
  review: 6-10
  total: 30-50
  owner: ML
  blocked_by: [G03]
  calendar_waits: none
  wait_days: 0
  handoff: 2
- goal: G09
  phase: 1
  hands_on: 40-70
  review: 6-10
  total: 46-80
  owner: ML
  blocked_by: [G03]
  calendar_waits: none
  wait_days: 0
  handoff: 1
- goal: G10
  phase: 1
  hands_on: 36-56
  review: 12-20
  total: 48-76
  owner: Integration
  blocked_by: [G02, G04, G06, W2]
  calendar_waits: W2
  wait_days: 0
  handoff: 3
- goal: G11
  phase: 1
  hands_on: 60-100
  review: 14-24
  total: 74-124
  owner: Frontend
  blocked_by: [G03]
  calendar_waits: none
  wait_days: 0
  handoff: 2
- goal: G12
  phase: 1
  hands_on: 22-36
  review: 8-14
  total: 30-50
  owner: Lead
  blocked_by: [G05, G07]
  calendar_waits: none
  wait_days: 0
  handoff: 2
- goal: G13
  phase: 1
  hands_on: 20-32
  review: 8-14
  total: 28-46
  owner: Lead
  blocked_by: [G06, G08]
  calendar_waits: none
  wait_days: 0
  handoff: 4
- goal: G14
  phase: 1
  hands_on: 8-12
  review: 2-4
  total: 10-16
  owner: Security
  blocked_by: [G05, G07, G13]
  calendar_waits: none
  wait_days: 0
  handoff: 2
- goal: G15
  phase: 1
  hands_on: 12-20
  review: 4-8
  total: 16-28
  owner: Agent
  blocked_by: [G06]
  calendar_waits: none
  wait_days: 0
  handoff: 0
- goal: G16
  phase: 1
  hands_on: 18-30
  review: 6-10
  total: 24-40
  owner: Frontend
  blocked_by: [G04, G10]
  calendar_waits: none
  wait_days: 0
  handoff: 2
- goal: G17
  phase: 1
  hands_on: 18-30
  review: 6-10
  total: 24-40
  owner: Frontend
  blocked_by: [G04, G09]
  calendar_waits: none
  wait_days: 0
  handoff: 3
- goal: G18
  phase: 1
  hands_on: 12-20
  review: 4-8
  total: 16-28
  owner: Platform
  blocked_by: [G04, G05, G07, G10, G11]
  calendar_waits: none
  wait_days: 0
  handoff: 4
- goal: G19
  phase: 1
  hands_on: 36-60
  review: 8-14
  total: 44-74
  owner: ML
  blocked_by: [G06, G08, G09]
  calendar_waits: none
  wait_days: 0
  handoff: 2
- goal: G20
  phase: 1
  hands_on: 12-20
  review: 4-6
  total: 16-26
  owner: Agent
  blocked_by: [G18, W4]
  calendar_waits: W4
  wait_days: 0
  handoff: 2
- goal: G21
  phase: 1
  hands_on: 10-18
  review: 4-6
  total: 14-24
  owner: Lead
  blocked_by: [G12, G14, G15, G16, G17, G18, G19, G20, G22, G23, G24, G25, W1, W6]
  calendar_waits: none
  wait_days: 0
  handoff: 4
- goal: G22
  phase: 1
  hands_on: 14-24
  review: 4-6
  total: 18-30
  owner: Platform
  blocked_by: [G16, G24]
  calendar_waits: none
  wait_days: 0
  handoff: 2
- goal: G23
  phase: 1
  hands_on: 16-26
  review: 6-10
  total: 22-36
  owner: Agent
  blocked_by: [G07, G10]
  calendar_waits: none
  wait_days: 0
  handoff: 3
- goal: G24
  phase: 1
  hands_on: 14-24
  review: 6-10
  total: 20-34
  owner: Platform
  blocked_by: [G04]
  calendar_waits: none
  wait_days: 0
  handoff: 0
- goal: W7
  phase: 1
  total: 0
  blocked_by: [G21]
  calendar_waits: limited-customer pilot running in production
  wait_days: 10-15
- goal: G25
  phase: 1
  hands_on: 4-7
  review: 2-3
  total: 6-10
  owner: Security
  blocked_by: [G10, G12, G23]
  calendar_waits: none
  wait_days: 0
  handoff: 2
- goal: G26
  phase: 1
  hands_on: 10-19
  review: 4-7
  total: 14-26
  owner: Lead
  blocked_by: [G22, G27, W3, W7]
  calendar_waits: none
  wait_days: 0
  handoff: 2
- goal: G27
  phase: 1
  hands_on: 12-22
  review: 4-6
  total: 16-28
  owner: ML
  blocked_by: [G21]
  calendar_waits: none
  wait_days: 0
  handoff: 3
```

**Schedule check** (`check_schedule.py`, run 2026-10-14):

```
python3.11 .claude/skills/adk-system-designer/scripts/check_schedule.py \
  --plan docs/plans/home-claim-intake.md --tickets docs/tickets/home-claim-intake/ \
  --days 100 --reserve 0.25 --person Lead=5 --person Integration=5 \
  --person Platform=5 --person Frontend=5 --person Agent=5 --person ML=5 --person Security=1.2
```

Result: 668–1,122 h. Capacity 2,340 h, fits. Finish 58–95 working days of 100, fits.
The longest chain (high) is 91.7 days. Exit 0.
In the helper's schedule the pilot starts between days 41 and 67 and its run (W7) ends between days 54 and 88.

Changes made after failing runs. Each change reflects how the work actually splits. No
dependency was removed and no wait was shortened.

| Run | Finish (high) | Change made and why |
| --- | --- | --- |
| 1 | 158 | Production environment split out of G04 into G24. Guidewire photo attachment split out of G10 into G23, given to Agent. Submission's own forbidden-effect tests moved into G10, so G13 no longer waits for G10. |
| 2 | 135 | **G12 was missing from the pilot's prerequisites; added.** G17 moved from Platform to Frontend, which was idle after G11. |
| 3 | 124 | Security review split per boundary: G14 covers identity and upload, G25 covers submission and data. Operational readiness (G22) separated from the GA go/no-go (G26). |
| 4 | 119 | G07 moved to Agent, which was idle while Integration was serial. Pilot split into launch (G21), run (W7) and quality review (G27). |
| 5 | 114 | G16 moved to Frontend. What-if with Integration as owner: 110 days. |
| 6 | 102.5 | G12 moved from Integration to Lead, who was free from about day 35. The missing G16→G22 handoff was added. |
| 7 | **95 (pass)** | G27 depends on the pilot launch, because claims are reviewed while the pilot runs. G26 waits for the pilot run (W7) to end. |

What-if not offered as a remedy: giving Security 2 h/day *worsens* the helper's
finish to 60.9–101.7 days. The helper orders goals greedily, so extra
hours change which goal goes first rather than shortening the chain.

If time runs short, cut in this order. Each remaining goal is still useful.

1. Replace the G20 load test with quota checks only. This raises the storm risk.
2. Shrink G19 quality iteration to one round.
3. Shorten W7 from 15 to 10 days, if the business accepts it.

Never cut G10, G12, G13, G14, G15, G25 or W1. They are the floor.

## Implementation map

| Decision | Component and integration point (proposed) | GCP responsibility | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |
| D1, D2 | `app/agent.py`: intake `LlmAgent`. `app/drafts/`: ClaimDraft repository and `update_claim_draft` tool. | Vertex AI EU | `adk-agent-instructions` | ADK pin (O3) |
| D3, D4 | `app/submission/`: `/confirm`, `SubmissionOperation`, Cloud Tasks worker, Guidewire client, reconciler | Cloud Tasks, Cloud Run worker, Secret Manager | `safe-api-tool-calls` | Replay contract (O1) |
| D5 | `app/photos/analyser.py`: tool-less model call with `output_schema` | Vertex AI EU | `adk-model-and-output-contracts` | Model in an EU region (O2) |
| D6 | `app/auth/middleware.py`: OIDC verify → `customer_id` in session state. `before_tool_callback` scope check. | — | `adk-tool-auth-and-secrets` | CIAM claims (O4) |
| D7 | Cloud Run ×2, Cloud SQL, GCS, Tasks, via Terraform in `infra/` | EU projects dev, staging, prod | `deploy-adk-on-google-cloud` | Region availability (G01) |
| D9 | `app/api/` SSE plus `/draft`, `/photos`, `/submissions`. Portal widget. | — | `adk-frontend-integration` | Portal stack (O4) |
| D10 | `app/privacy/`: EXIF strip, retention and erasure jobs, Model Armor client | Model Armor, GCS lifecycle | `protect-adk-sensitive-data` | Model Armor EU (O5) |
| D11 | `app/limits/`: RunConfig, allowances table, kill switch | Cloud SQL | `adk-operational-guardrails` | — |
| D13, D14 | `release/manifest.json`, CI gate, OTel setup | Cloud Trace, Monitoring, CI runner | `adk-release-engineering`, `adk-agent-observability` | — |

## Goals and dependencies

Each ticket is the home of its goal's scope, route and acceptance. Estimates,
owners and waits come from the schedule block.

| ID and goal | Type | Depends on | Primary skill | State |
| --- | --- | --- | --- | --- |
| [G01 Platform, model and EU availability facts; request external waits](../tickets/home-claim-intake/G01-platform-model-discovery.md) | discovery | — | adk-model-and-output-contracts | ready |
| [G02 Guidewire FNOL contract and fake](../tickets/home-claim-intake/G02-guidewire-contract-and-fake.md) | discovery + implementation | — | safe-api-tool-calls | ready |
| [G03 Walking skeleton: agent, Runner, API contract, CI](../tickets/home-claim-intake/G03-walking-skeleton.md) | implementation | — | adk-workflow-design | ready |
| [G04 Dev and staging GCP foundation](../tickets/home-claim-intake/G04-gcp-foundation.md) | implementation | W5 | deploy-adk-on-google-cloud | blocked (W5) |
| [G05 Customer identity and ownership](../tickets/home-claim-intake/G05-customer-identity-and-ownership.md) | implementation | G01, G03 | adk-tool-auth-and-secrets | blocked |
| [G06 Intake conversation and claim draft](../tickets/home-claim-intake/G06-intake-conversation-and-draft.md) | implementation | G03 | adk-agent-instructions | blocked |
| [G07 Photo upload and storage](../tickets/home-claim-intake/G07-photo-upload-and-storage.md) | implementation | G04, G05 | adk-memory-architecture | blocked |
| [G08 Quarantined photo damage analysis](../tickets/home-claim-intake/G08-photo-damage-analysis.md) | implementation | G03 | adk-model-and-output-contracts | blocked |
| [G09 Evaluation set and harness](../tickets/home-claim-intake/G09-evaluation-set-and-harness.md) | implementation | G03 | adk-agent-evaluation | blocked |
| [G10 Confirmed, idempotent Guidewire submission](../tickets/home-claim-intake/G10-guidewire-submission-outbox.md) | implementation | G02, G04, G06, W2 | safe-api-tool-calls | blocked |
| [G11 Portal chat widget and review screen](../tickets/home-claim-intake/G11-portal-widget-and-review.md) | implementation | G03 | adk-frontend-integration | blocked |
| [G12 Sensitive data, retention and erasure](../tickets/home-claim-intake/G12-sensitive-data-retention-erasure.md) | implementation | G05, G07 | protect-adk-sensitive-data | blocked |
| [G13 Threat model and adversarial suite](../tickets/home-claim-intake/G13-threat-model-and-adversarial-suite.md) | implementation | G06, G08 | adk-agent-security | blocked |
| [G14 Security review I: identity, upload, agent structure](../tickets/home-claim-intake/G14-security-review-identity-upload.md) | review | G05, G07, G13 | adk-agent-security | blocked |
| [G15 Budgets, allowances and kill switch](../tickets/home-claim-intake/G15-budgets-and-kill-switch.md) | implementation | G06 | adk-operational-guardrails | blocked |
| [G16 Observability: SLIs, alerts, no-content telemetry](../tickets/home-claim-intake/G16-observability.md) | implementation | G04, G10 | adk-agent-observability | blocked |
| [G17 Release manifest and evaluation gate](../tickets/home-claim-intake/G17-release-manifest-and-eval-gate.md) | implementation | G04, G09 | adk-release-engineering | blocked |
| [G18 Staging end to end against Guidewire sandbox](../tickets/home-claim-intake/G18-staging-end-to-end.md) | implementation | G04, G05, G07, G10, G11 | deploy-adk-on-google-cloud | blocked |
| [G19 Quality iteration to targets](../tickets/home-claim-intake/G19-quality-iteration.md) | implementation | G06, G08, G09 | adk-agent-evaluation | blocked |
| [G20 Load and cost test](../tickets/home-claim-intake/G20-load-and-cost-test.md) | implementation | G18, W4 | optimise-adk-on-google-cloud | blocked |
| [G21 Limited-customer pilot launch](../tickets/home-claim-intake/G21-pilot-launch.md) | implementation | G12, G14–G20, G22–G25, W1, W6 | adk-release-engineering | blocked |
| [G22 Operational readiness and rollback rehearsal](../tickets/home-claim-intake/G22-operational-readiness.md) | implementation | G16, G24 | deploy-adk-on-google-cloud | blocked |
| [G23 Idempotent photo attachment to the claim](../tickets/home-claim-intake/G23-photo-attachment-to-claim.md) | implementation | G07, G10 | safe-api-tool-calls | blocked |
| [G24 Production environment](../tickets/home-claim-intake/G24-production-environment.md) | implementation | G04 | deploy-adk-on-google-cloud | blocked |
| [G25 Security review II: submission and data](../tickets/home-claim-intake/G25-security-review-submission-data.md) | review | G10, G12, G23 | adk-agent-security | blocked |
| [G26 GA go/no-go and pen-test remediation](../tickets/home-claim-intake/G26-ga-go-no-go.md) | implementation | G22, G27, W3, W7 | adk-release-engineering | blocked |
| [G27 Pilot quality and outcome review](../tickets/home-claim-intake/G27-pilot-quality-review.md) | evaluation | G21 | adk-agent-evaluation | blocked |

Waits have no tickets. Their owners request them on day 1 as part of G01, or later as part of G11 and G18.

| Wait | What | Requested in |
| --- | --- | --- |
| W1 | DPIA sign-off by the DPO (25–40 days) | G01, on day 1 |
| W2 | Guidewire sandbox tenant and API client (10–20 days) | G01, on day 1 |
| W3 | External pen test of staging (10–15 days, after G18) | G01 books the slot. G18 triggers the test. |
| W4 | Vertex AI EU quota increase (5–10 days) | G01, on day 1 |
| W5 | GCP projects and org IAM from the platform team (3–8 days) | G01, on day 1 |
| W6 | Legal review of customer-facing wording and AI disclosure (5–10 days) | G11 |
| W7 | Pilot running in production (10–15 days) | G21 |

### Phase 2 (after GA; tickets not written)

- **P2-01 Claim status and follow-up questions in chat.** Read-only Guidewire scope.
  Primary `adk-tool-interface-design`. 30–55 h. Acceptance: a customer sees only their
  own claim's status, and a cross-customer lookup is denied.
- **P2-02 Second EU market.** Language, legal wording and its own eval cases.
  Primary `adk-agent-evaluation`. 30–60 h, plus a legal wait. Acceptance: eval
  thresholds are met for the new language.
- **P2-03 Mobile app integration**, with the camera capture flow. Primary
  `adk-frontend-integration`. 40–70 h. Acceptance: the same review/confirm contract
  holds, checked by an app E2E test.
- **P2-04 Redacted production samples feed the eval set** (needs DPIA terms).
  Primary `adk-agent-observability`. 20–40 h. Acceptance: a sampled session becomes a
  redacted eval case with no PII sentinel left.
- **P2-05 Context caching and cost tuning.** Primary `optimise-adk-on-google-cloud`.
  15–30 h. Acceptance: cached-token count is above 0 and cost per completed claim drops without
  a quality regression.
- **P2-06 Model migration rehearsal** before the pinned model's next retirement.
  Primary `adk-release-engineering`. 15–35 h. Acceptance: a side-by-side on the
  frozen dev set and a joint rollback both work.

## Later

| Item | Trigger that brings it forward | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| Live handoff to a human chat agent | Pilot shows high "call us" use | Customers switch channel to phone | adk-agent-interoperability |
| Video upload | Adjusters ask for it | Fewer details for some damages | adk-memory-architecture |
| Contents/inventory claims | Business scope decision | Out of scope at GA | adk-workflow-design |
| Multi-region failover | RTO below 4 h required | Regional outage delays new chats; queued claims survive | deploy-adk-on-google-cloud |
| Adjuster-facing summary copilot | Phase 2 success | — | adk-system-designer (new design) |

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| [Design](../architecture/home-claim-intake.md) | Method, assumed answers, decisions, invariants |
| Eval summary (produced by G09/G19, `eval/summary.md`, proposed) | Latest result per case |
| This plan | Schedule, remaining limits, deferred controls |

## Open decisions for further planning

See the design's [open decisions](../architecture/home-claim-intake.md#open-decisions) O1–O7.
O1 blocks the final form of G10. O2 blocks G08 and G19 live runs. Neither blocks G01–G03.

## Resume here

- **Next goal:** G03 Walking skeleton. It is ready and on the critical path. G01 and
  G02 are also ready and can run at the same time in other sessions. G01 should start on day 1
  because it requests the external waits.
- **Read first:** the design, this plan, and the G03 ticket.
- **Next action:** create the proposed `app/` layout with an `App` and Runner, a
  scripted-model test, and the JSON/SSE API contract, and confirm the ADK pin.
- **Continuation prompt:**

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G03-walking-skeleton.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

After that, `/adk-engineer Continue the next ready goal in docs/plans/home-claim-intake.md.`
