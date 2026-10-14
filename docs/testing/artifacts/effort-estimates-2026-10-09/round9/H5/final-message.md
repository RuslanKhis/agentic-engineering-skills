I've written the design, the plan and 27 phase 1 tickets. Everything is still a draft: you weren't available, so all choices rest on 15 assumed answers (A1–A15, at the top of the design). Nothing was implemented, provisioned or verified online.

**Files**
- Design: `docs/architecture/home-claim-intake.md`
- Plan, with the schedule: `docs/plans/home-claim-intake.md`
- Tickets: `docs/tickets/home-claim-intake/G01…G27-*.md`
- Report you asked for: `REPORT.md`

**Profile:** a production service. Customers are external, the data is regulated personal data, and the system writes to Guidewire. I've treated phase 1 as everything up to GA in Germany on 2027-03-15: staging on synthetic data, then a limited pilot with real customers, then GA.

**How the claim gets created:** the AI never creates the claim itself. One assistant collects the claim into a saved draft. A separate model call describes the photos and has no tools. A Guidewire claim is only created when the customer presses Confirm on a review screen showing the exact draft. A background worker then makes the call, built so a timeout or a double click can't produce a second claim.

**Cut line**
- **Effort:** phase 1 is 668–1,122 person-hours against 2,340 available after a 25 % reserve, or 29–48 % of capacity.
- **Calendar:** the schedule script projects 58–95 working days out of 100. The limit is the chain of dependent work, not the hours; the longest chain is 91.7 days at the high end.
- **After GA:** six phase 2 items, including claim status in chat, a second market and the mobile app. A later list holds the rest.
- **Check:** the final schedule run passed, and the 27 tickets match the plan exactly.

**Decisions still open**
- **O1, Guidewire:** I don't know whether ClaimCenter lets us find a claim again by our own reference. Until G02 answers this, "one claim per confirmation" is a goal, not a guarantee.
- **O2, model:** `gemini-3.8-flash` was chosen because the version table shows the 3.7 and 3.6 models retiring before GA. It hasn't been confirmed in an EU region (G01).
- **O3, ADK version:** 2.8.0, which the skills were written against, or 2.10.0 or later, which the observability skill recommends for new production systems (G03).
- **O4, sign-in and portal:** what the customer portal's login token contains, and what its frontend is built with.
- **O5, input screening:** whether Model Armor is available in the EU.
- **O7, spare hours:** should some phase 2 items move forward? I'd suggest keeping the extra hours as a buffer against underestimates.
- **Your confirmation:** the assumed answers A1–A15 and the cut line.

**Outside waits:** the DPIA sign-off (25–40 days) and the Guidewire sandbox access gate the pilot and the Guidewire work. G01 requests them on day 1.

**Next step:** G03 is ready and starts the longest chain. G01 and G02 are also ready and can run in parallel; start G01 on day 1 because it sends the requests above.

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G03-walking-skeleton.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```