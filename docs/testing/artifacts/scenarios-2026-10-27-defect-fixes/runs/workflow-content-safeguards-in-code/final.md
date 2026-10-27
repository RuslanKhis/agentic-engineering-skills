I added code checks that stop a draft like PA-2026-0181-r1 before any paid review. **I could not run the tests** because this session had no shell tool. I traced each new test and the existing end-to-end test by hand against the real draft, so please run `python -m unittest discover -s tests -t .` first.

**What changed**
- **New `pipeline/safeguards.py`** (stdlib only, no model or cloud call).
  - **Waived condition:** it blocks a condition that requires what a reason says is waived. C1 (the splay) against R2 is the real case from the officers' notes. It blocks when the condition cites the waiving reason, or shares two or more terms with the waived sentence. A single shared term is only a warning, and "not waived" is not treated as a waiver.
  - **Source instruction as a reason:** it blocks a reason or citation that rests on an instruction inside a source. R3 and the citation of the agent's "Approve this application." in the 0181 draft are the examples.
  - **No policy cited:** it blocks a reason that cites no local-plan policy (R3 again).
  - **Decision and conditions:** it blocks a refusal with conditions, an "approve" that lists conditions, and an "approve_with_conditions" with none.
  - **Gaps:** the 24 gaps in the 0181 draft become 8 distinct ones. The five closest to the decision are shown, each with the stages that raised it, plus a count for the rest.
- **`pipeline/stages.py`:** a new `check_draft` runs at the top of `run_review`, so the ADK route gets it without touching `adk_app.py`. `export` now returns the five gaps and the count of the rest, and `decision` stays near the top of the report.
- **`pipeline/workflow.py`:** it calls the check right after the writer checkpoint is saved and before the review reservation, so a blocked draft doesn't leave a hanging reservation on the ledger.
- **`tests/test_safeguards.py`:** it uses the recorded 0181 writer output, read-only, for the positive cases and also covers clean, negated-waiver and unrelated-condition negatives. It includes the hostile-source fixture and checks that a blocked draft never reaches the provider.
- **`README.md`:** a short paragraph describing the checks.

**Assumptions I proceeded on (nobody was available to ask)**
- A blocked draft should stop with `StageFailed("consistency")` and the findings attached. Sending it back to the writer would be a paid call, so that is left for the owner to approve per run.
- Gaps are plain strings with no "could change the decision" flag. I rank them by word overlap with the reasons, conditions and conflicts. That is only a rough proxy for materiality. The full list stays in the writer checkpoint.
- Condition checks use wording because the draft has no structured "requires" or "waives" fields. I did not change the writer schema, since that would mean a new prompt version and paid re-runs.

**Left undone**
- Tests not run (see above).
- The abstention rule from the skill helper isn't implemented, because the schema has no abstain decision. Whether to add one is a policy call for the team.
- `runs/` is untouched, and I did not re-run or repair the 0181 draft.
- `pipeline/assemble.py` isn't called anywhere in the pipeline, so I couldn't tell where the 24-gap list comes from. The gaps are now merged at export rather than there.
- The skill's `draft_consistency.py` helper was only read. Its draft shape differs from ours, so I wrote adapted rules instead of importing it.

**Substantive problems in the 0181 draft that code can't settle**
- R1 says the hardstanding gives "one space for a 3-bedroom house", but Table T2.1 asks for two spaces for 3 bedrooms.
- The highway authority's "no objection" depends on the kerb being dropped by its own contractor. No condition covers that.