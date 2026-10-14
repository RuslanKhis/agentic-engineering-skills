I've written the design and a phased plan for the advertiser assistant, but the plan is still a draft. Every answer you'd normally give was assumed, and I've recorded each one. At the high end it doesn't fit a three-week build: it fits if the build window is 17 working days.

**Profile:** pilot. Five external advertisers placing real orders means real money, so the safety basics stay in even though it's a pilot.

**Key design choices:**
- **One assistant, no buying power.** The AI has four tools, and none of them can place an order.
- **Buying happens outside the AI.** The advertiser confirms on a card showing the exact assets, dates and price from the stored quote. That card goes to an ordinary endpoint, which re-checks rights, quote expiry and ownership before recording anything.
- **Sales ops places orders by hand in phase 1.** The booking system's replay and status-lookup behaviour is undocumented. Automating the order now would mean promising "one confirmation, one order" with nothing to back it. Sales ops enters each confirmed request into the booking system, using the request ID as the booking reference.
- **Rights are checked live.** Search results are filtered by the advertiser's brands and channel before the AI sees them, and checked again at quote and at confirm.
- **Stack:** sign-in through your existing identity provider, model `gemini-3.8-flash` pinned, one Cloud Run service with a Cloud SQL database, ADK 2.8.0 as the working version.

**Schedule.** I assumed one full-time engineer new to ADK, which gives 54 hours after a 25% reserve. The figures come from the schedule-check script:

| | Hours | Working days | Fits 15 days? |
|---|---|---|---|
| Build (G01–G06) | 33–53 | 9.4–16.5 | Low end only; 17 days fits |
| Including go-live (approval, then onboarding) | 34–56 | 12.7–22.3 | No |
| Automated booking pulled into phase 1 | 44–73 | 12.4–22.1 | No; needs about 24 days |

**Cut line:** phase 1 covers search, live quotes, sign-in and confirmed purchase requests, plus an evaluation and a full run on the staging system. Go-live comes after the commercial approval, which is given on that evidence. Phase 2 (G07–G11) adds automated booking once the booking team answers, status lookup, an evaluation gate in CI and tracing.

An independent review of the plan found 18 problems, all now fixed in the plan. The two biggest:
- The go-live approval can't come before there's evidence to approve.
- The identity-provider registration needs the hosted URL, so it can't start on day 1.

Together those moved the go-live finish from about 16 to about 22 days.

**Decisions only you can make:**
- Whether sales ops can place orders by hand during the pilot. The cut line depends on this.
- A 15- or 17-day build window.
- Whether rights also depend on territory or dates.
- Whether the booking system supports a replay key or lookup by reference.
- Whether the security review needs the built system as well as the design.

**Checks:**
- The schedule check fails on 15 days (finish only fits at the low end) and passes on 17.
- Every failure-grid cell cites a test case, and all 11 promises in the design are covered by a goal.
- The schedule script's own 18 tests pass.
- Nothing that imports ADK was run (it isn't installed), and nothing touched the network or cloud. Prices and the exact ADK API names are unverified and are acceptance items in G01 and G02.

Next, send the access and approval requests listed in the plan (W2–W5 and W7–W10) on day 1, then run:

```text
/adk-engineer Carry out G01 from docs/plans/advertiser-campaign-assistant.md.
```

Files are in docs:
- architecture/advertiser-campaign-assistant.md
- plans/advertiser-campaign-assistant.md
- REPORT.md (in the project root)

---- next turn ----

I've revised the design and plan so rights cover territory, flight dates and modification, and appended a "Revision 2" section to `REPORT.md`. The cost is time: the build no longer fits three weeks. It now needs a 19-day build window (17 before this change), and both documents are still drafts.

**What changed in the design**
- **C1, the main rights promise, now checks all six fields.** An asset can only be quoted or bought if its grants cover every requested country for every day of the flight. One piece of code makes that decision everywhere it's checked: search, quote, proposal, confirmation, and the daily export just before sales ops places the order. It handles rights split across several grants and gives a reason when it says no, such as "rights end 31 July; your flight ends 14 August".
- **The assistant won't guess where or when.** It asks for countries and dates before searching. "UK" is mapped to the country code GB. The confirmation card shows the countries, dates and "as-is" use explicitly.
- **New C12: the cleared terms travel with each order.** The order request stores the countries, dates and grant IDs it was cleared against. Sales ops can only mark it placed if the booking matches those terms. That way delivery also knows not to modify the creative.
- **Phase 1 is as-is use only.** Advertisers can't request modified creatives during the pilot; that becomes a new phase-2 goal (G13). Because nothing modified is ever cleared, the modification right is always respected.
- **If the rights system is down**, confirmation is refused and the daily export holds the request rather than passing it on unchecked.
- **New failure cases:** rights narrowed before confirmation, rights narrowed before placement, rights ending mid-flight, and rights revoked during a live flight. The last one sits with the rights and delivery teams; I've left it as open decision O11.

**What changed in the plan**
- Four phase-1 goals grew: G01 to 7–11 h, G03 to 7–13 h, G05 to 6–9 h, G06 to 5–8 h.
- Two new waits, both requested on day 1:
  - W12: the rights team's answers on how dates, territories and modification are recorded.
  - W13: matching test data in the rights and booking staging systems.
- Phase 1 is now 38–63 hours against 54 available, and finishes in 10.6–18.5 working days against 15. Advertisers would start using it after 13.8–24.3 days.

**Options from the schedule script**

| Option | Fits? |
|---|---|
| 15 days | Only at the low end |
| 19-day build window | Yes (my recommendation) |
| 17 days, if the engineer has fewer interruptions (0.7 focus instead of 0.6) | Yes |
| Modification requests in phase 1 | Needs 21 days |

**Review.** A fresh reviewer found 16 problems, all now fixed in the plan, including two wrong what-if figures in my first pass:
- the proposal step had no rights test;
- nobody had defined what happens when the rights system is down at confirmation or export;
- test data wasn't requested;
- the next-step prompt still listed the old acceptance cases.

Nothing was removed. Every changed test was widened, and the only reduction is in scope: no modified creatives in phase 1.

The schedule check passes with `--days 19` and fails at 15 because it only fits at the low end. All 12 promises are covered by a goal. Nothing that needs ADK, the network or the cloud was run.

**Decisions for you**
- A 15- or 19-day build window.
- Confirm pilot campaigns use creatives as-is. If not, modification support moves into phase 1 and the window becomes 21 days.
- Confirm the assumed rules for dates (inclusive, no timezones) and territories (country codes).

The next step is unchanged:

```text
/adk-engineer Carry out G01 from docs/plans/advertiser-campaign-assistant.md.
```