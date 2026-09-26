# Offline review-service repair

The retained failure is a representational defect in the checker. The draft
refuses because access is unsafe. The resolved, nonmaterial roof issue has no
honest place in either the decision-claim list or unresolved-gap list. Both
`check()` and `serve()` originally return `issue coverage`. Worse, appending
`roof` to the access claim passes the old checker without assessing roof evidence.

The candidate evaluation skill's honest-contract checkpoint and workflow skill's
review-contract guidance led to a narrow ordinary-Python change, before any model
tuning. No bundled skill checker was used as evidence for the service.

## Changed boundary

`review.py` preserves `check(draft, issues, review)` and `serve(payload)`, including
the response's `accepted` and `errors` fields. Optional `issue_dispositions` rows
give resolved, nonmaterial issues an independent, supported, evidenced
`nondecisive` disposition. `reference.json` supplies that assessment for the roof
without changing the draft's refusal reason. `case.json` is unchanged and still
fails: the service does not invent the missing assessment.

Claim issue/source associations must match the trusted draft. Registered issue
sources must be covered. Unsupported judgments, missing evidence, unknown or
duplicate identities, and fabricated associations are rejected. Material issues
cannot be omitted, downgraded by review fields, passed as nondecisive, or released
while unresolved. This small service conservatively requires material issues to
be addressed by supported decision claims. It retains the existing ability to
report an unresolved nonmaterial gap. There is no independent required-controls
registry in the supplied service; this change enforces the supplied materiality
and source obligations rather than introducing a new controls subsystem.

`accepted` remains this service's combined validation/publication-gate result.
There is no separate structural-acceptance flag and no actual publication effect.

## Executed evidence

Interpreter: `/private/tmp/adk-system-designer-maintainer-venv/bin/python`,
Python **3.12.9**. No installs, SDK changes, credentials, network, or provider calls.

Command from this trial directory:

```sh
/private/tmp/adk-system-designer-maintainer-venv/bin/python -m unittest -v test_review
```

**PASS:** 18 tests, zero failures, errors, or skips; exit 0. Each test exercises
the actual checker and JSON `serve()` path, asserts their agreement, and repeats
the served invocation to check determinism. Input mutation is checked and socket
creation is denied during the executions. Import inspection found only stdlib
`json` in the service; the test harness does not claim OS-level network isolation.

Coverage includes truthful refusal and approval references, the independent roof
transformation, false associations, fabricated/duplicate/missing claims, wrong or
missing evidence, registered evidence omitted from the draft review, unsupported
and uncertain judgments, materiality laundering, and unresolved material gaps.

Retained evidence:

- `review_before.py`: unchanged original service.
- `baseline.json`: original failure and original source/case hashes.
- `reference.json`: honest passing response using the additive disposition.
- `test_review.py`: executable regression suite.
- `boundary-results.json`: complete inputs and actual before/after `check()` and
  `serve()` results, plus interpreter, revised source hash, and reference size.

The unchanged original fails before and after; the honest reference changes from
rejected to accepted; the false-association control changes from accepted to
rejected. The original failed observation is preserved, not rewritten as success.

## Limits and next experiment

This is deterministic evidence about this synthetic service. No real ADK Runner,
model generation, provider schema route, HTTP server, browser, deployment, or
publication was exercised. Those are **NOT RUN** or **N/A** here. No external
resources were created, so cleanup is **N/A**.

Evidence IDs establish provenance/coverage, not substantive entailment. A model
could still falsely label supplied evidence `supported`; no semantic judge is
implemented. The supplied draft and issue registry are assumed trusted. JSON
type/schema hardening, revision ownership, concurrent release, and real required
control policies were not part of this narrow repair.

Another model experiment would test the new hypothesis that the model can use an
expressible contract honestly: keep decision associations fixed, assess independent
issues, retain required evidence, and report uncertainty. It would not be needed
to rediscover whether the contract can represent this reference. First review a
fixed set of decisive/nondecisive, approval/refusal, evidence-deletion, and
contradiction cases; then, under separately authorized live scope, retain the exact
model/adapter/schema, prompts, cases, trial IDs, failed attempts, request/retry
bounds, and complete outputs. Measure structural acceptance, publication eligibility,
and independently judged support separately. A canary would establish only its
observed provider route; fixed repeated trials and reviewed fresh cases would
measure reliability. An actual application's Runner and release boundary would
need their own tests. No such calls or approval request were made in this trial.
