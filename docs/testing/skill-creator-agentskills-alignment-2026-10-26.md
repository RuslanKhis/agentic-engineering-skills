# skill-creator and Agent Skills reference alignment — 26 October 2026

Source note: [comparison](../research/skill-creator-agentskills-comparison-2026-10-26.md).

## Changed journey

The maintainer's: changing a skill's description, through `CONTRIBUTING.md`
and `docs/testing/skill-quality.md`. No skill's own journey changed.

## Fresh-agent trial

A fresh agent acting as a maintainer worked on a copy of the repository
(made with `rsync`, excluding `.git`, `.venv` and `docs/research`), never the
original, on a report that `adk-agent-security` activates for plain FastAPI
auth unit tests. With no model credentials, it changed the description
(1,016 characters before and after, all five exclusions kept, a new one
added), added a training near-miss, a held-out near-miss and a positive to
`evals/activation.json`, added a contextual scenario, saved the old file and
its hash, and wrote a record. `validate_skills.py` exited 0; the
repository check failed only because the copy lacked
`docs/research/source-register.json`, which the trial's own exclusion
removed. It recorded the reproduction, the repeated-run trigger-rate
comparison and blind grading as not run, and called the description an
unmeasured candidate rather than an improvement.

Ease: 3 of 5.

## Frictions and fixes (same day)

1. `python3 -m venv` picked up an older system Python. Fixed: the guide
   names `python3.12`.
2. Excluding `docs/research` broke the repository check, and the runner
   stops at the first failing stage. Not changed: the exclusion was the
   trial's own; the register is part of the repository.
3. "Contextual" cases were undefined. Fixed.
4. No way to mark held-out cases. Fixed: a `split` field, validated by
   `check_repo.py` (tested).
5. `"source": "issue #N"` covered only issues. Fixed.
6. No offline path when reproduction needs model sessions. Fixed: add the
   case, change as an unmeasured candidate, record not run.
7. No advice on what to cut near the length limit. Fixed: never an
   exclusion.
8. `git diff --check` needs a git checkout. Not changed: the trial's copy
   had none.
9. Whether a not-run record belongs in `docs/testing/`. Fixed: it does.
10. and 11. Whether to update `short_description`, the CHANGELOG and the
    README entry. Fixed for the description's consistency with the README
    entry and `short_description`; the CHANGELOG is written at release.

## Limits

No activation run: the trigger-rate method is documented, not exercised.
