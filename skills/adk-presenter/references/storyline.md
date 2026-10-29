# Storyline: answer first, a claim per slide, evidence on the same slide

Read before writing any outline. These rules are the converging practitioner
prescriptions of the consulting and presentation sources (dated and linked
in the repository's research note `docs/research/stakeholder-presentations.md`),
not measured outcomes; the AI-specific surveys add why agent projects stall:
unclear value, escalating cost, inadequate risk controls, no workflow change.

## Find the question before the slides

Write four lines before anything else, from the project record:

- **Situation:** what the business does today and the baseline, with source.
- **Complication:** what hurts or changed (the discovery brief's friction,
  the POC's result, the production incident).
- **Question:** the decision the audience must make, in their words.
- **Answer:** the recommendation in one sentence that someone could disagree
  with, with what is at stake. If nobody could disagree, it is a topic, not
  an answer.

If the record lacks the complication or the baseline, ask the user; do not
invent one. The four lines become the executive summary slide and the first
thirty seconds of speech.

## Build the ghost deck first

List the action titles in order and read them as a paragraph. If the titles
alone do not carry the argument from Situation to Answer to Ask, the deck is
not ready for bodies. Each title is the one sentence the slide proves; the
body is the proof, not a second message. "Results" is a label. "Checkout
completion rose from 31% to 36% on 2,140 advertisers" is a title. Keep one
message per slide; split a slide that needs two.

## Put the evidence on the slide that makes the claim

Every slide carries an `Evidence:` line (see the deck format) naming the
goal and acceptance case, contract, decision, file or URL the claim comes
from, or the label that says it is a hypothesis or an assumption. A number
with no source does not go on a slide. Beside each measured number give the
method and the sample in one clause: "on 312 sessions, 10 to 23 October,
measured by the booking service's receipts". Three voices, kept apart by
word choice and never mixed in a title: *we measured* for results, *we
estimate* for projections, *we hypothesise* for untested claims.

Vanity metrics (conversations, messages, chat usage) go to the appendix at
most. The headline is the outcome agreed at approval time against its
baseline, with the counter-metric beside it.

A demo is not the measured system unless it is the same build on the same
inputs; say which build the demo is and which build the numbers cover, or
that there is no demo. Projected impact is not a result. A benchmark score
is not a business outcome. A small lift on a small sample may be noise.
The 95% margin of one proportion measured on n cases is at most about one
over the square root of n (about six points on 300). A lift is the
difference of two measurements, so its margin is wider: for two separate
samples (this month against a baseline period) it is
1.96 × √(p₁(1 − p₁)/n₁ + p₂(1 − p₂)/n₂), about eight points for 300 and
300 near 50%. Outcomes grouped by customer, site or document widen it
again. When both figures come from the same cases, as in an offline
evaluation of two builds, cite the paired interval adk-agent-evaluation
reports instead (its quality-iteration reference, "Tell a change from
noise"); it is usually narrower (both forms are from Evan Miller, "Adding
Error Bars to Evals", Anthropic, arXiv 2411.00640, section 4, read
2026-10-29). When the lift is inside its margin, the
title says "within the margin". When the margin cannot be computed from
what was recorded, ask the user for the test that was run.

## Choose the chart from the comparison

Decide the message, then the comparison it implies, then the chart: a
component (share of a whole), an item comparison (agent against baseline),
a time series (cost per conversation across the pilot), a distribution, or a
correlation. Bars, columns and lines cover nearly everything; a chart whose
message is not the slide title is cut. Show the sample size on the chart.

## Make the five-minute path survive

Assume the slot is cut to five minutes: the title, the executive summary
and the decision slide must carry the whole argument. Say in the first
sentence that the summary comes first and discussion after. For an
executive audience, the appendix (slides tagged `questions` or `appendix`,
outside the timed count) holds what the questions will need and can be
several times the size of the talk.

## Ask for a decision between real options

Frame every ask as two or three real options with the recommended one
marked: stop, extend the pilot, build for production at scope X. Decisions
made from a single option fail more often in the one observational study
that looked. Name the single person who decides, what they are being asked,
the date, and what happens if nothing is decided. The decision slide appears
at the end and its content at the start.

## Answer the three cancellation causes on purpose

Every deck has a value slide against a baseline, a cost slide (per
conversation and per month, model and cloud and people, actuals separated
from estimates) and a risk slide with a control and an accountable owner per
risk. The production-approval deck also names the workflow change, the
executive sponsor and the points where a person validates the output,
because those are what the largest survey associates with value; present
them as practices, not guarantees.

## Technical audiences: link the record, do not compress it

Slides compress evidence; a technical reader needs the design, the
contracts table, the evaluation report and the runbook. Link them by path
and quote the figures. Uncertainty goes in the title ("two acceptance cases
not yet run"), never in a sub-bullet. A risk is a full sentence with its
consequence. Deviations from the design are listed, not implied.

## Pre-wire, premortem, rehearse

No surprises in the room: list the decision-makers and brief each one before
the meeting, and record what they said. Then run a premortem on the deck:
"this presentation failed to get the decision; why?" Write the reasons for
two minutes, leader first. The reasons become the question bank and the
appendix. Rehearse once with someone who did not build the system, and time
it against the minutes in the front matter.

## Leave something behind

A one-page decision memo (the pre-read and, after the meeting, the record)
with the decision requested, the options, the result against criteria, and
after the meeting the decision, owners and next checkpoint. When the
organisation reads rather than watches, offer the approval case as a
one-page future press release plus a short FAQ instead of a deck, read in
silence at the start of the meeting.
