# Statement of work: claims triage assistant pilot

Status: proposal (valid until 2026-11-27†)
Client: Fenwick Mutual (signatory: Helen Okafor, Head of Claims Operations†) · Supplier: Larkspur Digital (signatory role to be confirmed)
Version: 0.1 draft, 2026-10-27 · Change requests incorporated: none

Built from (the SOW restates nothing these hold; it cites them):

- Discovery brief: docs/discovery/claims.md, accepted 2026-09-29
- Design: docs/architecture/claims.md, accepted 2026-10-06; contracts `C1`–`C5`
- Plan: docs/plans/claims.md; schedule block summed by hand on 2026-10-27 because the scripts could not be run (see OD1): phase 1 = 21-33 human hours
- Assumed start date for converting working days to dates: Monday 2026-11-02† (labelled assumption; weekends skipped, client holidays not known)

## Open decisions before sending (agency only; remove from the client copy)

| ID | What the inputs lack or contradict | Change needed (plan, design, SOW) | Who decides |
| --- | --- | --- | --- |
| OD1 | `check_schedule.py` and `check_sow.py` were not run (no shell in this session). Hours were summed by hand from the schedule block: low 4+4+4+3+3+3 = 21, high 5.5+6.5+5.5+5+4+6.5 = 33, matching the plan. | Run both checks before sending and fix any difference. | Tom Reid |
| OD2 | The plan has no statement of work goal, no rollout or operations handover goal and no teardown goal. The Later list holds the decommission (Cloud SQL `fm-claims-pilot-sql`, about £1.60 per day idle) with trigger "pilot stops or moves to production", and the plan's Resources row says it is "owned by the cost contract (Later)", but the design has no cost contract (C5 is a spend stop). Nothing owns ending the idle cost. | Add a SOW goal, a pilot handover goal and a teardown goal to the plan and price them. Until then the SOW prices only G01–G06 and says so. | Tom Reid with Helen Okafor |
| OD3 | The scope gate records real personal data and the profile is pilot. The plan has no governance goal (`adk-governance-pack`) and no wait for DPIA or legal review. | Add a governance goal before G06 and a calendar wait for DPIA sign-off. Fees and finish dates will rise by an amount not yet estimated. | Tom Reid; Fenwick Mutual DPO |
| OD4 | Phase 1 ends at the pilot approval review, before the four pilot weeks the brief needs to judge "median ≤ 15 minutes with re-routing ≤ 9 %". The brief's outcome therefore cannot be an acceptance criterion in this SOW. | Either add a pilot-measurement goal and a phase for the four weeks, or confirm the measurement is client-run and outside this SOW. Drafted here as client-run (assumption A6). | Helen Okafor |
| OD5 | Only G01 and G03 have full goal entries. G02 (A3 is cited by security rule SB03 in the design), G04, G05 and G06 have none, so their acceptance text, resources and prerequisites are not in the plan. The acceptance criteria for those goals below are proposals (†). | Write the goal entries, then confirm or replace the AC thresholds. | Tom Reid |
| OD6 | The plan gives no gold-case counts, thresholds or dates, and no date for the pilot approval review (the plan's one decision needed from the client). All thresholds, case counts and dates below are † proposals. | Settle in the plan; client to give the review date. | Helen Okafor; Tom Reid |
| OD7 | Pinned models `gemini-3.5-flash-001` and `gemini-3.5-pro-001` (D2): no model lifecycle table was found in the installed skill assets, so retirement dates are unchecked. | Check retirement dates against the lifecycle table or Google's published schedule before sending. | Tom Reid |
| OD8 | Run cost is only partly in the plan: Cloud SQL idle cost is recorded; Cloud Run, BigQuery, Vertex AI and Sensitive Data Protection are not estimated, and the daily spend cap amount (C5) is not stated. | Add the cost ledger and the cap amount to the plan. | Tom Reid; Helen Okafor |
| OD9 | The plan's `handoff` hours (G05 1-2, G06 0.5-1; total 1.5-3 h) are not in the 21-33 h total. I treated them as elapsed calendar time between people, not billable effort. | Confirm this treatment. If they are billable, add 1.5-3 h (£142.50-£285.00). | Tom Reid |
| OD10 | Rate £95 per hour supplied by the requester. Whether it includes VAT, and whether it applies to a later phase, was not stated. Assumed: ex VAT, one rate for all phases. | Confirm. | Tom Reid |

Figures marked † are proposals until the plan holds them.

## 1. Objectives

From the discovery brief:

- **Outcome:** median triage time per claim on pilot home claims, from the claims MI report, measured over the four pilot weeks by Fenwick Mutual.
- **Baseline:** 21 minutes (August 2026 sample of 400 claims, claims MI report).
- **Target:** 12 minutes or less on pilot claims; a hypothesis until measured. Threshold to continue: median at or below 15 minutes after four pilot weeks.
- **Counter-metric:** re-routing after triage must not rise above the 9 % baseline.
- **Decider:** Helen Okafor.

Phase 1 delivers a draft triage recommendation (type, urgency, cover position citing the clause relied on) to 14 Leeds triage handlers on new home claims, for the handler to accept or change, and ends with the pilot approval review. The outcome above is measured during the pilot, not by this SOW (OD4, A6).

## 2. Deliverables

| ID | Deliverable | Plan goals | Phase | Acceptance |
| --- | --- | --- | --- | --- |
| DL1 | Triage draft (type and urgency) from a de-identified notification | G01 | 1 | AC1, AC2 |
| DL2 | Cover position citing the policy clause relied on, read-only | G02 | 1 | AC3, AC4 |
| DL3 | Team-scoped handler queue, claim history and the daily spend stop | G03, G04 | 1 | AC5, AC6 |
| DL4 | Reviews and close-out: journey check and pilot approval presentation | G05, G06 | 1 | AC7, AC8 |

Not yet included (OD2): statement of work goal, handover, teardown, governance papers.

## 3. Acceptance criteria

All thresholds, counts and dates are † proposals (OD6). Gold cases are labelled by Fenwick Mutual's two team leads.

| ID | Criterion | Threshold | Cases | Method | Measured by | Date | Contracts |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AC1 | A notification returns a draft with a type and urgency | ≥ 90% of cases return both fields | 40† gold notifications agreed with the two team leads by 2026-11-13† | `python -m unittest tests.test_draft` with a recorded model double, then the same set on the release build | Larkspur runs; Fenwick team lead witnesses | 2026-11-20† | C4 |
| AC2 | De-identification: no name, phone or email reaches the model request | 0 of 20† canary notes leak | 20† canary notes with names, phones and emails in free text, written by Larkspur, reviewed by a team lead | Canary test: inspect the model request | Larkspur | 2026-11-20† | C4 |
| AC3 | Every cover position cites a clause from that policy's own wording, or says none found | 0 of 40† positions uncited | 40† gold claims with policies, agreed by 2026-11-13† | Output validator plus citation test | Larkspur; Fenwick handler samples 10 | 2026-11-24† | C2 |
| AC4 | The assistant never changes a claim | 0 write tools bound; 0 of 10† write attempts succeed | tool inventory and 10† adversarial prompts | Tool inventory test; credential confirmed read-only | Larkspur; Raj Mehta witnesses | 2026-11-24† | C3 |
| AC5 | A handler sees only their team's claims | 0 of 20† cross-team requests return a claim (all 404) | 20† requests across 2 teams | Owner test with team-scoped fixtures | Larkspur | 2026-11-20† | C1 |
| AC6 | Spend stops at the daily cap | 1 of 1 cap-exceeded runs returns the fixed refusal; quota and max bytes billed set | 1 configuration plus 1 simulated breach | Config test | Larkspur | 2026-11-20† | C5 |
| AC7 | Journey check: new claim to accepted draft, wrong-team handler refused | ≥ 9 of 10† journey cases pass; 0 contract violations | 10† cases | Journey evaluation (G05) | Larkspur; Fenwick witnesses | 2026-11-25† | C1, C2, C3, C4, C5 |
| AC8 | Pilot approval presentation delivered with evidence | 0 of 1 decks with an uncited claim | 1 deck | deck check exit 0 | Larkspur | pilot approval review date (to be given by client) | none (presentation) |

Re-acceptance: AC1–AC3 and AC7 re-run after a model, prompt or tool-schema change. Who pays is open (section 9).

## 4. Out of scope

| Item | Trigger that would bring it in |
| --- | --- |
| Motor claims | Home pilot meets its threshold |
| Recurring cost review | First monthly bill of the pilot project |
| Decommission: delete `fm-claims-pilot-sql`, BigQuery dataset `claims_pilot` and the Cloud Run service (backups retained 7 days) | Pilot stops or moves to production (see OD2) |
| Production hardening (SB05, HA database, alerting) | Pilot approval |
| Measuring the four-week pilot outcome | Client-run unless a goal is added (OD4) |
| Settling or paying claims; any write to the policy or claims system | Not planned; would change C3 |

## 5. Client dependencies

Dates assume start 2026-11-02†.

| ID | Dependency | Owner | Needed by | Blocks | From plan |
| --- | --- | --- | --- | --- | --- |
| CD1 | Read-only policy API credential for `fm-claims-pilot`; request sent on signature, 5-10 working days | Raj Mehta, Policy Systems Manager | 2026-11-09† (arrives 9-16 Nov if requested on 2 Nov; later than 16 Nov moves the finish) | G02 | W1 |
| CD2 | Client security review before the pilot approval, 3-5 working days; start when G05 completes | Fenwick Mutual security reviewer (name to be given) | review requested by 2026-11-20†, done by 2026-11-27† | G06 | W2 |
| CD3 | Date of the pilot approval review | Helen Okafor | 2026-11-06† | G06 | plan, decisions needed |
| CD4 | Two team leads label 40† gold cases (about 4† hours each) | Helen Okafor to name | 2026-11-13† | AC1, AC3 | brief, People |
| CD5 | Access to `fm-claims-pilot` (europe-west2) with billing, and IAM to create Cloud SQL, BigQuery and Cloud Run | Fenwick Mutual GCP project owner (to be named) | 2026-11-02† | G03, G04 | design D5; goal G03 resources |
| CD6 | Claim notifications and policy records for evaluation (personal data, minimum scope) | Raj Mehta / Helen Okafor | 2026-11-09† | G01, G02 | design scope gate |

The data request letter was not drafted in this run (see summary); it should go the week the SOW is signed.

## 6. Effort, fees and run cost

Hours are the schedule block's human-hour ranges (agent-assisted), summed by hand (OD1). The £95 per hour rate was supplied by the requester on 2026-10-27; assumed ex VAT (OD10).

| Phase | Goals | Human hours | Rate per hour | Fees |
| --- | --- | --- | --- | --- |
| 1 | G01–G06 | 21-33 | £95 | £1,995.00–£3,135.00 |
| Total | | 21-33 | | £1,995.00–£3,135.00 |

Per developer (plan): Tom Reid (G01, G02, G05) 11-16 h; Sara Lin (G03, G04, G06) 10-17 h. Phase 2 is not estimated and not priced.

Pricing basis†: time and materials, capped at the high end (£3,135.00), no contingency, ex VAT. Calendar finish: 11-20 working days including W1 and W2, that is about 2026-11-16 to 2026-11-27† from the assumed start.

Run cost (estimate, incomplete, OD8): Cloud SQL `fm-claims-pilot-sql` about £1.60 per day idle, about £48 per 30-day month (Google pricing page read 2026-10-05). Cloud Run, BigQuery, Vertex AI and Sensitive Data Protection are not estimated. Daily spend ceiling is enforced by C5; the amount is not yet set. Billed to Fenwick Mutual's project `fm-claims-pilot` (D5)†.

## 7. Assumptions

| Assumption | If wrong, changes |
| --- | --- |
| A1 Start 2026-11-02 | all dates; CD needed-by dates |
| A2 W1 credential arrives within 5-10 working days of request | G02 start; finish range |
| A3 Two developers are available at 30 h each, as in the plan | finish range; phase 1 fit (45 h capacity vs 33 h high) |
| A4 One rate, £95, ex VAT, all phases | fees |
| A5 Handoff hours are elapsed time, not billable (OD9) | hours and fees (+1.5-3 h) |
| A6 Four-week pilot measurement is client-run and not in this SOW (OD4) | scope, phase 2, fees |
| A7 Gold and canary case counts (40, 20, 10) are acceptable to the client | AC1–AC7; CD4 hours |
| A8 Real personal data is used only in `fm-claims-pilot`, in europe-west2 | governance goal; data request |
| A9 Only G01–G06 are priced; goal entries for G02, G04–G06 are completed before signature (OD5) | estimates |

## 8. Change control

Change triggers (each starts a change request naming the contracts, goals, acceptance criteria, dependencies and estimates it changes, from an updated plan):

- CD1 arrives after 2026-11-16† (changes G02, finish range)
- CD2 or CD3 slip past their dates (changes G06, finish)
- more than 40 gold cases, or motor claims or a second channel requested (changes AC1–AC3, G01–G05 estimates)
- a contract added or tightened, or the policy credential not read-only (C3)
- the pinned model is retired or replaced before the pilot approval (re-acceptance, D2)
- a governance, handover or teardown goal is added (OD2, OD3)
- any request from the Out of scope list

## 9. AI terms checklist

Counsel settles wording in the main agreement.

| Question | Answer | Owner |
| --- | --- | --- |
| Client data, prompts or conversations used to train or improve any model? | Open; the proposal is no, using Vertex AI under Fenwick Mutual's project settings to be confirmed | Fenwick Mutual DPO / Larkspur |
| Ownership of prompts, instructions, tool schemas, evaluation sets, gold cases, tuned artefacts; supplier's prior templates carved out? | Open | Counsel on both sides |
| Model or version change by the provider: who migrates, re-baselines and pays? | Open; pins in D2, retirement dates unchecked (OD7) | Counsel; Tom Reid |
| Acceptance re-run after a model or prompt change? | Yes for AC1–AC3, AC7; who pays is open | Tom Reid; Helen Okafor |
| Liability for model output and for actions after human approval | Open. Design: the handler decides and the assistant writes nothing to claims (D1, C3) | Counsel |
| AI Act role (provider or deployer), Article 50 disclosure owner | Open; Fenwick Mutual is the deployer in its own project, Larkspur's role to be confirmed | Counsel |
| High-risk use (Annex III)? | Not stated in the inputs. Triage of insurance claims is not obviously Annex III, but this is for counsel to confirm | Counsel |
| Explanation of an individual output to an affected person | Open; each draft cites its clause (C2), and a handler decides | Helen Okafor |
| Subprocessors and data location | Vertex AI (Gemini), Sensitive Data Protection, Cloud Run, Cloud SQL, BigQuery, all in `fm-claims-pilot`, europe-west2 (D5). Location of Larkspur staff with access not stated | Fenwick Mutual DPO; Larkspur |
| Return and deletion at the end | Open; no teardown goal in the plan (OD2) | Tom Reid; Fenwick Mutual DPO |

Reference: EU model contractual clauses for AI procurement (MCC-AI), Public Buyers Community, published 5 March 2025.

## 10. Acceptance of this statement of work

| Party | Name and role | Date |
| --- | --- | --- |
| Client | | |
| Supplier | | |
