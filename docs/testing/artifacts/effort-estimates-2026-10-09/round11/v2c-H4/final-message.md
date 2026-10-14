I've written the design, the plan and nine phase 1 tickets, plus `REPORT.md`. The main finding: with three developers, launching at a pilot salon fits 12 working days, but 10 only if the work runs at the low end of the estimates.

**Profile:** MVP or pilot. Real customers and real bookings are involved, so these are built in phase 1, not deferred:
- Customers are identified from the website login.
- The model can only *propose* a change; nothing is written until the customer taps Confirm in the widget.
- Each confirmation changes a booking at most once, and an unclear outcome is checked rather than retried blindly.

**Cut line:** phase 1 (G01–G09) puts the assistant live for logged-in customers of **one pilot salon**. That's 69.5–109 hours of work, which fits the 135 hours the three of you have after a 25 % reserve. The schedule finishes in **7.2–11.7 working days**. Phase 2 starts with G10, turning on the other four salons after one clean pilot day.

Before giving the 11.7-day figure, I tried every way of splitting the goals between the three of you, plus several scope cuts. The best result was 10.2 days, so I kept full scope and recorded a 12-day pilot date as an assumption for you to accept or replace.

A reviewer agent with no prior context checked the plan. It found missing items: no wait for GCP approval, wording sign-off asked for before the wording exists, nobody owning the kill switch or the staging credential, and some failure cases pointing at tests that didn't cover them. I settled all of them in the plan's change table; fixing them is what pushed the finish past 10 days. The scheduling script passes against a 12-day date and reports "low end only" against 10 days.

**Who could take which:**
| Person | Goals |
| --- | --- |
| Dev A (agent, model, deployment) | G02 agent and its tools, G07 deployment, alerts and runbook |
| Dev B (login and frontend) | G06 chat widget, G03 login check, sessions and kill switch, G05 instructions and 15-case evaluation set |
| Dev C (booking API and writes) | G01 booking API contract, credential and test data, G04 confirmed writes, G08 end-to-end on staging, G09 pilot launch |
| Team lead | Ask on day 1 for GCP approval and the salon chain's sign-off; wording sign-off follows later |

**Questions for you (all assumed for now, listed in the design):**
- **Website login (Q2):** can your backend verify the website's customer login? This needs settling before day 1: if customers need a one-time code instead, the finish moves to 9–14.8 days.
- **Date or scope (Q15):** accept 12 working days, or name what to drop.
- **Booking rules (Q7):** 24-hour cutoff for moves and cancellations, consultation-only services excluded.
- **Website (Q16):** I assumed your team maintains the website and can embed the widget.
- **Booking API (Q6):** whether it supports idempotency keys and an atomic reschedule. G01 finds this out.

Nothing was run except the scheduling script: there is no code, and no tests or live calls. I couldn't check prices, regions or the model's retirement dates online, so those are still to verify. My scratch copies and the reviewer's ended up in `/tmp`, outside this directory; I deleted them and a stray cache file, and noted it in `REPORT.md`. Nothing is committed.

Files are in `docs/`:
- `architecture/salon-booking-assistant.md`
- `plans/salon-booking-assistant.md`
- `tickets/salon-booking-assistant/` (G01–G09)

Next prompt:

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-write-contract.md.
```