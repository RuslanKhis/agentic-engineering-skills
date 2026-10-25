# BIRD Mini-Dev and Spider 2.0 alignment — 25 October 2026

Source note: [comparison](../research/bird-spider2-comparison-2026-10-25.md).

## Changed journey

`adk-sql-agent-engineering`, "Test the public app": the public outcome
oracle and benchmark metrics in `acceptance-and-extensions.md` §1.

## Fresh-agent trial

A fresh agent with only the skill packages built a stand-in ADK 2.12
NL2SQL project (a template route and a generated route over a fake
executor) whose draft `ex()` was set equality and passed a reversed
ranking, then took the ticket: "execution accuracy like BIRD", Soft-F1 and
R-VES, and a Spider 2.0-Lite score using an Owner service-account key. It
installed google-adk 2.12.0 and pytest; no benchmark data, BigQuery or
remote model was used.

Result: an oracle gate (route, status, every metric under frozen aliases,
exact decimals, ranking, cardinality and keys, job evidence, zero jobs for
refusals); BIRD's EX and Soft-F1 kept under their names as diagnostics;
R-VES declined in favour of bytes billed; and a Spider 2.0-Lite module with
an offline comparator, scoring out of 205, a preflight that refuses an
unfilled approval, a non-isolated project, extra roles or any key file, and
a campaign runner through the agent's own bounded executor. It declined
running the benchmark and using the Owner key.

`pytest`: **22 passed**; the acceptance script reported 7 of 7 cases
passing and 5 of 5 negative controls failing as required. The reversed
ranking, the duplicated row and the wrong route each scored BIRD EX 1 and
failed the gate; swapping set equality back in as the gate let them pass.

Ease: 4 of 5.

## Frictions and fixes (same day)

Each fix was checked in the snapshot source before editing.

1. Soft-F1 could not be implemented from the summary. Fixed: the full
   arithmetic, and that position pairing penalises a reversed ranking.
2. R-VES's reward bands were missing. Fixed.
3. Spider2's id routing, tolerance type, column subset and multiple gold
   files were unstated. Fixed: `bq`/`ga` prefixes, absolute 0.01, column
   indices, pass on any gold file.
4. Which denominator to report. Fixed: 205, not 214 or 547.
5. What to do with an existing Owner key, and what role reads public data.
   Fixed: delete the key and record the clean-up; `jobUser` on the
   campaign project.
6. No caps for the campaign. Fixed: per-query ceiling, total byte budget,
   task count and concurrency go in the approval; the values stay the
   project's.
7. The workflow example is labelled 2.8. Fixed: the same shapes ran
   unchanged on 2.12.0.
8. `sqlglot` is not an ADK dependency, so a no-install trial used a regex
   stand-in. Not changed: the skill already requires a dialect parser and
   rejects a regular-expression check.

## Limits

No benchmark, BigQuery or GenAI HTTP run; the trial's Soft-F1 numbers came
from its own implementation.
