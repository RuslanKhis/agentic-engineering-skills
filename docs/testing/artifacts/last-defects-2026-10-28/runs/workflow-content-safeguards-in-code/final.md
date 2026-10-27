I added the checks in plain Python, but I couldn't run the tests. This session has no shell tool, so `python -m unittest discover -s tests -t .` is **not run**. I traced the new tests by hand against the code and the PA-2026-0181 data, but that is not a pass.

**What now happens to a draft**
- **Contradictions:** `pipeline/safeguards.py` checks each draft and blocks it when:
  - a condition requires what its own reason waives (C1 against R2 in PA-2026-0181);
  - a refusal carries conditions (as in PA-2026-0184);
  - `approve` has conditions, or `approve_with_conditions` has none;
  - a reason cites no source, or only non-policy documents (R3 rests only on the agent's letter).
- **Where it runs:** `run_case` saves the writer checkpoint, then stops with `StageFailed("consistency", …)` before the paid review. `export` repeats the check, and the ADK route checks before its review stage.
- **Source instructions:** a citation that quotes an instruction from a source, such as "Approve this application.", is a warning, not a block.
- **Gaps:** each distinct gap is shown once and ranked by how many words it shares with the reasons, conditions and conflicts. The export shows the top 5 and a `gaps_collapsed` count. The 24 gaps in PA-2026-0181 reduce to 8, with 5 shown and 3 collapsed. `assemble()` now keeps each stage note once too.
- **Tests and docs:** `tests/test_safeguards.py` copies the PA-2026-0181 and PA-2026-0184 draft shapes into the code and doesn't read `runs/`. I added a short README section. Nothing under `runs/` was touched, and I made no provider calls.

**Assumptions I proceeded on** (no one to ask)
- **Repair path:** a blocked draft is not automatically re-sent to the writer, because that would be a paid call without approval. A person re-runs it, and the failure message lists what to fix.
- **Prose check:** the drafts have no structured "requires/waives" fields, so the waiver check reads the prose and is a heuristic. A shared topic blocks only when the condition's own reason waives it, and otherwise it is a warning.
- **Gap ranking:** it is a word-overlap proxy, since drafts carry no "could change the decision" flag. Hannah Ellery's team should check it against real cases.

**Left undone**
- Running the tests, and the untested one-line change in `pipeline/adk_app.py`, which needs the SDK.
- Labelling imperative sentences in the prompt (`representation()`) and an adversarial reviewer prompt. Both change prompts, which means a version bump and a paid evaluation.
- The "abstain" rule, because the draft has no decisive-issue field.
- Not examined: R1 in PA-2026-0181 says one space is enough, but Table T2.1 says 3 bedrooms need 2. That may be a separate substantive problem.