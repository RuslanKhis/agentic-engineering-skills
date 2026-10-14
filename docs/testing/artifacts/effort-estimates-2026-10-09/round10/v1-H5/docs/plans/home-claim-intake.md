# Implementation plan: home-insurance claim intake agent (EU)

Status: draft — ready goals identified; schedule checked; awaiting user
confirmation of the cut line and the assumed answers
Architecture: [docs/architecture/home-claim-intake.md](../architecture/home-claim-intake.md)
Continuation source of truth: this plan; each phase 1 goal's scope and
acceptance live in its ticket under [docs/tickets/home-claim-intake/](../tickets/home-claim-intake/)

## Summary for the reader

- **Profile and phase 1:** production service. Phase 1 delivers GA in one EU
  market: signed-in policyholders file a home claim with photos through the
  portal, and a claim appears in Guidewire ClaimCenter, after an invite-only
  pilot (G22).
- **Effort and finish:** phase 1 is 702–1070 human hours against 2280 hours
  of capacity after a 25% reserve, so hours fit. The calendar is the
  constraint: with dependencies, one goal per person at a time and calendar
  waits, the finish range is **70.6–106.7 working days against 95**: fits at
  the low end only. Moving GA to 107 working days (about end of March 2027
  instead of mid-March) fits the high end. Hours are not the problem, so more
  people do not close the gap (checked below).
- **Largest risks:** (1) Guidewire non-prod access and the replay contract (W1,
  O2) arrive late or lack a safe lookup: requested on day 1, G01 owns it.
  (2) The pilot runs alongside the external pen test (O3); if security
  refuses, GA moves by about 12 working days (what-if below). (3) The model
  is not served from an EU regional endpoint (O1): G02 checks it first.
- **Decisions needed from you:** confirm or move the cut line (GA date 95 vs
  107 working days); O3 (pilot during pen test); the assumed answers A1–A18
  in the design, especially A2, A5, A7, A15.
- **Next prompt:** `/adk-engineer Carry out docs/tickets/home-claim-intake/G02-walking-skeleton.md.`
  On day 1 also send the requests behind W1–W5 and book the pen-test vendor
  for W7.

## Destination and constraints

End result: decisions D1–D14 of the design built, tested and released to all
customers of one EU market. Non-goals are in the design's purpose section.
Accepted stack: none yet accepted by the user; proposed Python 3.11,
google-adk 2.8.0 (working assumption, D14), Cloud Run, Cloud SQL Postgres,
GCS, Vertex AI in one EU region. Pinned model `gemini-3.8-flash` for agent,
photo reader and judge (D7); prompt versions are versioned files; a change to
any of them is a release (G17). Current authorization: design and planning
only. No cloud resources, IAM changes, Guidewire calls or deployments are
authorized by this plan; each goal names what it needs.

Repository: empty apart from `.claude/skills`; every path below is proposed:

```text
app/            FastAPI app, auth middleware, routes (turn, upload-url, confirm)
app/agent/      intake_agent, instructions/, tools.py, release_check.py
app/photos/     sanitiser, photo_reader
app/submission/ ledger, executor, guidewire_adapter, reconciler
app/limits/     allowances, kill switch
evals/          cases, photo sets, runner, thresholds
infra/          Terraform or the landing zone's convention (decided in G03)
web/            portal panel (in the portal repo if it is separate; G12 decides)
```

## Delivery profile and capacity

Profile: production (design, delivery constraints). Capacity: five engineers
and one ML engineer at 5 focused h/day, security reviewer at 2 h/day, 95
working days from an assumed start on 2026-10-19, 25% reserve. Estimates are
person-hours of human effort with a coding agent (hands-on plus review and
verify), **already multiplied by 1.5 for a team new to ADK** on every goal.
Calendar waits are W entries or `wait_days` on their goal, never hours.

| Phase | Delivers | Goals | Human hours (range) | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship | GA in one EU market | G01–G25 | 702–1070 | 2280 h after 25% reserve; calendar fits low end only |
| 2, harden | Feedback loop, second market, mobile, tuning, model migration | G30–G34 | 124–208 | After GA |

| Person or role | Goals | Hours | Their capacity (95 days, after reserve) |
| --- | --- | --- | --- |
| Eng A (agent lead) | G02, G06, G11, G22 | 114–171 | 356 |
| Eng B (integration) | G01, G09, G10, G20 | 122–184 | 356 |
| Eng C (frontend) | G05, G12 | 86–131 | 356 |
| Eng D (platform) | G03, G16, G17, G18, G23 | 136–204 | 356 |
| Eng E (security engineering) | G04, G13, G14, G21 | 108–170 | 356 |
| ML | G07, G08, G24 | 94–144 | 356 |
| Sec (part time) | G15, G25, G19 | 42–66 | 142.5 |

Spare hours are real: every person is under half loaded. They are not for
pulling phase 2 forward until the chain below is safe; the best use is pairing
on the chain goals (G06, G09, G10, G18) and absorbing live-integration
surprises, which these estimates are least sure of.

Schedule block (the single source of each estimate; tickets copy it):

```yaml
- goal: W1
  phase: 1
  total: 0
  calendar_waits: Guidewire non-prod tenant, API client and external-reference field
  wait_days: 10-20
- goal: W2
  phase: 1
  total: 0
  calendar_waits: CIAM OIDC client registration
  wait_days: 5-10
- goal: W3
  phase: 1
  total: 0
  calendar_waits: GCP EU projects from landing-zone team
  wait_days: 5-10
- goal: W4
  phase: 1
  total: 0
  calendar_waits: legal review of AI disclosure and customer wording
  wait_days: 10-15
- goal: W5
  phase: 1
  total: 0
  calendar_waits: Guidewire non-prod load-test window agreed
  wait_days: 10-20
- goal: W6
  phase: 1
  total: 0
  calendar_waits: DPIA sign-off by the DPO
  wait_days: 15-25
  blocked_by: [G15]
- goal: W7
  phase: 1
  total: 0
  calendar_waits: external pen test window and report
  wait_days: 10-15
  blocked_by: [G18, G19]
- goal: W8
  phase: 1
  total: 0
  calendar_waits: go-live approval by the change board
  wait_days: 3-5
  blocked_by: [G21, G22, G23]
- goal: G01
  phase: 1
  hands_on: 16-24
  review: 4-6
  total: 20-30
  owner: Eng B
  blocked_by: [W1]
- goal: G02
  phase: 1
  hands_on: 12-18
  review: 4-6
  total: 16-24
  owner: Eng A
  blocked_by: []
- goal: G03
  phase: 1
  hands_on: 24-36
  review: 6-10
  total: 30-46
  owner: Eng D
  blocked_by: [W3, G02]
  handoff: 1
- goal: G04
  phase: 1
  hands_on: 18-28
  review: 8-12
  total: 26-40
  owner: Eng E
  blocked_by: [G02, W2]
  handoff: 2
- goal: G05
  phase: 1
  hands_on: 18-28
  review: 6-10
  total: 24-38
  owner: Eng C
  blocked_by: [G02]
  handoff: 1
- goal: G06
  phase: 1
  hands_on: 30-45
  review: 10-15
  total: 40-60
  owner: Eng A
  blocked_by: [G02]
- goal: G07
  phase: 1
  hands_on: 22-34
  review: 4-6
  total: 26-40
  owner: ML
  blocked_by: [G02]
  handoff: 1
- goal: G08
  phase: 1
  hands_on: 24-36
  review: 6-10
  total: 30-46
  owner: ML
  blocked_by: [G05, G07]
  handoff: 1
- goal: G09
  phase: 1
  hands_on: 36-54
  review: 14-20
  total: 50-74
  owner: Eng B
  blocked_by: [G04, G06]
  handoff: 3
- goal: G10
  phase: 1
  hands_on: 20-30
  review: 6-10
  total: 26-40
  owner: Eng B
  blocked_by: [G01, G09]
- goal: G11
  phase: 1
  hands_on: 16-24
  review: 6-8
  total: 22-32
  owner: Eng A
  blocked_by: [G06]
- goal: G12
  phase: 1
  hands_on: 50-75
  review: 12-18
  total: 62-93
  owner: Eng C
  blocked_by: [G05, W4]
- goal: G13
  phase: 1
  hands_on: 24-36
  review: 8-12
  total: 32-48
  owner: Eng E
  blocked_by: [G03, G04, G05]
  handoff: 1
- goal: G14
  phase: 1
  hands_on: 24-36
  review: 8-12
  total: 32-48
  owner: Eng E
  blocked_by: [G06, G08, G09]
  handoff: 2
- goal: G15
  phase: 1
  hands_on: 24-36
  review: 4-6
  total: 28-42
  owner: Sec
  blocked_by: []
- goal: G16
  phase: 1
  hands_on: 20-30
  review: 6-8
  total: 26-38
  owner: Eng D
  blocked_by: [G02, G03]
  handoff: 1
- goal: G17
  phase: 1
  hands_on: 24-36
  review: 6-10
  total: 30-46
  owner: Eng D
  blocked_by: [G03, G06, G07, G08]
  handoff: 2
- goal: G18
  phase: 1
  hands_on: 20-30
  review: 8-12
  total: 28-42
  owner: Eng D
  blocked_by: [G10, G11, G12, G13, G16, G17]
  handoff: 3
- goal: G19
  phase: 1
  hands_on: 4-8
  review: 2-3
  total: 6-11
  owner: Sec
  blocked_by: [G14, G25]
  handoff: 1
- goal: G25
  phase: 1
  hands_on: 6-10
  review: 2-3
  total: 8-13
  owner: Sec
  blocked_by: [G04, G09]
  handoff: 1
- goal: G20
  phase: 1
  hands_on: 20-30
  review: 6-10
  total: 26-40
  owner: Eng B
  blocked_by: [G18, W5]
  handoff: 1
- goal: G21
  phase: 1
  hands_on: 12-24
  review: 6-10
  total: 18-34
  owner: Eng E
  blocked_by: [W7]
- goal: G22
  phase: 1
  hands_on: 30-45
  review: 6-10
  total: 36-55
  owner: Eng A
  blocked_by: [W6, G18, G19, G24]
  handoff: 2
  calendar_waits: pilot runs with invited customers
  wait_days: 10-15
- goal: G24
  phase: 1
  hands_on: 32-50
  review: 6-8
  total: 38-58
  owner: ML
  blocked_by: [G07, G17]
  handoff: 1
  calendar_waits: claims-handler review of labels
  wait_days: 5-10
- goal: G23
  phase: 1
  hands_on: 16-24
  review: 6-8
  total: 22-32
  owner: Eng D
  blocked_by: [G18, G20]
  handoff: 2
- goal: G30
  phase: 2
  total: 16-28
  blocked_by: [G23]
- goal: G31
  phase: 2
  total: 40-70
  blocked_by: [G23]
- goal: G32
  phase: 2
  total: 40-60
  blocked_by: [G23]
- goal: G33
  phase: 2
  total: 16-30
  blocked_by: [G20]
- goal: G34
  phase: 2
  total: 12-20
  blocked_by: [G17]
```

Schedule check, run 2026-10-14 with
`python3.11 .claude/skills/adk-system-designer/scripts/check_schedule.py --plan docs/plans/home-claim-intake.md --tickets docs/tickets/home-claim-intake/ --days 95 --reserve 0.25`
and `--person` 5 h/day for Eng A–E and ML, 2 h/day for Sec:
**702–1070 h; longest chain G02 → G06 → G09 → G10 → G18 → G22 → W8 at
the low end (65.3 days) and G02 → G07 → G08 → G17 → G24 → G22 → W8 at the
high end (101.7 days); finish 70.6–106.7 working days; fits the calendar at
the low end only** (exit 1, for that reason only; no other problem reported). The same run with
`--days 107` reports "fits: yes" (exit 0). Settled as mention only: G04→G12,
G06→G08, G09→G12 (out-of-scope pointers), G13 and G15 name the DPIA without
depending on its sign-off, G15→W4 (legal wording is separate).

If time runs out early, each completed goal stays useful in this order: G02,
G06, G04, G09, G10 (claims reach Guidewire), then G05/G08 (photos), G12
(customer-facing), then the hardening goals. None of the floor (G04, G09,
G11, G13, G14, G15) is a cut candidate.

### Changes after failing runs

The first run of the plan as first drafted gave 100.5–157.3 days ("no").
Each remedy was run as a what-if with the same people and reserve:

| Change | Why it is true of the work | Finish (working days) | Adopted |
| --- | --- | --- | --- |
| Sec at 4 h/day instead of 2 | — | 98.4–154.1 | no: does not close the gap |
| Split the eval set: G07 harness and photo dev set, G24 conversation set later | The photo reader needs only photo labels; conversation labelling can follow | 96.5–151.8 | yes |
| Pilot runs during the pen test (needs O3) | Pilot is invite-only and follows the internal security review | 85.7–133.2 | yes, provisional on O3 |
| G09 ledger built against a contract fake, not waiting for G01; G10 adapter waits for G01 | Ledger, approval binding and states do not depend on Guidewire specifics | 81.3–122.1 (with the two above) | yes |
| GA operations readiness (G23) runs alongside the pilot; go-live (W8) waits for both | Runbooks, on-call and rollback rehearsal do not need pilot results | 75.4–113.6 (cumulative) | yes |
| Security review split: identity and write boundaries reviewed as they land (G25), injection review after G14 (G19) | The reviewer can review G04 and G09 without waiting for G14 | 70.6–106.7 (cumulative) | yes |
| Same, without the pilot during the pen test | — | 90.2–137.7 (before the split review) | shown for O3 |
| + Sec 4 h/day | — | 70.6–106.7 | no: no change |
| + pilot shortened to 5–10 days | — | 65.8–101.7 | no: still over |
| + budgets goal G11 moved to Eng C | — | 70.6–106.7 | no: no change |
| + Guidewire discovery G01 moved to Eng C | — | 69.5–105.9 | no: negligible |
| GA at 107 working days | — | 70.6–106.7 | **closes the gap** (recommended if the high end matters) |
| G22 also waits for the conversation eval set G24 | A pilot with real customers needs a measured baseline | 70.6–106.7 | yes (no change to finish) |
| G03 also waits for G02 (found by the helper's mention check on the tickets) | G03 deploys the G02 image and takes its region from O1, which G02 answers | 70.6–106.7 | yes (no change to finish) |

## Implementation map

| Decision / requirement | ADK or application component and integration point | GCP service | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |
| D1, D5 | `LlmAgent` `intake_agent` in an `App` run by a `Runner` in `app/main.py`; `claim_drafts` table; `DatabaseSessionService` | Cloud SQL | adk-workflow-design | Constructor names against the chosen pin (G02) |
| D2, D3 | Confirm route `POST /claims/{draft_id}/confirm`; `app/submission/` ledger + executor + reconciler (Cloud Run job) | Cloud SQL, Cloud Scheduler | safe-api-tool-calls | Guidewire replay contract (G01, O2) |
| D4 | ASGI middleware verifies OIDC, loads entitlements, writes `customer_id`/`policy_ids` into session state before `Runner.run_async`; tools read `tool_context.state` | Secret Manager for client secrets | adk-tool-auth-and-secrets | CIAM token claims (W2) |
| D7, D10 | Instruction files under `app/agent/instructions/`; `after_model_callback` release check; `photo_reader` with `output_schema` | Vertex AI EU | adk-model-and-output-contracts | EU availability (O1) |
| D8 | JSON turn API; portal panel | — | adk-frontend-integration | Portal stack (G12) |
| D9 | Signed upload URLs; sanitiser worker in-process with a bounded pool | GCS EU | protect-adk-sensitive-data | HEIC decode library choice (G05) |
| D11 | `RunConfig(max_llm_calls=10)`; allowance table; kill-switch flag read per request | Cloud SQL | adk-operational-guardrails | — |
| D12 | Lifecycle rules; purge and erasure jobs | GCS, Cloud SQL | protect-adk-sensitive-data | DPO confirmation of A15 |
| D13 | Release manifest; CI gate; Cloud Run tags and traffic split | Cloud Build or existing CI | adk-release-engineering | CI system (G03) |
| Observability | One OpenTelemetry provider per process; content capture off | Cloud Trace, Logging, Monitoring (EU) | adk-agent-observability | Exporter region (G16) |

## Goals and dependencies

Tickets are the home of each phase 1 goal's scope and acceptance.

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | State / blocker |
| --- | --- | --- | --- | --- | --- | --- |
| [G01 Guidewire FNOL contract and replay evidence](../tickets/home-claim-intake/G01-guidewire-fnol-contract.md) | 1 | discovery | 20–30 | W1 | safe-api-tool-calls | blocked: W1 |
| [G02 Walking skeleton with pinned model](../tickets/home-claim-intake/G02-walking-skeleton.md) | 1 | implementation | 16–24 | — | adk-workflow-design | **ready** |
| [G03 GCP EU foundation](../tickets/home-claim-intake/G03-gcp-eu-foundation.md) | 1 | implementation | 30–46 | W3, G02 | deploy-adk-on-google-cloud | blocked: W3, G02 |
| [G04 Customer identity and policy entitlement](../tickets/home-claim-intake/G04-identity-and-entitlement.md) | 1 | implementation | 26–40 | G02, W2 | adk-tool-auth-and-secrets | blocked |
| [G05 Photo upload and sanitisation](../tickets/home-claim-intake/G05-photo-upload-sanitisation.md) | 1 | implementation | 24–38 | G02 | protect-adk-sensitive-data | blocked: G02 |
| [G06 Intake conversation and claim draft](../tickets/home-claim-intake/G06-intake-conversation-and-draft.md) | 1 | implementation | 40–60 | G02 | adk-agent-instructions | blocked: G02 |
| [G07 Evaluation harness and photo dev set](../tickets/home-claim-intake/G07-eval-harness-photo-set.md) | 1 | implementation | 26–40 | G02 | adk-agent-evaluation | blocked: G02 |
| [G08 Photo reader](../tickets/home-claim-intake/G08-photo-reader.md) | 1 | implementation | 30–46 | G05, G07 | adk-model-and-output-contracts | blocked |
| [G09 Confirmed submission and ledger](../tickets/home-claim-intake/G09-confirmed-submission-ledger.md) | 1 | implementation | 50–74 | G04, G06 | safe-api-tool-calls | blocked |
| [G10 Guidewire adapter and reconciliation](../tickets/home-claim-intake/G10-guidewire-adapter-reconciliation.md) | 1 | implementation | 26–40 | G01, G09 | safe-api-tool-calls | blocked |
| [G11 Budgets, allowances and kill switch](../tickets/home-claim-intake/G11-budgets-kill-switch.md) | 1 | implementation | 22–32 | G06 | adk-operational-guardrails | blocked |
| [G12 Customer chat panel in the portal](../tickets/home-claim-intake/G12-portal-chat-panel.md) | 1 | implementation | 62–93 | G05, W4 | adk-frontend-integration | blocked |
| [G13 Sensitive data, retention and erasure](../tickets/home-claim-intake/G13-sensitive-data-retention.md) | 1 | implementation | 32–48 | G03, G04, G05 | protect-adk-sensitive-data | blocked |
| [G14 Capability checks and adversarial suite](../tickets/home-claim-intake/G14-adversarial-suite.md) | 1 | implementation | 32–48 | G06, G08, G09 | adk-agent-security | blocked |
| [G15 DPIA and AI-transparency pack](../tickets/home-claim-intake/G15-dpia-pack.md) | 1 | discovery | 28–42 | — | adk-agent-security | **ready** |
| [G16 Observability and SLOs](../tickets/home-claim-intake/G16-observability-slos.md) | 1 | implementation | 26–38 | G02, G03 | adk-agent-observability | blocked |
| [G17 Release manifest, CI gate and canary](../tickets/home-claim-intake/G17-release-ci-gate.md) | 1 | implementation | 30–46 | G03, G06, G07, G08 | adk-release-engineering | blocked |
| [G18 Staging end to end against Guidewire non-prod](../tickets/home-claim-intake/G18-staging-end-to-end.md) | 1 | implementation | 28–42 | G10–G13, G16, G17 | deploy-adk-on-google-cloud | blocked |
| [G19 Security review: injection and output](../tickets/home-claim-intake/G19-security-review-injection.md) | 1 | review | 6–11 | G14, G25 | adk-agent-security | blocked |
| [G20 Load and resilience test](../tickets/home-claim-intake/G20-load-resilience.md) | 1 | implementation | 26–40 | G18, W5 | optimise-adk-on-google-cloud | blocked |
| [G21 Pen-test remediation](../tickets/home-claim-intake/G21-pentest-remediation.md) | 1 | implementation | 18–34 | W7 | adk-agent-security | blocked |
| [G22 Invite-only pilot](../tickets/home-claim-intake/G22-invite-only-pilot.md) | 1 | implementation | 36–55 | W6, G18, G19, G24 | adk-agent-evaluation | blocked |
| [G23 GA operations readiness](../tickets/home-claim-intake/G23-ga-operations-readiness.md) | 1 | implementation | 22–32 | G18, G20 | deploy-adk-on-google-cloud | blocked |
| [G24 Conversation evaluation set](../tickets/home-claim-intake/G24-conversation-eval-set.md) | 1 | implementation | 38–58 | G07, G17 | adk-agent-evaluation | blocked |
| [G25 Security review: identity and write boundaries](../tickets/home-claim-intake/G25-security-review-identity-write.md) | 1 | review | 8–13 | G04, G09 | adk-tool-auth-and-secrets | blocked |

Calendar waits, requested on day 1 unless they depend on a goal:

| Wait | What | Requested by | Days (assumed) |
| --- | --- | --- | --- |
| W1 | Guidewire non-prod tenant, API client, external-reference field | Eng B, day 1 | 10–20 |
| W2 | CIAM OIDC client registration | Eng E, day 1 | 5–10 |
| W3 | GCP EU projects from the landing-zone team | Eng D, day 1 | 5–10 |
| W4 | Legal review of the AI notice and customer wording (drafts from the design) | Eng C, day 1 | 10–15 |
| W5 | Guidewire non-prod load-test window | Eng B, day 1 | 10–20 |
| W6 | DPIA sign-off by the DPO, after G15 | Sec | 15–25 |
| W7 | External pen test window and report, after G18 and G19; vendor booked day 1 | Sec | 10–15 |
| W8 | Go-live approval by the change board, after G21–G23 | Eng D | 3–5 |

### Phase 2, harden or graduate

#### G30 Production samples into the eval set

Redacted, handler-corrected pilot and GA claims become eval cases monthly.
Primary skill adk-agent-observability; 16–28 h. Acceptance: the CI gate runs
at least 30 cases sampled from production with no personal data in the repo.

#### G31 Second EU market and language

Instructions, release-check rules, eval cases and legal wording for a second
market. Primary skill adk-agent-evaluation; 40–70 h. Acceptance: the new
language meets the same gate thresholds as the first.

#### G32 Mobile app channel

The same JSON API from the mobile app with its own photo capture. Primary
skill adk-frontend-integration; 40–60 h. Acceptance: a claim filed from the
app reaches Guidewire in staging with the same ledger guarantees.

#### G33 Cost and latency tuning from measured traffic

Context caching, photo token reduction, history shaping. Primary skill
optimise-adk-on-google-cloud; 16–30 h. Acceptance: tokens per submitted claim
fall with no drop in the gate's scores.

#### G34 Model migration rehearsal

Re-baseline on the next stable model with a side-by-side on the frozen set.
Primary skill adk-release-engineering; 12–20 h. Acceptance: a release manifest
with the new model passes the gate, and rollback to the old one is rehearsed.

## Later

| Item | Trigger that brings it forward | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| Model Armor input screening | A bypass in G14 or the pen test | Unscreened text reaches the model; structure limits the effect to a draft | protect-adk-sensitive-data |
| Multi-region failover | Availability target above 99.5% | Region outage sends customers to the form | deploy-adk-on-google-cloud |
| Claim status follow-up in chat | Product request after GA | Customers use the existing status page | adk-workflow-design |
| Cross-claim memory | Product need for previous claims | None | adk-memory-architecture |
| Shared token budget across replicas | Cost spikes in G20 or production | Per-invocation and per-customer limits only | adk-operational-guardrails |

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| [Design](../architecture/home-claim-intake.md) | Method, decisions, assumed answers |
| `evals/SUMMARY.md` (created in G07) | Latest result per case, linked to run records |
| This plan | Schedule, remaining limits and deferred controls |

## Open decisions for further planning

O1–O6 are in the design's open decisions. Those that move dates: O3 (about
12 working days), O1 (blocks G02's acceptance and G03's region), O2 (G10's
mechanism).

## Resume here

- **Next goal:** G02 Walking skeleton; it has no dependency. G15 is also
  ready, for the security reviewer, in parallel.
- **Read first:** the design, this plan, the G02 ticket.
- **Next action:** create the Python 3.11 project with google-adk pinned,
  confirm the pin and O1, and get the offline Runner test passing.
- **Continuation prompt:**

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G02-walking-skeleton.md.
Read docs/architecture/home-claim-intake.md and preserve its decisions.
Use adk-workflow-design with adk-model-and-output-contracts.
Work locally only, verify the ticket's acceptance cases, and record evidence
and remaining blockers in the ticket.
```

After that goal, `/adk-engineer Continue the next ready goal in docs/plans/home-claim-intake.md.`
