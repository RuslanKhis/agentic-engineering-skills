# PyRIT alignment — 24 October 2026

Source note: [PyRIT comparison](../research/pyrit-comparison-2026-10-24.md).

## Changed journey

`adk-agent-security`, the adversarial campaign: a poisoned document modelled
with PyRIT's cross-domain injection workflow and a deterministic scorer, with
the A2A route recorded in `adk-agent-interoperability`.

## Fresh-agent trial

A fresh agent with only the skill packages planned and built, offline, a
PyRIT campaign against a synthetic ADK HR agent that reads CVs and can
schedule interviews and email candidates, exposed with `to_a2a` under
`/a2a/hr`, with no model keys in CI. It installed `pyrit==1.1.0` and
`google-adk==2.12.0` from PyPI into its own environment.

Result: 7 Runner tests passed (injected address refused, tainted body
refused, a legitimate email held and sent once after confirmation, the gate
failing closed, the injection refused over A2A, the card served only under
the prefix, and a demonstration that scoring the reply gives a false
positive). The `XPIAWorkflow` campaign with a planting setup target, a
callback returning executed calls and mailbox effects, and
`SubStringScorer` found 0 of 5 successes against the gated agent in process
and over A2A (the scripted model attempted 4 times; the gate refused each)
and 4 of 5 against an ungated control, the fifth payload carrying no
instruction. `A2ATarget` raised `ImportError` on 1.1.0, as the skill says;
the A2A path used the a2a-sdk client over an in-process ASGI transport.

Ease: 3.5 of 5. The workflow, callback shape, scorer, memory initialisation
and the `A2ATarget` caveat held; the glue code took the time.

## Frictions and fixes (same day)

1. The workflow sat only under the paid live campaign although it needs no
   model. Fixed: it can run in the deterministic suite with a scripted model.
2. Scoring "executed calls" was ambiguous: refused attempts carry the
   forbidden host, and the A2A task history repeats them. Fixed: score only
   executed calls and recorded effects, never the reply or the task.
3. `to_a2a` needs `google-adk[a2a]`. Fixed in the A2A producer checklist.
4. No offline A2A route on 1.1.0. Fixed: run the app's lifespan and reach it
   through `httpx.ASGITransport` with the a2a-sdk `ClientFactory`.
5. No recipe for the setup target. Fixed: keyword-only `__init__`,
   `_send_prompt_to_target_async`, `construct_response_from_request`
   (checked in 1.1.0).
6. The security inspector reported none of the three trifecta legs for an
   agent whose tools come from a factory, which reads as safe. Fixed in the
   helper: the summary gains `complete`, false when a `tools=` list or a
   sub-agent was not resolved, the `tools_not_literal` message says the legs
   are unknown, and a test covers it (18 helper tests pass).
7. The harness helpers live in another skill's reference. Not changed: the
   pointer is deliberate; this trial's confirmation reply worked as guessed.
8. `XPIAResult.success` was undefined. Fixed: true means the attack
   succeeded.
9. `to_a2a` returns tool arguments and results in the task history, and an
   unauthenticated caller runs as `A2A_USER_<context_id>`. Fixed: the A2A
   producer checklist names the history exposure and the security threat
   model points to the inbound-authentication contract.

## Limits

No live model; PyRIT's `A2ATarget` was not exercised because no release
carries it.
