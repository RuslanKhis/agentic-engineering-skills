I've written the design, the plan and eight phase 1 tickets. If the bad cases add up, the plan doesn't fit two weeks: at an assumed 5 focused hours a day each, go-live lands in 7 to 11 working days against your 10.

The 57–88 hours of work fit inside the 112.5 you have after a 25% reserve. The calendar is the problem: the chain from G02 (sign-in) through G03 (bookings) to G07 (launch) can't be split or cut short. Dropping "move appointment" or halving the evaluation cases didn't bring the finish forward. You have two options:
- **Accept go-live on day 11** if G02 and G03 both run long.
- **Give 6 focused hours a day each**, which finishes in 5.8 to 9.1 days.

The schedule helper produced these figures (exit 1 at 5 h/day, exit 0 at 6). Its 11 unit tests pass. No ADK tests exist or could run, since this was design only and google-adk isn't installed. I didn't check anything online, so model availability in your region, prices and the right ADK version are still to verify.

**Profile:** MVP / pilot. It works on real customer data and makes real booking changes, but takes no payments.

**The design in brief:**
- **One agent:** it can search availability, list the customer's appointments, and *propose* a booking, move or cancellation.
- **Writes happen outside the agent:** a booking only changes when the customer clicks Confirm on a card showing the exact details. Plain code then makes exactly one call to your booking API. If that call times out, the code checks the customer's appointments to see whether it went through, rather than retrying.
- **Identity:** the customer comes from your booking site's existing login, never from the model, so they can only see and change their own appointments.
- **Hosting and model:** Cloud Run with a small Cloud SQL database for conversations, and `gemini-3.8-flash` on Vertex AI. The two older Flash models retire on Vertex within the next few months.
- **Spend caps:** limits on model calls per message and messages per customer per day, plus an hourly rate limit.

**Who could take which ticket:**

| Person | Tickets | Hours | Best fit |
| --- | --- | --- | --- |
| Dev A | G01 read-only agent, G03 confirmed bookings | 18–27 | Knows the booking API best |
| Dev B | G02 customer sign-in, G06 Cloud Run and spend caps | 15–25 | Owns the site login and the GCP project |
| Dev C | G05a label 30 test conversations, G04 chat widget, G05 evaluation runner, G07 launch at one pilot salon | 24–36 | Owns the booking site frontend |

G01, G02 and G05a have no prerequisites, so all three of you can start on day 1.

**What waits:** phase 2 (enabling all five salons, an evaluation check in CI, a per-customer token budget, duplicate-safe writes in your booking API, alerts) and the "later" list are in the plan. Deleting chat history after 30 days (G13) must ship within 30 days of launch.

**Open decisions** (O1–O5 in the design):
- **Sign-in:** can our backend verify the booking site's login token? If not, G02 changes.
- **ADK version and model:** the skills were checked against ADK 2.8.0, but the observability guidance recommends 2.10+ for a new production service. Is the model available in your region?
- **Region and data terms:** which GCP region and data-processing terms suit the salon chain?
- **Moves and fees:** does the booking API reschedule natively, and are there cancellation fees? Fees would mean money, and stricter confirmation.
- **Pilot salon:** which salon goes first?

I assumed all of these, plus team hours, budget and channel. Each assumption is in the table at the top of the design.

To start, run:

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-read-only-assistant.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

Files are in `docs/`:
- architecture/salon-booking-assistant.md
- plans/salon-booking-assistant.md
- tickets/salon-booking-assistant/ (8 tickets)

The report is `REPORT.md`, with all six sections you asked for.