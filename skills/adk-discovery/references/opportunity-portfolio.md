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
- **Price of each error:** for a use case that decides or flags (approve
  or refuse, audit or pass, act or escalate), name its two errors: a case
  that needed the action and did not get it (a miss), and a case flagged
  that did not need it (a false flag). Record what a miss costs in money
  and what handling a flag costs, with who said so (a missed audit's average
  loss; a review's handling minutes at a stated hourly rate). Every flag
  costs its handling, needed or not; a false flag is the part that buys
  nothing. Record too the share of cases that need the action, and today's
  rate of each error and cost per case under the current process. With the
  volume, these let
  adk-agent-evaluation turn measured rates into a cost for the period and
  compare the candidate with today's process at the same volume, instead
  of with a round accuracy target. For example: 1 million receipts a year,
  5% needing an audit, $2 an audit, $30 for each missed one; today's
  process misses 3%, needlessly flags 2% and costs $0.20 a receipt, about
  $380,000 a year in all (Wimberly, Marker, Siegel and Kwatra,
  "Eval-Driven System Design: From Prototype to Production", OpenAI
  cookbook, with Fractional, 2 June 2025,
  https://developers.openai.com/cookbook/examples/partners/eval_driven_system_design/receipt_inspection,
  read 2026-10-29; the figures are the authors' assumptions). An error
  that changes no decision has no price. A price nobody can give is
  "unknown: ask <role>", and the first goal estimates it.
- **Leading indicator:** an earlier signal that the chain is moving (fewer
  abandonments at the step) when the lagging outcome (revenue) takes months.
- **Window and sample:** how long, how many, and who reads the number.
  Size "how many" from the smallest lift the sponsor would act on (δ), not
  from what a month happens to hold. For a rate measured before and during
  the pilot, each period needs about 7.85 × (p₁(1 − p₁) + p₂(1 − p₂)) / δ²
  cases at 5% significance and 80% power, where p₁ is the baseline and
  p₂ = p₁ + δ. From a 60% baseline, a 5-point lift needs about 1,470 cases
  per period and a 10-point lift about 350 (the power formula in Evan
  Miller, "Adding Error Bars to Evals", Anthropic, arXiv 2411.00640,
  section 5, read 2026-10-29, applied to two separate samples). When the
  pilot's volume cannot reach that in the window, lengthen the window, agree
  a larger lift, or label the measure indicative in the brief. Running the
  same cases through both the current process and the agent (a shadow run)
  needs fewer, because each case is compared with itself; adk-agent-evaluation
  sizes that design.

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
