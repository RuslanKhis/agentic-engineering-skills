# Stage outlines

One outline per stage and audience. Each line is an action-title placeholder
with the `Covers:` tag it satisfies and the evidence it needs. Angle brackets
are values that come from the project record; when the record lacks one, the
slide says "not yet measured" or the agent asks. Business decks keep a
five-minute path (slides 1 to 3 and the decision) and ask for a decision
between options. Technical decks link the design, contracts, evaluation
report and runbooks by path. The required `Covers:` tags per stage are in
[the deck format](../assets/deck-format.md); the checker enforces them.

## Proof-of-concept approval

**Business, about 10 slides, 10 to 15 minutes**

1. Executive summary: "<Step> loses <baseline measure> today; a <timebox> proof of concept tests whether <use case> changes it by <hypothesis>" (`summary`; SCQA in four lines, from the discovery brief)
2. "Today <step> loses <baseline measure> per <unit>" (`problem`; funnel or process data with source and date)
3. "The complication is <what changed or hurts>" (`problem`; the brief's friction)
4. "We will test one hypothesis: <hypothesis chain>" (`hypothesis`; labelled as such)
5. "Success means <criteria and thresholds>, measured by <method> on <sample>" (`success-criteria`; the design's outcome contract and measurement plan, or the brief's threshold sentences when drafted before the design)
6. "We stop early if <kill criteria>, reviewed on <date>" (`success-criteria`; plan milestones)
7. "Scope: <first use case>; not <exclusions>; a person before every <effect>" (`scope`; design profile and floor)
8. "The proof of concept costs <human hours> and about <model and cloud> over <timebox>" (`cost`; the plan's hours and spend ceiling, estimates labelled; "pending design" from the brief alone. Per-conversation cost is measured in the pilot, not promised here)
9. "Three risks, each with a control and an owner" (`risks`; design contracts and deferred-control table)
10. "Decision: do nothing, run the proof of concept, run a wider pilot; we recommend <option>; <decider> by <date>" (`ask`; what you will see at the end: a measured report, not only a demo)

**Technical, about 12 slides, 20 to 30 minutes**

1. Executive summary: "<Agent> is <architecture> on <runtime>; the proof of concept tests <hypothesis> in <timebox>" (`summary`)
2. "Today <step> loses <baseline measure>; the proof of concept measures <metric> against it" (`problem`, `success-criteria`; the brief's baseline and the design's outcome contract)
3. "The user and task boundary is <scope>" (`scope`; in and out of scope, profile)
4. "Architecture: <components and trust boundaries>" (`architecture`; design diagram)
5. "Contracts the proof of concept must keep" (`contracts`; C IDs with enforcement points)
6. "Data and access: <sources> through <identity>" (`dependencies`; data owners, permissions requested, waits)
7. "Evaluation plan: <n> cases, trajectory and response checks, thresholds" (`evidence-plan`; acceptance cases by goal)
8. "Security and sensitive-data boundaries" (`risks`; exposure table, floor controls)
9. "What the proof of concept costs: <hours>, <spend ceiling>, and the goal that measures cost per conversation" (`cost`; the plan's hours and the design's ceiling or symbolic estimate, labelled)
10. "What we ask of your team: <hours, reviews, environments>" (`dependencies`)
11. "What you get back if it stops: code, evaluation set, findings" (`hypothesis`; plan's phase 1 deliverables)
12. "Decision: we need <access, environment, reviewer> by <date>; owner <name>" (`ask`; the front matter's decider is the person who grants these)

## Production approval (proof-of-concept review)

The business summary counts the agreed success criteria met; the technical
summary counts acceptance cases passed. Each deck states both numbers once
so the two audiences cannot be quoted against each other.

**Business, about 11 slides, 15 minutes**

1. Executive summary: "The proof of concept met <n of m> criteria; we recommend <option> at <cost>" (`summary`)
2. "Criteria agreed on <date> and what we measured" (`criteria-results`; table: criterion, threshold, measured, method, sample; G/A citations)
3. "<Metric> moved from <baseline> to <measured> on <sample>" (`criteria-results`; chart by comparison type)
4. "What did not work" (`learned`; failed criteria, failure modes with counts, not-run cases named)
5. "What we learned that changes the plan" (`learned`; recorded findings and revised contracts)
6. "Production scope: <scope> for <users>, with <workflow change>" (`production-scope`; phase 2 goals, adoption plan, sponsor)
7. "Production cost: <per conversation>, <per month>, <build hours>" (`cost`; actuals from the pilot, estimates labelled)
8. "Risks seen and the controls that contain them, with owners" (`risks`; incidents, mitigations, deferred controls brought forward)
9. "Where a person validates the output, and who is accountable" (`risks`; approval points, governance)
10. "Timeline and checkpoints" (`production-scope`; phases, go and no-go dates, waits)
11. "Decision: stop, extend, build; we recommend <option>; <decider> by <date>" (`ask`)

**Technical, about 13 slides, 30 minutes**

For a proof-of-concept profile most of the operations, release, latency and
security-test slides will say "not yet built; G<n>", because the design
deferred those controls on purpose. Keep the slides: they are the work this
room inherits, and a slide that names it beats one that implies it exists.

1. Executive summary: "The proof of concept passed <n of m> gates; production needs <changes>" (`summary`)
2. "What was built against the design: deviations" (`architecture`)
3. "Evaluation results: <pass rate> on <n> cases, trajectory and response, <repeats>" (`evidence`; report path, variance)
4. "Failure analysis: <top failure modes>, counts, root causes" (`learned`)
5. "The demo is build <x>; the numbers cover build <y>" (`evidence`; with no demo, one line on the evaluation slide instead)
6. "Measured latency, tokens and cost per conversation" (`cost`; traces, sample; a proof-of-concept profile that deferred observability says "not measured; G<n>")
7. "Production architecture changes: hosting, memory, identity, guardrails" (`architecture`; phase 2 decisions)
8. "Contracts your services will depend on" (`contracts`; tool, API, schema, versioning)
9. "Security, sensitive data and approval points, with the tests that prove them" (`risks`)
10. "Observability, alerts and who is paged" (`operations`; SLIs, dashboards)
11. "Release and rollback: gates, pinned models, joint rollback" (`operations`)
12. "What your team inherits and the work it needs" (`production-scope`; hours, skills, documents)
13. "Decision: we need <owners, environments, reviews> by <date>" (`ask`)

## Final results

**Business, about 10 slides, 10 to 15 minutes**

1. Executive summary: "<Agent> is live for <users>; <metric> is <measured> against <baseline>; next is <proposal>" (`summary`)
2. "Outcome against baseline over <period>" (`outcome`; time series, method, sample)
3. "Adoption: <users, share of cases>, with the definition of active" (`adoption`)
4. "Cost: <per conversation>, <per month>, against the estimate" (`cost`; billing actuals)
5. "Incidents and how they were handled" (`incidents`; count, severity, response)
6. "What changed in the workflow" (`outcome`; process change delivered)
7. "What we would do differently" (`next`; recorded lessons)
8. "The team and partners" (`team`)
9. "What is next and what it needs" (`next`; options)
10. "Decision: <ask>; owner <name>" (`ask`), or no ask slide when the review is information only and the front matter says so

**Technical, about 12 slides, 20 to 30 minutes**

Link the production-approval technical deck for the architecture, contracts
and security that did not change; spend these slides on deviations, SLIs,
incidents, cost actuals and the handover.

1. Executive summary: "Production over <period>: <SLO attainment>, <cost>, <incidents>" (`summary`)
2. "Architecture as shipped: <deviations from the plan>, the rest unchanged (see the production-approval deck)" (`architecture`)
3. "Evaluation and release gates in force, with the last results" (`evidence`)
4. "Production quality: <SLIs> over <period>" (`outcome`; monitoring data)
5. "Incidents, root causes, fixes" (`incidents`; postmortem links)
6. "Cost breakdown: model, hosting, people" (`cost`; actuals)
7. "Security and data boundary status: verified controls, open items" (`evidence`)
8. "Operations handover: runbooks, alerts, on-call ownership" (`handover`)
9. "Known limitations and technical debt" (`handover`)
10. "Evaluation-set refresh and model migration dates" (`operations`)
11. "Adoption and the workflow as it runs now" (`adoption`)
12. "Next work and the decisions it needs" (`next`, `ask`)

## Value report (monthly, after launch)

Not a deck: one page per month for the sponsor, in the
[value-report template](../assets/value-report-template.md), checked by
`scripts/check_value_report.py`; see [value report](value-report.md). Its
`M` and `I` records are the series the final-results outcome, cost and
incident slides draw, so cite the same records there.

## Case study (public)

Read the [case-study reference](case-study.md) and use its template. The
`case-study` stage requires `challenge`, `solution`, `results` and `next`;
the checker also fails wording Google's co-branding guidelines do not allow.
A case-study deck exists only when results are measured and approved for
publication; before that, the honest artefact is the final-results deck.

## The written alternative

When the organisation reads memos rather than watches decks, the approval
case can be a one-page future press release from the user's point of view
plus a short FAQ, read in silence at the start of the meeting. Keep the same
evidence lines in the margin and run the same premortem.
