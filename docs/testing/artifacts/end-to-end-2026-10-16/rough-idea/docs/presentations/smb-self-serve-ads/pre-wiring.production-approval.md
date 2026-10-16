# Pre-wiring and premortem: production decision, 6 November 2026

The proof-of-concept approval record is `pre-wiring.poc-approval.md`.

## Pre-wiring record

Briefings not yet held; rows read "pending" until someone has been briefed.

| Decision-maker | Briefed on | Their concern | What changed in the deck |
| --- | --- | --- | --- |
| Director of SMB Sales (decider, sponsor) | pending | expected: cost per month at full adoption, and whether 312 sessions is enough (business slides 4 and 8) | pending |
| Platform team lead (hosting sign-off) | pending | expected: on-call ownership, retention of the sentence, the unrun switch-off (technical slides 9, 10) | pending |
| Platform product owner (judges the measure) | pending | expected: the control arm's 63.1% against the 62% baseline; the 1.3% unmatched starts | pending |
| One sceptic from sales | pending | expected: escalations were not measured in the window (business slide 5) | pending |

## Premortem: "this presentation failed to get the decision; why?"

| Reason | Where the deck answers it |
| --- | --- |
| Someone said 312 sessions is too few and the lift is noise | Business slide 4: control arm 63.1% in the same weeks; margin about 5.7 points estimated; lift 7.7 above it; no significance test, said on the slide |
| The cost was per session and nobody converted it to a month | Business slide 8: $0.46 a session and about $330 a month, both estimates, with the arithmetic on the slide and the build-spend caveat |
| A known failure was left out | Business slide 5 and technical slide 5: G06/A3 not run, 58 hours over the estimate, escalations not measured, seven misses with root causes |
| The platform team heard persuasion | Technical deck quotes acceptance IDs per contract and names what does not exist (traces, alerts, runbook) in titles |
| The decision had one option | Both ask slides give three options with the recommendation, the decider and the date |
| The demo differed from the measured system | There is no demo; the appendix says which build the numbers cover |
| The retention question stopped the sign-off | Technical slide 9 names it as the open item and the ask makes it a condition rather than a blocker |

## Rehearsal

Two runs out loud per deck, one before a colleague playing the Director of SMB Sales (business) or the platform team lead (technical) who interrupts at slide 3. Time each section against the production-approval skeleton (1 / 3 / 2 / 2 / 1.5 / 1.5 minutes for the 15-minute slot; 1.5 / 5 / 4 / 4 / 2.5 / 3 for 30). The business notes script about 6.9 minutes of the 11 of talk; the technical notes about 7.2 of 20; the rest is the criteria table spoken, the one case (the bakery owner, labelled constructed), and the questions.
