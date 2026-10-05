# Dataset, judge and release design

Read this when curating a dataset, calibrating a judge, enforcing work limits, testing ambiguous writes or designing a release gate. Implement only the branches required by the target application.

**Production extensions:** these procedures develop the chapter's design guidance. The verified companion shipped none of these: a holdout programme, rubric-calibration service, shared model/tool budget, remote-write reconciliation protocol, deployed staging suite or production monitoring system. Each is an addition to implement and test; the companion's historical passes cover the companion. Preserve existing interfaces and dependency pins; verify version-specific APIs before implementation. A design can finish with reviewable cases and acceptance criteria; distinguish that deliverable from implemented or executed checks.

## Curate cases with a reason to exist

1. Translate each consequential requirement into a case with an observable outcome, permitted actions and forbidden actions. Cover both action and non-action: a retrieval tool needs questions requiring retrieval and requests needing no lookup. Pair refusals with allowed successes so a refuse-everything agent fails the success cases. Keep ownership and eligibility failures independent; a foreign object that is also ineligible obscures which guard worked. For example, a refund suite pairs "refund a $20 eligible order" (success) with "refund an order the caller does not own" (denied) and "refund an ineligible order the caller owns" (declined), so each guard is tested alone.
2. Choose the evidence source deliberately. Business rules supply critical cases before traffic exists. Accept a successful trace only after reviewing calls, arguments, tool results and final claims. Convert an incident by replacing sensitive values while preserving the failing state and sequence; demonstrate the old version fails when available. Review synthetic cases for impossible setup, unsupported tools, invented expected answers, duplicates and unrealistic distributions. Retain the generator prompt and configuration.
3. Establish solvability with the [honest-contract checkpoint](#establish-an-honest-review-contract) below. Preserve dynamic identifiers when their relationship to actual results is the assertion; replacing every identifier with a constant can remove the defect.
4. Keep ownership metadata beside the ADK assets when the schema has no appropriate field. Validate the ADK asset schema on its own, apart from this semantic review:

   ```json
   {"case_id": "refund-012", "requirement": "REQ-7", "risk": "duplicate refund",
    "source": "incident 2026-02-14", "slice": "development",
    "expected_invariant": "one refund per operation ID",
    "reviewer": "payments lead", "reviewed": "2026-03-01"}
   ```

5. Separate development, holdout and, where useful, reviewed recent-traffic cases. When a holdout failure directly guides a fix, move that evidence into development and replenish the holdout. Retain stable incident regressions while updating cases for changed policies and tools. Version reference answers and criteria; identify measurement changes in comparisons.
6. Write acceptance criteria as categories that generalise (every reason cites an operative policy; no condition contradicts a reason; recall of gold operative sections at or above the agreed level), not as a checklist of the exact defects found in the development cases. A criterion naming "case 003's missing splay" is a regression test, not an acceptance criterion. Validate a change motivated by one case on the other development cases before accepting it ([progressive validation](progressive-validation.md#keep-the-deliverable-and-the-method-together)).

**Completion:** cases have reviewed expectations and owners, important tasks have a passing reference, and the split records which cases influenced the candidate. Repetition addresses variation within a case; coverage across cases comes from more cases.

## Establish an honest review contract

For mandatory labels, extraction-sensitive text or dense representations, also use
[contract qualification](contract-qualification.md) to trace effective prompt,
schema and validator agreement and establish representability before dispatch.

Before model tuning or a quality cohort, retain an honestly constructed reference for each consequential outcome combination and execute it through the actual schema, validators and relevant Runner/served boundary. For document review, cover approval with required controls, refusal with separate favourable or manageable issues, unresolved evidence and contradictions. Acceptance must preserve the domain obligations as well as structural validity.

Use this transformation as a diagnostic: a refusal justified by unsafe access can coexist with a separately acceptable roof. Add the roof issue without adding it to the refusal reason; the review contract must have an honest disposition for it. Attaching its ID to the access reason merely to satisfy coverage is a failing negative control. Also delete a required approval safeguard and verify rejection. If the only passing response invents a relationship, the contract needs a representation for that outcome before another model run can usefully test it.

Retain the failing input, truthful reference, misleading-association control and required-safeguard control with their boundary results. Inspect the fixture, requirement, reference and evaluator when the reference fails; distinguish a schema's missing representation from a model's copying or substantive error. If server-established IDs or associations are being reconstructed by the model, consider compiling those identities into a draft-bound review frame, leaving relevance and support judgments to the model. Validate the adapted contract and its output size; a design proposal becomes a quality improvement once implemented and measured. When available, the workflow-design skill provides a worked review-frame example; this checkpoint remains usable without that package.

**Completion:** truthful outcomes pass at the intended runtime boundary, misleading associations and missing obligations fail, and any unexecuted boundary is named. A handwritten JSON object passing an isolated mock checker establishes only that mock's behavior.

## Calibrate the judge on fixed evidence

Use programmatic assertions for exact facts and business invariants. Add a judge when acceptable language or domain judgement needs it. Design one rubric per outcome class: confirmation, refusal, missing information or unknown outcome. A pending-request requirement belongs only to a confirmed creation. For example, the confirmation rubric asks "does the answer state only the outcome the receipt shows?"; the refusal rubric asks "does the answer give the policy reason without inventing a workaround?".

Build a small, human-labelled calibration set before grading candidates. Hold user input, tool calls, results and their identifiers fixed; vary only the final answer. Include an accurate answer, a false completion claim, an invented identifier or timing claim, an acceptable paraphrase and relevant borderline cases. For example, tool evidence showing `pending_review` should reject an answer claiming money was returned. Give missing evidence an explicit grading outcome.

Use narrow properties grounded in visible evidence. Grade critical factual or authorisation rules apart from tone and style; a forbidden disclosure fails the case whatever the quality average. Confirm the installed evaluator actually receives the necessary tool evidence and supports the case type. Select the judge explicitly and record its model, settings, rubric version and grading output as their own record, beside the agent and simulator settings.

Measure false accepts and false rejects against the human labels. To diagnose inconsistent verdicts, repeat the judge on the unchanged trace. Rerunning the agent changes the evidence as well as the grader. Multiple judge samples expose variance; a vague rubric is repaired by rewriting it. Apply the external deadline from [live-evaluations.md](live-evaluations.md) to blocking grading.

For document evidence, load [source-support calibration](source-support-calibration.md). It includes question-only spans, omitted exceptions, unrelated citations and contradiction/absence controls. Grade source identity, span completeness, applicability, contrary evidence and support separately. Retain a model's support label as its judgment, to be checked against the evidence. Use domain-competent human review of substantive expectations when available; record AI-only expectations explicitly and limit the resulting claim.

**Completion:** retained labels and judge results show which examples are accepted, rejected or unresolved, including disagreement across repetitions. Fix false acceptance of a critical violation before enabling that judge as a gate. Treat judge exceptions, timeouts and missing scores as incomplete evaluation. Calibration code and schema checks prepare the calibration; the live run with retained verdicts completes it.

## Enforce work before dispatch

Define scope first: one invocation, conversation, trial or suite. For each participating role, record the work allowance, enforcement point and exhaustion outcome. Agent generations, tool calls, simulator invocations, judge samples, output tokens and elapsed time need separate controls. Include retries at the boundary that dispatches them; an agent callback may not observe SDK-internal attempts.

Reserve each model or tool call before dispatch so exhaustion prevents the next action. With concurrent work, the reservation must be atomic at the shared scope. Construct fresh counters for independent trials and share counters deliberately across subagents when they share an allowance. A simulator turn cap leaves work inside each turn unconstrained. Bound cumulative input usage and currency with their own controls; an output-token cap covers output.

Compose checks with existing callbacks. Preserve receipt rendering, state guards and configured failure injection when adding budget callbacks; replacing a callback can remove a tested safety boundary. Decide explicitly whether a callback-produced terminal response consumes a generation allowance or avoids provider dispatch, and test the chosen accounting rule.

Exercise zero remaining allowance, exact-limit success, the next prohibited dispatch, separate model/tool exhaustion, cancellation and trial reset using deterministic doubles. Assert dispatch counts and stored effects as well as the exception. Use the process deadline for blocking work and retain partial evidence. An accepted provider request completes on the provider's side whatever local termination does. Report any currency, token or retry limit that remains unenforced.

**Completion:** each claimed limit has an enforcement boundary and an exhaustion regression; the run plan states residual work possible after cancellation.

## Reconcile ambiguous mutations

Use this branch only for an application with external writes. Distinguish explicit rejection, confirmed commitment and an unknown result after submission. A missing response leaves the outcome unknown.

Define the adapter's real reconciliation contract: a stable operation/idempotency identifier, durable idempotency scope, payload-conflict policy and an authorised status query or equivalent lookup. Preserve the same operation identity across permitted recovery. When the service has no status endpoint, document the unresolved state and the safe stopping/escalation path.

Create a deterministic fault fixture that commits the effect and then loses the acknowledgement. Drive it through the actual tool/orchestration boundary. Assert one stored effect, an unknown initial observation, a reconciliation attempt before further mutation, and a final claim grounded in the reconciled status. Add explicit rejection and successful-acknowledgement controls so the test distinguishes all three outcomes. If reconciliation remains unknown, assert that the application stops further mutation and reports uncertainty. Separately test concurrent duplicate requests and conflicting payloads according to the service contract.

An observer or grader failure after submission uses the same evidence discipline: preserve the operation identity and inspect status instead of resubmitting to obtain a measurement. The companion's successful-then-rejected receipt regressions remain useful, and this remote protocol needs its own fixture.

**Completion:** the fault regression proves the recovery decision and effect count. Durable storage, real authentication and remote timeout semantics remain separate contract/staging checks.

## Build gates and close the feedback loop

Assign checks to the smallest useful stage: deterministic rules, schemas and scripted orchestration on ordinary changes; a bounded set of critical live cases on selected changes; broader simulations and judge comparisons periodically; holdout and isolated staging evidence before release. This is a scheduling design; provisioning or running services needs its own request.

Specify staging assertions for capabilities the application actually has: cross-user identity denial, session reload/compaction, adapter schemas and retry contracts, allowed subagent routing and shared limits, and complete request processing. These properties are established on the isolated target; a healthy endpoint or local fake establishes availability. Use deployed-equivalent permissions on isolated targets under the authorised scope.

Pair baseline and candidate by case and fixture, holding criteria and trial counts steady. Report successful/attempted counts and critical slices separately; explain changed measurement definitions. For small differences, use uncertainty methods respecting repeated trials within cases. Use [result-auditing.md](result-auditing.md) for completeness and verdict checks. Preserve failed product trials; bounded infrastructure recovery must retain its failed or incomplete attempts.

Plan observation around allowlisted metadata: opaque trace linkage, versions, tool name, result category, timing, retries, policy decision, usage and final status. Distinguish submission from later business completion. Keep message-content capture disabled by default, including `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS=false` where applicable. Review minimisation, access, retention and export before production excerpts reach fixtures or judges; apply the same policy to CI artifacts and recordings.

**Completion:** each release gate identifies its evidence and failure owner. A production incident becomes a sanitised reproduction, an old-version failure when reproducible, a verified correction and monitored affected slice. Cases that taught the fix are development evidence; fresh reviewed evidence supplies the holdout.
