I've written the design, the plan, ten phase 1 tickets and `REPORT.md`. Everything is design only and still a **draft**, because each of the 12 assumptions I had to make is unconfirmed (they're listed at the top of the design).

**Where things are**
- Design: `docs/architecture/salon-booking.md`
- Plan: `docs/plans/salon-booking.md`
- Tickets: `docs/tickets/salon-booking/G01…G10-*.md`
- Report: `REPORT.md`

**What it is:** an MVP/pilot. Customers who are signed in to the website chat with one ADK agent. The agent can look things up and *propose* a booking, move or cancellation, but it cannot change anything itself. The change happens only when the customer presses Confirm on a card showing the exact details. A database record of each change stops a retry or timeout from booking twice. It runs on one Cloud Run service with Cloud SQL, using `gemini-3.8-flash`, chosen from the skill's dated list of model retirement dates.

**Cut line:** phase 1 is G01–G10 and ends with **one pilot salon live**. It's 62–95 hours of work against 135 available. The schedule checker gives a finish of 6–9.1 working days out of 10. Phase 2 (G11–G15) covers the other four salons, running the evaluation in CI, tracing and alerts, a sweep that settles uncertain bookings, and handing customers to salon staff.

- **Hours assumption:** the schedule depends on about 6 focused hours a day per person. At 5 hours the pilot needs one more working day. Moving goals between people made it worse in both versions I tried.
- **First run failed:** my first plan finished at 10.2 days. I fixed that by splitting the security tests (G09) from go-live (G10), since the tests can be written against a fake booking API before the confirm step exists.

**Who could take which** (roles, since I don't have names):

| Person | Goals |
| --- | --- |
| Dev A, agent lead | G02 agent skeleton, G07 instructions and evaluation set, G08 staging deploy |
| Dev B, knows the booking API | G01 booking API and sign-in check, G03 safe writes, G05 confirm step |
| Dev C, web and platform | G04 customer identity, G06 chat widget, G09 security tests, G10 pilot go-live |

**Decisions still open**
- **A2:** can our backend verify the website's customer sign-in? G01 checks this. If not, G04 grows by about a day.
- **A3:** does the booking API offer idempotency keys and a reschedule endpoint? G01 checks this too.
- **A6:** are there any cancellation fees? A fee would turn cancelling into a money operation.
- **A8 and A10:** which salon pilots first, and when does the operations manager sign off? Ask them on day 1.
- Do you accept the cut line, or would you move the pilot to day 11?

**Checks:** the final schedule check passed, and there are no broken links in the docs. I ran no tests that import `google.adk`, made no network or cloud calls, and looked up no live provider facts, so the model's region, prices and the ADK 2.8.0 version are unverified. The first ticket checks the ADK version. I put the what-if copies of the plan in `/tmp`, outside this directory against your rule, and deleted them at the end.

**Next prompt** (the skill's form):

```text
/adk-engineer Carry out G01 from docs/plans/salon-booking.md.
```

The longer form from the ticket template is in the plan summary and in `REPORT.md` section 6.