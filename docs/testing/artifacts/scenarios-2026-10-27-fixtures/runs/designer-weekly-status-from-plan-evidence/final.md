I've drafted this week's sponsor update at `docs/status/2026-10-27.md`, using the same shape as the 2026-10-18 one. I'm ending here with the summary below.

**What it says**
- **Overall:** amber.
- **G01:** built, with its tests passing locally on 2026-10-20. Priya's 0.5 h review of the forget path is still owed.
- **G02:** in progress. One of its three checks passes; the second is being fixed and the third isn't started.
- **G03, G04, G05:** not started.
- **Hours:** 8.5 of 14 h spent, from the ticket records: G01 took 6 h against 2–3 h estimated, and G02 has 2.5 h so far. I estimate 5–9 h remaining, which gives a projected total of 13.5–17.5 h. That uses the reserve but stays inside the 20 h raw allowance.
- **Decisions put to Mark:**
  1. Whether forget keeps its 30-day soft delete or deletes immediately. My recommendation is immediate deletion unless the privacy notice and support both accept 30 days.
  2. Whether to hold scope and use the reserve, or trim. My recommendation is to hold scope and revisit when G02 closes.
  3. The phase-1 review date (D3), still open.

**Assumptions to check before sending**
- **Remaining-hours estimate:** I made up the 5–9 h by taking the plan's estimates less the G02 hours already spent. Ana should confirm it.
- **`plan_status.py --weekly`:** I couldn't run it, because I had no shell tool in this session. The draft is built by hand from the plan and the five tickets, so the script's own numbers weren't cross-checked.
- **Commit and worktree:** the repository has no git history, so I couldn't check commit `7d2f0b9` or the G02 worktree at `../wt-G02`. I took them from the ticket notes.
- **Wasted call:** I called the `update-config` skill by mistake. It changed nothing.

**Left undone**
- **Plan and design left stale:** I didn't touch them, since you asked for the status draft only. Both would need a checkpoint:
  - The plan's "Resume here" still says "Next: G01", and its change log has no entry for this week.
  - The design's C1 and C2 evidence cells still read "planned", and the C2 change (forget also clears the session copy) isn't recorded there.
  - The 30-day soft delete is not yet a numbered decision (the ticket's ruling line doesn't say `settled: D<n>` or `rejected`).
- **G01 notes:** G01's ticket says "leave changes uncommitted" but records a commit on main.
- **Tickets:** I didn't run `check_tickets.py`.

Next prompt:
```text
/adk-engineer Carry out docs/tickets/support/G02.md.
```