I've revised the design, plan and tickets in `docs/` for the 8-day launch, without implementing anything. The pilot now launches with **booking only**. Moving and cancelling stay on the phone until right after launch, and anyone using the chat must sign in.

The schedule check reports 48–74 hours of work against 90 available after the 25 % reserve, and a finish of **5.2–8 working days against 8**. That fits, but with **no slack at the high end**. The limit is the calendar, not the hours: the longest run of dependent goals takes 7.87 days at the high end (contract → read-only agent → evaluation set → go-live).

**What changed:**
- **Phase 1 delivers:** signed-in customers at the pilot salon can see availability, list their own appointments and book with one confirmed click. When they ask to move or cancel, the assistant gives the salon's phone number.
- **Moved to phase 2:** cancel (G05) and move (G06) become the first goals after launch, each released on its own. Monitoring the first pilot days and recording baseline numbers move into G12.
- **Chat requires sign-in:** visitors without an account can no longer browse availability. Requests without a login are refused before any model call, so the per-IP limit is no longer needed. Anonymous browsing is on the plan's Later list.
- **New goal G22:** CI and the 30-day session deletion job came out of the platform goal so they don't hold up go-live. Until G22 lands, tests and the scripted evaluation are run by hand before each deploy, and the deletion job must exist before the first session is 30 days old.
- **Owners:** the chat API and widget (G07) moved to Dev A, and launch readiness (G10) to Dev C.
- **Not cut:** the 30-case evaluation set keeps its hours, rebalanced for booking only. All the minimum safety controls stay: verified login, click-to-confirm with safe retries, spend caps and the kill switch, and the pre-launch evaluation.
- **Rollback fix:** reviewing failures turned up one gap. If the later cancel or move release is rolled back, leftover proposals of that kind must be refused at confirm. I added that as a test in G04.

The plan lists each change with the finish date the check gave after it, plus the options that didn't close the gap.

**Decisions open:**
- **Cut line:** confirm a booking-only launch on day 8. Launching with booking and cancel needs the original 10 days; 9 days is not enough.
- **Assumptions:** confirm the assumed answers, especially that chat may require sign-in (A12), that nothing is built yet so day 1 starts now (A11), and that the existing login can be verified by our backend (A4). If A4 fails, the email one-time-code fallback (6–10 h) does not fit 8 days.

The only checks that ran were the schedule check (final run passes, no ticket mismatches) and the skill's own 11 tests for that script (all pass). No application tests exist yet, nothing that imports `google.adk` could run here, and prices and regions were not looked up because there was no network. I created a few temporary files while testing schedule options, including one empty file outside the project folder, and deleted them all. `REPORT.md` has the questions I would have asked and the friction log.

Next step, for the booking API contract and fake (Dev C starts the login ticket, G03, the same day):

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-contract-and-fake.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```