I've written the design and a phased plan, but three weeks only works if things go well: the pilot goes live between working day 12 and day 21. A date you can commit to needs 21 working days. Waiting on other teams sets that date, not coding.

**Saved files:**
- Design (draft): `docs/architecture/campaign-assistant.md`
- Plan: `docs/plans/campaign-assistant.md`
- Report: `REPORT.md`
- Nothing was committed.

**Profile:** MVP/pilot, because five outside advertisers will use it and the journey ends in money committed.

**Design in brief:**
- **Sign-in and access:** advertisers sign in with your existing identity provider. A small table we keep maps each advertiser to its brands, and code checks each search against the rights system. The model never chooses which brand it searches for.
- **Shape:** one ADK agent with three tools (search, quote, propose order), run on Cloud Run with a Cloud SQL Postgres database.
- **Buying:** because the booking system's replay and status-lookup behaviour is undocumented, the assistant does not create orders directly in phase 1. The model can only propose an order. The advertiser confirms it with a button that the model cannot press. That creates exactly one order request, which booking operations enter by hand.
- **Direct ordering:** this is phase 2. It starts with a short investigation of the booking system (G11), then direct submission (G12), which marks an order "uncertain" when its outcome is unknown.

**Cut line, to confirm or move:**
- **Phase 1 (G01–G10):** sign-in, rights-filtered search, live quotes, confirmed order requests and a hosted go-live. That is 48.5–71.5 hours against 67.5 hours of capacity, so it also fits only at the low end.
- **Phase 2 (G11–G15):** direct ordering, tracing, an evaluation gate in CI and an attack test suite, about 27.5–43.5 hours.

**Schedule check:** the schedule script fails at 15 working days and passes at 21. Two outside waits sit on the critical path: API documentation from the rights, booking and identity teams, and the go-live sign-off after the hosted rehearsal. I tested other remedies against the schedule and none of them closes the gap:
- 20 working days
- a read-only pilot, which also drops buying
- an engineer who already knows ADK
- teams committing to shorter waits

**Review:** an independent reviewer found three prerequisites the schedule had left out, and those changed the verdict from "fits" to "fits only at the low end". It also found wrong or untested cells in the failure-coverage tables. All findings are settled in the plan's change table.

**Not checked:** there is no code yet and google-adk isn't installed, so no tests ran. With no network access, I couldn't verify the model choice (`gemini-3.8-flash`), Vertex prices or the ADK version (assumed 2.8.0); those checks are acceptance items in G01 and G08.

**Decisions open for you:**
- Accept a go-live window of day 12–21 (commit to day 21), or set another date.
- Confirm request mode for phase 1, or move direct ordering earlier.
- Confirm my eleven assumed answers in the design, especially whether the engineer is new to ADK and whether direct ordering may wait.
- Get the booking team's answers on replay and status lookup.

Next prompt:

```text
/adk-engineer Carry out G01 from docs/plans/campaign-assistant.md.
```

---- next turn ----

I've revised the design and plan for the new rights terms. The pilot no longer fits three weeks, even if everything goes well. Phase 1 is now 57.5–86 hours against 67.5 hours of capacity, and go-live lands between working day 16 and 28.56. A date you can commit to needs 29 working days, about six weeks. The schedule check fails at 15 days and passes at 29; I also added a revision 2 section to `REPORT.md`.

**What the change does to the design:**
- **Rights decided by code, not the model.** A new rule in code (D10) decides whether an asset is covered for the requested brand, channel, territory, whole flight and modification intent.
  - It expands region groups such as "DACH" and joins adjacent rights records.
  - It treats unknown territory codes or bad dates as not covered.
  - Assets covered for only part of the flight are listed with their gaps but can't be quoted or ordered.
- **No guessing.** Territory, flight dates and "will you modify the creative?" are now required inputs; if one is missing, the assistant asks.
- **The same rule runs at four points:** search, quote, the advertiser's Confirm, and when booking ops mark the order entered.
  - The quote must be for exactly the requested market and dates.
  - The order request carries the terms.
  - Ops must type in the booked dates and market, and can't mark the order entered if they differ or the rights have lapsed.
  - A new invariant (I6) covers this.
- **The rights team checks the rules.** They confirm the rule table before the rehearsal and go-live (new wait W5), with hours set aside for corrections (new goal G16). A wrong rule would show assets the advertiser isn't licensed to use.

**Why the date moved twice:** the first revision gave 23 working days. A second independent review then found prerequisites the schedule was missing:
- The sign-off has to follow the ops runbook.
- The day-1 requests have to be sent before any of the waits can start.
- The rights-semantics request needed its own wait of 2–5 days.
- The rule review needs correction time.
- Pilot planners and booking-ops time need their own waits.

**Remedies tested:** none of these closes the gap on its own:
- a read-only pilot (13.44–25 days, and it drops buying)
- an engineer who already knows ADK (12.37–23.08 days)
- the teams committing to shorter waits (14–23 days)

All three together would fit, but I don't recommend that.

**What was removed or weakened:** I compared everything against a saved copy of revision 1. All 81 acceptance items, 63 failure-table cells, the waits and the safety floor are still there, and 15 items were added. My first claim of "nothing weakened" was wrong: two items had been quietly weakened. A rights outage was being reported as "not covered" instead of "cannot check rights", and one cross-advertiser check no longer covered the new partly-covered list. Both are restored, and each change is listed in the plan's change table.

**Decisions for you:**
- Commit to working day 29 for go-live, or set another date.
- Confirm my four assumptions about how rights work: territory codes, date comparison, the modification flag, and combining rights records.
- Confirm that phase 1 keeps request-only ordering, with booking ops entering orders.
- Get the booking team's answers on replay and status lookup.

As before, no tests or network checks ran. `.revision-snapshot/` holds the revision 1 copies; delete it once you no longer need to recheck the comparison.

First, send the day-1 requests in G00 yourself; it's a 30-minute human task with no prompt. Then:

```text
/adk-engineer Carry out G01 from docs/plans/campaign-assistant.md.
```

Files are in `docs/`:
- `architecture/campaign-assistant.md`
- `plans/campaign-assistant.md`