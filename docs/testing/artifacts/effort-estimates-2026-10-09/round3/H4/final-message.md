I've written the design, the plan and nine phase-1 tickets. Everything is still a draft: you weren't available, so every product decision rests on an assumption (A1–A10 at the top of the design). Nothing has been run against real code; the only check run was the schedule helper.

**The design.** One ADK agent (an AI agent built with Google's Agent Development Kit) in a chat widget on your existing booking site.
- **What the model can do:** look things up and *propose* a booking, move or cancel. It cannot change anything itself.
- **How a change happens:** the customer presses **Confirm** on a card showing the stored proposal. Only that confirm action writes to your booking API, and at most once per proposal.
- **When a write's result is unknown** (for example a timeout), the card says "We're checking this booking" and the code looks it up before trying anything again.
- **Who the customer is** comes from your site's existing login token, checked on the server. The model never gets to choose it.
- **Hosting:** Cloud Run with a small Postgres database, using `gemini-3.8-flash` on Vertex AI. I avoided the newer-looking alternatives that retire within a few months.

**Profile:** MVP / pilot for real customers of all five salons, behind a "beta" link, with the existing booking form kept as the fallback.

**Cut line.**
- Phase 1 (G01–G09) is 44.5–74 hours of the 81 available after a 25% reserve, so the hours fit.
- The calendar fits only at the low end: finishing takes 5.8–10.6 working days against 10. I tried every way of splitting the work between the three of you and none beats 10.6 days at the high end.
- The plan has a check at the end of day 6. If the work is running high, moving becomes "cancel, then book" (two confirmation cards). Together with booking the salon manager's walkthrough in advance, that brings the high end to 9.8 days.
- Phase 2 (G10–G14, 19–36 hours) adds automated evaluation on every change, retry-safe writes in the booking API, monitoring alerts, attack testing and streamed replies.

**Who could take which:**

| Person | Goals | Hours | Who fits |
| --- | --- | --- | --- |
| Dev A | G01, G02, G06, G07: booking API client, the agent, its evaluation, spend limits | 15.5–26.5 | Knows the booking API, likes model work |
| Dev B | G03, G05: the whole confirm path, from executing the change to the card | 13.5–21.5 | Most careful reviewer; a bug here double-books |
| Dev C | G04, G08, G09: login checks, deployment, launch | 15.5–26 | Knows the site's login and your Google Cloud project |

**Open decisions:**
- Whether your site's login token can be verified by our server (if not, add a magic-link login, about a day more).
- Whether the booking API accepts a key that makes repeated writes safe (G01 answers this).
- Customers or front-desk staff, and all five salons or one first.
- How long to keep conversations and proposals (I assumed 30 and 90 days).
- The cut line itself.

**Checks:**
- The schedule helper fits the hours but flags the calendar overrun above, which is why it exits with a failure.
- The helper's own tests weren't run: pytest isn't installed.
- No application tests exist yet, and `google-adk` isn't installed.
- The model's availability in your region and current prices aren't verified (no network here); G02 does that.

I briefly wrote one trial file to `/tmp`, outside the project folder, and deleted it straight away. REPORT.md has the full question log and friction notes.

G01 and G04 are ready to start now and don't depend on each other. Next:

```text
/adk-engineer Carry out G01 from docs/plans/salon-booking-assistant.md.
```

Files are in `docs/`:
- `architecture/salon-booking-assistant.md`
- `plans/salon-booking-assistant.md`
- `tickets/salon-booking-assistant/`
- `REPORT.md` (at the project root)