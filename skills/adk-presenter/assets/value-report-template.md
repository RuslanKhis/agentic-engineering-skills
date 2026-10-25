---
stage: value-report
period: <YYYY-MM, or YYYY-MM-DD to YYYY-MM-DD>
title: <agent> value report, <month year>
sources: docs/discovery/<topic>.md, docs/plans/<topic>.md
decider: <the one person who makes the call; the brief's decider or senior owner>
date: <when the call is made>
call: <stop | continue | scale>
---

# <Agent>: <month year>

One page for the sponsor. Every figure cites a measurement (`M<n>`) or
incident (`I<n>`) record in the plan; a line that opens with *Estimate*,
*Target* or *Threshold* may cite the plan's cost contract or the brief
instead. A figure the plan does not hold is written there first, or the
line says "not measured" and names the goal that will measure it. A line
that cites last month's record for the trend says "last period".

**Bottom line:** <one sentence: the outcome against baseline and the call,
each figure cited>.

## Outcome against baseline

- <Outcome measure from the brief §4>: <value> against a baseline of
  <baseline> (<M n>; window <dates>, sample <n>, method <how>).
- <One clause on whether the change is beyond chance on this sample, or
  "within the margin".> <Optional: last period <value> (<M n>).>

## Counter-metric

- <Counter-metric from the brief>: <value> against <baseline> (<M n>),
  or "<value> (<M n>); no baseline yet, <goal> measures one".

## Adoption

- Active means <definition, for example one completed task in the month>.
- <Active users or share of eligible cases> (<M n>); <acceptance,
  intervention or revert rate where recorded> (<M n>).

## Cost per outcome

- Actual: <money> per <outcome unit>: <cost> (<M n>: billing export
  filtered by labels, or the observability token cost; say which) over
  <outcome count> (<M n>), in the unit of the plan's cost contract and the
  sponsor's ceiling.
- Estimate: <money> per <outcome unit> (<plan cost contract C n>); the
  difference is <reason>.

## Incidents

- <I n>: <date>, severity <s>, <effect>; <response>; <fix>; <open / closed on date>.
- <or: "No incidents recorded in the period" when the plan holds none.>

## Thresholds

| Threshold sentence (brief §4) | This period | Fired |
| --- | --- | --- |
| If <metric> <drops below / rises above> <threshold>, we will <action> | <value> (<M n>) | <yes / no> |

## Call: <stop / continue / scale>

<Decider> decides by <date>. <One sentence: the call recommended and the
threshold or figure it rests on.> Options: stop (<what it frees>),
continue (<what is watched next month>), scale (<scope, the cost per
outcome at that scope as an estimate, and what it needs>).
