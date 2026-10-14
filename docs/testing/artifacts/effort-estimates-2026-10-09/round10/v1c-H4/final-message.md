The design, plan and nine phase 1 tickets are written, but the plan only fits the two weeks if the work comes in at the low end. At the high end it finishes on day 10.44 of 10. No code was written, and nothing that imports `google.adk` could run here. Everything rests on assumptions I made without you, so the design is marked **draft**.

**What's built:** an MVP for signed-in customers of the five salons, using a chat widget on the existing website. They can book, move and cancel their own appointments. The assistant only drafts the change. The booking happens when the customer presses Confirm on a card that our code builds, and the booking API makes the change exactly once. The model never has a write tool, and the customer's identity comes from the website login, not the conversation.

**Does it fit:** phase 1 (G01–G09) is 61–96 hours against about 135 available after a 25 % reserve, so the hours fit. Dev B's queue (G02, G07, G08) is what pushes the finish past day 10. I tried ten other ways to close the gap in the schedule checker, and none worked:
- Cutting move/cancel (G05) changed nothing.
- Moving goals between people made it worse or no better.

The only change that worked is **Dev B putting in 7 focused hours a day instead of 6**, which brings the finish to 6.06–9.49 days. Otherwise launch slips to day 11. That choice is yours. Phase 2 (G10–G14, 32–60 h) holds the evaluation check in CI, monitoring and alerts, guest browsing, attack testing and latency work.

**Who could take which** (roles, since I don't know your names):

| Person | Goals | Hours |
| --- | --- | --- |
| Dev A, knows the booking API | G01 shared interfaces, test double of the booking API and answers about the API; G04 confirmed booking runs once; G05 move/cancel with the 24-hour rule; G09 end-to-end test and launch | 27–41 |
| Dev B, owns the agent | G02 agent and its tools; G07 test set of 20–25 labelled conversations; G08 staging setup on Google Cloud | 19–30 |
| Dev C, web and sign-in | G03 sign-in and per-customer access; G06 chat API and widget, then reviews G04/G05 with spare time | 15–25 |

**Decisions you need to make:**
- Confirm or move the cut line, and say whether Dev B can give the extra hour a day.
- Does the website login give a token our backend can verify? If not, sign-in takes about a day longer.
- Does the booking API support idempotency keys (so a retried request can't book twice) and moving an appointment in one step? You own the API, so these can be added.
- Can the pinned model (`gemini-3.8-flash`) run in an Australian region, or is the chain fine with it running elsewhere?
- The salon chain must sign off the 24-hour rule, a test stylist for live checks, the use of customer data and the go-live date. Ask on day 1; I've allowed 3–5 working days.

All my assumptions (three full-time developers at about 6 focused hours a day, new to ADK, no payments, Australia region) are in the Assumed answers table at the top of the design. REPORT.md has the six sections you asked for.

Files are in `docs/` under the current directory:
- `architecture/salon-booking-assistant.md`
- `plans/salon-booking-assistant.md`
- `tickets/salon-booking-assistant/G01…G09-*.md`
- `REPORT.md` (top level)

Next prompt, taken from the G01 ticket:

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-contracts-and-skeleton.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

Once G01 is done, G02, G03 and G08 can start in parallel.