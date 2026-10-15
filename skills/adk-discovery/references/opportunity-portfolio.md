# Opportunity portfolio: from friction to a ranked, measurable first use case

Read when the journey or the process map is on the table and the question is
what to do first. The portfolio is where every candidate gets the same five
judgements, so the first use case is chosen for reasons the stakeholder can
read, not for the loudest idea in the room.

## Find the friction, not the feature

Work from signals the business already has before anyone names a technology:

| Signal | Where it lives | What it shows |
| --- | --- | --- |
| Funnel counts by step | Analytics, CRM, booking or order systems | Where people abandon; the largest drop with the most people behind it |
| Time per step and queue time | Ticketing, workflow tools, process mining, a day of shadowing | Where people wait, re-key, or wait for someone else |
| Rework and hand-offs | Returns, corrections, escalations, "ask a colleague" moments | Where judgement is applied twice or by the wrong person |
| Ticket and call drivers | Support categories, call reasons, chat transcripts | What the user could not do alone, and how often |
| Exceptions | Manual overrides, spreadsheets beside the system | Where the rules stopped fitting |

Record each signal as measured (value, source, date) or reported (who said it).
A reported pain with no count behind it is a candidate for measurement, not yet
for a build.

## Score each candidate the same way

| Column | 1 | 5 | Ask |
| --- | --- | --- | --- |
| Value | Touches a small share of a minor KPI | Moves a KPI leadership watches, for many users or much money | Which KPI, by how much if the hypothesis holds, for how many |
| Feasibility | Needs systems that do not exist, or a technology that does not fit | The facts live in systems we can reach; the fit is clear; a small team could show it in weeks | Who owns the systems; has anyone done this before here |
| Data readiness | No records of the inputs or outcomes; access unknown | Inputs and historical outcomes are recorded, accessible and clean enough | Where the data is, who grants access, what is missing |
| Risk | Reversible, internal, a person reviews before any effect | Money, messages to real people, regulated decisions, or irreversible effects without review | What a wrong answer costs, who notices, how it is undone |

Scores are the conversation's judgements and say whose. `Fit` comes from
[technology fit](technology-fit.md). `Measure` is the outcome metric the
candidate would be judged on; `Baseline` is its current value with source and
date, or unknown. Run the helper so the ordering is computed, not recalled:

```bash
python3 "$SKILL_DIR/scripts/rank_opportunities.py" --brief docs/discovery/<topic>.md
```

It adds `value + feasibility + data - risk` (weights adjustable with
`--weights`), breaks ties on lower risk, and reports what blocks the handoff:
a first candidate with no measure or an unclear fit. Warnings name an unknown
baseline (the first goal becomes measuring), high risk for a first use case,
low data readiness (a data-access discovery goal comes first), a tie the brief
must explain, and a pick that is not rank 1 (say why in the brief). Quote its
figures; when the user's judgement overrides the order, record the reason
beside the table.

## Why the first use case is narrow

Most pilots that stall do so for reasons visible at selection time: no
business outcome agreed in advance, cost nobody converted to a month, risk
controls missing, and no change to the workflow the tool was meant to enter.
The first use case is chosen to make those four things easy: one workflow,
one measure with a baseline, a low risk score or a person before every
effect, and data the team can reach this month. A bigger idea with a higher
value score waits as O-next in the portfolio with the trigger that brings it
forward (the first measure moved, access granted, a budget approved).

## Define the measure before the build

- **Outcome measure:** the number the use case is judged on, observable in
  an existing system (completion rate, time to first usable result, cost per
  case, error rate). Chat volume, messages and "engagement" are not
  outcomes.
- **Baseline:** the current value, its source and date, over a stated
  window. Unknown is an honest answer; it makes measurement the first goal.
- **Counter-metric:** what must not get worse while the outcome improves
  (refunds, complaints, support load, cycle time elsewhere, cost per unit).
  A larger basket with more cancellations is a worse outcome.
- **Leading indicator:** an earlier signal that the chain is moving (fewer
  abandonments at the step) when the lagging outcome (revenue) takes months.
- **Window and sample:** how long, how many, and who reads the number.

Write the chain as arrows and treat every arrow as a hypothesis:

```text
less effort to <step>
  → more <intermediate outcome>
  → <business outcome>, with <counter-metric> flat
```

More usage of the tool does not establish that any arrow held; only the
measure does.

Write "improve efficiency" as "reduce invoice processing from 72 hours to
12 hours": the characterise rewrite, with units and a frequency, is the most
useful editing rule for the brief. Then the threshold sentence for the
outcome and for the counter-metric: "If <metric> for <workflow> <drops below
/ rises above> <threshold>, we will <specific action>."

## Say what 90 days looks like

One sentence a stakeholder would sign: who is using it, on what, and which
number moved against which baseline. The designer turns it into the
outcome contract; the presenter puts it on the success-criteria slide; the
review compares the result with it.
