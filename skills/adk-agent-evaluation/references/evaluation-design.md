# Dataset, judge and release design

Read this when curating a dataset, calibrating a judge, enforcing work limits, testing ambiguous writes or designing a release gate. Implement only the branches required by the target application.

**Production extensions:** these procedures develop the chapter's design guidance. The verified companion did not ship a holdout programme, rubric-calibration service, shared model/tool budget, remote-write reconciliation protocol, deployed staging suite or production monitoring system. Its historical passes do not validate an adaptation. Preserve existing interfaces and dependency pins; verify version-specific APIs before implementation. A design can finish with reviewable cases and acceptance criteria; distinguish that deliverable from implemented or executed checks.

## Curate cases with a reason to exist

1. Translate each consequential requirement into a case with an observable outcome, permitted actions and forbidden actions. Cover both action and non-action: a retrieval tool needs questions requiring retrieval and requests needing no lookup. Pair refusals with allowed successes so an agent that refuses everything cannot satisfy the suite. Keep ownership and eligibility failures independent; a foreign object that is also ineligible obscures which guard worked.
2. Choose the evidence source deliberately. Business rules supply critical cases before traffic exists. Accept a successful trace only after reviewing calls, arguments, tool results and final claims. Convert an incident by replacing sensitive values while preserving the failing state and sequence; demonstrate the old version fails when available. Review synthetic cases for impossible setup, unsupported tools, invented expected answers, duplicates and unrealistic distributions. Retain the generator prompt and configuration.
3. Establish solvability. For each important task, retain an accepted reference trace or implementation that satisfies its graders. If it fails, inspect fixture, requirement, reference and evaluator before tuning the candidate. Preserve dynamic identifiers when their relationship to actual results is the assertion; replacing every identifier with a constant can remove the defect.
4. Keep ownership metadata beside the ADK assets when the schema has no appropriate field: stable case ID, requirement, risk, source, slice, expected invariant, reviewer and review date. Validate the ADK asset schema separately from this semantic review.
5. Separate development, holdout and, where useful, reviewed recent-traffic cases. When a holdout failure directly guides a fix, move that evidence into development and replenish the holdout. Retain stable incident regressions while updating cases for changed policies and tools. Version reference answers and criteria; identify measurement changes in comparisons.

**Completion:** cases have reviewed expectations and owners, important tasks have a passing reference, and the split records which cases influenced the candidate. Repetition addresses variation within a case; it does not replace coverage across cases.

## Calibrate the judge on fixed evidence

Use programmatic assertions for exact facts and business invariants. Add a judge when acceptable language or domain judgement needs it. Design a separate rubric for each outcome class: confirmation, refusal, missing information or unknown outcome. A pending-request requirement belongs only to a confirmed creation.

Build a small, human-labelled calibration set before grading candidates. Hold user input, tool calls, results and their identifiers fixed; vary only the final answer. Include an accurate answer, a false completion claim, an invented identifier or timing claim, an acceptable paraphrase and relevant borderline cases. For example, tool evidence showing `pending_review` should reject an answer claiming money was returned. Missing evidence must have an explicit grading outcome.

Use narrow properties grounded in visible evidence. Keep critical factual or authorisation rules separate from tone and style; a quality average cannot compensate for a forbidden disclosure. Confirm the installed evaluator actually receives the necessary tool evidence and supports the case type. Select the judge explicitly and record model, settings, rubric version and grading output; agent or simulator settings do not establish judge settings.

Measure false accepts and false rejects against the human labels. To diagnose inconsistent verdicts, repeat the judge on the unchanged trace. Rerunning the agent changes the evidence as well as the grader. Multiple judge samples can expose or reduce variance, but majority voting does not repair a vague rubric. Apply the external deadline from [live-evaluations.md](live-evaluations.md) to blocking grading.

**Completion:** retained labels and judge results show which examples are accepted, rejected or unresolved, including disagreement across repetitions. Fix false acceptance of a critical violation before enabling that judge as a gate. Treat judge exceptions, timeouts and missing scores as incomplete evaluation. Calibration code and schema checks alone are not a successful live calibration.

## Enforce work before dispatch

Define scope first: one invocation, conversation, trial or suite. For each participating role, record the work allowance, enforcement point and exhaustion outcome. Agent generations, tool calls, simulator invocations, judge samples, output tokens and elapsed time need separate controls. Include retries at the boundary that dispatches them; an agent callback may not observe SDK-internal attempts.

Reserve each model or tool call before dispatch so exhaustion prevents the next action. With concurrent work, the reservation must be atomic at the shared scope. Construct fresh counters for independent trials and share counters deliberately across subagents when they share an allowance. A simulator turn cap leaves work inside each turn unconstrained. An output-token cap does not bound cumulative input usage or currency.

Compose checks with existing callbacks. Preserve receipt rendering, state guards and configured failure injection when adding budget callbacks; replacing a callback can remove a tested safety boundary. Decide explicitly whether a callback-produced terminal response consumes a generation allowance or avoids provider dispatch, and test the chosen accounting rule.

Exercise zero remaining allowance, exact-limit success, the next prohibited dispatch, separate model/tool exhaustion, cancellation and trial reset using deterministic doubles. Assert dispatch counts and stored effects, not just an exception. Use the process deadline for blocking work and retain partial evidence. Local termination cannot recall an accepted provider request. Report any currency, token or retry limit that remains unenforced.

**Completion:** each claimed limit has an enforcement boundary and an exhaustion regression; the run plan states residual work possible after cancellation.

## Reconcile ambiguous mutations

Use this branch only for an application with external writes. Distinguish explicit rejection, confirmed commitment and an unknown result after submission. A missing response is not evidence that nothing happened.

Define the adapter's real reconciliation contract: a stable operation/idempotency identifier, durable idempotency scope, payload-conflict policy and an authorised status query or equivalent lookup. Preserve the same operation identity across permitted recovery. Do not invent a status endpoint when the service has none; document the unresolved state and safe stopping/escalation path.

Create a deterministic fault fixture that commits the effect and then loses the acknowledgement. Drive it through the actual tool/orchestration boundary. Assert one stored effect, an unknown initial observation, a reconciliation attempt before further mutation, and a final claim grounded in the reconciled status. Add explicit rejection and successful-acknowledgement controls so the test distinguishes all three outcomes. If reconciliation remains unknown, assert that the application stops further mutation and reports uncertainty. Separately test concurrent duplicate requests and conflicting payloads according to the service contract.

An observer or grader failure after submission uses the same evidence discipline: preserve the operation identity and inspect status instead of resubmitting to obtain a measurement. The companion's successful-then-rejected receipt regressions remain useful, but they do not establish this remote protocol.

**Completion:** the fault regression proves the recovery decision and effect count. Durable storage, real authentication and remote timeout semantics remain separate contract/staging checks.

## Build gates and close the feedback loop

Assign checks to the smallest useful stage: deterministic rules, schemas and scripted orchestration on ordinary changes; a bounded set of critical live cases on selected changes; broader simulations and judge comparisons periodically; holdout and isolated staging evidence before release. This is a scheduling design, not permission to provision or run services.

Specify staging assertions for capabilities the application actually has: cross-user identity denial, session reload/compaction, adapter schemas and retry contracts, allowed subagent routing and shared limits, and complete request processing. A healthy endpoint or local fake does not establish these properties. Use deployed-equivalent permissions on isolated targets under the authorised scope.

Pair baseline and candidate by case and fixture, holding criteria and trial counts steady. Report successful/attempted counts and critical slices separately; explain changed measurement definitions. For small differences, use uncertainty methods respecting repeated trials within cases. Use [result-auditing.md](result-auditing.md) for completeness and verdict checks. Preserve failed product trials; bounded infrastructure recovery must retain its failed or incomplete attempts.

Plan observation around allowlisted metadata: opaque trace linkage, versions, tool name, result category, timing, retries, policy decision, usage and final status. Distinguish submission from later business completion. Keep message-content capture disabled by default, including `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS=false` where applicable. Review minimisation, access, retention and export before production excerpts reach fixtures or judges; apply the same policy to CI artifacts and recordings.

**Completion:** each release gate identifies its evidence and failure owner. A production incident becomes a sanitised reproduction, an old-version failure when reproducible, a verified correction and monitored affected slice. Cases that taught the fix are development evidence; fresh reviewed evidence supplies the holdout.
