The design, plan and 11 phase 1 tickets are written. The hours fit easily. The two-week calendar fits at the low end, but at the high end it overruns by about an hour. Every answer is my own assumption, since nobody was available to confirm anything, so the design is marked **draft**.

**Profile: MVP or pilot.** Real customers make real appointment changes and personal data is involved, so the safety minimum applies in full:
- **Confirmation in code:** the assistant can only *propose* a booking, move or cancellation. The change happens only when the customer presses Confirm on a card built from the stored proposal, and that step is ordinary code the model can't reach.
- **Exactly once:** each confirmed change is a stored record, so double clicks, retries and timeouts can't create a second booking.
- **Own data only:** the customer's identity comes from the booking site's verified login, never from anything the model says.
- **Spend stop:** a cap on model calls per turn, a daily limit per customer, a budget alert and a kill switch.
- **Pinned model:** `gemini-3.8-flash`, taken from the bundled model list. The 3.6 and 3.7 versions retire within the plan's horizon.

**Phase 1 (ship): G01–G11.** One pilot salon goes live with confirmed bookings, moves and cancellations, verified identity, a 30-case evaluation set and a runbook.
- Effort is 64–89 human hours against 112.5 h of capacity, after holding back 25 % as reserve.
- The finish range is **7.5–10.1 working days**, checked with `check_schedule.py`, against 10 available.
- With the same check, giving Dev A 6 focused hours a day instead of 5 brings it to 6.4–9.0 days. Accepting a launch on day 11 also works.

**Phase 2 (later): G12–G17.** An evaluation gate in CI, monitoring and alerts, an attack test suite, a 30-day deletion job, automatic recovery of unconfirmed bookings, then all five salons.

| Person | Goals | Hours |
| --- | --- | --- |
| Dev A: booking API, writes, cloud setup, launch | G01, G03, G07, G11 | 25–34 |
| Dev B: agent and evaluation (also reviews G03) | G02, G06, G08, G09 | 19–28 |
| Dev C: identity, chat widget, runbook | G04, G05, G10 | 20–27 |

**Decisions still open:**
- Can the booking API take idempotency keys, and is a reschedule one step or two? G01 answers this, and it shapes G03.
- Can our service verify the booking site's customer token? This is G04's first step.
- The salon owner has to sign off the policy windows, the pilot salon and the privacy notice. Request it on day 1; go-live (G11) waits for it.
- More hours for Dev A, or a day-11 launch.
- Confirm or move the cut between phase 1 and phase 2.

**Checks:** the schedule checker ran clean against the tickets, with the result above, and the checker's own 10 tests pass. None of the tests the tickets describe exist yet, and nothing importing `google.adk` was run. Design plus plan is about 5,000 words against the skill's 4,000 target, because I kept every failure case and invariant table.

Files are in `docs/`:
- `architecture/salon-booking-assistant.md`
- `plans/salon-booking-assistant.md`
- `tickets/salon-booking-assistant/` (G01–G11)

`REPORT.md` is in the current directory.

Next prompt:

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-contract.md. Read its design and plan, use its primary and supporting skills, run its verification locally, fill in the Evidence section and set status. Leave changes uncommitted.
```