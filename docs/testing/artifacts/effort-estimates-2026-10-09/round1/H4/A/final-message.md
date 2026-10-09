I've written the design, a phased plan, eight phase 1 tickets and `REPORT.md`, all design only. Every product answer is assumed because you weren't available, so the design is marked **draft** and the decisions that rest on an assumption are marked provisional. No tests ran: there's no code yet and google-adk isn't installed. I checked that the files and skills the tickets link to exist, and they all do.

**Profile:** MVP. Real customers make real changes to bookings, but no money moves.

**How it works:** one ADK agent, and the model never writes a booking itself. It only proposes a booking, move or cancellation. The customer then presses **Confirm** on a card built from the stored proposal, and ordinary code makes the call to your booking API. Each change is recorded so that a double click or a lost reply can't book twice. The rest:
- Customers are identified from your website's existing login, and the agent only sees their own appointments.
- Hosting is Cloud Run with Cloud SQL, on `gemini-3.8-flash` through Vertex AI.
- Spend is capped per turn, per customer per day and per IP address.

**Capacity and cut line:** I assumed about 126 focused hours across the three of you; keeping 30 in reserve leaves 96. Phase 1 (G00 to G07) is estimated at 65 to 94 hours, so it fits even at the high end, with little to spare. If it runs over, three things move to phase 2 first: the per-IP limit, half of the test cases, and widget polish. The safety controls don't move.

**Who could take which** (I used roles, since I don't know who is who):

| Developer | Goals | Hours |
| --- | --- | --- |
| Dev A, knows the booking API | G00 API check, G02 confirmed writes, G06 spend limits | 23 to 31 |
| Dev B, agent and Python | G01 agent reads availability, G03 customers see only their own bookings, G05 test cases | 22 to 31 |
| Dev C, web and infra | G04 chat widget and card, G07 deploy to Cloud Run | 22 to 32 |

**Phase 2 (weeks 3 to 5):**
- Tests running automatically before each release.
- Tracing. This is below the usual MVP level, moved out to make phase 1 fit.
- Deleting chat history after 30 days.
- Handing a conversation to salon staff.
- Tests that try to trick the agent.

**Decisions still open:**
- Whether your website login can be checked by the server. If not, customers need another way to sign in.
- Whether the booking API has a reschedule endpoint and accepts duplicate-protection keys. G00 finds out.
- Whether `gemini-3.8-flash` is available in your region, and its price. I couldn't look this up offline.
- Whether to launch at one salon first or all five. I recommend one salon for two days.
- Whether chat will ever take payments or cancellation fees.

The design came out at about 3,650 words, longer than the skill's two-to-four-page target for an MVP. `REPORT.md` has the full assumptions table, the checks, and a friction log with pointers into the skill files.

Files are in `docs/`:
- `architecture/salon-booking-assistant.md`
- `plans/salon-booking-assistant.md`
- `tickets/salon-booking-assistant/` (G00 to G07)

Next step, while Dev B starts G01 and Dev C starts the G04 skeleton:

```text
/adk-engineer Carry out G00 from docs/plans/salon-booking-assistant.md.
```