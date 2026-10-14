I've written the design, the plan and 12 phase 1 tickets. **Two weeks doesn't fit at the high end of the estimates**, so I recommend a later go-live date rather than cutting scope. Everything is a draft built on assumed answers; nothing was implemented or deployed.

**Profile:** MVP. Signed-in customers of all five salons book, move and cancel their own appointments through a chat widget on your existing site. The assistant can only propose a change; it happens when the customer clicks Confirm on a card, and it happens once even if the click is repeated.

**Cut line:**
- **Hours:** phase 1 is 53.5–77.5 human hours against 81 available. That assumes three developers at 3.6 focused hours a day for 10 days, with 25 % held in reserve.
- **Calendar:** the work finishes in 9.2–13.7 working days. The end can't be squeezed: run it on staging, wait for the salon chain's approval, then go live.
- **Recommendation:** keep the full scope and go live after 14 working days (Thu 5 Nov 2026).
- **Alternative:** 11 working days, if all three developers give 4.8 focused hours a day.
- **Cuts that don't help:** dropping the move operation, dropping the evaluation set, or even a read-only assistant (7.3–11.6 days) still miss 10 days at the high end. The scheduling script was run on each option.

**Who could take which:**
- **Dev A** (knows the booking API): G01 booking API discovery, G04 confirmed operations, G06 write adapter on staging, G11 go-live. 19–27 h.
- **Dev B** (front end, prompting): G03 the assistant and its tools, G07 chat widget, G09 evaluation set. 17.5–24.5 h.
- **Dev C** (backend, GCP): G02 sign-in and chat API, G05 spend and abuse limits, G08 Cloud Run deployment, G10 staging run and demo, G12 failure drills. 17–26 h.

**Decisions still open:**
- **The date (OD3):** confirm 14 days, or more hours for 11.
- **Login token (OD1):** whether your existing login gives a token the chat backend can verify. If not, add 8–14 h, and the finish moves out to 11.4–18.1 days.
- **Booking API (OD2):** whether moving an appointment is one safe call, and whether repeated requests are safely ignored. G01 settles this on days 1–2.
- **Salon chain:** their policies (W1) and their go-live approval (W2).
- **Cloud setup (W0):** the GCP project, region and monthly budget.
- **Model:** pinned to `gemini-3.5-flash` on Vertex AI.

**Review:** a separate reviewer found 17 problems in the first draft. The main ones were that the salon chain's approval has to wait for the staging run, and handoff hours weren't counted in the totals. They moved the finish from about day 11 to day 14. All 17 are fixed or recorded in the plan's change table. The plan wasn't reviewed a second time after the fixes.

**Checks:** the schedule, coverage grid and ticket consistency check finds no problems. It still exits 1 at 10 days, only because the calendar fits at the low end only; at 14 days it passes. The scheduling script's own 16 tests pass. No application tests were run because there is no code and `google-adk` isn't installed. I did no network lookups, so prices, model availability in the region and ADK's confirmation limits are unchecked.

Files are in `docs/`:
- `architecture/salon-booking-assistant.md`
- `plans/salon-booking-assistant.md`
- `tickets/salon-booking-assistant/`

`REPORT.md` is in the project root. G01, G02 and G03 can all start on day 1; G01 comes first because G04 depends on it:

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-write-contract.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```