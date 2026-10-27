I fixed the correction code and its tests, but I couldn't run the test suite. This session has no shell tool, so nothing has been executed. Please run `python -m unittest discover -s tests -t .` before relying on this.

**The problem in the old code**
- `correct_warnings` overwrote `runs/PA-2026-0165-r1/writer.json`. `AGENTS.md` forbids editing anything under `runs/`.
- `repair_review` also overwrote the saved review. It deleted the findings it matched and could flip the verdict to `accept`. For this case that would have discarded the quotation finding without trace, and it would have wiped the other findings if they ever matched its filter. The saved review rejected the draft for a decisive, unresolved conflict (3.9 m against 4.3 m), and the correction doesn't touch that.
- Nothing checked that the "corrected" draft stayed in scope. Two of the three recorded replies fail that check. One drops the `LP-H4@2024:p31:4` citation and the survey gap. The other changes the decision to `approve` and drops the conditions. Only the third is a clean fix.

**What I changed**
- **`pipeline/correction.py`:**
  - `correct_warnings(run_id, new_run_id, …)` now writes to a new run (`PA-2026-0165-r2` in the tests). It refuses to write to the original run and copies `source.json` across.
  - A new `scope_errors` check allows only the warned citations' quote text to change. A draft that alters the decision, reasons, conditions, conflicts or gaps, or that adds, drops or reorders citations, raises `StageFailed` and saves nothing.
  - The correction prompt now says to fix only the quotes.
  - `repair_review(run_id, new_run_id, store, spans)` copies the review into the new run with verdict `reject`, claims, findings, frame hash and images all unchanged. The fixed quotation finding is recorded in `meta.resolved_findings` instead of being deleted. `meta` also notes where the review came from and that `r2` needs its own review.
- **`tests/test_correction.py`:** it now covers six things:
  - the `r1` files are byte-identical after a correction;
  - only the `DAS@1:p1:1` quote changes;
  - the reply that drops a citation or gap is rejected;
  - the reply that changes the decision is rejected;
  - the carried review keeps its verdict `reject` and every finding;
  - the original review is untouched.

  Tests use the recorded replies and `ScriptedTransport` only.

**Assumptions** (nobody was available to ask)
- I treated the third recorded writer reply as the intended correction, since it is the only in-scope one.
- I assumed "don't change the decision" means the old `reject` stays on record. The old review judged `r1`, so the `r2` draft is not accepted and needs a fresh review before export. That review is a paid provider call, which needs the owner's approval, so I made none.

**Left undone**
- Running the tests (above).
- A manifest for the `r2` run. Nothing in the repo writes one for a correction.
- The `r2` run directory itself. The code and tests create it, but I didn't generate it in `runs/`.
- The fresh review of `r2`, and export.

No provider calls, network use or installs.