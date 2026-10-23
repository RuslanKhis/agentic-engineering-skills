# The speech: what the speaker says, in what order, for how long

Read while writing `Notes:` and the question bank. The slides prove; the
speech persuades, and it is judged by whether the room reaches the right
decision. The rules below are the measured and converging findings of the
rhetoric and persuasion sources (dated and linked in the repository's
research note `docs/research/speech-craft.md`); where a rule is ours rather
than a finding, it says so.

## Before the notes: one sentence

Write the throughline: one sentence someone in the room could disagree with,
carrying the decision and the one number that justifies it. Every section of
the speech serves it; a sentence that does not is cut. Explain the agent in
the company's own vocabulary (the ticket, the claim, the order), never in
model internals.

## The shape

- **Bottom line first.** The first spoken sentence is the decision requested
  and the number: "I am asking for four weeks and one developer to test
  whether a guided brief lifts checkout completion from 31 percent." Then
  "interrupt me whenever you want to go to the decision." Context comes
  second; the backstory stays short.
- **Alternate today and after.** One paragraph of the costly present (the
  recorded baseline), one of the credible future (the measured or estimated
  result), never more than two in a row of either, ending on the new normal.
- **One real case on the spine.** The user's ordinary day; the day the agent
  was switched on; three consequences, each with a number; what is now
  routine. One case, told once, with its method.
- **Three reasons, spoken as three.** An audience that knows you want
  something trusts three claims and doubts the fourth. Hold further evidence
  for questions.
- **Say what did not work, and answer it.** A failure named and answered
  persuades more than a one-sided case and raises credibility; a failure
  named without a response is the weakest option. This section comes before
  the ask.
- **Uncertainty as a number.** "61 percent, range 55 to 67, on 120 cases"
  costs almost no trust; "roughly works most of the time" costs more. Bad
  news takes the same form: we measured X; it missed the threshold; here is
  the cause and the change.
- **Signpost with claims, not labels.** "Second, the cost per case" rather
  than "next, the cost slide". A preview that is a table of contents, or
  that delays the decision past the first minute, is cut.
- **Options, decider, date, then credit.** Close the body with the two or
  three options, the recommendation, who decides and by when; name the team
  and what each person did.
- **The close comes after the questions.** Restate the decision, the decider
  and the date as the last words of the meeting, not the last answer.

## Skeletons with timings

Minutes for a 15-minute and a 30-minute slot; the longer slot adds questions
and the case, never more claims. Angle brackets come from the record; a
missing value is spoken as "not yet measured".

**Proof-of-concept approval** (15: 10 talk, 5 questions; 30: 18 and 12)

1. Bottom line and the invitation to interrupt (1 / 1.5)
2. What is: one user's day today, the baseline and who measured it (2 / 3)
3. What could be: the same day after, said as "we hypothesise" (1.5 / 2.5)
4. Three reasons to test now: the complication, the data and access in
   hand, the kill criteria (2 / 4)
5. What could go wrong and the answer: two risks, each with a control and
   an owner (1.5 / 3)
6. Criteria, options, ask: thresholds; stop, run, wider pilot; the
   recommendation, decider and date (2 / 4)
7. Questions, then the close

**Production approval** (15: 11 and 4; 30: 20 and 10)

1. Bottom line: criteria met n of m, the recommended option at its cost per
   month, the decision and date (1 / 1.5)
2. What we measured: the criteria table spoken, method and sample in one
   clause each; the recorded demo of the measured build, or the measured
   result alone when there is no demo (3 / 5)
3. One real case before and after, on the spine (2 / 4)
4. What did not work and what changed: failures with counts, the fix or the
   scope cut (2 / 4)
5. Three reasons to build: outcome against baseline, cost against estimate,
   the workflow change and where a person validates (1.5 / 2.5)
6. Options, ask, credit (1.5 / 3)
7. Questions, then the close

**Final results** (15: 10 and 5; 30: 17 and 13)

1. Bottom line: period run, outcome against baseline, cost against
   estimate, incidents (1 / 1.5)
2. The number and its method: the series, the sample, who measured, and the
   counterfactual with its reason: a control queue, a shadow period or the
   baseline trend, named as such (2 / 4)
3. One user's year on the spine, including the day something failed (2 / 3.5)
4. What did not work and what we learned (2 / 3.5)
5. Credit: names, what each did, partners (1 / 1.5)
6. What is next: options and a recommendation, or "no decision today" (2 / 3)
7. Questions, then the close

## Words and pace

Prepared speech runs at about 150 words a minute, so a 15-minute slot holds
about 1,500 words of notes with room for questions; the deck check estimates
the spoken minutes from the notes. Cut rather than speed up. Fillers are
reduced by pausing, not by effort; "uh" does listeners no harm. Spread eye
contact across the room; holding a sceptic's gaze while arguing against their
view persuades less. Never say that most communication is non-verbal; the
7-38-55 figure applies only to talk about feelings.

Words that do not appear unless a recorded measurement backs them:
revolutionary, understands, intelligent, eliminates, always, guarantees.
Risk controls are spoken as confidence: what the agent cannot do, who
approves what, and the test that proves it.

## Demo discipline

The demo is a recording of the build that produced the numbers, labelled
with build and date, narrated live; when there is none, say so and show the
measured result instead. A live run belongs only in a technical
session, with the recording open as the fallback. Nobody wants to watch
anyone type. Record from the replay mode of the measured build
(`adk-frontend-integration`'s demo readiness) and say aloud that it is a
replay, and of which date.

## Rehearsal checklist

- Throughline written; first sentence is the ask and the number.
- Three reasons spoken as first, second, third; extra evidence parked.
- Every number with method and sample in the same breath; ranges, not
  adverbs; the three voices kept apart.
- One "did not work" section with the response, before the ask.
- Demo recorded, labelled, with a fallback copy.
- Notes within the minutes at 150 words a minute.
- Two full runs out loud, one before a colleague who plays the decider and
  interrupts; each section timed against the skeleton.
- The decider and one sceptic pre-wired; the question bank updated from
  what they asked.
- Say "I am excited" before walking in, not "calm down".
- Hype words removed; leave-behind and decision memo ready.

## Questions: the protocol

1. Let the question finish; pause two beats.
2. Restate it in one neutral sentence so the room hears it.
3. Answer in one sentence; then the evidence with method and sample; then
   restate the answer.
4. Bridge: "which is why the recommendation is <option>."
5. Unknown: "I don't know. I will find out and send it to <name> by
   <date>." Never guess.
6. Hostile: acknowledge, ask what they would need to see, answer the fact,
   look at the whole room, offer to continue afterwards.
7. Off-topic or unanswerable here: park it with an owner and a date.
8. End with the close, not the last answer; the memo goes out within a day
   with decisions, parked questions with owners and dates, and the next
   checkpoint.
