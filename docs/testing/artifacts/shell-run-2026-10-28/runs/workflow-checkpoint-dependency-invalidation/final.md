Resume now reuses a saved stage only when its inputs still match. Anything it rejects, and everything downstream of it, runs again. All 12 offline tests pass, run with `python -m unittest discover -s tests -t .`. No provider calls were made, `runs/` is unchanged, and the ledger is untouched.

**Not run:** `pipeline/adk_app.py` was only byte-compiled, since `google.adk` isn't installed here. I covered the same call sequence in a test that builds a separate `Continuation` per stage, as the ADK agents do. No real ADK session has run it.

**What each retained run needs:**
- **PA-2026-0141-r3:** every stage still matches, so resume makes zero sends.
- **PA-2026-0147-r1:** the design and access statement is now `DAS@2`, so the source, writer and review are rejected. The constraints stage is kept because the address and GIS layers are unchanged. A continuation needs 2 paid calls (writer, then review).
- **PA-2026-0152-r1:** the officer's `r2` draft replaces the model draft, so there is no writer call. The old review was of `r1`, so it is rejected and re-run. A continuation needs 1 paid call.
- **Hand-edited writer response:** it is never read. It can't enter a checkpoint or publication, and a test checks it never reaches the model.

**What changed:**
- `pipeline/resume.py` checks each saved stage against the current spans, instructions, schema and model settings. A review also has to match the exact draft it checked. Anything the manifest can't prove is treated as not reusable. Results go to a new run directory (`<case>-r<n>`) whose manifest records the parent, what was reused and why anything was rejected.
- Asking again finds the continuation's own checkpoints and sends nothing. Re-running a stage whose inputs haven't changed would cost a call and prove nothing.
- A review is committed only if the draft hasn't been amended while it ran.
- I fixed two bugs. `publish` used to export the newest amended draft with the old review. The `latest_draft` ordering also put `r10` before `r2`.
- `pipeline/adk_app.py` goes through the same logic. The only addition is an optional `continuation_run_id` in session state. `resume_case` and the other signatures are the same, apart from an optional `drafts_dir`.
- I added `PARSER` to `pipeline/sources.py`.
- The tests are in `tests/test_resume.py`.

**Questions I couldn't ask, and what I assumed:**
1. Is writing continuations as new `runs/<case>-r<n>` directories acceptable? I assumed yes, since `AGENTS.md` says to write a new run directory instead of editing one.
2. Should an officer's draft stand in for a model draft with no writer call? I assumed yes and only schema-check it.
3. Is `max_source_chars` unchanged since the old runs? The old manifests don't record it. I assumed the default of 60,000, and new manifests record it.

**Left undone:**
- The two paid continuations (0147 and 0152) are not run. They need the owner's approval for those runs; the ledger has no entries yet.
- `resume_case` doesn't reserve against the ledger, as before. I'd add that once the approval process is settled.
- `workflow.py` still writes a thin manifest without the identity hashes. Its runs will always be treated as not reusable, which is safe but wasteful.
- The old manifests' `code_version` isn't compared, because there's no current value to compare it to.
- I didn't run the skill's draft-consistency check on the officer's draft.