I've written the design and a phased plan, both still drafts because every product choice rests on answers I had to assume. The biggest one: in the pilot, ad-ops place the orders in the booking system, not the assistant. Advertisers confirm a priced proposal, and ad-ops place it within one business day. I chose this because nobody knows whether the booking system accepts a repeated order safely, so an automated order could be created twice after a lost response.

**Profile:** MVP or pilot: five external advertisers placing real orders.

**What phase 1 delivers (G01–G09):**
- Sign-in with your identity provider, limited to the five advertisers.
- Asset search that only returns assets each advertiser's brands are licensed for on that channel; rights are checked again at confirmation and when ad-ops place the order.
- Prices read from the booking system and stored with an expiry.
- A confirm button the model cannot press. Each confirmation creates exactly one request in a queue for ad-ops.
- A 12-case evaluation set, deployment to Cloud Run with spend limits, and a rehearsal with ad-ops.

**Does it fit:** I ran the planning skill's schedule script. It needs 42–67 hours against 67.5 available, assuming one full-time engineer at 6 focused hours a day and 25% held back for surprises. The finish lands at 10.4–14.9 working days out of 15, so it fits with less than a day to spare at the high end. The first run failed: the hours fitted, but the engineer sat idle waiting for system access. I moved one access dependency to where it is really needed, and the change is recorded in the plan.

**What waits for phase 2 (G10–G13):** automated orders (only possible if the booking team confirms it can safely handle a repeated order), order status from the booking system, streaming replies, and running the evaluation in CI.

**Not done:**
- No application code or tests exist yet, as requested.
- Cloud regions, limits and prices weren't checked because network access wasn't allowed. They're marked provisional and checked in G08.
- I skipped the independent plan review: the skill requires it only for multi-person or production plans. I recommend running it before G06, the goal that builds the confirm-and-order path, because real money is involved.

**Decisions only you can make** (16 assumed answers are listed at the top of the design):
- Whether ad-ops should place pilot orders, as above.
- Whether your engineer is full time and new to ADK; this sets the capacity.
- That pilot orders are real.
- That the identity token carries an advertiser organisation you can map to brands.
- Who the ad-ops contact is, plus contacts on the booking and rights teams.
- Rights territory and flight dates, which the rights system doesn't key on; the booking team's answers on repeated orders come back in G02.

In `REPORT.md`, the friction log points to where the skills were unclear. The two main ones were whether a one-person pilot needs the review, and the acceptance-item formatting the schedule script requires.

Next prompt:

```text
/adk-engineer Carry out G01 from docs/plans/advertiser-campaign-assistant.md.
```

Files are in `docs/`:
- `architecture/advertiser-campaign-assistant.md`
- `plans/advertiser-campaign-assistant.md`
- `../REPORT.md`

---- next turn ----

I've revised the design and plan for the new rights fields, but phase 1 no longer fits the three weeks. Even after two cuts it needs 44–68 hours against 67.5 available, and the planning skill's schedule check puts the finish at 10.7–17.6 working days against 15. So it fits only if the work runs at the low end.

**What changed in the design**
- **C1** (the rights promise) now says an asset is shown, quoted or proposed only when a single rights grant covers all of these:
  - the brand, channel and territory;
  - every day of the flight;
  - modification, if the advertiser intends to change the creative.

  Any missing or unknown field counts as not granted, so a wrong assumption makes the assistant offer too little rather than too much.
- **D13 (new):** one shared function decides rights coverage. Search, the advertiser's confirmation and ad-ops' claim all call it, so the three checks can't drift apart.
- The search tool now requires territory and dates, so the assistant has to ask for them. Quotes are priced per territory. The confirmation covers territory, flight and modification intent, so changing any of them needs a new confirmation.
- **C9 (new):** each order request carries the grant and its conditions, and ad-ops see them before placing the order. What happens to the creative after placement can't be enforced here; I've recorded that as a gap.
- New tests:
  - every rights field denied on its own;
  - two grants that only cover the flight together are refused;
  - a grant that expires or narrows, or a flight that starts, between confirmation and ad-ops' claim.

**Cuts I made to protect the date** (please confirm or reverse them):
- One territory per proposal (D14). A multi-country campaign needs one confirmation per country.
- Traces move to a new phase 2 goal, G14. The pilot gets one structured log line per request instead.

**Your decision: the date.** These are the options the schedule check showed to fit:

| Option | Finish (working days) |
| --- | --- |
| Current scope, 18 days | 10.7–17.6 of 18 |
| Evaluation set (G07) moved to phase 2, 17 days | 10.0–16.4 of 17 |
| No cuts, 19 days | 11.1–18.7 of 19 |

Moving G07 alone, keeping 15 days, doesn't fit (16.4 days). Overtime at 7.5 hours a day would fit, but I don't recommend three weeks of it. The check's high end is pessimistic: it has the engineer sit idle waiting for booking-system access instead of building the sign-in page meanwhile. I quoted its figure anyway, as the skill requires, and noted this in the plan.

**Other open questions** (assumed, in the design as Q17–Q22):
- the territory names the rights system uses;
- whether grant dates include both ends;
- whether grants can be combined to cover one campaign;
- whether the delivery team's format adaptation counts as modifying the creative (a question for that team).

**Checks:** schedule check rerun: no problems, all 9 contracts covered by goals, every failure-table cell cites a real test. A diff against the previous version caught two errors, both fixed: a test assertion I had dropped by accident, and a revision 1 failure-table cell that pointed at the wrong test. Every removed or weakened item is in the plan's change table. No application tests or cloud checks ran; there is no code yet. The independent plan review is still not run.

REPORT.md has a new "Revision 2" section covering the questions, checks, what-ifs and friction log. The next step hasn't changed: G01 needs no access and can start now.

```text
/adk-engineer Carry out G01 from docs/plans/advertiser-campaign-assistant.md.
```

Files are in `docs/`:
- `architecture/advertiser-campaign-assistant.md`
- `plans/advertiser-campaign-assistant.md`
- `../REPORT.md`