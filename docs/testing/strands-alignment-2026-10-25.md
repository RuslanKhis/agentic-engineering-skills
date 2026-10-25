# Strands alignment — 25 October 2026

Source note: [comparison](../research/strands-comparison-2026-10-25.md).

## Changed journey

`adk-agent-evaluation`, fault injection and resilience scoring.

## Fresh-agent trial

A fresh agent with only the skill packages built a stand-in ADK 2.12 claims
agent (`lookup_policy` read, `file_claim` write over fake backends) and
designed offline and live tests for a slow (40 s), empty, corrupted and 503
`lookup_policy`. It installed google-adk 2.12.0 and pytest; no network or
model was used.

Result: a strict scripted model; one fault per case beside a no-fault twin,
injected both through ADK's Environment Simulation (the real tool never
runs) and through a backend double (the real tool runs); deterministic
graders for fault fired (else NOT RUN), end state, honesty, recovery
discipline and usage against the twin; an opt-in live driver with unbiased
pass^k and a live plan checked against the installed config model. The 40 s
delay was never waited: the engine's sleep was recorded, or cut by a
deadline.

`pytest`: **33 passed**, twice, with the network blocked. Built-in bad
agents were all caught (filing on corrupted data, a retry storm, a retry
after a permanent failure, an invented limit, a do-nothing agent, an
injection naming the wrong tool, an extra model call). Six deliberate code
breaks, each in a fresh copy: **6 of 6 caught**.

Ease: 4 of 5.

## Frictions and fixes (same day)

1. How to avoid the real sleep, and that it runs in the before-tool
   callback where a tool deadline cannot cut it. Fixed (checked in 2.12.0
   source).
2. Whether a slow call cut off by a deadline counts as fired. Fixed.
3. A designed static stop read as an abnormal end scoring zero. Fixed.
4. "A sharp rise is a retry storm" had no threshold, and a ratio missed a
   four-retry storm. Fixed: count calls to the faulted tool by error class
   against the bound; usage is a diagnostic.
5. No retry bound in the project. Fixed: that is a finding for
   `safe-api-tool-calls`.
6. "CORRUPTED" as a sentinel collides with honest prose. Fixed: a token
   honest text cannot contain.
7. Which expected effects partial completion counts. Fixed: those the case
   expects under the fault.
8. Checking "says what could not be done" without a judge. Fixed: a
   structured status, or a calibrated pinned judge.
9. No routing entry for a flaky tool. Fixed.
10. No per-case hook in `AgentEvaluator`. Fixed: run the matrix in your own
    harness.
11. The injected error shape and the experimental warning. Fixed (checked
    in source).
12. Unit-testing a tool body without a real `ToolContext`. Not changed: the
    deterministic-tests reference already keeps tools callable apart from
    the agent; a stub's adequacy depends on the tool.

## Limits

No live run; the honesty regex and thresholds are the trial's own.
