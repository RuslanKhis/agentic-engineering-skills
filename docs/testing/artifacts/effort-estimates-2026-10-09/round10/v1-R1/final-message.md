I've revised the design, plan and tickets for the 8-day launch. The skill's schedule check passes on the real files: 48.5–74.5 human hours against 90 available after the 25% reserve, and a finish of 5.47–8 working days against 8. Nothing was implemented, and no application tests could run because there is no app code yet and google-adk isn't installed.

**There is no calendar slack beyond the reserve.** At the high end all three developers finish their last pre-launch goal on day 6.67, and the go-live goal (G11) fills the rest. A 1–2 hour overrun near the end (I tested one on G05) pushes the finish to 8.53 days and eats into the reserve.

The previous scope can't fit 8 days under any owner assignment (best 9.6 days), so I made five cuts. Each is an assumed answer (A11–A15) for the owners to confirm. None removes a safety baseline item (identity, click-to-confirm, safe retries, caps, kill switch, budget alert, pinned model, no personal data in logs).

| Cut | What it costs |
| --- | --- |
| A11: moving an appointment becomes two confirmed steps, book the new time then cancel the old one; one-step move (G06) moves to phase 2 | Not atomic: if the cancel fails, the customer holds two appointments. This now has its own failure row |
| A12: chat requires sign-in; anonymous chat later (G22) | Visitors can't ask the assistant before signing in. It also removes model spend from unauthenticated visitors |
| A13: pre-launch evaluation drops from 30 to 20 cases, every category kept | Weaker evidence; G14 grows it back to 30 or more |
| A14: Cloud Trace export waits for G16; structured logs only at launch | The pinned ADK version lacks the trace fix anyway |
| A15: 30-day session deletion job built after launch (G21) | Hard deadline: it must run before launch day + 30 |

Three structural changes go with the cuts:
- **G04 split:** the old booking goal is now G04a (confirm-and-dispatch core) and G04 (the booking tool), so cancel and the chat API can start earlier.
- **Hidden dependency fixed:** the chat API ticket (G07) now depends on G04a. Revision 1 missed this even though G07's acceptance used confirmed bookings.
- **Budget alert moved:** it went from G09 to G10, which takes half an hour off Dev C, the developer who finished last.

The plan lists every removed or weakened test, failure row and acceptance case with its reason. The design also gained the failure coverage grid the skill requires, which revision 1 lacked.

**Alternatives I tested:**
- 9 days restores the 30 cases, trace export and the pre-launch deletion job (finish 7.67–8.67).
- Keeping the one-step move doesn't fit even 9 days, because Dev A would be overloaded.
- If the existing login can't be verified (A4), the email-code fallback gives 6.8–10.67 days with these owners and would force a re-plan.

**Decisions for you or the salon owners:**
- **The cut package:** confirm A11–A15, or choose 9 working days instead.
- **Earlier assumptions:** confirm A4 (login), A5 (no deposits) and A7 (24-hour policy window).

**Rule slip:** for a few minutes my scratch scripts sat in `/tmp`, outside the working directory. I moved them in and deleted them, and also deleted a `__pycache__` folder my search created inside the skill folder.

REPORT.md lists the questions I'd have asked, the checks (the skill's own helper tests passed, 14 of 14) and the friction log.

Next prompt, from the plan (Dev C can start G03 the same day):

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-contract-and-fake.md.
Read docs/architecture/salon-booking-assistant.md and preserve its accepted decisions.
Use safe-api-tool-calls with adk-tool-interface-design.
Work locally only, verify the ticket's acceptance cases, and record evidence and
remaining blockers in the ticket.
```

Files are in `docs/`:
- `architecture/salon-booking-assistant.md`
- `plans/salon-booking-assistant.md`
- `tickets/salon-booking-assistant/` (`G04a-operations-core.md` is new)

REPORT.md is in the project root.