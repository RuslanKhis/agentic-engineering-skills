I've written the design, the plan and 11 phase 1 tickets. Phase 1 fits your two weeks only if the launch covers one pilot salon with a plain chat widget; adding the other four salons and slot cards fits in 11 working days instead. Nobody could answer questions, so every decision rests on assumptions (A1 to A10) listed at the top of the design. The design stays a draft until you confirm or correct them.

**Profile: MVP.** Real customers, real bookings, and the team needs to see failures and cost.

**What phase 1 delivers:**
- **Scope:** signed-in customers of the pilot salon can book, move and cancel their own appointments through a chat widget on the salon website.
- **Design:** one ADK agent on the pinned model `gemini-3.8-flash` (Vertex AI), running on Cloud Run with a Postgres database.
- **How changes happen:** the agent can only *propose* a booking change. Nothing reaches your booking API until the customer clicks Confirm on a proposal showing the exact salon, service, stylist and time. A double click or a lost response can't create two bookings.

**Effort and finish:**
- Phase 1 needs 56–88.5 hours against 112.5 hours of capacity (three people × 5 focused hours a day × 10 days, with 25% held in reserve).
- The schedule helper puts the finish at 6.13–9.87 working days, so it fits with little slack.
- Two scope cuts were needed to get there. My first plan finished at 11.47 days at the high end; reassigning goals and splitting them along real dependencies only brought it to 10.67.

**Cut line:**
- **Phase 1 (G01–G11):** the pilot salon, with a plain widget.
- **Phase 2:** the other four salons (G12, straight after a clean pilot), slot cards (G13), and a CI evaluation gate, adversarial tests, alerts, data erasure and automatic recovery of unclear bookings (G14–G19).
- **Instead of the cut:** the full scope fits in 11 working days.

**Who could take which:**

| Person | Goals | Hours |
|---|---|---|
| Dev A (knows the booking API best) | G01 API contract and test fake, G04 booking with confirmation, G06 move, G10 runbook and drills | 19–29.5 |
| Dev B (agent, evaluation, frontend) | G02 read-only agent, G07 chat API and widget, G08 30-conversation evaluation set, G11 pilot go-live | 19–31 |
| Dev C (identity and platform) | G03 customer login, G05 cancel, G09 Cloud Run platform | 18–28 |

On day 1, Dev C should request the GCP project and a staging key for the booking API, and Dev A should ask the salon owner to sign off the assistant's wording, the cancellation policy text and the pilot salon.

**Decisions you need to make:**
- **A4: can our backend verify your existing customer login?** If not, an email one-time code costs 6–10 more hours and pushes the finish past 10 days.
- **A6: does the booking API accept an idempotency key, and does it have a reschedule endpoint?** This decides how strongly duplicate bookings are prevented.
- **A7: who enforces the cancellation window?**
- **A5:** confirm that no deposits or payments are involved.
- Confirm the cut line, or choose the extra day.

**Checks:**
- The schedule check passes on the final plan and tickets, and the helper's own 11 tests pass.
- No application tests exist or ran: this was design only, and `google-adk` isn't installed.
- I couldn't look up prices, quotas or regions without network access; that lookup is part of G09.
- After the schedule check I added one small item to G07 (one chat turn at a time per conversation) without re-estimating it.

Files are in `docs/`:
- `architecture/salon-booking-assistant.md` (design)
- `plans/salon-booking-assistant.md` (plan)
- `tickets/salon-booking-assistant/` (tickets G01–G11)

`REPORT.md` covers the questions, assumptions, checks and friction log.

Next prompt (Dev C can start G03 the same day):

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-contract-and-fake.md.
```