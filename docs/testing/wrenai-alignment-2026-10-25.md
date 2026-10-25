# WrenAI alignment — 25 October 2026

Source note: [comparison](../research/wrenai-comparison-2026-10-25.md).

## Changed journey

`adk-sql-agent-engineering`, defining the semantic map ("Define metrics,
joins, values or selected context") and the read-only execution check.

## Fresh-agent trial

A fresh agent with only the skill packages built a stand-in ADK 2.12 SQL
project (a dict semantic map, a collector that expands a derived table's SQL
into the candidate, a sqlglot read-only policy and a `Workflow`), then took
the ticket: move the map to YAML files in WrenAI's layout, run `wren context
validate` in CI, and save every successful query as an example. It
installed google-adk 2.12.0, sqlglot, PyYAML and pytest, and the published
`wrenai` 0.16.0 in a separate environment; no network or BigQuery was used.

Result: the map in WrenAI's MDL layout with domains and metrics in a file of
its own; a CI check that fails on every finding (join type and condition,
known join columns, the "one" side on its primary key, qualification, stored
SQL under the read-only policy, metric columns, domain scope, examples);
drift comparison in the collector; a scheduled duplicate-key check; and
examples written as pending candidates and promoted by a reviewer. It
declined auto-saving examples into prompts, Wren as gate or runtime, and a
uniqueness query per request.

`pytest`: **48 passed, 0 failed**, 39 of them negative or adversarial (17
broken semantic trees, 3 drifts, a metadata outage, a duplicated key, 4 bad
derived-SQL definitions with zero jobs, 4 workflow rejections, 8 example
cases). Run over the same 17 broken trees, `wren context validate` caught 2
by default and 5 with `--strict`.

Ease: 3 of 5.

## Frictions and fixes (same day)

1. No route for saving queries as examples, and no warning about
   poisoning or leakage between users. Fixed: a routing row and a rule in
   troubleshooting.
2. "Adopt the file shape, not the tool" against a ticket naming the tool,
   and no description of the shape. Fixed: the layout named, and Wren's
   validator allowed beside the gate, never as it.
3. Wren accepted more than the skill said. Fixed with the trial's observed
   counts and cases.
4. No home for domains and metrics. Fixed.
5. Where the duplicate-key check runs. Fixed: on a schedule, with a CI
   fixture.
6. No definition of drift; legacy BigQuery type names would raise false
   drift. Fixed.
7. "Missing key" was ambiguous. Fixed: the table's primary key, and the
   "one" side must join on it.
8. The host-to-node sentence was vague for 2.12. Fixed: the two context
   fields the trial used, which identify the request but carry no scope.
9. `inspect_project.py` listed an unpacked wheel. Not changed: it lists
   project files for inspection and its findings are leads, as the skill
   says.
10. No mapping from Wren's `join_type` to cardinality, or rule for
    many-to-many. Fixed.
11. No Python floor for ADK 2.x. Fixed: 3.11, from the package metadata.

## Limits

No BigQuery, GenAI HTTP serialisation or hosted CI run.
