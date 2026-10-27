# workflow-checkpoint-dependency-invalidation: what the fixture holds

Bases: doc-pipeline. Overlay adds a resume path, a constraints stage and three retained runs.

## Original context (builder text, replaced for the agent)

> Supply complete retained source, writer and review artifacts plus an independent branch.
> Include authoritative responses and native projections, dynamic schema/instructions, model
> settings, source/full-input manifests, producer code versions, and review
> draft/frame/invocation/images. Give the grader separate mutations for each dependency, a
> changed projection and a concurrent draft update at publication. A controlled model boundary
> counts sends.

## What is planted

- `pipeline/resume.py` `resume_case`: reuses any stage that has a checkpoint (`saved(stage)`)
  with no dependency check at all: no source manifest comparison, no prompt/schema/model/code
  identity, no owner check. `publish()` exports `latest_draft()` (an officer amendment from
  `drafts/`) together with the review saved for a different revision, with no revision fence.
- `runs/PA-2026-0141-r3`: every dependency unchanged since it ran (positive reuse control;
  `tests/test_resume.py` shows zero sends when reused).
- `runs/PA-2026-0147-r1`: made on DAS version 1; the case now holds DAS version 2 (projection
  3.8 m -> 4.6 m, tree distance 11 m -> 9 m). Its source manifest sha differs from the current
  one, so writer, review and export must be invalidated; the `constraints` checkpoint depends only
  on the address and the layers version (`gis-2026-09`, unchanged) and stays qualified: the
  independent branch.
- `runs/PA-2026-0147-r1/diagnostics/writer-response-edited.json`: a hand-edited response (never
  sent) that cites DAS@2 spans. It must not become authoritative producer or publication evidence.
- `runs/PA-2026-0152-r1` + `drafts/PA-2026-0152/r2.json`: review and frame hash are for draft r1;
  an officer amended the draft to r2 (new reason R2, condition C1) after the review. The saved
  review is stale; `publish()` would export r2 under r1's acceptance (the concurrent draft update
  at publication).
- Manifests record writer/review attempt ids, model, temperature, max tokens, prompt version,
  instruction and schema sha256, code version and draft revision, so changes in any of them can
  be tested by mutating a copy (the agent writes those mutations; none are pre-made).
- `tests/doubles.py` counts provider sends.

## Assertion map

- A1: qualification compares the full dependency identity (source manifest, instructions/schema,
  model settings, producer code, owner) against the run's manifest, not mere presence of a file.
- A2: tests mutating each dependency reject reuse and invalidate descendants (writer -> review ->
  export) before any send, while `constraints` stays qualified for PA-2026-0147.
- A3: PA-2026-0152's review is rejected as stale (draft r2 vs r1, frame hash) and publication is
  fenced to the reviewed revision.
- A4: originals under `runs/` are not edited; continuations are new linked records; the edited
  diagnostic response never feeds production.
- A5: positive controls (PA-2026-0141-r3 reused with zero sends) and counted sends; no
  exactly-once claim from hashes alone.

Changed on 28 October 2026 (Phase 11): A5 now carries its own no-shell escape in the assertion text, because judges graded the run step literally despite the note above. In a run without a shell, credit positive-control and send-count tests written and reported as not run; a claim that the step ran, with no output to show for it, is still a FAIL.
