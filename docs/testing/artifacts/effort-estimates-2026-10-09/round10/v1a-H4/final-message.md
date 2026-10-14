The design, plan and nine phase 1 tickets are written. Phase 1 makes the two-week deadline only by going live at **one salon first**. The design is a draft, because none of the assumptions about your team and booking API could be confirmed with you.

**What was built:** a single ADK agent, using the pinned `gemini-3.8-flash` model, that customers reach through a chat widget on your booking site.
- **Identity:** the customer is identified from your site's existing login, never from what they type.
- **Writes:** booking, moving and cancelling only happen after the customer confirms the exact details on a card the code produces. Each change is recorded first so a retry or double click can't book twice.
- **Spend:** there are per-conversation and per-customer daily limits plus an off switch.
- **Where it lives:** Cloud Run, with sessions and the change record stored in a new schema on your existing Postgres.

**The cut line (please confirm or move it):**
- **Phase 1 (G01–G09):** 56.5–88.5 hours against 112.5 hours of capacity, after holding back 25% of each day.
- **Finish:** 6.4–10 working days. At the high end it lands exactly on day 10, with no slack beyond that reserve.
- **All five salons (G10):** about 3 working days after the deadline, once the first salon has run 3 days without problems.
- **If the work runs high:** "move" is the first thing to slip, if your API has no single reschedule call. Confirmation, change records and the misuse tests stay in.

**Who could take which:**

| Person | Goals | Hours | Strongest fit |
| --- | --- | --- | --- |
| Dev A | G01, G02, G07, G08 | 19–29.5 | Most interested in the agent and evaluation |
| Dev B | G03, G04 | 17.5–27.5 | Knows the booking API best |
| Dev C | G06, G05, G09 | 20–31.5 | Owns the website and GCP |

**Still open:**
- **Booking API:** whether it supports idempotency keys and a single reschedule call. G01 answers this on day 1.
- **Site login:** whether it issues a token we can verify. Also G01.
- **Confirmation emails:** whether you accept that each confirmed change sends the customer a real email or SMS.
- **Limits:** the per-customer allowance and the monthly budget.
- **Sign-off:** ask the salon chain owner to approve wording, policies and the privacy notice on day 1. It takes 3–5 days and blocks go-live.
- **Your team:** everything rests on the assumptions in the table at the top of the design. The biggest are about 5 focused hours a day each and a team new to ADK, which raises every estimate by half.

**Checks:** the scheduling script that comes with the skill passed against the plan and tickets. Its own 14 tests pass. No ADK code exists, so no `google.adk` tests ran. I made no network or cloud calls, so model prices and the ADK version (assumed 2.8.0) are unverified; G01 checks both.

G01 and G06 can both start on day 1. Next prompt:

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-api-contract-and-pins.md. Read its design and plan, use its primary and supporting skills, run its verification locally, fill in the Evidence section and set status. Leave changes uncommitted.
```

Files are in `docs/`:
- `architecture/salon-booking-assistant.md`
- `plans/salon-booking-assistant.md`
- `tickets/salon-booking-assistant/` (G01–G09)

`REPORT.md` is in the project root.