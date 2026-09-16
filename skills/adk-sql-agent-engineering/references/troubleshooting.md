# Troubleshooting from observed failures

Use this after locating the failing boundary. Preserve the original input, sanitised response, versions and verdict before changing a checker or repeating work. An uncertain provider outcome requires reconciliation; a new request is not a diagnostic default. For cloud operations use the [lifecycle runbook](lifecycle-runbook.md); for model plumbing use [ADK runtime](adk-runtime.md).

## Find the first broken boundary

Trace one invocation in this order: trusted request → routing → value resolution → selected metadata → author request/response → policy → dry run → query submission/result → formatter → HTTP/browser observation. Record bounded status and call counts at each stage. Stop at the earliest violated contract instead of rewriting prompts to compensate for a downstream failure.

| Symptom | First check | Narrow correction and regression |
| --- | --- | --- |
| Project changed in the UI but requests still fail | Actual process configuration, CLI access, Python ADC, source quota consumer, billing and API visibility independently | Pin the selected target in preflight; a UI selection or installed SDK is not connectivity. Restart configured clients after a project change. |
| Root key changed but chapter still uses old settings | Which `.env` is read, environment precedence, backend and cached settings | Fix only the applicable configuration. The verified Vertex/ADC route required no Gemini API key; an API key alone never supplies BigQuery identity. Never print values. |
| Read-only CLI offers to enable an API | Exact command target/consumer and process prompt settings | Disable prompts **and implicit API activation**; pin `--project` and `--billing-project`. Permission denied or `SERVICE_DISABLED` is unknown state, not an instruction to activate. |
| `--plan` discovers ADC or changes a provider resource | Public command/import path, including package `__init__` | Parse/reject flags before client construction; keep root-agent export lazy. Test the real command with credential/client sentinels and a nonexistent credentials file. |
| Impersonation fails just after scoped IAM grants | Account ownership, bindings, then structured token-mint error | Only the recognised IAM propagation denial merits bounded readiness retry. Stop on service-disabled/quota errors; do not test readiness by repeating paid model/query calls. |
| Setup interrupted or deletion seems stuck | Saved intent, stable job/account identity and authoritative resource state | Resume reconciliation from the journal. Never create a new job or delete a same-named replacement to force progress. |
| Generated path uses more model calls than expected | Actual provider calls across the public workflow, including context summaries/tool loops | Put validated metadata collection in application code; pass the exact result to a tool-free author. Reassert correct rows and refusal behaviour after removing a stage. |
| Author says READY with no SQL | Actual outbound SDK schema and response, not only `model_json_schema()` | Separate wire-required nullable keys from runtime defaults; use the callback and offline wire test. Missing/empty SQL must still stop before any database call. |
| A null-bearing refusal crashes Runner or HTTP | Provider response → ADK output conversion → second Pydantic validation | Runtime nullable fields need defaults in the recorded ADK version. Preserve stricter READY checks rather than making execution accept incomplete candidates. |
| Physical references are unqualified or invented | Context's exact `fully_qualified_name` and the message actually delivered to the author | Pass physical schema metadata verbatim; distinguish logical selectors from physical identifiers. Retain rejection of ungrounded references. |
| `unpaid` resolves to `paid` | Substring matching, reviewed dictionary aliases and negation handling | Match approved words/phrases with boundaries; clarify unsupported negation. Test `unresolved` separately if it is an explicitly approved alias. |
| Whitespace or NaN reaches a query | Normalisation order and numeric validation | Trim before checking length/business values; require finite decimals before binding. Assert zero dry runs and executions for rejected input. |
| A qualified AI/ML call passes the guard | Parsed AST parent/namespace, not just function leaf name | Test fully qualified function forms and nested placements; deny unsupported function/connection capabilities. A short denylist is not a general SQL sandbox. |
| Smoke test says PASS on wrong data | Exact rows/all metrics/ranking and the oracle's independence | Mutate one seeded amount while keeping route/status successful; the public assertion must fail. Status OK and a job ID are insufficient. |
| Correct aggregates fail only because of column names | Explicit equivalence of each alias, every value and required metric | Preserve the failure; add only justified aliases with regression tests and replay the exact saved response. Do not rerun the model until it produces a preferred alias. |
| Browser automation times out after an answer appears | Application/job state and rendered final event versus selector state | Observe again without resubmission. Record an observer failure separately from an application or provider timeout. |
| History survives restart | Model/query counters around reload | Prove history rendering causes no new work. It does not demonstrate semantic follow-ups, result freshness or permission revalidation. |

These signatures came from the September 2026 companion audits. The corrections address recorded cases, not every possible cause of the symptom. The extended policy cases below are implementation recommendations and require target-specific tests.

## SQL policy tests worth preserving

Build candidates through the public executor and instrument the provider boundary. For rejection cases assert both `dry_run_count == 0` and `execution_count == 0`; a returned error after a remote tool already executed is not prevention.

1. Test `AI.GENERATE`, `AI.FORECAST` and `ML.PREDICT` in supported parser positions. SQLGlot 29 represented namespace information on a parent `Dot`; inspecting only an anonymous function's name missed it in the original implementation. Inspect the installed dialect AST and apply the complete permitted-function policy. These three regression names are examples, not an exhaustive policy.
2. Exercise nested CTE scope and shadowing. A globally collected CTE name must not hide an unrelated physical reference in another lexical scope. Validate physical project/dataset/table identities after name resolution; do not blanket-lowercase case-sensitive identities.
3. Exercise disallowed views, external/remote functions, table functions, connections, wildcard/time-travel references and joins according to the supported grammar. Unknown or unresolved constructs stop before submission. A read-only result shape is insufficient.
4. Normalise and validate values before binding. Cover empty-after-trimming strings, hostile quote text, `NaN`, positive/negative infinity, duplicate names, missing/extra SQL parameters, date boundaries and provider precision/range limits. Preserve exact decimals; converting through binary float can hide a mismatch.
5. Compare candidate references with the **retrieved scope for this invocation**. Test another domain that is globally approved and a permitted table that was never retrieved. The companion's domain-wide allowlist alone did not provide this stronger binding.
6. Test missing dry-run estimates, expensive small results, row/byte truncation and uncertain submission. Keep a billing ceiling on the executed job as well as the dry-run gate. A total request deadline and confirmed cancellation require separate implementation.

The companion has recorded offline regression evidence for qualified AI/ML blocking, trimmed inputs, finite numeric parameters and portions of query scope/timeouts. Lexical scope completeness, function/column/join policy, strict parameter inventory, retrieved-scope binding and cumulative budgets remain production extensions; do not claim them by copying a parser function.

## Keep framework failures offline and observable

Before importing the target, substitute the permitted external boundaries and make accidental ADC discovery or network use fail immediately. A test that replaces the entire agent or its serialiser cannot prove the provider wire contract. The optional [contract asset](../assets/test_adk_contract.py) retains those layers and supplies synthetic HTTP responses; it is a starting fixture, not the target's acceptance test.

For a malformed response, incomplete READY or metadata failure, inspect final events through the actual Runner and then HTTP route. Keep user-visible failures sanitised; raw Pydantic errors can include input values. Assert a subsequent valid request still works and no prior question is replayed. Bound model calls and consume the stream through completion, including cleanup in `finally`.

A failed import or missing method can mean an incompatible installed version. Record resolved packages separately from declared ranges. The historical live stack and the new portable asset stack differ; see [compatibility.md](compatibility.md). Do not repair a failed probe by silently changing the project's dependencies, removing assertions or mocking a higher layer.

## Turn a successful generated trace into a reviewed template

This is a **PRODUCTION PRINCIPLE**, not an automated companion feature. Use it when repeated supported questions justify a fast path:

1. Select sanitised, permission-appropriate examples by repeated **meaning**, not by similar words. Trace retention must already be authorised.
2. Have the metric owner settle grain, denominator, currency, reporting interval, joins, ranking/ties and caller restrictions. Generalise only variable values; identifiers remain catalogue-owned.
3. Convert the query into reviewed SQL with typed bound values and a versioned template contract. Parameterise all required user-derived values; keep execution policy and billing/output limits.
4. Compare exact results with an independent oracle on adversarial fixtures and representative permitted data. Check join policy independently of totals.
5. Add router counterexamples: extra filters, negation, new metric, changed period or unsupported cohort must clarify or take another route. Verify the template path skips author/schema calls and preserves final output semantics.
6. Roll out under the project's release process and observe correctness/refusal/routing metrics. Retire or revise the template when source schema or business meaning changes. A previously successful model trace is a candidate for review, not automatic approval.

## Preserve what a result proves

An SDK request-count pass proves a graph property; a database fixture pass proves the asserted answers; an identity probe proves the observed runtime principal; resource absence proves the inspected resources at the recorded time. Keep these separate. The follow-up campaign achieved six correct answers per route but still failed its first-answer responsiveness target. A genuine failed gate stays recorded even when latency is outside the current user's priorities.
