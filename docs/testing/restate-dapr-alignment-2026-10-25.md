# Restate and Dapr alignment — 25 October 2026

Source note: [comparison](../research/restate-dapr-comparison-2026-10-25.md).

## Changed journeys

`adk-workflow-design`, choosing a durable engine, and
`adk-operational-guardrails`, keeping bounds and approvals under one.

## Fresh-agent trial

A fresh agent with only the skill packages built a stand-in ADK 2.12
refund agent (a `SequentialAgent` root, a token-budget
`after_model_callback`, `max_llm_calls`, a confirmation-gated refund over a
fake payments backend with idempotency keys) and took the ticket: make it
durable with Restate or Dapr and prove the guardrails still hold. It
installed google-adk 2.12.0, pytest and `restate-sdk` 1.1.0, read
`diagrid` 0.5.3 in a separate environment, and wrote a journaling stand-in
for the Restate context; no server or sidecar ran.

Result: Restate, with four changes. The root became an `LlmAgent` (a
`Workflow` also works); a guard plugin listed before Restate admits calls,
caps them, blocks tools once over budget and records usage in
`on_event_callback`; and ADK confirmation was replaced by an operation the
tool submits and a separate durable workflow that waits for the decision
and checks reviewer, payload, expiry and preconditions before the journaled
refund with its key. It declined Dapr (no ADK callbacks, state or
confirmation; size-limited licence), plain resumability, and an awakeable
inside the tool (it holds the object's lock for days and its resolve call
is unauthenticated).

`pytest`: **27 passed**: 4 baseline tests on plain ADK; 6 tests that assert
each breakage with the engine installed (composite root rejected, budget
callback silent, `max_llm_calls=1` letting 2 calls through, confirmation
resume failing, an unwrapped tool refunding twice after a crash, and a
plugin listed before Restate still losing its after-model callback); and 17
for the adapted design (crash replay deduplicated, every bad approval
making zero payment calls, an approval days later refunding once, and the
kill-after-the-write cases).

Ease: 3 of 5.

## Frictions and fixes (same day)

1. "Two engines publish ADK integrations" before a list of four. Fixed.
2. The plugin skips the after-model callbacks of every plugin, not only
   those listed after it (the trial's test; consistent with the 2.12.0
   source and the guardrails skill). Fixed.
3. No alternative for accounting usage, and in-place event mutation is
   dropped. Fixed: `on_event_callback` with assigned fields (the Runner's
   field merge checked in source).
4. No package names or versions. Fixed.
5. The kill-after-the-write test was cited from a skill that never defined
   it. Fixed: defined in `safe-api-tool-calls`, with Restate named.
6. The confirmation failure had no cause or replacement. Fixed: the
   per-invocation tool gate (checked in the plugin source) and a
   submit-then-durable-workflow pattern.
7. No stand-in shape. Fixed.
8. Admission-time budgets still deliver the crossing response. Fixed.
9. Whether the call cap counts across `Workflow` nodes. Not changed:
   unverified.
10. The workflow inspector's exit 3 gave no reason. Fixed, with a test.
11. A contract test pinned to 2.8.0. Not changed: the skill's recorded
    baseline.

## Limits

No Restate server or Dapr sidecar ran; replay and suspension were
simulated by the trial's stand-in.
