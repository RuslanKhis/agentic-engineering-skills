# Progressive validation for staged paid applications

Read when a live case fails partway through a route, a saved stage needs recovery,
or repeated complete cases and full suites are consuming the diagnostic budget.
This procedure schedules the required evidence; it supplies neither a checkpoint
implementation nor authority for additional paid work.

## Define the evidence and next boundary

Before testing, record required cases, acceptance criteria, dependency order,
failure/stop rules and the approved call, spending and time envelope. Separate
diagnostic continuations from a fixed quality cohort; preserve that cohort's
declared cases and attempt rules. A reference label is an outcome to compare,
not an implicit requirement for perfect agreement. Retry policy belongs in the
plan before observations, rather than rerunning until the desired outcome appears.

## Advance from the retained failure

1. Inspect the immutable failed attempt: exact request/response, selected output,
   source/config/code identities, state transitions, storage result and charges.
   Reproduce offline where possible through the earliest failing boundary. Inspect
   later known blockers too; the first exception may conceal another failure.
   Classify retrieval, observation, reconciliation, drafting, review and evaluator
   separately. A reviewer cannot repair operative policy absent from its inputs.
   Use [contract qualification](contract-qualification.md) for prompt/schema/validator
   disagreement or an unrepresentable document shape before another paid attempt.
2. Fix that boundary. If changing schemas shared across stages, authorization,
   accounting, cancellation, persistence or publication, run the affected wider
   invariants before further paid execution. Dependency impact, rather than patch
   size, determines this scope.
3. Run focused regressions and the relevant real Runner, serialized transport or
   configured storage checks with controlled external responses. Include realistic
   payloads through Runner → serialization → checkpoint write → reopen → producer
   reuse before spending. Native schema acceptance alone does not prove storage fit.
   Assert byte limits at the actual envelope, including metadata, warnings and
   images/references. Use lossless compaction or integrity-checked references to
   complete private inputs where supported; truncating evidence to fit is a failure.
4. Qualify unaffected upstream checkpoints against their complete dependency
   identities and current trusted owner. For reviews include the exact draft,
   frame, invocation and images. Check authoritative response and native projection,
   not just a populated session key. Invalidate changed stages and their descendants;
   keep failed originals immutable and link a separate continuation. When installed,
   workflow-design supplies the detailed checkpoint contract; these qualification
   requirements apply even without that optional skill. If reuse cannot be proven,
   use a fresh case only within its authorized scope.
5. Reconcile any existing operation before dispatch. Duplicate guards cover failed,
   interrupted and no-response attempts as well as successes. Within the existing
   envelope, retry only the affected stage and continue downstream while its gates
   hold; unaffected upstream stages should incur zero model sends. Record new
   attempts durably, retaining consumed calls and unknown charges. Expanded paid
   scope needs new approval; local-fix permission creates no retry allowance.
6. Once the route works, run the required **fresh end-to-end API cases through the
   normal application**, with the declared initial state and without diagnostic
   checkpoint injection. Keep latency and outcome agreement separate. Recovery of
   a saved review is not a fresh complete-case result.
7. After those API cases stabilize under the declared criteria, freeze the tested
   snapshot and run full regression and release/submission checks. A subsequent
   change invalidates its affected evidence; rerun checks justified by that impact.
   Preserve missing and failed observations instead of rewriting their verdicts.

For recurring structural failures before another broad cohort, also prepare the
[experiment re-entry record](experiment-reentry.md). Diagnostic counterfactuals
remain labelled analysis: an edited replay or hand-authored passing response must
never replace an authoritative provider response.

## Diagnose review and correction semantics

Inspect the precise proposition, supporting and contrary evidence, policy
qualification and review judgment before changing a checker or retrying a model.
Source coverage can be complete while a material attributed uncertainty remains
unresolved. A missing keyword in application prose does not remove policy
relevance established by other source facts. Preserve decisive citations and
uncertainty; clearing them to obtain acceptance changes the task.

For a warning-only writer repair, assert unchanged decision, reasons, conditions,
citations, conflicts and existing gaps except the specifically authorized warning
correction. For review repair bind the unchanged draft/frame and retain unresolved
findings. Correction instructions must allow another rejection. Use
[source-support calibration](source-support-calibration.md) for judge mistakes
and [evaluation design](evaluation-design.md) for honest references.

## Keep execution ownership and timing interpretable

When verification is delegated, assign one owner to runtime edits and paid
dispatch, with independent offline review using isolated state. Record the exact
tested source/configuration manifest and hashes, including relevant uncommitted,
new and ignored runtime/checkpoint helpers. A clean worktree at HEAD can omit
the implementation; added files can alter runtime discovery without modifying
old files. Integrate relevant blocking findings before the affected call;
unrelated audits need not stop qualified progress. Reverify affected checks when
reviewed and executing snapshots differ.

Record human pauses, laptop closure and connection loss as interruptions with
failures and charges retained. They do not alone establish a performance defect.
Reconnect to existing work through the authorized status/recovery path where
possible. Measure clean end-to-end latency separately from interrupted recovery;
keep confounded timing inconclusive.

## Report separate gates

Use PASS/FAIL/BLOCKED/NOT RUN/INCONCLUSIVE with attempt and snapshot identities.

| Gate | Evidence required for the stated pass |
| --- | --- |
| Transport/schema/native validity | Exact route/request and actual validators accept the response |
| Source support and coverage | Evidence identities, coverage and substantive support checked separately; unresolved findings retained |
| Saved-stage recovery | Qualified checkpoint reopens and downstream continuation succeeds |
| Fresh end-to-end completion and latency | Required fresh cases complete through the normal API; separately identified clean timings meet declared limits |
| Outcome agreement | Observed outcomes compared to the versioned expectations using predeclared criteria |
| Fixture/UI/export functionality | Actual fixture, browser or export boundary exercised, with real/double dependencies named |
| Full regression and submission readiness | Required checks pass for the frozen tested snapshot |

No row substitutes for another. Valid prediction JSON does not establish correct
predictions, fixture journeys do not establish model quality, and a saved-stage
pass does not establish full-route acceptance. These are target-project acceptance
requirements, not claims of tests supplied or executed by this skill.
