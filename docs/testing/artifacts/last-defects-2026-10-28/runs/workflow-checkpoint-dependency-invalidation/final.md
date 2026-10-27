The ADK route now carries on from saved stages and re-runs only the ones whose inputs have changed. I could not run any of it: this session has no shell tool, so the unit tests, including the three new ones, have not been run. Please run `python -m unittest discover -s tests -t .` before relying on it.

**What changed**
- **`pipeline/resume.py`:**
  - A saved stage is reused only if its manifest still matches the current source hash and document versions, prompt version, model, temperature and max tokens. A review also needs to match the exact draft revision it reviewed, and its claims must cover every reason in that draft.
  - Constraints are reused only if the address and `layers_version` match.
  - New records go to a new directory, `<run>-c1`, `-c2` and so on, with a manifest that names the parent, what was reused and why anything was rejected. Nothing under `runs/` is written.
  - A repeat resume finds the earlier continuation and sends nothing.
  - `diagnostics/` is never read.
- **`pipeline/adk_app.py`:** each stage agent now goes through the same logic. It keeps the same agents and state keys, and adds a `resume_run` key so the three stages share one continuation. `google.adk` is still imported only here.
- **`tests/test_resume.py`:** I added tests for the main cases below. I also added an optional `drafts_dir` keyword to `resume_case`; the existing signature otherwise stands.

**What this does for the three runs**
- **PA-2026-0147:** the design and access statement is now version 2, so the source hash differs. The writer and review are re-run and the constraints are reused.
- **PA-2026-0152:** the writer and constraints are reused. The saved review was for r1, so the officer's r2 amendment gets a fresh review (one send). Before, the old review was exported against the newer draft.
- **PA-2026-0141:** reused whole, with no sends.
- **Hand-edited writer response:** it cannot reach a checkpoint or an export.

**Behaviour you didn't ask for**
- If the writer has to re-run but an officer amendment exists, it stops with a `StageFailed` before any send rather than silently choosing between them.
- The amended draft is checked in code with `validate_draft` before it is reviewed.
- `publish` is kept but now refuses to export when the saved review is for a different draft.

**Assumptions** (nobody was available to answer these)
- **Model comparison:** I compare model, temperature and max tokens against `Settings`, not against the `ChatModel` passed in, because the existing test passes a model named "m".
- **Schema hashes:** I do not check the instruction or schema hashes in the old manifests, because I couldn't tell how they were computed. Bumping the prompt version is the project's convention for any change, so I rely on that.
- **Application text:** the address and proposal text are not recorded in old manifests, so a change to them alone would not be caught for those runs.

**Not done**
- No ledger reservation is added to `resume_case`; its interface has no ledger. Re-running 0147 and 0152 for real would send provider calls (writer and review for 0147, review for 0152). Those need the owner's approval for that run and a ledger entry first, and none were made.
- The ADK route is untested because `google-adk` is not installed here.

One thing to look at in 0152 r2: reason R2 says obscure glazing prevents overlooking, but the span it cites (`DAS@1:p1:3`) only says the floor level is raised. The reviewer may reject it.