I changed the correction code so it writes to a new run directory instead of overwriting `runs/`, but I couldn't run the tests. I only have file tools in this session, with no shell. Please run `python -m unittest discover -s tests -t .`.

**What was wrong**
- The old `correct_warnings` and `repair_review` saved over `runs/PA-2026-0165-r1/`. That broke the rule that a run's files are evidence.
- `repair_review` could also switch a verdict to `accept`. It would drop the quote finding and keep the "reject" reason: the 3.9 m against 4.3 m conflict that the reviewer called decisive.

**What I changed**
- **`pipeline/correction.py`:** Both functions now take a new run id (for example `PA-2026-0165-r2`) and refuse to write to the original run.
- **Draft check:** The corrected draft is rejected unless only citation quotes changed. It must keep the same decision, reasons, conditions, conflicts, gaps and cited spans.
- **Review repair:** The review is copied into the new run and only the finding about the quote not being verbatim is dropped. The verdict (still `reject`), the claims and the other two findings stay as they were. The new review's metadata says it is derived from r1, that the reviewer was not re-run, and which finding was dropped.
- **`tests/test_correction.py`:** I rewrote the tests to cover these cases:
  - Replies 0 and 1 in `replies.json` are refused. Reply 0 drops a citation and a gap, and reply 1 changes the decision to `approve` and drops the conditions. Reply 2 is the only one that fixes just the quote.
  - The original run's files are unchanged after a correction.

**Not done**
- **No r2 run on disk:** Creating it means running the correction against the real writer. That is a paid call and needs the owner's approval, so I made none.
- **Reviewer not re-run:** The carried-over review is about the r1 draft. Re-running the reviewer on the corrected draft is a paid call and also needs approval.
- **Export:** The review still says `reject`, so the case can't be exported. Resolving the 3.9 m against 4.3 m conflict needs a survey or an officer's decision.
- **Callers:** I didn't search for other callers of the two functions. Their signatures changed, so any caller needs the new run id argument.

**Assumptions (nobody to ask)**
- A "small correction" means the quote fix only. A correction that also changed the decision should fail rather than be saved.
- You want the existing review kept, not replaced by the recorded sandbox review reply, which differs from the saved one (it drops one cited span from R1).