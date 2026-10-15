# Audiences and the questions they ask

Read while drafting speaker notes and the question bank. Two audiences, two
decks; the same evidence, different claims.

## What each audience must decide, and reads

| | Business decision-makers | Internal technical teams |
| --- | --- | --- |
| Decides | Whether to fund, extend, build, stop; who sponsors | Whether to depend on it, host it, be paged for it; what to change first |
| Reads | The executive summary, the result against criteria, cost, risk, the ask | The design, the contracts table, the evaluation report, the runbook, the diff from the design |
| Time | 10 to 15 minutes, discussion after a five-minute summary | 20 to 30 minutes with the documents linked |
| Numbers | Outcome against baseline, cost per month, hours | Pass rates with repeats, p95 latency, tokens per turn, SLIs, cost per conversation |
| Risk | Consequence, control, accountable owner | Threat, control, the test that proves it, what is still open |
| Credit | Sponsor and team named | Contributors and owners named |

Keep the business deck free of component names unless a decision depends on
one; keep the technical deck free of persuasion. Both state what was not
measured and what was not run.

## Speaker narrative pattern

Open with the Question and the Answer in two sentences, then say how the
time runs: summary first, discussion after. For each slide, speak the action
title, point to the evidence, give its method and sample size in one clause,
and end with the implication for the decision. Keep the three voices apart:
*we measured*, *we estimate*, *we hypothesise*. Close by restating the
options, the recommendation, the decider and the date, and name what the
audience receives afterwards: the one-page memo and the decision record.

Write the notes as speech, in full sentences, with the pause and the handover
to the next slide. A note that reads "talk about costs" is not a note.

## Question bank

Prepare an answer with evidence for each, and put the evidence in the
appendix. A question with no evidence behind it gets the honest answer "not
measured" and the goal that would measure it.

**Business**

- What is the baseline, who measured it, and when?
- What exactly are you asking me to decide today?
- What does it cost per month at full adoption, and what did the pilot cost?
- What happens if the model's price or behaviour changes?
- Who is accountable when it gives a customer a wrong answer?
- What would make you recommend stopping?
- Why this scope and not larger or smaller?
- How many users and cases is this result based on?
- What did not work?
- Who else has signed off, and who is the sponsor?
- How does this change the way people work, and who trains them?

**Technical**

- Which evaluation cases cover the worst failure modes, and how many times
  were they run?
- Is the demo the same build as the measured numbers?
- What are the tool contracts, and who owns changes to them?
- How is identity propagated, and what can the agent write?
- What is the p95 latency and the token cost per turn?
- What stops a runaway loop or a prompt injection?
- How do we roll back the prompt, model and schema together?
- What do we inherit for on-call, and what are the alerts?
- Which model version is pinned, and when is it retired?
- Where are the sensitive-data boundaries, and which tests prove them?
- What deviated from the design, and why?

## Premortem prompts

"This presentation failed to get the decision. Why?" Common answers, each
of which the outline should already have prevented:

- The executive stopped reading at slide two.
- A number on slide three had no method or sample behind it.
- The demo differed from the measured system.
- The cost was per request and nobody could convert it to a month.
- The risk slide had no owner.
- The decision was never asked for, or had one option.
- A known failure was left out and someone in the room knew it.
- The technical team heard persuasion and stopped trusting the numbers.

## Pre-wiring record

| Decision-maker | Briefed on | Their concern | What changed in the deck |
| --- | --- | --- | --- |

Keep it with the premortem answers in `pre-wiring.md` beside the outline;
the decision memo links to it.
