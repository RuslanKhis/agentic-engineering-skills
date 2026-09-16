# Validation by boundary

Use the target project's runner and existing virtual environment. The bundled helpers need Python 3.11 or later and only the standard library; `pytest` can run their `unittest` tests. All ordinary tests must remain offline. Mark every provider substitute explicitly.

The optional [ADK contract asset](../assets/test_adk_contract.py) exercises real framework/SDK serialisation with synthetic HTTP responses; read [adk-runtime.md](adk-runtime.md) before running or adapting it. It has separate dependencies and does not import the target application. Use [acceptance-and-extensions.md](acceptance-and-extensions.md) for target-level Runner/HTTP/browser checks and [semantic-contracts.md](semantic-contracts.md) for adversarial data fixtures. Passing the asset does not establish that the target is wired correctly.

## Minimum useful cases

| Boundary | Positive case | Negative case and observable outcome |
| --- | --- | --- |
| Router | Full approved template intent | Extra filter, negation or changed metric is not silently sent to that template |
| Template | Bound values give expected rows | Hostile value remains data; no SQL-structure interpolation |
| Context | Only the selected authorised schemas reach the author | Unknown/cross-scope/ambiguous selection or metadata failure causes zero author and query calls |
| Author | Actual SDK payload carries required fields | Null refusal round-trips; incomplete READY cannot reach the database |
| SQL execution | Allowed query with expected job settings | DML/DDL, multiple statements, scope escape and disallowed functions cause zero job submissions |
| Meaning | Independent fixture establishes grain, dates and each metric | Repeated facts, zero-activity entities, nulls and boundary dates expose changed answers |
| Resource bounds | Accepted estimate and bounded output | Cost rejection, deadline, uncertain submission and partial rows produce the appropriate controlled result |
| Workflow | Final useful result through public Runner/HTTP | Refusal has no dry run or query; intermediate candidate is not the final answer |
| Repetition | Second invocation preserves intended state | Setup creates no duplicate loads/grants; repair/retry does not repeat uncertain execution |

Add tests for the production controls actually being implemented: caller scope, exact retrieved-schema binding, nested CTE resolution, strict parameters, cumulative deadlines, result completeness, cache isolation or follow-up intent. A missing implementation should be reported, not covered by a test that simply repeats the specification.

Measure model, metadata and query counts independently. Scripted model responses can prove the application graph and refusal flow; they cannot prove model quality. SQLite can validate selected fixture arithmetic; it cannot establish BigQuery dialect, IAM, partition enforcement, billing or service latency. Use the real framework/SDK serializer with an HTTP double for schema compatibility checks.

## Aggregate result checker

The checker adapts the tested lesson that explicitly equivalent aliases may differ while numerical answers must remain exact. Provide two local JSON files with synthetic or approved sanitised data.

Expected contract:

```json
{
  "key_columns": ["cohort"],
  "metrics": {
    "client_count": ["client_count", "total_clients"],
    "ticket_count": ["ticket_count", "total_tickets"],
    "tickets_per_client": ["tickets_per_client", "avg_tickets_per_client"]
  },
  "rows": [
    {"cohort": "Churned", "client_count": 1, "ticket_count": 3, "tickets_per_client": 3},
    {"cohort": "Renewed", "client_count": 2, "ticket_count": 3, "tickets_per_client": 1.5}
  ]
}
```

Actual result:

```json
{
  "rows": [
    {"cohort": "Renewed", "total_clients": 2, "total_tickets": 3, "avg_tickets_per_client": "1.5"},
    {"cohort": "Churned", "total_clients": 1, "total_tickets": 3, "avg_tickets_per_client": "3.0"}
  ]
}
```

Invoke `scripts/check_results.py --expected expected.json --actual actual.json` using the installed skill's script path and the target interpreter. `--help` is authoritative for supported flags; `--dry-run` validates input shapes and within-row alias consistency but returns no cross-result correctness verdict. Both modes are read-only. Exit 0 means PASS or labelled DRY_RUN, 1 means a mismatch, and 2 means invalid input. Ordinary inspection needs no credentials.

The checker requires exact finite decimals, all expected metrics and matching unique cohort keys. It rejects conflicting aliases and duplicate JSON keys. Actual-row nonmetric extras are ignored. It deliberately does not infer semantic equivalence, compare row order, validate dimensions outside the configured keys, establish job evidence or check SQL safety. For rankings, assert order independently. For empty expected results, add a project-specific assertion rather than weakening this aggregate contract.

Freeze expected values and the alias contract before evaluating new model samples. If a checker defect is found, preserve the original verdict, amend only justified equivalence rules, add a regression, and replay the exact saved response. Do not resample until an answer passes or silently loosen numerical comparisons.

## Approved live campaign

Only after explicit scoped approval, use a disposable target, agreed cost/time/call limits and recorded ownership. Verify prerequisites and fixture answers before paying for a model answer. Exercise a reviewed route, generated route and unsupported request through the actual user-facing entry point; record genuine model/query evidence and exact data assertions without exposing secrets or customer data.

Count diagnostics separately from acceptance samples. Preserve failures and sample sizes. Record model, endpoint, package versions, cold/warm definition, measurement boundary and both time to meaningful answer and final completion when measuring latency. A spinner does not count. Small samples warrant ranges/medians, not SLA or percentile claims. Verify cleanup separately and report retained provider history or resources precisely.

## Report format

For each changed boundary, report the relevant files, command, exit status, assertion and evidence class. Then list absent prerequisites and untested claims. Use these labels consistently:

- **LIVE VERIFIED:** real service exercised in the named environment and bounded sample.
- **OFFLINE VERIFIED:** local execution, with each model/database/HTTP substitute named.
- **NOT RUN:** no evidence for this run; explain the missing prerequisite or scope.
- **PRODUCTION PRINCIPLE:** recommended design requiring target-specific implementation and validation.

Valid skill Markdown alone does not establish agent behaviour. Forward-test greenfield implementation, adaptation of custom code, missing prerequisites, an approval-bound operation, a near-miss request and a repeat invocation. Give independent evaluators only the skill, fixture and realistic request; inspect their actual changes and results.
