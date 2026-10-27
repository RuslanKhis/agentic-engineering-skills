I ran the checkpoint by hand and moved the cut line on an assumption, because nobody was there to answer. I could not run `plan_status.py`, `check_schedule.py` or `check_tickets.py`: Bash is disabled in this session. The totals are hand-computed and none of the checkers has run.

**Contract delta on C2:** I revised the C2 row in place and kept its ID. Forget now also clears the cached `user:language` from session state, and removes the stored row outright. I also set C1 and C2 evidence to `evidenced: local`. G01 and G06 already cite C2.

**Ruling on soft delete: rejected.** G01 built a 30-day soft delete that nobody had decided. The design says "forget", and hard delete is the reversible default. I recorded this as provisional D4 and added G06 (1 h) to replace the soft delete with a row delete. G06 also carries Priya's owed 0.5 h read of the forget path.

G01's A3 test is named `..._clears_row_and_session_copy`, but the ruling says the row is kept. G06 must check what that test really asserts.

**Overrun:** G01 took 6 h against an estimate of 2-3 h, so 6 of the 10 h are spent. The remaining work (G02 to G05 plus the G06 rework) needs 7-12 h against 4 h left, so it doesn't fit even at the low end. I re-estimated G02 from 2-4 h to 3-5 h. I left G03 and G04 as they were. I cut the floor nowhere:

- **Phase 1 (9-10 h):** G01, G06 and G05, the review of the language-preference slice.
- **Phase 2 (5-9 h, unfunded):** G02, G03 and G04, streaming and failed replies. C3 and C5 stay planned.
- **G05:** it now depends on G06 instead of G04.

I wrote the plan, the design and the tickets (including the new `G06.md`) to disk.

**Questions written down, with the assumption I proceeded on:**
- Does the privacy notice allow 30-day retention, and does support need the complaint view? I assumed no. Priya and the support lead can settle it.
- Is capacity still 10 h? I assumed yes. About 15-19 h would put streaming back in the review.
- Does the review go ahead on the language slice alone? I assumed yes.

**Left undone:**
- The three scripts above, including a rerun of `check_schedule.py` and the ticket check.
- The independent plan review.
- The `--gate` run, since phase 1 is not closing yet.
- I recorded no phase base commit, because this workspace has no git history.
- The G01 hands-on/review split (5 h and 1 h) is assumed; only the 6 h total was reported.

Next prompt:

```text
/adk-engineer Carry out docs/tickets/support/G06.md.
```