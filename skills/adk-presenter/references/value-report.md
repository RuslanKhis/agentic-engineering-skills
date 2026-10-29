# Value report: one page a month after launch

Read this for the `value-report` stage: a live pilot or production system
whose sponsor needs, every month, the outcome against the baseline, what it
cost per outcome, what went wrong, and a stop, continue or scale call. It
is one page in the [value-report template](../assets/value-report-template.md),
not a deck, saved as `docs/presentations/<topic>/value-report-<YYYY-MM>.md`.
Its records are what the final-results deck later draws as a time series,
so a month without a report is a gap in that chart.

## Read the inputs by name

- **Discovery brief** (`docs/discovery/<topic>.md`, §4 and §6): *Outcome
  measure* (metric, how, window, by whom), *Baseline* (value, source, date,
  and which part of the rollout scope it covers), *Counter-metric*,
  *Threshold sentences* ("If <metric> for <workflow> drops below
  <threshold>, we will <action>"), *How the measure reaches a KPI line*,
  *Unit economics known so far* (volume, accepted cost ceiling), and the
  *Decider* and *Senior owner*.
- **Design** (`docs/architecture/<topic>.md`): the cost contract (ceiling
  at volume, variable and fixed parts, the stop) and the resource cost
  ledger's while-provisioned rows, which are fixed monthly cost whatever
  the volume.
- **Plan** (`docs/plans/<topic>.md`, and tickets' Evidence sections): the
  measurement records `M<n>` (value, baseline, window, sample, method,
  owner, build) and incident records `I<n>` (date, severity, effect,
  response, fix, status). The token and cost figures come from the observability
  goal (`adk-agent-observability` counts usage once per logical model call)
  or the billing export filtered by the application's labels.

When a figure the sponsor needs has no record, write it into the plan as
the next `M<n>` with its source before drafting, or the line says "not
measured" and names the goal that will measure it. Write records one per
line with semicolon-separated fields and ISO dates, so the check can read
them:

```text
- M3: metric claims triaged within one day; value 74%; baseline 61% (brief §4); window 2026-09-01 to 2026-09-30; sample 3,310 claims; method claims system export; owner ops lead; build v1.4.2
- M8: metric handlers at full rollout; value 160; kind assumption; method assumed from the four-queue headcount
- I1: date 2026-09-14; severity 2; effect 31 replies quoted a withdrawn clause; response paused auto-send; fix C4 test; status closed 2026-09-20
```

Mark a baseline measurement `kind baseline`, anything not measured `kind
assumption`, and every incident `status open` or `status closed <date>`.

## Write the seven sections

1. **Outcome against baseline.** The brief's outcome measure this period
   against its baseline, measured on the same definition and scope. When
   the brief's baseline covers only part of the live scope, say which part
   the comparison holds for. A lift smaller than its 95% margin is within
   the margin; say so. This month against a baseline period is two separate
   samples, so the margin is that of a difference, not of one proportion
   ([storyline](storyline.md) gives the formula).
   Last month's figure may sit beside it for the trend on a line that says
   "last period"; it never stands in for this month's.
2. **Counter-metric.** The brief's counter-metric against its own baseline,
   beside the outcome, every month, even when nothing moved. When it has no
   baseline, report the value anyway with "no baseline" on the same line
   and the goal that measures one; the check warns rather than fails.
3. **Adoption.** State what *active* means, then the share of eligible
   users or cases that are active. Google Cloud's KPI guide defines
   adoption rate as the percentage of active users and reads its shape:
   consistently low suggests lack of awareness, high then falling suggests
   lack of performance. For an agent, add the recorded acceptance,
   take-over or revert rate where the plan has it; Google's production-agent
   KPI piece treats a high human take-over rate as a trust signal.
   Conversations and messages are not adoption and not outcome. When this
   month's adoption was not measured, say so and name the goal; last
   month's figure may follow as "last period".
4. **Cost per outcome.** Actual: the period's cost (model, hosting and the
   ledger's fixed resources, from the billing export or observability token
   cost; say which and what it leaves out) over the period's count of
   successful outcomes, both cited. Count outcomes in the unit of the plan's
   cost contract and the sponsor's ceiling, so actual and estimate compare;
   when the brief's outcome measure uses a stricter unit (claims triaged
   within a day rather than claims triaged), add the second figure on its
   own line, because the call can turn on it. Google's
   production-agent KPI piece names cost per successful task as the metric
   that matters most because it pairs cost with outcomes; per-token or
   per-conversation cost hides failures. Then the plan's estimate on its
   own line opening with *Estimate*, and the reason for the difference
   (volume, retries, a model change, fixed costs spread over low volume).
   When the brief prices each error type (adk-discovery's "Price of each
   error"), add the cost of errors on its own line: every flag handled in
   the period, needed or not, at the brief's handling cost, plus the misses
   at the brief's price of a miss, beside today's process priced the same
   way at this period's volume (its flags and misses at today's rates). Do
   not price only the false flags on one side: both totals count every
   handled flag, or the comparison is not like for like. A cost per outcome
   without it flatters a cheaper model that misses more; in one worked
   example a version twenty times cheaper per case cost more in all than
   the process it replaced (Wimberly, Marker, Siegel and Kwatra,
   "Eval-Driven System Design: From Prototype to Production", OpenAI
   cookbook, with Fractional, 2 June 2025,
   https://developers.openai.com/cookbook/examples/partners/eval_driven_system_design/receipt_inspection,
   read 2026-10-29). Counts recorded for the whole period (a log of every
   miss found) are measured. Counts scaled up from a reviewed sample, or
   from the evaluation's rates times this period's volume, are an
   estimate, so that line opens with *Estimate*. Cite the brief for the
   rates rather than writing "£30 a miss" on a measured line: the check
   reads a money figure followed by "a", "per" or "each" as a cost per
   outcome and asks for its two records.
5. **Incidents.** Every `I` record dated in the period, with severity,
   effect, response, fix and whether it is closed; "no incidents recorded" only when the plan
   holds none.
6. **Thresholds.** Each threshold sentence from the brief, this period's
   value with its record, and whether it fired. A fired threshold's action
   is the default call; overriding it needs the decider's reason in the
   plan.
7. **Call.** Stop, continue or scale, the one decider (the brief's decider,
   or the senior owner when the call commits budget), the date, and the
   figure or threshold the call rests on. A scale trigger agreed in the
   plan (its Later table or the decision memo) takes precedence over the
   table below. Default reading, which the decider may override with a
   recorded reason:

   | Call | When the record shows |
   | --- | --- |
   | Scale | Outcome beyond the margin against baseline for the agreed number of periods; counter-metric held; cost per outcome within the ceiling, with the scaled figure as an estimate on one stated assumption; no open severity-1 or -2 incident |
   | Continue | Outcome moving but within the margin, or one condition for scale not yet met; name what next month must show |
   | Stop | A stop threshold fired; or cost per outcome above what the outcome is worth on the brief's KPI line, with no fix in hand |

Open the page with a one-sentence bottom line: the outcome against baseline
and the call, each figure cited. When the period's decision date has
passed, write the report anyway, date it, put the next decision date in the
front matter and record the late month in the plan's change table.

Keep the voices apart as in the rest of this skill: a line is measured
unless it opens with *Estimate*, *Target* or *Threshold* or says "we
estimate". A projection may rest on one recorded figure and one stated
assumption; two assumptions on one line is stacking, and is cut.

## Check and record

```bash
python3 "$SKILL_DIR/scripts/check_value_report.py" \
  --report docs/presentations/<topic>/value-report-2026-09.md \
  --plan docs/plans/<topic>.md --brief docs/discovery/<topic>.md
```

Add ticket files after `--plan` when records live there. Wrapped bullets
are read as one line. Exit 0 means every
figure cites a record the plan holds, measurement windows fall in the
period, the outcome has a baseline, cost per outcome cites both its parts,
every incident in the period is reported, a scale call has no open
severity 1 or 2 incident, and the call has a decider. Fix
every error; read every warning. A missing baseline is not fixed in the
report: the call becomes "continue, measure the baseline", and the plan
gets the goal that measures it.

After the decider makes the call, record it, the date and the figures it
rested on in the plan's change table, as for any presentation decision.
A scale call that commits budget or a stop call goes to the
[decision memo](../assets/decision-memo-template.md) and, when a meeting is
needed, the `final-results` stage, whose outcome, cost and incident slides
cite the same records.

Sources read 25 October 2026: Google Cloud, [Measuring gen AI success: a
deep dive into the KPIs you need](https://cloud.google.com/transform/gen-ai-kpis-measuring-ai-success-deep-dive)
(Chinoy and Liu, 26 November 2024: adoption rate, frequency of use,
business-value KPIs); Google Cloud, [The KPIs that actually matter for
production AI agents](https://cloud.google.com/transform/the-kpis-that-actually-matter-for-production-ai-agents)
(Fateh and Liu, 27 February 2026: cost per successful task, take-over and
revert signals, reliability before adoption before value). Neither gives a
baseline method, a reporting cadence or a stop rule; the monthly cadence,
the section order and the default call table are this skill's choices.
