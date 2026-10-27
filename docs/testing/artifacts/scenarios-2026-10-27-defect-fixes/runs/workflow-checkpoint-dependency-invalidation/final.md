The ADK route now carries on from saved stages and re-runs only the ones whose inputs have changed. I couldn't run anything, because this session has no shell, so none of it has been run, including the existing test suite. Please run `python -m unittest discover -s tests -t .` before relying on it.

**What changed**
- **`pipeline/resume.py`:** A saved stage is reused only if it still matches the case:
  - **source:** the saved source manifest must match the current documents and policies.
  - **constraints:** the saved result must equal a fresh lookup for the address, since this stage doesn't depend on the documents or the writer.
  - **writer:** needs a qualified source, the same prompt version and model as the run's manifest, and a draft that still validates against the current source spans.
  - **review:** must be of the current draft, meaning the officer's latest amendment if there is one, otherwise the writer's. It also needs the same prompt version and model as the run's manifest, and it must cover every reason in the draft.
- **Stale stages:** A stale stage and everything after it is re-run.
- **Retained runs:** `runs/` is never edited. Any write goes to a new `<run>-cN` directory holding copies of the stages that still qualify, plus a manifest listing what was kept and what was invalidated. Calling resume again carries on in that directory, so nothing is paid for twice.
- **`pipeline/adk_app.py`:** `StageAgent` calls the same resume helpers, so the served route behaves like `resume_case`. It still doesn't add any `google.adk` imports elsewhere.
- **Interfaces:** `resume_case`, `publish`, `latest_draft` and `CheckpointStore` keep their signatures.
- **`publish`:** It now refuses to export a review that was made of an older draft.
- **Draft ordering bug:** `latest_draft` sorted revisions as text, so `r10` came before `r2`. It now sorts them as numbers.
- **Provider spend:** Paid calls in resume are reserved and settled on the ledger, as `workflow.py` does.

**What this does to your three runs**

| Run | Reused | Re-run |
| --- | --- | --- |
| PA-2026-0141-r3 | everything | nothing |
| PA-2026-0147-r1 (statement resubmitted as DAS@2) | constraints | source, writer, review |
| PA-2026-0152-r1 (officer's draft r2) | source, constraints, writer | review only, against r2 |

The hand-edited writer response under `diagnostics/` is never read.

**Tests:** I added tests to `tests/test_resume.py` for each case above, covering these checks:
- Retained run files are byte-identical afterwards.
- A repeat resume sends nothing.
- A review of the old draft isn't published.

**Left undone / assumptions** (nobody was available to answer, so I proceeded on these)
- **Unrun:** The tests are unrun, and the 0141 "reuse everything" result depends on its saved source hash matching what the code computes now. If it doesn't, the existing resume test will fail on an unexpected send.
- **Hashes not compared:** I did not compare the manifests' `instructions_sha256` or `schema_sha256`, because I couldn't compute them here to see how they were produced. I compare prompt version labels and model names instead, so an edit to a prompt without a version bump would go unnoticed.
- **Where the resume writes:** I assumed that adding files to an existing run directory counts as editing evidence. That means even finishing an unexported run writes a new `-c1` directory.
- **Old review records:** Review records saved before this change have no draft hash, so they are checked by revision label only.
- **Paid approval:** I made no provider calls. Re-running stale stages on 0147 and 0152 will spend from the ledger (0.40 and 0.25 reserved per writer and review call) once the route is run. I assumed the campaign allowance covers that, so the owner should confirm it per run.
- **Not touched:** `runs/README.md` doesn't list the new continuation runs.