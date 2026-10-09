I've written the design, the plan and the 9 phase 1 tickets. It's design only: nothing is implemented, nothing is committed, and no tests exist yet. Every product decision rests on answers I assumed, because I couldn't ask you; they're listed at the top of the design, which is marked **draft**.

**Where it is**
- Design: `docs/architecture/salon-booking-assistant.md`
- Plan: `docs/plans/salon-booking-assistant.md`
- Tickets: `docs/tickets/salon-booking-assistant/G01…G09-*.md`
- Report: `REPORT.md`

**Profile:** MVP. The users are real salon customers, and the assistant changes real appointments.

**Main design choices**
- **One agent, no direct write.** A single agent has three read tools and three "propose" tools that save a pending booking change. The model never writes to the booking API.
- **Customer confirms in the widget.** A booking changes only when the customer presses Confirm on a card built from the saved proposal. The confirm step is ordinary code: it checks the slot is still free, then makes the change once, even after retries or a lost response.
- **Why not ADK's built-in confirmation:** the skills note it isn't supported with the database-backed session storage that multiple Cloud Run instances need.
- **Sign-in:** customers use their existing website login. The customer's identity comes only from that verified login, never from the model.
- **Model:** `gemini-3.8-flash` on Vertex AI, pinned. The 3.6 and 3.7 versions retire on Vertex before phase 2 would end.

**Capacity and cut line.** I assumed each of you can give about 6 hours a day for the 10 days. That gives about 108 focused hours, or 81 after a 25% reserve. Phase 1 (G01–G09) is estimated at 48–79.5 hours, so it fits even at the high end. These estimates include a 1.5× allowance because I assumed you're new to ADK. Phase 2 (G10–G16: evaluation in CI, tracing and alerts, a security test suite, data retention and erasure, hand-off to salon staff, remembering preferences, safer releases) is written up at 33–66 hours for after launch. If phase 1 runs over, the plan cuts in this order: fewer evaluation cases, then launching at one salon only, then a lighter cost dashboard. None of these cuts touches the customer-confirmation step or the spending limits.

**Who could take which**

| Developer | Goals | Hours | Their share after reserve |
| --- | --- | --- | --- |
| Dev A (backend, knows the booking API) | G01 API contract and test fake, G03 propose/confirm, G08 Cloud Run deploy | 18–28.5 | 27 |
| Dev B (agent and quality) | G02 read-only assistant, G06 20-case evaluation set, G09 staging tests and soft launch | 13.5–22.5 | 27 |
| Dev C (web and auth) | G04 customer scoping, G05 saved conversations and daily limit, G07 chat widget | 16.5–28.5 | 27 |

At the high end Dev A and Dev C each go 1.5 hours into their reserve. Dev B has about 4.5 hours of slack, so they should do the second review of G03. G01, G02, G04, G06 and G07 can all start on day 1.

**Decisions you need to make**
- **Idempotency keys (G01 settles this):** whether your booking API accepts them. If it doesn't, the design still prevents duplicates by checking the customer's appointments after an unclear result.
- **Website login (G01 settles this):** whether the backend can verify the website's customer login. If not, a one-time-code login has to come into phase 1 and something else moves out.
- **Cancellation fees and wording sign-off:** whether cancelling ever costs the customer money, and who signs off on the assistant's wording. That sign-off takes a few days, so request it on day 1.
- **Budget, region and launch shape:** I assumed about USD 300 a month, your booking API's existing GCP region, and one salon for two days before all five.

**Checks.** I checked that the goal estimates add up, that every ticket matches the plan, that each person's load is right, and that all links resolve. That check caught one wrong phase 2 total, which I fixed. Not done:
- No tests exist yet, and none importing `google.adk` could run here.
- I didn't look up model or cloud prices (no network), so cost per conversation is something G08 measures.
- No ADK names were checked against an installed version.

The design is also longer than the skill's two-to-four-page guideline for an MVP; `REPORT.md` covers this with the other notes on the skills.

Next prompt:

```text
/adk-engineer Carry out G01 Booking API contract and fake from docs/plans/salon-booking-assistant.md.
Read docs/architecture/salon-booking-assistant.md and preserve its accepted decisions.
Use safe-api-tool-calls with adk-tool-auth-and-secrets.
Work within local code and offline tests, verify the fake reproduces commit-then-timeout
and the contract answers A6 and A7, and update the plan with actual evidence and remaining blockers.
```