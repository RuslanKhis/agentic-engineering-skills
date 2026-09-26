# Feedback-driven ADK skill validation

The 27 September 2026 update turns document-review failure modes into concrete
offline examples and focused loading triggers in four existing skills. All new
fixtures are synthetic. The private feedback document, application data and raw
application traces are not included. Dependency pins, invocation settings and
SDK `last-tested` metadata remain unchanged.

## Changes and evidence

| Concern | Delivered resource | Evidence and limit |
| --- | --- | --- |
| Review outcomes cannot be honestly represented | [Review-contract example](../../skills/adk-workflow-design/references/review-contracts.md) and prominent evaluation prerequisite | 14 helper regressions plus a separate fresh-agent repair trial; no real ADK Runner test |
| Model reconstructs established identities | Optional server-owned frame, per-source judgment slots, separate issue dispositions and stale-frame rejection | Honest refusal/approval, required controls, contradictions, warnings and byte limits; model labels remain judgments |
| Valid citations hide unsupported claims | [17-case grounding contrasts](../../skills/adk-agent-evaluation/references/source-support-calibration.md) and scorer | 6 scorer tests, negative controls and one independent AI judgment trial; expectations remain provisional |
| Main-policy retrieval misses supplements/visuals | [Local-document coverage pack](../../skills/adk-memory-architecture/references/local-document-coverage.md) | 13 new coverage regressions; synthetic extracted pages only, no PDF/image bytes or extraction benchmark |
| Generic JSON tests miss the real provider schema | [Compatibility matrix](../../skills/adk-agent-evaluation/references/provider-compatibility.md) and exact-request evidence matcher | 5 controlled-transport tests; remote compatibility remains unverified |
| Recurring paid runs reveal one blocker at a time | [Experiment re-entry/accounting record](../../skills/adk-agent-evaluation/references/experiment-reentry.md), live checklist and guardrail guidance | Offline procedure and authored scenario; no new paid allowance or application provider calls |

The main skill files gained short conditional pointers rather than the full
examples. Four new cases in [scenarios.json](../../evals/scenarios.json) retain
expected behavior for later trials; authored cases alone are not measured passes.

## Offline checks

The final repository run used existing CPython 3.12.9 on macOS, PyYAML 6.0.3,
markdown-it-py 4.0.0 and pytest 9.1.1. No dependencies were installed.

- All 13 skill packages validated with zero errors or warnings.
- Repository/helper checks: **433 passed, 59 optional SDK tests skipped**.
- This change adds **38 helper regression cases**: 14 workflow, 13 retrieval,
  6 grounding and 5 provider-evidence controls.
- The official skill validator passed for all four modified skill packages;
  `git diff --check` passed.

The [retained check output](artifacts/review-contract/repo-checks.txt) records the
individual suites. The default runner now includes the workflow's new synthetic
contract tests without adding its SDK-dependent runtime suite.

An independent audit found two defects in the new retrieval scorer: an unknown
required section passed vacuously, and an agent-origin label without recorded
queries implied execution. Both were reproduced with failing regressions, fixed,
and included in the final passing run. This does not authenticate external traces;
the scorer still expects trusted adapter observations.

## Fresh-agent execution trials

Both trials used fresh subagents without conversation history. Inputs, candidate
hashes, limitations and unavailable model/usage metadata are recorded in the
[trial manifest](artifacts/review-contract/trial-manifest.json). No old-skill or
no-skill comparison was run, so these observations do not establish comparative
skill quality. Full agent transcripts are not retained; raw inputs, outputs and
independent checks are available.

### Review service

The agent received the [unchanged task](artifacts/review-contract/prompt.txt), a
[small broken service](artifacts/review-contract/seed/review.py), its
[retained case](artifacts/review-contract/seed/case.json) and copies of the two
candidate skills. It did not receive the grader's expectations.

It reproduced the coverage failure, identified the missing independent issue
disposition, and repaired the service before proposing more model work. The
[generated service](artifacts/review-contract/generated/review.py) accepts an
honest refusal plus a separately acceptable issue and rejects the invented claim
association. It retains source and material-issue obligations. Its own 18 tests
passed; the maintainer's separate [5 acceptance checks](artifacts/review-contract/acceptance.py)
also passed through both `check()` and the JSON `serve()` boundary.

The seed, original failure, generated reference, tests and boundary outcomes are
retained. This service has no ADK dependency, persistence, authentication or real
model. The narrow repair is trial output, not a recommended production schema;
the packaged frame example covers additional outcome/control/stale-response cases.

### Source support

The agent received only the skill/rubric, raw synthetic cases and diagram, with
expected labels and scorer withheld. Its [judgments](artifacts/review-contract/grounding/judgments.json)
agreed on supported versus rejected outcomes for all 17 cases: six supported,
eleven rejected, with zero false accepts/rejects relative to the provisional labels.
Full five-dimensional agreement was **15/17**, and the
[scorer exited 1](artifacts/review-contract/grounding/score.json) for those disagreements.

The differences concern the unscaled-pixel case (`s11`: unsupported versus a
contradicted inference) and secondary dimensions for a quote attributed to the
wrong source (`s17`). Both remain rejection controls. Original judgments and
expectations were retained rather than relabelled to manufacture agreement.
Guidance to adjudicate these rubric conventions was added after the trial; that
addition was not rerun. The [rubric used at trial](artifacts/review-contract/grounding/rubric-at-trial.md)
is preserved. No domain-competent human review or target-provider judge calibration
is claimed.

The intentionally weak controls expose 10 false accepts from ID-only acceptance;
literal substring matching produces one false accept and four false rejects;
always-reject produces six false rejects. Replaying expected labels is only a
scorer self-check.

## Reproduce the local checks

Use a project interpreter with the existing maintainer requirements:

```bash
python scripts/check_repo.py
python docs/testing/artifacts/review-contract/acceptance.py \
  docs/testing/artifacts/review-contract/generated -v
python -m unittest discover \
  -s docs/testing/artifacts/review-contract/generated -p test_review.py -v
python skills/adk-agent-evaluation/scripts/check_source_support.py --demo
python skills/adk-agent-evaluation/scripts/check_source_support.py --judgments \
  docs/testing/artifacts/review-contract/grounding/judgments.json
```

The final command intentionally exits 1 for the retained disagreements. None of
these commands establishes real PDF extraction, provider compatibility, production
publication safety or substantive recommendation quality.
