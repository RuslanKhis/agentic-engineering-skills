# Implementation plan: home-insurance claim intake agent (EU)

Status: draft. Ready goals are identified. The plan is **unreviewed by the user**,
and every decision rests on the assumed answers Q1–Q14 in the design. It was
reviewed once by an independent reviewer with a fresh context (findings
settled below).
Architecture: [docs/architecture/home-claim-intake.md](../architecture/home-claim-intake.md)
Continuation source of truth: this plan (schedule and goals table) and the
phase 1 tickets in [docs/tickets/home-claim-intake/](../tickets/home-claim-intake/)

## Summary for the reader

- **Profile and phase 1:** production service. Phase 1 is GA in Germany
  (German and English). Signed-in customers describe home damage, upload
  photos, confirm a server-rendered summary and get a ClaimCenter claim
  number; the photos land on the claim. Storm peaks and outages fall back to
  the prefilled classic form.
- **Effort and finish:** 573–853 human hours (agent-assisted, ×1.5 for a
  team new to ADK) against 2,208.75 h of capacity after a 25 % reserve.
  Finish is 67.27–102.47 working days against the 95 working days to
  Mon 2027-03-15. **It fits at the low end only.** Hours are not the
  constraint; they use about a third of capacity. The calendar is set by the
  chain G02 → G16 → G18 → G10 → G11 → pen test (W3) → G21 → retest (W8) →
  go-live approval (W6) → G22 → rollout soak (W11).
- **Recommended date:** GA on Thu **2027-03-25** (103 working days), which
  fits at the high end with 0.5 days of slack. The other remedies tried, in
  the what-if table, do not close the gap.
- **Largest risks:**
  1. The pen test or its retest slips. Any pen-test day over 15 breaks even
     the 103-day date. Book W3 and W8 on day 1.
  2. The Guidewire contract (dedup header, reference lookup, documents)
     differs from the documentation. G01 builds from the docs and a fake;
     G25 verifies live after W1 and G08 (it starts around day 26–39, not
     the moment W1 ends).
  3. `gemini-3.8-flash` or Model Armor may not be available in an EU region.
     G02/A6 and G12/A2 check this early. The fallback is `gemini-3.5-flash`,
     with a migration after GA.
- **Decisions needed from you:**
  - Confirm or correct Q1–Q14 in the design.
  - Accept residual risks R1–R3.
  - Choose between the GA date and the cut line below.
  - Send the day-1 requests: W1, W3 and W8 bookings, W5, W9, W10, W13, W16.
    W4 follows W13. W7, W14 and W15 follow G16.
- **Next prompt:** `/adk-engineer Carry out docs/tickets/home-claim-intake/G02-agent-service-skeleton.md.`
  G01, G13 and G15 are also ready on day 1, for Eng B, Eng E and the
  security reviewer.

## Destination and constraints

GA destination as in the summary. Non-goals and accepted stack: design
sections "Purpose and constraints" and D1–D16. Authorization: this session
produced design and plan only; no code, cloud resources, IAM, Guidewire
access or paid model calls are authorized by it. Each goal's execution scope
is in its ticket.

Inspected: the repository has no application code, manifest or lockfile;
every module path in the tickets is **proposed**. Inherited pins: ADK
`google-adk==2.8.0` (working assumption; G02/A6 confirms), model and judge
`gemini-3.8-flash` on Vertex AI EU (D3), prompt version `intake-v1` from G06.
A goal that changes one of these is a release (G19), not a side effect.

## Delivery profile and capacity

Profile: production service (design, "Delivery constraints").

| Phase | Delivers | Goals | Human hours, agent-assisted (range) | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship | GA in Germany, all floor and production controls | G01–G26, G33–G39; waits W1–W18 | 573–853 | 6 people × 5 h × 95 days + reviewer 1 h × 95 days, 25 % reserve → 2,208.75 h |
| 2, harden or extend | Second market, cross-device drafts, cost tuning, model migration, coverage guard | G27–G32 | 152–230 | After GA, with the slack phase 1 leaves |

Estimates are person-hours of human effort with a coding agent (hands-on
plus review and verify). They are assumptions for this team and already
include the ×1.5 for a team new to ADK. Calendar waits are the schedule
entries W1–W18; they carry no hours.

| Person or role | Goals | Hours | Their capacity |
| --- | --- | --- | --- |
| Eng A (agent lead) | G02, G06, G14, G18, G20, G36 | 107–162 | 356.25 |
| Eng B (Guidewire integration) | G01, G04, G08, G09, G25, G38 | 94–140 | 356.25 |
| Eng C (platform) | G05, G16, G17, G22, G35, G37 | 106–157 | 356.25 |
| Eng D (portal frontend, Guidewire adapter) | G34, G10, G11, G24 | 82–122 | 356.25 |
| Eng E (identity and data protection) | G03, G12, G13, G21, G33, G39 | 78–117 | 356.25 |
| ML engineer | G07, G19, G23 | 94–138 | 356.25 |
| Security reviewer (≈1 h/day) | G15, G26 | 12–17 | 71.25 |

**Calendar waits. Request every wait with no prerequisite on day 1
(2026-10-19).**

| Wait | What | After | Requested by | Working days |
| --- | --- | --- | --- | --- |
| W1 | Guidewire non-prod tenant access and API client | day 1 | Eng B | 10–20 |
| W2 | DPIA review and sign-off by the DPO | G12, G13 | Eng E | 15–25 |
| W3 | External pen test window and report; booked day 1 | feature-complete staging (G11, G12, G20, G26, G33, G37, G38) | Security reviewer | 10–15 |
| W4 | Vertex AI quota increase for the staging project | W13 | Eng C | 5–10 |
| W5 | Data owner approval for anonymised FNOL samples | day 1 | ML engineer | 10–20 |
| W6 | Go-live approval by claims operations and the change board, including signing accepted risks | G21, G23, W2, W8, W12, W17, W18 | Eng C | 3–5 |
| W7 | Guidewire production API client and IP allowlist | G16 (egress IP) | Eng B | 10–20 |
| W8 | External pen test retest; booked with W3 | G21 | Security reviewer | 3–5 |
| W9 | CIAM test tenant and client registration | day 1 | Eng E | 5–10 |
| W10 | Portal team change so the classic form accepts a prefilled draft | day 1 | Eng D | 10–20 |
| W11 | Rollout soak through the staff, 5 % and 50 % steps | G22 | Eng C | 3–6 |
| W12 | Cost-per-claim approval by finance | G20 | Eng A | 3–10 |
| W13 | Staging and production projects with budget alert, from the platform team | day 1 | Eng C | 2–5 |
| W14 | Vertex AI production quota increase | G16 | Eng C | 5–10 |
| W15 | Guidewire non-prod allowlist of the staging egress IP | G16 | Eng B | 10–20 |
| W16 | Booking of five claims handlers and the rubric with claims operations | day 1 | Eng D | 10–20 |
| W17 | Claims handlers' UAT review window | G24 | Eng D | 3–5 |
| W18 | Legal review of the AI Act classification, disclosure and privacy notice | G13 | Eng E | 10–20 |

Wait lengths for outside parties are assumptions until each party confirms.

Schedule block (the single source of each estimate; tickets copy it):

```yaml
- goal: W1
  phase: 1
  total: 0
  blocked_by: []
  calendar_waits: Guidewire non-prod tenant access and API client (access request)
  wait_days: 10-20
- goal: W2
  phase: 1
  total: 0
  blocked_by: [G12, G13]
  calendar_waits: DPIA review and sign-off by the DPO
  wait_days: 15-25
- goal: W3
  phase: 1
  total: 0
  blocked_by: [G11, G12, G20, G26, G33, G37, G38, G39]
  calendar_waits: External pen test window and report
  wait_days: 10-15
- goal: W4
  phase: 1
  total: 0
  blocked_by: [W13]
  calendar_waits: Vertex AI EU quota increase request
  wait_days: 5-10
- goal: W5
  phase: 1
  total: 0
  blocked_by: []
  calendar_waits: Data owner approval for anonymised FNOL samples (access request)
  wait_days: 10-20
- goal: W6
  phase: 1
  total: 0
  blocked_by: [G21, G23, W2, W8, W12, W17, W18]
  calendar_waits: Go-live approval by claims operations and change board
  wait_days: 3-5
- goal: W8
  phase: 1
  total: 0
  blocked_by: [G21]
  calendar_waits: External pen test retest of fixed findings
  wait_days: 3-5
- goal: W7
  phase: 1
  total: 0
  blocked_by: [G16]
  calendar_waits: Guidewire production API client and IP allowlist (access request)
  wait_days: 10-20
- goal: G01
  phase: 1
  hands_on: 10-14
  review: 2-4
  total: 12-18
  owner: Eng B
  blocked_by: []
- goal: G02
  phase: 1
  hands_on: 12-18
  review: 4-6
  total: 16-24
  owner: Eng A
  blocked_by: []
- goal: G03
  phase: 1
  hands_on: 10-15
  review: 6-9
  total: 16-24
  owner: Eng E
  blocked_by: [G02]
  handoff: 1
- goal: G04
  phase: 1
  hands_on: 8-12
  review: 4-6
  total: 12-18
  owner: Eng B
  blocked_by: [G01, G03, G34]
  handoff: 2
- goal: G05
  phase: 1
  hands_on: 14-20
  review: 5-8
  total: 19-28
  owner: Eng C
  blocked_by: [G02, G03, G16]
  handoff: 2
- goal: G06
  phase: 1
  hands_on: 16-24
  review: 5-8
  total: 21-32
  owner: Eng A
  blocked_by: [G02, W13]
  mentions_only: [G05, G12, W18]
- goal: G07
  phase: 1
  hands_on: 30-45
  review: 6-9
  total: 36-54
  owner: ML
  blocked_by: [W5, G02, G06]
  handoff: 1
- goal: G08
  phase: 1
  hands_on: 26-38
  review: 9-13
  total: 35-51
  owner: Eng B
  blocked_by: [G04, G34]
  handoff: 2
- goal: G09
  phase: 1
  hands_on: 14-20
  review: 6-9
  total: 20-29
  owner: Eng B
  blocked_by: [G05, G08]
  handoff: 1
- goal: G10
  phase: 1
  hands_on: 24-36
  review: 6-9
  total: 30-45
  owner: Eng D
  blocked_by: [G03, G05, G06, G18, W10]
  handoff: 2
- goal: G11
  phase: 1
  hands_on: 16-24
  review: 4-6
  total: 20-30
  owner: Eng D
  blocked_by: [G08, G10]
  handoff: 1
- goal: G12
  phase: 1
  hands_on: 14-20
  review: 4-7
  total: 18-27
  owner: Eng E
  blocked_by: [G05, G16, G18]
  handoff: 2
  mentions_only: [G09, G14]
- goal: G13
  phase: 1
  hands_on: 10-16
  review: 2-3
  total: 12-19
  owner: Eng E
  blocked_by: []
  mentions_only: [G12, wait]
- goal: G14
  phase: 1
  hands_on: 16-24
  review: 6-10
  total: 22-34
  owner: Eng A
  blocked_by: [G03, G06, G15]
  mentions_only: [G08, G12, wait]
  handoff: 1
- goal: G15
  phase: 1
  hands_on: 5-8
  review: 1-1
  total: 6-9
  owner: SecRev
  blocked_by: []
  mentions_only: [wait]
- goal: G16
  phase: 1
  hands_on: 30-44
  review: 9-13
  total: 39-57
  owner: Eng C
  blocked_by: [G02, W13]
  handoff: 1
- goal: G17
  phase: 1
  hands_on: 12-19
  review: 4-6
  total: 16-25
  owner: Eng C
  blocked_by: [G08, G16]
  handoff: 1
- goal: G18
  phase: 1
  hands_on: 16-24
  review: 6-9
  total: 22-33
  owner: Eng A
  blocked_by: [G06, G16, W10]
  handoff: 1
- goal: G19
  phase: 1
  hands_on: 18-26
  review: 6-9
  total: 24-35
  owner: ML
  blocked_by: [G07, G14, G16, G17]
  handoff: 2
- goal: G20
  phase: 1
  hands_on: 16-24
  review: 6-9
  total: 22-33
  owner: Eng A
  blocked_by: [G09, G12, G18, G25, G35, W4, W15]
  handoff: 2
- goal: G21
  phase: 1
  hands_on: 14-22
  review: 6-9
  total: 20-31
  owner: Eng E
  blocked_by: [W3]
  mentions_only: [wait]
- goal: G22
  phase: 1
  hands_on: 18-26
  review: 6-9
  total: 24-35
  owner: Eng C
  blocked_by: [G19, W6, W7, W14]
  handoff: 2
- goal: G23
  phase: 1
  hands_on: 28-40
  review: 6-9
  total: 34-49
  owner: ML
  blocked_by: [G06, G07]
  handoff: 1
  mentions_only: [G19]
- goal: G24
  phase: 1
  hands_on: 12-18
  review: 4-6
  total: 16-24
  owner: Eng D
  blocked_by: [G09, G11, G16, G25, W15, W16]
  handoff: 1
  mentions_only: [G17]
- goal: G25
  phase: 1
  hands_on: 8-12
  review: 3-4
  total: 11-16
  owner: Eng B
  blocked_by: [G08, W1]
  handoff: 1
  mentions_only: [W7, W15]
- goal: G26
  phase: 1
  hands_on: 5-7
  review: 1-1
  total: 6-8
  owner: SecRev
  blocked_by: [G03, G08, G14, G15, G36]
  handoff: 1
  mentions_only: [wait]
- goal: G33
  phase: 1
  hands_on: 7-9
  review: 2-3
  total: 9-12
  owner: Eng E
  blocked_by: [G09, G12]
  handoff: 1
- goal: G34
  phase: 1
  hands_on: 12-17
  review: 4-6
  total: 16-23
  owner: Eng D
  blocked_by: [G01]
  handoff: 2
  mentions_only: [wait]
- goal: W9
  phase: 1
  total: 0
  blocked_by: []
  calendar_waits: CIAM test tenant and client registration (access request)
  wait_days: 5-10
- goal: W10
  phase: 1
  total: 0
  blocked_by: []
  calendar_waits: Portal team change so the classic form accepts a prefilled draft
  wait_days: 10-20
- goal: W11
  phase: 1
  total: 0
  blocked_by: [G22]
  calendar_waits: Rollout soak: staff, 5 % and 50 % steps each run long enough for their thresholds
  wait_days: 3-6
- goal: W12
  phase: 1
  total: 0
  blocked_by: [G20]
  calendar_waits: Cost-per-claim approval by finance (budget approval)
  wait_days: 3-10
- goal: W13
  phase: 1
  total: 0
  blocked_by: []
  calendar_waits: Platform team creates staging and production projects with budget alert (access request)
  wait_days: 2-5
- goal: W14
  phase: 1
  total: 0
  blocked_by: [G16]
  calendar_waits: Vertex AI production quota increase request
  wait_days: 5-10
- goal: W15
  phase: 1
  total: 0
  blocked_by: [G16]
  calendar_waits: Guidewire non-prod allowlist of the staging egress IP (access request)
  wait_days: 10-20
- goal: W16
  phase: 1
  total: 0
  blocked_by: []
  calendar_waits: Booking of five claims handlers and the completeness rubric with claims operations
  wait_days: 10-20
- goal: W17
  phase: 1
  total: 0
  blocked_by: [G24]
  calendar_waits: UAT review window for claims handlers
  wait_days: 3-5
- goal: W18
  phase: 1
  total: 0
  blocked_by: [G13]
  calendar_waits: Legal review of AI Act classification, disclosure and privacy notice (legal review)
  wait_days: 10-20
- goal: G35
  phase: 1
  hands_on: 4-5
  review: 1-2
  total: 5-7
  owner: Eng C
  blocked_by: [G09, G12, G17, G18]
  handoff: 2
  mentions_only: [G33]
- goal: G36
  phase: 1
  hands_on: 3-4
  review: 1-2
  total: 4-6
  owner: Eng A
  blocked_by: [G04, G08, G14]
  handoff: 1
- goal: G37
  phase: 1
  hands_on: 2-3
  review: 1-2
  total: 3-5
  owner: Eng C
  blocked_by: [G16, G34, W1]
  handoff: 1
- goal: G38
  phase: 1
  hands_on: 3-6
  review: 1-2
  total: 4-8
  owner: Eng B
  blocked_by: [G26]
  handoff: 1
  mentions_only: [wait]
- goal: G39
  phase: 1
  hands_on: 2-3
  review: 1-1
  total: 3-4
  owner: Eng E
  blocked_by: [G03, W9]
- goal: G27
  phase: 2
  hands_on: 48-72
  review: 12-18
  total: 60-90
  blocked_by: [G22]
- goal: G28
  phase: 2
  hands_on: 18-27
  review: 6-9
  total: 24-36
  blocked_by: [G22]
- goal: G29
  phase: 2
  hands_on: 12-18
  review: 4-6
  total: 16-24
  blocked_by: [G22]
- goal: G30
  phase: 2
  hands_on: 15-24
  review: 5-8
  total: 20-32
  blocked_by: [G22]
- goal: G31
  phase: 2
  hands_on: 12-18
  review: 4-6
  total: 16-24
  blocked_by: [G22]
- goal: G32
  phase: 2
  hands_on: 11-17
  review: 5-7
  total: 16-24
  blocked_by: [G22]
```

Schedule check, run 2026-10-15 with
`python3.11 .claude/skills/adk-system-designer/scripts/check_schedule.py --plan docs/plans/home-claim-intake.md --tickets docs/tickets/home-claim-intake/ --design docs/architecture/home-claim-intake.md --days 95 --reserve 0.25 --person "Eng A=5" --person "Eng B=5" --person "Eng C=5" --person "Eng D=5" --person "Eng E=5" --person "ML=5" --person "SecRev=1"`:
573–853 h of 2,208.75 h. Longest chain G02 → G16 → G18 → G10 → G11 → W3 →
G21 → W8 → W6 → G22 → W11, 64.6–99 working days. Finish 67.27–102.47 of 95
days, low end only. Every grid cell cites an existing acceptance item; no
mentions are left to review. Exit status 1 (calendar). The same command with
`--days 103` exits 0.

**Changes after failing runs, the independent review, and what-ifs** (one
row each; figures are from the helper):

| Step | Change | Why it is true of the work | Finish (working days) |
| --- | --- | --- | --- |
| First run | — | — | 72.07–113.07 |
| Fix 1 | G01 builds the contract and a fake from documentation; live checks in new G25 after W1 | Integration can be built against a documented-contract fake | 66.07–99.2 |
| Fix 2 | Security review split: G15 reviews the design on day 1; G26 reviews code before the pen test | The design review needs no code | 66.07–99.2 |
| Fix 3 | G06 uses photo fixtures instead of waiting for G05 | The real pipeline is checked in G05/A3 | 66.07–99.2 |
| Fix 4 | G09 moved from Eng C to Eng B | Eng C's queue delayed G09 | 63.4–94.93 |
| Helper mentions | G12 needs G09; G14 needs G15; new W8 retest | Real prerequisites described in the text | 66.4–99.93 |
| Fix 5 | Erasure of filed photos split into G33 | Only that part needs transfer states | 66.4–99.93 |
| Fix 6 | Guidewire client and adapter split into G34 (Eng D) | Separate seam from the operation state machine | 63.47–95.4 |
| Fix 7 | G25 to Eng D | Shortened Eng B's queue at the time | 62.93–94.87 (later reversed, row R-C3) |
| R-P1 | Production network and egress IP applied in G16 (+5–7 h) so W7 can start | Without it W7 waited for G22 (reviewer: 72.93–114.87) | included below |
| R-P2 | G17's dashboards and runbook walkthrough moved to new G35 after G09, G12, G18 | They need the whole filing path | included below |
| R-P3 | Filing and policy adversarial cases moved to new G36 after G08; G26 waits for it | They need the operation store | included below |
| R-P4 | Secret rotation moved from G16 to new G37 after W1 | Needs the real Guidewire client | included below |
| R-P5 | New W9 for the CIAM tenant; tenant check split into G39 so G03 starts on local tokens | Only the real-tenant check needs W9 | included below |
| R-P6 | G10 waits for G06, G18 and portal-team wait W10; G18 waits for W10 | Disclosure text, `degraded` answer and form prefill are inputs | included below |
| R-P7 | Rollout soak W11 after G22 | Staged steps need calendar time | included below |
| R-P8–P12 | G12 waits for G18; G05 for G16; G20 for G12; G19 for G14 and G17; G07 for G06; cost approval W12 before W6 | Each acceptance item needs that input | included below |
| R-P13 | Project wait W13 before G16 and G06 (with budget alert); W4 after W13; production quota W14 | Quota and live runs need a project | included below |
| R-P14–P16 | W15 staging allowlist; W16 handler booking and W17 review window; W18 legal review before W6 | Outside parties act before those checks | included below |
| R-M4 | New G38 for fixing G26's findings (Eng B, 4–8 h) before W3 | Fixes had no hours | included below |
| R-M1, coverage | Grid re-cited: Model Armor untrusted content → new G12/A6; OIDC unavailable → new G03/A7; rejects → new G04/A7 and G12/A2 (4xx); revoked roles → new G16/A5; Cloud Tasks untrusted → new G08/A13; locked draft → new G08/A14; erasure resume → new G33/A4; staging Cloud SQL HA in G16/A1; two workers in G09/A3; draft lock in one transaction in G08/A1; token revocation bounded by lifetime (G03/A3, G39/A2) | Each cell now cites a test of what it claims | — |
| R-M2, M3 | W2 waits for G12; stale mention entries removed from G04 and G09 | DPIA inventory depends on G12's regions | — |
| After all review fixes | — | — | 68.07–104.73 |
| Fix 8 | G39 split (above); G33 writes its own runbook section, so G35 no longer waits for G33 | The erasure runbook belongs with erasure | 68.07–104.07 |
| R-C3, fix 9 | G25 back to Eng B, as the reviewer found | Eng D's queue now delays it | **67.27–102.47 (adopted)** |
| What-if: G05 to Eng E | Not adopted | No effect | 68.07–104.07 (before fix 9) |
| What-if: reviewer at 2 h/day | Not adopted | Reviewer off the chain | 68.07–104.07 (before fix 9) |
| What-if: G10 without waiting for G18 | Not adopted | G10/A4 needs `degraded` | 67.27–102.73 (before fix 9) |
| What-if: rollout soak after the GA date (W11 = 0) | Offered as a definition choice | GA would mean "rollout started" | 64.27–96.47; low end only |
| What-if: GA date 103 working days (2027-03-25) | **Recommended** | Keeps every floor item | 67.27–102.47; fits |
| What-if: pen test window 10–20 days | Risk only | Shows the slack | 67.27–107.47; low end only even at 103 days |
| What-if: G32 and G30 into phase 1 (ML after G06; Eng C after G20; both before W6) | Offered at the cut line | Off the chain | 67.27–102.47 at 609–909 h; same fit as without |
| What-if: G32 alone into phase 1 | Offered at the cut line | Off the chain | 67.27–102.47 at 589–877 h |

The reviewer's claim C-5 is accepted: "scope cuts do not help" was wrong,
because waits are only part of the chain. The goals now on the chain (G16,
G18, G10, G11) carry floor items: infrastructure, spend stop and fallback,
and the confirmation screen. None was cut to fit the date.

Phase 1 is ordered so each completed goal stays useful: G02 → G03 → G04 →
G34 → G08 is an end-to-end filing path on its own.

**Cut line and date (please choose):** ships at GA: G01–G26 and G33–G39.
Waits for phase 2: G27–G32 and the later list. With 95 working days the
plan fits only at the low end. The recommendation is GA on 2027-03-25. If
the date cannot move, the alternatives are to define GA as the start of the
staged rollout (still 96.47 days at the high end, so it does not close the
gap on its own), or to accept the risk of a late launch. Spare hours allow
G32 (deterministic coverage guard, ends R1) and G30 (cost tuning) to move
into phase 1 without changing the finish.

## Implementation map

Proposed greenfield layout (labelled proposed; nothing exists yet):
`app/api/` (FastAPI routes, auth middleware), `app/agent/` (agent factory,
instruction, tools), `app/drafts/` (ClaimDraft model, validator, store),
`app/photos/`, `app/submission/` (operation store, worker, sweeper),
`app/guidewire/` (client, adapter, fake), `app/guards/` (allowances, kill
switch), `infra/` (Terraform), `evals/`, `tests/`.

| Decision / requirement | ADK or application component and integration point | GCP service/responsibility | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |
| D1, D10 single agent, own-draft tools | `LlmAgent` built in `app/agent/factory.py`, run by `Runner` from the messages route; tools in `app/agent/tools.py` read `customer_id` and `draft_id` from trusted session state | Vertex AI model endpoint | `adk-workflow-design` | G02, G14 |
| D3 pinned model | `Gemini` model config from `app/config.py` + release manifest | Vertex AI EU region | `adk-model-and-output-contracts` | EU availability G02/A6 |
| D4 sessions and drafts | `DatabaseSessionService` + SQLAlchemy tables for drafts, photos, operations | Cloud SQL PostgreSQL | `adk-memory-architecture` | G02/A7 |
| D5 photos | Signed-URL route, finalize handler, derivative builder; image `Part`s attached to the turn | GCS, Eventarc or Pub/Sub notification | `protect-adk-sensitive-data` | G05 |
| D6 identity | Starlette middleware verifying the OIDC token; policy lookup service | CIAM; Secret Manager for Guidewire client | `adk-tool-auth-and-secrets` | G03, G04 |
| D7, D8 submission | Confirm route, operation store, Cloud Tasks worker route, sweeper; Guidewire client and adapter in `app/guidewire/` | Cloud Tasks, Cloud SQL | `safe-api-tool-calls` | G34, G08, G09, G25 |
| D9 sensitive data | Model Armor calls in `before_model_callback`/`after_model_callback` or around the Runner; logging filter; retention and erasure jobs | Model Armor, Cloud Scheduler, GCS lifecycle | `protect-adk-sensitive-data` | G12, G33 |
| D11, D12 portal | JSON API (turns, uploads, summary, confirm, status); React components in the existing portal | Existing BFF | `adk-frontend-integration` | G10, G11 |
| D13 budgets | `RunConfig.max_llm_calls`; allowance table checked before each invocation; kill switch flag | Cloud Run max instances, budgets | `adk-operational-guardrails` | G18, G20 |
| D14 telemetry | OTel setup in app start-up, one provider per process | Cloud Trace, Logging, Monitoring | `adk-agent-observability` | G17 |
| D15 release | CI workflow, manifest file, traffic split script | Cloud Run revisions, Artifact Registry | `adk-release-engineering` | G19 |
| D16 transparency | Static texts in `app/agent/texts/`; DPIA pack | — | `adk-agent-instructions` | G06, G13 |

## Goals and dependencies

Each phase 1 ticket is the home of its scope, route and acceptance.

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | State / blocker |
| --- | --- | --- | --- | --- | --- | --- |
| [G01 Guidewire contract and fake from documentation](../tickets/home-claim-intake/G01-guidewire-contract-and-fake.md) | 1 | discovery | 12–18 | — | `safe-api-tool-calls` | ready |
| [G02 Agent service skeleton](../tickets/home-claim-intake/G02-agent-service-skeleton.md) | 1 | implementation | 16–24 | — | `adk-workflow-design` | ready |
| [G03 Customer identity and draft ownership](../tickets/home-claim-intake/G03-identity-and-ownership.md) | 1 | implementation | 16–24 | G02 | `adk-tool-auth-and-secrets` | proposed |
| [G04 Policy lookup and selection](../tickets/home-claim-intake/G04-policy-lookup.md) | 1 | implementation | 12–18 | G01, G03, G34 | `adk-tool-auth-and-secrets` | proposed |
| [G05 Photo upload and model-ready derivatives](../tickets/home-claim-intake/G05-photo-upload.md) | 1 | implementation | 19–28 | G02, G03, G16 | `protect-adk-sensitive-data` | proposed |
| [G06 Intake conversation](../tickets/home-claim-intake/G06-intake-conversation.md) | 1 | implementation | 21–32 | G02, W13 | `adk-agent-instructions` | proposed |
| [G07 Evaluation set and harness](../tickets/home-claim-intake/G07-evaluation-set.md) | 1 | implementation | 36–54 | W5, G02, G06 | `adk-agent-evaluation` | proposed |
| [G08 Confirmed, idempotent claim filing](../tickets/home-claim-intake/G08-claim-filing.md) | 1 | implementation | 35–51 | G04, G34 | `safe-api-tool-calls` | proposed |
| [G09 Photo transfer to the filed claim](../tickets/home-claim-intake/G09-photo-transfer.md) | 1 | implementation | 20–29 | G05, G08 | `safe-api-tool-calls` | proposed |
| [G10 Portal chat and upload](../tickets/home-claim-intake/G10-portal-chat.md) | 1 | implementation | 30–45 | G03, G05, G06, G18, W10 | `adk-frontend-integration` | proposed |
| [G11 Portal summary, confirm and status](../tickets/home-claim-intake/G11-portal-confirm-status.md) | 1 | implementation | 20–30 | G08, G10 | `adk-frontend-integration` | proposed |
| [G12 Sensitive data, retention, erasure, residency](../tickets/home-claim-intake/G12-sensitive-data.md) | 1 | implementation | 18–27 | G05, G16, G18 | `protect-adk-sensitive-data` | proposed |
| [G13 DPIA and transparency input](../tickets/home-claim-intake/G13-dpia-input.md) | 1 | discovery | 12–19 | — | `protect-adk-sensitive-data` | ready |
| [G14 Threat model and adversarial suite](../tickets/home-claim-intake/G14-threat-model.md) | 1 | implementation | 22–34 | G03, G06, G15 | `adk-agent-security` | proposed |
| [G15 Security design review](../tickets/home-claim-intake/G15-security-design-review.md) | 1 | review | 6–9 | — | `adk-agent-security` | ready |
| [G16 Staging and production infrastructure](../tickets/home-claim-intake/G16-infrastructure.md) | 1 | implementation | 39–57 | G02, W13 | `deploy-adk-on-google-cloud` | proposed |
| [G17 Telemetry, SLIs and alerts](../tickets/home-claim-intake/G17-observability.md) | 1 | implementation | 16–25 | G08, G16 | `adk-agent-observability` | proposed |
| [G18 Budgets, admission, kill switch, form fallback](../tickets/home-claim-intake/G18-budgets-fallback.md) | 1 | implementation | 22–33 | G06, G16, W10 | `adk-operational-guardrails` | proposed |
| [G19 Release pipeline](../tickets/home-claim-intake/G19-release-pipeline.md) | 1 | implementation | 24–35 | G07, G14, G16, G17 | `adk-release-engineering` | proposed |
| [G20 Staging resilience and storm-surge test](../tickets/home-claim-intake/G20-resilience-test.md) | 1 | implementation | 22–33 | G09, G12, G18, G25, G35, W4, W15 | `optimise-adk-on-google-cloud` | proposed |
| [G21 Pen test remediation](../tickets/home-claim-intake/G21-pentest-remediation.md) | 1 | implementation | 20–31 | W3 | `adk-agent-security` | proposed |
| [G22 Production launch and staged rollout](../tickets/home-claim-intake/G22-production-launch.md) | 1 | implementation | 24–35 | G19, W6, W7, W14 | `deploy-adk-on-google-cloud` | proposed |
| [G23 Quality iteration to the release threshold](../tickets/home-claim-intake/G23-quality-iteration.md) | 1 | implementation | 34–49 | G06, G07 | `adk-agent-evaluation` | proposed |
| [G24 Claims-handler UAT and completeness baseline](../tickets/home-claim-intake/G24-claims-handler-uat.md) | 1 | implementation | 16–24 | G09, G11, G16, G25, W15, W16 | `adk-agent-evaluation` | proposed |
| [G25 Live Guidewire contract verification](../tickets/home-claim-intake/G25-guidewire-live-verification.md) | 1 | discovery | 11–16 | G08, W1 | `safe-api-tool-calls` | blocked: W1 |
| [G26 Security code review before pen test](../tickets/home-claim-intake/G26-security-code-review.md) | 1 | review | 6–8 | G03, G08, G14, G15, G36 | `adk-agent-security` | proposed |
| [G33 Photo retention and erasure after filing](../tickets/home-claim-intake/G33-photo-retention-after-filing.md) | 1 | implementation | 9–12 | G09, G12 | `protect-adk-sensitive-data` | proposed |
| [G34 Guidewire client and claims/documents adapter](../tickets/home-claim-intake/G34-guidewire-adapter.md) | 1 | implementation | 16–23 | G01 | `safe-api-tool-calls` | proposed |
| [G35 Dashboards and runbook walkthrough](../tickets/home-claim-intake/G35-dashboards-and-runbook.md) | 1 | implementation | 5–7 | G09, G12, G17, G18 | `adk-agent-observability` | proposed |
| [G36 Adversarial filing and policy cases](../tickets/home-claim-intake/G36-adversarial-filing-cases.md) | 1 | implementation | 4–6 | G04, G08, G14 | `adk-agent-security` | proposed |
| [G37 Guidewire secret rotation](../tickets/home-claim-intake/G37-secret-rotation.md) | 1 | implementation | 3–5 | G16, G34, W1 | `adk-tool-auth-and-secrets` | proposed |
| [G38 Fixes from the internal code review](../tickets/home-claim-intake/G38-pre-pentest-fixes.md) | 1 | implementation | 4–8 | G26 | `adk-agent-security` | proposed |
| [G39 CIAM test-tenant check](../tickets/home-claim-intake/G39-ciam-tenant-check.md) | 1 | implementation | 3–4 | G03, W9 | `adk-tool-auth-and-secrets` | proposed |

### Phase 2 (after GA; coarse until phase 1 has run)

- **G27 Second market and language.** Outcome: a second EU market (assumed
  France or the Netherlands) files claims in its language. Primary
  `adk-agent-instructions`; supporting `adk-agent-evaluation`. 60–90 h.
  Acceptance A1: the new-language held-out set meets T3.
- **G28 Resume a draft across devices, with abandoned-draft reminder.**
  Primary `adk-memory-architecture`. 24–36 h. Acceptance A1: a draft started
  on mobile continues on desktop for the same customer and is denied to
  another.
- **G29 Production samples into the evaluation set.** Primary
  `adk-agent-observability`; supporting `adk-release-engineering`. 16–24 h.
  Acceptance A1: a monthly redacted sample of 30 sessions becomes labelled
  cases the G19 gate runs.
- **G30 Cost and latency tuning.** Primary `optimise-adk-on-google-cloud`.
  20–32 h. Acceptance A1: tokens per filed claim fall at least 20 % with no
  T3 regression, measured on captured requests.
- **G31 Model migration rehearsal.** Primary `adk-release-engineering`;
  supporting `adk-model-and-output-contracts`. 16–24 h. Acceptance A1: a
  side-by-side on the frozen development set for the next stable Gemini
  model, released as its own change.
- **G32 Deterministic coverage-statement guard (ends R1).** Primary
  `adk-model-and-output-contracts`. 16–24 h. Acceptance A1: replies on
  coverage, amounts or liability are replaced by a reviewed template; 0
  model-authored coverage statements on the adversarial set.

## Later

| Item | Trigger that brings it forward | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| CMEK on Cloud SQL and GCS | Security or regulator requirement (Q14) | Google default encryption only | `deploy-adk-on-google-cloud` |
| Multi-region failover | Availability target above 99.5 % or a regional incident | R3 | `deploy-adk-on-google-cloud` |
| Photo authenticity and fraud signals | Claims fraud lead asks, or a fraud pattern via digital channel | R2 | `adk-agent-security` |
| AI photo notes for adjusters | Claims operations ask; needs AI Act and bias assessment | Adjusters view raw photos only | `adk-model-and-output-contracts` |
| Native app and voice channels | Product roadmap | Web and mobile web only | `adk-frontend-integration` |
| Other lines (contents, motor) | Product roadmap | Home only | `adk-system-designer` |

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| [Design](../architecture/home-claim-intake.md) | Method, decisions D1–D16, invariants, failure grids |
| `evals/summary.md` (created by G07) | Latest result per case, linked to raw runs |
| This plan | Schedule, remaining limits and deferred controls |

## Open decisions for further planning

| Decision / question | Known facts and alternatives | Evidence or user decision needed | Blocks which goals? |
| --- | --- | --- | --- |
| GA date | 95 days fits low end only; 103 days (2027-03-25) fits | You choose | G22 |
| Assumed answers Q1–Q14 | Design, "Assumed answers" | Product owner confirms | Re-plan if changed |
| Residual risks R1–R3 | Design, "Delivery constraints" | Claims product owner accepts | W6 |
| Cut line | G32 and G30 fit in spare hours | You confirm or move | None now |
| Outside wait lengths W1–W18 | All assumed | Each party confirms | Finish range |
| Guidewire dedup semantics | Documented header vs. reference lookup | G01, then G25 live | G08 final acceptance |
| Model and Model Armor in an EU region | Lifecycle table 2026-10-08; regional pages not checked | G02/A6, G12/A2 | Model path in staging |

## Resume here

- **Next goal:** G02 Agent service skeleton. It has no prerequisites, and
  the rest of the agent path builds on it. G01, G13 and G15 are ready in
  parallel.
- **Read first:** the design, this plan, the G02 ticket.
- **Next action:** confirm the ADK pin and the model's EU availability
  (G02/A6), then build the scripted-model Runner test.
- **Continuation prompt:**

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G02-agent-service-skeleton.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

After that goal, the same request without a goal ID continues with the next
ready one: `/adk-engineer Continue the next ready goal in docs/plans/home-claim-intake.md.`

## Change table

| Version | Change | Removed or weakened (reason) |
| --- | --- | --- |
| 2026-10-15 v1 | First draft, schedule fits (62.93–94.87) | — |
| 2026-10-15 v2 | Independent review settled (rows R-… above): new goals G35–G39, waits W9–W18, re-cited grid cells; finish 67.27–102.47, low end only | G17/A2 and A4 moved to G35/A1–A2; G16/A5 (rotation) moved to G37/A1; G12/A6 (erasure while pending) moved to G33/A2 in v1; G03/A1 now uses local tokens, with the real-tenant check in G39/A1. Nothing was removed without a new home. Grid cells changed from n/a to cited tests: OIDC unavailable, credential revoked for Vertex, Model Armor, Cloud SQL and Cloud Tasks, Cloud Tasks untrusted content |
