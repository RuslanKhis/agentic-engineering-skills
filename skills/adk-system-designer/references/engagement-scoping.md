# Engagement scoping: proposal, statement of work and change requests

Read when the system is built for a client under a contract (an agency, a
consultancy, an internal team charging another department) and the user asks
for a proposal, a statement of work (SOW), a change request or the letter
asking the client for data and access. The SOW is written from the
artefacts the design already holds, never from memory: if a figure is not
in the brief, the design or the plan's schedule block, it does not go in the
SOW until it is. This reference is not legal advice; the AI terms checklist
lists questions for the client's and the agency's counsel, not clauses.

## Inputs and where each SOW section comes from

| SOW section | Source | Rule |
| --- | --- | --- |
| Objectives | Discovery brief §4: outcome measure, baseline, target, counter-metric | Quote the measure and the baseline with its source; no brief, then the objective says "baseline to be measured in G01" |
| Deliverables (`DL1` …) | Plan goals and phases | Every deliverable lists the goal IDs it delivers; every goal in a priced phase belongs to one deliverable (reviews and teardown go under a "reviews and close-out" deliverable) |
| Acceptance criteria (`AC1` …) | Goals' acceptance items, the design's contracts and evaluation plan | Measurable threshold, case count, who agreed the cases, method, measured by, date, contracts proved (below) |
| Out of scope | Plan's Later list, deferred controls with triggers | One line each with its trigger, so a later request is visibly a change |
| Client dependencies (`CD1` …) | Plan's calendar waits, prerequisites and execution-scope lines | Owner (a client role), needed-by date, what it blocks, and the plan entry it came from |
| Effort and fees | `scripts/check_schedule.py` totals per phase × the rate the user supplied | Never invent or assume a rate; without one, fee cells read `rate to be supplied` |
| Run cost | The plan's cost ledger and each goal's **Resources created** rows | An estimate with pricing date, per month and per unit; who pays the cloud and model bills |
| Assumptions | The design's Assumed answers table and labelled assumptions | Each names the decision or estimate that changes if it is wrong |
| Change triggers | Assumptions, dependencies, the cut line | Each trigger names what it changes: contracts, goals, estimates |
| AI terms checklist | Below, with the EU model clauses | Every row answered, or marked open with an owner |

Write the SOW to `docs/engagement/<topic>/sow.md` (or the project's own
convention) from the [SOW template](../assets/statement-of-work-template.md).
A proposal is the same document before signature with a validity date and
the pricing options; do not keep two documents.

When the inputs disagree or lack something the SOW needs (a forbidden-effect
count, a statement of work goal, the go-live goals, a model that retires
inside the engagement), do not paper over it: put it in the template's
**Open decisions before sending** section (agency only, removed from the
client copy) with the change the plan needs, and mark any figure you
propose in its place (`†`) until the plan holds it. A plan that lacks the
statement of work, rollout or operations handover goals gets them added
(with the user) before those goals are priced. When the user cannot be
asked, assume one rate for every phase, time and materials capped at each
phase's high end, no contingency and prices excluding VAT, each as a
labelled assumption.

## Acceptance criteria that work for probabilistic output

An agent's output varies between runs and model versions, so an acceptance
criterion is a measured rate on an agreed set, never a promise about every
answer. Each criterion has all of:

- **Threshold:** a comparator and a number: `≥ 85% pass`, `≤ 2 of 40`,
  `p95 ≤ 8 s`. Words such as "correctly", "accurately", "high quality" or
  "fit for purpose" with no number are not criteria.
- **Cases:** how many, drawn how, and agreed by whom: "40 gold cases agreed
  with the client's claims leads by 6 November 2026". Size the set with the
  threshold: on 40 cases one failure moves the rate 2.5 points, so a
  threshold of 97% on 40 cases allows one failure; say which.
- **Method:** the evaluator and rubric (`adk eval` with the grounded-answer
  rubric, a deterministic check, a human review by two SMEs with a tie-break
  rule), the build it runs on, the repeats when the judge is a model.
- **Measured by and date:** who runs it, who witnesses it, by when.
- **Contracts:** the design contract IDs it proves (`C2`), so a change to the
  contract is visibly a change to acceptance.

A criterion with no contract behind it (the outcome measure, the
counter-metric, a presentation) writes `none (<why>)` in the Contracts
cell. A presentation deliverable's criterion counts decks: "0 of 2 decks
with an uncited claim; deck check exit 0 on 2 of 2".

Pair every quality criterion with a forbidden-effect criterion when the agent
can act ("0 of 25 adversarial cases send an email without approval") and,
where the brief has one, the counter-metric ("escalation rate no more than
2 points above the 4-week baseline"). Acceptance on the client's live
traffic needs a window and a sample size too. Size the sample from the
smallest difference the client would act on, not from what the window
happens to hold: `adk-discovery` sizes a before-and-during comparison, and
`adk-agent-evaluation` sizes a paired one (both versions on the same cases)
and reports its minimum detectable difference. When the window cannot reach
that sample, say so in the criterion.

Write the acceptance sentence in one line, in this shape:

```text
AC1: ≥ 85% of 40 gold cases agreed with the client's experts pass the
grounded-answer rubric, measured by adk eval (3 repeats, median) on the
release build by 2026-12-04; proves C2.
```

## Client dependencies and the data request

List each thing only the client can provide, with a date, from the plan:
subject-matter-expert hours (labelling gold cases, judging output), data
extracts or read access, IAM grants and a GCP project with billing, an OAuth
client or app verification, security or DPIA review, a named product owner,
and the go/no-go decision dates of the presentation goals. The date is the
latest day the plan can absorb; the plan's wait entry (`W1`) carries the
same date. The schedule check reports working days, not dates: state the
assumed start date (signature, or the first goal) in the SOW and convert
from it, skipping weekends and the client's holidays. Draft the
[data request letter](../assets/data-request-letter.md) with the SOW
whenever a dependency is data or access, and send it the week the SOW is
signed: it lists each data set and access grant, the
purpose, the minimum scope, the format, retention and deletion, and who on
the client side approves it. Real personal data enters only by the client's
choice, scoped to the journey (the floor in
[delivery profiles](delivery-profiles.md#keep-the-floor-at-every-profile)).

## Effort and fees

Run the schedule check on the plan first and copy its phase totals; then
run the SOW check, which reads the same schedule block through
`check_schedule.py`'s parser and fails when the SOW's hours differ:

```bash
python3 "$SKILL_DIR/scripts/check_schedule.py" --plan docs/plans/<topic>.md --phase ""
python3 "$SKILL_DIR/scripts/check_sow.py" --sow docs/engagement/<topic>/sow.md \
  --plan docs/plans/<topic>.md [--design docs/architecture/<topic>.md] \
  [--change docs/engagement/<topic>/cr-01.md]
```

Fees are the hour range × the hourly rate the user gave, shown as a range
(the schedule's low and high ends), with the rate's source and date. A day
rate is converted at the client's stated hours per day, written beside it.
Fixed price is the high end plus any contingency the user chooses, stated
as such; the agency's margin decisions are the user's. Run cost is separate
from fees: the cost ledger's monthly estimate for the environments the SOW
keeps running, the model spend ceiling from the cost contract, and who
holds the billing account after handover.

## Assumptions and change requests

An assumption is a fact the estimate rests on that the agency does not
control ("the claims export arrives as one CSV per month", "two SME hours a
week"). A change trigger is the observable event that breaks it ("CD2 lands
after 13 November", "more than 60 gold cases requested", "a second channel
added"). Each trigger names what it changes.

A change request uses the [change request template](../assets/change-request-template.md)
and cites by ID: the contracts added or revised (with the plan's change
table row), the goals added, removed or re-estimated (with the new schedule
check's figures), the acceptance criteria and dependencies affected, and
the fee and run-cost difference. Update the plan and design first, rerun
both checks, then write the request from the diff; never price a change the
plan does not yet contain.

## AI terms checklist

The EU model contractual clauses for AI procurement (MCC-AI, a high-risk
version and a light version for other systems, published by the
Commission-supported Community of Practice on the Public Buyers Community
on 5 March 2025, file version February 2025) are a schedule to a main
agreement. They are written for public buyers, non-binding and "not an
official position of the European Commission", and private buyers adapt
them clause by clause. They cover data-set rights, documentation, human
oversight, accuracy metrics in an annex, explanation of an individual
output and cross-indemnities. They exclude intellectual property in the
system, acceptance, payment, liability and applicable law, which is why
most of the list below must be settled in the main agreement. Read the
current files on the Public Buyers Community before citing a clause number.

| Question | Why it matters for an agent | Where MCC-AI helps |
| --- | --- | --- |
| May the client's data, prompts or conversations be used to train or improve any model (the agency's, the model provider's)? | Provider terms differ by product and tier; the answer sets which API and settings are allowed | Section C: the buyer's data sets are used only for the agreement and destroyed on request |
| Who owns the prompts, instructions, tool schemas, evaluation sets and gold cases, and any tuned model or adapter? | These are the reusable value; an agency's prior templates need a carve-out | Data sets only; the rest is the main agreement's IP clause |
| What happens when the model provider changes or retires the pinned model? | Retirement dates are fixed by the provider (see `adk-model-and-output-contracts`' lifecycle table); a migration is work with a re-baseline | Not covered: write who pays for migrations and re-acceptance |
| What does acceptance mean for probabilistic output, and when is it re-run? | Criteria above; re-run after a model or prompt change | Accuracy metrics annex (Annex G in the light version) |
| Who is liable for an output the agent produced, and for actions it took after a human approved them? | Separates the agency's build defects from the client's use and approvals | Not covered: the main agreement |
| Where are the client, the people whose data the agent handles and the processing, including the agency's own staff who support it? | Decides which of Australian (with NSW and Commonwealth government rules), US, EU, UK, New Zealand, Singapore and Canadian privacy and AI law applies, and whether agency access from Australia is a restricted transfer (SCCs or an IDTA), a Singapore or Quebec transfer needing a contract or assessment, or a NSW s 19(2) question. For a NSW or Commonwealth agency, also ask the contract vehicle (ICTA or Core&) and its model-change notice period | Not covered: the data processing agreement and `adk-governance-pack`'s jurisdiction screen |
| Who is the provider under the EU AI Act, and who writes the user-facing AI disclosure (Article 50, applying since 2 August 2026)? | The party putting the system into service under its own name carries Article 50(1) duties | Transparency and instructions for use |
| Is the system high-risk under the AI Act (Annex III use, such as recruitment or credit)? | Switches to the high-risk clauses and a much larger plan; Annex III obligations apply from 2 December 2027 | The high-risk version |
| Explanation of an individual decision to an affected person | Needed when output feeds decisions about people | Explanation obligation in the light version |
| Subprocessors and data location: model provider, region, logging | The client's DPO approves them | Not covered: the data processing agreement |
| Return and deletion at the end: data sets, evaluation records, logs, the GCP project | Feeds the handover's access transfer and the teardown goal | Section C handover and destruction |

## Check before sending

`check_sow.py` exits 0 only when every deliverable maps to plan goals that
exist, every goal in a priced phase belongs to a deliverable, each phase's
hours and the total match the schedule block, fees equal hours × rate when
a rate is given, every client dependency has an owner and a date, and every
acceptance criterion has a numeric threshold with a comparator, a case
count, a method and a date and is cited by a deliverable. With `--design`,
contract IDs in acceptance criteria must exist in the design. With
`--change`, the change request must cite the goals, contracts and estimate
change it makes, and its goal IDs must exist in the plan or be marked new.
A passing check proves consistency with the plan, not that the plan's
estimates or the commercial terms are right; say so when sending.
