# Statement of work: <engagement name>

Status: proposal (valid until <date>) / for signature / signed <date>
Client: <organisation, signatory role> · Supplier: <organisation, signatory role>
Version: <n>, <date> · Change requests incorporated: <CR IDs or none>

Built from (the SOW restates nothing these hold; it cites them):

- Discovery brief: <path and date>
- Design: <path, version>; contracts `C1`–`Cn`
- Plan: <path>; schedule check run `<command>` on <date>: <phase totals>
- Assumed start date for converting working days to dates: <date>

## Open decisions before sending (agency only; remove from the client copy)

| ID | What the inputs lack or contradict | Change needed (plan, design, SOW) | Who decides |
| --- | --- | --- | --- |
| OD1 | <e.g. pinned model retires mid-engagement; no handover goal> | | |

Figures marked † are proposals until the plan holds them.

## 1. Objectives

From the discovery brief's outcome measure:

- **Outcome:** <metric>, measured <how>, over <window>, by <whom>.
- **Baseline:** <value, source, date> or "to be measured in <goal ID>".
- **Target for this engagement:** <value and date>, a hypothesis until measured.
- **Counter-metric:** <what must not get worse, with its threshold>.

What this engagement delivers towards it, in one sentence per phase.

## 2. Deliverables

Every goal in a priced phase belongs to exactly one deliverable. Reviews,
presentations and teardown are deliverables too.

| ID | Deliverable | Plan goals | Phase | Acceptance |
| --- | --- | --- | --- | --- |
| DL1 | <what the client receives, in their words> | G01, G02 | 1 | AC1, AC2 |
| DL2 | Reviews and close-out: <presentations, teardown or handover> | G05, G06 | 1 | AC3 |

## 3. Acceptance criteria

A measured rate on an agreed set, never "the agent answers correctly".

| ID | Criterion | Threshold | Cases | Method | Measured by | Date | Contracts |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AC1 | <behaviour, e.g. grounded answer to a claims question> | ≥ <n>% pass | <n> gold cases agreed with <client role> by <date> | <evaluator, rubric, build, repeats> | <who runs; who witnesses> | <YYYY-MM-DD> | C2 |
| AC2 | <forbidden effect, e.g. no email sent without approval> | 0 of <n> | <n> adversarial cases | <deterministic check> | <who> | <YYYY-MM-DD> | C4 |
| AC3 | <presentation delivered with evidence> | 0 of <n> decks with an uncited claim | <n> decks | deck check exit 0 | <who> | <YYYY-MM-DD> | none (presentation) |

Re-acceptance: <which criteria re-run after a model, prompt or tool-schema
change, and who pays for it>.

## 4. Out of scope

From the plan's Later list and deferred controls. A request for any of these
is a change request.

| Item | Trigger that would bring it in |
| --- | --- |

## 5. Client dependencies

Each from the plan's calendar waits and prerequisites; a date missed moves
the plan and is a change trigger.

| ID | Dependency | Owner | Needed by | Blocks | From plan |
| --- | --- | --- | --- | --- | --- |
| CD1 | <SME hours: n per week for gold cases> | <client role> | <YYYY-MM-DD> | G03 | W1 |
| CD2 | <read access to the claims export, scope> | <client role> | <YYYY-MM-DD> | G02 | G02 prerequisites |
| CD3 | <IAM grant / GCP project with billing> | <client IT role> | <YYYY-MM-DD> | G04 | W2 |

The data request letter (`data-request.md`, drafted with this SOW from the
designer's data request template) lists each data set and grant in detail.

## 6. Effort, fees and run cost

Hours are the schedule check's human-hour ranges (agent-assisted). The rate
was supplied by <name> on <date>; nothing here assumes a rate.

| Phase | Goals | Human hours | Rate per hour | Fees |
| --- | --- | --- | --- | --- |
| 1 | G01–G06 | <low>-<high> | <currency amount, or rate to be supplied> | <low × rate>–<high × rate> |
| Total | | <low>-<high> | | <low>–<high> |

Pricing basis: time and materials up to the high end / fixed at <amount>,
<contingency as the user chose>.

Run cost (estimate, list prices on <pricing date>, from the plan's cost
ledger): <per month per environment; per conversation or unit>; model spend
ceiling <amount> enforced by <cost contract ID>; billed to <client billing
account / supplier, re-charged>.

## 7. Assumptions

| Assumption | If wrong, changes |
| --- | --- |
| <e.g. the export arrives as one CSV per month> | <G02 estimate; CD2 date> |

## 8. Change control

Change triggers (each starts a change request in the agreed template):

- <CD1 lands after its date>
- <more than n gold cases or a second channel requested>
- <the pinned model is retired before go-live>
- <a contract added or tightened>

A change request cites the contracts, goals, acceptance criteria,
dependencies and estimates it changes, from an updated plan.

## 9. AI terms checklist

Answer each row or mark it open with an owner; counsel settles the wording
in the main agreement.

| Question | Answer | Owner |
| --- | --- | --- |
| Client data, prompts or conversations used to train or improve any model? | | |
| Ownership of prompts, instructions, tool schemas, evaluation sets, gold cases, tuned artefacts; supplier's prior templates carved out? | | |
| Model or version change by the provider: who migrates, re-baselines and pays? | | |
| Acceptance re-run after a model or prompt change? | | |
| Liability for model output and for actions after human approval | | |
| AI Act role (provider or deployer), Article 50 disclosure owner | | |
| High-risk use (Annex III)? If yes, the high-risk clauses apply | | |
| Explanation of an individual output to an affected person | | |
| Subprocessors and data location (model provider, region, logs) | | |
| Return and deletion at the end: data sets, evaluation records, logs, project | | |

Reference: EU model contractual clauses for AI procurement (MCC-AI, high-risk
and light versions), Public Buyers Community, published 5 March 2025.

## 10. Acceptance of this statement of work

| Party | Name and role | Date |
| --- | --- | --- |
| Client | | |
| Supplier | | |
