I've written the design, the plan and 11 phase 1 tickets. All three developers have enough hours, but the 10-day deadline only holds if estimates come in low; at the high end the launch slips to day 11–12. It's design only: no code, and no live checks of the booking API or Google Cloud.

**Where things are**
- Design (draft): `docs/architecture/salon-booking-assistant.md`
- Plan: `docs/plans/salon-booking-assistant.md`
- Tickets: `docs/tickets/salon-booking-assistant/G01…G11`
- Session report: `REPORT.md`

**The shape.** This is an MVP for real customers making real bookings. One ADK agent can look up services, free slots and the customer's own appointments, and propose a booking, move or cancel. It has no tool that writes to the booking API. A change happens only when the customer presses Confirm on a card showing the exact details; code then checks it's their booking, makes the change once, and shows the booking API's reference. If the API's reply is lost, the change is marked "uncertain" and checked rather than retried blindly. Customers must be signed in through the existing booking platform, and their identity comes from code, never from the model. Model: `gemini-3.8-flash` on Vertex AI; ADK version: `google-adk==2.8.0`. Both are provisional until checked.

**Cut line.** Phase 1 (G01–G11) launches at all five salons, one salon first. It needs 57–88 of the 112.5 hours available. That assumes 3 people × 5 focused hours a day × 10 days, with 25% held in reserve. Phase 2 (G12–G18, 47–80 h) waits: CI evaluation gate, session retention and erasure, security test suite, alerts, cost dashboard, guest booking.

**The deadline.** The schedule checker puts the finish at 6.7–11.1 working days. I tested three scope cuts (cancel-only, booking-only, a smaller managers' goal) and none fits 10 days. Only two things close the gap: the team confirming about 6 focused hours a day, or moving launch to day 12. Since you weren't available, I assumed: aim for day 10, decide go/no-go at the end of day 7, and launch on day 12 if needed. The safety basics (sign-in checks, confirm-before-change, spend limits) stay in either way.

**Who takes what**

| Developer | Focus | Tickets | Hours |
| --- | --- | --- | --- |
| Dev A | the agent and its booking changes | G02, G04, G05 | 17–27 |
| Dev B | booking API check, chat widget, test conversations, managers' daily change list | G01, G06, G07, G10 | 21–31 |
| Dev C | customer sign-in and sessions, cloud setup, hosting, launch | G03, G08, G09, G11 | 19–30 |

On day 1, also ask for staging booking API credentials, the GCP project and a slot to brief the salon managers.

**Still open**
- Whether the booking API accepts a customer token you can verify, and whether it supports idempotency keys and has staging (G01 answers these).
- Today's baseline of phone or manual changes per salon, to measure the benefit.
- Whether guests without an account can book.
- `gemini-3.8-flash` versus `gemini-3.5-flash` (the test conversations in G07 decide).
- Day 10 versus day 12 for launch.

**Mistake:** I wrote one file to `/tmp`, outside the allowed directory, and deleted it in the next step. It's noted in `REPORT.md`.

Next prompt:

```text
/adk-engineer Carry out G01 from docs/plans/salon-booking-assistant.md.
Read docs/architecture/salon-booking-assistant.md and preserve its accepted decisions.
Use safe-api-tool-calls with adk-tool-auth-and-secrets.
Work within the staging booking API only, verify G01's acceptance cases, and update
the plan with actual evidence and remaining blockers.
```