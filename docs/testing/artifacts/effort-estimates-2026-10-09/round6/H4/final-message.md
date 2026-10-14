I've written the design, the plan and ten phase 1 tickets, but phase 1 does not reliably fit your two weeks. At the high end of the estimates it finishes in 6.9–11.9 working days against your 10. The total hours fit; what slips is the order the work has to happen in. Every product answer is my assumption, since you weren't available to ask, so the design is marked **draft**.

**Profile:** an MVP pilot. Signed-in customers book, move and cancel real appointments through a chat widget inside your existing booking web app.

**How a change happens:** one ADK agent reads the booking data and proposes a booking, move or cancellation. It cannot make the change itself. The customer presses **Confirm** on a card, and ordinary code then makes exactly one call to your booking API, with a key that stops duplicates. If that call times out, the change is marked "uncertain" and checked by looking it up, never sent again. The customer's identity comes from your web app's sign-in, not from anything the model says.

**Phase 1 is 57–90 hours of work, against about 112 hours available after a 25% reserve.** The finish depends on dependencies and on each person doing one goal at a time, which is where it slips.

Two changes I tested would make it fit, and you need to pick one:
- **Allow 12 working days instead of 10.** This fits at the high end.
- **Launch only the pilot salon in phase 1, and have all three of you give 6 focused hours a day.** This finishes in 5.6–9.9 days. The other four salons become the first step of phase 2.

There's also a fallback built into the plan: if G04 or G06 isn't done by the end of day 6, go live at the pilot salon only.

**Who could take what:**

| Developer | Goals | Hours |
|---|---|---|
| Dev A, who knows the booking API | G01 API contract and test fake, G03 proposals, G04 confirmed changes, G10 testing and go-live | 21–33 |
| Dev B, testing and data | G07 labelled test conversations (can start on day 1), G02 read-only assistant, G08 evaluation and tuning | 16–25 |
| Dev C, frontend and sign-in | G05 gateway with identity and a daily limit per customer, G06 chat widget, G09 staging on Cloud Run | 20–32 |

Dev B has the most slack, so they help first if someone falls behind. Phase 2 (G11–G16) and a "later" list with what triggers each item are in the same plan.

**Decisions still open:**
- Does your web app issue a sign-in token the backend can check?
- Does the booking API accept a duplicate-protection key, and can it move an appointment in one call? G01 answers these two in its first hours.
- Which salon is the pilot, and who at the chain approves go-live?
- Which of the two schedule options you want.
- Who handles "uncertain" changes after launch.

**Checks:** the skill's schedule checker found no differences between the plan and the tickets. It exits with status 1 only because of the calendar slip above. Its own 10 tests passed. Nothing else was tested: there is no application code yet, ADK isn't installed, and I made no network lookups. So prices, regions and the availability of the pinned model (`gemini-3.8-flash`, ADK 2.8.0) are unverified and are checks inside G01 and G09. Design plus plan come to about 4,950 words against a guide of about 4,000, and tickets run about 245 words against about 150.

REPORT.md has the six sections you asked for. It covers the skill files in the order I opened them, the 13 assumed answers, the checks, and the friction log with pointers into `.claude/skills/...`.

Next, type:
```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-contract.md.
```
G05, G07 and G09 have no dependencies, so they can start the same day.

Files are in `docs/`:
- architecture/salon-booking-assistant.md
- plans/salon-booking-assistant.md
- tickets/salon-booking-assistant/ (G01–G10)