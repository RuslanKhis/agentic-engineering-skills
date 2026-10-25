# Claude and OpenAI cookbooks alignment — 25 October 2026

Source note: [comparison](../research/cookbooks-comparison-2026-10-25.md).

## Changed journeys

`adk-operational-guardrails` with `adk-agent-evaluation`, calibrating
escalation; and `optimise-adk-on-google-cloud`, trimming context under an
explicit cache. One fresh-agent trial each, offline, google-adk 2.12.0.

## Trial 1: escalation

A stand-in expense agent whose rules (travel and legal always escalate,
over 500 needs a manager) lived only in its instruction; the ticket asked
to bring a 60% escalation rate under 10%. The agent moved the rules into
code (a pre-model route and a write-time check that re-reads the stored
claim) and measured missed, over- and raw escalation on 20 labelled claims.

| Variant | Model | Raw | Missed | Over |
| --- | --- | --- | --- | --- |
| rules in code | cautious | 0.60 | 0 | 0.50 |
| rules in code | calibrated | 0.20 | 0 | 0 |
| rules in instruction | approve all | 0.00 | 1.00 | |
| floor lowered to hit 10% | approve all | 0.05 | 0.75 | |

The code floor alone forces 20% of claims to review, so the 10% target is
unreachable without dropping required escalations. Tests: 28 passed for the
gated agent; the instruction-only agent failed 18 and the lowered floor 10.
Ease 3 of 5.

Frictions and fixes:

1. No routing for escalation targets or reviewer fatigue. Fixed.
2. Tool-level checks fire only when the model calls a tool; a do-nothing
   model left a travel claim unrouted. Fixed: a pre-model route.
3. Confirmation versus an existing review queue. Fixed.
4. "Never lower the floor" without "compute the floor share and report an
   unreachable target". Fixed.
5. One strict script across variants. Fixed: a script per variant.
6. On 2.12 the strict model's error arrives wrapped as
   `DynamicNodeFailError`. Fixed (class checked in source).
7. A test helper pinned to 2.8.0. Not changed: it is the skill's own
   recorded baseline.
8. No pytest async guidance. Not changed: the runner is the project's
   choice.
9. A scripted model cannot prove a rate drop. Fixed: NOT RUN until live.
10. Fail closed on unreadable stored fields. Fixed.
11. The inspector ignored `before_agent_callback`. Fixed, with a test.
12. A domain choice, not a skill gap.

## Trial 2: context and cache

A stand-in support agent with a long instruction, 8,000-character tool
records, `ContextCacheConfig` and `ContextFilterPlugin(num_invocations_to_keep=3)`.
The agent ran the real `Gemini` class over a fake client to exercise the
cache manager. Original set-up: the order id vanished from every request
from turn 4, the agent asked for it again on turn 5, and no cache formed
after the window started sliding. Fixed set-up (no filter, long text in
`static_instruction`, the id in state read through the dynamic
instruction, bounded results, token-threshold compaction): the id was in
every request once, the cache served 12 of 14 requests, and synthetic
uncached tokens fell from 37,709 to 14,285. Tests: 10 passed. The skill's
claims about the filter and the cache held exactly on 2.12. Ease 3 of 5.

Frictions and fixes:

1. 2.8.0 file paths. Fixed: the 2.12 locations.
2. `LoadArtifactsTool` plus the bounded-result asset broke the cache:
   the artifact list lands in the system instruction. Fixed (checked in
   source: the routing feature is experimental and off by default).
3. The placement check was wrong for tool continuations. Fixed.
4. How to test the explicit cache offline. Fixed.
5. Split pairs cannot be checked by id at the SDK boundary. Not changed:
   an observation from one trial, not yet read in source.
6. The asset's 20,000-byte default never fires on these records. Fixed.
7. The compaction threshold counts cached tokens. Fixed.
8. No recipe for keeping an authoritative locator. Fixed.
9. `EventsCompactionConfig`'s import path on 2.12. Fixed (checked).
10. What the inspector's 2.8.0 gate means on 2.12. Fixed.
11. Whether the filter counts a dynamic-instruction block as an
    invocation. Not changed: read only, not tested.
12. A confirmation that the filter and cache claims held, not a gap.

## Limits

No live model: real cache hits, provider minimums, summary quality and
whether the model uses the id from the dynamic slot were not measured.
